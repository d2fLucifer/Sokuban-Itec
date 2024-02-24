import time
import heapq
from collections import deque

class Solver(object):
    def __init__(self, initial_state, strategy):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.time = None
        self.expanded_states = 0
        self.generated_states = 0
        self.moves_to_goal = 0  # Initialize moves_to_goal attribute

    def solve(self):
        start_time = time.time()
        solving_method = getattr(self, self.strategy.lower(), None)
        if solving_method:
            self.solution = solving_method()
            self.print_solution(self.solution, start_time)
        else:
            raise Exception('Invalid strategy')
        self.time = time.time() - start_time

    def print_solution(self, path, start_time):
        end_time = time.time()
        print("Time taken:", round(end_time - start_time, 3), "seconds")

        if path is not None:
            print("Expanded states:", self.expanded_states)
            print("Generated states:", self.generated_states)
            moves_to_goal = len(path)
            print("Number of moves to reach the goal:", moves_to_goal)
            self.moves_to_goal = moves_to_goal  # Update moves_to_goal attribute
        else:
            print("No solution found.")

    def get_legal_action(self, state):
        """
        Get legal actions for a given state.
        You need to implement this method based on your state representation.
        """
        return state.get_legal_actions()

    def bfs(self):
        open_queue = deque([(self.initial_state, [])])
        closed_set = set()

        while open_queue:
            current_state, path = open_queue.popleft()

            if current_state.check_solved():
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)
                self.generated_states += 1

                for direction in self.get_legal_action(current_state):
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        open_queue.append((next_state, path + [direction]))
                        self.expanded_states += 1

        return None

    def dfs(self):
        stack = [(self.initial_state, [])]
        closed_set = set()

        while stack:
            current_state, path = stack.pop()

            if current_state.check_solved():
                self.expanded_states += 1
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)
                self.generated_states += 1

                for direction in self.get_legal_action(current_state):
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        stack.append((next_state, path + [direction]))
                        self.expanded_states += 1  # Increment for each expanded state

        return None

    def astar(self):
        open_list = [(self.initial_state.get_total_cost(), self.initial_state, [])]
        closed_set = set()

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                self.expanded_states += 1
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)
                self.generated_states += 1

                for direction in self.get_legal_action(current_state):
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        new_cost = next_state.get_total_cost()
                        heapq.heappush(open_list, (new_cost, next_state, path + [direction]))
                        self.expanded_states += 1  # Increment for each expanded state

        return None

    def greedy(self):
        open_list = [(self.initial_state.get_heuristic(), self.initial_state, [])]
        heapq.heapify(open_list)
        closed_set = set()

        while open_list:
            _, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                self.expanded_states += 1
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)
                self.generated_states += 1

                for direction in self.get_legal_action(current_state):
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        new_cost = next_state.get_heuristic()
                        heapq.heappush(open_list, (new_cost, next_state, path + [direction]))
                        self.expanded_states += 1  # Increment for each expanded state

        return None
    
    def ucs(self):
        open_list = [(self.initial_state.get_current_cost(), self.initial_state, [])]
        heapq.heapify(open_list)
        closed_set = set()

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                self.expanded_states += 1
                return path

            current_state_hash = hash(current_state)
            if current_state_hash in closed_set:
                continue

            closed_set.add(current_state_hash)
            self.generated_states += 1

            for direction in self.get_legal_action(current_state):
                next_state = current_state.move(direction)
                next_state_hash = hash(next_state)
                if next_state_hash not in closed_set:
                    new_cost = next_state.get_current_cost() + next_state.get_heuristic()
                    self.add_to_open_list(open_list, new_cost, next_state, path + [direction])

        return None

    def add_to_open_list(self, open_list, cost, state, path):
        heapq.heappush(open_list, (cost, state, path))
        self.expanded_states += 1

    def all_directions(self):
        return ['U', 'D', 'L', 'R']

    def get_solution(self):
        return self.solution

    def custom(self):
        return ["L", "L"]
