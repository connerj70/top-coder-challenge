#!/usr/bin/env python3
"""
Test script for pattern analysis on real data
"""

from calculate_reimbursement import *

def analyze_real_error_patterns():
    """Analyze error patterns on real test cases using our current model."""
    print("Loading test cases...")
    test_cases = load_public_test_cases('public_cases.json')
    
    # Test on first 100 cases for quick analysis
    print("Analyzing first 100 cases...")
    sample_cases = test_cases[:100]
    
    # Calculate our predictions and get error metrics
    calculated = []
    expected = []
    
    for case in sample_cases:
        inputs = case['input']
        calc_value = calculate_reimbursement(
            inputs['trip_duration_days'],
            inputs['miles_traveled'],
            inputs['total_receipts_amount']
        )
        calculated.append(calc_value)
        expected.append(case['expected_output'])
    
    # Get error metrics
    error_metrics = calculate_error_metrics(calculated, expected)
    error_data = error_metrics['error_data']
    
    # Analyze patterns
    print("Analyzing error patterns...")
    patterns = analyze_error_patterns(error_data, sample_cases)
    
    # Print comprehensive pattern analysis
    print("\n" + "="*70)
    print("ERROR PATTERN ANALYSIS")
    print("="*70)
    
    # Critical Issues
    print(f"\n🚨 CRITICAL ISSUES:")
    critical = patterns['critical_issues']
    for issue_type, cases in critical.items():
        if cases:
            count = len(cases)
            percentage = patterns['summary']['critical_issues'][issue_type]['percentage_of_total']
            print(f"  {issue_type.replace('_', ' ').title()}: {count} cases ({percentage:.1f}%)")
            
            # Show examples
            for i, case in enumerate(cases[:3]):  # Show first 3 examples
                inputs = case['inputs']
                print(f"    Example {i+1}: {inputs['trip_duration_days']} days, {inputs['miles_traveled']} miles, ${inputs['total_receipts_amount']:.2f}")
                print(f"      Calculated: ${case['calculated']:.2f}, Expected: ${case['expected']:.2f}")
    
    # Error Type Distribution
    print(f"\n📊 ERROR TYPE DISTRIBUTION:")
    error_types = patterns['summary']['error_types']
    for error_type, stats in error_types.items():
        if stats['count'] > 0:
            print(f"  {error_type.replace('_', ' ').title()}: {stats['count']} cases")
            print(f"    Avg Absolute Error: ${stats['avg_abs_error']:.2f}")
            print(f"    Avg Percentage Error: {stats['avg_pct_error']:.1f}%")
    
    # Magnitude Groups
    print(f"\n💥 ERROR MAGNITUDE DISTRIBUTION:")
    magnitudes = patterns['summary']['magnitudes']
    for magnitude, stats in magnitudes.items():
        if stats['count'] > 0:
            print(f"  {magnitude.title()}: {stats['count']} cases (avg: ${stats['avg_abs_error']:.2f})")
    
    # Input Correlations
    print(f"\n🔍 INPUT CORRELATIONS:")
    
    # Trip Duration Correlations
    print(f"\n  By Trip Duration:")
    duration_corr = patterns['input_correlation_patterns']['by_trip_duration']
    for duration_cat, stats in duration_corr.items():
        if isinstance(stats, dict) and 'count' in stats:
            print(f"    {duration_cat.replace('_', ' ').title()}: {stats['count']} cases")
            print(f"      Mean Abs Error: ${stats['mean_absolute_error']:.2f}")
            print(f"      Mean % Error: {stats['mean_percentage_error']:.1f}%")
            print(f"      Overestimate Rate: {stats['overestimate_rate']:.1f}%")
    
    # Efficiency Correlations
    print(f"\n  By Efficiency Category:")
    efficiency_corr = patterns['input_correlation_patterns']['by_efficiency_category']
    for efficiency_cat, stats in efficiency_corr.items():
        if isinstance(stats, dict) and 'count' in stats:
            print(f"    {efficiency_cat.replace('_', ' ').title()}: {stats['count']} cases")
            print(f"      Mean Abs Error: ${stats['mean_absolute_error']:.2f}")
            print(f"      Mean % Error: {stats['mean_percentage_error']:.1f}%")
            print(f"      Overestimate Rate: {stats['overestimate_rate']:.1f}%")
    
    # Receipt Range Correlations
    print(f"\n  By Receipt Range:")
    receipt_corr = patterns['input_correlation_patterns']['by_receipt_range']
    for receipt_cat, stats in receipt_corr.items():
        if isinstance(stats, dict) and 'count' in stats:
            print(f"    {receipt_cat.replace('_', ' ').title()}: {stats['count']} cases")
            print(f"      Mean Abs Error: ${stats['mean_absolute_error']:.2f}")
            print(f"      Mean % Error: {stats['mean_percentage_error']:.1f}%")
            print(f"      Overestimate Rate: {stats['overestimate_rate']:.1f}%")
    
    # Find worst performing combinations
    print(f"\n🎯 WORST PERFORMING COMBINATIONS:")
    combined_corr = patterns['input_correlation_patterns']['by_combined_factors']
    worst_combinations = []
    
    for combo_key, stats in combined_corr.items():
        if isinstance(stats, dict) and 'count' in stats and stats['count'] >= 2:
            worst_combinations.append((combo_key, stats['mean_percentage_error'], stats['count']))
    
    # Sort by worst mean percentage error
    worst_combinations.sort(key=lambda x: x[1], reverse=True)
    
    for i, (combo, error, count) in enumerate(worst_combinations[:5]):
        duration_cat, efficiency_cat = combo.split('_', 1)
        print(f"  {i+1}. {duration_cat.replace('_', ' ').title()} + {efficiency_cat.replace('_', ' ').title()}")
        print(f"     {count} cases, {error:.1f}% avg error")
    
    # Actionable Insights
    print(f"\n💡 KEY INSIGHTS:")
    
    # Check for negative value pattern
    if patterns['critical_issues']['negative_values']:
        print("  🚨 Model produces negative reimbursements - critical bug!")
        negative_cases = patterns['critical_issues']['negative_values']
        efficiency_categories = [case['derived_metrics']['efficiency_category'] for case in negative_cases]
        duration_categories = [case['derived_metrics']['trip_duration_category'] for case in negative_cases]
        print(f"     Most common in: {max(set(efficiency_categories), key=efficiency_categories.count)} efficiency")
        print(f"     Most common duration: {max(set(duration_categories), key=duration_categories.count)}")
    
    # Check for efficiency-based patterns
    efficiency_errors = [(cat, stats['mean_percentage_error']) for cat, stats in efficiency_corr.items() 
                        if isinstance(stats, dict) and stats.get('count', 0) > 0]
    efficiency_errors.sort(key=lambda x: x[1], reverse=True)
    
    if efficiency_errors:
        worst_efficiency = efficiency_errors[0]
        print(f"  📈 Worst efficiency category: {worst_efficiency[0].replace('_', ' ').title()} ({worst_efficiency[1]:.1f}% avg error)")
    
    # Check for duration-based patterns  
    duration_errors = [(cat, stats['mean_percentage_error']) for cat, stats in duration_corr.items() 
                      if isinstance(stats, dict) and stats.get('count', 0) > 0]
    duration_errors.sort(key=lambda x: x[1], reverse=True)
    
    if duration_errors:
        worst_duration = duration_errors[0]
        print(f"  📅 Worst duration category: {worst_duration[0].replace('_', ' ').title()} ({worst_duration[1]:.1f}% avg error)")
    
    print("\n" + "="*70)
    return patterns

if __name__ == "__main__":
    analyze_real_error_patterns() 