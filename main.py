from generator import Generator
from pathfinding import Graph, Pathfinding
from simulation import Simulation


def main() -> None:
    gen = Generator()
    map = gen.generate_map()
    if not map:
        return None

    graph = Graph(map)
    graph.init_hubs()
    graph.init_connections()
    graph.init_neighbors()

    pathfinder = Pathfinding(graph)
    paths = pathfinder.find_multiple_path("start", "goal")
    if not paths[0]:
        print("no paths are find, disconnected graph")
        return

    simulation = Simulation(graph, paths)
    simulation.init_drone_list()
    simulation.init_occupancy()
    simulation.simu()

    for line in simulation.list_stdout:
        print(line)
    print(f"Total turns: {simulation.turn}")


if __name__ == "__main__":
    main()
