from parsing import Zone
from pathfinding import Graph


class Drone:
    """
    Represents a drone during the simulation
    """
    def __init__(
            self,
            graph: Graph, shortest_path: list[str], drone_id: int) -> None:
        """
        Init the drone with the id, pos, status, the shortest path and
        the nbr of turns remaining
        """
        self.drone_id: int = drone_id
        self.actual_pos: Zone = graph.hubs["start"]
        self.shortest_path: list[str] = shortest_path
        self.path_index: int = 0
        self.status: str = "waiting"
        self.turns_remaining: int = 0
        self.graph: Graph = graph

    def next_hub(self) -> str | None:
        """
        Give the next hub available
        """
        if self.path_index >= len(self.shortest_path):
            return None
        return self.shortest_path[self.path_index]

    def advance(self) -> str | None:
        """
        Advance the drone on the path and returns the next zone
        """
        next_pos = self.next_hub()
        if not next_pos:
            return None

        if next_pos == self.graph.map_data.end_hub.name:
            self.actual_pos = self.graph.hubs[next_pos]
            self.path_index += 1
            self.status = "arrived"
            return next_pos

        if self.graph.hubs[next_pos].type == "restricted":
            if self.turns_remaining == 1:
                self.path_index += 1
                self.actual_pos = self.graph.hubs[next_pos]
                self.turns_remaining = 0
                self.status = "waiting"
                return next_pos
            self.status = "in transit"
            self.turns_remaining = 1
            for neighbor, connec, _ in \
                    self.graph.neighbors[self.actual_pos.name]:
                if neighbor == next_pos:
                    return connec.name

            return None

        self.actual_pos = self.graph.hubs[next_pos]
        self.path_index += 1
        self.status = "waiting"
        return next_pos
