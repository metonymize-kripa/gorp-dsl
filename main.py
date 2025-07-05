from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
x = solver.IntVar(0, 10, 'x')
y = solver.IntVar(0, 10, 'y')
solver.Add(x + y <= 10)
solver.Maximize(2 * x + 3 * y)
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print(f'x = {x.solution_value()}')
    print(f'y = {y.solution_value()}')
    print(f'Maximum value = {solver.Objective().Value()}')
else:
    print('The problem does not have an optimal solution.')
    if status == pywraplp.Solver.INFEASIBLE:
        print('The problem is infeasible.')
    elif status == pywraplp.Solver.UNBOUNDED:
        print('The problem is unbounded.')
    else:
        print('Solver status:', status)
    print('Solver name:', solver.name())
    print('Solver version:', solver.version())
    print('Solver parameters:', solver.parameters())