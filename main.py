#!/usr/bin/env python3
"""
Main entry point for Mamdani Policy Monte Carlo Simulation

Usage:
    python main.py [--simulations N] [--threshold T] [--seed S]
"""

import argparse
import sys
import json
from pathlib import Path

from src.config import (
    DEFAULT_NUM_SIMULATIONS,
    DEFAULT_BUDGET_THRESHOLD,
    DEFAULT_RANDOM_SEED,
    RESULTS_DIR
)
from src.parameters import validate_parameters, get_total_policy_costs, get_policy_summary
from src.simulation import MonteCarloSimulator, run_sensitivity_analysis
from src.visualization import SimulationVisualizer


def parse_arguments():
    """
    Parse command-line arguments

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Monte Carlo simulation for Mamdani policy cost analysis'
    )

    parser.add_argument(
        '--simulations',
        type=int,
        default=DEFAULT_NUM_SIMULATIONS,
        help=f'Number of Monte Carlo simulations (default: {DEFAULT_NUM_SIMULATIONS})'
    )

    parser.add_argument(
        '--threshold',
        type=float,
        default=DEFAULT_BUDGET_THRESHOLD,
        help=f'Budget threshold in billions (default: {DEFAULT_BUDGET_THRESHOLD})'
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=DEFAULT_RANDOM_SEED,
        help=f'Random seed for reproducibility (default: {DEFAULT_RANDOM_SEED})'
    )

    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='Skip visualization generation'
    )

    return parser.parse_args()


def print_header():
    """
    Print application header
    """
    print("\n" + "=" * 70)
    print("MAMDANI POLICY ANALYSIS: MONTE CARLO SIMULATION")
    print("=" * 70)
    print("\nAnalyzing fiscal viability of NYC mayoral candidate")
    print("Zohran Mamdani's policy proposals\n")


def print_policy_overview():
    """
    Print overview of policies being analyzed
    """
    print("\n" + "-" * 70)
    print("POLICY OVERVIEW")
    print("-" * 70)

    summary = get_policy_summary()
    total_mean, total_std = get_total_policy_costs()

    for policy_key, stats in summary.items():
        print(f"\n{stats['name']}:")
        print(f"  Mean Cost: ${stats['mean']:.2f}B ± ${stats['std_dev']:.2f}B")
        print(f"  Range (±2σ): ${stats['min_estimate']:.2f}B - ${stats['max_estimate']:.2f}B")

    print(f"\nTotal Expected Cost: ${total_mean:.2f}B ± ${total_std:.2f}B")
    print(f"Proposed Revenue: $10.0B ± $1.5B (from tax increases)")
    print(f"Expected Budget Gap: ${total_mean - 10.0:.2f}B")


def save_results_to_json(results, sensitivity, output_dir: str = RESULTS_DIR):
    """
    Save results to JSON file

    Args:
        results: SimulationResults object
        sensitivity: Sensitivity analysis dictionary
        output_dir: Output directory
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    results_dict = {
        "statistics": results.statistics,
        "sensitivity": sensitivity
    }

    json_path = output_path / 'simulation_results.json'
    with open(json_path, 'w') as f:
        json.dump(results_dict, f, indent=2)

    print(f"\nResults saved to: {json_path}")


def main():
    """
    Main execution function
    """
    # Parse arguments
    args = parse_arguments()

    # Print header
    print_header()

    # Validate parameters
    try:
        validate_parameters()
        print("✓ Policy parameters validated")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Print policy overview
    print_policy_overview()

    # Create simulator
    simulator = MonteCarloSimulator(
        num_simulations=args.simulations,
        budget_threshold=args.threshold,
        random_seed=args.seed
    )

    print("\n" + "-" * 70)
    print("RUNNING SIMULATION")
    print("-" * 70)

    # Run simulation
    results = simulator.run_simulation()

    # Print summary
    simulator.print_summary(results)

    # Sensitivity analysis
    print("\n" + "-" * 70)
    print("SENSITIVITY ANALYSIS")
    print("-" * 70)
    sensitivity = run_sensitivity_analysis(simulator, results)

    # Save results to JSON
    save_results_to_json(results, sensitivity)

    # Generate visualizations
    if not args.no_viz:
        print("\n" + "-" * 70)
        print("GENERATING VISUALIZATIONS")
        print("-" * 70)

        visualizer = SimulationVisualizer(results)
        visualizer.create_all_visualizations()
        visualizer.plot_sensitivity_analysis(sensitivity)

        print("\n✓ All visualizations generated successfully!")
        print(f"\nOpen {RESULTS_DIR}/interactive_dashboard.html in your browser")
        print("to explore the interactive dashboard.")

    # Final message
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to: {RESULTS_DIR}/")
    print("\nKey Findings:")
    print(f"  • Probability of exceeding ${args.threshold}B threshold: "
          f"{results.statistics['threshold_analysis']['percentage']:.1f}%")
    print(f"  • Mean total cost: ${results.statistics['total_costs']['mean']:.2f}B")
    print(f"  • Mean budget impact: ${results.statistics['net_budget_impact']['mean']:.2f}B")

    if results.statistics['net_budget_impact']['mean'] > 0:
        print(f"\n⚠️  Policies create an average deficit of "
              f"${results.statistics['net_budget_impact']['mean']:.2f}B")
    else:
        print(f"\n✓ Policies are fully funded with an average surplus of "
              f"${-results.statistics['net_budget_impact']['mean']:.2f}B")

    print("\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
