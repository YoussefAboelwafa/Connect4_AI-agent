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
