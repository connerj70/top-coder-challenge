# Reimbursement System Data Analysis Report

**Date:** June 2025  
**Analyst:** AI Assistant  
**Dataset:** 1,000 public test cases  
**Analysis Tool:** Custom Python analysis functions

## Executive Summary

The comprehensive analysis of 1,000 public test cases reveals that the legacy reimbursement system operates quite differently from employee perceptions. The data shows a predominantly deterministic system where **receipt amounts are the primary factor** (correlation: 0.704), contradicting employee theories about complex "sweet spots" and efficiency bonuses.

### Key Contradictions to Employee Claims:
- ❌ No 5-day trip sweet spot exists
- ❌ No 180-220 mile/day efficiency bonus found
- ❌ System actually penalizes efficiency rather than rewarding it
- ❌ Base rate is ~$800-900/day, not $100/day as claimed

## Dataset Overview

- **Total Cases:** 1,000 test cases
- **Trip Duration Range:** 1-14 days (avg: 7.04 days)
- **Miles Traveled Range:** 5-1,317 miles (avg: 597.41 miles)
- **Receipt Amount Range:** $1.42-$2,503.46 (avg: $1,211.06)
- **Reimbursement Range:** $117.24-$2,337.73 (avg: $1,349.11)

## Core Findings

### 1. Correlation Analysis

| Factor | Correlation with Reimbursement | Strength |
|--------|--------------------------------|----------|
| **Receipt Amount** | **0.704** | **Strong** |
| Trip Duration | 0.514 | Moderate |
| Total Miles | 0.432 | Moderate |
| Miles Per Day | -0.142 | Weak (Negative) |
| Receipts Per Day | 0.051 | Very Weak |

**Key Insight:** Receipt amounts are by far the strongest predictor of reimbursement amounts, suggesting a primarily receipt-based calculation system.

### 2. Trip Duration Analysis

**Employee Claim:** "5-day trips get consistent bonuses" (Lisa, Jennifer)  
**Reality:** No evidence of 5-day sweet spot found.

| Trip Length | Avg Per Day | Count | Pattern |
|-------------|-------------|--------|---------|
| 1 day | $873.55 | 92 | Highest rate |
| 2 days | $523.12 | 59 | Sharp decline |
| 3 days | $336.85 | 83 | Continued decline |
| 4 days | $304.49 | 67 | Still declining |
| **5 days** | **$254.52** | **112** | **Lower than shorter trips** |
| 6+ days | $149-228 | 487 | Continued decline |

**Conclusion:** Shorter trips get significantly higher per-day reimbursement rates. The 5-day "sweet spot" is actually below the optimal range.

### 3. Mileage Efficiency Analysis

**Employee Claim:** "180-220 miles/day gets maximum bonuses" (Kevin)  
**Reality:** Lower efficiency gets better per-mile rates.

| Efficiency Range | Avg Reimbursement | Per-Mile Rate | Count |
|------------------|-------------------|---------------|--------|
| Very Low (0-50 mi/day) | $1,249.18 | **$16.64/mile** | 293 |
| Low (50-100 mi/day) | $1,486.87 | $2.53/mile | 287 |
| Medium Low (100-150 mi/day) | $1,514.78 | $2.09/mile | 162 |
| Medium (150-180 mi/day) | $1,476.20 | $1.86/mile | 48 |
| **"Sweet Spot" (180-220 mi/day)** | **$1,318.86** | **$1.74/mile** | **41** |
| High (300-400 mi/day) | $1,054.77 | $1.43/mile | 45 |
| Very High (400+ mi/day) | $1,103.86 | $1.37/mile | 74 |

**Conclusion:** The system actually penalizes efficiency. Lower miles-per-day ratios receive dramatically higher per-mile reimbursement rates.

### 4. Receipt Patterns Analysis

Receipt amounts show consistent positive correlation across all trip categories:

**Short Trips (1-3 days):**
- Very low receipts: $255.67 avg
- Very high receipts: $1,067.63 avg

**Medium Trips (3-6 days):**
- Very low receipts: $585.91 avg
- Very high receipts: $1,457.61 avg

**Long Trips (6+ days):**
- Very low receipts: $1,029.33 avg
- Very high receipts: $1,713.00 avg

**Pattern:** Higher receipt amounts consistently lead to higher reimbursements across all trip lengths.

### 5. System Consistency Analysis

**Employee Claim:** "System has randomization to prevent gaming" (Kevin)  
**Reality:** System is 98.5% consistent.

- **Total Similar Trip Groups:** 976
- **Consistent Groups (≤5% variance):** 961 (98.5%)
- **Inconsistent Groups (>5% variance):** 15 (1.5%)

**Conclusion:** The system is highly deterministic with minimal variance, suggesting rule-based calculations rather than randomization or machine learning.

## Proposed Calculation Model

Based on the analysis, the reimbursement calculation likely follows this structure:

```
Reimbursement = Base_Rate + (Receipt_Factor × Receipts) - (Efficiency_Penalty × Miles_Per_Day)
```

### Model Components:

1. **Base Rate:** ~$800-900 for single-day trips, declining with duration
2. **Receipt Factor:** Strong linear component (~0.7-0.8 multiplier)
3. **Efficiency Penalty:** Inverse relationship with miles/day ratio

### Evidence Supporting This Model:

- Receipt correlation (0.704) suggests ~70% of calculation variance
- Negative miles/day correlation (-0.142) indicates efficiency penalty
- High consistency (98.5%) indicates deterministic formula
- 1-day trip rate ($873.55) suggests high base rate

## Discrepancies with Employee Interviews

### Major Contradictions:

1. **Base Rate:** Employees claimed $100/day; data shows ~$800-900/day base
2. **5-Day Bonus:** No evidence found; 5-day trips are suboptimal
3. **Efficiency Rewards:** System penalizes, not rewards, high efficiency
4. **Complex Interactions:** Primary factor is simply receipt amounts
5. **Randomization:** System is highly consistent, not randomized

### Possible Explanations:

1. **Selection Bias:** Employees may have observed non-representative subsets
2. **Confirmation Bias:** Looking for patterns that don't exist
3. **System Changes:** Rules may have changed since employee observations
4. **Incomplete Information:** Employees may not see the full calculation

## Recommendations

### For Algorithm Development:
1. **Focus on receipt-based calculations** as the primary component
2. **Implement efficiency penalty** rather than efficiency bonus
3. **Use high base rates** for short trips with duration-based decline
4. **Test simple linear models** before complex interaction models

### For Further Analysis:
1. **Validate proposed model** against test cases
2. **Identify the 15 inconsistent cases** for special rules
3. **Look for threshold effects** in the linear relationships
4. **Test seasonal/timing effects** if date data becomes available

### For Employee Communication:
1. **Address misconceptions** about efficiency rewards
2. **Explain receipt-dominance** in the calculation
3. **Clarify that optimization strategies** based on "sweet spots" are ineffective

## Limitations

1. **No temporal data:** Cannot analyze seasonal/timing effects mentioned in interviews
2. **No user data:** Cannot analyze department/experience effects
3. **Public cases only:** May not represent full range of edge cases
4. **No access to source code:** Cannot confirm exact calculation method

## Conclusion

The analysis reveals a much simpler and more deterministic system than employee perceptions suggested. The reimbursement calculation is primarily driven by receipt amounts with additional factors for trip duration and an efficiency penalty. The data strongly contradicts employee theories about complex "sweet spots" and efficiency bonuses, suggesting that optimization strategies based on these theories would be counterproductive.

The high consistency (98.5%) of the system indicates that a deterministic mathematical model can be developed with high accuracy. The next phase should focus on developing and testing a simple linear model based on receipts, duration, and miles-per-day factors.

---

*Analysis conducted using Python scripts with comprehensive statistical analysis functions. Raw data and detailed calculations available in calculate_reimbursement.py with --analyze flag.* 