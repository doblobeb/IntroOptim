import math

C = [int(i) for i in input().split()]
k = True
A = []
while (k):
    b = [int(i) for i in input().split()]
    if (len(b) > 1):
        A.append(b)
    else:
        acc = b
        b = A[-1]
        A = A[:-1]
        k = False

global pivots
pivots = []
global l
l = len(A)
global kl
kl = len(A[0])

C = C + [0] * (l + 1)
for i in range(l):
    A[i] += [0] * l
    A[i] += [b[i]]
    A[i][kl + i] = 1

MaxC = [-i for i in C]
MinC = [i for i in C]

Table1 = A + [MaxC]
Table2 = A + [MinC]

basic_vars = [f"s{i + 1}" for i in range(l)]
non_basic_vars = [f"x{i + 1}" for i in range(kl)]


def Pivot(Table):
    PivotC = min([i for i in Table[-1] if i < 0])
    PivotC_id = Table[-1].index(PivotC)
    Ratio = []
    for i in range(len(Table) - 1):
        if (Table[i][PivotC_id] > 0):
            Ratio.append(Table[i][-1] / Table[i][PivotC_id])
        else:
            Ratio.append(99999999)
    PivotR = min([i for i in Ratio if i > 0])
    PivotR_id = Ratio.index(PivotR)
    return (PivotC_id, PivotR_id)


def new_table(Table):
    New_Table = []
    for i in range(len(Table)):
        c = []
        for j in range(len(Table[0])):
            c.append(0)
        New_Table.append(c)

    return (New_Table)


def Simplex(Table):
    g = 0
    while (True):
        g += 1
        if (min(Table[-1]) >= 0):
            return (Table)
        New_Table = new_table(Table)
        C, R = Pivot(Table)
        pivots.append(C)

        basic_vars[R] = non_basic_vars[C]

        for i in range(len(Table[R])):
            if (Table[R][C] != 0):
                New_Table[R][i] = Table[R][i] / Table[R][C]
            else:
                New_Table[R][i] = 0

        for i in range(len(Table)):
            if (i != R):
                for j in range(len(Table[0])):
                    New_Table[i][j] = Table[i][j] - Table[i][C] * New_Table[R][j]

        if (min(New_Table[-1]) >= 0):
            return (New_Table)
        if (g > 200):
            print("The method is not applicable!")
            return 0
        Table = New_Table


k = Simplex(Table1)
if (k != 0):
    print("max = " + str(round(float(k[-1][-1]), acc[0])))
    for i in k[-1][:-1]:
        print(round(i, acc[0]), end=" ")
    print()
    for i in range(len(k) - 1):
        if (basic_vars[i] != str('s' + str(i + 1))):
            print(f"{basic_vars[i]} = {round(k[i][-1], acc[0])}", end=" ")
    print()

    for var in non_basic_vars:
        if var not in basic_vars:
            print(f"{var} = 0", end=" ")
    print()
    print("-----------------------------------")

k = Simplex(Table2)
if (k != 0):
    print("min = " + str(round(float(k[-1][-1]), acc[0])))
    for i in k[-1][:-1]:
        print(round(i,acc[0]),end=" ")
    print()
    for i in range(len(k) - 1):
        if (basic_vars[i] != str('s' + str(i + 1))):
            print(f"{basic_vars[i]} = {round(k[i][-1], acc[0])}", end=" ")
    print()
    for var in non_basic_vars:
        if var not in basic_vars:
            print(f"{var} = 0", end=" ")
    print()