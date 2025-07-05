"""Example of a simple nurse scheduling problem with clear helper nodes and visualization."""

from ortools.sat.python import cp_model
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main() -> None:
    # ===============================
    # [1] Problem Data
    # ===============================
    num_nurses = 4
    num_shifts = 3
    num_days = 3
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    print(f"=== Nurse Scheduling ===")
    print(f"  - Nurses: {num_nurses}")
    print(f"  - Shifts per day: {num_shifts}")
    print(f"  - Days: {num_days}")

    # ===============================
    # [2] Create CP-SAT Model
    # ===============================
    model = cp_model.CpModel()

    # ===============================
    # [3] Create Decision Variables
    # ===============================
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")

    # ===============================
    # [4] Hard Constraints
    # ===============================

    # (a) Each shift on each day is assigned to exactly one nurse
    for d in all_days:
        for s in all_shifts:
            model.add_exactly_one(shifts[(n, d, s)] for n in all_nurses)

    # (b) Each nurse works at most one shift per day
    for n in all_nurses:
        for d in all_days:
            model.add_at_most_one(shifts[(n, d, s)] for s in all_shifts)

    # (c) Each nurse should have a fair workload
    total_shifts = num_shifts * num_days
    min_shifts_per_nurse = total_shifts // num_nurses
    max_shifts_per_nurse = min_shifts_per_nurse + (1 if total_shifts % num_nurses != 0 else 0)

    for n in all_nurses:
        shifts_worked = []
        for d in all_days:
            for s in all_shifts:
                shifts_worked.append(shifts[(n, d, s)])
        model.add(sum(shifts_worked) >= min_shifts_per_nurse)
        model.add(sum(shifts_worked) <= max_shifts_per_nurse)

    print(f"  - Shifts per nurse: {min_shifts_per_nurse}-{max_shifts_per_nurse}")

    # ===============================
    # [5] Solver Setup
    # ===============================
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    solver.parameters.enumerate_all_solutions = True

    # ===============================
    # [6] Solution Printer with Visualization
    # ===============================
    class NursesVisualSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Collect and visualize solutions."""

        def __init__(self, shifts, num_nurses, num_days, num_shifts, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_nurses = num_nurses
            self._num_days = num_days
            self._num_shifts = num_shifts
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            self._solution_count += 1
            print(f"\n=== Solution {self._solution_count} ===")
            records = []
            for d in range(self._num_days):
                for s in range(self._num_shifts):
                    for n in range(self._num_nurses):
                        if self.Value(self._shifts[(n, d, s)]):
                            records.append({"Day": d, "Shift": s, "Nurse": n})

            df = pd.DataFrame(records)
            print(df)

            # Pivot to Day vs Shift with Nurse numbers
            pivot = df.pivot(index="Day", columns="Shift", values="Nurse")
            print("\nPivot table: Nurse assigned to each (Day, Shift)")
            print(pivot)

            # Heatmap
            plt.figure(figsize=(8, 4))
            sns.heatmap(
                pivot,
                annot=True,
                fmt=".0f",
                cmap="YlGnBu",
                cbar=False,
                linewidths=0.5,
                linecolor='gray'
            )
            plt.title(f"Nurse Assignment Heatmap (Solution {self._solution_count})")
            plt.xlabel("Shift")
            plt.ylabel("Day")
            plt.show()

            if self._solution_count >= self._solution_limit:
                print(f"Stop search after {self._solution_limit} solutions")
                self.StopSearch()

        def solutionCount(self):
            return self._solution_count

    # ===============================
    # [7] Solve
    # ===============================
    solution_limit = 3
    solution_printer = NursesVisualSolutionPrinter(
        shifts, num_nurses, num_days, num_shifts, solution_limit
    )

    solver.Solve(model, solution_printer)

    # ===============================
    # [8] Solver Statistics
    # ===============================
    print("\n=== Solver Statistics ===")
    print(f"  - Conflicts      : {solver.NumConflicts()}")
    print(f"  - Branches       : {solver.NumBranches()}")
    print(f"  - Wall time (s)  : {solver.WallTime():.2f}")
    print(f"  - Solutions found: {solution_printer.solutionCount()}")


if __name__ == "__main__":
    main()