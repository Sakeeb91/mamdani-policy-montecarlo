"""
Visualization module for Monte Carlo simulation results
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
from typing import Optional

from .simulation import SimulationResults
from .parameters import POLICY_PARAMETERS
from .config import (
    RESULTS_DIR,
    FIGURE_DPI,
    COLOR_PALETTE,
    PLOT_STYLE,
    FIGURE_SIZE
)


class SimulationVisualizer:
    """
    Create visualizations for Monte Carlo simulation results
    """

    def __init__(self, results: SimulationResults, output_dir: str = RESULTS_DIR):
        """
        Initialize visualizer

        Args:
            results: SimulationResults object
            output_dir: Directory to save figures
        """
        self.results = results
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Set style
        sns.set_style(PLOT_STYLE)
        sns.set_palette(COLOR_PALETTE)

    def create_all_visualizations(self):
        """
        Create all visualization plots
        """
        print("\nGenerating visualizations...")

        self.plot_total_costs_distribution()
        self.plot_individual_policy_distributions()
        self.plot_net_budget_impact()
        self.plot_threshold_analysis()
        self.plot_correlation_heatmap()
        self.create_interactive_dashboard()

        print(f"\nAll visualizations saved to: {self.output_dir}")

    def plot_total_costs_distribution(self):
        """
        Plot distribution of total policy costs
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZE)

        # Histogram with KDE
        ax1.hist(
            self.results.total_costs,
            bins=50,
            density=True,
            alpha=0.7,
            color='steelblue',
            edgecolor='black'
        )

        # Add KDE line
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(self.results.total_costs)
        x_range = np.linspace(
            self.results.total_costs.min(),
            self.results.total_costs.max(),
            200
        )
        ax1.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE')

        # Add threshold line
        threshold = self.results.statistics['budget_threshold']
        ax1.axvline(
            threshold,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Threshold: ${threshold}B'
        )

        # Add mean line
        mean_cost = self.results.statistics['total_costs']['mean']
        ax1.axvline(
            mean_cost,
            color='green',
            linestyle='--',
            linewidth=2,
            label=f'Mean: ${mean_cost:.2f}B'
        )

        ax1.set_xlabel('Total Policy Cost (Billions USD)', fontsize=12)
        ax1.set_ylabel('Density', fontsize=12)
        ax1.set_title('Distribution of Total Policy Costs', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Box plot
        ax2.boxplot(
            self.results.total_costs,
            vert=True,
            patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5)
        )

        # Add threshold line
        ax2.axhline(
            threshold,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Threshold: ${threshold}B'
        )

        ax2.set_ylabel('Total Policy Cost (Billions USD)', fontsize=12)
        ax2.set_title('Total Costs: Box Plot', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig(
            self.output_dir / 'total_costs_distribution.png',
            dpi=FIGURE_DPI,
            bbox_inches='tight'
        )
        plt.close()

        print("  ✓ Total costs distribution plot saved")

    def plot_individual_policy_distributions(self):
        """
        Plot distributions for each individual policy
        """
        n_policies = len(self.results.policy_costs.columns)
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        for idx, (policy_key, policy_data) in enumerate(self.results.policy_costs.items()):
            ax = axes[idx]

            # Histogram
            ax.hist(
                policy_data,
                bins=30,
                alpha=0.7,
                color=sns.color_palette()[idx],
                edgecolor='black'
            )

            # Add mean line
            mean_val = policy_data.mean()
            ax.axvline(
                mean_val,
                color='red',
                linestyle='--',
                linewidth=2,
                label=f'Mean: ${mean_val:.2f}B'
            )

            policy_name = POLICY_PARAMETERS[policy_key].name
            ax.set_xlabel('Cost (Billions USD)', fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.set_title(policy_name, fontsize=11, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)

        plt.suptitle(
            'Individual Policy Cost Distributions',
            fontsize=16,
            fontweight='bold',
            y=1.00
        )
        plt.tight_layout()
        plt.savefig(
            self.output_dir / 'individual_policy_distributions.png',
            dpi=FIGURE_DPI,
            bbox_inches='tight'
        )
        plt.close()

        print("  ✓ Individual policy distributions plot saved")

    def plot_net_budget_impact(self):
        """
        Plot net budget impact (costs - revenues)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZE)

        # Distribution plot
        ax1.hist(
            self.results.net_budget_impact,
            bins=50,
            alpha=0.7,
            color='coral',
            edgecolor='black'
        )

        # Add zero line
        ax1.axvline(0, color='green', linestyle='--', linewidth=2, label='Balanced Budget')

        # Add mean line
        mean_impact = self.results.statistics['net_budget_impact']['mean']
        ax1.axvline(
            mean_impact,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Mean: ${mean_impact:.2f}B'
        )

        ax1.set_xlabel('Net Budget Impact (Billions USD)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Net Budget Impact Distribution', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Stacked comparison: costs vs revenues
        categories = ['Total Costs', 'Total Revenues']
        means = [
            self.results.statistics['total_costs']['mean'],
            self.results.statistics['revenues']['mean']
        ]
        stds = [
            self.results.statistics['total_costs']['std'],
            self.results.statistics['revenues']['std']
        ]

        x_pos = np.arange(len(categories))
        colors = ['#e74c3c', '#27ae60']

        bars = ax2.bar(x_pos, means, yerr=stds, capsize=10, alpha=0.7, color=colors, edgecolor='black')

        ax2.set_xlabel('Category', fontsize=12)
        ax2.set_ylabel('Amount (Billions USD)', fontsize=12)
        ax2.set_title('Costs vs. Revenues', fontsize=14, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(categories)
        ax2.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar, mean_val in zip(bars, means):
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'${mean_val:.2f}B',
                ha='center',
                va='bottom',
                fontweight='bold'
            )

        plt.tight_layout()
        plt.savefig(
            self.output_dir / 'net_budget_impact.png',
            dpi=FIGURE_DPI,
            bbox_inches='tight'
        )
        plt.close()

        print("  ✓ Net budget impact plot saved")

    def plot_threshold_analysis(self):
        """
        Plot threshold exceedance analysis
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZE)

        # Cumulative distribution
        sorted_costs = np.sort(self.results.total_costs)
        cumulative_prob = np.arange(1, len(sorted_costs) + 1) / len(sorted_costs)

        ax1.plot(sorted_costs, cumulative_prob, linewidth=2, color='steelblue')

        # Add threshold line
        threshold = self.results.statistics['budget_threshold']
        ax1.axvline(
            threshold,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'Threshold: ${threshold}B'
        )

        # Calculate and show probability at threshold
        prob_at_threshold = np.sum(sorted_costs <= threshold) / len(sorted_costs)
        ax1.axhline(
            prob_at_threshold,
            color='red',
            linestyle=':',
            linewidth=1.5,
            alpha=0.5
        )

        ax1.set_xlabel('Total Policy Cost (Billions USD)', fontsize=12)
        ax1.set_ylabel('Cumulative Probability', fontsize=12)
        ax1.set_title('Cumulative Distribution Function', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Pie chart: above/below threshold
        exceedances = self.results.statistics['threshold_analysis']['exceedances']
        below_threshold = self.results.statistics['num_simulations'] - exceedances

        sizes = [below_threshold, exceedances]
        labels = [
            f'Below Threshold\n({below_threshold:,} runs)',
            f'Above Threshold\n({exceedances:,} runs)'
        ]
        colors = ['#27ae60', '#e74c3c']
        explode = (0, 0.1)

        ax2.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            textprops={'fontsize': 11}
        )
        ax2.set_title(
            f'Threshold Exceedance Analysis\n(${threshold}B threshold)',
            fontsize=14,
            fontweight='bold'
        )

        plt.tight_layout()
        plt.savefig(
            self.output_dir / 'threshold_analysis.png',
            dpi=FIGURE_DPI,
            bbox_inches='tight'
        )
        plt.close()

        print("  ✓ Threshold analysis plot saved")

    def plot_correlation_heatmap(self):
        """
        Plot correlation heatmap between policies
        """
        # Create correlation matrix
        corr_matrix = self.results.policy_costs.corr()

        # Rename columns for display
        display_names = {
            key: POLICY_PARAMETERS[key].name
            for key in corr_matrix.columns
        }
        corr_matrix = corr_matrix.rename(columns=display_names, index=display_names)

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.3f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={'shrink': 0.8},
            ax=ax
        )

        ax.set_title(
            'Policy Cost Correlation Matrix',
            fontsize=14,
            fontweight='bold',
            pad=20
        )

        plt.tight_layout()
        plt.savefig(
            self.output_dir / 'correlation_heatmap.png',
            dpi=FIGURE_DPI,
            bbox_inches='tight'
        )
        plt.close()

        print("  ✓ Correlation heatmap saved")

    def create_interactive_dashboard(self):
        """
        Create interactive Plotly dashboard
        """
        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                'Total Cost Distribution',
                'Individual Policy Costs',
                'Net Budget Impact',
                'Cumulative Distribution'
            ),
            specs=[
                [{"type": "histogram"}, {"type": "box"}],
                [{"type": "histogram"}, {"type": "scatter"}]
            ]
        )

        # 1. Total cost histogram
        fig.add_trace(
            go.Histogram(
                x=self.results.total_costs,
                name='Total Costs',
                nbinsx=50,
                marker_color='steelblue',
                opacity=0.7
            ),
            row=1,
            col=1
        )

        # Add threshold line
        threshold = self.results.statistics['budget_threshold']
        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Threshold: ${threshold}B",
            row=1,
            col=1
        )

        # 2. Box plots for individual policies
        for policy_key, policy_data in self.results.policy_costs.items():
            policy_name = POLICY_PARAMETERS[policy_key].name
            fig.add_trace(
                go.Box(
                    y=policy_data,
                    name=policy_name,
                    boxmean='sd'
                ),
                row=1,
                col=2
            )

        # 3. Net budget impact histogram
        fig.add_trace(
            go.Histogram(
                x=self.results.net_budget_impact,
                name='Net Impact',
                nbinsx=50,
                marker_color='coral',
                opacity=0.7
            ),
            row=2,
            col=1
        )

        # Add zero line
        fig.add_vline(x=0, line_dash="dash", line_color="green", row=2, col=1)

        # 4. Cumulative distribution
        sorted_costs = np.sort(self.results.total_costs)
        cumulative_prob = np.arange(1, len(sorted_costs) + 1) / len(sorted_costs)

        fig.add_trace(
            go.Scatter(
                x=sorted_costs,
                y=cumulative_prob,
                mode='lines',
                name='CDF',
                line=dict(color='steelblue', width=2)
            ),
            row=2,
            col=2
        )

        # Add threshold line
        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            row=2,
            col=2
        )

        # Update layout
        fig.update_layout(
            title_text="Mamdani Policy Analysis: Interactive Dashboard",
            title_font_size=20,
            showlegend=True,
            height=800,
            template="plotly_white"
        )

        # Update axes labels
        fig.update_xaxes(title_text="Total Cost (Billions USD)", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=1)

        fig.update_yaxes(title_text="Cost (Billions USD)", row=1, col=2)

        fig.update_xaxes(title_text="Net Budget Impact (Billions USD)", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)

        fig.update_xaxes(title_text="Total Cost (Billions USD)", row=2, col=2)
        fig.update_yaxes(title_text="Cumulative Probability", row=2, col=2)

        # Save as HTML
        fig.write_html(self.output_dir / 'interactive_dashboard.html')

        print("  ✓ Interactive dashboard saved (open interactive_dashboard.html in browser)")

    def plot_sensitivity_analysis(self, sensitivity: dict):
        """
        Plot sensitivity analysis results

        Args:
            sensitivity: Sensitivity analysis dictionary
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        policies = [POLICY_PARAMETERS[key].name for key in sensitivity.keys()]
        contributions = [sens['percentage'] for sens in sensitivity.values()]

        colors = sns.color_palette(COLOR_PALETTE, len(policies))
        bars = ax.barh(policies, contributions, color=colors, edgecolor='black', alpha=0.7)

        ax.set_xlabel('Contribution to Total Variance (%)', fontsize=12)
        ax.set_title('Sensitivity Analysis: Variance Contribution by Policy', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        # Add value labels
        for bar, value in zip(bars, contributions):
            width = bar.get_width()
            ax.text(
                width,
                bar.get_y() + bar.get_height() / 2,
                f' {value:.1f}%',
                ha='left',
                va='center',
                fontweight='bold'
            )

        plt.tight_layout()
        plt.savefig(
            self.output_dir / 'sensitivity_analysis.png',
            dpi=FIGURE_DPI,
            bbox_inches='tight'
        )
        plt.close()

        print("  ✓ Sensitivity analysis plot saved")
