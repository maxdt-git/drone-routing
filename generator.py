from parsing import Parser, Zone
import sys


class Generator:
    def __init__(self) -> None:
        self.conf = Parser()
        self.parsed = self.conf.extract_dict(sys.argv[1])

    def generate_hub_list(self) -> list[dict[str, Zone]] | None:
        if not self.parsed:
            return None
        hub_list: list[dict[str, Zone]] = []
        max = 1
        if self.conf.parse_hub(self.parsed):
            for key in self.parsed:
                if key == "start_hub":
                    line = self.parsed[key].replace(
                        "[", "").replace("]", "").split(" ")
                    name = line[1]
                    x = int(line[2])
                    y = int(line[3])
                    color = line[4].split("=")[1]
                    max = int(line[5].split("=")[1]) if len(line) > 5 else int(self.parsed["nb_drones"])
                    start = Zone(name, x, y, color=color, max_drones=max)
                    hub_list.append({"start": start})

                if key.startswith("hub"):
                    line = self.parsed[key].replace("[", "").replace("]", "").split(" ")
                    name = line[1]
                    x = int(line[2])
                    y = int(line[3])
                    color = line[4].split("=")[1]
                    if len(line) > 5:
                        max = int(line[5].split("=")[1]) if line[5].startswith("max_drones") else 1
                    start = Zone(name, x, y, color=color, max_drones=max)
                    hub_list.append({f"{line[1]}": start})

                if key == "end_hub":
                    line = self.parsed["end_hub"].replace(
                        "[", "").replace("]", "").split(" ")
                    name = line[1]
                    x = int(line[2])
                    y = int(line[3])
                    color = line[4].split("=")[1]
                    if line[5]:
                        max = int(line[5].split("=")[1])
                    end = Zone(name, x, y, color=color, max_drones=max)
                    hub_list.append({"end": end})

        return hub_list


def main() -> None:
    # conf = Parser()
    gen = Generator()
    hub_list = gen.generate_hub_list()
    if not hub_list:
        return None
    print(hub_list)

if __name__ == "__main__":
    main()
