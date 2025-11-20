"""
Unit tests for Monte Carlo simulation
"""

import unittest
import numpy as np

from src.parameters import (
    PolicyParameter,
    POLICY_PARAMETERS,
    REVENUE_PARAMETERS,
    get_total_policy_costs,
    validate_parameters
)
from src.simulation import MonteCarloSimulator
from src.config import DEFAULT_BUDGET_THRESHOLD


class TestPolicyParameter(unittest.TestCase):
    """Test PolicyParameter class"""

    def test_parameter_creation(self):
        """Test creating a policy parameter"""
        param = PolicyParameter(
            name="Test Policy",
            mean=5.0,
            std_dev=1.0,
            description="Test description",
            source="Test source"
        )

        self.assertEqual(param.name, "Test Policy")
        self.assertEqual(param.mean, 5.0)
        self.assertEqual(param.std_dev, 1.0)

    def test_parameter_sampling(self):
        """Test sampling from parameter distribution"""
        param = PolicyParameter(
            name="Test Policy",
            mean=5.0,
            std_dev=1.0,
            description="Test",
            source="Test"
        )

        samples = param.sample(size=1000, seed=42)

        self.assertEqual(len(samples), 1000)
        self.assertTrue(np.all(samples >= 0))  # All samples should be non-negative
        self.assertAlmostEqual(np.mean(samples), 5.0, delta=0.2)

    def test_parameter_validation(self):
        """Test parameter validation"""
        self.assertTrue(validate_parameters())


class TestMonteCarloSimulator(unittest.TestCase):
    """Test MonteCarloSimulator class"""

    def test_simulator_initialization(self):
        """Test simulator initialization"""
        simulator = MonteCarloSimulator(
            num_simulations=100,
            budget_threshold=2.0,
            random_seed=42
        )

        self.assertEqual(simulator.num_simulations, 100)
        self.assertEqual(simulator.budget_threshold, 2.0)
        self.assertEqual(simulator.random_seed, 42)

    def test_simulation_run(self):
        """Test running simulation"""
        simulator = MonteCarloSimulator(
            num_simulations=100,
            budget_threshold=2.0,
            random_seed=42
        )

        results = simulator.run_simulation()

        # Check results structure
        self.assertEqual(len(results.total_costs), 100)
        self.assertEqual(len(results.revenues), 100)
        self.assertEqual(len(results.net_budget_impact), 100)

        # Check all costs are non-negative
        self.assertTrue(np.all(results.total_costs >= 0))
        self.assertTrue(np.all(results.revenues >= 0))

        # Check statistics are present
        self.assertIn('total_costs', results.statistics)
        self.assertIn('revenues', results.statistics)
        self.assertIn('net_budget_impact', results.statistics)
        self.assertIn('threshold_analysis', results.statistics)

    def test_threshold_analysis(self):
        """Test threshold exceedance calculation"""
        simulator = MonteCarloSimulator(
            num_simulations=1000,
            budget_threshold=2.0,
            random_seed=42
        )

        results = simulator.run_simulation()

        # Most simulations should exceed $2B threshold
        # (since mean total cost is ~$16.8B)
        exceedance_rate = results.statistics['threshold_analysis']['probability']
        self.assertGreater(exceedance_rate, 0.95)  # Should be > 95%

    def test_statistics_calculation(self):
        """Test statistics calculation"""
        simulator = MonteCarloSimulator(
            num_simulations=1000,
            budget_threshold=2.0,
            random_seed=42
        )

        results = simulator.run_simulation()
        stats = results.statistics

        # Check mean is reasonable
        total_mean = stats['total_costs']['mean']
        expected_mean, _ = get_total_policy_costs()
        self.assertAlmostEqual(total_mean, expected_mean, delta=1.0)

        # Check that percentiles are ordered
        percentiles = stats['total_costs']['percentiles']
        prev_val = 0
        for p in [5, 25, 50, 75, 95]:
            self.assertGreater(percentiles[p], prev_val)
            prev_val = percentiles[p]


class TestPolicyParameters(unittest.TestCase):
    """Test policy parameter definitions"""

    def test_all_policies_defined(self):
        """Test that all expected policies are defined"""
        expected_policies = [
            'free_buses',
            'universal_childcare',
            'affordable_housing',
            'government_grocery_stores'
        ]

        for policy in expected_policies:
            self.assertIn(policy, POLICY_PARAMETERS)

    def test_revenue_parameters_defined(self):
        """Test that revenue parameters are defined"""
        self.assertIn('tax_increases', REVENUE_PARAMETERS)

    def test_policy_costs_reasonable(self):
        """Test that policy costs are reasonable"""
        for policy_key, param in POLICY_PARAMETERS.items():
            # All costs should be positive
            self.assertGreater(param.mean, 0)
            self.assertGreater(param.std_dev, 0)

            # Standard deviation shouldn't be too large relative to mean
            self.assertLess(param.std_dev, param.mean * 2)

    def test_total_cost_calculation(self):
        """Test total cost calculation"""
        mean_total, std_total = get_total_policy_costs()

        # Total should be sum of individual means
        expected_mean = sum(p.mean for p in POLICY_PARAMETERS.values())
        self.assertAlmostEqual(mean_total, expected_mean, places=2)

        # Check that combined std dev is calculated
        self.assertGreater(std_total, 0)


if __name__ == '__main__':
    unittest.main()
