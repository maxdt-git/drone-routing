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
        Parse the nb_drones before stock it in Map
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

    def parse_hub(self, conf: dict[str, str] | None) -> bool:
        """
        Parse the start_hub, all the hubs and end_hub
        before stock it in Zone and then Map
        """
        if not conf:
            return False

        for key in conf:
            if key.startswith("start_hub"):
                line = conf["start_hub"].replace(
                    "[", "").replace("]", "").split(" ")
                for i in range(1, len(line)):
                    if i == 1:
                        try:
                            name = line[i]
                            if name != "start":
                                raise Exception(
                                    "start_hub should be the first word")
                        except Exception as e:
                            print(e)
                            return False

                    if i == 2:
                        try:
                            int(line[i])
                        except Exception:
                            print("coordinate should be an integer")
                            return False

                    if i == 3:
                        try:
                            int(line[i])
                        except Exception:
                            print("coordinate should be an integer")
                            return False

                    if i == 4:
                        if line[i].startswith("color"):
                            color = line[i].split("=")[1]
                            colors = [
                                "blue", "red", "green", "orange", "yellow"]
                            try:
                                if color not in colors:
                                    raise Exception(
                                        "colors allowed are blue, red, green,"
                                        " orange and yellow")
                            except Exception as e:
                                print(e)
                                return False
                        else:
                            raise Exception("should start with color")

                    if i == 5:
                        if line[i].startswith("max_drones"):
                            max = line[i].split("=")[1]
                            try:
                                int(max)
                                if int(max) < 1:
                                    raise Exception("max_drones should be an "
                                                    "integer >= 1")
                            except Exception:
                                print("max_drones should be an integer >= 1")
                                return False

            if key.startswith("hub"):
                line = conf[key].replace("[", "").replace("]", "").split(" ")
                for i in range(2, len(line)):
                    if i == 2:
                        try:
                            int(line[i])
                        except Exception:
                            print("coordinate should be an integer")
                            return False

                    if i == 3:
                        try:
                            int(line[i])
                        except Exception:
                            print("coordinate should be an integer")
                            return False

                    if i == 4 or i == 5 or i == 6:
                        if line[i].startswith("zone"):
                            zone = line[i].split("=")[1]
                            zones = [
                                "normal", "blocked", "restricted", "priority"]
                            try:
                                if zone not in zones:
                                    raise Exception(
                                        "zones should be normal, blocked, "
                                        "restricted or priority")
                            except Exception as e:
                                print(e)
                                return False

                        if line[i].startswith("color"):
                            color = line[i].split("=")[1]
                            colors = [
                                "blue", "red", "green", "orange", "yellow"]
                            try:
                                if color not in colors:
                                    raise Exception(
                                        "colors allowed are blue, red,"
                                        " green, orange and yellow")
                            except Exception as e:
                                print(e)
                                return False

                        if line[i].startswith("max_drones"):
                            max = line[i].split("=")[1]
                            try:
                                int(max)
                                if int(max) < 1:
                                    raise Exception("max_drones should be an "
                                                    "integer >= 1")
                            except Exception:
                                print("max_drones should be an integer >= 1")
                                return False

            if key.startswith("end_hub"):
                line = conf["end_hub"].replace(
                    "[", "").replace("]", "").split(" ")
                for i in range(1, len(line)):
                    if i == 1:
                        try:
                            name = line[i]
                            if name != "goal":
                                raise Exception(
                                    "end_hub should be the first word")
                        except Exception as e:
                            print(e)
                            return False

                    if i == 2:
                        try:
                            int(line[i])
                        except Exception:
                            print("coordinate should be an integer")
                            return False

                    if i == 3:
                        try:
                            int(line[i])
                        except Exception:
                            print("coordinate should be an integer")
                            return False

                    if i == 4:
                        if line[i].startswith("color"):
                            color = line[i].split("=")[1]
                            colors = [
                                "blue", "red", "green", "orange", "yellow"]
                            try:
                                if color not in colors:
                                    raise Exception(
                                        "colors allowed are blue, red, "
                                        "green, orange and yellow")
                            except Exception as e:
                                print(e)
                                return False
                        else:
                            raise Exception("should start with color")

                    if i == 5:
                        if line[i].startswith("max_drones"):
                            max = line[i].split("=")[1]
                            try:
                                int(max)
                                if int(max) < 1:
                                    raise Exception("max_drones should be an "
                                                    "integer >= 1")
                            except Exception:
                                print("max_drones should be an integer >= 1")
                                return False

        return True
