# Mamdani Policy Analysis: Monte Carlo Simulation Project Plan

## Project Overview

This project uses Monte Carlo simulation to analyze the fiscal viability of NYC mayoral candidate Zohran Mamdani's policy proposals. By running hundreds of simulations with varying parameters, we can assess the probability of costs exceeding the $2 billion threshold and understand the range of possible fiscal outcomes.

## Objectives

1. Model Mamdani's major policy proposals with realistic cost estimates
2. Account for uncertainty in cost projections using statistical distributions
3. Run Monte Carlo simulations to generate probability distributions of outcomes
4. Visualize results to understand fiscal risks and opportunities
5. Provide data-driven insights on policy affordability

## Policy Parameters

### Major Policies (Annual Costs in Billions)

| Policy | Mean Cost | Std Dev | Distribution | Source |
|--------|-----------|---------|--------------|---------|
| Free Buses | $0.7B | $0.1B | Normal | Public estimates |
| Universal Free Childcare | $6.0B | $1.0B | Normal | High-end estimates with wage increases |
| Affordable Housing | $10.0B | $1.5B | Normal | $100B over 10 years |
| Government Grocery Stores | $0.075B | $0.025B | Normal | Estimated for 5 stores |

### Revenue Parameters

| Source | Mean Revenue | Std Dev | Distribution |
|--------|--------------|---------|--------------|
| Tax Increases | $10.0B | $1.5B | Normal |

### Budget Threshold

- **Critical Threshold**: $2.0B (tracking frequency of exceeding this amount)
- **Context**: NYC current budget ~$118B with $4.7B deficit projection

## Methodology

### 1. Parameter Setup
- Define probability distributions for each policy cost
- Use normal distributions with means and standard deviations
- Account for correlation between some variables (e.g., housing costs and inflation)

### 2. Monte Carlo Simulation
- Run 10,000 simulations
- For each simulation:
  - Sample from each policy cost distribution
  - Calculate total cost
  - Calculate net budget impact (costs - revenues)
  - Track threshold exceedances

### 3. Analysis Metrics
- Probability of exceeding $2B threshold
- Mean, median, and percentile values for total costs
- Distribution of net budget impact
- Sensitivity analysis: which policies drive most variance

### 4. Visualization
- Histogram of total cost distribution
- Box plots for individual policy costs
- Time series of cumulative probability
- Heatmap showing correlation between variables
- Interactive plots using Plotly

## Technical Architecture

### Project Structure
```
politics_montecarlo/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration and constants
│   ├── parameters.py      # Policy parameter definitions
│   ├── simulation.py      # Core Monte Carlo logic
│   └── visualization.py   # Plotting and visualization
├── tests/
│   ├── __init__.py
│   └── test_simulation.py # Unit tests
├── docs/
│   ├── project-plan.md    # This file
│   └── results.md         # Analysis results
├── results/               # Output directory
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── README.md            # Project documentation
```

### Key Components

#### 1. `config.py`
- Global configuration
- Simulation parameters (number of runs, random seed)
- Budget thresholds

#### 2. `parameters.py`
- Policy cost distributions
- Revenue distributions
- Parameter validation

#### 3. `simulation.py`
- `MonteCarloSimulator` class
- Sampling methods
- Result aggregation
- Statistical analysis

#### 4. `visualization.py`
- Multiple plotting functions
- Plotly for interactive visualizations
- Seaborn for statistical plots
- Export to PNG/PDF/HTML

#### 5. `main.py`
- CLI interface
- Orchestrates simulation workflow
- Generates reports

## Implementation Steps

1. **Setup** (Phase 1)
   - Create project structure
   - Set up version control
   - Install dependencies

2. **Core Implementation** (Phase 2)
   - Implement parameter definitions
   - Build Monte Carlo simulator
   - Add statistical analysis functions

3. **Visualization** (Phase 3)
   - Create plotting modules
   - Design interactive dashboards
   - Export functionality

4. **Testing & Validation** (Phase 4)
   - Unit tests for all components
   - Validate statistical properties
   - Sensitivity testing

5. **Documentation** (Phase 5)
   - Complete README
   - Document results
   - Create usage examples

## Expected Outcomes

1. **Probability Analysis**
   - P(Total Cost > $2B threshold)
   - Distribution of net fiscal impact
   - Confidence intervals

2. **Risk Assessment**
   - Identify high-variance policies
   - Quantify downside risk
   - Budget gap scenarios

3. **Policy Insights**
   - Which policies are most affordable
   - Revenue sufficiency analysis
   - Recommendations for prioritization

## Future Enhancements

1. Add time-series analysis (multi-year projections)
2. Include economic scenarios (recession, growth)
3. Model policy interdependencies
4. Add more sophisticated distributions (skewed, multimodal)
5. Web dashboard for interactive exploration
6. Comparison with alternative policy packages

## Dependencies

- Python 3.9+
- NumPy: Numerical computing
- SciPy: Statistical distributions
- Pandas: Data manipulation
- Matplotlib/Seaborn: Statistical plotting
- Plotly: Interactive visualizations
- Kaleido: Static image export

## References

1. Jacobin: "Mayor Mamdani's Budget Can Add Up"
2. THE CITY: "Adams Boosts Budget, Leaving a $4.7 Billion Hole for Mamdani"
3. CNN: "Here's a look at Zohran Mamdani's policy ideas"
4. TIME: "Can Mamdani Fulfill His Ambitious Campaign Promises?"

---

**Last Updated**: November 20, 2025
**Status**: Implementation Phase
