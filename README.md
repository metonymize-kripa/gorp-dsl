# gorp-dsl

A collection of optimization and forecasting examples using Google OR-Tools and NeuralProphet.

## Overview

This project demonstrates various optimization techniques and time series forecasting methods through practical examples:

- Linear programming optimization using [OR-Tools](https://github.com/google/or-tools)
- Constraint programming for nurse scheduling problems using [OR-Tools CP-SAT solver](https://developers.google.com/optimization/cp/cp_solver)
- Time series forecasting with [NeuralProphet](https://neuralprophet.com/)

## Requirements

- Python 3.12+
- Dependencies listed in pyproject.toml:
  - ortools
  - pandas
  - matplotlib
  - seaborn
  - neuralprophet
  - plotly
  - ipython

## Installation

```bash
# Clone the repository
git clone https://github.com/username/gorp-dsl.git
cd gorp-dsl

# Create and ync the virtual environment (optional but recommended)
```bash
uv sync
```

## Usage

The project contains several example scripts:

### Linear Programming Example

```bash
uv run main.py
```
Demonstrates a simple linear programming problem using OR-Tools' SCIP solver.

### Nurse Scheduling Example

```bash
uv run nurse_scheduler.py
```
Implements a constraint programming solution to the nurse scheduling problem with visualization using pandas and seaborn.

### Time Series Forecasting

```bash
uv run np_tester.py
```
Shows how to use NeuralProphet for time series forecasting with visualization.

## Features

- **Linear Programming**: Optimization with variables, constraints, and objective functions
- **Constraint Programming**: Complex scheduling problems with multiple constraints
- **Visualization**: Clear presentation of optimization results and forecasts
- **Time Series Analysis**: Forecasting using neural network-based prophet models

### Scheduling Pipeline DSL

The scheduling pipeline DSL is a declarative language that lets you stitch together data, forecast, geo, weather, and optimisation services in a single file. Read more about it in the [DSL concept](dsl_concept.md).

```bash
trucking_demo.yaml
```

illustrates how one might declare the scheduling pipeline DSL to solve a vehicle routing problem with multiple constraints.

## License

MIT