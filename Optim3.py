import copy


def north_west_algorithm(c_matrix, demand, supply):
    # North-West algorithm
    matrix = [[0 for j in range(len(demand))] for i in range(0,len(supply))]

    for i in range(0,len(supply)):
        for j in range(0,len(demand)):
            if matrix[i][j] != -1:
                matrix[i][j] = min(supply[i], demand[j])
                supply[i] -= matrix[i][j]
                demand[j] -= matrix[i][j]
                if supply[i] == 0: # i = row; j = column
                    for m in range(j+1,len(demand)):
                        matrix[i][m] = -1

                if demand[j] == 0:
                    for n in range(i+1,len(supply)):
                        matrix[n][j] = -1
    if supply[-1] != 0 or demand[-1] != 0:
        print("The method is not applicable!")
        return

    for i in range(0,len(supply)):
        for j in range(0,len(demand)):
            if matrix[i][j] == -1:
                matrix[i][j] = 0
            print(matrix[i][j],end=" ")
        print()


def condition(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                return False
    return True


def condition1(demand, supply):
    for i in range(len(supply)):
        if supply[i] != 0:
            return False
    for j in range(len(demand)):
        if demand[j] != 0:
            return False
    return True


def vogels_approximation_method(c_matrix, demand, supply):
    c_matrix_copy = copy.deepcopy(c_matrix)
    new_matrix = copy.deepcopy(c_matrix)
    new_matrix = [[0 for _ in i] for i in new_matrix]

    while not condition(c_matrix_copy):
        fines_row = [sorted([el for el in i if el != 0]) for i in c_matrix_copy]
        fines_row = [sorted_row[1] - sorted_row[0] if len(sorted_row) > 1 else (sorted_row[0] if len(sorted_row) == 1 else 0) for sorted_row in fines_row]

        fines_column = [sorted([el for el in j if el != 0]) for j in zip(*c_matrix_copy)]
        fines_column = [sorted_col[1] - sorted_col[0] if len(sorted_col) > 1 else (sorted_col[0] if len(sorted_col) == 1 else 0) for sorted_col in fines_column]

        max_el = max(max(fines_column), max(fines_row))
        if max_el == 0:
            break
        if max_el in fines_row:
            ind = fines_row.index(max_el)

            new_row = [el for el in c_matrix_copy[ind] if el != 0]
            if not new_row:
                return
            min_value = min(new_row)
            ind_in_matrix = c_matrix_copy[ind].index(min_value)

            # ind_in_matrix = c_matrix_copy[ind].index(min(c_matrix_copy[ind]))
            new_matrix[ind][ind_in_matrix] = min(demand[ind_in_matrix], supply[ind])
            demand[ind_in_matrix] -= new_matrix[ind][ind_in_matrix]
            supply[ind] -= new_matrix[ind][ind_in_matrix]
            if demand[ind_in_matrix] == 0:
                for i in c_matrix_copy:
                    i[ind_in_matrix] = 0
            if supply[ind] == 0:
                c_matrix_copy[ind] = [0 for j in range(len(demand))]
        else:
            ind = fines_column.index(max_el)
            new_col = []
            for i in c_matrix_copy:
                if i[ind] != 0:
                    new_col.append(i[ind])
            # new_col = [el for el in zip(*c_matrix_copy[ind]) if el != 0]
            if not new_col:
                return
            min_value = min(new_col)
            # min_value = min(row[ind] for row in c_matrix_copy)
            for i in c_matrix_copy:
                if i[ind] == min_value:
                    ind_in_matrix = c_matrix_copy.index(i)
                    break
            # ind_in_matrix = next(i for i, row in enumerate(c_matrix_copy) if row[ind] == min_value)
            new_matrix[ind_in_matrix][ind] = min(supply[ind_in_matrix], demand[ind])
            demand[ind] -= new_matrix[ind_in_matrix][ind]
            supply[ind_in_matrix] -= new_matrix[ind_in_matrix][ind]
            if supply[ind_in_matrix] == 0:
                c_matrix_copy[ind_in_matrix] = [0 for j in range(len(demand))]
            if demand[ind] == 0:
                for i in c_matrix_copy:
                    i[ind] = 0

        # for i in c_matrix_copy:
        #     for j in i:
        #         print(j,end=" ")
        #     print()

    for i in range(0,len(supply)):
        for j in range(0,len(demand)):
            print(new_matrix[i][j], end=" ")
        print()


def russels_approximation_method(c_matrix, demand, supply):
    c_matrix_copy = copy.deepcopy(c_matrix)
    new_matrix = copy.deepcopy(c_matrix)
    new_matrix = [[0 for _ in i] for i in new_matrix]

    while not condition1(demand, supply):
        c_matrix = copy.deepcopy(c_matrix_copy)
        max_row = [sorted([el for el in i if el != 0]) for i in c_matrix_copy]
        max_row = [sorted_max[-1] if len(sorted_max) >= 1 else 0 for sorted_max in max_row]

        max_col = [sorted([el for el in j if el != 0]) for j in zip(*c_matrix_copy)]
        max_col = [sorted_max[-1] if len(sorted_max) >= 1 else 0 for sorted_max in max_col]

        for i in range(len(c_matrix_copy)):
            for j in range(len(c_matrix_copy[i])):
                if supply[i] > 0 and demand[j] > 0:
                    c_matrix[i][j] -= (max_row[i] + max_col[j])
                else:
                    c_matrix[i][j] = 0

        max_value = 0
        for i in range(len(c_matrix)):
            for j in range(len(c_matrix[i])):
                if abs(c_matrix[i][j]) > max_value:
                    max_value = abs(c_matrix[i][j])
                    ind_row = i
                    ind_col = j
                elif abs(c_matrix[i][j]) == max_value:
                    if c_matrix_copy[i][j] < c_matrix_copy[ind_row][ind_col]:
                        ind_row = i
                        ind_col = j
                        max_value = abs(c_matrix[i][j])

        c_matrix_copy[ind_row][ind_col] = 0
        # c_matrix[ind_row][ind_col] = 0

        if max_value == 0:
            break
        if all(c_matrix_copy) == 0:
            break

        new_matrix[ind_row][ind_col] = min(demand[ind_col], supply[ind_row])
        demand[ind_col] -= new_matrix[ind_row][ind_col]
        supply[ind_row] -= new_matrix[ind_row][ind_col]

        if demand[ind_col] == 0:
            for i in range(len(c_matrix_copy)):
                c_matrix_copy[i][ind_col] = 0
                c_matrix[i][ind_col] = 0
        if supply[ind_row] == 0:
            c_matrix_copy[ind_row] = [0 for j in range(len(demand))]
            c_matrix[ind_row] = [0 for j in range(len(demand))]

    for i in range(0, len(supply)):
        for j in range(0, len(demand)):
            print(new_matrix[i][j], end=" ")
        print()


S = list(map(int, input().split()))
D = list(map(int, input().split()))
C = []
for i in range(0,len(S)):
    C.append(list(map(int, input().split())))

if any(el < 0 for i in C for el in i):
    print("The method is not applicable!")
    exit()

if sum(S) != sum(D):
    print("The problem is not balanced!")
    exit()

# Input parameter table
table = copy.deepcopy(C)
table.append(D)
width = [max(len(str(el)) for el in j) for j in zip(*table)]
for i in table:
    output = "| ".join(f"{str(el).rjust(w)}" for el, w in zip(i, width))
    print(output, end="| ")
    if table.index(i) < len(S):
        print(S[table.index(i)])
print()

# North-West corner method
north_west_algorithm(C.copy(), D.copy(), S.copy())
# Vogel’s approximation method
vogels_approximation_method(C.copy(), D.copy(), S.copy())
# Russell’s approximation method
russels_approximation_method(C.copy(), D.copy(), S.copy())