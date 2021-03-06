from operator import itemgetter
from LocalFileProgram import parse_csv


class Bid():
    def __init__(self, bid):
        self.bid_id = int(bid["AuctionID"])
        self.title = bid["AuctionTitle"]
        self.fund = bid["Fund"]
        self.amount = bid["AuctionFeeTotal"]


class Node():
    def __init__(self, bid):
        self.right = None
        self.left = None
        self.bid = bid


# Count created for the purpose of testing in its current state.
# from the CSV file.
class BinarySearchTree():
    def __init__(self):
        self.root = None
        self.node_count = 0

    def load_bids(self, csv_path):
        print("Loading CSV file...")
        list_bids = parse_csv.open_file(csv_path)

        # Sorting the entries taken in from the CSV file so that the BST is balanced. This results
        # in the most efficient traversal of the BST when searching or deleting an entry.
        sorted_list = sorted(list_bids, key=itemgetter("AuctionID"))
        start = 0
        end = len(sorted_list) - 1
        print("%s files loaded..." % len(sorted_list))

        try:
            self.root = self.create_tree(sorted_list, start, end)
            print("Loading Complete...")
        except IOError:
            print("An error occurred when trying to read the file")

    # Recursive function below handles the creation of the BST. This is called in the load_bids function
    # directly above. We will also handle a count for node numbers in this function.  
    def create_tree(self, bid_list, start, end):
        if start > end:
            return None

        # Code below sets the root as the middle most bid based on ID values. This process creates a balanced tree
        # making the most efficient traversal.
        try:
            self.node_count += 1
            midpoint = int((start + end) / 2)
            root = Node(Bid(bid_list[midpoint]))
            root.left = self.create_tree(bid_list, start, midpoint - 1)
            root.right = self.create_tree(bid_list, midpoint + 1, end)

            return root
        except:
            print("Out of bounds thrown. Midpoint is %s and end is %s" % (midpoint, end))

    def display_all_bids(self, node):
        if node is not None:
            self.display_all_bids(node.left)
            parse_csv.print_bid(node.bid)
            self.display_all_bids(node.right)

    def search_tree(self, search_bid):
        if self.root is None:
            print("No file loaded...")
            return
        current_node = self.root
        found = False
        while not found:
            # This is statement handles if a bid has been deleted.
            if current_node.bid is None:
                return None
            if search_bid == current_node.bid.bid_id:
                return current_node
            elif search_bid < current_node.bid.bid_id:
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node is None:
                return None

    # Method used in delete_bid 
    def minimum_value_bid(self, bid):
        current_bid = bid
        while current_bid.left is not None:
            current_bid = current_bid.left

        return current_bid

    # This function runs in check_bid_for_deletion method.    
    def delete_bid(self, bid, bid_id):
        # Setting up base case
        if bid is None:
            return None

        # If bid_id passed in is smaller than root.
        if bid_id < bid.bid.bid_id:
            bid.left = self.delete_bid(bid.left, bid_id)
        # If bid_id passed in is larger than root.
        elif bid_id > bid.bid.bid_id:
            bid.right = self.delete_bid(bid.right, bid_id)
        # If bid_id matches the bid_id of the bid passed into the function
        else:
            # Two conditions handle if there is one or no children nodes to the root
            if bid.left is None:
                temp = bid.right
                bid = None
                return temp
            elif bid.right is None:
                temp = bid.left
                bid = None
                return temp

            # if there are two children, the following code traverses the code to
            # the smallest successor

            temp = self.minimum_value_bid(bid.right)

            bid.bid = temp.bid
            bid.right = self.delete_bid(bid.right, temp.bid.bid_id)
        return bid
