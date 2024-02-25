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

import numpy as np

class GameState:
    def __init__(self, map, current_cost=0, parent=None):
        self.map = map
        self.current_cost = current_cost
        self.parent = parent
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes_and_targets('$', '*')
        self.targets = self.find_boxes_and_targets('.', '*')
        self.is_solved = self.check_solved()
        self.solution_path = []

        # 1. Precompute derived properties
        self.walls = {(row, col) for row in range(self.height) for col in range(self.width) if self.is_wall((row, col))}
        self.box_positions = set(self.boxes + self.targets)

    def __lt__(self, other):
        return self.get_total_cost() < other.get_total_cost()

    def find_player(self):
        for row in range(self.height):
            for col in range(self.width):
                cell = self.map[row][col]
                if cell in ['@', '+']:
                    return row, col

    def find_boxes_and_targets(self, symbol1, symbol2):
        boxes_and_targets = []
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] in [symbol1, symbol2]:
                    boxes_and_targets.append((row, col))
        return boxes_and_targets

    def is_wall(self, position):
        row, col = position
        return self.map[row][col] == '#'

    def is_box(self, position):
        row, col = position
        return self.map[row][col] in ['$', '*']

    def is_target(self, position):
        row, col = position
        return self.map[row][col] in ['.', '*']

    def is_empty(self, position):
        row, col = position
        return self.map[row][col] in [' ', '.']

    def is_box_on_target(self, position):
        row, col = position
        return self.map[row][col] == '*'

    def is_box_in_corner(self, new_player_position, new_box_position):
        player_row, player_col = new_player_position
        box_row, box_col = new_box_position

        # Check if the box is in a corner relative to the player's new position
        return (player_row + box_row) % 2 == 0 and (player_col + box_col) % 2 == 0


    def get_heuristic(self):
        box_target_distances = [
            min(abs(box[0] - target[0]) + abs(box[1] - target[1]) for target in self.targets)
            for box in self.boxes
        ]
        return sum(box_target_distances)


    def get_total_cost(self):
        return self.current_cost + self.get_heuristic()

    def is_valid_move(self, new_player_position, new_box_position=None):
        new_row, new_col = new_player_position

        if not (0 <= new_row < self.height and 0 <= new_col < self.width and (new_row, new_col) not in self.walls):
            return False

        if (new_row, new_col) in self.boxes:
            if new_box_position is None:
                return False
            new_box_row, new_box_col = new_box_position

            if not (0 <= new_box_row < self.height and 0 <= new_box_col < self.width and (new_box_row, new_box_col) not in self.walls):
                return False

            if (new_box_row, new_box_col) in self.boxes:
                return False

            if self.is_box_in_corner((new_row, new_col), (new_box_row, new_box_col)):
                return False

        return True

    def get_current_cost(self):
        return self.current_cost

    def get_possible_moves(self):
        possible_moves = []
        directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

        for direction, (dr, dc) in directions.items():
            new_player_position = (self.player[0] + dr, self.player[1] + dc)
            new_box_position = None

            if not (0 <= new_player_position[0] < self.height and 0 <= new_player_position[1] < self.width and new_player_position not in self.walls):
                continue

            if new_player_position in self.boxes:
                new_box_position = (new_player_position[0] + dr, new_player_position[1] + dc)

                if not (0 <= new_box_position[0] < self.height and 0 <= new_box_position[1] < self.width and new_box_position not in self.walls and new_box_position not in self.boxes):
                    continue

                if self.is_box_in_corner(new_player_position, new_box_position):
                    continue

            possible_moves.append((direction, new_player_position, new_box_position))

        return possible_moves


    def move(self, direction):
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

        new_game_state = self.clone()
        if new_game_state.is_empty((new_row, new_col)):
            new_game_state.map[row][col] = '.' if (row, col) in new_game_state.targets else ' '
            new_game_state.map[new_row][new_col] = '@' if new_game_state.map[new_row][new_col] == ' ' else '+'
            new_game_state.player = (new_row, new_col)
            new_game_state.current_cost += 1

        elif new_game_state.is_box((new_row, new_col)):
            new_box_row, new_box_col = new_row, new_col

            if direction == 'U':
                new_box_row -= 1
            elif direction == 'D':
                new_box_row += 1
            elif direction == 'L':
                new_box_col -= 1
            elif direction == 'R':
                new_box_col += 1

            if new_game_state.is_empty((new_box_row, new_box_col)):
                new_game_state.map[row][col] = '.' if (row, col) in new_game_state.targets else ' '
                new_game_state.map[new_row][new_col] = '@' if new_game_state.map[new_row][new_col] == ' ' else '+'
                new_game_state.map[new_box_row][new_box_col] = '$' if new_game_state.map[new_box_row][new_box_col] == ' ' else '*'
                new_game_state.player = (new_row, new_col)
                new_game_state.boxes.remove((new_row, new_col))
                new_game_state.boxes.append((new_box_row, new_box_col))
                new_game_state.current_cost += 1

        return new_game_state

    def clone(self):
        cloned_map = [row[:] for row in self.map]
        cloned_state = GameState(cloned_map, self.current_cost, self.parent)
        cloned_state.height = self.height
        cloned_state.width = self.width
        cloned_state.player = self.player
        cloned_state.boxes = self.boxes[:]
        cloned_state.targets = self.targets[:]
        cloned_state.is_solved = self.is_solved
        cloned_state.solution_path = self.solution_path[:]
        return cloned_state

    def check_solved(self):
        return all(box in self.targets for box in self.boxes)

    def __eq__(self, other):
        return isinstance(other, GameState) and self.map == other.map

    def __hash__(self):
        return hash(tuple(map(tuple, self.map)))

    def get_legal_actions(self):

        return [direction for direction, _, _ in self.get_possible_moves()]
