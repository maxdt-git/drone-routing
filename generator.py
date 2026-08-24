from parsing import Parser, Zone, Connection
import sys


class Generator:
    def __init__(self) -> None:
        self.conf = Parser()
        self.parsed = self.conf.extract_dict(sys.argv[1])

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

        try:
            nb_drones = int(self.parsed.get("nb_drones", "1"))
        except ValueError:
            nb_drones = 1

        hub_list: list[dict[str, Zone]] = []
        for key in self.parsed:
            if key == "start_hub":
                start = self.build_zone(
                    self.parsed[key], "start", nb_drones)
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
                    self.parsed[key], "goal", nb_drones)
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
        name1, name2, max_link_capacity = parsed
        try:
            max_link_capacity = int(
                max_link_capacity.get(
                    "max_link_capacity", default_max_link_capacity))
        except ValueError:
            return None
        return Connection(
            name1, name2, max_link_capacity)

    def generate_connection_list(self) -> list[dict[str, Connection]] | None:
        """
        Generate the connection list using parse_hub and build_connection
        """
        if not self.parsed:
            return None
        if not self.conf.parse_hub(self.parsed):
            return None

def main() -> None:
    gen = Generator()
    # hub_list = gen.generate_hub_list()
    # if not hub_list:
    #     return None
    # print(hub_list)

    connection = gen.build_connection(" start-junction", 2)
    print(connection)


if __name__ == "__main__":
    main()
