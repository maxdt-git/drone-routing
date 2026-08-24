graph = {
    "A": ["B", "C"],
    "B": ["A"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}


def dfs(
        graph: dict[str, list[str]],
        node: str,
        parent: dict[str, str | None],
        visited: set[str] | None=None) -> dict[str, str | None]:

    if visited is None:
        visited = set()

    visited.add(node)
    # print("je visite: ", node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            parent[neighbor] = node
            dfs(graph, neighbor, parent, visited)

    return parent


def path(parent: dict[str, str | None], end: str) -> list[str]:
    final_path: list[str] = []
    node = end
    while node is not None:
        final_path.append(node)
        node = parent[node]
    final_path.reverse()

    return final_path


def main() -> None:
    parent: dict[str, str | None] = {"A": None}
    dfs(graph, "A", parent)
    print(path(parent, "E"))


if __name__ == "__main__":
    main()
