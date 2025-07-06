"""
Adapter: DSL → OR‑Tools CP‑SAT
--------------------------------
Usage
-----
python dsl2cp.py <path_to_yaml>

• Parses the scheduling DSL (YAML v1.0)
• Builds a CP‑SAT model with standard rules implemented
• Solves and prints solutions (optionally visualises heat map)

Extend ‑ Add new rule handlers in `add_constraints()`.
"""

import sys
import pathlib
import argparse
import yaml
from typing import Dict, Tuple, List
from ortools.sat.python import cp_model

# ──────────────────────────────────────────────────────────────
# Helper – rule registry
# ──────────────────────────────────────────────────────────────

def add_constraints(model: cp_model.CpModel,
                    x: Dict[Tuple[int, int, int], cp_model.IntVar],
                    spec: dict,
                    days: range,
                    shifts: List[int],
                    nurses: List[str]):
    """Dispatch each rule found in spec["constraints"]."""

    rule_handlers = {
        "assign_exactly_one": _rule_assign_exactly_one,
        "at_most_one": _rule_at_most_one,
        "workload_balance": _rule_workload_balance,
        "equalized_shift_type": _rule_equalized_shift_type,
        "equal_days_worked": _rule_equal_days_worked,
    }

    for severity in ("hard", "soft"):
        for rule in spec.get("constraints", {}).get(severity, []):
            fn = rule_handlers.get(rule["rule"])
            if fn is None:
                raise ValueError(f"Unknown rule: {rule['rule']}")
            fn(model, x, rule, days, shifts, nurses, severity == "soft")

# ───── Rule implementations ─────

def _rule_assign_exactly_one(model, x, rule, days, shifts, nurses, soft):
    for d in days:
        for s in shifts:
            lits = [x[n_i, d, s] for n_i, _ in enumerate(nurses)]
            if soft:
                raise NotImplementedError("Soft version not implemented.")
            model.AddExactlyOne(lits)


def _rule_at_most_one(model, x, rule, days, shifts, nurses, soft):
    dim = rule["params"].get("dimension", "shift")
    if dim == "shift":
        for n_i, _ in enumerate(nurses):
            for d in days:
                lits = [x[n_i, d, s] for s in shifts]
                if soft:
                    raise NotImplementedError("Soft version not implemented.")
                model.AddAtMostOne(lits)
    elif dim == "nurse_day":
        # This dimension is effectively no‑op because every variable is already
        # unique per (nurse, day, shift). Implemented as >=1 if needed.
        pass
    else:
        raise ValueError(f"Unsupported dimension for at_most_one: {dim}")


def _rule_workload_balance(model, x, rule, days, shifts, nurses, soft):
    tol = rule.get("params", {}).get("tolerance", 1)
    total = len(days) * len(shifts)
    lo = total // len(nurses)
    hi = lo + (1 if total % len(nurses) else 0)
    lo -= tol
    hi += tol
    for n_i, _ in enumerate(nurses):
        expr = sum(x[n_i, d, s] for d in days for s in shifts)
        if soft:
            weight = rule.get("weight", 1)
            surplus = model.NewIntVar(0, total, f"surplus_{n_i}")
            deficit = model.NewIntVar(0, total, f"deficit_{n_i}")
            model.Add(expr - hi <= surplus)
            model.Add(lo - expr <= deficit)
            model.Minimize(weight * (surplus + deficit))
        else:
            model.Add(expr >= lo)
            model.Add(expr <= hi)


def _rule_equalized_shift_type(model, x, rule, days, shifts, nurses, soft):
    target_shifts = rule["params"]["shift_ids"]
    counts = []
    for n_i, _ in enumerate(nurses):
        c = model.NewIntVar(0, len(days) * len(target_shifts), f"cnt_n{n_i}")
        model.Add(c == sum(x[n_i, d, s] for d in days for s in target_shifts))
        counts.append(c)
    for c in counts[1:]:
        if soft:
            w = rule.get("weight", 1)
            diff = model.NewIntVar(0, len(days), "diff")
            model.Add(diff == counts[0] - c).OnlyEnforceIf(model.NewBoolVar("enf"))
            model.Minimize(w * diff)
        else:
            model.Add(c == counts[0])


def _rule_equal_days_worked(model, x, rule, days, shifts, nurses, soft):
    counts = []
    for n_i, _ in enumerate(nurses):
        worked_day = [model.NewBoolVar(f"wd_{n_i}_{d}") for d in days]
        for d, wd in zip(days, worked_day):
            model.AddMaxEquality(wd, [x[n_i, d, s] for s in shifts])
        cnt = model.NewIntVar(0, len(days), f"cnt_days_{n_i}")
        model.Add(cnt == sum(worked_day))
        counts.append(cnt)
    for c in counts[1:]:
        if soft:
            w = rule.get("weight", 1)
            diff = model.NewIntVar(0, len(days), "diff")
            model.Add(diff == counts[0] - c)
            model.Minimize(w * diff)
        else:
            model.Add(c == counts[0])

# ──────────────────────────────────────────────────────────────
# Heat‑map visualiser (optional)
# ──────────────────────────────────────────────────────────────

def show_heatmap(sol, x, nurses, days, shifts):
    try:
        import pandas as pd
    except ImportError:
        print("🔺 Install pandas for visualisation.")
        return

    records = [
        {"Day": d, "Shift": s, "Nurse": nurses[n_i]}
        for n_i in range(len(nurses))
        for d in days
        for s in shifts
        if sol.Value(x[n_i, d, s])
    ]
    if not records:
        return
        
    # Create a pivot table for better visualization
    df = pd.DataFrame(records).pivot(index="Day", columns="Shift", values="Nurse")
    
    # Print a formatted table
    print("\nNurse Assignment Table:")
    print("======================")
    print(df.to_string())
    print("======================")
    
    # Try to create a visual representation if possible
    try:
        import matplotlib.pyplot as plt
        
        # Create a simple table visualization
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('tight')
        ax.axis('off')
        
        # Create the table and add it to the plot
        table = ax.table(
            cellText=df.values,
            rowLabels=[f"Day {d}" for d in df.index],
            colLabels=[f"Shift {s}" for s in df.columns],
            cellLoc='center',
            loc='center'
        )
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        plt.title("Nurse Assignment Schedule")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Could not create visual table: {e}")
        # The text table is already printed, so we can continue

# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Solve scheduling DSL → CP‑SAT")
    parser.add_argument("yaml_file", type=pathlib.Path, help="DSL YAML spec")
    args = parser.parse_args()

    with args.yaml_file.open() as f:
        spec = yaml.safe_load(f)

    # Horizon & resources
    days = range(spec["horizon"]["days"])
    shifts = [s["id"] if isinstance(s, dict) else s for s in spec["horizon"]["shifts"]]
    nurses = spec["resources"]["nurses"].get("list") or [f"N{i}" for i in range(spec["resources"]["nurses"]["count"])]

    # Model & vars
    model = cp_model.CpModel()
    x = {(n_i, d, s): model.NewBoolVar(f"x_{n_i}_{d}_{s}")
         for n_i in range(len(nurses)) for d in days for s in shifts}

    # Constraints
    add_constraints(model, x, spec, days, shifts, nurses)

    # Solver params
    solver = cp_model.CpSolver()
    params = spec.get("solver", {}).get("parameters", {})
    
    # Handle solution_limit separately
    solution_limit = params.pop("solution_limit", None)
    
    # Set other parameters
    for k, v in params.items():
        setattr(solver.parameters, k, v)

    # Create a solution callback if solution_limit is specified
    if solution_limit is not None:
        class SolutionLimitCallback(cp_model.CpSolverSolutionCallback):
            def __init__(self, limit):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self._solution_count = 0
                self._solution_limit = limit

            def on_solution_callback(self):
                self._solution_count += 1
                if self._solution_count >= self._solution_limit:
                    print(f"Stop search after {self._solution_limit} solutions")
                    self.StopSearch()

        solution_callback = SolutionLimitCallback(solution_limit)
        result = solver.Solve(model, solution_callback)
    else:
        # Solve without callback
        result = solver.Solve(model)
        
    if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("❌ No solution found.")
        sys.exit(1)

    # Display solution
    print("\nSolution:")
    for d in days:
        for s in shifts:
            nurse = next(nurses[n_i] for n_i in range(len(nurses)) if solver.Value(x[n_i, d, s]))
            print(f"Day {d}, Shift {s}: {nurse}")
    show_heatmap(solver, x, nurses, days, shifts)

    print("\nStats: Conflicts =", solver.NumConflicts(), "Branches =", solver.NumBranches(), "Wall time =", solver.WallTime(), "s")

if __name__ == "__main__":
    main()
