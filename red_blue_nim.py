import sys
import math

class Node:
    def __init__(self, move, num_red, num_blue, depth=10, maxPlayer=True):
        self.move = move
        self.num_red = num_red
        self.num_blue = num_blue
        self.maxPlayer = maxPlayer
        self.depth = depth

    def info(self):
        print(self.num_red, self.num_blue, self.maxPlayer)

    def play_conditions(self):
        if self.num_red > 0 and self.num_blue > 0:
            return True
        else:
            return False

    def generate_children(self):
        children = []
        if self.num_red > 0:
            for red_move in range(1, min(self.num_red, 2) + 1):
                child = Node(
                    move=(red_move, 0),  # Only red pile is chosen
                    num_red=self.num_red - red_move,
                    num_blue=self.num_blue,
                    maxPlayer=False,
                )
                child.parent = self
                children.append(child)
        if self.num_blue > 0:
            for blue_move in range(1, min(self.num_blue, 2) + 1):
                child = Node(
                    move=(0, blue_move),  # Only blue pile is chosen
                    num_red=self.num_red,
                    num_blue=self.num_blue - blue_move,
                    maxPlayer=False,
                )
                child.parent = self
                children.append(child)
        self.children = children
        return self.children

    def get_score_standard(self):
        if self.depth == 0:
            if self.maxPlayer:
                return self.num_red * 2 + self.num_blue * 3
            else:
                return -(self.num_red * 2 + self.num_blue * 3)
        return self.num_red * 2 + self.num_blue * 3

    def get_score_misere(self):
        if self.depth == 0:
            if self.maxPlayer:
                return -(self.num_red * 2 + self.num_blue * 3)
            else:
                return self.num_red * 2 + self.num_blue * 3
        return -(self.num_red * 2 + self.num_blue * 3)

def display(num_red, num_blue, turn):
    s = f"\nTurn: {turn}\n"
    s += f"Current stack:\n"
    s += f"Red Marbles:  {num_red}\n"
    s += f"Blue Marbles: {num_blue}\n"
    print(s)

def print_winner_misere(winner, num_red, num_blue):
    print(winner)
    s = f"\n\n"
    s += f"################################################\n"
    s += f"WINNER: {winner:>14} \n"
    s += f"Red marbles:  {num_red:<7}\n"
    s += f"Blue marbles: {num_blue:<7}\n"
    s += f"They win by:  {num_red*2 + num_blue*3:<7} points\n"
    s += f"################################################\n"
    print(s)

def print_winner_standard(winner, num_red, num_blue):
    s = f"\n\n"
    s += f"################################################\n"
    s += f"WINNER: {winner:>14} \n"
    s += f"Red marbles:  {num_red:<7}\n"
    s += f"Blue marbles: {num_blue:<7}\n"
    s += f"They win by :  {num_red*2 + num_blue*3:<7} points\n"
    s += f"################################################\n"
    print(s)

def minimax_misere(node, depth, alpha, beta, maxPlayer):
    if depth == 0 or not node.play_conditions():
        return node.get_score_misere()
    if maxPlayer:
        maxValue = -math.inf
        for child in node.generate_children():
            child.value = minimax_misere(child, depth-1, alpha, beta, maxPlayer=False)
            maxValue = max(maxValue, child.value)
            alpha = max(alpha, child.value)
            if beta <= alpha:
                break
        return maxValue
    else:
        minValue = math.inf
        for child in node.generate_children():
            child.value = minimax_misere(child, depth-1, alpha, beta, maxPlayer=True)
            minValue = min(minValue, child.value)
            beta = min(beta, child.value)
            if beta <= alpha:
                break
        return minValue

def minimax_standard(node, depth, alpha, beta, maxPlayer):
    if depth == 0 or not node.play_conditions():
        return node.get_score_standard()
    if maxPlayer:
        maxValue = -math.inf
        for child in node.generate_children():
            child.value = minimax_standard(child, depth-1, alpha, beta, maxPlayer=False)
            maxValue = max(maxValue, child.value)
            alpha = max(alpha, child.value)
            if beta <= alpha:
                break
        return maxValue
    else:
        minValue = math.inf
        for child in node.generate_children():
            child.value = minimax_standard(child, depth-1, alpha, beta, maxPlayer=True)
            minValue = min(minValue, child.value)
            beta = min(beta, child.value)
            if beta <= alpha:
                break
        return minValue

def minimax_init_misere(num_red, num_blue, depth):
    rootNode = Node(move='root', depth=depth, num_red=num_red, num_blue=num_blue, maxPlayer=True)
    minmax_val = minimax_misere(rootNode, depth, alpha=-math.inf, beta=math.inf, maxPlayer=True)
    for child in rootNode.children:
        if child.value == minmax_val:
            move = child.move
    return move

def minimax_init_standard(num_red, num_blue, depth):
    rootNode = Node(move='root', depth=depth, num_red=num_red, num_blue=num_blue, maxPlayer=True)
    minmax_val = minimax_standard(rootNode, depth, alpha=-math.inf, beta=math.inf, maxPlayer=True)
    for child in rootNode.children:
        if child.value == minmax_val:
            move = child.move
    return move

def caller_function(num_red, num_blue, first_player, depth, is_misere):
    display(num_red, num_blue, first_player)
    while num_red != 0 and num_blue != 0:
        if first_player == 'human':
            pile_choice = input("Choose a pile (red/blue): ").lower()
            while pile_choice not in ['red', 'blue']:
                pile_choice = input("Invalid choice. Choose a pile (red/blue): ").lower()
            
            if pile_choice == 'red':
                move = int(input(f"Enter number of red marbles to remove (1 or 2, max {num_red}): "))
                while move not in [1, 2] or move > num_red:
                    move = int(input(f"Invalid input. Enter number of red marbles to remove (1 or 2, max {num_red}): "))
                num_red -= move
                num_blue -= 0
            else:
                move = int(input(f"Enter number of blue marbles to remove (1 or 2, max {num_blue}): "))
                while move not in [1, 2] or move > num_blue:
                    move = int(input(f"Invalid input. Enter number of blue marbles to remove (1 or 2, max {num_blue}): "))
                num_red -= 0
                num_blue -= move
        else:
            if is_misere:
                move = minimax_init_misere(num_red, num_blue, depth)
            else:
                move = minimax_init_standard(num_red, num_blue, depth)
            print(f"Move Chosen: {move}")
            num_red -= move[0]
            num_blue -= move[1]

        if first_player == 'human':
            first_player = 'computer'
        else:
            first_player = 'human'
            
        display(num_red, num_blue, first_player)

    winner = 'computer' if first_player == 'human' else 'human'
    if is_misere:
        print_winner_misere(winner, num_red, num_blue)
    else:
        print_winner_standard(winner, num_red, num_blue)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        num_red, num_blue = int(sys.argv[1]), int(sys.argv[2])
        version = sys.argv[3] if len(sys.argv) > 3 else 'standard'
        first_player = sys.argv[4] if len(sys.argv) > 4 else 'computer'
        depth = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        is_misere = version != 'standard'
        caller_function(num_red, num_blue, first_player, depth, is_misere)
    else:
        print("Usage: red_blue_nim.py <num-red> <num-blue> <version> <first-player> <depth>")

