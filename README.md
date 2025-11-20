# Mamdani Policy Analysis: Monte Carlo Simulation

A comprehensive Monte Carlo simulation analyzing the fiscal implications of NYC mayoral candidate Zohran Mamdani's policy proposals.

## 🌐 Live Demo

**Try the interactive simulation now:**

👉 **[Launch Interactive App](https://mamdani-policy-montecarlo.streamlit.app/)** 👈

Explore different policy scenarios, adjust costs and revenues in real-time, and see immediate fiscal projections!

## Overview

This project uses advanced statistical modeling to assess whether Zohran Mamdani's progressive policy agenda is financially viable. By running thousands of simulations with varying cost and revenue parameters, we can quantify the probability of different fiscal outcomes and identify potential budget risks.

## Key Features

- **Monte Carlo Simulation**: 10,000+ simulations modeling policy costs with uncertainty
- **Statistical Analysis**: Probability distributions, confidence intervals, and risk metrics
- **Interactive Visualizations**: Beautiful plots using Plotly, Matplotlib, and Seaborn
- **Modular Architecture**: Clean, testable code following software engineering best practices
- **Comprehensive Documentation**: Detailed project plan and results analysis

## Policy Proposals Analyzed

1. **Free Public Transportation**: $700M annually
2. **Universal Free Childcare**: $6B annually (including wage increases)
3. **Affordable Housing Program**: $10B annually ($100B over 10 years)
4. **Government-Subsidized Grocery Stores**: $75M annually (5 stores)

**Total Estimated Cost**: ~$16.8B annually
**Proposed Revenue (Tax Increases)**: $10B annually

## Budget Threshold

The simulation tracks how often total policy costs exceed the **$2 billion threshold**, providing insights into fiscal risk and budget sustainability.

## Project Structure

```
politics_montecarlo/
├── src/
│   ├── config.py          # Configuration and constants
│   ├── parameters.py      # Policy parameter definitions
│   ├── simulation.py      # Monte Carlo simulation engine
│   └── visualization.py   # Plotting and visualizations
├── tests/
│   └── test_simulation.py # Unit tests
├── docs/
│   ├── project-plan.md    # Detailed methodology
│   └── results.md         # Analysis findings
├── results/               # Simulation outputs
├── main.py               # Entry point
└── requirements.txt      # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sakeeb91/mamdani-policy-montecarlo.git
cd mamdani-policy-montecarlo
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Monte Carlo simulation:

```bash
python main.py
```

This will:
1. Load policy parameters with uncertainty distributions
2. Run 10,000 Monte Carlo simulations
3. Generate statistical analysis
4. Create visualizations in the `results/` directory
5. Display summary statistics

### Command-line Options

```bash
python main.py --simulations 10000 --threshold 2.0 --seed 42
```

- `--simulations`: Number of Monte Carlo runs (default: 10000)
- `--threshold`: Budget threshold in billions (default: 2.0)
- `--seed`: Random seed for reproducibility (default: 42)

## Interactive Web Application 🌐

### 🚀 Live Application

**Access the live app here:** [https://mamdani-policy-montecarlo.streamlit.app/](https://mamdani-policy-montecarlo.streamlit.app/)

### 💻 Run Locally

To run on your own machine:

```bash
streamlit run app.py
```

### Features

The Streamlit web application provides:
- 🎛️ **Interactive Parameter Adjustment**: Modify policy costs and revenues in real-time
- 📊 **Live Simulation Results**: See results update as you change parameters
- 📋 **Policy Summaries**: Detailed explanations of each proposal with context
- 📈 **Beautiful Visualizations**: Interactive Plotly charts you can explore
- 💡 **Automated Insights**: Get recommendations based on your scenario

### Features of the Web App:
1. **Policy Overview Tab**: Learn about each of Mamdani's proposals with real-world context
2. **Simulation Results Tab**: View detailed statistics and probability analysis
3. **Visualizations Tab**: Explore interactive charts and distributions
4. **Insights Tab**: Get actionable recommendations based on results

The app allows you to answer questions like:
- "What if affordable housing only costs $8B instead of $10B?"
- "How much additional revenue would make the budget balanced?"
- "What if we phase in childcare at $3B initially?"

📘 **For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## Results

Simulation results include:

- **Probability Analysis**: Likelihood of exceeding budget threshold
- **Distribution Plots**: Histograms and density plots of total costs
- **Sensitivity Analysis**: Which policies contribute most to variance
- **Risk Metrics**: Confidence intervals and percentiles
- **Interactive Dashboards**: Explore scenarios with Plotly

See [docs/results.md](docs/results.md) for detailed findings and interpretation.

## Visualizations 📊

The simulation generates comprehensive visualizations to help understand the results:

### Sample Results Summary

From the base scenario (10,000 simulations):

| Metric | Value |
|--------|-------|
| **Mean Total Cost** | $16.77B |
| **Mean Revenue** | $10.01B |
| **Average Deficit** | $6.76B |
| **P(Cost > $2B)** | 100% |
| **Cost Range (90% CI)** | $13.80B - $19.78B |

**Policy Breakdown:**
- 🏘️ Affordable Housing: $9.98B (59.5%)
- 👶 Universal Childcare: $6.01B (35.8%)
- 🚌 Free Buses: $0.70B (4.2%)
- 🛒 Grocery Stores: $0.07B (0.4%)

### Generated Visualizations

The following visualizations are automatically created in the `results/` directory:

#### 1. Total Cost Distribution
- **File**: `total_costs_distribution.png`
- **Shows**: Histogram and box plot of total policy costs across all simulations
- **Key Elements**:
  - Distribution of possible outcomes
  - Mean cost line (green)
  - Budget threshold line (red)
  - Percentile ranges

**Key Insight**: Most simulations cluster around $16-17B with 90% of outcomes between $13.80B and $19.78B.

#### 2. Individual Policy Distributions
- **File**: `individual_policy_distributions.png`
- **Shows**: Separate histograms for each policy
- **Key Elements**:
  - Cost distribution for each program
  - Mean values marked
  - Comparison of variance across policies

**Key Insight**: Affordable Housing shows the widest distribution, indicating highest uncertainty and risk.

#### 3. Net Budget Impact
- **File**: `net_budget_impact.png`
- **Shows**: Analysis of costs minus revenues
- **Key Elements**:
  - Distribution of deficits/surpluses
  - Zero line (balanced budget)
  - Comparison bar chart of costs vs. revenue
  - Standard deviation error bars

**Key Insight**: Average $6.76B deficit reveals significant funding gap; virtually no simulations show balanced budget.

#### 4. Threshold Analysis
- **File**: `threshold_analysis.png`
- **Shows**: Probability of exceeding the $2B threshold
- **Key Elements**:
  - Cumulative distribution function
  - Threshold exceedance probability
  - Pie chart showing percentage above/below threshold

**Key Insight**: 100% of simulations exceed $2B threshold, indicating virtual certainty of high costs.

#### 5. Correlation Heatmap
- **File**: `correlation_heatmap.png`
- **Shows**: Correlations between policy costs
- **Key Elements**:
  - Policy-to-policy correlation matrix
  - Color-coded correlation strengths
  - Numerical correlation values

**Key Insight**: Policies are largely independent (by design), validating our modeling assumptions.

#### 6. Sensitivity Analysis
- **File**: `sensitivity_analysis.png`
- **Shows**: Which policies contribute most to total variance
- **Key Elements**:
  - Affordable Housing: 67% of total variance
  - Universal Childcare: 30% of variance
  - Other policies: <3% combined

**Key Insight**: Cost control in housing is critical for budget certainty. Small changes in housing costs have outsized impacts on total budget.

#### 7. Interactive Dashboard
- **File**: `interactive_dashboard.html`
- **Type**: Interactive Plotly dashboard
- **Features**:
  - Hover tooltips with exact values
  - Zoom and pan capabilities
  - Multiple coordinated views
  - Export to PNG functionality
  - Responsive design for all screen sizes

**To view**: Open `results/interactive_dashboard.html` in any web browser after running the simulation.

### Understanding the Visualizations

**Box Plot Guide:**
- **Box**: 25th to 75th percentile (middle 50% of data)
- **Line in box**: Median (50th percentile)
- **Whiskers**: Extend to min/max or 1.5× IQR
- **Dots**: Outliers beyond whiskers

**Histogram Guide:**
- **Bars**: Frequency of outcomes in each cost range
- **Height**: How often that cost occurred
- **Spread**: Wider = more uncertainty

**CDF (Cumulative Distribution) Guide:**
- **Y-axis**: Probability that cost is ≤ X-axis value
- **Steep sections**: Common outcomes
- **Flat sections**: Rare outcomes
- **Threshold intersection**: Probability of staying under threshold

## Methodology

Our Monte Carlo simulation:

1. **Defines probability distributions** for each policy cost based on expert estimates
2. **Samples from distributions** thousands of times to generate possible scenarios
3. **Calculates total costs** and net budget impact for each scenario
4. **Aggregates results** to compute probabilities and statistics
5. **Visualizes outcomes** with multiple chart types

Each policy parameter includes a standard deviation to account for uncertainty in cost estimates, ensuring realistic modeling of fiscal risk.

## Key Technologies

- **Python 3.9+**: Core language
- **NumPy**: Numerical computing and random sampling
- **SciPy**: Statistical distributions
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Statistical visualizations
- **Plotly**: Interactive plots and dashboards
- **Streamlit**: Interactive web application framework
- **Kaleido**: High-quality static image export

## Documentation

- [Project Plan](docs/project-plan.md): Detailed methodology and implementation approach
- [Results Analysis](docs/results.md): Findings, interpretation, and recommendations

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Contributing

This is an academic analysis project. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

**Sakeeb Rahman**
GitHub: [@Sakeeb91](https://github.com/Sakeeb91)
Email: rahman.sakeeb@gmail.com

## Acknowledgments

- Policy data sourced from Jacobin, THE CITY, CNN, and TIME
- Inspired by evidence-based policy analysis
- Built with modern Python data science stack

## Disclaimer

This analysis is for educational and informational purposes only. Cost estimates are based on publicly available information and include assumptions about implementation. Actual policy costs may vary significantly based on economic conditions, implementation details, and political decisions.

---

**Last Updated**: November 20, 2025
**Status**: Active Development

**For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**
