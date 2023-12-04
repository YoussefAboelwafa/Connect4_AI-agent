# # Inside the ConnectFour class
class TreeNode:
    def __init__(self, board, value, parent=None):
        self.board = board
        self.value = value
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_board(self):
        return self.board
    def get_val(self):
        return self.value

        

    
# # def print_tree(tree, indent=0):
# #     state=list(tree.keys())[0]
    
# #     print("    " * indent + f"{state} | Depth: {tree[state]['depth']}, Piece: {tree[state]['piece']}, Value: {tree[state]['value']}")
# #     childs=tree[state]['childs']
# #     for child in childs:
# #         print_tree(child,indent+1)

# def print_tree(tree,indent=0):
#     print("     "*indent,tree.get_board(),tree.get_val())
#     for child in tree.children:
#         print_tree(child,indent+1)
# def main():
#     root=convert_state_to_tree(state)
#     print(root)
#     print_tree(root)
# if __name__ == '__main__':
#     main()
    
    
