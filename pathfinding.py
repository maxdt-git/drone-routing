from parsing import Zone, Connection, Map
import heapq


class Graph:
    """
    Graph used for the pathfinding, show real time of the map
    """
    def __init__(self, map_data: Map) -> None:
        """
        Init hubs thanks to map_data.hubs and change it into a
        dict[str, Zone] and init possible neighbors with connection
        """
        self.map_data = map_data
        self.hubs: dict[str, Zone] = {}
        self.connections: dict[str, Connection] = {}
        self.neighbors: dict[str, list[tuple[str, Connection, int]]] = {}

    def init_hubs(self) -> None:
        """
        Change map_data.hubs into a dict[str, Zone]
        """
        for hubs in self.map_data.hubs:
            for name in hubs:
                self.hubs[name] = hubs[name]
        self.hubs["start"] = self.map_data.start_hub
        self.hubs["goal"] = self.map_data.end_hub

    def init_connections(self) -> None:
        """
        Change map_data.connections into a dict[str, Connection]
        """
        for connection in self.map_data.connections:
            for name in connection:
                self.connections[name] = connection[name]

    def init_neighbors(self) -> None:
        """
        Init self.neighbors by creating a
        dict[str: name of zone1, list[tuple[str: name of zone2,
        Connection: class Connection created, int: cost]]]
        """
        for connection in self.connections:
            connec = self.connections[connection]
            zone1 = connec.zone1
            zone2 = connec.zone2
            if self.hubs[zone1].type == "blocked" \
                    or self.hubs[zone2].type == "blocked":
                continue
            cost_zone1 = self.hubs[zone1].cost
            cost_zone2 = self.hubs[zone2].cost
            if zone1 in self.neighbors:
                self.neighbors[zone1].append((zone2, connec, cost_zone2))
            else:
                self.neighbors[zone1] = [(zone2, connec, cost_zone2)]
            if zone2 in self.neighbors:
                self.neighbors[zone2].append((zone1, connec, cost_zone1))
            else:
                self.neighbors[zone2] = [(zone1, connec, cost_zone1)]


class Pathfinding:
    """
    Class for the pathfinding, where we find path for only one drone
    """
    def __init__(self, graph: Graph) -> None:
        """
        Init graph to be easier to find with the methods
        """
        self.graph = graph

    def paths(
            self, start: str, end: str,
            excluded: set[str] | None = None) -> list[str]:
        """
        Find the shortest path from start to end using djikstra algo
        """
        dist: dict[str, int] = {}
        previous: dict[str, str] = {}
        queue: list[tuple[int, str]] = []
        priority_count: dict[str, int] = {}

        dist[start] = 0
        heapq.heappush(queue, (0, start))
        priority_count[start] = 0

        while queue:
            actual_cost, actual_zone = heapq.heappop(queue)

            for neighbor in self.graph.neighbors[actual_zone]:
                name, connection, path_cost = neighbor
                if excluded and connection.name in excluded:
                    continue
                candidate_priority = priority_count[actual_zone] + \
                    (1 if self.graph.hubs[name].type == "priority" else 0)
                candidate = actual_cost + path_cost
                if name not in dist or candidate < dist[name]:
                    dist[name] = candidate
                    previous[name] = actual_zone
                    priority_count[name] = candidate_priority
                    heapq.heappush(queue, (candidate, name))
                elif candidate == dist[name] and \
                        candidate_priority > priority_count[name]:
                    previous[name] = actual_zone
                    priority_count[name] = candidate_priority
                    heapq.heappush(queue, (candidate, name))

            if actual_zone == end:
                break

        if end not in dist:
            return []

        final_path: list[str] = []

        node = end
        while node != start:
            final_path.append(node)
            node = previous[node]
        final_path.reverse()

        return final_path

    def connection_of(self, start: str, path: list[str]) -> set[str]:
        """
        Create a set of connections already seen
        """
        excluded: set[str] = set()
        visited = [start] + path

        for i in range(len(visited) - 1):
            for name, connec, _ in self.graph.neighbors[visited[i]]:
                if name == visited[i + 1]:
                    excluded.add(connec.name)

        return excluded

    def path_cost(self, path: list[str]) -> int:
        """
        Return the cost of the path
        """
        return sum(self.graph.hubs[zone].cost for zone in path)

    def find_multiple_path(
            self, start: str, end: str, nb_paths: int = 10) -> list[list[str]]:
        """
        Find nb_paths paths in the map
        """
        result: list[list[str]] = []

        first_path = self.paths(start, end)
        result.append(first_path)

        while len(result) < nb_paths:
            all_used: set[str] = set()
            candidates: list[list[str]] = []
            for path in result:
                all_used.update(self.connection_of(start, path))

            for connec in all_used:
                candidate = self.paths(start, end, {connec})
                if candidate and candidate not in result:
                    candidates.append(candidate)

            if not candidates:
                break

            result.append(min(candidates, key=self.path_cost))

        return result
