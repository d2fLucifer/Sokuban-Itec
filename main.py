import argparse

from modules.game_state import GameState
from modules.game_visualization import GameVisualization
from modules.solver import Solver


def load_map(map_path):
    """Load the map from the given path"""
    f = open(map_path, 'r')
    map = []
    for line in f:
        map.append(list(line.strip()))
    f.close()
    return map


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--map', help='The map file', default='maps/sokoban1.txt')
    parser.add_argument(
        '--strategy', help='The strategy to solve the game', default='greedy')
    args = parser.parse_args()

    map = load_map(args.map)

    game_state = GameState(map)
    strategy = args.strategy
    solver = Solver(game_state, strategy)
    solver.solve()
    solution = solver.get_solution()
  
    game_visualization = GameVisualization(game_state, solution)
    game_visualization.start()