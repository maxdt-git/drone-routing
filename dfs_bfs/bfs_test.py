from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}


def bfs(graph: dict[str, list[str]], start: str) -> dict[str, str | None]:
    visited = {start}
    queue = deque([start])
    parent: dict[str, str | None] = {start: None}

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

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
    un = bfs(graph, "A")
    print(un)
    deux = path(un, "E")
    print(deux)


if __name__ == "__main__":
    main()
