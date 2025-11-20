"""
Policy parameter definitions with uncertainty distributions
"""

import numpy as np
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class PolicyParameter:
    """
    Represents a policy with its cost distribution

    Attributes:
        name: Policy name
        mean: Mean annual cost in billions
        std_dev: Standard deviation in billions
        description: Policy description
        source: Data source
    """
    name: str
    mean: float
    std_dev: float
    description: str
    source: str

    def sample(self, size: int = 1, seed: int = None) -> np.ndarray:
        """
        Sample from the policy cost distribution

        Args:
            size: Number of samples to generate
            seed: Random seed for reproducibility

        Returns:
            Array of sampled costs (ensuring non-negative values)
        """
        if seed is not None:
            np.random.seed(seed)

        # Use normal distribution and truncate at zero (costs can't be negative)
        samples = np.random.normal(self.mean, self.std_dev, size)
        return np.maximum(samples, 0)


# Policy cost parameters (all values in billions USD)
POLICY_PARAMETERS = {
    "free_buses": PolicyParameter(
        name="Free Public Transportation",
        mean=0.7,
        std_dev=0.1,
        description="Free bus service for all NYC residents",
        source="Public estimates"
    ),

    "universal_childcare": PolicyParameter(
        name="Universal Free Childcare",
        mean=6.0,
        std_dev=1.0,
        description="Free childcare with increased wages for workers",
        source="High-end estimates with wage increases"
    ),

    "affordable_housing": PolicyParameter(
        name="Affordable Housing Program",
        mean=10.0,
        std_dev=1.5,
        description="$100B over 10 years, union labor, 200K units",
        source="Mamdani campaign proposal"
    ),

    "government_grocery_stores": PolicyParameter(
        name="Government-Subsidized Grocery Stores",
        mean=0.075,
        std_dev=0.025,
        description="5 government-run grocery stores (1 per borough)",
        source="Estimated from similar programs"
    )
}


# Revenue parameters
REVENUE_PARAMETERS = {
    "tax_increases": PolicyParameter(
        name="Tax Revenue Increases",
        mean=10.0,
        std_dev=1.5,
        description="2% tax on >$1M income + corporate tax increase to 11.5%",
        source="Mamdani campaign proposal"
    )
}


def get_total_policy_costs() -> Tuple[float, float]:
    """
    Calculate total mean and combined standard deviation for all policies

    Returns:
        Tuple of (mean_total, std_dev_total) in billions
    """
    mean_total = sum(param.mean for param in POLICY_PARAMETERS.values())

    # Assuming policies are independent, combine variances
    variance_total = sum(param.std_dev ** 2 for param in POLICY_PARAMETERS.values())
    std_dev_total = np.sqrt(variance_total)

    return mean_total, std_dev_total


def get_policy_summary() -> Dict[str, Dict[str, float]]:
    """
    Get summary statistics for all policies

    Returns:
        Dictionary with policy names and their statistics
    """
    summary = {}

    for key, param in POLICY_PARAMETERS.items():
        summary[key] = {
            "name": param.name,
            "mean": param.mean,
            "std_dev": param.std_dev,
            "min_estimate": max(0, param.mean - 2 * param.std_dev),
            "max_estimate": param.mean + 2 * param.std_dev
        }

    return summary


def validate_parameters() -> bool:
    """
    Validate that all parameters are properly configured

    Returns:
        True if all parameters are valid

    Raises:
        ValueError if any parameter is invalid
    """
    for key, param in {**POLICY_PARAMETERS, **REVENUE_PARAMETERS}.items():
        if param.mean < 0:
            raise ValueError(f"Parameter {key} has negative mean: {param.mean}")

        if param.std_dev < 0:
            raise ValueError(f"Parameter {key} has negative std_dev: {param.std_dev}")

        if param.std_dev > param.mean:
            print(f"Warning: {key} has std_dev > mean, may produce many zero values")

    return True


# Correlation matrix (for future enhancement)
# Currently assuming independence, but could model correlations
CORRELATION_MATRIX = None
