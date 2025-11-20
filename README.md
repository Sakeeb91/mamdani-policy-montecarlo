# Mamdani Policy Analysis: Monte Carlo Simulation

A comprehensive Monte Carlo simulation analyzing the fiscal implications of NYC mayoral candidate Zohran Mamdani's policy proposals.

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

## Results

Simulation results include:

- **Probability Analysis**: Likelihood of exceeding budget threshold
- **Distribution Plots**: Histograms and density plots of total costs
- **Sensitivity Analysis**: Which policies contribute most to variance
- **Risk Metrics**: Confidence intervals and percentiles
- **Interactive Dashboards**: Explore scenarios with Plotly

See [docs/results.md](docs/results.md) for detailed findings and interpretation.

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
