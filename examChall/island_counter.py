def count_island(matrix: list[list[str]]) -> int:

    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def dfs(r: int, c: int) -> None:

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if visited[r][c] or matrix[r][c] != "1":
            return

        visited[r][c] = True

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1" and not visited[r][c]:
                count += 1
                dfs(r, c)

    return count


def main() -> None:
    grid = [
    ["1", "1", "1", "0", "1"],
    ["1", "1", "0", "1", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"],
]
    print(count_island(grid))


if __name__ == "__main__":
    main()
