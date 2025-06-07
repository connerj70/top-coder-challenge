#!/usr/bin/env python3
"""
Test script for the error analysis framework
"""

from calculate_reimbursement import *

def test_current_model_performance():
    """Test the current model performance using the error analysis framework."""
    print("Loading test cases...")
    test_cases = load_public_test_cases('public_cases.json')
    
    # Test on first 100 cases for quick feedback
    print("Testing on first 100 cases...")
    sample_cases = test_cases[:100]
    
    # Calculate our predictions
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
    
    # Analyze errors
    print("Analyzing errors...")
    result = calculate_error_metrics(calculated, expected)
    
    # Print results
    print("\n" + "="*50)
    print("CURRENT MODEL PERFORMANCE ANALYSIS")
    print("="*50)
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Cases analyzed: {result['summary_stats']['total_cases']}")
    print(f"  Mean Absolute Error: ${result['summary_stats']['mean_absolute_error']:.2f}")
    print(f"  Mean Percentage Error: {result['summary_stats']['mean_percentage_error']:.1f}%")
    print(f"  Median Absolute Error: ${result['summary_stats']['median_absolute_error']:.2f}")
    print(f"  Max Absolute Error: ${result['summary_stats']['max_absolute_error']:.2f}")
    print(f"  Overall Bias: ${result['summary_stats']['overall_bias']:.2f}")
    
    print(f"\n🎯 Accuracy Metrics:")
    print(f"  Exact Matches: {result['accuracy_metrics']['exact_matches']} ({result['accuracy_metrics']['exact_match_rate']:.1f}%)")
    print(f"  Close within $1: {result['accuracy_metrics']['close_1_dollar_count']} ({result['accuracy_metrics']['close_1_dollar_rate']:.1f}%)")
    print(f"  Close within 5%: {result['accuracy_metrics']['close_5_percent_count']} ({result['accuracy_metrics']['close_5_percent_rate']:.1f}%)")
    print(f"  Close within 10%: {result['accuracy_metrics']['close_10_percent_count']} ({result['accuracy_metrics']['close_10_percent_rate']:.1f}%)")
    
    print(f"\n📈 Error Distribution:")
    print(f"  Overestimates: {result['accuracy_metrics']['overestimate_count']} ({result['accuracy_metrics']['overestimate_rate']:.1f}%)")
    print(f"  Underestimates: {result['accuracy_metrics']['underestimate_count']} ({result['accuracy_metrics']['underestimate_rate']:.1f}%)")
    
    # Show some examples of worst errors
    print(f"\n🔍 Worst Error Examples:")
    error_data = result['error_data']
    sorted_errors = sorted(error_data, key=lambda x: x['absolute_percentage_error'], reverse=True)
    
    for i in range(min(5, len(sorted_errors))):
        err = sorted_errors[i]
        idx = err['test_case_index']
        case = sample_cases[idx]
        inputs = case['input']
        
        print(f"  Case {idx}: {inputs['trip_duration_days']} days, {inputs['miles_traveled']} miles, ${inputs['total_receipts_amount']:.2f} receipts")
        print(f"    Expected: ${err['expected']:.2f}, Calculated: ${err['calculated']:.2f}")
        print(f"    Error: ${err['absolute_error']:.2f} ({err['percentage_error']:+.1f}%)")
    
    print("\n" + "="*50)
    return result

if __name__ == "__main__":
    test_current_model_performance() 