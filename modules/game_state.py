class GameState:
    def __init__(self, map, current_cost=0, parent=None):  # Add parent parameter with default value None
        self.map = map
        self.current_cost = current_cost
        self.parent = parent 
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()
        self.solution_path = [] 
    def __lt__(self, other):
        """Define the comparison between two GameState instances."""
        return self.get_total_cost() < other.get_total_cost()
    def find_player(self):
        """Find the player in the map and return its position"""
        for row in range(self.height):
            for col in range(self.width):
                cell = self.map[row][col]
                if cell in ['@', '+']:
                    return row, col


    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes = []
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] in ['$', '*']:
                    boxes.append((row, col))
        return boxes

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        targets = []
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] in ['.', '*']:
                    targets.append((row, col))
        return targets

    def is_wall(self, position):
        """Check if the given position is a wall"""
        row, col = position
        return self.map[row][col] == '#'

    def is_box(self, position):
        """Check if the given position is a box"""
        row, col = position
        return self.map[row][col] in ['$', '*']

    def is_target(self, position):
        """Check if the given position is a target"""
        row, col = position
        return self.map[row][col] in ['.', '*']

    def is_empty(self, position):
        """Check if a position is empty or a target."""
        row, col = position
        return self.map[row][col] in [' ', '.']
    
    def is_box_on_target(self, position):
        row, col = position
        return self.map[row][col] in [ '*']
    def is_box_in_corner(self, box_position):
        """Check if the box is being pushed into a corner"""
        row, col = box_position
        # Implement logic to check if the box is in a corner
        return False  # Placeholder implementation, replace with actual logic



    def get_heuristic(self):
        """Get the heuristic for the game state"""
        heuristic = 0
        box_target_distances = {(box, target): abs(box[0] - target[0]) + abs(box[1] - target[1])
                                for box in self.boxes for target in self.targets}

        for box in self.boxes:
            min_distance = min(box_target_distances[box, target] for target in self.targets)
            heuristic += min_distance

        return heuristic


    def get_total_cost(self):
        """Get the cost for the game state"""
        return self.current_cost + self.get_heuristic()
    def is_valid_move(self, new_player_position, new_box_position=None):
        """Check if the move is valid (not hitting a wall or pushing a box into a corner)"""
        new_row, new_col = new_player_position

        # Check if the new position is within the boundaries of the map and not a wall
        if not (0 <= new_row < self.height and 0 <= new_col < self.width and (new_row, new_col) not in self.walls):
            return False

        # Check if the new position is a box
        if (new_row, new_col) in self.boxes:
            # Calculate the position after pushing the box
            if new_box_position is None:
                return False  # No box position provided
            new_box_row, new_box_col = new_box_position

            # Check if the new position for the box is within the boundaries of the map and not a wall
            if not (0 <= new_box_row < self.height and 0 <= new_box_col < self.width and (new_box_row, new_box_col) not in self.walls):
                return False

            # Check if the new position for the box is not occupied by another box
            if (new_box_row, new_box_col) in self.boxes:
                return False

            # Check if the box is being pushed into a corner
            if self.is_box_in_corner((new_row, new_col), (new_box_row, new_box_col)):
                return False

        return True


    def is_box_in_corner(self, old_box_position, new_box_position):
        """Check if the box is being pushed into a corner"""
        # Implementation to check if the box is being pushed into a corner
        return False  # Placeholder implementation, replace with actual logic
    def get_current_cost(self):
        """Get the current cost for the game state"""
        return self.current_cost
    def get_possible_moves(self):
        possible_moves = []

        for direction in ['U', 'D', 'L', 'R']:
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

            new_player_position = (new_row, new_col)

            # Check if the new position is within the boundaries of the map and not a wall
            if not (0 <= new_row < self.height and 0 <= new_col < self.width and (new_row, new_col) not in self.walls):
                continue

            if (new_row, new_col) in self.boxes:
                # Calculate the position after pushing the box
                new_box_row, new_box_col = new_row, new_col

                if direction == 'U':
                    new_box_row -= 1
                elif direction == 'D':
                    new_box_row += 1
                elif direction == 'L':
                    new_box_col -= 1
                elif direction == 'R':
                    new_box_col += 1

                new_box_position = (new_box_row, new_box_col)

                # Check if the new position for the box is within the boundaries of the map and not a wall
                if not (0 <= new_box_row < self.height and 0 <= new_box_col < self.width and (new_box_row, new_box_col) not in self.walls):
                    continue

                # Check if the new position for the box is not occupied by another box
                if (new_box_row, new_box_col) in self.boxes:
                    continue

                # Check if the box is being pushed into a corner
                if self.is_box_in_corner((new_row, new_col), (new_box_row, new_box_col)):
                    continue

                # Add the move to possible_moves
                possible_moves.append((direction, new_player_position, new_box_position))
            else:
                # If the new position is empty, only update the player position
                possible_moves.append((direction, new_player_position, None))

        return possible_moves

    
    def move(self, direction):
        """Generate the next game state by moving the player in the given direction."""
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

        new_game_state = self.clone()  # Create a clone of the current GameState object
        if new_game_state.is_empty((new_row, new_col)):
            # If the new position is empty, move the player
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
                # If the new position for the box is empty, push the box
                new_game_state.map[row][col] = '.' if (row, col) in new_game_state.targets else ' '
                new_game_state.map[new_row][new_col] = '@' if new_game_state.map[new_row][new_col] == ' ' else '+'
                new_game_state.map[new_box_row][new_box_col] = '$' if new_game_state.map[new_box_row][new_box_col] == ' ' else '*'
                new_game_state.player = (new_row, new_col)
                new_game_state.boxes.remove((new_row, new_col))
                new_game_state.boxes.append((new_box_row, new_box_col))
                new_game_state.current_cost += 1

        return new_game_state

    def clone(self):
        """Create a deep copy of the current game state."""
        cloned_map = [row[:] for row in self.map]  # Deep copy of the map
        cloned_state = GameState(cloned_map, self.current_cost, self.parent)  # Create a new GameState object
        cloned_state.height = self.height
        cloned_state.width = self.width
        cloned_state.player = self.player
        cloned_state.boxes = self.boxes[:]
        cloned_state.targets = self.targets[:]
        cloned_state.is_solved = self.is_solved
        cloned_state.solution_path = self.solution_path[:]
        return cloned_state


    def check_solved(self):
        """Check if the game is solved"""
        return all(box in self.targets for box in self.boxes)

    def __eq__(self, other):
        return isinstance(other, GameState) and self.map == other.map

    def __hash__(self):
        return hash(tuple(map(tuple, self.map)))