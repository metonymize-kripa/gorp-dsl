Scheduling-Pipeline DSL (Version 2.0)

This README explains the ideas embodied in the trucking_demo.yaml example and how the domain-specific language (DSL) lets you stitch together data, forecast, geo, weather, and optimisation services in a single declarative file.

⸻

1  What Problem Does the Example Solve?

Scenario A mid-west cross-dock operator must allocate four tractor-trailers to deliver goods to 25 stores over the next three days.  Good plans must account for:
	•	expected demand at each store (forecast)
	•	driving distances & times (Google Maps)
	•	disruptive winter weather (NOAA /NWS)
	•	driver hours-of-service rules (optimisation constraints)

Goal Minimise total kilometres while respecting labour rules and avoiding risky weather.

The YAML file expresses every step—from pulling historic orders to solving the vehicle-routing problem—without a single line of Python.

⸻

2  Core Concept: Pipeline ≈ Directed Acyclic Graph of Capability Blocks

 data  →  forecast  →  geo  →  weather  →  optimise
│orders │demand fc │distances│snow risk │route plan

Each stage:
	1.	uses one horizontal capability block (data, forecast, geo, weather, optimize).
	2.	with parameters specific to that block.
	3.	produces a typed object (table, matrix, JSON) that later stages can reference by alias.

Because all blocks share a thin schema, they can be recomposed for trucking, retail, healthcare, or any other vertical.

⸻

3  YAML Walk-through

Stage ID	Block	Purpose	Key Params
orders_raw	data	Pull 90 days of order history from Snowflake.	sql, conn
demand_fc	forecast	Fit NeuralProphet per store; predict 14 days ahead.	target_col, horizon
store_coords	geo (geocoding)	Turn store addresses into lat/lon for routing & weather.	api_key_ref
dist_matrix	geo (distance)	Google Maps Distance Matrix between all stops.	mode: distance_matrix
wx_risk	weather	NOAA forecast → snow/ice probability score for next 3 days.	risk_metric
route_plan	optimize	OR-Tools CP-SAT model producing a 3-day vehicle plan.	constraints, objective

Resulting artefacts cascade—e.g. route_plan consumes the distance matrix and demand forecast, plus a penalty for high wx_risk zones.

⸻

4  Quick Start

# 1. Install libraries (conda or venv recommended)
pip install ortools neuralprophet snowflake-connector-python \
            googlemaps pandas pyyaml matplotlib seaborn

# 2. Set secrets (Snowflake creds, Google Maps key, etc.)
export SNOWFLAKE_DEMO_USER=…
export SNOWFLAKE_DEMO_PASSWORD=…
export GOOGLE_MAPS_KEY=…

# 3. Run the adapter
python dsl2cp.py trucking_demo.yaml

The adapter topologically sorts the pipeline, streams logs per stage, and finally prints a roster plus a heat-map visualisation of vehicle assignments.

⸻

5  How to Customise for Another Domain

If you need…	Change this field	Example
Different data warehouse	orders_raw.conn	BIGQUERY_US_EAST
Longer forecast horizon	demand_fc.horizon	28d
Alternative distance source	Replace geo stage with OpenStreetMap block	uses: geo-osrm
Extra constraints	Add rules under route_plan.constraints	driver_break_every: {hours: 4}

Because each block is a plug-in, you rarely touch Python—just add a YAML stage and a corresponding plug-in class.

⸻

6  Extending the DSL
	1.	New capability block → write a plug-in subclass with run() and schema(); register it under a unique uses: tag.
	2.	New optimisation rule → implement handler in dsl2cp.py::add_constraints() and reference it in YAML.
	3.	Validation → add the rule to the JSON-Schema so typos fail early.

⸻

7  Known Limitations / Roadmap
	•	Secrets handling is environment-variable only → replace with Vault / AWS SM.
	•	Error paths are naive; failures stop the whole pipeline—support retries & skip-on-error.
	•	Parallel execution not yet implemented; DAG currently runs serially.
	•	UI planned: VS Code plugin that offers auto-complete based on schema.

⸻

8  License

Apache-2.0 for the DSL & adapter.

⸻

Happy planning!  Open an issue or PR if you add a new block so others can reuse it.
