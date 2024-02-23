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

        print(self.solution)

    def print_solution(self, path, start_time):
        end_time = time.time()
        print("Time taken:", round(end_time - start_time, 3), "seconds")
        
        if path is not None:
            print("Expanded state:", path)
            print("Solved:", self.initial_state.check_solved())
            self.moves_to_goal = len(path)  # Update moves_to_goal attribute
        else:
            print("No solution found.")

    def bfs(self):
        open_queue = deque([(self.initial_state, [])])
        closed_set = set()

        while open_queue:
            current_state, path = open_queue.popleft()

            if current_state.check_solved():
                self.expanded_states = len(closed_set)
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in self.all_directions():
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        open_queue.append((next_state, path + [direction]))

        return None

    def dfs(self):
        start_time = time.time()

        # Set a reasonable maximum depth
        max_depth = 1000  # Adjust this value based on your problem's characteristics

        result = None
        for depth_limit in range(1, max_depth + 1):
            result = self.dfs_recur(self.initial_state, depth_limit, set())
            if result:
                self.expanded_states = len(result) - 1  # Exclude the initial state from the count
                self.time = time.time() - start_time
                self.print_solution(result, start_time)
                return result

        self.time = time.time() - start_time
        self.print_solution(None, start_time)
        return None

    def dfs_recur(self, current_state, depth_limit, closed_set):
        if current_state.check_solved():
            return []

        current_state_hash = hash(current_state)
        if current_state_hash in closed_set or depth_limit == 0:
            return None

        closed_set.add(current_state_hash)

        for direction in self.all_directions():
            next_state = current_state.move(direction)
            result = self.dfs_recur(next_state, depth_limit - 1, closed_set)

            if result is not None:
                return [direction] + result

        return None

    def astar(self):
        open_list = [(self.initial_state.get_heuristic(), self.initial_state, [])]
        heapq.heapify(open_list)
        closed_set = set()

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                self.expanded_states = len(closed_set)
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in self.all_directions():
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        new_cost = next_state.get_heuristic()
                        heapq.heappush(open_list, (new_cost, next_state, path + [direction]))

        return None

    def ucs(self):
        open_list = [(self.initial_state.get_current_cost(), self.initial_state, [])]
        heapq.heapify(open_list)
        closed_set = set()

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                self.expanded_states = len(closed_set)
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in self.all_directions():
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        new_cost = next_state.get_current_cost()
                        heapq.heappush(open_list, (new_cost, next_state, path + [direction]))

        return None

    def greedy(self):
        open_list = [(self.initial_state.get_heuristic(), self.initial_state, [])]
        heapq.heapify(open_list)
        closed_set = set()

        while open_list:
            _, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                self.expanded_states = len(closed_set)
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in self.all_directions():
                    next_state = current_state.move(direction)
                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        new_cost = next_state.get_heuristic()
                        heapq.heappush(open_list, (new_cost, next_state, path + [direction]))

        return None

    def all_directions(self):
        return ['U', 'D', 'L', 'R']

    def get_solution(self):
        return self.solution

    def custom(self):
        return ["L", "L"]
