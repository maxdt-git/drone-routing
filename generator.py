from parsing import Parser, Zone
import sys


class Generator:
    def __init__(self) -> None:
        self.conf = Parser()
        self.parsed = self.conf.extract_dict(sys.argv[1])

    def _build_zone(
        self, value: str, expected_name: str | None,
        default_max_drones: int
    ) -> Zone | None:
        """
        Build a Zone from a hub line, reading tags with the key
        """
        line = value.replace("[", "").replace("]", "").split()
        if len(line) < 3:
            return None
        name = line[0]
        if expected_name is not None and name != expected_name:
            return None
        try:
            x = int(line[1])
            y = int(line[2])
        except ValueError:
            return None
        tags = self.conf.parse_hub_tags(line[3:])
        if tags is None:
            return None
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
                start = self._build_zone(
                    self.parsed[key], "start", nb_drones)
                if start is None:
                    return None
                hub_list.append({"start": start})

            elif key.startswith("hub"):
                hub = self._build_zone(self.parsed[key], None, 1)
                if hub is None:
                    return None
                hub_list.append({hub.name: hub})

            elif key == "end_hub":
                end = self._build_zone(
                    self.parsed[key], "goal", nb_drones)
                if end is None:
                    return None
                hub_list.append({"goal": end})

        return hub_list


def main() -> None:
    gen = Generator()
    hub_list = gen.generate_hub_list()
    if not hub_list:
        return None
    print(hub_list)


if __name__ == "__main__":
    main()
