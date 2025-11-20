#!/usr/bin/env python3
"""
Streamlit web application for Mamdani Policy Monte Carlo Simulation
Interactive dashboard for exploring fiscal scenarios
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.simulation import MonteCarloSimulator
from src.parameters import POLICY_PARAMETERS, REVENUE_PARAMETERS

# Page configuration
st.set_page_config(
    page_title="Mamdani Policy Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .policy-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""

    # Header
    st.markdown('<div class="main-header">📊 Mamdani Policy Analysis: Monte Carlo Simulation</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 1.1rem; color: #555;'>
    Interactive analysis of NYC mayoral candidate Zohran Mamdani's progressive policy proposals
    </p>
    """, unsafe_allow_html=True)

    # About section
    with st.expander("📖 About This Analysis", expanded=False):
        st.markdown("""
        This Monte Carlo simulation analyzes the fiscal viability of Zohran Mamdani's policy proposals for NYC.
        By running thousands of simulations with varying parameters, we can assess budget risks and affordability.

        **What is Monte Carlo Simulation?**
        - A statistical method that runs thousands of scenarios with random sampling
        - Accounts for uncertainty in cost and revenue estimates
        - Provides probability distributions of outcomes instead of single-point estimates
        - Widely used in finance, engineering, and policy analysis
        """)

    # Sidebar for parameter inputs
    st.sidebar.markdown("## 🎛️ Adjust Parameters")
    st.sidebar.markdown("Modify policy costs and revenues to explore different scenarios:")

    # Simulation settings
    st.sidebar.markdown("### Simulation Settings")
    num_simulations = st.sidebar.slider(
        "Number of Simulations",
        min_value=1000,
        max_value=20000,
        value=5000,
        step=1000,
        help="More simulations = more accurate results (but slower)"
    )

    threshold = st.sidebar.slider(
        "Budget Threshold (Billions $)",
        min_value=1.0,
        max_value=10.0,
        value=2.0,
        step=0.5,
        help="Track how often costs exceed this amount"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Policy Costs (Annual, Billions $)")

    # Policy parameter inputs
    free_buses_mean = st.sidebar.number_input(
        "🚌 Free Buses - Mean Cost",
        min_value=0.0,
        max_value=5.0,
        value=0.7,
        step=0.1,
        help="Expected annual cost for free public transportation"
    )
    free_buses_std = st.sidebar.number_input(
        "🚌 Free Buses - Std Dev",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05,
        help="Uncertainty in cost estimate"
    )

    childcare_mean = st.sidebar.number_input(
        "👶 Universal Childcare - Mean Cost",
        min_value=0.0,
        max_value=15.0,
        value=6.0,
        step=0.5,
        help="Expected annual cost including wage increases"
    )
    childcare_std = st.sidebar.number_input(
        "👶 Universal Childcare - Std Dev",
        min_value=0.0,
        max_value=3.0,
        value=1.0,
        step=0.1,
        help="Uncertainty in cost estimate"
    )

    housing_mean = st.sidebar.number_input(
        "🏘️ Affordable Housing - Mean Cost",
        min_value=0.0,
        max_value=20.0,
        value=10.0,
        step=0.5,
        help="Expected annual cost ($100B over 10 years)"
    )
    housing_std = st.sidebar.number_input(
        "🏘️ Affordable Housing - Std Dev",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Uncertainty in cost estimate"
    )

    grocery_mean = st.sidebar.number_input(
        "🛒 Government Grocery Stores - Mean Cost",
        min_value=0.0,
        max_value=0.5,
        value=0.075,
        step=0.005,
        help="Expected annual cost for 5 stores"
    )
    grocery_std = st.sidebar.number_input(
        "🛒 Government Grocery Stores - Std Dev",
        min_value=0.0,
        max_value=0.1,
        value=0.025,
        step=0.005,
        help="Uncertainty in cost estimate"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Revenue Projections (Annual, Billions $)")

    revenue_mean = st.sidebar.number_input(
        "💰 Tax Revenue Increases - Mean",
        min_value=0.0,
        max_value=30.0,
        value=10.0,
        step=0.5,
        help="Expected revenue from tax increases"
    )
    revenue_std = st.sidebar.number_input(
        "💰 Tax Revenue Increases - Std Dev",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Uncertainty in revenue estimate"
    )

    # Run simulation button
    st.sidebar.markdown("---")
    run_simulation = st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True)

    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Policy Overview",
        "📊 Simulation Results",
        "📈 Visualizations",
        "💡 Insights & Recommendations"
    ])

    # Tab 1: Policy Overview
    with tab1:
        display_policy_overview(
            free_buses_mean, childcare_mean, housing_mean,
            grocery_mean, revenue_mean
        )

    # Tab 2 & 3: Run simulation and display results
    if run_simulation or 'simulation_run' not in st.session_state:
        with st.spinner("Running Monte Carlo simulation... This may take a moment."):
            results = run_custom_simulation(
                num_simulations,
                threshold,
                free_buses_mean, free_buses_std,
                childcare_mean, childcare_std,
                housing_mean, housing_std,
                grocery_mean, grocery_std,
                revenue_mean, revenue_std
            )
            st.session_state['simulation_run'] = True
            st.session_state['results'] = results

    if 'results' in st.session_state:
        results = st.session_state['results']

        with tab2:
            display_results(results, threshold)

        with tab3:
            display_visualizations(results, threshold)

        with tab4:
            display_insights(results)


def display_policy_overview(free_buses, childcare, housing, grocery, revenue):
    """Display overview of Mamdani's policy proposals"""

    st.markdown('<div class="sub-header">Zohran Mamdani\'s Policy Proposals</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        **Zohran Mamdani**, a Democratic Socialist NYC Council member, is running for mayor with
        an ambitious progressive agenda. His proposals aim to address inequality, housing affordability,
        and public services through significant public investment funded by taxes on the wealthy.
        """)

    with col2:
        st.info("""
        **NYC Budget Context**
        - Current Budget: ~$118B
        - Projected Deficit: $4.7B
        - Future Gap (Years 2-3): >$10B
        """)

    st.markdown("---")
    st.markdown("### 📋 Policy Details")

    # Policy 1: Free Buses
    with st.container():
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.markdown("#### 🚌 Free Public Transportation")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Proposal**: Eliminate fares on all NYC buses

            **Reality**:
            - MTA currently charges $2.90 per ride
            - ~2 million daily bus riders
            - Bus revenue: ~$500M annually

            **Your Scenario**: ${:.2f}B annual cost
            """.format(free_buses))
        with col2:
            st.metric("Cost", f"${free_buses:.2f}B")
        st.markdown('</div>', unsafe_allow_html=True)

    # Policy 2: Universal Childcare
    with st.container():
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.markdown("#### 👶 Universal Free Childcare")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Proposal**: Free childcare for all families with wage increases for workers

            **Reality**:
            - ~500,000 children under 5 in NYC
            - Current childcare cost: $15,000-30,000/year per child
            - Many workers earn below living wage

            **Your Scenario**: ${:.2f}B annual cost
            """.format(childcare))
        with col2:
            st.metric("Cost", f"${childcare:.2f}B")
        st.markdown('</div>', unsafe_allow_html=True)

    # Policy 3: Affordable Housing
    with st.container():
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.markdown("#### 🏘️ Affordable Housing Program")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Proposal**: $100B investment over 10 years to build 200,000 affordable units using union labor

            **Reality**:
            - NYC has ~3.5M housing units total
            - Median rent: $3,500/month in Manhattan
            - ~500,000 rent-stabilized units
            - Union construction costs ~30% higher than non-union

            **Your Scenario**: ${:.2f}B annual cost
            """.format(housing))
        with col2:
            st.metric("Cost", f"${housing:.2f}B")
        st.markdown('</div>', unsafe_allow_html=True)

    # Policy 4: Government Grocery Stores
    with st.container():
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.markdown("#### 🛒 Government-Subsidized Grocery Stores")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Proposal**: Create 5 government-run grocery stores (one per borough) with subsidized prices

            **Reality**:
            - Addresses food deserts in low-income neighborhoods
            - Precedent: Some cities have food co-ops
            - Operating costs + subsidies needed

            **Your Scenario**: ${:.2f}B annual cost
            """.format(grocery))
        with col2:
            st.metric("Cost", f"${grocery:.2f}B")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💰 Revenue Plan")

    with st.container():
        st.markdown('<div class="policy-card">', unsafe_allow_html=True)
        st.markdown("#### Tax Increases on the Wealthy")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            **Proposal**:
            - 2% tax on NYC residents earning >$1M/year
            - Increase corporate tax rate to 11.5%

            **Reality**:
            - ~40,000 NYC households earn >$1M
            - Concerns about wealthy residents leaving
            - Requires state approval for income tax changes

            **Your Scenario**: ${:.2f}B annual revenue
            """.format(revenue))
        with col2:
            st.metric("Revenue", f"${revenue:.2f}B", delta_color="normal")
        st.markdown('</div>', unsafe_allow_html=True)

    # Summary
    st.markdown("---")
    total_cost = free_buses + childcare + housing + grocery
    net_impact = total_cost - revenue

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Policy Cost", f"${total_cost:.2f}B")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Projected Revenue", f"${revenue:.2f}B")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Net Budget Impact", f"${net_impact:.2f}B",
                 delta=f"{net_impact:.2f}B deficit" if net_impact > 0 else f"{-net_impact:.2f}B surplus")
        st.markdown('</div>', unsafe_allow_html=True)


def run_custom_simulation(num_sims, threshold, fb_mean, fb_std, cc_mean, cc_std,
                          ah_mean, ah_std, gs_mean, gs_std, rev_mean, rev_std):
    """Run simulation with custom parameters"""

    # Override parameters temporarily
    from src.parameters import PolicyParameter

    custom_policies = {
        "free_buses": PolicyParameter("Free Buses", fb_mean, fb_std, "", ""),
        "universal_childcare": PolicyParameter("Universal Childcare", cc_mean, cc_std, "", ""),
        "affordable_housing": PolicyParameter("Affordable Housing", ah_mean, ah_std, "", ""),
        "government_grocery_stores": PolicyParameter("Grocery Stores", gs_mean, gs_std, "", "")
    }

    custom_revenue = PolicyParameter("Tax Revenue", rev_mean, rev_std, "", "")

    # Run simulation
    policy_costs_dict = {}
    for key, param in custom_policies.items():
        policy_costs_dict[key] = param.sample(size=num_sims)

    revenues = custom_revenue.sample(size=num_sims)
    policy_costs_df = pd.DataFrame(policy_costs_dict)
    total_costs = policy_costs_df.sum(axis=1).values
    net_budget_impact = total_costs - revenues
    threshold_exceedances = np.sum(total_costs > threshold)

    return {
        'policy_costs': policy_costs_df,
        'total_costs': total_costs,
        'revenues': revenues,
        'net_budget_impact': net_budget_impact,
        'threshold': threshold,
        'exceedances': threshold_exceedances,
        'num_sims': num_sims
    }


def display_results(results, threshold):
    """Display simulation results"""

    st.markdown('<div class="sub-header">Simulation Results</div>', unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Mean Total Cost",
            f"${np.mean(results['total_costs']):.2f}B",
            delta=f"±${np.std(results['total_costs']):.2f}B"
        )

    with col2:
        st.metric(
            "Mean Revenue",
            f"${np.mean(results['revenues']):.2f}B",
            delta=f"±${np.std(results['revenues']):.2f}B"
        )

    with col3:
        deficit = np.mean(results['net_budget_impact'])
        st.metric(
            "Average Deficit",
            f"${deficit:.2f}B",
            delta="Needs Funding" if deficit > 0 else "Surplus",
            delta_color="inverse"
        )

    with col4:
        prob = 100 * results['exceedances'] / results['num_sims']
        st.metric(
            f"P(Cost > ${threshold}B)",
            f"{prob:.1f}%",
            delta=f"{results['exceedances']:,} times"
        )

    # Budget analysis
    st.markdown("---")
    if np.mean(results['net_budget_impact']) > 0:
        st.markdown(f"""
        <div class="warning-box">
        <strong>⚠️ Budget Gap Identified</strong><br>
        The simulation shows an average deficit of <strong>${np.mean(results['net_budget_impact']):.2f}B</strong> annually.
        This means the proposed policies would cost more than the projected revenue from tax increases.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
        <strong>✓ Budget Surplus</strong><br>
        The simulation shows an average surplus of <strong>${-np.mean(results['net_budget_impact']):.2f}B</strong> annually.
        The proposed revenue would be sufficient to cover the policy costs.
        </div>
        """, unsafe_allow_html=True)

    # Detailed statistics
    st.markdown("### 📊 Detailed Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Total Policy Costs")
        stats_df = pd.DataFrame({
            'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', '5th %ile', '95th %ile'],
            'Value ($B)': [
                f"${np.mean(results['total_costs']):.2f}",
                f"${np.median(results['total_costs']):.2f}",
                f"${np.std(results['total_costs']):.2f}",
                f"${np.min(results['total_costs']):.2f}",
                f"${np.max(results['total_costs']):.2f}",
                f"${np.percentile(results['total_costs'], 5):.2f}",
                f"${np.percentile(results['total_costs'], 95):.2f}"
            ]
        })
        st.dataframe(stats_df, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("#### Individual Policy Costs (Mean)")
        policy_stats = []
        for col in results['policy_costs'].columns:
            policy_name = col.replace('_', ' ').title()
            mean_cost = np.mean(results['policy_costs'][col])
            pct = 100 * mean_cost / np.mean(results['total_costs'])
            policy_stats.append({
                'Policy': policy_name,
                'Mean Cost ($B)': f"${mean_cost:.2f}",
                '% of Total': f"{pct:.1f}%"
            })
        policy_df = pd.DataFrame(policy_stats)
        st.dataframe(policy_df, hide_index=True, use_container_width=True)


def display_visualizations(results, threshold):
    """Display interactive visualizations"""

    st.markdown('<div class="sub-header">Interactive Visualizations</div>', unsafe_allow_html=True)

    # Chart 1: Total Cost Distribution
    st.markdown("#### Distribution of Total Policy Costs")
    fig1 = go.Figure()

    fig1.add_trace(go.Histogram(
        x=results['total_costs'],
        nbinsx=50,
        name='Total Costs',
        marker_color='steelblue',
        opacity=0.7
    ))

    fig1.add_vline(
        x=threshold,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Threshold: ${threshold}B",
        annotation_position="top right"
    )

    fig1.add_vline(
        x=np.mean(results['total_costs']),
        line_dash="dash",
        line_color="green",
        annotation_text=f"Mean: ${np.mean(results['total_costs']):.2f}B",
        annotation_position="top left"
    )

    fig1.update_layout(
        xaxis_title="Total Cost (Billions USD)",
        yaxis_title="Frequency",
        title="Monte Carlo Simulation: Total Policy Cost Distribution",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Individual Policy Box Plots
    st.markdown("#### Individual Policy Cost Distributions")

    fig2 = go.Figure()

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    for idx, col in enumerate(results['policy_costs'].columns):
        policy_name = col.replace('_', ' ').title()
        fig2.add_trace(go.Box(
            y=results['policy_costs'][col],
            name=policy_name,
            marker_color=colors[idx],
            boxmean='sd'
        ))

    fig2.update_layout(
        yaxis_title="Cost (Billions USD)",
        title="Policy Cost Distributions (Box Plots)",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Chart 3: Net Budget Impact
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Net Budget Impact Distribution")
        fig3 = go.Figure()

        fig3.add_trace(go.Histogram(
            x=results['net_budget_impact'],
            nbinsx=50,
            marker_color='coral',
            opacity=0.7
        ))

        fig3.add_vline(x=0, line_dash="dash", line_color="green",
                      annotation_text="Balanced Budget")

        fig3.update_layout(
            xaxis_title="Net Impact (Billions USD)",
            yaxis_title="Frequency",
            template="plotly_white",
            height=400
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("#### Costs vs Revenue")

        comparison_data = pd.DataFrame({
            'Category': ['Total Costs', 'Revenue'],
            'Mean': [np.mean(results['total_costs']), np.mean(results['revenues'])],
            'Std': [np.std(results['total_costs']), np.std(results['revenues'])]
        })

        fig4 = go.Figure()

        fig4.add_trace(go.Bar(
            x=comparison_data['Category'],
            y=comparison_data['Mean'],
            error_y=dict(type='data', array=comparison_data['Std']),
            marker_color=['#e74c3c', '#27ae60'],
            text=[f"${val:.2f}B" for val in comparison_data['Mean']],
            textposition='outside'
        ))

        fig4.update_layout(
            yaxis_title="Amount (Billions USD)",
            template="plotly_white",
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig4, use_container_width=True)

    # Chart 4: Cumulative Distribution
    st.markdown("#### Cumulative Probability Distribution")

    sorted_costs = np.sort(results['total_costs'])
    cumulative_prob = np.arange(1, len(sorted_costs) + 1) / len(sorted_costs)

    fig5 = go.Figure()

    fig5.add_trace(go.Scatter(
        x=sorted_costs,
        y=cumulative_prob,
        mode='lines',
        line=dict(color='steelblue', width=2),
        name='CDF'
    ))

    fig5.add_vline(
        x=threshold,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Threshold: ${threshold}B"
    )

    fig5.update_layout(
        xaxis_title="Total Cost (Billions USD)",
        yaxis_title="Cumulative Probability",
        title="Cumulative Distribution Function",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(fig5, use_container_width=True)


def display_insights(results):
    """Display insights and recommendations"""

    st.markdown('<div class="sub-header">Insights & Recommendations</div>', unsafe_allow_html=True)

    deficit = np.mean(results['net_budget_impact'])

    st.markdown("### 🔍 Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Budget Reality")
        st.markdown(f"""
        - **Average Deficit**: ${deficit:.2f}B annually
        - **Revenue Coverage**: {100 * np.mean(results['revenues']) / np.mean(results['total_costs']):.1f}% of costs
        - **Threshold Exceedance**: {100 * results['exceedances'] / results['num_sims']:.1f}% of simulations
        - **Risk Level**: {"High" if deficit > 5 else "Moderate" if deficit > 2 else "Low"}
        """)

    with col2:
        st.markdown("#### Policy Breakdown")
        for col in results['policy_costs'].columns:
            policy_name = col.replace('_', ' ').title()
            mean_cost = np.mean(results['policy_costs'][col])
            pct = 100 * mean_cost / np.mean(results['total_costs'])
            st.markdown(f"- **{policy_name}**: ${mean_cost:.2f}B ({pct:.1f}%)")

    st.markdown("---")
    st.markdown("### 💡 Recommendations")

    if deficit > 5:
        st.markdown("""
        <div class="warning-box">
        <strong>Significant Budget Gap Requires Action</strong><br><br>
        The simulation reveals a substantial budget shortfall. Consider:
        <ul>
        <li><strong>Phased Implementation</strong>: Roll out policies sequentially rather than simultaneously</li>
        <li><strong>Enhanced Revenue</strong>: Increase tax rates or broaden the tax base</li>
        <li><strong>Cost Optimization</strong>: Redesign programs for greater efficiency (e.g., non-union housing construction)</li>
        <li><strong>Means Testing</strong>: Target benefits to those most in need</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    elif deficit > 0:
        st.markdown("""
        <div class="warning-box">
        <strong>Moderate Budget Gap - Manageable with Adjustments</strong><br><br>
        The deficit is manageable but requires careful planning:
        <ul>
        <li><strong>Priority Sequencing</strong>: Implement highest-impact policies first</li>
        <li><strong>Revenue Enhancement</strong>: Modest tax increase or new revenue sources</li>
        <li><strong>Efficiency Gains</strong>: Find cost savings in implementation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
        <strong>Budget Surplus - Policies Are Affordable</strong><br><br>
        The simulation shows the policies can be funded with the proposed revenue:
        <ul>
        <li><strong>Full Implementation</strong>: All policies can proceed as planned</li>
        <li><strong>Reserve Fund</strong>: Use surplus for contingencies or additional programs</li>
        <li><strong>Gradual Expansion</strong>: Start conservatively and expand if costs are lower than expected</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 Further Analysis")

    st.markdown("""
    To deepen this analysis, consider exploring:

    1. **Multi-Year Projections**: Model compounding effects over 10 years
    2. **Economic Scenarios**: Analyze impact during recession vs growth
    3. **Behavioral Responses**: Model how taxpayers might respond to tax increases
    4. **Alternative Packages**: Compare different policy combinations
    5. **Political Feasibility**: Assess likelihood of passing different components
    """)

    st.markdown("---")
    st.markdown("### 📖 Sources & Methodology")

    with st.expander("View Sources"):
        st.markdown("""
        **Data Sources:**
        - Jacobin: "Mayor Mamdani's Budget Can Add Up" (November 2025)
        - THE CITY: "Adams Boosts Budget, Leaving a $4.7 Billion Hole for Mamdani" (November 2025)
        - CNN: "Here's a look at Zohran Mamdani's policy ideas" (November 2025)
        - TIME: "Can Mamdani Fulfill His Ambitious Campaign Promises?" (2025)

        **Methodology:**
        - Monte Carlo simulation with configurable number of runs
        - Normal distributions with specified means and standard deviations
        - Non-negative sampling (costs can't be negative)
        - Independent policy assumptions (no correlations modeled)
        """)


# Footer
def display_footer():
    """Display footer with credits"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>
    <strong>Mamdani Policy Analysis Tool</strong> |
    Built with Streamlit & Python |
    <a href='https://github.com/Sakeeb91/mamdani-policy-montecarlo'>View on GitHub</a>
    </p>
    <p>
    For educational and informational purposes only. Cost estimates based on publicly available information.
    </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    display_footer()
