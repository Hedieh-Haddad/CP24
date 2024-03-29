from pycsp3 import *

def WarOrPeace():
    with open('datavarval.txt', 'r') as f:
        varh = f.readline().strip()
        valh = f.readline().strip()
        phase = f.readline().strip()
        solver = f.readline().strip()
        restart = f.readline().strip()
        restartsequence = f.readline().strip()
        geocoef = f.readline().strip()

    n = data or 8
    WAR, PEACE = 0, 1
    x = VarArray(size=[n, n], dom=lambda i, j: {WAR, PEACE} if i < j else None)

    if not variant():
        satisfy((x[i][j] == PEACE) | (Sum((x[min(i, k)][max(i, k)] == WAR) & (x[min(j, k)][max(j, k)] == WAR) for k in range(n) if different_values(i, j, k)) == 0)
            for i, j in combinations(range(n), 2))
    elif variant("or"):
        satisfy((x[i][j] == PEACE) | ((x[i][j] == WAR) & conjunction((x[k][i] == PEACE) | (x[k][j] == PEACE) for k in range(i)))
            for i, j in combinations(range(1, n), 2))
    minimize(Sum(x))

    if solver == 'choco':
        if restart == "GEOMETRIC":
            solve(solver=solver,
                  options=f"-f -varh={varh} -valh={valh} -best -last -lc 1 -restarts [GEOMETRIC,{restartsequence},{geocoef},50000,true]")  # -restarts [GEOMETRIC,500,0,50000,true]
        elif restart == "luby":
            solve(solver=solver,
                  options=f"-f -varh={varh} -valh={valh} -best -last -lc 1 -restarts [luby,{restartsequence},0,50000,true]")

    elif solver == 'ace':
        if restart == "GEOMETRIC":
            solve(solver=solver, options=f"-varh={varh} -valh={valh} -r_n={restartsequence} -ref="" ")
        elif restart == "luby":
            solve(solver=solver, options=f"-varh={varh} -valh={valh} -luby -r_n={restartsequence} -ref="" ")
    print("NSolution", n_solutions())
    print("Objective", bound())
    print("Status", status())
    print("Solution", solution())
    return n_solutions(), bound(), status(), solution()

WarOrPeace()