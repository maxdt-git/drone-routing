from generator import Generator
from pathfinding import Graph, Pathfinding


def main() -> None:
    gen = Generator()
    map = gen.generate_map()
    if not map:
        return None

    graph = Graph(map)
    graph.init_hubs()
    graph.init_connections()
    # print(graph.hubs)
    graph.init_neighbors()
    # print(graph.neighbors)
    pathfinder = Pathfinding(graph)
    path = pathfinder.shortest_path("start", "goal")
    print(path)


if __name__ == "__main__":
    main()
