#!/usr/bin/env python3
"""
Detailed Error Analysis for Task 10.6
Analyzes the worst-performing test cases to identify specific patterns for targeted fixes
"""

import json
import sys
from calculate_reimbursement import calculate_reimbursement, load_public_test_cases

def load_and_analyze_worst_cases(num_worst=50):
    """
    Load all test cases, calculate errors, and identify the worst-performing cases.
    
    Args:
        num_worst (int): Number of worst cases to analyze in detail
        
    Returns:
        dict: Analysis results including worst cases and patterns
    """
    print(f"Loading test cases and analyzing worst {num_worst} cases...")
    
    # Load test cases
    test_cases = load_public_test_cases()
    
    # Calculate errors for all cases
    error_analysis = []
    
    for i, case in enumerate(test_cases):
        if i % 100 == 0:
            print(f"Processing case {i+1}/{len(test_cases)}...")
            
        input_data = case['input']
        expected = case['expected_output']
        
        # Extract inputs
        days = input_data['trip_duration_days']
        miles = input_data['miles_traveled']
        receipts = input_data['total_receipts_amount']
        
        # Calculate our reimbursement
        calculated = calculate_reimbursement(days, miles, receipts)
        
        # Calculate errors
        absolute_error = abs(calculated - expected)
        percentage_error = (absolute_error / expected * 100) if expected > 0 else 0
        
        # Determine error direction
        direction = "overestimate" if calculated > expected else "underestimate"
        
        # Calculate derived metrics
        miles_per_day = miles / days if days > 0 else 0
        receipts_per_day = receipts / days if days > 0 else 0
        
        error_analysis.append({
            'case_id': i,
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'miles_per_day': miles_per_day,
            'receipts_per_day': receipts_per_day,
            'expected': expected,
            'calculated': calculated,
            'absolute_error': absolute_error,
            'percentage_error': percentage_error,
            'direction': direction
        })
    
    # Sort by absolute error to find worst cases
    error_analysis.sort(key=lambda x: x['absolute_error'], reverse=True)
    
    return {
        'all_cases': error_analysis,
        'worst_cases': error_analysis[:num_worst],
        'total_cases': len(error_analysis)
    }

def analyze_error_patterns(worst_cases):
    """
    Analyze patterns in the worst-performing cases.
    
    Args:
        worst_cases (list): List of worst-performing cases
        
    Returns:
        dict: Pattern analysis results
    """
    print("Analyzing error patterns...")
    
    patterns = {
        'high_receipt_overestimation': [],
        'long_trip_underestimation': [],
        'single_day_extremes': [],
        'moderate_receipt_long_trips': [],
        'very_high_mileage': [],
        'other_patterns': []
    }
    
    for case in worst_cases:
        days = case['days']
        miles = case['miles']
        receipts = case['receipts']
        receipts_per_day = case['receipts_per_day']
        miles_per_day = case['miles_per_day']
        direction = case['direction']
        error = case['absolute_error']
        
        # Categorize by pattern
        categorized = False
        
        # High receipt overestimation pattern
        if (receipts >= 1800 and direction == "overestimate" and error > 800):
            patterns['high_receipt_overestimation'].append(case)
            categorized = True
        
        # Long trip underestimation pattern  
        elif (days >= 8 and receipts_per_day < 200 and direction == "underestimate" and error > 500):
            patterns['long_trip_underestimation'].append(case)
            categorized = True
        
        # Single day extreme cases
        elif (days <= 1.5 and (receipts > 1500 or miles > 800)):
            patterns['single_day_extremes'].append(case)
            categorized = True
        
        # Moderate receipt long trips
        elif (days >= 7 and 100 <= receipts_per_day <= 300):
            patterns['moderate_receipt_long_trips'].append(case)
            categorized = True
            
        # Very high mileage cases
        elif (miles_per_day > 400):
            patterns['very_high_mileage'].append(case)
            categorized = True
        
        if not categorized:
            patterns['other_patterns'].append(case)
    
    return patterns

def analyze_high_receipt_cases(cases):
    """
    Detailed analysis of high-receipt overestimation cases.
    
    Args:
        cases (list): List of high-receipt cases
        
    Returns:
        dict: Detailed analysis
    """
    if not cases:
        return {}
    
    print(f"Analyzing {len(cases)} high-receipt overestimation cases...")
    
    analysis = {
        'count': len(cases),
        'receipt_ranges': {},
        'duration_impact': {},
        'average_overestimation': 0,
        'specific_examples': []
    }
    
    # Analyze by receipt ranges
    receipt_ranges = [
        (1800, 2000, "1800-2000"),
        (2000, 2200, "2000-2200"), 
        (2200, 2500, "2200-2500"),
        (2500, float('inf'), "2500+")
    ]
    
    total_error = 0
    
    for case in cases:
        total_error += case['absolute_error']
        
        # Categorize by receipt range
        receipts = case['receipts']
        for min_r, max_r, label in receipt_ranges:
            if min_r <= receipts < max_r:
                if label not in analysis['receipt_ranges']:
                    analysis['receipt_ranges'][label] = {'count': 0, 'total_error': 0, 'cases': []}
                analysis['receipt_ranges'][label]['count'] += 1
                analysis['receipt_ranges'][label]['total_error'] += case['absolute_error']
                analysis['receipt_ranges'][label]['cases'].append(case)
                break
        
        # Store top examples
        if len(analysis['specific_examples']) < 10:
            analysis['specific_examples'].append({
                'case_id': case['case_id'],
                'days': case['days'],
                'miles': case['miles'],
                'receipts': case['receipts'],
                'expected': case['expected'],
                'calculated': case['calculated'],
                'error': case['absolute_error']
            })
    
    analysis['average_overestimation'] = total_error / len(cases)
    
    # Calculate averages for each range
    for label, data in analysis['receipt_ranges'].items():
        if data['count'] > 0:
            data['average_error'] = data['total_error'] / data['count']
    
    return analysis

def analyze_long_trip_cases(cases):
    """
    Detailed analysis of long trip underestimation cases.
    
    Args:
        cases (list): List of long trip cases
        
    Returns:
        dict: Detailed analysis
    """
    if not cases:
        return {}
    
    print(f"Analyzing {len(cases)} long trip underestimation cases...")
    
    analysis = {
        'count': len(cases),
        'duration_ranges': {},
        'receipt_patterns': {},
        'average_underestimation': 0,
        'specific_examples': []
    }
    
    total_error = 0
    
    for case in cases:
        total_error += case['absolute_error']
        
        # Categorize by duration
        days = case['days']
        duration_key = f"{int(days//2)*2}-{int(days//2)*2+1}"
        if duration_key not in analysis['duration_ranges']:
            analysis['duration_ranges'][duration_key] = {'count': 0, 'total_error': 0, 'cases': []}
        analysis['duration_ranges'][duration_key]['count'] += 1
        analysis['duration_ranges'][duration_key]['total_error'] += case['absolute_error']
        analysis['duration_ranges'][duration_key]['cases'].append(case)
        
        # Store examples
        if len(analysis['specific_examples']) < 10:
            analysis['specific_examples'].append({
                'case_id': case['case_id'],
                'days': case['days'],
                'miles': case['miles'],
                'receipts': case['receipts'],
                'receipts_per_day': case['receipts_per_day'],
                'expected': case['expected'],
                'calculated': case['calculated'],
                'error': case['absolute_error']
            })
    
    analysis['average_underestimation'] = total_error / len(cases)
    
    # Calculate averages for each range
    for label, data in analysis['duration_ranges'].items():
        if data['count'] > 0:
            data['average_error'] = data['total_error'] / data['count']
    
    return analysis

def print_detailed_analysis(analysis_results):
    """
    Print detailed analysis results in a readable format.
    
    Args:
        analysis_results (dict): Complete analysis results
    """
    worst_cases = analysis_results['worst_cases']
    patterns = analysis_results['patterns']
    
    print("\n" + "="*80)
    print("DETAILED ERROR ANALYSIS RESULTS - TASK 10.6")
    print("="*80)
    
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"Total cases analyzed: {analysis_results['total_cases']}")
    print(f"Worst cases examined: {len(worst_cases)}")
    
    if worst_cases:
        total_error = sum(case['absolute_error'] for case in worst_cases)
        avg_error = total_error / len(worst_cases)
        print(f"Average error in worst {len(worst_cases)} cases: ${avg_error:.2f}")
        print(f"Worst single error: ${worst_cases[0]['absolute_error']:.2f}")
    
    print(f"\n🎯 PATTERN BREAKDOWN:")
    for pattern_name, cases in patterns.items():
        if cases:
            avg_error = sum(case['absolute_error'] for case in cases) / len(cases)
            print(f"  {pattern_name.replace('_', ' ').title()}: {len(cases)} cases, avg error ${avg_error:.2f}")
    
    # Detailed analysis for high receipt cases
    if patterns['high_receipt_overestimation']:
        print(f"\n🔥 HIGH RECEIPT OVERESTIMATION ANALYSIS:")
        high_receipt_analysis = analyze_high_receipt_cases(patterns['high_receipt_overestimation'])
        
        print(f"Total cases: {high_receipt_analysis['count']}")
        print(f"Average overestimation: ${high_receipt_analysis['average_overestimation']:.2f}")
        
        print(f"\nBy receipt range:")
        for range_label, data in high_receipt_analysis['receipt_ranges'].items():
            print(f"  ${range_label}: {data['count']} cases, avg error ${data['average_error']:.2f}")
        
        print(f"\nTop examples:")
        for i, example in enumerate(high_receipt_analysis['specific_examples'][:5], 1):
            print(f"  {i}. Case {example['case_id']}: {example['days']} days, {example['miles']} miles, ${example['receipts']:.2f} receipts")
            print(f"     Expected: ${example['expected']:.2f}, Got: ${example['calculated']:.2f}, Error: ${example['error']:.2f}")
    
    # Detailed analysis for long trip cases
    if patterns['long_trip_underestimation']:
        print(f"\n📏 LONG TRIP UNDERESTIMATION ANALYSIS:")
        long_trip_analysis = analyze_long_trip_cases(patterns['long_trip_underestimation'])
        
        print(f"Total cases: {long_trip_analysis['count']}")
        print(f"Average underestimation: ${long_trip_analysis['average_underestimation']:.2f}")
        
        print(f"\nTop examples:")
        for i, example in enumerate(long_trip_analysis['specific_examples'][:5], 1):
            print(f"  {i}. Case {example['case_id']}: {example['days']} days, {example['miles']} miles, ${example['receipts']:.2f} receipts")
            print(f"     Receipts/day: ${example['receipts_per_day']:.2f}")
            print(f"     Expected: ${example['expected']:.2f}, Got: ${example['calculated']:.2f}, Error: ${example['error']:.2f}")
    
    # Other significant patterns
    for pattern_name in ['single_day_extremes', 'moderate_receipt_long_trips', 'very_high_mileage']:
        if patterns[pattern_name]:
            cases = patterns[pattern_name]
            avg_error = sum(case['absolute_error'] for case in cases) / len(cases)
            print(f"\n📋 {pattern_name.replace('_', ' ').upper()}:")
            print(f"Count: {len(cases)}, Average error: ${avg_error:.2f}")
            
            for i, case in enumerate(cases[:3], 1):
                print(f"  {i}. Case {case['case_id']}: {case['days']} days, {case['miles']} miles, ${case['receipts']:.2f} receipts")
                print(f"     Expected: ${case['expected']:.2f}, Got: ${case['calculated']:.2f}, Error: ${case['absolute_error']:.2f} ({case['direction']})")

def save_analysis_to_file(analysis_results, filename="task_10_6_error_analysis.json"):
    """
    Save detailed analysis results to a JSON file for further processing.
    
    Args:
        analysis_results (dict): Complete analysis results
        filename (str): Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(analysis_results, f, indent=2)
        print(f"\n💾 Detailed analysis saved to {filename}")
    except Exception as e:
        print(f"⚠️  Could not save analysis to file: {e}")

def main():
    """
    Main function to run the comprehensive error analysis for Task 10.6.
    """
    print("🔍 TASK 10.6: DETAILED ERROR ANALYSIS")
    print("Analyzing worst-performing cases to identify patterns for targeted fixes")
    print("-" * 80)
    
    try:
        # Load and analyze worst cases
        analysis_results = load_and_analyze_worst_cases(num_worst=50)
        
        # Analyze patterns in worst cases
        patterns = analyze_error_patterns(analysis_results['worst_cases'])
        analysis_results['patterns'] = patterns
        
        # Print detailed analysis
        print_detailed_analysis(analysis_results)
        
        # Save to file for further analysis
        save_analysis_to_file(analysis_results)
        
        print(f"\n✅ Error analysis complete!")
        print(f"\n🎯 KEY FINDINGS SUMMARY:")
        print(f"1. High-receipt overestimation: {len(patterns['high_receipt_overestimation'])} cases")
        print(f"2. Long-trip underestimation: {len(patterns['long_trip_underestimation'])} cases") 
        print(f"3. Single-day extremes: {len(patterns['single_day_extremes'])} cases")
        print(f"4. Moderate-receipt long trips: {len(patterns['moderate_receipt_long_trips'])} cases")
        print(f"5. Very high mileage: {len(patterns['very_high_mileage'])} cases")
        
        print(f"\n📋 NEXT STEPS:")
        print(f"- Focus first on high-receipt overestimation (highest error impact)")
        print(f"- Address long-trip underestimation (Version 3.0 improvement needed)")
        print(f"- Fine-tune extreme cases handling")
        
    except Exception as e:
        print(f"❌ Error analysis failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 