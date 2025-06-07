#!/usr/bin/env python3

import json
import random

# Load test cases
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Select diverse sample
random.seed(42)  # For reproducibility
sample_cases = []

# Get diverse cases covering different ranges
ranges = [
    {'duration': (1, 2), 'miles': (5, 100), 'receipts': (0, 200)},      # Short, low efficiency, low receipts
    {'duration': (1, 2), 'miles': (5, 100), 'receipts': (500, 1000)},   # Short, low efficiency, high receipts
    {'duration': (3, 4), 'miles': (100, 300), 'receipts': (200, 600)},  # Medium trip
    {'duration': (5, 5), 'miles': (800, 1200), 'receipts': (500, 800)}, # Test employee "5-day sweet spot"
    {'duration': (5, 5), 'miles': (200, 220), 'receipts': (600, 800)},  # Test efficiency "sweet spot"
    {'duration': (8, 12), 'miles': (300, 800), 'receipts': (1000, 2000)}, # Long trips
]

for r in ranges:
    matching = [case for case in data if 
                r['duration'][0] <= case['input']['trip_duration_days'] <= r['duration'][1] and
                r['miles'][0] <= case['input']['miles_traveled'] <= r['miles'][1] and
                r['receipts'][0] <= case['input']['total_receipts_amount'] <= r['receipts'][1]]
    if matching:
        sample_cases.extend(random.sample(matching, min(2, len(matching))))

# Add some random cases to reach 15
remaining_needed = 15 - len(sample_cases)
if remaining_needed > 0:
    remaining_pool = [case for case in data if case not in sample_cases]
    sample_cases.extend(random.sample(remaining_pool, remaining_needed))

# Print results
print('Selected 15 test cases for hypothesis development:')
print()
print('| Case | Duration | Miles | Receipts | Expected | Miles/Day | Notes |')
print('|------|----------|-------|----------|----------|-----------|-------|')

for i, case in enumerate(sample_cases[:15]):
    inputs = case['input']
    expected = case['expected_output']
    duration = inputs['trip_duration_days']
    miles = inputs['miles_traveled']
    receipts = inputs['total_receipts_amount']
    miles_per_day = miles / duration
    
    notes = ""
    if duration == 1:
        notes = "1-day test"
    elif duration == 5 and 180 <= miles_per_day <= 220:
        notes = "Employee sweet spot test"
    elif duration == 5:
        notes = "5-day test"
    elif miles_per_day < 50:
        notes = "Low efficiency"
    elif miles_per_day > 300:
        notes = "High efficiency"
    
    print(f'| {chr(65+i)} | {duration} | {miles:.0f} | ${receipts:.2f} | ${expected:.2f} | {miles_per_day:.1f} | {notes} |')

print()
print("Detailed cases for analysis:")
for i, case in enumerate(sample_cases[:15]):
    inputs = case['input']
    expected = case['expected_output']
    print(f"Case {chr(65+i)}: {inputs['trip_duration_days']} days, {inputs['miles_traveled']:.1f} miles, ${inputs['total_receipts_amount']:.2f} receipts -> ${expected:.2f} expected") 