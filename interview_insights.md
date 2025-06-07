# Employee Interview Insights Analysis

This document analyzes the interviews from 5 employees to extract potential rules, patterns, and calculation logic for the legacy reimbursement system.

## Summary of Interviewees

1. **Marcus (Sales)** - Regional Sales Director, frequent traveler, focuses on practical patterns
2. **Lisa (Accounting)** - Senior Staff Accountant, sees data patterns from accounting perspective
3. **Dave (Marketing)** - Regional Marketing Manager, casual user with basic observations
4. **Jennifer (HR)** - HR Business Partner, sees complaint patterns and fairness issues
5. **Kevin (Procurement)** - Senior Procurement Analyst, obsessive data tracker with statistical analysis

## Core Calculation Components Identified

### 1. Base Per Diem
- **Base rate**: $100 per day (Lisa - Accounting)
- Applied to all trips as starting point
- Subject to various adjustments and bonuses

### 2. Mileage Calculation (Complex Tiered System)
- **Standard rate**: ~58 cents per mile for first 100 miles (Lisa)
- **Tiered structure**: Rate decreases after 100 miles in a non-linear curve
- **Not linear or simple percentage**: Lisa attempted Excel modeling, couldn't determine exact curve
- **Potential efficiency bonuses**: High miles-per-day ratios get bonuses
- **Sweet spot**: 180-220 miles per day for maximum bonuses (Kevin)
- **Diminishing returns**: Very high daily mileage (400+ miles) starts to get penalized

### 3. Receipt/Expense Processing
- **Baseline**: Small receipts (<$50-80) often get penalized vs. no receipts
- **Optimal ranges vary by trip length**:
  - Short trips: <$75/day optimal (Kevin)
  - Medium trips (4-6 days): Up to $120/day optimal (Kevin)
  - Long trips: <$90/day optimal to avoid penalties (Kevin)
- **Diminishing returns**: High expense amounts get progressively less reimbursement
- **Not proportional**: $1000 receipts → $800 reimbursement, $1200 receipts → $850 reimbursement (Lisa)

## Identified Patterns and Rules

### Trip Length Effects
1. **Sweet spot at 5 days**: Consistently gets bonuses (Lisa, Jennifer)
   - Exception: Some 5-day trips don't get bonus (reason unclear)
2. **Optimal range**: 4-6 days generally perform well (Jennifer, Kevin)
3. **Length penalties**: Very short (<3 days) and very long (8+ days) trips often penalized
4. **"Vacation penalty"**: 8+ day trips with high spending get significant penalties (Kevin)

### Efficiency Bonuses
1. **Miles per day ratio is crucial** (Kevin, Marcus)
2. **Optimal range**: 180-220 miles per day (Kevin's analysis)
3. **Below threshold**: <180 miles/day gets penalties
4. **Above threshold**: >220 miles/day bonuses start declining
5. **Extreme high mileage**: 400+ miles/day gets penalized (system assumes non-business activity)

### Seasonal and Timing Effects
1. **Quarterly patterns**:
   - End of Q4 more generous (Marcus)
   - Q2 was more generous last year but not this year (Lisa)
   - End of quarter generally busier but unclear if more generous
2. **Monthly patterns**:
   - Early vs. late month differences (Marcus noticed pattern)
   - End of month better than mid-month (Kevin)
3. **Weekly patterns**:
   - Tuesday submissions 8% higher than Friday (Kevin's data)
   - Thursday also good (Kevin)
   - Friday submissions consistently poor (Kevin)
4. **Lunar cycles**: 4% correlation between moon phases and reimbursements (Kevin)

### Department/User Patterns
1. **Sales department**: Generally better reimbursements (Jennifer)
2. **Experience effect**: Long-term employees do better (Jennifer)
3. **New employee penalty**: Lower reimbursements initially (Jennifer)
4. **User history**: System may track and adjust based on submission patterns (Marcus)

### Special Combinations and Bonuses
1. **"Sweet spot combo"**: 5-day trips + 180+ miles/day + <$100/day spending = guaranteed bonus (Kevin)
2. **High mileage + low spending**: Usually good outcomes
3. **Low mileage + high spending**: Usually poor outcomes
4. **Medium-high receipts ($600-800)**: Get particularly good treatment (Lisa)

## Contradictions and Inconsistencies

### Between Employees
1. **Seasonal patterns**: Marcus sees Q4 patterns, Lisa doesn't see consistent quarterly patterns
2. **Mileage calculations**: Marcus thinks 800-mile trips get better per-mile rates than 600-mile trips, but Lisa has contradictory evidence
3. **Submission timing**: Various theories (Tuesday vs. end-of-quarter) with no consensus

### Within Individual Experiences
1. **Identical trip variation**: Marcus had nearly identical Cleveland-Detroit trips with different reimbursements ($847 vs $623)
2. **5-day bonus exceptions**: Lisa noted 5-day trips that didn't get expected bonuses
3. **Experience variation**: Kevin notes his early tracked trips got different treatment than recent ones

## Potential Technical Explanations

### System Architecture Theories
1. **Multiple calculation paths**: Kevin theorizes 6 different paths based on trip characteristics
2. **Legacy evolution**: System likely started simple and had rules added over time (Lisa)
3. **Intentional complexity**: May be designed to prevent gaming (Dave, Kevin)
4. **Machine learning component**: System may adapt and learn from user patterns (Kevin)

### Calculation Method Theories
1. **Interaction effects**: Not just individual factors but combinations (trip_length × efficiency, spending_per_day × total_mileage) (Kevin)
2. **Threshold triggers**: Certain combinations trigger bonuses/penalties
3. **Decision tree structure**: Hidden branching logic based on trip characteristics
4. **Randomization component**: Some intentional noise to prevent gaming (Kevin)

## Specific Bugs or Quirks Identified

### Rounding Issues
1. **Receipt ending benefits**: Receipts ending in 49¢ or 99¢ often get extra money (Lisa)
2. **Double rounding**: System may round up twice in some cases

### Edge Cases
1. **Very small receipts**: Often worse than submitting no receipts at all
2. **High mileage anomalies**: Some very high mileage trips get unexpected bonuses
3. **Day-of-week submission effects**: Consistent patterns suggest system state varies by day

## Employees' Optimization Strategies

### Kevin (Most Sophisticated)
- Statistical analysis with k-means clustering
- 247 submissions tracked across multiple variables
- Can predict reimbursements within 15% accuracy
- Plans trips specifically to hit optimal combinations

### Sarah (Operations - mentioned by Jennifer)
- Plans routes and timing for optimization
- Treats reimbursement calculation "like a game"
- Gets consistently good results through strategic planning

### Marcus (Sales)
- Spaces out big trips based on "system memory" theory
- Avoids certain submission timings
- Focuses on end-of-quarter patterns

### Lisa (Accounting)
- Times lunch purchases to hit beneficial receipt endings (49¢, 99¢)
- Built multiple Excel models attempting to predict patterns

## Recommended Investigation Priorities

### High Confidence Patterns (Multiple Sources)
1. Trip length sweet spot around 5 days
2. Mileage efficiency bonuses (miles per day ratios)
3. Receipt amount optimal ranges varying by trip length
4. Small receipt penalties
5. End-of-quarter timing effects

### Medium Confidence Patterns (Single Strong Source)
1. Specific optimal ranges (Kevin's analysis)
2. Weekly submission timing effects
3. Department-based variations
4. User history/learning effects

### Low Confidence Patterns (Speculative)
1. Lunar cycle correlations
2. Market condition influences
3. Randomization algorithms
4. Geographic location effects

## Key Questions for Data Analysis

1. Can we identify the 6 calculation paths Kevin theorizes?
2. Is there evidence of the mileage efficiency curve Lisa described?
3. Do receipt amount optimal ranges vary by trip length as Kevin suggests?
4. Are there measurable seasonal/timing effects in the public test cases?
5. Is there evidence of randomization or noise in the calculations?
6. Can we identify the threshold values that trigger bonuses/penalties?

## Next Steps

1. Analyze public test cases for evidence of these patterns
2. Look for clustering in trip characteristics that might indicate different calculation paths
3. Test hypotheses about efficiency bonuses and receipt optimal ranges
4. Investigate timing and seasonal correlations in the data
5. Build models incorporating interaction effects between variables

---

*This analysis is based on employee interviews conducted March-April 2025. Employee theories should be validated against actual test case data before implementation.* 