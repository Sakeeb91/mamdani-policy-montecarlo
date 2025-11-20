"""
Configuration file for Mamdani Policy Monte Carlo Simulation
"""

# Simulation parameters
DEFAULT_NUM_SIMULATIONS = 10000
DEFAULT_RANDOM_SEED = 42
DEFAULT_BUDGET_THRESHOLD = 2.0  # in billions

# Output settings
RESULTS_DIR = "results"
FIGURE_DPI = 300
FIGURE_FORMAT = ["png", "html"]

# Statistical settings
CONFIDENCE_LEVEL = 0.95
PERCENTILES = [5, 25, 50, 75, 95]

# Visualization settings
COLOR_PALETTE = "husl"
PLOT_STYLE = "whitegrid"
FIGURE_SIZE = (12, 8)

# NYC Budget context (in billions)
NYC_CURRENT_BUDGET = 118.0
NYC_PROJECTED_DEFICIT = 4.7
NYC_FUTURE_BUDGET_GAP = 10.0

# Policy categories
POLICY_CATEGORIES = {
    "transportation": ["free_buses"],
    "social_services": ["universal_childcare"],
    "housing": ["affordable_housing"],
    "food_security": ["government_grocery_stores"]
}
