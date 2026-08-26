class Zone:
    """
    Represent one zone of the map
    """
    def __init__(self, name: str, x: int, y: int, type: str = "normal",
                 color: str = "", max_drones: int = 1):
        """
        Init all the data of the zone
        """
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.max_drones = max_drones


class Connection:
    """
    Represent a link between two Zone
    """
    def __init__(
            self, connec_name: str, name1: str, name2: str,
            max_link_capacity: int):
        """
        Init the the name of the 2 linked zone and the max_link_capacity
        """
        self.name = connec_name
        self.zone1 = name1
        self.zone2 = name2
        self.max_link_capacity = max_link_capacity


class Map:
    """
    Represent the map with all the zones, connections and drones
    """
    def __init__(self,
                 nb_drones: int,
                 start_hub: Zone,
                 zones: list[dict[str, Zone]],
                 end_hub: Zone,
                 connections: list[dict[str, Connection]]):
        """
        Init all the zones (start, end and the hubs), connections and
        the nb of drones
        """
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.hubs = zones
        self.end_hub = end_hub
        self.connections = connections
