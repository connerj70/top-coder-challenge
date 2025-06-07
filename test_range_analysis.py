#!/usr/bin/env python3
"""
Test script for detailed range analysis on real data
"""

from calculate_reimbursement import *

def analyze_error_prone_ranges():
    """Perform detailed range analysis on real test cases."""
    print("Loading test cases...")
    test_cases = load_public_test_cases('public_cases.json')
    
    # Test on first 100 cases for detailed analysis
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
    
    # Perform range analysis
    print("Performing systematic range analysis...")
    range_analysis = identify_error_prone_ranges(error_data, sample_cases, num_bins=8)
    
    # Print comprehensive range analysis
    print("\n" + "="*80)
    print("ERROR-PRONE INPUT RANGE ANALYSIS")
    print("="*80)
    
    # Parameter Range Analysis
    print(f"\n📊 PARAMETER RANGE ANALYSIS:")
    
    for param_name, ranges in range_analysis['parameter_ranges'].items():
        print(f"\n  {param_name.replace('_', ' ').title()}:")
        
        # Sort ranges by error rate
        sorted_ranges = sorted(
            [(range_key, stats) for range_key, stats in ranges.items()],
            key=lambda x: x[1]['mean_percentage_error'],
            reverse=True
        )
        
        for range_key, stats in sorted_ranges[:5]:  # Show top 5 worst ranges
            if stats['count'] >= 2:  # Only show ranges with multiple cases
                print(f"    Range {range_key}: {stats['count']} cases")
                print(f"      Mean % Error: {stats['mean_percentage_error']:.1f}%")
                print(f"      Mean Abs Error: ${stats['mean_absolute_error']:.2f}")
                if stats['negative_value_rate'] > 0:
                    print(f"      🚨 Negative Values: {stats['negative_value_rate']:.1f}%")
                if stats['error_rate_severe'] > 0:
                    print(f"      ⚠️  Severe Errors (>100%): {stats['error_rate_severe']:.1f}%")
    
    # Critical Ranges
    print(f"\n🎯 CRITICAL RANGES (Above-Average Error Scores):")
    
    for param_name, critical_ranges in range_analysis['critical_ranges'].items():
        if critical_ranges:
            print(f"\n  {param_name.replace('_', ' ').title()}:")
            for range_info in critical_ranges:
                range_key = range_info['range_key']
                stats = range_info['stats']
                error_score = range_info['error_score']
                
                print(f"    Range {range_key} (Error Score: {error_score:.1f})")
                print(f"      Cases: {stats['count']}")
                print(f"      Mean % Error: {stats['mean_percentage_error']:.1f}%")
                
                if stats['negative_value_rate'] > 0:
                    print(f"      🚨 Negative Rate: {stats['negative_value_rate']:.1f}%")
                if stats['error_rate_severe'] > 0:
                    print(f"      ⚠️  Severe Error Rate: {stats['error_rate_severe']:.1f}%")
    
    # Range Interactions
    print(f"\n🔗 CRITICAL RANGE INTERACTIONS:")
    
    interactions = range_analysis['range_interactions']
    if interactions:
        # Sort interactions by error severity
        sorted_interactions = sorted(
            interactions.items(),
            key=lambda x: x[1]['mean_percentage_error'],
            reverse=True
        )
        
        for interaction_key, stats in sorted_interactions:
            print(f"\n  {interaction_key}:")
            print(f"    Cases: {stats['count']}")
            print(f"    Mean % Error: {stats['mean_percentage_error']:.1f}%")
            print(f"    Mean Abs Error: ${stats['mean_absolute_error']:.2f}")
            
            if stats.get('negative_value_rate', 0) > 0:
                print(f"    🚨 Negative Rate: {stats['negative_value_rate']:.1f}%")
            if stats.get('severe_error_rate', 0) > 0:
                print(f"    ⚠️  Severe Error Rate: {stats['severe_error_rate']:.1f}%")
    else:
        print("  No significant range interactions found")
    
    # Recommendations
    print(f"\n💡 SPECIFIC RECOMMENDATIONS:")
    
    recommendations = range_analysis['recommendations']
    if recommendations:
        for i, rec in enumerate(recommendations[:10], 1):  # Show top 10 recommendations
            priority_icon = "🚨" if rec['priority'] == 'high' else "⚠️"
            print(f"\n  {i}. {priority_icon} {rec['recommendation']}")
            print(f"     Type: {rec['type'].replace('_', ' ').title()}")
            print(f"     Mean % Error: {rec['error_stats']['mean_pct_error']:.1f}%")
            
            if rec['error_stats'].get('negative_rate', 0) > 0:
                print(f"     Negative Value Rate: {rec['error_stats']['negative_rate']:.1f}%")
    else:
        print("  No specific recommendations generated")
    
    # Detailed Analysis of Most Critical Ranges
    print(f"\n🔍 DETAILED ANALYSIS OF MOST CRITICAL CASES:")
    
    # Find the most problematic individual cases
    worst_cases = sorted(error_data, key=lambda x: abs(x['percentage_error']), reverse=True)[:5]
    
    for i, case in enumerate(worst_cases, 1):
        idx = case['test_case_index']
        inputs = sample_cases[idx]['input']
        
        duration = inputs['trip_duration_days']
        miles = inputs['miles_traveled']
        receipts = inputs['total_receipts_amount']
        miles_per_day = miles / duration if duration > 0 else 0
        receipts_per_day = receipts / duration if duration > 0 else 0
        
        print(f"\n  Case {i} (Index {idx}):")
        print(f"    Inputs: {duration} days, {miles} miles, ${receipts:.2f} receipts")
        print(f"    Derived: {miles_per_day:.1f} mi/day, ${receipts_per_day:.2f}/day")
        print(f"    Expected: ${case['expected']:.2f}")
        print(f"    Calculated: ${case['calculated']:.2f}")
        print(f"    Error: {case['percentage_error']:+.1f}% (${case['absolute_error']:+.2f})")
        
        # Identify which critical ranges this case falls into
        critical_memberships = []
        for param_name, critical_ranges in range_analysis['critical_ranges'].items():
            param_values = {
                'trip_duration_days': duration,
                'miles_traveled': miles,
                'total_receipts_amount': receipts,
                'miles_per_day': miles_per_day,
                'receipts_per_day': receipts_per_day
            }
            
            if param_name in param_values:
                value = param_values[param_name]
                for range_info in critical_ranges:
                    range_start, range_end = range_info['stats']['range']
                    if range_start <= value <= range_end:
                        critical_memberships.append(f"{param_name}:{range_info['range_key']}")
        
        if critical_memberships:
            print(f"    Critical Ranges: {', '.join(critical_memberships)}")
    
    # Summary Insights
    print(f"\n📋 SUMMARY INSIGHTS:")
    
    # Count total critical ranges
    total_critical_ranges = sum(len(ranges) for ranges in range_analysis['critical_ranges'].values())
    total_interactions = len(range_analysis['range_interactions'])
    high_priority_recs = sum(1 for rec in recommendations if rec['priority'] == 'high')
    
    print(f"  • Total critical ranges identified: {total_critical_ranges}")
    print(f"  • Critical range interactions: {total_interactions}")
    print(f"  • High priority recommendations: {high_priority_recs}")
    
    # Identify most problematic parameter
    param_criticality = {}
    for param_name, ranges in range_analysis['critical_ranges'].items():
        if ranges:
            avg_error_score = sum(r['error_score'] for r in ranges) / len(ranges)
            param_criticality[param_name] = (len(ranges), avg_error_score)
    
    if param_criticality:
        most_critical_param = max(param_criticality.items(), key=lambda x: x[1][1])
        print(f"  • Most problematic parameter: {most_critical_param[0].replace('_', ' ').title()}")
        print(f"    ({most_critical_param[1][0]} critical ranges, avg score: {most_critical_param[1][1]:.1f})")
    
    print("\n" + "="*80)
    return range_analysis

if __name__ == "__main__":
    analyze_error_prone_ranges() 