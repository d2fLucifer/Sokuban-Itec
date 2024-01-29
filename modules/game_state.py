"""
Sokuban game state class
The state of the game consists the map which is a 2D array of characters. There are 6 types of characters:
- ' ': empty space
- '#': wall
- '$': box
- '.': target
- '@': player
- '+': player on target
- '*': box on target
The game state class keeps track of the map.
The game state also keeps track of the player and box positions, and whether the game is solved or not.
The game state class has the following methods:
- find_player(): find the player in the map and return its position
- find_boxes(): find all the boxes in the map and return their positions
- find_targets(): find all the targets in the map and return their positions  
- generate_next_state(direction): generate the next game state by moving the player to the given direction
- check_solved(): check if the game is solved
"""


class GameState:
    def __init__(self, map, current_cost=0):
        self.map = map
        self.current_cost = current_cost
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()

    def find_player(self):
        """Find the player in the map and return its position"""
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] in ('@', '+'):
                    return (i, j)
        return None

    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes = []
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] in ('$', '*'):
                    boxes.append((i, j))
        return boxes

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        targets = []
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] in ('.', '*'):
                    targets.append((i, j))
        return targets

    def is_wall(self, position):
        """Check if the given position is a wall"""
        return self.map[position[0]][position[1]] == '#'

    def is_box(self, position):
        """Check if the given position is a box"""
        return self.map[position[0]][position[1]] in ('$', '*')

    def is_target(self, position):
        """Check if the given position is a target"""
        return self.map[position[0]][position[1]] in ('.', '*')

    def is_empty(self, position):
        """Check if the given position is empty"""
        return self.map[position[0]][position[1]] == ' '

    def get_heuristic(self):
        """Get the heuristic for the game state"""
        heuristic = 0
        for box in self.boxes:
            min_distance = min(
                [abs(box[0] - target[0]) + abs(box[1] - target[1]) for target in self.targets])
            heuristic += min_distance
        return heuristic

    def get_total_cost(self):
        """Get the cost for the game state"""
        return self.current_cost + self.get_heuristic()

    def get_current_cost(self):
        """Get the current cost for the game state"""
        return self.current_cost

    def move(self, direction):
        """Generate the next game state by moving the player to the given direction"""
        row, col = self.player
        new_row, new_col = row, col

        if direction == 'U':
            new_row -= 1
        elif direction == 'D':
            new_row += 1
        elif direction == 'L':
            new_col -= 1
        elif direction == 'R':
            new_col += 1

        if self.is_wall((new_row, new_col)):
            return self  # Cannot move into a wall

        if self.is_box((new_row, new_col)):
            # Check if the box can be pushed
            box_new_row, box_new_col = new_row, new_col
            if direction == 'U':
                box_new_row -= 1
            elif direction == 'D':
                box_new_row += 1
            elif direction == 'L':
                box_new_col -= 1
            elif direction == 'R':
                box_new_col += 1

            if self.is_wall((box_new_row, box_new_col)) or self.is_box((box_new_row, box_new_col)):
                return self  # Cannot push the box into a wall or another box

            # Move the box
            self.map[new_row][new_col], self.map[box_new_row][box_new_col] = self.map[box_new_row][box_new_col], self.map[new_row][new_col]
            self.boxes.remove((new_row, new_col))
            self.boxes.append((box_new_row, box_new_col))

        # Move the player
        self.map[row][col], self.map[new_row][new_col] = self.map[new_row][new_col], self.map[row][col]
        self.player = (new_row, new_col)
        self.current_cost += 1
        self.is_solved = self.check_solved()
        return self

    def check_solved(self):
        """Check if the game is solved"""
        return all(self.map[target[0]][target[1]] in ('$', '*') for target in self.targets)
