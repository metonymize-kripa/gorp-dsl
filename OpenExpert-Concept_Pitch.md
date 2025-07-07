
## OpenExpert: Expert-Steered AI Applications

_“Expert knowledge. DSL-driven. Hosted once. Scalable forever.”_
Domain experts steer AI apps at the speed of thought — zero vendor lock-in, zero technical debt bloat.

### Purpose
**Empower domain experts** (non-engineers) to rapidly design, steer, and maintain AI-powered applications using a **Domain-Specific Language (DSL)** that sits between reusable standard libraries and an auto-generated user interface.

### Architecture
|**Layer**|**What It Does**|
|---|---|
|**1️⃣ User Interface Layer**|- Auto-generated UI (charts, sliders, buttons).- Exposes app functions to end-users.|
|**2️⃣ Domain-Specific Language (DSL) Layer**|- Encodes domain expertise and problem logic.- Connects UI with capabilities and data.|
|**3️⃣ Data/Capability Interop Layer**|- Connectors: Snowflake, Google Sheets, etc.- Libraries: OR-Tools (optimization), NeuralProphet (forecasting), others.|
|**Hosted Renderer**|- Executes the DSL spec.- Connects all parts securely.- Manages versioning and updates.|

### How It Works
1️⃣ **Expert writes DSL spec**
```
spec-v: 1.0
name: "Sales Forecast"
data:
  source: snowflake.sales
capabilities:
  - forecast: neuralprophet
ui:
  - chart: forecast.y_hat
  - slider: forecast.period
```
2️⃣ **Renderer spins up** secure connectors + libraries.
3️⃣ **UI auto-generates:** users see charts, sliders, buttons.
4️⃣ **Maintenance:** updates to libraries auto-propagate with DSL versioning.

### Key Benefits
|**ROI Factor**|**Value**|
|---|---|
|**Speed**|Rapid app development — experts build without engineers for every tweak.|
|**Reusability**|Standard libraries reused across domains.|
|**Consistency**|DSL generates consistent UIs automatically.|
|**Low TCO**|Hosted runtime manages updates, scaling, and security centrally.|

### **Design Principles**
- 🔗 **Modular:** UI, DSL, and capabilities are decoupled.
- 🔍 **Declarative:** Focus on ‘what’ not ‘how’.
- 🔄 **Extensible:** Plug in new capabilities/connectors easily.
- 🛡️ **Secure:** Data/auth handled via sandboxed connectors.
- 🗂️ **Maintainable:** Versioned DSL, standard test suite for libraries.

### Risks & Mitigations
|**Risk**|**Mitigation**|
|---|---|
|Library bugs|Versioning + rollback.|
|Security|Sandboxed runtime, RBAC.|
|Complexity creep|Minimal DSL syntax, clear affordance library.|

### Next Steps**
✅ Draft DSL for 1–2 domains (forecasting, optimization).
✅ Build hosted renderer MVP.
✅ Test with real experts + iterate.
✅ Establish library registry + versioning.

## Appendix: OpenExpert Vs DataRobot

|**Aspect**|**OpenExpert (Expert-Steered AI DSL)**|**DataRobot (AutoML)**|
|---|---|---|
|**Core Intent**|Let domain experts _design, steer,_ and _modify_ AI apps with reusable DSL & libraries.|Let analysts/data scientists _automate model selection, training,_ and _deployment_ with minimal coding.|
|**Customization**|High: DSL lets you define problem-specific logic, UI, data flow, capabilities.|Low/Medium: You adjust inputs & target variables, pick metrics, but underlying model pipelines are black-box.|
|**Ownership**|Hosted renderer + DSL versioning keeps logic transparent and modifiable.|Platform-owned pipelines; you rarely see full model code.|

## How It’s Designed
|**Aspect**|**Expert-Steered AI DSL**|**DataRobot**|
|---|---|---|
|**Modularity**|3 clear layers: UI ↔ DSL ↔ Capabilities/Interop; each can evolve separately.|Monolithic platform; UI is tied to their workflow.|
|**Extensibility**|Add new capabilities: OR-Tools, forecasting, simulation, optimizers.|Limited: You can tweak which algorithms are included; adding new external capabilities = hard.|
|**UI Surface**|Affordances (charts, sliders, buttons) generated automatically from DSL.|Basic dashboards; visualizations for model performance; no custom end-user UI.|
|**Data Interop**|Connect any source: Snowflake, Sheets, APIs via plug-in connectors.|Limited to built-in connectors or upload CSVs; more static.|

## Outcomes
|**Outcome**|**Expert-Steered AI DSL**|**DataRobot**|
|---|---|---|
|**Speed to Prototype**|Fast once DSL & renderer exist; experts iterate themselves.|Fast for training models — slow for building custom decision apps.|
|**Total Cost of Ownership (TCO)**|Lower: standard libraries + versioning avoid bloat.|Higher: subscription/seat pricing, plus model maintenance cost grows with use.|
|**Maintainability**|DSL specs versioned like code; you know what’s running.|Model versioning exists, but full app logic may be opaque.|
|**Governance**|Clear: domain knowledge encoded in DSL is auditable.|Harder: black-box models need separate interpretability tools.|

## Risks
|**Risk**|**Expert-Steered AI DSL**|**DataRobot**|
|---|---|---|
|**Complexity**|Too flexible for non-experts without good DSL design.|Too rigid: harder to embed AutoML in tailored workflows.|
|**Security**|Connector sandboxing required.|Data lives inside vendor cloud; governance depends on vendor trust.|
|**Vendor Lock-in**|Low: You control the hosted renderer.|High: DataRobot is fully closed-source; exit costs are real.|


## Takeaways

**👉 Use Expert-Steered DSL Architecture when:**
- You want reusable, domain-specific AI workflows that combine multiple capabilities (e.g., planning + forecasting + custom UI).
- Domain experts want to change logic often, without full rebuilds.
- You care about governance, modularity, and long-term TCO.

**👉 Use DataRobot when:**
- You want to quickly try multiple ML models on tabular data, with strong AutoML performance tuning and you’re OK with a mostly fixed workflow.
- You don’t need custom end-user apps or rich UI affordances.
- You have data science talent that wants fast baselines but will likely build production pipelines elsewhere.
