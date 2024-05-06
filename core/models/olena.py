import copy


# Вивід шапки для симплекс таблиці
def printHeaderTable(F):
    print("Ci", end="\t")
    for e in F:
        print(f"{e:<7}", end="")
    print("\n \t", end="")
    for i in range(0, len(F)):
        print(f"p{i+1:<6}", end="")
    print("b", end="\n\n")


# Вивід симплекс таблиці
def printTable(arr, ID, F, z, iteration):
    printLine()
    printHeaderTable(F)
    for i in range(0, len(arr)):
        print(f"P{ID[i]+1}", end="\t")
        for j in range(0, len(arr[i])):
            print(f"{arr[i][j]:<7.2f}", end="")
        print()
    print(f"Z{iteration}-C", end=" ")
    for i in range(0, len(z)):
        print(f"{z[i]:<7.2f}", end="")
    print()


def printLine():
    print("-" * 60)


# Пошук одиниці в масиві
def findOne(arr):
    n = len(arr) - 1
    while n >= 0:
        if arr[n] == 1:
            return n
        n -= 1
    return 0


# Знаходження базису
def getID(A):
    ID = []
    for e in A:
        ID.append(findOne(e))
    return ID


# Обчислення Zi-C
def sumplRow(A, F, ID):
    z = []
    for i in range(0, len(A[0])):
        z.append(0)
    for i in range(0, len(A[0])):
        for j in range(0, len(ID)):
            z[i] += A[j][i] * F[ID[j]]
        try:
            z[i] -= F[i]
        except:
            continue
    return z


def JordanGauss(A, ID):
    row = ID.index(0)
    divider = A[row][0]
    for i in range(0, len(A[row])):
        A[row][i] = A[row][i] / divider
    for i in range(0, len(A)):
        if i == row:
            continue
        multiplier = A[i][0]
        for j in range(0, len(A[i])):
            A[i][j] -= A[row][j] * multiplier
    return A


# Перевірка плану на оптимальність
def check(z):
    for i in range(0, len(z) - 1):
        if z[i] < 0:
            return False
    return True


# Перевірка чи план є цілочисловим
def checkInt(A):
    for i in range(0, len(A)):
        if A[i][-1] - int(A[i][-1]) != 0:
            return False
    return True


# Перевірка на правило А
def ruleA(z):
    max = 0
    j = -1
    for i in range(len(z)):
        if z[i] < 0 and abs(z[i]) >= max:
            max = abs(z[i])
            j = i
    return j


# Перевірка на правило B
def ruleB(A, n):
    min = float("inf")
    j = -1
    for i in range(0, len(A)):
        if A[i][n] != 0:  # Додано перевірку, щоб уникнути ділення на нуль
            temp = A[i][-1] / A[i][n]
            if temp > 0 and temp < min:
                min = temp
                j = i
    return j if j != -1 else None


def squareJordanGauss(A, rX, rY, eX, eY):
    if eX < rX and eY < rY:
        return float(A[eY][eX] - (A[rY][eX] * A[eY][rX] / A[rY][rX]))
    if eX > rX and eY < rY:
        return float(A[eY][eX] - (A[eY][rX] * A[rY][eX] / A[rY][rX]))
    if eX < rX and eY > rY:
        return float(A[eY][eX] - (A[rY][eX] * A[eY][rX] / A[rY][rX]))
    if eX > rX and eY > rY:
        return float(A[eY][eX] - (A[eY][rX] * A[rY][eX] / A[rY][rX]))


# Створення симплекс-таблиці з новим планом
def newTable(A, ID, rA, rB):
    newA = copy.deepcopy(A)
    dividerZ = A[rB][rA]
    for i in range(0, len(A[0])):  # Ділю рядок, де є розв'язувальний елемент
        newA[rB][i] /= dividerZ
    ID[rB] = rA  # Записую новий базис
    # Записуємо в симплекс таблицю базисні стовпці
    for k in range(0, len(ID)):
        for i in range(0, len(A[0]) - 1):
            for j in range(0, len(A)):
                if i in ID:
                    if k == j and i == ID[k]:
                        newA[j][i] = 1.0
                    elif k == j and i != ID[k]:
                        newA[j][i] = 0.0
    # за допомогою метода прямокутника Жордана-Гауса дописуємо нову симплекс таблицю
    for i in range(0, len(A[0])):
        for j in range(0, len(A)):
            if i not in ID:
                if j == rB:
                    continue
                newA[j][i] = squareJordanGauss(A, rA, rB, i, j)
    return newA


def createNewRow(A, row, b):
    newRow = []
    for i in range(0, len(A[row]) - 1):
        newRow.append(A[row][i] - int(A[row][i]))
    newRow.append(b)
    A.append(newRow)


def createNewColumn(A):
    insertIndexelement = len(A[0]) - 1
    for i in range(0, len(A) - 1):
        A[i].insert(insertIndexelement, 0)
    A[-1].insert(insertIndexelement, -1)


def JordanGauss2(A, ID, F):
    for row in range(0, len(F)):
        if row not in ID:
            break
    divider = A[row][row]
    for i in range(0, len(A[row])):
        A[row][i] = A[row][i] / divider
    for i in range(0, len(A)):
        if i == row:
            continue
        multiplier = A[i][row]
        for j in range(0, len(A[i])):
            A[i][j] -= A[row][j] * multiplier
    ID[-1] = row
    return A


def simplex(A, F, max_iterations=1000):
    ID = getID(A)
    iteration = 0
    while iteration < max_iterations:
        iteration += 1
        z = sumplRow(A, F, ID)
        if check(z):
            printTable(A, ID, F, z, iteration)
            if not checkInt(A):
                print(
                    "План оптимальний, але не цілочисельний, тому додаємо до нього нове обмеження\n"
                )
                max = 0.0
                indexMax = 0
                for i in range(0, len(A)):
                    if max < abs(A[i][-1] - int(A[i][-1])):
                        max = abs(A[i][-1] - int(A[i][-1]))
                        indexMax = i
                createNewRow(A, indexMax, max)
                createNewColumn(A)
                F.append(0.0)
                ID.append(len(F) - 1)
                A = JordanGauss2(A, ID, F)
            else:
                break
        else:
            rA = ruleA(z)
            if (
                rA == -1
            ):  # Якщо не знайдено від'ємних елементів у Zi-C, то вихід з циклу
                break
            rB = ruleB(A, rA)
            if rB is None:  # Якщо не знайдено розв'язувального рядка, то вихід з циклу
                print("Не знайдено розв'язувального рядка.")
                break
            A = newTable(A, ID, rA, rB)
    printTable(A, ID, F, z, iteration)
    return A, ID, F, z


def printAnswer(point, F, isMax=True):
    printLine()
    if isMax:
        answer = "F_max("
    else:
        answer = "F_min("
    for i in range(0, len(point)):
        answer += f"{point[i]}"
        if i != len(point) - 1:
            answer += ", "
    answer += f")={F}"
    print(answer)


def findMaxF(A, F):
    print("\n\n\t\t***Max***")
    point, maxF = simplex(A, F)
    printAnswer(point, maxF, True)


def findMinF(A, F):
    print("\n\n\t\t***Min***")
    for i in range(0, len(F)):
        F[i] *= -1
    point, minF = simplex(A, F)
    printAnswer(point, minF * (-1), False)


def printInfo():
    print("\t\t\t***Бичковський Ігор. КН-204. Варіант - 22***")
    print("Цільова функція:\n F = 2x1 + 6x2")
    print(
        "Обмеження:\n\
    8x1-5x2 <= 40,\n\
    2x1+5x2 >=10,\n\
    -6x1+5x2 <=60,\n\
    2x1+x2 <=14,\n\
    x1 >= 0, x2 >= 0"
    )
    print("\t\tКанонічна форма:")
    print("Цільова функція:\n F = 2x1 + 6x2->max")
    print(
        "Обмеження:\n\
    8x1-5x2+x3 = 40,\n\
    2x1+5x2-x4 = 10,\n\
    -6x1+5x2+x5 = 60,\n\
    2x1+x2+x6 =14,\n\
    x1, x2, x3, x4, x5, x6 >= 0"
    )


def main():
    printInfo()
    A = [
        [8.0, -5.0, 1.0, 0.0, 0.0, 0.0, 40.0],
        [2.0, 5.0, 0.0, -1.0, 0.0, 0.0, 10.0],
        [-6.0, 5.0, 0.0, 0.0, 1.0, 0.0, 60.0],
        [2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 14.0],
    ]

    F = [2.0, 6.0, 0.0, 0.0, 0.0, 0.0]
    findMaxF(copy.copy(A), copy.copy(F))
    findMinF(copy.copy(A), F)


# if __name__ == "__main__":
main()
