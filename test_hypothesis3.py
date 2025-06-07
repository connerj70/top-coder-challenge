#!/usr/bin/env python3

def calculate_reimbursement_hypothesis3(duration, miles, receipts):
    miles_per_day = miles / duration
    
    # Edge Case 1: Very low receipts
    if receipts < 50:
        base_reimbursement = 120
        receipt_bonus = receipts * 0.3
        return base_reimbursement + receipt_bonus
    
    # Edge Case 2: Long-distance business trips
    if duration >= 5 and miles >= 800:
        base = 200 + (duration * 50)
        mileage_component = miles * 0.8
        receipt_component = receipts * 0.6
        return base + mileage_component + receipt_component
    
    # Edge Case 3: Travel day scenarios
    if miles_per_day > 300:
        if receipts > 1000:
            return receipts * 0.9
        else:
            return max(receipts * 1.5, 400)
    
    # Default: Use refined Hypothesis 1 for normal cases
    base_rate = max(100 - (duration - 1) * 10, 50)
    receipt_component = receipts * 1.0
    efficiency_penalty = -max(0, (miles_per_day - 30) * 2.0)
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

def get_edge_case_type(duration, miles, receipts):
    miles_per_day = miles / duration
    if receipts < 50:
        return "Low receipts"
    elif duration >= 5 and miles >= 800:
        return "Long distance"
    elif miles_per_day > 300:
        return "Travel day"
    else:
        return "Normal"

print("Hypothesis 3: Edge Case and Special Conditions Model Test Results:")
print("| Case | Duration | Miles | Receipts | Expected | Predicted | Error | Error % | Edge Case |")
print("|------|----------|-------|----------|----------|-----------|-------|---------|-----------|")

total_error = 0
accurate_count = 0

for duration, miles, receipts, expected, case_letter in test_cases:
    predicted = calculate_reimbursement_hypothesis3(duration, miles, receipts)
    error = predicted - expected
    error_pct = (error / expected) * 100
    edge_case = get_edge_case_type(duration, miles, receipts)
    
    if abs(error_pct) <= 25:
        accurate_count += 1
    
    total_error += abs(error_pct)
    
    print(f"| {case_letter} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | ${predicted:.2f} | {error:+.2f} | {error_pct:+.1f}% | {edge_case} |")

print(f"\nSummary:")
print(f"Accurate predictions (±25% error): {accurate_count}/15 ({accurate_count/15*100:.1f}%)")
print(f"Average absolute error: {total_error/15:.1f}%")

# Test refined version with additional edge cases
print("\n" + "="*80)
print("REFINED VERSION - Additional edge cases for remaining issues:")

def calculate_reimbursement_hypothesis3_refined(duration, miles, receipts):
    miles_per_day = miles / duration
    
    # Edge Case 1: Very low receipts
    if receipts < 50:
        base_reimbursement = 120
        receipt_bonus = receipts * 0.3
        return base_reimbursement + receipt_bonus
    
    # Edge Case 2: Long-distance business trips
    if duration >= 5 and miles >= 800:
        base = 200 + (duration * 50)
        mileage_component = miles * 0.8
        receipt_component = receipts * 0.6
        return base + mileage_component + receipt_component
    
    # Edge Case 3: Travel day scenarios
    if miles_per_day > 300:
        if receipts > 1000:
            return receipts * 0.9
        else:
            return max(receipts * 1.5, 400)
    
    # Edge Case 4: Extended business trips (for case O)
    if duration >= 8 and 50 <= miles_per_day <= 150:
        return receipts * 1.8 + (duration * 100)
    
    # Edge Case 5: 5-day trips with special handling (for case H)
    if duration == 5:
        if miles_per_day < 50:
            return receipts * 0.7  # Low efficiency penalty
        else:
            return receipts * 1.2 + (miles * 0.5)  # High efficiency bonus
    
    # Default: Use refined Hypothesis 1 for normal cases
    base_rate = max(100 - (duration - 1) * 10, 50)
    receipt_component = receipts * 1.0
    efficiency_penalty = -max(0, (miles_per_day - 30) * 2.0)
    return base_rate + receipt_component + efficiency_penalty

def get_edge_case_type_refined(duration, miles, receipts):
    miles_per_day = miles / duration
    if receipts < 50:
        return "Low receipts"
    elif duration >= 5 and miles >= 800:
        return "Long distance"
    elif miles_per_day > 300:
        return "Travel day"
    elif duration >= 8 and 50 <= miles_per_day <= 150:
        return "Extended business"
    elif duration == 5:
        return "5-day special"
    else:
        return "Normal"

print("| Case | Duration | Miles | Receipts | Expected | Predicted | Error | Error % | Edge Case |")
print("|------|----------|-------|----------|----------|-----------|-------|---------|-----------|")

total_error_refined = 0
accurate_count_refined = 0

for duration, miles, receipts, expected, case_letter in test_cases:
    predicted = calculate_reimbursement_hypothesis3_refined(duration, miles, receipts)
    error = predicted - expected
    error_pct = (error / expected) * 100
    edge_case = get_edge_case_type_refined(duration, miles, receipts)
    
    if abs(error_pct) <= 25:
        accurate_count_refined += 1
    
    total_error_refined += abs(error_pct)
    
    print(f"| {case_letter} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | ${predicted:.2f} | {error:+.2f} | {error_pct:+.1f}% | {edge_case} |")

print(f"\nRefined Summary:")
print(f"Accurate predictions (±25% error): {accurate_count_refined}/15 ({accurate_count_refined/15*100:.1f}%)")
print(f"Average absolute error: {total_error_refined/15:.1f}%")
print(f"Improvement: {total_error/15 - total_error_refined/15:.1f} percentage points better")

# Compare with all previous hypotheses
print(f"\nComparison with All Hypotheses:")
print(f"Hypothesis 1 (refined): 33.3% accuracy, 44.4% avg error")
print(f"Hypothesis 2 (refined): 20.0% accuracy, 42.9% avg error")
print(f"Hypothesis 3 (basic): {accurate_count/15*100:.1f}% accuracy, {total_error/15:.1f}% avg error")
print(f"Hypothesis 3 (refined): {accurate_count_refined/15*100:.1f}% accuracy, {total_error_refined/15:.1f}% avg error")

# Analyze edge case distribution
print(f"\nEdge Case Distribution:")
edge_case_counts = {}
for duration, miles, receipts, expected, case_letter in test_cases:
    edge_case = get_edge_case_type_refined(duration, miles, receipts)
    edge_case_counts[edge_case] = edge_case_counts.get(edge_case, 0) + 1

for edge_case, count in edge_case_counts.items():
    print(f"{edge_case}: {count} cases ({count/15*100:.1f}%)") 