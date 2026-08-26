from parsing import Parser, Zone, Connection, Map
import sys


class Generator:
    """
    Generator permits to build the hub_list, the connection_list,
    and create the final map with all the data parsed
    """
    def __init__(self) -> None:
        """
        Init the self.parsed which is the config
        """
        self.conf = Parser()
        self.parsed = self.conf.extract_dict(sys.argv[1])

    def check_nb_drones(self) -> int | None:
        """
        Check nb_drones before stocking it in map
        """
        if self.parsed is None:
            return None
        if not self.conf.parse_nb_drones(self.parsed):
            return None
        return int(self.parsed["nb_drones"])

    def build_zone(
        self, value: str, expected_name: str | None,
        default_max_drones: int
    ) -> Zone | None:
        """
        Build a Zone from an already-parsed hub line, reusing
        parse_hub_line
        """
        parsed = self.conf.parse_hub_line(value, expected_name)
        if parsed is None:
            return None
        name, x, y, tags = parsed
        color = tags.get("color", "")
        zone_type = tags.get("zone", "normal")
        try:
            max_drones = int(tags.get("max_drones", default_max_drones))
        except ValueError:
            return None
        return Zone(
            name, x, y, type=zone_type, color=color, max_drones=max_drones)

    def generate_hub_list(self) -> list[dict[str, Zone]] | None:
        """
        Generate the hub list using parse_hub and build_zone
        """
        if not self.parsed:
            return None
        if not self.conf.parse_hub(self.parsed):
            return None

        nb_drones = self.conf.parse_nb_drones(self.parsed)
        if not nb_drones:
            return None

        try:
            drones = int(self.parsed.get("nb_drones", "1"))
        except ValueError:
            drones = 1

        hub_list: list[dict[str, Zone]] = []
        for key in self.parsed:
            if key == "start_hub":
                start = self.build_zone(
                    self.parsed[key], "start", drones)
                if start is None:
                    return None
                hub_list.append({"start": start})

            elif key.startswith("hub"):
                hub = self.build_zone(self.parsed[key], None, 1)
                if hub is None:
                    return None
                hub_list.append({hub.name: hub})

            elif key == "end_hub":
                end = self.build_zone(
                    self.parsed[key], "goal", drones)
                if end is None:
                    return None
                hub_list.append({"goal": end})

        return hub_list

    def build_connection(
            self, value: str, default_max_link_capacity: int
    ) -> Connection | None:
        """
        Build a Connection from an already-parsed connection line, reusing
        parse_connection_line
        """
        parsed = self.conf.parse_connection_line(value)
        if parsed is None:
            return None
        connec_name, name1, name2, max_link_capacity = parsed
        try:
            tags = int(
                max_link_capacity.get(
                    "max_link_capacity", default_max_link_capacity))
        except ValueError:
            return None
        return Connection(
            connec_name, name1, name2, tags)

    def generate_connection_list(self) -> list[dict[str, Connection]] | None:
        """
        Generate the connection list using parse_connection
        and build_connection
        """
        if not self.parsed:
            return None
        if not self.conf.parse_connection(self.parsed):
            return None

        try:
            max_link_capacity = int(self.parsed.get("nb_drones", "1"))
        except ValueError:
            max_link_capacity = 1

        connection_list: list[dict[str, Connection]] = []

        for key in self.parsed:
            if key.startswith("connection"):
                connection = self.build_connection(
                    self.parsed[key], max_link_capacity)
                if connection is None:
                    return None
                connection_list.append({connection.name: connection})

        return connection_list

    def generate_map(self) -> Map | None:
        """
        Generate the Map using the created hub_list, connection_list
        and nb_drones
        """
        hub_list = self.generate_hub_list()
        if not hub_list:
            return None

        list_connec = self.generate_connection_list()
        if not list_connec:
            return None

        nb_drones = self.check_nb_drones()
        if not nb_drones:
            return None

        start: Zone | None = None
        goal: Zone | None = None

        for zone in hub_list:
            for name in zone:
                if name.startswith("start"):
                    start = zone[name]
                if name.startswith("goal"):
                    goal = zone[name]

        if start is None or goal is None:
            return None

        return Map(nb_drones, start, hub_list, goal, list_connec)
