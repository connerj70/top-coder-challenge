#!/usr/bin/env python3

def calculate_reimbursement_hypothesis1(duration, miles, receipts):
    base_rate = max(900 - (duration - 1) * 200, 100)
    receipt_component = receipts * 0.75
    miles_per_day = miles / duration
    efficiency_penalty = -max(0, (miles_per_day - 50) * 0.5)
    
    return base_rate + receipt_component + efficiency_penalty

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

print("Hypothesis 1 Test Results:")
print("| Case | Duration | Miles | Receipts | Expected | Predicted | Error | Error % |")
print("|------|----------|-------|----------|----------|-----------|-------|---------|")

total_error = 0
accurate_count = 0

for duration, miles, receipts, expected, case_letter in test_cases:
    predicted = calculate_reimbursement_hypothesis1(duration, miles, receipts)
    error = predicted - expected
    error_pct = (error / expected) * 100
    
    if abs(error_pct) <= 25:
        accurate_count += 1
    
    total_error += abs(error_pct)
    
    print(f"| {case_letter} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | ${predicted:.2f} | {error:+.2f} | {error_pct:+.1f}% |")

print(f"\nSummary:")
print(f"Accurate predictions (±25% error): {accurate_count}/15 ({accurate_count/15*100:.1f}%)")
print(f"Average absolute error: {total_error/15:.1f}%")

# Let's also test a refined version
print("\n" + "="*80)
print("REFINED VERSION - Lower base rates, higher receipt multiplier:")

def calculate_reimbursement_hypothesis1_refined(duration, miles, receipts):
    base_rate = max(100 - (duration - 1) * 10, 50)  # Much lower base
    receipt_component = receipts * 1.0  # Higher receipt multiplier
    miles_per_day = miles / duration
    efficiency_penalty = -max(0, (miles_per_day - 30) * 2.0)  # Stronger penalty
    
    return base_rate + receipt_component + efficiency_penalty

print("| Case | Duration | Miles | Receipts | Expected | Predicted | Error | Error % |")
print("|------|----------|-------|----------|----------|-----------|-------|---------|")

total_error_refined = 0
accurate_count_refined = 0

for duration, miles, receipts, expected, case_letter in test_cases:
    predicted = calculate_reimbursement_hypothesis1_refined(duration, miles, receipts)
    error = predicted - expected
    error_pct = (error / expected) * 100
    
    if abs(error_pct) <= 25:
        accurate_count_refined += 1
    
    total_error_refined += abs(error_pct)
    
    print(f"| {case_letter} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | ${predicted:.2f} | {error:+.2f} | {error_pct:+.1f}% |")

print(f"\nRefined Summary:")
print(f"Accurate predictions (±25% error): {accurate_count_refined}/15 ({accurate_count_refined/15*100:.1f}%)")
print(f"Average absolute error: {total_error_refined/15:.1f}%")
print(f"Improvement: {total_error/15 - total_error_refined/15:.1f} percentage points better") 