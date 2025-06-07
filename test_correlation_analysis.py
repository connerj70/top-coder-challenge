#!/usr/bin/env python3
"""
Test script for comprehensive correlation analysis on real data
"""

from calculate_reimbursement import *

def analyze_input_feature_correlations():
    """Perform comprehensive correlation analysis on real test cases."""
    print("Loading test cases...")
    test_cases = load_public_test_cases('public_cases.json')
    
    # Test on first 100 cases for detailed correlation analysis
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
    
    # Perform correlation analysis
    print("Performing comprehensive correlation analysis...")
    correlation_analysis = correlate_input_features_with_errors(error_data, sample_cases)
    
    # Print comprehensive correlation analysis
    print("\n" + "="*80)
    print("INPUT FEATURE CORRELATION ANALYSIS")
    print("="*80)
    
    # Top Correlations
    print(f"\n📊 STRONGEST FEATURE-ERROR CORRELATIONS:")
    
    ranked_correlations = correlation_analysis['feature_correlations']['ranked_correlations']
    
    for i, corr in enumerate(ranked_correlations[:15], 1):  # Top 15 correlations
        strength_icon = "🔴" if corr['strength'] == 'strong' else "🟡" if corr['strength'] == 'moderate' else "🟢"
        direction = "+" if corr['correlation'] > 0 else "-"
        
        print(f"  {i:2d}. {strength_icon} {corr['feature'].replace('_', ' ').title()} → {corr['error_metric'].replace('_', ' ').title()}")
        print(f"      Correlation: {direction}{corr['abs_correlation']:.3f} ({corr['strength']})")
        
        # Add interpretation
        if corr['error_metric'] == 'is_negative' and corr['abs_correlation'] > 0.3:
            print(f"      🚨 Strong predictor of negative reimbursement values")
        elif corr['error_metric'] == 'percentage_error' and corr['abs_correlation'] > 0.5:
            print(f"      ⚠️  Major contributor to calculation errors")
    
    # Feature Interactions
    print(f"\n🔗 FEATURE INTERACTION ANALYSIS:")
    
    interactions = correlation_analysis['interaction_analysis']
    
    # Analyze numeric feature interactions
    interaction_pairs = [
        ('trip_duration_days_x_miles_per_day', 'Duration × Efficiency'),
        ('miles_per_day_x_receipts_per_day', 'Efficiency × Spending'),
        ('trip_duration_days_x_receipts_per_day', 'Duration × Spending'),
        ('efficiency_ratio_x_spending_intensity', 'Efficiency Ratio × Spending Intensity')
    ]
    
    for interaction_key, friendly_name in interaction_pairs:
        if interaction_key in interactions:
            interaction_data = interactions[interaction_key]
            print(f"\n  {friendly_name}:")
            
            # Sort regions by error severity
            sorted_regions = sorted(
                [(region, stats) for region, stats in interaction_data.items()],
                key=lambda x: x[1]['mean_error'],
                reverse=True
            )
            
            for region, stats in sorted_regions[:3]:  # Top 3 worst regions
                if stats['count'] >= 2:
                    print(f"    {region.replace('_', ' ').title()}: {stats['count']} cases")
                    print(f"      Mean Error: {stats['mean_error']:.1f}%")
                    if stats['negative_rate'] > 0:
                        print(f"      🚨 Negative Rate: {stats['negative_rate']:.1f}%")
    
    # Categorical Trip Type Analysis
    print(f"\n📋 TRIP TYPE ERROR PATTERNS:")
    
    trip_type_patterns = [(k, v) for k, v in interactions.items() if k.startswith('trip_type_')]
    trip_type_patterns.sort(key=lambda x: x[1]['mean_error'], reverse=True)
    
    for trip_type_key, stats in trip_type_patterns[:10]:  # Top 10 worst trip types
        trip_type = trip_type_key.replace('trip_type_', '').replace('_', ' + ').title()
        print(f"  {trip_type}: {stats['count']} cases")
        print(f"    Mean Error: {stats['mean_error']:.1f}%")
        if stats['negative_rate'] > 0:
            print(f"    🚨 Negative Rate: {stats['negative_rate']:.1f}%")
        print(f"    Error Variance: {stats['error_variance']:.1f}")
    
    # Root Cause Analysis
    print(f"\n🔍 ROOT CAUSE ANALYSIS:")
    
    root_causes = correlation_analysis['root_cause_analysis']
    
    # Primary Error Drivers
    print(f"\n  Primary Error Drivers:")
    primary_drivers = root_causes['primary_drivers']
    
    for driver in primary_drivers:
        feature = driver['feature']
        strength = driver['total_correlation_strength']
        is_primary = driver['primary_error_driver']
        
        status_icon = "🎯" if is_primary else "📊"
        print(f"    {status_icon} {feature.replace('_', ' ').title()}: {strength:.3f} total correlation")
        
        # Show specific correlations
        for error_type, corr in driver['correlations'].items():
            if abs(corr) > 0.2:  # Only show significant correlations
                print(f"      → {error_type.replace('_', ' ').title()}: {corr:+.3f}")
    
    # Negative Value Analysis
    if root_causes['negative_value_causes']:
        print(f"\n  🚨 Negative Value Root Causes:")
        negative_causes = root_causes['negative_value_causes']
        
        print(f"    Common Characteristics:")
        common_chars = negative_causes['common_characteristics']
        print(f"      Most Common Duration: {common_chars['most_common_duration_category'].replace('_', ' ').title()}")
        print(f"      Most Common Efficiency: {common_chars['most_common_efficiency_category'].replace('_', ' ').title()}")
        print(f"      Avg Miles/Day: {common_chars['avg_miles_per_day']:.1f}")
        
        print(f"    Feature Ranges:")
        for feature, stats in negative_causes.items():
            if isinstance(stats, dict) and 'mean' in stats:
                print(f"      {feature.replace('_', ' ').title()}: {stats['common_range']}")
    
    # Severe Error Analysis
    if root_causes['severe_error_causes']:
        print(f"\n  ⚠️  Severe Error Patterns:")
        severe_causes = root_causes['severe_error_causes']
        
        for pattern_type, characteristics_key in [
            ('extreme_overestimates', 'extreme_overestimates_characteristics'),
            ('extreme_underestimates', 'extreme_underestimates_characteristics'),
            ('moderate_severe', 'moderate_severe_characteristics')
        ]:
            if characteristics_key in severe_causes:
                chars = severe_causes[characteristics_key]
                print(f"    {pattern_type.replace('_', ' ').title()}: {chars['count']} cases")
                print(f"      Avg Miles/Day: {chars['avg_miles_per_day']:.1f}")
                print(f"      Avg Receipts/Day: ${chars['avg_receipts_per_day']:.2f}")
                print(f"      Common Trip Type: {chars['common_trip_type'].replace('_', ' ').title()}")
    
    # Systematic Biases
    if root_causes['systematic_biases']:
        print(f"\n  ⚖️  Systematic Biases by Duration:")
        biases = root_causes['systematic_biases']
        
        for duration_range, bias_data in biases.items():
            range_name = duration_range.replace('duration_', '').replace('_days', '').replace('_', '-')
            bias_direction = bias_data['bias_direction']
            bias_icon = "📈" if bias_direction == 'overestimate' else "📉" if bias_direction == 'underestimate' else "⚖️"
            
            print(f"    {bias_icon} {range_name} days: {bias_direction.title()}")
            print(f"      Overestimate Rate: {bias_data['overestimate_rate']:.1f}%")
            print(f"      Avg Error: {bias_data['avg_signed_error']:+.1f}%")
    
    # Threshold Analysis
    print(f"\n🎯 THRESHOLD EFFECT ANALYSIS:")
    
    threshold_analysis = correlation_analysis['threshold_analysis']
    
    for feature_name, thresholds in threshold_analysis.items():
        print(f"\n  {feature_name.replace('_', ' ').title()}:")
        
        # Find the most significant threshold effects
        significant_thresholds = []
        
        for threshold_key, threshold_data in thresholds.items():
            if 'threshold_effect' in threshold_data:
                effect = threshold_data['threshold_effect']
                error_change = abs(effect['error_change'])
                negative_change = abs(effect['negative_rate_change'])
                
                if error_change > 10 or negative_change > 5:  # Significant thresholds
                    threshold_value = threshold_key.replace('threshold_', '')
                    significant_thresholds.append((threshold_value, effect, threshold_data))
        
        # Sort by significance
        significant_thresholds.sort(key=lambda x: abs(x[1]['error_change']), reverse=True)
        
        for threshold_value, effect, data in significant_thresholds[:3]:  # Top 3 significant thresholds
            print(f"    Threshold {threshold_value}:")
            print(f"      Below: {data['below_threshold']['count']} cases, {data['below_threshold']['mean_error']:.1f}% error")
            print(f"      Above: {data['above_threshold']['count']} cases, {data['above_threshold']['mean_error']:.1f}% error")
            print(f"      Effect: {effect['error_change']:+.1f}% error change")
            
            if abs(effect['negative_rate_change']) > 1:
                print(f"      🚨 Negative Rate Change: {effect['negative_rate_change']:+.1f}%")
    
    # Summary Insights
    print(f"\n📋 KEY CORRELATION INSIGHTS:")
    
    # Identify strongest predictors
    strongest_predictors = [corr for corr in ranked_correlations[:5] if corr['abs_correlation'] > 0.4]
    
    if strongest_predictors:
        print(f"  • Strongest Error Predictors:")
        for corr in strongest_predictors:
            feature = corr['feature'].replace('_', ' ').title()
            error_type = corr['error_metric'].replace('_', ' ').title()
            print(f"    - {feature} → {error_type} ({corr['abs_correlation']:.3f})")
    
    # Identify critical thresholds
    critical_thresholds = []
    for feature_name, thresholds in threshold_analysis.items():
        for threshold_key, threshold_data in thresholds.items():
            if 'threshold_effect' in threshold_data:
                effect = threshold_data['threshold_effect']
                if abs(effect['negative_rate_change']) > 10:  # Major negative rate changes
                    threshold_value = threshold_key.replace('threshold_', '')
                    critical_thresholds.append((feature_name, threshold_value, effect['negative_rate_change']))
    
    if critical_thresholds:
        print(f"  • Critical Thresholds (Negative Value Risk):")
        for feature, threshold, change in critical_thresholds:
            print(f"    - {feature.replace('_', ' ').title()} @ {threshold}: {change:+.1f}% negative rate change")
    
    # Identify problematic interactions
    high_risk_interactions = []
    for interaction_key, interaction_data in interactions.items():
        if interaction_key.startswith('trip_type_'):
            if interaction_data.get('negative_rate', 0) > 20:  # High negative rate
                trip_type = interaction_key.replace('trip_type_', '').replace('_', ' + ')
                high_risk_interactions.append((trip_type, interaction_data['negative_rate']))
    
    if high_risk_interactions:
        print(f"  • High-Risk Trip Type Combinations:")
        high_risk_interactions.sort(key=lambda x: x[1], reverse=True)
        for trip_type, negative_rate in high_risk_interactions[:3]:
            print(f"    - {trip_type.title()}: {negative_rate:.1f}% negative rate")
    
    print("\n" + "="*80)
    return correlation_analysis

if __name__ == "__main__":
    analyze_input_feature_correlations() 