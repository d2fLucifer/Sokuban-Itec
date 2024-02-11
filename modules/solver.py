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
        if self.strategy == 'bfs':
            self.solution = self.bfs()
        elif self.strategy == 'dfs':
            self.solution = self.dfs()
        elif self.strategy == 'astar':
            self.solution = self.astar()
        elif self.strategy == 'ucs':
            self.solution = self.ucs()
        elif self.strategy == 'greedy':
            self.solution = self.greedy()
        elif self.strategy == 'custom':
            self.solution = self.custom()
        else:
            raise Exception('Invalid strategy')
        self.time = time.time() - start_time

        print(self.solution)

    
    def bfs(self):
        open_queue = deque([(self.initial_state, [])])
        closed_set = set()

        start_time = time.time()

        while open_queue:
            current_state, path = open_queue.popleft()

            if current_state.check_solved():
                end_time = time.time()
                print("Time taken:", round(end_time - start_time, 3), "seconds")
                print("Expanded state:", path)
                print("Solved:", current_state.check_solved())
                self.moves_to_goal = len(path)  # Update moves_to_goal attribute
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in ['U', 'D', 'L', 'R']:
                    next_state = current_state.move(direction)

                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        open_queue.append((next_state, path + [direction]))

        return None

    def dfs(self):
        max_depth = 100  # Adjust this value as needed
        start_time = time.time()

        for depth_limit in range(1, max_depth + 1):
            closed_set = set()
            result = self.dfs_recursive(self.initial_state, [], depth_limit, closed_set)
            if result:
                end_time = time.time()
                print("Time taken:", round(end_time - start_time, 3), "seconds")
                print("Expanded state:", result)
                print("Solved:", self.initial_state.check_solved())
                self.moves_to_goal = len(result)  # Update moves_to_goal attribute
                return result

        return None

    def dfs_recursive(self, state, path, depth_limit, closed_set):
        if state.check_solved():
            return path

        if depth_limit == 0:
            return None

        for direction in ['U', 'D', 'L', 'R']:
            next_state = state.move(direction)
            next_state_hash = hash(next_state)
            if next_state_hash not in closed_set:
                closed_set.add(next_state_hash)
                result = self.dfs_recursive(next_state, path + [direction], depth_limit - 1, closed_set)
                if result:
                    return result

        return None
    def astar(self):
        open_list = [(self.initial_state.get_heuristic(), self.initial_state, [])]
        heapq.heapify(open_list)
        closed_set = set()

        start_time = time.time()

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                end_time = time.time()
                print("Time taken:", round(end_time - start_time, 3), "seconds")
                print("Expanded state:", path)
                print("Solved:", current_state.check_solved())
                self.moves_to_goal = len(path)  # Update moves_to_goal attribute
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in ['U', 'D', 'L', 'R']:
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

        start_time = time.time()

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                end_time = time.time()
                print("Time taken:", round(end_time - start_time, 3), "seconds")
                print("Expanded state:", path)
                print("Solved:", current_state.check_solved())
                return path

            current_state_hash = hash(current_state)
            if current_state_hash not in closed_set:
                closed_set.add(current_state_hash)

                for direction in ['U', 'D', 'L', 'R']:
                    temp_state = current_state.move('')  # Use a neutral move to get a copy of the current state
                    next_state = temp_state.move(direction)

                    next_state_hash = hash(next_state)
                    if next_state_hash not in closed_set:
                        new_cost = next_state.get_current_cost()
                        heapq.heappush(open_list, (new_cost, next_state, path + [direction]))

        return None

    def custom (self):
        return["L","L"]
    def get_solution(self):
        return self.solution

