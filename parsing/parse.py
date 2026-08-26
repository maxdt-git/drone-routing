class Parser:
    def extract_dict(self, cfile: str) -> dict[str, str] | None:
        """
        Open the config and return a dict
        """
        config: dict[str, str] = {}
        try:
            with open(cfile, "r") as file:
                j = 1
                i = 1
                if not file:
                    raise Exception
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    if not line.startswith("#"):
                        if line.startswith("hub"):
                            key, value = line.split(":")
                            config[key + str(i)] = value
                            i += 1
                        elif line.startswith("connection"):
                            key, value = line.split(":")
                            config[key + str(j)] = value
                            j += 1
                        else:
                            key, value = line.split(":")
                            config[key] = value
            return config
        except Exception as e:
            print(e)
            return None

    def parse_nb_drones(self, conf: dict[str, str] | None) -> bool:
        """
        Parse the nb_drones to test the data
        """
        if not conf:
            return False
        try:
            nb_drones = int(conf["nb_drones"])
            if nb_drones < 1:
                raise Exception("nb_drones should be an integer >= 1")
        except ValueError:
            print("nb_drones should be an integer >= 1")
            return False
        except Exception as e:
            print(e)
            return False
        return True

    def parse_hub_tags(self, tokens: list[str]) -> dict[str, str] | None:
        """
        Parse a list of key=value and return a dict
        """
        tags: dict[str, str] = {}
        for token in tokens:
            if "=" not in token:
                print(f"invalid tag '{token}': expected key=value")
                return None
            tag_key, tag_value = token.split("=", 1)
            tags[tag_key] = tag_value
        return tags

    def parse_hub_line(
        self, value: str, expected_name: str | None = None
    ) -> tuple[str, int, int, dict[str, str]] | None:
        """
        Parse "<name> <x> <y> [tag=val ...]" regardless
        of the order of the tags
        """
        line = value.replace("[", "").replace("]", "").split()
        if len(line) < 3:
            print("hub line is missing a name and/or coordinates")
            return None
        name = line[0]
        if expected_name is not None and name != expected_name:
            print(f"hub should be named '{expected_name}'")
            return None
        try:
            x = int(line[1])
            y = int(line[2])
        except ValueError:
            print("coordinate should be an integer")
            return None
        tags = self.parse_hub_tags(line[3:])
        if tags is None:
            return None
        return name, x, y, tags

    def parse_hub(self, conf: dict[str, str] | None) -> bool:
        """
        Parse the start_hub, all the hubs and end_hub and return a bool
        """
        if not conf:
            return False

        colors = [
            "green", "blue", "red", "yellow", "orange", "cyan", "purple",
            "brown", "lime", "magenta", "black", "maroon", "gold", "darkred",
            "violet", "crimson", "rainbow"]
        zones = ["normal", "blocked", "restricted", "priority"]

        for key in conf:
            if key == "start_hub":
                parsed = self.parse_hub_line(conf[key], "start")
                if parsed is None:
                    return False
                _, _, _, tags = parsed
                if "color" in tags and tags["color"] not in colors:
                    print("colors allowed are green, blue, red, yellow, " \
                    "orange, cyan, purple, brown, lime, magenta, black, " \
                    "maroon, gold, darkred, violet, crimson, rainbow")
                    return False

            elif key.startswith("hub"):
                parsed = self.parse_hub_line(conf[key])
                if parsed is None:
                    return False
                _, _, _, tags = parsed
                if "zone" in tags and tags["zone"] not in zones:
                    print("zones should be normal, blocked, "
                          "restricted or priority")
                    return False
                if "color" in tags and tags["color"] not in colors:
                    print("colors allowed are blue, red, green, "
                          "orange and yellow")
                    return False
                if "max_drones" in tags:
                    try:
                        max_drones = int(tags["max_drones"])
                        if max_drones < 1:
                            raise ValueError
                    except ValueError:
                        print("max_drones should be an integer >= 1")
                        return False

            elif key == "end_hub":
                parsed = self.parse_hub_line(conf[key], "goal")
                if parsed is None:
                    return False
                _, _, _, tags = parsed
                if "color" in tags and tags["color"] not in colors:
                    print("colors allowed are blue, red, green, "
                          "orange and yellow")
                    return False

        return True

    def parse_connection_line(
            self, value: str
    ) -> tuple[str, str, str, dict[str, str]] | None:
        """
        Parse "<start>-<end> [max_link_capacity=val]"
        """
        line = value.replace("[", "").replace("]", "").split()

        if not line:
            print("invalid tag : expected start-end")
            return None

        if "-" not in line[0] or line[0].count("-") != 1:
            print("invalid tag : expected start-end")
            return None

        start, end = line[0].split("-", 1)
        if not start or not end:
            print("invalid tag : expected start-end")
            return None

        name = line[0]
        tags: dict[str, str] = {}

        if len(line) > 1:
            if "=" not in line[1]:
                print("invalid tag : expected max_link_capacity=int")
                return None
            tag_key, tag_value = line[1].split("=", 1)
            tags[tag_key] = tag_value

        return name, start, end, tags

    def parse_connection(self, conf: dict[str, str] | None) -> bool:
        """
        Parse the connection data and returns a bool
        """
        if not conf:
            return False

        zone_names: set[str] = set()
        for key, value in conf.items():
            if key == "start_hub":
                parsed_hub = self.parse_hub_line(value, "start")
            elif key == "end_hub":
                parsed_hub = self.parse_hub_line(value, "goal")
            elif key.startswith("hub"):
                parsed_hub = self.parse_hub_line(value)
            else:
                continue
            if parsed_hub is None:
                return False
            name = parsed_hub[0]
            if name in zone_names:
                print(f"duplicate zone name: {name}")
                return False
            zone_names.add(name)

        for key in conf:
            if key.startswith("connection"):
                parsed = self.parse_connection_line(conf[key])
                if parsed is None:
                    return False
                name, name1, name2, tags = parsed
                if name1 == name2:
                    print("In connection, start should be different the end")
                    return False
                if name1 not in zone_names or name2 not in zone_names:
                    print(f"connection references an undefined zone: "
                          f"{name1}-{name2}")
                    return False

                if "max_link_capacity" in tags:
                    try:
                        max_link = int(tags["max_link_capacity"])
                        if max_link < 1:
                            raise ValueError
                    except ValueError:
                        print(
                            "max_link_capacity should be an integer >= 1")
                        return False

        return True
