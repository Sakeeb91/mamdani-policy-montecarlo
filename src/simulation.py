"""
Monte Carlo simulation engine for policy cost analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from scipy import stats

from .parameters import POLICY_PARAMETERS, REVENUE_PARAMETERS
from .config import (
    DEFAULT_NUM_SIMULATIONS,
    DEFAULT_BUDGET_THRESHOLD,
    CONFIDENCE_LEVEL,
    PERCENTILES
)


@dataclass
class SimulationResults:
    """
    Container for simulation results

    Attributes:
        policy_costs: DataFrame with costs for each policy in each simulation
        total_costs: Array of total costs for each simulation
        revenues: Array of revenues for each simulation
        net_budget_impact: Array of net impact (costs - revenues)
        threshold_exceedances: Number of times threshold was exceeded
        statistics: Dictionary of summary statistics
    """
    policy_costs: pd.DataFrame
    total_costs: np.ndarray
    revenues: np.ndarray
    net_budget_impact: np.ndarray
    threshold_exceedances: int
    statistics: Dict


class MonteCarloSimulator:
    """
    Monte Carlo simulator for policy cost analysis
    """

    def __init__(
        self,
        num_simulations: int = DEFAULT_NUM_SIMULATIONS,
        budget_threshold: float = DEFAULT_BUDGET_THRESHOLD,
        random_seed: Optional[int] = None
    ):
        """
        Initialize the Monte Carlo simulator

        Args:
            num_simulations: Number of simulation runs
            budget_threshold: Budget threshold in billions
            random_seed: Random seed for reproducibility
        """
        self.num_simulations = num_simulations
        self.budget_threshold = budget_threshold
        self.random_seed = random_seed

        if random_seed is not None:
            np.random.seed(random_seed)

    def run_simulation(self) -> SimulationResults:
        """
        Run the Monte Carlo simulation

        Returns:
            SimulationResults object with all results
        """
        print(f"Running {self.num_simulations:,} Monte Carlo simulations...")

        # Initialize storage for results
        policy_costs_dict = {}

        # Sample costs for each policy
        for policy_key, policy_param in POLICY_PARAMETERS.items():
            costs = policy_param.sample(size=self.num_simulations)
            policy_costs_dict[policy_key] = costs
            print(f"  Sampled {policy_param.name}: μ={costs.mean():.3f}B, σ={costs.std():.3f}B")

        # Sample revenues
        revenue_param = REVENUE_PARAMETERS["tax_increases"]
        revenues = revenue_param.sample(size=self.num_simulations)
        print(f"  Sampled {revenue_param.name}: μ={revenues.mean():.3f}B, σ={revenues.std():.3f}B")

        # Convert to DataFrame
        policy_costs_df = pd.DataFrame(policy_costs_dict)

        # Calculate total costs
        total_costs = policy_costs_df.sum(axis=1).values

        # Calculate net budget impact (positive means deficit)
        net_budget_impact = total_costs - revenues

        # Count threshold exceedances
        threshold_exceedances = np.sum(total_costs > self.budget_threshold)

        # Calculate statistics
        statistics = self._calculate_statistics(
            policy_costs_df, total_costs, revenues, net_budget_impact, threshold_exceedances
        )

        print("\nSimulation complete!")

        return SimulationResults(
            policy_costs=policy_costs_df,
            total_costs=total_costs,
            revenues=revenues,
            net_budget_impact=net_budget_impact,
            threshold_exceedances=threshold_exceedances,
            statistics=statistics
        )

    def _calculate_statistics(
        self,
        policy_costs: pd.DataFrame,
        total_costs: np.ndarray,
        revenues: np.ndarray,
        net_budget_impact: np.ndarray,
        threshold_exceedances: int
    ) -> Dict:
        """
        Calculate comprehensive statistics from simulation results

        Returns:
            Dictionary of statistics
        """
        stats_dict = {
            "num_simulations": self.num_simulations,
            "budget_threshold": self.budget_threshold,

            # Total costs
            "total_costs": {
                "mean": float(np.mean(total_costs)),
                "median": float(np.median(total_costs)),
                "std": float(np.std(total_costs)),
                "min": float(np.min(total_costs)),
                "max": float(np.max(total_costs)),
                "percentiles": {
                    p: float(np.percentile(total_costs, p))
                    for p in PERCENTILES
                }
            },

            # Revenues
            "revenues": {
                "mean": float(np.mean(revenues)),
                "median": float(np.median(revenues)),
                "std": float(np.std(revenues)),
                "min": float(np.min(revenues)),
                "max": float(np.max(revenues))
            },

            # Net budget impact
            "net_budget_impact": {
                "mean": float(np.mean(net_budget_impact)),
                "median": float(np.median(net_budget_impact)),
                "std": float(np.std(net_budget_impact)),
                "min": float(np.min(net_budget_impact)),
                "max": float(np.max(net_budget_impact)),
                "percentiles": {
                    p: float(np.percentile(net_budget_impact, p))
                    for p in PERCENTILES
                }
            },

            # Threshold analysis
            "threshold_analysis": {
                "exceedances": int(threshold_exceedances),
                "probability": float(threshold_exceedances / self.num_simulations),
                "percentage": float(100 * threshold_exceedances / self.num_simulations)
            },

            # Confidence intervals
            "confidence_intervals": self._calculate_confidence_intervals(
                total_costs, revenues, net_budget_impact
            ),

            # Individual policy statistics
            "policy_statistics": {
                policy_key: {
                    "mean": float(policy_costs[policy_key].mean()),
                    "std": float(policy_costs[policy_key].std()),
                    "median": float(policy_costs[policy_key].median())
                }
                for policy_key in policy_costs.columns
            }
        }

        return stats_dict

    def _calculate_confidence_intervals(
        self,
        total_costs: np.ndarray,
        revenues: np.ndarray,
        net_budget_impact: np.ndarray
    ) -> Dict:
        """
        Calculate confidence intervals for key metrics

        Returns:
            Dictionary of confidence intervals
        """
        alpha = 1 - CONFIDENCE_LEVEL

        def ci(data):
            mean = np.mean(data)
            sem = stats.sem(data)
            interval = stats.t.interval(CONFIDENCE_LEVEL, len(data) - 1, loc=mean, scale=sem)
            return {"lower": float(interval[0]), "upper": float(interval[1])}

        return {
            "total_costs": ci(total_costs),
            "revenues": ci(revenues),
            "net_budget_impact": ci(net_budget_impact)
        }

    def print_summary(self, results: SimulationResults):
        """
        Print summary of simulation results

        Args:
            results: SimulationResults object
        """
        stats = results.statistics

        print("\n" + "=" * 70)
        print("MONTE CARLO SIMULATION RESULTS SUMMARY")
        print("=" * 70)

        print(f"\nSimulations run: {stats['num_simulations']:,}")
        print(f"Budget threshold: ${stats['budget_threshold']:.1f}B")

        print("\n--- TOTAL POLICY COSTS ---")
        print(f"Mean:   ${stats['total_costs']['mean']:.2f}B")
        print(f"Median: ${stats['total_costs']['median']:.2f}B")
        print(f"Std:    ${stats['total_costs']['std']:.2f}B")
        print(f"Range:  ${stats['total_costs']['min']:.2f}B - ${stats['total_costs']['max']:.2f}B")

        print("\nPercentiles:")
        for p, value in stats['total_costs']['percentiles'].items():
            print(f"  {p}th: ${value:.2f}B")

        print("\n--- REVENUE PROJECTIONS ---")
        print(f"Mean:   ${stats['revenues']['mean']:.2f}B")
        print(f"Median: ${stats['revenues']['median']:.2f}B")
        print(f"Std:    ${stats['revenues']['std']:.2f}B")

        print("\n--- NET BUDGET IMPACT (Cost - Revenue) ---")
        print(f"Mean:   ${stats['net_budget_impact']['mean']:.2f}B")
        print(f"Median: ${stats['net_budget_impact']['median']:.2f}B")
        print(f"Std:    ${stats['net_budget_impact']['std']:.2f}B")

        if stats['net_budget_impact']['mean'] > 0:
            print(f"\n⚠️  Average deficit: ${stats['net_budget_impact']['mean']:.2f}B")
        else:
            print(f"\n✓ Average surplus: ${-stats['net_budget_impact']['mean']:.2f}B")

        print("\n--- THRESHOLD ANALYSIS ---")
        print(f"Times exceeded ${stats['budget_threshold']:.1f}B: {stats['threshold_analysis']['exceedances']:,}")
        print(f"Probability: {stats['threshold_analysis']['probability']:.4f}")
        print(f"Percentage: {stats['threshold_analysis']['percentage']:.2f}%")

        print("\n--- CONFIDENCE INTERVALS (95%) ---")
        ci = stats['confidence_intervals']
        print(f"Total Costs: ${ci['total_costs']['lower']:.2f}B - ${ci['total_costs']['upper']:.2f}B")
        print(f"Net Impact:  ${ci['net_budget_impact']['lower']:.2f}B - ${ci['net_budget_impact']['upper']:.2f}B")

        print("\n--- INDIVIDUAL POLICY COSTS ---")
        for policy_key, policy_stats in stats['policy_statistics'].items():
            policy_name = POLICY_PARAMETERS[policy_key].name
            print(f"{policy_name}:")
            print(f"  Mean: ${policy_stats['mean']:.2f}B, Std: ${policy_stats['std']:.2f}B")

        print("\n" + "=" * 70)


def run_sensitivity_analysis(
    base_simulator: MonteCarloSimulator,
    results: SimulationResults
) -> Dict:
    """
    Perform sensitivity analysis to identify which policies drive the most variance

    Args:
        base_simulator: The base simulator configuration
        results: Base simulation results

    Returns:
        Dictionary with sensitivity analysis results
    """
    print("\nPerforming sensitivity analysis...")

    sensitivity = {}
    base_variance = np.var(results.total_costs)

    # For each policy, calculate how much it contributes to total variance
    for policy_key in results.policy_costs.columns:
        policy_variance = np.var(results.policy_costs[policy_key])
        contribution = policy_variance / base_variance
        sensitivity[policy_key] = {
            "variance": float(policy_variance),
            "contribution_to_total": float(contribution),
            "percentage": float(100 * contribution)
        }

    # Sort by contribution
    sensitivity = dict(
        sorted(sensitivity.items(), key=lambda x: x[1]['contribution_to_total'], reverse=True)
    )

    print("\nVariance contribution by policy:")
    for policy_key, sens in sensitivity.items():
        policy_name = POLICY_PARAMETERS[policy_key].name
        print(f"  {policy_name}: {sens['percentage']:.1f}%")

    return sensitivity
