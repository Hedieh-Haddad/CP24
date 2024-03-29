"""
See Problem 034 on CSPLib

Examples of Execution:
  python3 Warehouse.py -data=Warehouse_example.json
  python3 Warehouse.py -data=Warehouse_example.txt -dataparser=Warehouse_Parser.py
  python3 Warehouse.py -data=Warehouse_example.txt -dataparser=Warehouse_Parser.py -variant=compact
"""

from pycsp3 import *

def Warehouse():
    with open('datavarval.txt', 'r') as f:
        varh = f.readline().strip()
        valh = f.readline().strip()
        phase = f.readline().strip()
        solver = f.readline().strip()
        restart = f.readline().strip()
        restartsequence = f.readline().strip()
        geocoef = f.readline().strip()

    cost, capacities, costs = data  # cost is the fixed cost when opening a warehouse
    nWarehouses, nStores = len(capacities), len(costs)

    # w[i] is the warehouse supplying the ith store
    w = VarArray(size=nStores, dom=range(nWarehouses))

    satisfy(
        # capacities of warehouses must not be exceeded
        Count(w, value=j) <= capacities[j] for j in range(nWarehouses)
    )

    if not variant():
        # c[i] is the cost of supplying the ith store
        c = VarArray(size=nStores, dom=lambda i: costs[i])

        # o[j] is 1 if the jth warehouse is open
        o = VarArray(size=nWarehouses, dom={0, 1})

        satisfy(
            # the warehouse supplier of the ith store must be open
            [o[w[i]] == 1 for i in range(nStores)],

            # computing the cost of supplying the ith store
            [costs[i][w[i]] == c[i] for i in range(nStores)]
        )

        minimize(
            # minimizing the overall cost
            Sum(c) + Sum(o) * cost
        )

    elif variant("compact"):
        minimize(
            # minimizing the overall cost
            Sum(costs[i][w[i]] for i in range(nStores)) + NValues(w) * cost
        )

    """ Comments
    1) when compiling the 'compact' variant, some auxiliary variables are automatically introduced
       in order to remain in the perimeter of XCP3-core   
    """
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


Warehouse()