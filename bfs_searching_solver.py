import random
import copy

class LightsOutPuzzle(object):
    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        if row >= 0 and col >= 0:
            max_nth_row, max_nth_col = len(self.board)-1, len(self.board[0][:])-1
            self.board[row][col] = not self.board[row][col]
            if row-1 >= 0:
                self.board[row-1][col] = not self.board[row-1][col]
            if row+1 <= max_nth_row:
                self.board[row+1][col] = not self.board[row+1][col]
            if col-1 >= 0:
                self.board[row][col-1] = not self.board[row][col-1]
            if col+1 <= max_nth_col:
                self.board[row][col+1] = not self.board[row][col+1]

    def scramble(self):
        rows, cols, = len(self.board), len(self.board[0][:])
        for r in range(rows):
            for c in range(cols):
                if random.random() < 0.5:
                    self.perform_move(r, c)

    def is_solved(self):
        rows, cols, = len(self.board), len(self.board[0][:])
        for r in range(rows):
            for c in range(cols):
                if self.board[r][c]:
                    return False
        return True

    def copy(self):
        board_copy = copy.deepcopy(self.board)
        return LightsOutPuzzle(board_copy)

    def successors(self):
        rows, cols, = len(self.board), len(self.board[0][:])
        for r in range(rows):
            for c in range(cols):
                successors = self.copy()   # board won't change
                successors.perform_move(r, c)
                yield ((r, c), successors)

    def find_solution(self):
        if self.is_solved():
            return []
        sol_list = []
        visited_node = {}
        frontier = [self]
        while True:
            if len(frontier) == 0:
                return None
            parent_node = frontier.pop(0)
            for move, children_node in parent_node.successors():
                children_node_key = tuple(tuple(element) for element in children_node.board)
                if children_node_key not in visited_node:
                    visited_node[children_node_key] = [move]
                    if children_node.is_solved():
                        while self.board != children_node.board:
                            temp_children_node_key = tuple(tuple(element) for element in children_node.get_board())
                            move_list = visited_node[temp_children_node_key]
                            sol_list = sol_list + move_list
                            children_node.perform_move(move_list[0][0], move_list[0][1])
                        return list(reversed(sol_list))
                else:
                    continue
                frontier.append(children_node)


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for c in range(cols)]for r in range(rows)])
