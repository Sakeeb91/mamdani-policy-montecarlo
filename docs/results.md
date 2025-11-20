# Mamdani Policy Analysis: Simulation Results

## Executive Summary

This Monte Carlo analysis evaluated the fiscal viability of NYC mayoral candidate Zohran Mamdani's progressive policy agenda using 10,000 simulations. The results reveal significant budget challenges that require careful consideration.

**Key Findings:**
- **Mean Total Cost**: $16.77B annually
- **Mean Revenue**: $10.01B annually (from proposed tax increases)
- **Mean Budget Deficit**: $6.76B annually
- **Threshold Exceedance**: 100% of simulations exceeded the $2B threshold
- **Highest Variance Contributors**: Affordable Housing (66.8%), Universal Childcare (30.3%)

## Detailed Results

### 1. Total Policy Costs

The Monte Carlo simulation generated the following cost distribution for Mamdani's combined policy proposals:

| Metric | Value (Billions USD) |
|--------|---------------------|
| Mean | $16.77B |
| Median | $16.76B |
| Standard Deviation | $1.82B |
| Minimum (observed) | $10.75B |
| Maximum (observed) | $23.31B |
| 5th Percentile | $13.80B |
| 95th Percentile | $19.78B |

**Interpretation**:
The policies would cost an average of $16.77B annually, with 90% of simulations falling between $13.80B and $19.78B. The relatively tight distribution (std dev of $1.82B) indicates moderate uncertainty in cost projections.

### 2. Revenue Projections

Mamdani's proposed tax increases are expected to generate:

| Metric | Value (Billions USD) |
|--------|---------------------|
| Mean | $10.01B |
| Median | $10.01B |
| Standard Deviation | $1.50B |

**Interpretation**:
The proposed tax increases (2% on incomes >$1M and corporate tax increase to 11.5%) would generate approximately $10B annually. However, this falls significantly short of the $16.77B needed to fund the policies.

### 3. Net Budget Impact

The gap between costs and revenues creates a substantial deficit:

| Metric | Value (Billions USD) |
|--------|---------------------|
| Mean Deficit | $6.76B |
| Median Deficit | $6.75B |
| Standard Deviation | $2.35B |
| 95% Confidence Interval | $6.71B - $6.81B |

**Interpretation**:
On average, Mamdani's policies would create a **$6.76B annual deficit** after accounting for proposed revenue. With 95% confidence, this deficit falls between $6.71B and $6.81B.

### 4. Threshold Analysis

The analysis tracked how often total costs exceeded a $2B threshold:

- **Exceedances**: 10,000 out of 10,000 simulations (100%)
- **Probability**: 1.0000 (100%)

**Interpretation**:
Every single simulation exceeded the $2B threshold, indicating virtual certainty that costs will significantly surpass this baseline. In fact, all simulations showed costs above $10B.

### 5. Individual Policy Cost Breakdown

| Policy | Mean Cost | Std Dev | % of Total |
|--------|-----------|---------|-----------|
| Affordable Housing | $9.98B | $1.49B | 59.5% |
| Universal Childcare | $6.01B | $1.00B | 35.8% |
| Free Buses | $0.70B | $0.10B | 4.2% |
| Government Grocery Stores | $0.07B | $0.03B | 0.4% |

**Interpretation**:
- **Affordable Housing** dominates costs at nearly 60% of the total budget
- **Universal Childcare** accounts for over one-third of costs
- Transportation and food security programs are relatively modest

### 6. Sensitivity Analysis

Variance contribution by policy (measuring which policies drive budget uncertainty):

| Policy | Variance Contribution |
|--------|----------------------|
| Affordable Housing | 66.8% |
| Universal Childcare | 30.3% |
| Free Buses | 0.3% |
| Government Grocery Stores | 0.0% |

**Interpretation**:
- **Affordable Housing** contributes two-thirds of total budget variance, making it the highest-risk component
- **Universal Childcare** adds significant uncertainty
- Transportation and grocery programs have predictable costs

This suggests that cost overruns are most likely to come from housing and childcare initiatives.

## Visualizations

The following visualizations have been generated in the `results/` directory:

1. **total_costs_distribution.png**: Histogram and box plot showing the range of possible total costs
2. **individual_policy_distributions.png**: Cost distributions for each policy
3. **net_budget_impact.png**: Deficit/surplus analysis and cost vs. revenue comparison
4. **threshold_analysis.png**: Cumulative distribution and threshold exceedance pie chart
5. **correlation_heatmap.png**: Correlation between policy costs
6. **sensitivity_analysis.png**: Variance contribution by policy
7. **interactive_dashboard.html**: Interactive Plotly dashboard (open in browser)

## Statistical Rigor

### Methodology Strengths
- **Large sample size**: 10,000 simulations provide robust statistical power
- **Uncertainty modeling**: Normal distributions with standard deviations capture cost uncertainty
- **Non-negative constraints**: Ensured all sampled costs are realistic (≥ 0)
- **Confidence intervals**: 95% CIs provide reliable bounds on estimates

### Assumptions and Limitations
1. **Independence assumption**: Policies assumed independent; in reality, some may have correlations (e.g., inflation affecting both housing and childcare)
2. **Normal distributions**: Actual costs may have skewed or multimodal distributions
3. **Static analysis**: Single-year snapshot; doesn't model multi-year dynamics
4. **Parameter uncertainty**: Cost estimates based on available public information
5. **No economic scenarios**: Doesn't account for recession/growth impacts

## Interpretation & Implications

### Budget Gap Challenge

The simulation reveals a **$6.76B average annual deficit** between policy costs and proposed revenues. To contextualize this:

- **NYC Current Budget**: ~$118B
- **Projected Deficit**: $4.7B (before Mamdani's proposals)
- **Future Budget Gap**: Expected to exceed $10B in years 2-3

**Implication**: Mamdani's policies would significantly worsen NYC's fiscal position, potentially increasing the structural deficit by 60-140%.

### Affordability Assessment

At the $2B threshold:
- **100% of simulations exceeded** this baseline
- **Minimum observed cost**: $10.75B (5.4x the threshold)

**Implication**: The policies vastly exceed the $2B threshold, suggesting they are not affordable under current revenue assumptions.

### Risk Factors

The sensitivity analysis identifies **Affordable Housing** as the primary fiscal risk:
- Contributes 66.8% of total budget variance
- Mean cost of $9.98B with $1.49B standard deviation
- Could range from ~$7B to ~$13B (±2σ)

**Implication**: Cost control in housing is critical. Overruns in this area would have outsized budget impacts.

### Revenue Sufficiency

Proposed revenues ($10B) cover only **59.7%** of expected costs ($16.77B).

**Implication**: To fully fund these policies, Mamdani would need to either:
1. Increase taxes by an additional 68% beyond current proposals (~$16.8B total needed)
2. Identify $6.76B in offsetting cuts elsewhere in the NYC budget
3. Scale back policy ambitions

## Policy Recommendations

Based on the simulation results, several pathways forward emerge:

### Option 1: Phased Implementation
Implement policies sequentially rather than simultaneously:
- **Year 1**: Free Buses ($0.7B) - Most affordable, immediate public benefit
- **Year 2**: Add Government Grocery Stores ($0.075B)
- **Year 3**: Begin scaled childcare program ($2-3B initially)
- **Year 4-10**: Gradual housing program expansion

**Pros**: Manageable fiscal impact, allows revenue growth to catch up
**Cons**: Delays key benefits, may disappoint supporters

### Option 2: Enhanced Revenue
Increase tax proposals to match spending:
- Additional $6.8B in annual revenue needed
- Could require higher tax rates or broader base
- Example: 3-4% tax on >$1M incomes instead of 2%

**Pros**: Fully funds agenda
**Cons**: Political feasibility concerns, potential behavioral responses (wealthy residents leaving)

### Option 3: Policy Redesign
Modify policies to reduce costs while preserving goals:
- **Housing**: Use more cost-effective construction methods, reduce union requirements, or lower target from 200K to 100K units
- **Childcare**: Means-test benefits or phase in wage increases gradually
- **Transportation**: Start with select high-traffic bus routes rather than full system

**Pros**: Achieves policy goals more affordably
**Cons**: May reduce policy impact, disappoint advocates

### Option 4: Mixed Approach
Combine elements of all three:
- Implement free buses immediately
- Phase in childcare with initial means-testing
- Redesign housing program for cost efficiency
- Seek additional revenue (~$3-4B instead of $6.8B)

**Pros**: Balanced approach, politically pragmatic
**Cons**: Requires careful sequencing and communication

## Future Analysis Recommendations

To strengthen this analysis, consider:

1. **Multi-year projections**: Model 10-year fiscal impact with compounding effects
2. **Economic scenarios**: Run simulations under recession, baseline, and growth conditions
3. **Correlation modeling**: Account for dependencies between policy costs
4. **Behavioral responses**: Model how taxpayers might respond to tax increases
5. **Alternative distributions**: Use skewed or empirical distributions if data becomes available
6. **Dynamic revenue**: Model how policy implementation might affect tax base
7. **Comparison scenarios**: Analyze alternative policy packages (moderate, aggressive variants)
8. **Political feasibility**: Incorporate probability of passage for different components

## Conclusion

This Monte Carlo analysis provides a data-driven assessment of Zohran Mamdani's policy agenda. The key conclusions are:

1. **Significant Budget Gap**: The policies would create an average $6.76B annual deficit
2. **Affordable Housing Dominates**: 60% of costs and 67% of variance come from housing
3. **Revenue Shortfall**: Proposed taxes cover only 60% of costs
4. **High Certainty**: Statistical analysis shows tight confidence intervals around estimates
5. **Implementation Challenges**: Full simultaneous implementation poses major fiscal risks

**Final Assessment**: While Mamdani's policies address important social needs, they face significant affordability challenges under current revenue assumptions. Successful implementation would require either substantial additional revenue, phased rollout, policy redesign, or some combination of these approaches.

The analysis suggests that **selective implementation** with **enhanced revenue measures** represents the most fiscally sustainable path forward, though this may require difficult political choices about priorities and sequencing.

## Appendix: Technical Details

### Simulation Parameters
- **Simulations**: 10,000
- **Random Seed**: 42 (for reproducibility)
- **Budget Threshold**: $2.0B
- **Confidence Level**: 95%

### Policy Cost Distributions
All policies modeled as truncated normal distributions (non-negative):

```
Free Buses: N(0.7, 0.1²)
Universal Childcare: N(6.0, 1.0²)
Affordable Housing: N(10.0, 1.5²)
Government Grocery Stores: N(0.075, 0.025²)
Tax Revenues: N(10.0, 1.5²)
```

### Software Stack
- Python 3.9+
- NumPy 1.24+ for numerical computing
- SciPy 1.10+ for statistical distributions
- Matplotlib/Seaborn for statistical visualization
- Plotly 5.14+ for interactive dashboards
- Pandas 2.0+ for data manipulation

### Data Sources
1. Jacobin: "Mayor Mamdani's Budget Can Add Up" (November 2025)
2. THE CITY: "Adams Boosts Budget, Leaving a $4.7 Billion Hole for Mamdani" (November 17, 2025)
3. CNN: "Here's a look at Zohran Mamdani's policy ideas" (November 4, 2025)
4. TIME: "Can Mamdani Fulfill His Ambitious Campaign Promises?" (2025)

---

**Analysis Date**: November 20, 2025
**Analyst**: Sakeeb Rahman
**Version**: 1.0
**Status**: Complete

For questions or to reproduce this analysis, see the [README.md](../README.md) and [project-plan.md](project-plan.md).
