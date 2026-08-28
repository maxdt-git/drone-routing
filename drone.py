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
        self.shortest_path = shortest_path
        self.path_index: int = 0
        self.status: str = "waiting"
        self.turns_remaining: int = 0
