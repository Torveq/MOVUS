import math

sudokuGrid = [[0,0,0,4],
              [0,0,0,0],
              [2,0,0,3],
              [4,0,1,2]]

size = len(sudokuGrid)

for row in range(size):
    print(sudokuGrid[row])

area = int(math.sqrt(size))

gridUpdated = True
while (gridUpdated):
    gridUpdated = False

    for target in range(1, size + 1):
        row = 0 
        while (row < size):
            col = 0
            while (col < size):
                foundTarget = False
                for r in range(row, row + area):
                    for c in range(col, col + area):
                        if (sudokuGrid[r][c] == target):
                            foundTarget = True
                            break
                if not foundTarget:
                    placeTargetAt = []

                    for r in range(row, row + area):
                        for c in range(col, col + area):
                            if (sudokuGrid[r][c] == 0):
                                currentRowValues = sudokuGrid[r]
                                currentColValues = [item[c] for item in sudokuGrid]

                                if target not in currentRowValues and target not in currentColValues:
                                    placeTargetAt.append([r, c])
                    if (len(placeTargetAt) == 1):
                        sudokuGrid[placeTargetAt[0][0]][placeTargetAt[0][1]] = target
                        gridUpdated = True  
                col += area
            row += area

print("\nThe Completed Sudoku")
for row in range(size):
    print(sudokuGrid[row])        
    