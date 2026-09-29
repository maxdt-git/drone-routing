from pathfinding import Graph
from drone import Drone
from colors import Color


class Simulation:
    """
    Class for the multidrone pathfinding with all the conditions
    """
    def __init__(self, graph: Graph, paths_list: list[list[str]]) -> None:
        """
        Init a list of drones, the nbr of turns and the graph
        """
        self.drones: list[Drone] = []
        self.graph: Graph = graph
        self.turn: int = 0
        self.list_stdout: list[str] = []
        self.paths_list: list[list[str]] = paths_list
        self.zone_occupancy: dict[str, int] = {}
        self.connection_occupancy: dict[str, int] = {}

    def init_drone_list(self) -> None:
        """
        Init the list of drones
        """
        for i in range(self.graph.map_data.nb_drones):
            self.drones.append(
                Drone(
                    self.graph,
                    self.paths_list[i % len(self.paths_list)], i))

    def init_occupancy(self) -> None:
        """
        Init the dict of zone and connection occupancy
        """
        for zone in self.graph.hubs:
            self.zone_occupancy[zone] = 0
        for connec in self.graph.connections:
            self.connection_occupancy[connec] = 0

    def reset_occupancy(self) -> None:
        """
        Reset the occupancy depending of the drone status
        """
        for connec_name in self.graph.connections:
            self.connection_occupancy[connec_name] = 0

        for drone in self.drones:
            next_pos = drone.next_hub()
            if drone.status == "in transit":
                for name, connec, _ in \
                        self.graph.neighbors[drone.actual_pos.name]:
                    if name == next_pos:
                        self.connection_occupancy[connec.name] += 1

    def stack_list(self) -> None:
        """
        Create the return list with all the movement of the drones
        """
        color = Color()
        turn_move: list[str] = []
        for drone in self.drones:
            next_pos = drone.next_hub()
            if not next_pos:
                continue
            if next_pos == self.graph.map_data.end_hub.name or \
                    next_pos == self.graph.map_data.start_hub.name:
                previous_zone = drone.actual_pos.name
                drone.advance()
                self.zone_occupancy[previous_zone] -= 1
                turn_move.append(
                    color.chose_color(self.graph.hubs[next_pos].color) +
                    "D" + str(drone.drone_id) + "-" +
                    self.graph.hubs[next_pos].name + "\033[0m")
                continue
            if self.graph.hubs[next_pos].type == "restricted":
                for name, connec, _ in \
                        self.graph.neighbors[drone.actual_pos.name]:
                    if drone.turns_remaining != 1:
                        if name == next_pos:
                            if self.connection_occupancy[connec.name] < \
                                    connec.max_link_capacity:
                                previous_zone = drone.actual_pos.name
                                drone.advance()
                                self.zone_occupancy[previous_zone] -= 1
                                self.connection_occupancy[connec.name] += 1
                                turn_move.append(
                                    color.chose_color(
                                        self.graph.hubs[next_pos].color) +
                                    "D" + str(drone.drone_id) + "-" +
                                    connec.name + "\033[0m")
                            else:
                                continue
                    else:
                        if name == next_pos:
                            if self.zone_occupancy[next_pos] < \
                                    self.graph.hubs[next_pos].max_drones:
                                self.connection_occupancy[connec.name] -= 1
                                drone.advance()
                                self.zone_occupancy[next_pos] += 1
                                turn_move.append(
                                    color.chose_color(
                                        self.graph.hubs[next_pos].color) +
                                    "D" + str(drone.drone_id) + "-" +
                                    self.graph.hubs[next_pos].name + "\033[0m")
            else:
                for name, connec, _ in \
                        self.graph.neighbors[drone.actual_pos.name]:
                    if name == next_pos:
                        if self.zone_occupancy[next_pos] < \
                            self.graph.hubs[next_pos].max_drones and \
                                self.connection_occupancy[connec.name] < \
                                connec.max_link_capacity:
                            previous_zone = drone.actual_pos.name
                            drone.advance()
                            self.zone_occupancy[previous_zone] -= 1
                            self.connection_occupancy[connec.name] += 1
                            self.zone_occupancy[next_pos] += 1
                            turn_move.append(
                                color.chose_color(
                                    self.graph.hubs[next_pos].color) +
                                "D" + str(drone.drone_id) + "-" +
                                self.graph.hubs[next_pos].name + "\033[0m")
                        else:
                            continue

        if turn_move:
            self.list_stdout.append(" ".join(turn_move))

    def simu(self) -> None:
        """
        Creathe the simulation with all the drones
        """
        while not all(drone.status == "arrived" for drone in self.drones):
            self.reset_occupancy()
            self.stack_list()
            self.turn += 1
