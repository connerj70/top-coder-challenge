#!/usr/bin/env python3

def calculate_reimbursement_hypothesis2(duration, miles, receipts):
    # Receipt base calculation
    receipt_base = receipts * 1.1
    
    # Receipt multiplier based on amount
    if receipts < 300:
        receipt_multiplier = 0.8
    elif receipts < 800:
        receipt_multiplier = 1.0
    elif receipts < 1500:
        receipt_multiplier = 1.1
    else:
        receipt_multiplier = 0.95
    
    # Efficiency penalty factor
    miles_per_day = miles / duration
    if miles_per_day <= 40:
        efficiency_factor = 1.2
    elif miles_per_day <= 80:
        efficiency_factor = 1.0
    elif miles_per_day <= 150:
        efficiency_factor = 0.8
    elif miles_per_day <= 250:
        efficiency_factor = 0.5
    else:
        efficiency_factor = 0.3
    
    # Duration bonus
    if duration == 1:
        duration_bonus = 50
    elif 2 <= duration <= 4:
        duration_bonus = 100
    elif duration == 5:
        duration_bonus = 80
    elif 6 <= duration <= 8:
        duration_bonus = 60
    else:
        duration_bonus = 40
    
    return receipt_base * receipt_multiplier * efficiency_factor + duration_bonus

# Test cases from our sample
test_cases = [
    (1, 47, 17.97, 128.91, 'A'),
    (1, 55, 3.60, 126.06, 'B'),
    (2, 68, 756.61, 648.53, 'C'),
    (4, 159, 568.58, 647.00, 'D'),
    (3, 182, 347.82, 384.77, 'E'),
    (5, 831, 591.65, 1090.31, 'F'),
    (5, 1028, 653.19, 1313.95, 'G'),
    (5, 210, 710.49, 483.34, 'H'),
    (12, 482, 1710.47, 1746.74, 'I'),
    (8, 592, 1402.98, 1561.41, 'J'),
    (5, 751, 407.43, 1063.46, 'K'),
    (5, 262, 1173.79, 1485.59, 'L'),
    (2, 623, 347.54, 625.15, 'M'),
    (2, 941, 1565.77, 1432.79, 'N'),
    (9, 963, 588.50, 1434.42, 'O'),
]

print("Hypothesis 2: Efficiency-Penalty Focused Model Test Results:")
print("| Case | Duration | Miles | Receipts | Expected | Predicted | Error | Error % | Efficiency |")
print("|------|----------|-------|----------|----------|-----------|-------|---------|------------|")

total_error = 0
accurate_count = 0

for duration, miles, receipts, expected, case_letter in test_cases:
    predicted = calculate_reimbursement_hypothesis2(duration, miles, receipts)
    error = predicted - expected
    error_pct = (error / expected) * 100
    miles_per_day = miles / duration
    
    if abs(error_pct) <= 25:
        accurate_count += 1
    
    total_error += abs(error_pct)
    
    print(f"| {case_letter} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | ${predicted:.2f} | {error:+.2f} | {error_pct:+.1f}% | {miles_per_day:.1f} mi/day |")

print(f"\nSummary:")
print(f"Accurate predictions (±25% error): {accurate_count}/15 ({accurate_count/15*100:.1f}%)")
print(f"Average absolute error: {total_error/15:.1f}%")

# Test a refined version with softer penalties
print("\n" + "="*80)
print("REFINED VERSION - Softer efficiency penalties, better low-receipt handling:")

def calculate_reimbursement_hypothesis2_refined(duration, miles, receipts):
    # Receipt base calculation with minimum for low receipts
    if receipts < 50:
        receipt_base = max(receipts * 1.1, 80)
    else:
        receipt_base = receipts * 1.1
    
    # Receipt multiplier based on amount
    if receipts < 300:
        receipt_multiplier = 0.9  # Less penalty for low receipts
    elif receipts < 800:
        receipt_multiplier = 1.0
    elif receipts < 1500:
        receipt_multiplier = 1.1
    else:
        receipt_multiplier = 0.95
    
    # Efficiency penalty factor (softer penalties)
    miles_per_day = miles / duration
    if miles_per_day <= 40:
        efficiency_factor = 1.2
    elif miles_per_day <= 80:
        efficiency_factor = 1.0
    elif miles_per_day <= 150:
        efficiency_factor = 0.85  # Less penalty
    elif miles_per_day <= 250:
        efficiency_factor = 0.6   # Less penalty
    else:
        efficiency_factor = 0.4   # Less severe penalty
    
    # Duration bonus (higher for short trips)
    if duration == 1:
        duration_bonus = 100  # Higher bonus
    elif 2 <= duration <= 4:
        duration_bonus = 100
    elif duration == 5:
        duration_bonus = 80
    elif 6 <= duration <= 8:
        duration_bonus = 60
    else:
        duration_bonus = 40
    
    return receipt_base * receipt_multiplier * efficiency_factor + duration_bonus

print("| Case | Duration | Miles | Receipts | Expected | Predicted | Error | Error % | Efficiency |")
print("|------|----------|-------|----------|----------|-----------|-------|---------|------------|")

total_error_refined = 0
accurate_count_refined = 0

for duration, miles, receipts, expected, case_letter in test_cases:
    predicted = calculate_reimbursement_hypothesis2_refined(duration, miles, receipts)
    error = predicted - expected
    error_pct = (error / expected) * 100
    miles_per_day = miles / duration
    
    if abs(error_pct) <= 25:
        accurate_count_refined += 1
    
    total_error_refined += abs(error_pct)
    
    print(f"| {case_letter} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | ${predicted:.2f} | {error:+.2f} | {error_pct:+.1f}% | {miles_per_day:.1f} mi/day |")

print(f"\nRefined Summary:")
print(f"Accurate predictions (±25% error): {accurate_count_refined}/15 ({accurate_count_refined/15*100:.1f}%)")
print(f"Average absolute error: {total_error_refined/15:.1f}%")
print(f"Improvement: {total_error/15 - total_error_refined/15:.1f} percentage points better")

# Compare with Hypothesis 1 refined results
print(f"\nComparison with Hypothesis 1 (Refined):")
print(f"Hypothesis 1 accuracy: 33.3% (5/15 cases)")
print(f"Hypothesis 2 accuracy: {accurate_count_refined/15*100:.1f}% ({accurate_count_refined}/15 cases)")
print(f"Hypothesis 1 avg error: 44.4%")
print(f"Hypothesis 2 avg error: {total_error_refined/15:.1f}%") 