

import argparse
from modules.game_state import GameState
from modules.solver import Solver

def load_map(map_path):
    """Load the map from the given path"""
    with open(map_path, 'r') as f:
        game_map = [list(line.strip()) for line in f]
    return game_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--map', help='The map file', default='maps/sokoban1.txt')
    parser.add_argument('--strategy', help='The strategy to solve the game', default='ucs')
    args = parser.parse_args()

    maps = ["maps/sokoban1.txt", "maps/sokoban2.txt", "maps/sokoban3.txt", "maps/sokoban4.txt"]
    algorithms = ["bfs", "dfs", "astar", "ucs", "greedy"]

    for map_path in maps:
        for algorithm in algorithms:
            print(f"\nRunning Algorithm: {algorithm} on Map: {map_path}\n")
            
            game_map = load_map(map_path)
            game_state = GameState(game_map)
            solver = Solver(game_state, algorithm)
            solver.solve()
            solution = solver.get_solution()
            
            print("\n-----------------------\n")
