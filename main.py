from generator import Generator


def main() -> None:
    gen = Generator()
    map = gen.generate_map()
    if not map:
        return None
    print(f"\033[38;5;131m{map.start_hub}")


if __name__ == "__main__":
    main()
