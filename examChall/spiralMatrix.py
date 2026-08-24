def spiral_matrix(size: int) -> list[list[int]]:
    # remplir la matrice
    matrice = [[0 for _ in range(size)] for _ in range(size)]

    top = 0
    bottom = size - 1
    left = 0
    right = size - 1
    value = 1

    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            matrice[top][i] = value
            value += 1
        top += 1

        for i in range(top, bottom + 1):
            matrice[i][right] = value
            value += 1
        right -= 1

        # if top <= bottom:
        for i in range(right, left - 1, -1):
            matrice[bottom][i] = value
            value += 1
        bottom -= 1

        # if left <= right:
        for i in range(bottom, top - 1, -1):
            matrice[i][left] = value
            value += 1
        left += 1

    return matrice

if __name__ == "__main__":
    matrice = spiral_matrix(7)
    for i in range(7):
        print(matrice[i])
