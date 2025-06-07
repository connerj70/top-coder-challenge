# Reimbursement Calculation Logic - Synthesis of Findings

**Date:** June 2025  
**Purpose:** Consolidate data analysis and interview insights for hypothesis formulation  
**Source:** 1,000 public test cases + 5 employee interviews

## Executive Summary

The analysis reveals a **significant disconnect** between employee perceptions and actual system behavior. The data strongly suggests a **receipt-dominant, deterministic system** that contradicts most employee theories about complex efficiency bonuses and "sweet spots."

## Core Contradictions: Data vs. Employee Claims

| Employee Claim | Data Evidence | Verdict |
|----------------|---------------|---------|
| $100/day base rate (Lisa) | ~$800-900/day for 1-day trips | ❌ **Contradicted** |
| 5-day trip sweet spot (Lisa, Jennifer) | 5-day trips: $254.52/day vs. 1-day: $873.55/day | ❌ **Contradicted** |
| 180-220 mi/day efficiency bonus (Kevin) | Sweet spot range: $1,318.86 avg vs. Low efficiency: $1,486.87 avg | ❌ **Contradicted** |
| Complex mileage tiers (Lisa) | Linear negative correlation (-0.142) with efficiency | ❌ **Contradicted** |
| Receipt penalties for small amounts | Consistent positive correlation (0.704) across all ranges | ❌ **Contradicted** |
| System randomization (Kevin) | 98.5% consistency across similar trips | ❌ **Contradicted** |

## Confirmed Data Patterns

### 1. Receipt Amount Dominance
- **Correlation:** 0.704 (strongest predictor)
- **Pattern:** Linear positive relationship across all trip types
- **Evidence:** Every increase in receipt amount correlates with reimbursement increase
- **Range:** $1.42 - $2,503.46 (receipts) → $117.24 - $2,337.73 (reimbursements)

### 2. Trip Duration Impact (Decreasing Returns)
- **Correlation:** 0.514 (moderate positive)
- **Pattern:** Diminishing per-day returns as trip length increases
- **Evidence:**
  - 1 day: $873.55/day
  - 2 days: $523.12/day  
  - 5 days: $254.52/day
  - 10+ days: $149-228/day

### 3. Efficiency Penalty Effect
- **Correlation:** -0.142 (weak negative)
- **Pattern:** Higher miles/day ratios receive lower per-mile rates
- **Evidence:**
  - 0-50 mi/day: $16.64/mile
  - 180-220 mi/day: $1.74/mile
  - 400+ mi/day: $1.37/mile

### 4. System Determinism
- **Consistency:** 98.5% of similar trips within 5% variance
- **Evidence:** 961 of 976 similar trip groups show consistent calculations
- **Implication:** Rule-based system, not randomized or machine learning

## Areas Where Employee Insights May Have Value

### 1. Temporal Effects (Untestable with Current Data)
- **Employee Claims:** Quarterly patterns, weekly submission effects, lunar cycles
- **Data Status:** No temporal data available in public cases
- **Assessment:** Could be valid but unverifiable

### 2. Threshold Effects
- **Employee Claims:** Specific breakpoints trigger bonuses/penalties
- **Data Hints:** Some evidence of potential thresholds in receipt ranges
- **Assessment:** Possible but masked by linear correlation

### 3. Interaction Effects
- **Employee Claims:** Complex combinations of factors (trip_length × efficiency)
- **Data Evidence:** Primary correlations suggest simpler relationships
- **Assessment:** May exist but secondary to main factors

### 4. Special Case Logic
- **Employee Claims:** Different calculation paths for different trip types
- **Data Evidence:** 1.5% of cases show inconsistent patterns
- **Assessment:** Likely exists for edge cases

## Potential Calculation Model Components

Based on the synthesis, the calculation likely includes:

### Base Components (High Confidence)
1. **Receipt Multiplier:** ~0.7-0.8 factor applied to receipt amounts
2. **Base Rate:** High starting value (~$800-900) for minimal trips
3. **Duration Factor:** Decreasing per-day rate as trip length increases
4. **Efficiency Penalty:** Negative adjustment for high miles/day ratios

### Possible Additional Components (Medium Confidence)
1. **Receipt Thresholds:** Different rates for different receipt ranges
2. **Duration Breakpoints:** Specific penalties at certain trip lengths
3. **Minimum/Maximum Caps:** Floor and ceiling values for reimbursements

### Speculative Components (Low Confidence)
1. **Temporal Modifiers:** Quarterly/seasonal adjustments
2. **User History:** Experience-based modifications
3. **Department Factors:** Role-based multipliers

## Mathematical Framework Hypothesis

```
Reimbursement = BaseRate(duration) × ReceiptFactor(receipts) × EfficiencyPenalty(miles/day) + Adjustments
```

Where:
- `BaseRate(duration)`: Decreasing function of trip length
- `ReceiptFactor(receipts)`: Linear function of receipt amounts (~0.7x)
- `EfficiencyPenalty(miles/day)`: Decreasing function of efficiency ratio
- `Adjustments`: Threshold effects, caps, special cases

## Test Cases for Hypothesis Validation

### Representative Sample (15 cases)
Selected to cover diverse scenarios:

| Case | Duration | Miles | Receipts | Actual | Notes |
|------|----------|-------|----------|--------|-------|
| A | 1 | 50 | $100 | TBD | Low efficiency baseline |
| B | 1 | 50 | $500 | TBD | High receipts, low efficiency |
| C | 5 | 1000 | $600 | TBD | "Employee sweet spot" test |
| D | 5 | 200 | $600 | TBD | High efficiency test |
| E | 10 | 500 | $1000 | TBD | Long trip test |
| ... | ... | ... | ... | ... | ... |

*Full test matrix to be populated from actual dataset*

## Priority Hypotheses to Develop

### Hypothesis 1: Receipt-Dominant Linear Model
- **Primary Factor:** Receipt amount × 0.7-0.8
- **Modifiers:** Duration and efficiency adjustments
- **Expected Accuracy:** 70-80%

### Hypothesis 2: Tiered Receipt Model  
- **Primary Factor:** Receipt amount with different rates by range
- **Modifiers:** Duration breakpoints and efficiency penalties
- **Expected Accuracy:** 75-85%

### Hypothesis 3: Conditional Logic Model
- **Primary Factor:** Different formulas based on trip characteristics
- **Trigger Conditions:** Duration, efficiency, or receipt thresholds
- **Expected Accuracy:** 80-90%

### Hypothesis 4: Hybrid Employee-Data Model
- **Primary Factor:** Receipt-based with employee-identified patterns
- **Special Cases:** 5-day bonuses, efficiency sweet spots for specific conditions
- **Expected Accuracy:** 60-75% (lower due to contradictions)

## Next Steps

1. **Develop detailed mathematical formulas** for each hypothesis
2. **Test against representative sample** of 15 diverse cases
3. **Calculate accuracy percentages** for each model
4. **Identify failure patterns** to refine models
5. **Select top 2 hypotheses** for full implementation and testing

## Confidence Assessment

- **High Confidence (>80%):** Receipt amounts are primary factor
- **Medium Confidence (60-80%):** Duration and efficiency are secondary factors
- **Low Confidence (<60%):** Complex interaction effects, temporal patterns

The synthesis strongly suggests that a relatively simple, receipt-dominant model will explain the majority of the reimbursement calculations, with additional factors providing refinement rather than fundamental changes to the logic. 