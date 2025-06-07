#!/usr/bin/env python3
"""
Reimbursement Calculation Script
This script calculates reimbursement amounts based on trip duration, miles traveled, and receipt amounts.
"""

import sys
import argparse
import json
import os

def validate_inputs(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Validate input parameters to ensure they are valid for reimbursement calculation.
    
    Args:
        trip_duration_days (float): Number of days for the trip
        miles_traveled (float): Total miles traveled
        total_receipts_amount (float): Total amount from receipts
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if trip_duration_days < 0:
        return False, "Trip duration cannot be negative"
    
    if miles_traveled < 0:
        return False, "Miles traveled cannot be negative"
    
    if total_receipts_amount < 0:
        return False, "Total receipts amount cannot be negative"
    
    return True, ""

def load_public_test_cases(file_path="public_cases.json"):
    """
    Load and parse the public test cases from JSON file.
    
    Args:
        file_path (str): Path to the public test cases JSON file
        
    Returns:
        list: List of test case dictionaries with 'input' and 'expected_output' keys
        
    Raises:
        FileNotFoundError: If the test cases file doesn't exist
        json.JSONDecodeError: If the JSON file is malformed
        ValueError: If the test cases don't have the expected structure
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test cases file not found: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            test_cases = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Malformed JSON in {file_path}: {str(e)}", e.doc, e.pos)
    
    # Validate the structure of test cases
    if not isinstance(test_cases, list):
        raise ValueError("Test cases must be a list")
    
    for i, case in enumerate(test_cases):
        if not isinstance(case, dict):
            raise ValueError(f"Test case {i} must be a dictionary")
        
        if 'input' not in case or 'expected_output' not in case:
            raise ValueError(f"Test case {i} must have 'input' and 'expected_output' keys")
        
        input_data = case['input']
        required_fields = ['trip_duration_days', 'miles_traveled', 'total_receipts_amount']
        
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Test case {i} input missing required field: {field}")
            
            if not isinstance(input_data[field], (int, float)):
                raise ValueError(f"Test case {i} field {field} must be numeric")
    
    return test_cases

def extract_test_case_data(test_cases):
    """
    Extract input parameters and expected outputs from test cases.
    
    Args:
        test_cases (list): List of test case dictionaries
        
    Returns:
        dict: Dictionary with separate lists for each parameter and expected outputs
    """
    extracted_data = {
        'trip_duration_days': [],
        'miles_traveled': [],
        'total_receipts_amount': [],
        'expected_outputs': []
    }
    
    for case in test_cases:
        input_data = case['input']
        extracted_data['trip_duration_days'].append(input_data['trip_duration_days'])
        extracted_data['miles_traveled'].append(input_data['miles_traveled'])
        extracted_data['total_receipts_amount'].append(input_data['total_receipts_amount'])
        extracted_data['expected_outputs'].append(case['expected_output'])
    
    return extracted_data

def calculate_dataset_statistics(extracted_data):
    """
    Calculate basic statistics for the dataset parameters.
    
    Args:
        extracted_data (dict): Dictionary with parameter lists
        
    Returns:
        dict: Dictionary with statistics for each parameter
    """
    statistics = {}
    
    for param in ['trip_duration_days', 'miles_traveled', 'total_receipts_amount', 'expected_outputs']:
        values = extracted_data[param]
        if values:
            statistics[param] = {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'average': sum(values) / len(values),
                'sum': sum(values)
            }
        else:
            statistics[param] = {
                'count': 0,
                'min': None,
                'max': None,
                'average': None,
                'sum': 0
            }
    
    return statistics

def load_and_analyze_public_cases(file_path="public_cases.json"):
    """
    Load public test cases and return both the data and basic statistics.
    
    Args:
        file_path (str): Path to the public test cases JSON file
        
    Returns:
        tuple: (test_cases, extracted_data, statistics)
    """
    test_cases = load_public_test_cases(file_path)
    extracted_data = extract_test_case_data(test_cases)
    statistics = calculate_dataset_statistics(extracted_data)
    
    return test_cases, extracted_data, statistics

def analyze_trip_length_patterns(extracted_data):
    """
    Analyze patterns related to trip length, focusing on the reported 5-day sweet spot.
    
    Args:
        extracted_data (dict): Dictionary with parameter lists
        
    Returns:
        dict: Analysis results for trip length patterns
    """
    trip_durations = extracted_data['trip_duration_days']
    reimbursements = extracted_data['expected_outputs']
    
    # Group by trip duration and calculate statistics
    duration_groups = {}
    for i, duration in enumerate(trip_durations):
        if duration not in duration_groups:
            duration_groups[duration] = []
        duration_groups[duration].append(reimbursements[i])
    
    # Calculate average reimbursement per day for each duration
    duration_analysis = {}
    for duration, amounts in duration_groups.items():
        avg_amount = sum(amounts) / len(amounts)
        duration_analysis[duration] = {
            'count': len(amounts),
            'avg_total_reimbursement': avg_amount,
            'avg_per_day': avg_amount / duration if duration > 0 else 0,
            'min': min(amounts),
            'max': max(amounts)
        }
    
    # Look for the 5-day sweet spot and other patterns
    sweet_spot_analysis = {}
    if 5.0 in duration_analysis:
        five_day_avg = duration_analysis[5.0]['avg_per_day']
        for duration, data in duration_analysis.items():
            if duration != 5.0:
                comparison = data['avg_per_day'] / five_day_avg if five_day_avg > 0 else 0
                sweet_spot_analysis[duration] = {
                    'vs_5_day_ratio': comparison,
                    'avg_per_day': data['avg_per_day']
                }
    
    return {
        'duration_groups': duration_analysis,
        'sweet_spot_analysis': sweet_spot_analysis,
        'total_unique_durations': len(duration_groups)
    }

def analyze_mileage_efficiency(extracted_data):
    """
    Analyze mileage efficiency patterns, focusing on miles per day ratios.
    
    Args:
        extracted_data (dict): Dictionary with parameter lists
        
    Returns:
        dict: Analysis results for mileage efficiency patterns
    """
    trip_durations = extracted_data['trip_duration_days']
    miles_traveled = extracted_data['miles_traveled']
    reimbursements = extracted_data['expected_outputs']
    
    # Calculate miles per day for each trip
    efficiency_data = []
    for i in range(len(trip_durations)):
        duration = trip_durations[i]
        miles = miles_traveled[i]
        reimbursement = reimbursements[i]
        
        miles_per_day = miles / duration if duration > 0 else 0
        efficiency_data.append({
            'miles_per_day': miles_per_day,
            'total_miles': miles,
            'duration': duration,
            'reimbursement': reimbursement,
            'reimbursement_per_mile': reimbursement / miles if miles > 0 else 0
        })
    
    # Group by efficiency ranges to find the 180-220 sweet spot
    efficiency_ranges = {
        'very_low': (0, 50),
        'low': (50, 100),
        'medium_low': (100, 150),
        'medium': (150, 180),
        'sweet_spot': (180, 220),
        'medium_high': (220, 300),
        'high': (300, 400),
        'very_high': (400, float('inf'))
    }
    
    range_analysis = {}
    for range_name, (min_val, max_val) in efficiency_ranges.items():
        matching_trips = [
            trip for trip in efficiency_data 
            if min_val <= trip['miles_per_day'] < max_val
        ]
        
        if matching_trips:
            reimbursements_in_range = [trip['reimbursement'] for trip in matching_trips]
            per_mile_rates = [trip['reimbursement_per_mile'] for trip in matching_trips if trip['reimbursement_per_mile'] > 0]
            
            range_analysis[range_name] = {
                'count': len(matching_trips),
                'avg_reimbursement': sum(reimbursements_in_range) / len(reimbursements_in_range),
                'avg_per_mile_rate': sum(per_mile_rates) / len(per_mile_rates) if per_mile_rates else 0,
                'range': (min_val, max_val)
            }
        else:
            range_analysis[range_name] = {
                'count': 0,
                'avg_reimbursement': 0,
                'avg_per_mile_rate': 0,
                'range': (min_val, max_val)
            }
    
    return {
        'efficiency_ranges': range_analysis,
        'raw_efficiency_data': efficiency_data
    }

def analyze_receipt_patterns(extracted_data):
    """
    Analyze receipt amount patterns and optimal ranges by trip length.
    
    Args:
        extracted_data (dict): Dictionary with parameter lists
        
    Returns:
        dict: Analysis results for receipt patterns
    """
    trip_durations = extracted_data['trip_duration_days']
    receipts = extracted_data['total_receipts_amount']
    reimbursements = extracted_data['expected_outputs']
    
    # Calculate receipts per day
    receipt_analysis = []
    for i in range(len(trip_durations)):
        duration = trip_durations[i]
        receipt_amount = receipts[i]
        reimbursement = reimbursements[i]
        
        receipts_per_day = receipt_amount / duration if duration > 0 else 0
        receipt_analysis.append({
            'receipts_per_day': receipts_per_day,
            'total_receipts': receipt_amount,
            'duration': duration,
            'reimbursement': reimbursement,
            'receipt_to_reimbursement_ratio': reimbursement / receipt_amount if receipt_amount > 0 else float('inf')
        })
    
    # Analyze by trip length categories
    trip_length_categories = {
        'short': (0, 3),
        'medium': (3, 6),
        'long': (6, float('inf'))
    }
    
    category_analysis = {}
    for category, (min_days, max_days) in trip_length_categories.items():
        matching_trips = [
            trip for trip in receipt_analysis 
            if min_days <= trip['duration'] < max_days
        ]
        
        if matching_trips:
            # Group by receipt per day ranges within each category
            receipt_ranges = {
                'very_low': (0, 50),
                'low': (50, 75),
                'optimal_short': (75, 120),
                'medium': (120, 150),
                'high': (150, 200),
                'very_high': (200, float('inf'))
            }
            
            range_data = {}
            for range_name, (min_receipt, max_receipt) in receipt_ranges.items():
                trips_in_range = [
                    trip for trip in matching_trips 
                    if min_receipt <= trip['receipts_per_day'] < max_receipt
                ]
                
                if trips_in_range:
                    ratios = [trip['receipt_to_reimbursement_ratio'] for trip in trips_in_range if trip['receipt_to_reimbursement_ratio'] != float('inf')]
                    range_data[range_name] = {
                        'count': len(trips_in_range),
                        'avg_ratio': sum(ratios) / len(ratios) if ratios else 0,
                        'avg_reimbursement': sum(trip['reimbursement'] for trip in trips_in_range) / len(trips_in_range)
                    }
                else:
                    range_data[range_name] = {'count': 0, 'avg_ratio': 0, 'avg_reimbursement': 0}
            
            category_analysis[category] = range_data
    
    return {
        'by_trip_category': category_analysis,
        'raw_receipt_data': receipt_analysis
    }

def calculate_correlations(extracted_data):
    """
    Calculate correlations between input parameters and output reimbursement amounts.
    
    Args:
        extracted_data (dict): Dictionary with parameter lists
        
    Returns:
        dict: Correlation analysis results
    """
    import math
    
    def pearson_correlation(x, y):
        """Calculate Pearson correlation coefficient"""
        n = len(x)
        if n == 0:
            return 0
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] * x[i] for i in range(n))
        sum_y2 = sum(y[i] * y[i] for i in range(n))
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    trip_durations = extracted_data['trip_duration_days']
    miles_traveled = extracted_data['miles_traveled']
    receipts = extracted_data['total_receipts_amount']
    reimbursements = extracted_data['expected_outputs']
    
    # Calculate derived variables
    miles_per_day = [miles_traveled[i] / trip_durations[i] if trip_durations[i] > 0 else 0 for i in range(len(trip_durations))]
    receipts_per_day = [receipts[i] / trip_durations[i] if trip_durations[i] > 0 else 0 for i in range(len(trip_durations))]
    
    correlations = {
        'trip_duration_vs_reimbursement': pearson_correlation(trip_durations, reimbursements),
        'miles_vs_reimbursement': pearson_correlation(miles_traveled, reimbursements),
        'receipts_vs_reimbursement': pearson_correlation(receipts, reimbursements),
        'miles_per_day_vs_reimbursement': pearson_correlation(miles_per_day, reimbursements),
        'receipts_per_day_vs_reimbursement': pearson_correlation(receipts_per_day, reimbursements)
    }
    
    return correlations

def identify_calculation_patterns(extracted_data):
    """
    Identify potential calculation patterns and thresholds in the reimbursement system.
    
    Args:
        extracted_data (dict): Dictionary with parameter lists
        
    Returns:
        dict: Pattern analysis results
    """
    trip_durations = extracted_data['trip_duration_days']
    miles_traveled = extracted_data['miles_traveled']
    receipts = extracted_data['total_receipts_amount']
    reimbursements = extracted_data['expected_outputs']
    
    # Look for linear relationships
    linear_patterns = {}
    
    # Check for base per diem pattern ($100/day mentioned in interviews)
    per_day_rates = [reimbursements[i] / trip_durations[i] if trip_durations[i] > 0 else 0 for i in range(len(trip_durations))]
    
    # Group similar trips to identify patterns
    similar_trip_groups = {}
    for i in range(len(trip_durations)):
        duration = trip_durations[i]
        miles = miles_traveled[i]
        receipt = receipts[i]
        reimbursement = reimbursements[i]
        
        # Create a key for grouping similar trips (rounded values)
        key = (round(duration), round(miles/50)*50, round(receipt/25)*25)
        
        if key not in similar_trip_groups:
            similar_trip_groups[key] = []
        
        similar_trip_groups[key].append({
            'duration': duration,
            'miles': miles,
            'receipts': receipt,
            'reimbursement': reimbursement
        })
    
    # Find groups with multiple similar trips to check for consistency
    consistent_groups = {}
    inconsistent_groups = {}
    
    for key, trips in similar_trip_groups.items():
        if len(trips) > 1:
            reimbursements_in_group = [trip['reimbursement'] for trip in trips]
            max_diff = max(reimbursements_in_group) - min(reimbursements_in_group)
            avg_reimbursement = sum(reimbursements_in_group) / len(reimbursements_in_group)
            
            # Consider consistent if variance is less than 5% of average
            if max_diff / avg_reimbursement < 0.05:
                consistent_groups[key] = {
                    'trips': trips,
                    'avg_reimbursement': avg_reimbursement,
                    'variance': max_diff
                }
            else:
                inconsistent_groups[key] = {
                    'trips': trips,
                    'avg_reimbursement': avg_reimbursement,
                    'variance': max_diff,
                    'variance_percent': (max_diff / avg_reimbursement) * 100
                }
    
    return {
        'per_day_rates': per_day_rates,
        'consistent_groups': consistent_groups,
        'inconsistent_groups': inconsistent_groups,
        'total_similar_groups': len(similar_trip_groups)
    }

def perform_comprehensive_analysis(file_path="public_cases.json"):
    """
    Perform comprehensive analysis of public test cases to identify patterns and potential rules.
    
    Args:
        file_path (str): Path to the public test cases JSON file
        
    Returns:
        dict: Complete analysis results
    """
    print("Loading and parsing public test cases...")
    test_cases, extracted_data, basic_stats = load_and_analyze_public_cases(file_path)
    
    print(f"Analyzing {len(test_cases)} test cases...")
    
    # Perform all analyses
    print("1. Analyzing trip length patterns...")
    trip_length_analysis = analyze_trip_length_patterns(extracted_data)
    
    print("2. Analyzing mileage efficiency patterns...")
    mileage_analysis = analyze_mileage_efficiency(extracted_data)
    
    print("3. Analyzing receipt patterns...")
    receipt_analysis = analyze_receipt_patterns(extracted_data)
    
    print("4. Calculating correlations...")
    correlations = calculate_correlations(extracted_data)
    
    print("5. Identifying calculation patterns...")
    calculation_patterns = identify_calculation_patterns(extracted_data)
    
    return {
        'basic_statistics': basic_stats,
        'trip_length_analysis': trip_length_analysis,
        'mileage_analysis': mileage_analysis,
        'receipt_analysis': receipt_analysis,
        'correlations': correlations,
        'calculation_patterns': calculation_patterns,
        'total_cases_analyzed': len(test_cases)
    }

# ============================================================================
# ERROR ANALYSIS FRAMEWORK
# ============================================================================

def calculate_error_metrics(calculated_values, expected_values):
    """
    Compare calculated reimbursement values with expected values and compute error metrics.
    
    This function forms the core of the error analysis framework, providing detailed
    error measurements for each test case to guide refinement of calculation logic.
    
    Args:
        calculated_values (list): List of calculated reimbursement amounts
        expected_values (list): List of expected reimbursement amounts from test cases
        
    Returns:
        dict: Dictionary containing comprehensive error metrics including:
            - error_data: List of error information for each test case
            - summary_stats: Overall error statistics
            - accuracy_metrics: Accuracy measurements at different tolerance levels
    
    Raises:
        ValueError: If input lists have different lengths or contain invalid values
    """
    if len(calculated_values) != len(expected_values):
        raise ValueError(f"Input lists must have same length: got {len(calculated_values)} calculated vs {len(expected_values)} expected")
    
    if not calculated_values or not expected_values:
        raise ValueError("Input lists cannot be empty")
    
    # Validate inputs
    for i, (calc, exp) in enumerate(zip(calculated_values, expected_values)):
        if not isinstance(calc, (int, float)) or not isinstance(exp, (int, float)):
            raise ValueError(f"All values must be numeric. Invalid values at index {i}: calculated={calc}, expected={exp}")
        if exp == 0:
            raise ValueError(f"Expected value at index {i} cannot be zero (would cause division by zero in percentage error)")
    
    error_data = []
    absolute_errors = []
    percentage_errors = []
    
    # Calculate errors for each test case
    for i, (calculated, expected) in enumerate(zip(calculated_values, expected_values)):
        # Absolute error (calculated - expected)
        absolute_error = calculated - expected
        
        # Percentage error ((calculated - expected) / expected * 100)
        percentage_error = (absolute_error / expected) * 100
        
        # Additional metrics
        absolute_percentage_error = abs(percentage_error)
        is_overestimate = calculated > expected
        is_underestimate = calculated < expected
        is_exact_match = calculated == expected
        
        # Tolerance-based accuracy checks
        is_close_1_dollar = abs(absolute_error) <= 1.0
        is_close_5_percent = abs(percentage_error) <= 5.0
        is_close_10_percent = abs(percentage_error) <= 10.0
        
        error_info = {
            'test_case_index': i,
            'calculated': calculated,
            'expected': expected,
            'absolute_error': absolute_error,
            'percentage_error': percentage_error,
            'absolute_percentage_error': absolute_percentage_error,
            'is_overestimate': is_overestimate,
            'is_underestimate': is_underestimate,
            'is_exact_match': is_exact_match,
            'is_close_1_dollar': is_close_1_dollar,
            'is_close_5_percent': is_close_5_percent,
            'is_close_10_percent': is_close_10_percent
        }
        
        error_data.append(error_info)
        absolute_errors.append(abs(absolute_error))
        percentage_errors.append(absolute_percentage_error)
    
    # Calculate summary statistics
    n_cases = len(error_data)
    
    summary_stats = {
        'total_cases': n_cases,
        'mean_absolute_error': sum(absolute_errors) / n_cases,
        'mean_percentage_error': sum(percentage_errors) / n_cases,
        'median_absolute_error': sorted(absolute_errors)[n_cases // 2],
        'median_percentage_error': sorted(percentage_errors)[n_cases // 2],
        'max_absolute_error': max(absolute_errors),
        'max_percentage_error': max(percentage_errors),
        'min_absolute_error': min(absolute_errors),
        'min_percentage_error': min(percentage_errors),
        'std_absolute_error': (sum((x - sum(absolute_errors)/n_cases)**2 for x in absolute_errors) / n_cases)**0.5,
        'total_absolute_error': sum(abs(err['absolute_error']) for err in error_data),
        'sum_calculated': sum(calculated_values),
        'sum_expected': sum(expected_values),
        'overall_bias': sum(calc - exp for calc, exp in zip(calculated_values, expected_values))
    }
    
    # Calculate accuracy metrics at different tolerance levels
    exact_matches = sum(1 for err in error_data if err['is_exact_match'])
    close_1_dollar = sum(1 for err in error_data if err['is_close_1_dollar'])
    close_5_percent = sum(1 for err in error_data if err['is_close_5_percent'])
    close_10_percent = sum(1 for err in error_data if err['is_close_10_percent'])
    overestimates = sum(1 for err in error_data if err['is_overestimate'])
    underestimates = sum(1 for err in error_data if err['is_underestimate'])
    
    accuracy_metrics = {
        'exact_matches': exact_matches,
        'exact_match_rate': exact_matches / n_cases * 100,
        'close_1_dollar_count': close_1_dollar,
        'close_1_dollar_rate': close_1_dollar / n_cases * 100,
        'close_5_percent_count': close_5_percent,
        'close_5_percent_rate': close_5_percent / n_cases * 100,
        'close_10_percent_count': close_10_percent,
        'close_10_percent_rate': close_10_percent / n_cases * 100,
        'overestimate_count': overestimates,
        'overestimate_rate': overestimates / n_cases * 100,
        'underestimate_count': underestimates,
        'underestimate_rate': underestimates / n_cases * 100
    }
    
    return {
        'error_data': error_data,
        'summary_stats': summary_stats,
        'accuracy_metrics': accuracy_metrics
    }

def test_error_calculation_with_synthetic_data():
    """
    Test the error calculation function with known synthetic data to verify correctness.
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("Testing error calculation function with synthetic data...")
    
    # Test case 1: Perfect predictions
    try:
        calculated = [100.0, 200.0, 300.0]
        expected = [100.0, 200.0, 300.0]
        result = calculate_error_metrics(calculated, expected)
        
        assert result['summary_stats']['mean_absolute_error'] == 0.0
        assert result['summary_stats']['mean_percentage_error'] == 0.0
        assert result['accuracy_metrics']['exact_match_rate'] == 100.0
        print("✅ Test 1 passed: Perfect predictions")
        
    except AssertionError:
        print("❌ Test 1 failed: Perfect predictions")
        return False
    
    # Test case 2: Known errors
    try:
        calculated = [110.0, 180.0, 330.0]  # +10, -20, +30
        expected = [100.0, 200.0, 300.0]
        result = calculate_error_metrics(calculated, expected)
        
        # Check absolute errors: |10| + |20| + |30| = 60, mean = 20
        expected_mean_abs_error = 20.0
        assert abs(result['summary_stats']['mean_absolute_error'] - expected_mean_abs_error) < 0.001
        
        # Check percentage errors: |10%| + |10%| + |10%| = 30, mean = 10
        expected_mean_pct_error = 10.0
        assert abs(result['summary_stats']['mean_percentage_error'] - expected_mean_pct_error) < 0.001
        
        # Check bias: +10 - 20 + 30 = +20
        assert result['summary_stats']['overall_bias'] == 20.0
        
        print("✅ Test 2 passed: Known errors")
        
    except AssertionError as e:
        print(f"❌ Test 2 failed: Known errors - {e}")
        return False
    
    # Test case 3: Edge cases
    try:
        # Test with very small values
        calculated = [0.01, 1.01]
        expected = [0.01, 1.00]
        result = calculate_error_metrics(calculated, expected)
        
        # Should not crash and should produce reasonable results
        assert result['summary_stats']['total_cases'] == 2
        assert result['accuracy_metrics']['exact_matches'] == 1  # First case is exact
        print("✅ Test 3 passed: Edge cases")
        
    except Exception as e:
        print(f"❌ Test 3 failed: Edge cases - {e}")
        return False
    
    # Test case 4: Error validation
    try:
        # Test mismatched lengths
        calculated = [100.0, 200.0]
        expected = [100.0]
        calculate_error_metrics(calculated, expected)
        print("❌ Test 4 failed: Should have raised ValueError for mismatched lengths")
        return False
        
    except ValueError:
        print("✅ Test 4 passed: Error validation")
    
    print("🎉 All synthetic data tests passed!")
    return True

def analyze_error_patterns(error_data, test_cases):
    """
    Analyze error patterns by grouping test cases based on error characteristics.
    
    Groups cases by error type, magnitude, and potential underlying causes to identify
    systematic calculation issues and guide refinement efforts.
    
    Args:
        error_data (list): List of error dictionaries from calculate_error_metrics()
        test_cases (list): Original test cases with input parameters
        
    Returns:
        dict: Dictionary containing pattern analysis results including:
            - error_type_groups: Cases grouped by overestimate/underestimate patterns
            - magnitude_groups: Cases grouped by error severity
            - critical_issues: Cases with severe problems (negative values, extreme errors)
            - input_correlation_patterns: Error patterns correlated with input characteristics
    """
    if len(error_data) != len(test_cases):
        raise ValueError(f"Error data and test cases must have same length: {len(error_data)} vs {len(test_cases)}")
    
    # Initialize pattern analysis structure
    patterns = {
        'error_type_groups': {
            'severe_overestimates': [],  # >100% error
            'moderate_overestimates': [], # 25-100% error
            'minor_overestimates': [],   # 5-25% error
            'close_overestimates': [],   # 0-5% error
            'close_underestimates': [],  # 0-5% error
            'minor_underestimates': [],  # 5-25% error
            'moderate_underestimates': [], # 25-100% error
            'severe_underestimates': []  # >100% error
        },
        'magnitude_groups': {
            'catastrophic': [],  # >$1000 absolute error
            'major': [],        # $500-1000 absolute error
            'significant': [],  # $100-500 absolute error  
            'moderate': [],     # $25-100 absolute error
            'minor': []         # <$25 absolute error
        },
        'critical_issues': {
            'negative_values': [],
            'extreme_percentage_errors': [], # >500% error
            'zero_expected_values': [],
            'invalid_calculations': []
        },
        'input_correlation_patterns': {
            'by_trip_duration': {},
            'by_efficiency_category': {},
            'by_receipt_range': {},
            'by_combined_factors': {}
        }
    }
    
    # Analyze each error case
    for i, (error_info, test_case) in enumerate(zip(error_data, test_cases)):
        inputs = test_case['input']
        
        # Extract input parameters
        duration = inputs['trip_duration_days']
        miles = inputs['miles_traveled']
        receipts = inputs['total_receipts_amount']
        miles_per_day = miles / duration if duration > 0 else 0
        receipts_per_day = receipts / duration if duration > 0 else 0
        
        calculated = error_info['calculated']
        expected = error_info['expected']
        abs_error = abs(error_info['absolute_error'])
        pct_error = error_info['percentage_error']
        abs_pct_error = error_info['absolute_percentage_error']
        
        # Enhanced error info with input context
        enhanced_error = {
            **error_info,
            'inputs': inputs,
            'derived_metrics': {
                'miles_per_day': miles_per_day,
                'receipts_per_day': receipts_per_day,
                'efficiency_category': categorize_efficiency(miles_per_day),
                'trip_duration_category': categorize_trip_duration(duration),
                'receipt_range_category': categorize_receipt_range(receipts_per_day)
            }
        }
        
        # Group by error type and magnitude
        if pct_error > 100:
            patterns['error_type_groups']['severe_overestimates'].append(enhanced_error)
        elif pct_error > 25:
            patterns['error_type_groups']['moderate_overestimates'].append(enhanced_error)
        elif pct_error > 5:
            patterns['error_type_groups']['minor_overestimates'].append(enhanced_error)
        elif pct_error > 0:
            patterns['error_type_groups']['close_overestimates'].append(enhanced_error)
        elif pct_error > -5:
            patterns['error_type_groups']['close_underestimates'].append(enhanced_error)
        elif pct_error > -25:
            patterns['error_type_groups']['minor_underestimates'].append(enhanced_error)
        elif pct_error > -100:
            patterns['error_type_groups']['moderate_underestimates'].append(enhanced_error)
        else:
            patterns['error_type_groups']['severe_underestimates'].append(enhanced_error)
        
        # Group by absolute error magnitude
        if abs_error > 1000:
            patterns['magnitude_groups']['catastrophic'].append(enhanced_error)
        elif abs_error > 500:
            patterns['magnitude_groups']['major'].append(enhanced_error)
        elif abs_error > 100:
            patterns['magnitude_groups']['significant'].append(enhanced_error)
        elif abs_error > 25:
            patterns['magnitude_groups']['moderate'].append(enhanced_error)
        else:
            patterns['magnitude_groups']['minor'].append(enhanced_error)
        
        # Identify critical issues
        if calculated < 0:
            patterns['critical_issues']['negative_values'].append(enhanced_error)
        
        if abs_pct_error > 500:
            patterns['critical_issues']['extreme_percentage_errors'].append(enhanced_error)
        
        if expected == 0:
            patterns['critical_issues']['zero_expected_values'].append(enhanced_error)
        
        if not isinstance(calculated, (int, float)) or calculated != calculated:  # NaN check
            patterns['critical_issues']['invalid_calculations'].append(enhanced_error)
    
    # Analyze input correlations
    patterns['input_correlation_patterns'] = analyze_input_correlations(error_data, test_cases)
    
    # Add summary statistics for each pattern group
    patterns['summary'] = generate_pattern_summary(patterns)
    
    return patterns

def categorize_efficiency(miles_per_day):
    """Categorize trip efficiency based on miles per day."""
    if miles_per_day < 50:
        return 'very_low'
    elif miles_per_day < 100:
        return 'low'
    elif miles_per_day < 150:
        return 'medium_low'
    elif miles_per_day < 180:
        return 'medium'
    elif miles_per_day < 220:
        return 'sweet_spot'
    elif miles_per_day < 300:
        return 'medium_high'
    elif miles_per_day < 400:
        return 'high'
    else:
        return 'very_high'

def categorize_trip_duration(duration):
    """Categorize trip duration."""
    if duration <= 1:
        return 'single_day'
    elif duration <= 2:
        return 'short'
    elif duration <= 5:
        return 'medium'
    elif duration <= 8:
        return 'long'
    else:
        return 'extended'

def categorize_receipt_range(receipts_per_day):
    """Categorize receipt spending per day."""
    if receipts_per_day < 50:
        return 'very_low'
    elif receipts_per_day < 75:
        return 'low'
    elif receipts_per_day < 120:
        return 'medium'
    elif receipts_per_day < 150:
        return 'high'
    else:
        return 'very_high'

def analyze_input_correlations(error_data, test_cases):
    """Analyze correlations between input parameters and error patterns."""
    correlations = {
        'by_trip_duration': {},
        'by_efficiency_category': {},
        'by_receipt_range': {},
        'by_combined_factors': {}
    }
    
    # Group errors by different input characteristics
    for i, (error_info, test_case) in enumerate(zip(error_data, test_cases)):
        inputs = test_case['input']
        duration = inputs['trip_duration_days']
        miles = inputs['miles_traveled']
        receipts = inputs['total_receipts_amount']
        miles_per_day = miles / duration if duration > 0 else 0
        receipts_per_day = receipts / duration if duration > 0 else 0
        
        # Group by trip duration
        duration_key = categorize_trip_duration(duration)
        if duration_key not in correlations['by_trip_duration']:
            correlations['by_trip_duration'][duration_key] = []
        correlations['by_trip_duration'][duration_key].append(error_info)
        
        # Group by efficiency category
        efficiency_key = categorize_efficiency(miles_per_day)
        if efficiency_key not in correlations['by_efficiency_category']:
            correlations['by_efficiency_category'][efficiency_key] = []
        correlations['by_efficiency_category'][efficiency_key].append(error_info)
        
        # Group by receipt range
        receipt_key = categorize_receipt_range(receipts_per_day)
        if receipt_key not in correlations['by_receipt_range']:
            correlations['by_receipt_range'][receipt_key] = []
        correlations['by_receipt_range'][receipt_key].append(error_info)
        
        # Group by combined factors (duration + efficiency)
        combined_key = f"{duration_key}_{efficiency_key}"
        if combined_key not in correlations['by_combined_factors']:
            correlations['by_combined_factors'][combined_key] = []
        correlations['by_combined_factors'][combined_key].append(error_info)
    
    # Calculate statistics for each group
    for category in correlations:
        for group_key in correlations[category]:
            errors = correlations[category][group_key]
            if errors:
                abs_errors = [abs(e['absolute_error']) for e in errors]
                pct_errors = [abs(e['percentage_error']) for e in errors]
                
                correlations[category][group_key] = {
                    'count': len(errors),
                    'mean_absolute_error': sum(abs_errors) / len(abs_errors),
                    'mean_percentage_error': sum(pct_errors) / len(pct_errors),
                    'max_absolute_error': max(abs_errors),
                    'overestimate_rate': sum(1 for e in errors if e['percentage_error'] > 0) / len(errors) * 100,
                    'errors': errors  # Keep for detailed analysis
                }
    
    return correlations

def generate_pattern_summary(patterns):
    """Generate summary statistics for pattern analysis."""
    summary = {}
    
    # Summarize error type groups
    summary['error_types'] = {}
    for error_type, cases in patterns['error_type_groups'].items():
        summary['error_types'][error_type] = {
            'count': len(cases),
            'avg_abs_error': sum(abs(c['absolute_error']) for c in cases) / len(cases) if cases else 0,
            'avg_pct_error': sum(abs(c['percentage_error']) for c in cases) / len(cases) if cases else 0
        }
    
    # Summarize magnitude groups
    summary['magnitudes'] = {}
    for magnitude, cases in patterns['magnitude_groups'].items():
        summary['magnitudes'][magnitude] = {
            'count': len(cases),
            'avg_abs_error': sum(abs(c['absolute_error']) for c in cases) / len(cases) if cases else 0
        }
    
    # Summarize critical issues
    summary['critical_issues'] = {}
    for issue_type, cases in patterns['critical_issues'].items():
        summary['critical_issues'][issue_type] = {
            'count': len(cases),
            'percentage_of_total': len(cases) / sum(len(cases) for cases in patterns['error_type_groups'].values()) * 100 if sum(len(cases) for cases in patterns['error_type_groups'].values()) > 0 else 0
        }
    
    return summary

def test_error_pattern_analysis():
    """Test the error pattern analysis with synthetic data."""
    print("Testing error pattern analysis with synthetic data...")
    
    # Create synthetic test data with known patterns
    test_cases = [
        # High-mileage single day (should cause issues)
        {'input': {'trip_duration_days': 1, 'miles_traveled': 400, 'total_receipts_amount': 150}},
        # Normal 5-day trip  
        {'input': {'trip_duration_days': 5, 'miles_traveled': 800, 'total_receipts_amount': 600}},
        # Low receipt trip
        {'input': {'trip_duration_days': 3, 'miles_traveled': 200, 'total_receipts_amount': 30}},
    ]
    
    # Create corresponding error data
    error_data = [
        {'test_case_index': 0, 'calculated': 500, 'expected': 200, 'absolute_error': 300, 'percentage_error': 150, 'absolute_percentage_error': 150, 'is_overestimate': True, 'is_underestimate': False, 'is_exact_match': False, 'is_close_1_dollar': False, 'is_close_5_percent': False, 'is_close_10_percent': False},
        {'test_case_index': 1, 'calculated': 1050, 'expected': 1000, 'absolute_error': 50, 'percentage_error': 5, 'absolute_percentage_error': 5, 'is_overestimate': True, 'is_underestimate': False, 'is_exact_match': False, 'is_close_1_dollar': False, 'is_close_5_percent': True, 'is_close_10_percent': True},
        {'test_case_index': 2, 'calculated': -50, 'expected': 120, 'absolute_error': -170, 'percentage_error': -141.67, 'absolute_percentage_error': 141.67, 'is_overestimate': False, 'is_underestimate': True, 'is_exact_match': False, 'is_close_1_dollar': False, 'is_close_5_percent': False, 'is_close_10_percent': False}
    ]
    
    try:
        patterns = analyze_error_patterns(error_data, test_cases)
        
        # Verify critical issues detected
        assert len(patterns['critical_issues']['negative_values']) == 1, "Should detect 1 negative value"
        assert len(patterns['error_type_groups']['severe_overestimates']) == 1, "Should detect 1 severe overestimate"
        assert len(patterns['error_type_groups']['close_overestimates']) == 1, "Should detect 1 close overestimate (5% error)"
        
        print("✅ Pattern analysis test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Pattern analysis test failed: {e}")
        return False

def identify_error_prone_ranges(error_data, test_cases, num_bins=10):
    """
    Systematically identify input parameter ranges with highest error rates.
    
    Analyzes input parameters by dividing them into bins and calculating error
    statistics for each range to pinpoint problematic scenarios.
    
    Args:
        error_data (list): List of error dictionaries from calculate_error_metrics()
        test_cases (list): Original test cases with input parameters
        num_bins (int): Number of bins to divide each parameter range into
        
    Returns:
        dict: Dictionary containing range analysis results including:
            - parameter_ranges: Error statistics for each input parameter range
            - critical_ranges: Ranges with highest error rates
            - range_interactions: Error patterns for parameter combinations
            - recommendations: Specific ranges that need attention
    """
    if len(error_data) != len(test_cases):
        raise ValueError(f"Error data and test cases must have same length: {len(error_data)} vs {len(test_cases)}")
    
    # Extract all input values
    durations = [case['input']['trip_duration_days'] for case in test_cases]
    miles = [case['input']['miles_traveled'] for case in test_cases]
    receipts = [case['input']['total_receipts_amount'] for case in test_cases]
    
    # Calculate derived metrics
    miles_per_day = [miles[i] / durations[i] if durations[i] > 0 else 0 for i in range(len(durations))]
    receipts_per_day = [receipts[i] / durations[i] if durations[i] > 0 else 0 for i in range(len(durations))]
    
    range_analysis = {
        'parameter_ranges': {},
        'critical_ranges': {},
        'range_interactions': {},
        'recommendations': []
    }
    
    # Analyze each parameter
    parameters = {
        'trip_duration_days': durations,
        'miles_traveled': miles,
        'total_receipts_amount': receipts,
        'miles_per_day': miles_per_day,
        'receipts_per_day': receipts_per_day
    }
    
    for param_name, values in parameters.items():
        range_analysis['parameter_ranges'][param_name] = analyze_parameter_ranges(
            values, error_data, param_name, num_bins
        )
    
    # Identify critical ranges (top 20% error rates)
    range_analysis['critical_ranges'] = identify_critical_ranges(range_analysis['parameter_ranges'])
    
    # Analyze range interactions for problematic combinations
    range_analysis['range_interactions'] = analyze_range_interactions(
        error_data, test_cases, range_analysis['critical_ranges']
    )
    
    # Generate specific recommendations
    range_analysis['recommendations'] = generate_range_recommendations(
        range_analysis['critical_ranges'], range_analysis['range_interactions']
    )
    
    return range_analysis

def analyze_parameter_ranges(values, error_data, param_name, num_bins):
    """Analyze error patterns across ranges of a specific parameter."""
    if not values:
        return {}
    
    min_val = min(values)
    max_val = max(values)
    
    # Handle edge case where all values are the same
    if min_val == max_val:
        return {
            f"{min_val}": {
                'range': (min_val, max_val),
                'count': len(values),
                'mean_absolute_error': sum(abs(err['absolute_error']) for err in error_data) / len(error_data),
                'mean_percentage_error': sum(abs(err['percentage_error']) for err in error_data) / len(error_data),
                'error_rate_high': sum(1 for err in error_data if abs(err['percentage_error']) > 25) / len(error_data) * 100,
                'negative_value_rate': sum(1 for err in error_data if err['calculated'] < 0) / len(error_data) * 100,
                'overestimate_rate': sum(1 for err in error_data if err['percentage_error'] > 0) / len(error_data) * 100
            }
        }
    
    # Create bins
    bin_width = (max_val - min_val) / num_bins
    ranges = {}
    
    for i in range(num_bins):
        range_start = min_val + i * bin_width
        range_end = min_val + (i + 1) * bin_width
        
        # Find cases in this range
        cases_in_range = []
        errors_in_range = []
        
        for j, value in enumerate(values):
            if i == num_bins - 1:  # Last bin includes upper boundary
                if range_start <= value <= range_end:
                    cases_in_range.append(j)
                    errors_in_range.append(error_data[j])
            else:
                if range_start <= value < range_end:
                    cases_in_range.append(j)
                    errors_in_range.append(error_data[j])
        
        if errors_in_range:
            abs_errors = [abs(err['absolute_error']) for err in errors_in_range]
            pct_errors = [abs(err['percentage_error']) for err in errors_in_range]
            
            range_key = f"{range_start:.1f}-{range_end:.1f}"
            ranges[range_key] = {
                'range': (range_start, range_end),
                'count': len(cases_in_range),
                'mean_absolute_error': sum(abs_errors) / len(abs_errors),
                'mean_percentage_error': sum(pct_errors) / len(pct_errors),
                'max_absolute_error': max(abs_errors),
                'max_percentage_error': max(pct_errors),
                'error_rate_high': sum(1 for err in errors_in_range if abs(err['percentage_error']) > 25) / len(errors_in_range) * 100,
                'error_rate_severe': sum(1 for err in errors_in_range if abs(err['percentage_error']) > 100) / len(errors_in_range) * 100,
                'negative_value_rate': sum(1 for err in errors_in_range if err['calculated'] < 0) / len(errors_in_range) * 100,
                'overestimate_rate': sum(1 for err in errors_in_range if err['percentage_error'] > 0) / len(errors_in_range) * 100,
                'case_indices': cases_in_range,
                'errors': errors_in_range
            }
    
    return ranges

def identify_critical_ranges(parameter_ranges):
    """Identify the most problematic ranges across all parameters."""
    critical_ranges = {}
    
    for param_name, ranges in parameter_ranges.items():
        # Find ranges with highest error rates
        critical_for_param = []
        
        for range_key, stats in ranges.items():
            # Score based on multiple criteria
            error_score = (
                stats['mean_percentage_error'] * 0.4 +  # Mean % error weight
                stats['error_rate_high'] * 0.3 +        # High error rate weight  
                stats['negative_value_rate'] * 2.0 +    # Negative values critical
                stats['error_rate_severe'] * 0.3        # Severe error rate weight
            )
            
            critical_for_param.append((range_key, error_score, stats))
        
        # Sort by error score and take top ranges
        critical_for_param.sort(key=lambda x: x[1], reverse=True)
        
        # Keep ranges with above-average error scores
        if critical_for_param:
            avg_score = sum(x[1] for x in critical_for_param) / len(critical_for_param)
            critical_ranges[param_name] = [
                {
                    'range_key': range_key,
                    'error_score': score,
                    'stats': stats
                }
                for range_key, score, stats in critical_for_param
                if score > avg_score
            ]
    
    return critical_ranges

def analyze_range_interactions(error_data, test_cases, critical_ranges):
    """Analyze interactions between critical ranges of different parameters."""
    interactions = {}
    
    # Find cases that fall into multiple critical ranges
    for i, (error_info, test_case) in enumerate(zip(error_data, test_cases)):
        inputs = test_case['input']
        duration = inputs['trip_duration_days']
        miles = inputs['miles_traveled'] 
        receipts = inputs['total_receipts_amount']
        miles_per_day = miles / duration if duration > 0 else 0
        receipts_per_day = receipts / duration if duration > 0 else 0
        
        # Check which critical ranges this case falls into
        critical_memberships = []
        
        param_values = {
            'trip_duration_days': duration,
            'miles_traveled': miles,
            'total_receipts_amount': receipts,
            'miles_per_day': miles_per_day,
            'receipts_per_day': receipts_per_day
        }
        
        for param_name, value in param_values.items():
            if param_name in critical_ranges:
                for critical_range in critical_ranges[param_name]:
                    range_start, range_end = critical_range['stats']['range']
                    if range_start <= value <= range_end:
                        critical_memberships.append(f"{param_name}:{critical_range['range_key']}")
        
        # Record interactions for cases in multiple critical ranges
        if len(critical_memberships) > 1:
            interaction_key = " + ".join(sorted(critical_memberships))
            
            if interaction_key not in interactions:
                interactions[interaction_key] = {
                    'cases': [],
                    'errors': [],
                    'count': 0
                }
            
            interactions[interaction_key]['cases'].append(i)
            interactions[interaction_key]['errors'].append(error_info)
            interactions[interaction_key]['count'] += 1
    
    # Calculate statistics for each interaction
    for interaction_key in interactions:
        errors = interactions[interaction_key]['errors']
        if errors:
            abs_errors = [abs(err['absolute_error']) for err in errors]
            pct_errors = [abs(err['percentage_error']) for err in errors]
            
            interactions[interaction_key].update({
                'mean_absolute_error': sum(abs_errors) / len(abs_errors),
                'mean_percentage_error': sum(pct_errors) / len(pct_errors),
                'max_absolute_error': max(abs_errors),
                'negative_value_rate': sum(1 for err in errors if err['calculated'] < 0) / len(errors) * 100,
                'severe_error_rate': sum(1 for err in errors if abs(err['percentage_error']) > 100) / len(errors) * 100
            })
    
    return interactions

def generate_range_recommendations(critical_ranges, range_interactions):
    """Generate specific recommendations for addressing problematic ranges."""
    recommendations = []
    
    # Recommendations based on critical ranges
    for param_name, ranges in critical_ranges.items():
        for range_info in ranges:
            range_key = range_info['range_key']
            stats = range_info['stats']
            
            recommendation = {
                'type': 'critical_range',
                'parameter': param_name,
                'range': range_key,
                'priority': 'high' if stats['negative_value_rate'] > 0 else 'medium',
                'issue_description': f"{param_name} in range {range_key}",
                'error_stats': {
                    'mean_pct_error': stats['mean_percentage_error'],
                    'negative_rate': stats['negative_value_rate'],
                    'severe_error_rate': stats.get('error_rate_severe', 0)
                }
            }
            
            # Add specific recommendation text
            if stats['negative_value_rate'] > 0:
                recommendation['recommendation'] = f"CRITICAL: Fix negative value bug for {param_name} in range {range_key}"
            elif stats['mean_percentage_error'] > 50:
                recommendation['recommendation'] = f"High priority: Review calculation logic for {param_name} in range {range_key}"
            else:
                recommendation['recommendation'] = f"Medium priority: Refine handling of {param_name} in range {range_key}"
            
            recommendations.append(recommendation)
    
    # Recommendations based on interactions
    for interaction_key, stats in range_interactions.items():
        if stats['count'] >= 2:  # Only recommend for interactions with multiple cases
            recommendation = {
                'type': 'range_interaction',
                'interaction': interaction_key,
                'priority': 'high' if stats.get('negative_value_rate', 0) > 0 else 'medium',
                'issue_description': f"Cases falling into multiple critical ranges: {interaction_key}",
                'error_stats': {
                    'mean_pct_error': stats['mean_percentage_error'],
                    'case_count': stats['count'],
                    'negative_rate': stats.get('negative_value_rate', 0)
                },
                'recommendation': f"Address interaction effects between: {interaction_key}"
            }
            recommendations.append(recommendation)
    
    # Sort by priority and error severity
    recommendations.sort(key=lambda x: (
        0 if x['priority'] == 'high' else 1,
        -x['error_stats'].get('negative_rate', 0),
        -x['error_stats']['mean_pct_error']
    ))
    
    return recommendations

def test_range_analysis():
    """Test the range analysis with synthetic data."""
    print("Testing range analysis with synthetic data...")
    
    # Create synthetic test data
    test_cases = [
        {'input': {'trip_duration_days': 1, 'miles_traveled': 100, 'total_receipts_amount': 50}},
        {'input': {'trip_duration_days': 1, 'miles_traveled': 300, 'total_receipts_amount': 150}},
        {'input': {'trip_duration_days': 5, 'miles_traveled': 500, 'total_receipts_amount': 400}},
        {'input': {'trip_duration_days': 10, 'miles_traveled': 1000, 'total_receipts_amount': 800}},
    ]
    
    # Create corresponding error data with known patterns
    error_data = [
        {'calculated': 75, 'expected': 100, 'absolute_error': -25, 'percentage_error': -25},
        {'calculated': -50, 'expected': 200, 'absolute_error': -250, 'percentage_error': -125},  # Negative value
        {'calculated': 450, 'expected': 400, 'absolute_error': 50, 'percentage_error': 12.5},
        {'calculated': 900, 'expected': 800, 'absolute_error': 100, 'percentage_error': 12.5}
    ]
    
    try:
        ranges = identify_error_prone_ranges(error_data, test_cases, num_bins=3)
        
        # Verify structure
        assert 'parameter_ranges' in ranges
        assert 'critical_ranges' in ranges
        assert 'recommendations' in ranges
        
        # Check that negative values are flagged as critical
        found_negative_flag = False
        for rec in ranges['recommendations']:
            if 'negative' in rec['recommendation'].lower():
                found_negative_flag = True
                break
        
        assert found_negative_flag, "Should flag negative value issues"
        
        print("✅ Range analysis test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Range analysis test failed: {e}")
        return False

def correlate_input_features_with_errors(error_data, test_cases):
    """
    Investigate relationships between specific input features and observed error patterns.
    
    Applies statistical analysis to find significant correlations between input values 
    and error types, helping to uncover root causes of calculation failures.
    
    Args:
        error_data (list): List of error dictionaries from calculate_error_metrics()
        test_cases (list): Original test cases with input parameters
        
    Returns:
        dict: Dictionary containing correlation analysis results including:
            - feature_correlations: Statistical correlations between features and errors
            - interaction_analysis: Analysis of feature interactions and error patterns
            - root_cause_analysis: Identification of primary error drivers
            - threshold_analysis: Analysis of error rates at different input thresholds
    """
    if len(error_data) != len(test_cases):
        raise ValueError(f"Error data and test cases must have same length: {len(error_data)} vs {len(test_cases)}")
    
    # Extract input features and derived metrics
    features = extract_feature_data(error_data, test_cases)
    
    correlation_analysis = {
        'feature_correlations': {},
        'interaction_analysis': {},
        'root_cause_analysis': {},
        'threshold_analysis': {}
    }
    
    # Calculate statistical correlations
    correlation_analysis['feature_correlations'] = calculate_feature_correlations(features, error_data)
    
    # Analyze feature interactions
    correlation_analysis['interaction_analysis'] = analyze_feature_interactions(features, error_data)
    
    # Identify root causes
    correlation_analysis['root_cause_analysis'] = identify_error_root_causes(features, error_data, test_cases)
    
    # Analyze threshold effects
    correlation_analysis['threshold_analysis'] = analyze_threshold_effects(features, error_data)
    
    return correlation_analysis

def extract_feature_data(error_data, test_cases):
    """Extract comprehensive feature data for correlation analysis."""
    features = {
        # Primary inputs
        'trip_duration_days': [],
        'miles_traveled': [],
        'total_receipts_amount': [],
        
        # Derived metrics
        'miles_per_day': [],
        'receipts_per_day': [],
        'efficiency_ratio': [],  # miles/receipts
        'spending_intensity': [],  # receipts/miles
        
        # Error metrics
        'absolute_error': [],
        'percentage_error': [],
        'is_negative': [],
        'is_severe_error': [],
        'is_overestimate': [],
        
        # Categorized features
        'duration_category': [],
        'efficiency_category': [],
        'receipt_category': [],
        'trip_type': []  # Combined categorization
    }
    
    for i, (error_info, test_case) in enumerate(zip(error_data, test_cases)):
        inputs = test_case['input']
        
        # Primary inputs
        duration = inputs['trip_duration_days']
        miles = inputs['miles_traveled']
        receipts = inputs['total_receipts_amount']
        
        features['trip_duration_days'].append(duration)
        features['miles_traveled'].append(miles)
        features['total_receipts_amount'].append(receipts)
        
        # Derived metrics
        miles_per_day = miles / duration if duration > 0 else 0
        receipts_per_day = receipts / duration if duration > 0 else 0
        efficiency_ratio = miles / receipts if receipts > 0 else 0
        spending_intensity = receipts / miles if miles > 0 else 0
        
        features['miles_per_day'].append(miles_per_day)
        features['receipts_per_day'].append(receipts_per_day)
        features['efficiency_ratio'].append(efficiency_ratio)
        features['spending_intensity'].append(spending_intensity)
        
        # Error metrics
        features['absolute_error'].append(abs(error_info['absolute_error']))
        features['percentage_error'].append(abs(error_info['percentage_error']))
        features['is_negative'].append(1 if error_info['calculated'] < 0 else 0)
        features['is_severe_error'].append(1 if abs(error_info['percentage_error']) > 100 else 0)
        features['is_overestimate'].append(1 if error_info['percentage_error'] > 0 else 0)
        
        # Categorized features
        features['duration_category'].append(categorize_trip_duration(duration))
        features['efficiency_category'].append(categorize_efficiency(miles_per_day))
        features['receipt_category'].append(categorize_receipt_range(receipts_per_day))
        
        # Trip type (combined categorization)
        trip_type = f"{categorize_trip_duration(duration)}_{categorize_efficiency(miles_per_day)}"
        features['trip_type'].append(trip_type)
    
    return features

def calculate_feature_correlations(features, error_data):
    """Calculate statistical correlations between input features and error metrics."""
    correlations = {}
    
    # Numeric features to correlate
    numeric_features = [
        'trip_duration_days', 'miles_traveled', 'total_receipts_amount',
        'miles_per_day', 'receipts_per_day', 'efficiency_ratio', 'spending_intensity'
    ]
    
    # Error metrics to correlate against
    error_metrics = [
        'absolute_error', 'percentage_error', 'is_negative', 'is_severe_error', 'is_overestimate'
    ]
    
    for feature in numeric_features:
        correlations[feature] = {}
        feature_values = features[feature]
        
        for error_metric in error_metrics:
            error_values = features[error_metric]
            
            # Calculate Pearson correlation
            correlation = calculate_pearson_correlation(feature_values, error_values)
            
            # Calculate correlation strength and significance
            correlation_strength = categorize_correlation_strength(correlation)
            
            correlations[feature][error_metric] = {
                'correlation': correlation,
                'strength': correlation_strength,
                'abs_correlation': abs(correlation)
            }
    
    # Rank correlations by strength
    all_correlations = []
    for feature in correlations:
        for error_metric in correlations[feature]:
            corr_data = correlations[feature][error_metric]
            all_correlations.append({
                'feature': feature,
                'error_metric': error_metric,
                'correlation': corr_data['correlation'],
                'abs_correlation': corr_data['abs_correlation'],
                'strength': corr_data['strength']
            })
    
    # Sort by absolute correlation strength
    all_correlations.sort(key=lambda x: x['abs_correlation'], reverse=True)
    correlations['ranked_correlations'] = all_correlations[:20]  # Top 20
    
    return correlations

def analyze_feature_interactions(features, error_data):
    """Analyze how combinations of features interact to produce errors."""
    interactions = {}
    
    # Define feature interaction pairs to analyze
    interaction_pairs = [
        ('trip_duration_days', 'miles_per_day'),
        ('miles_per_day', 'receipts_per_day'),
        ('trip_duration_days', 'receipts_per_day'),
        ('efficiency_ratio', 'spending_intensity'),
        ('miles_traveled', 'total_receipts_amount'),
        ('trip_duration_days', 'efficiency_ratio')
    ]
    
    for feature1, feature2 in interaction_pairs:
        interactions[f"{feature1}_x_{feature2}"] = analyze_feature_pair_interaction(
            features[feature1], features[feature2], features['percentage_error'], 
            features['is_negative'], feature1, feature2
        )
    
    # Analyze categorical interactions
    categorical_interactions = analyze_categorical_interactions(features)
    interactions.update(categorical_interactions)
    
    return interactions

def analyze_feature_pair_interaction(values1, values2, error_percentages, negative_flags, name1, name2):
    """Analyze interaction between two numeric features."""
    # Create interaction bins
    interaction_data = {}
    
    # Divide each feature into quartiles
    q1_1, q3_1 = calculate_quartiles(values1)
    q1_2, q3_2 = calculate_quartiles(values2)
    
    # Define interaction regions
    regions = {
        'low_low': (lambda v1, v2: v1 <= q1_1 and v2 <= q1_2),
        'low_high': (lambda v1, v2: v1 <= q1_1 and v2 >= q3_2),
        'high_low': (lambda v1, v2: v1 >= q3_1 and v2 <= q1_2),
        'high_high': (lambda v1, v2: v1 >= q3_1 and v2 >= q3_2),
        'med_med': (lambda v1, v2: q1_1 < v1 < q3_1 and q1_2 < v2 < q3_2)
    }
    
    for region_name, condition in regions.items():
        region_errors = []
        region_negatives = []
        
        for i, (v1, v2) in enumerate(zip(values1, values2)):
            if condition(v1, v2):
                region_errors.append(error_percentages[i])
                region_negatives.append(negative_flags[i])
        
        if region_errors:
            interaction_data[region_name] = {
                'count': len(region_errors),
                'mean_error': sum(region_errors) / len(region_errors),
                'max_error': max(region_errors),
                'negative_rate': sum(region_negatives) / len(region_negatives) * 100
            }
    
    return interaction_data

def analyze_categorical_interactions(features):
    """Analyze interactions between categorical features and errors."""
    categorical_analysis = {}
    
    # Group by trip type and analyze errors
    trip_type_errors = {}
    trip_types = features['trip_type']
    error_percentages = features['percentage_error']
    negative_flags = features['is_negative']
    
    for i, trip_type in enumerate(trip_types):
        if trip_type not in trip_type_errors:
            trip_type_errors[trip_type] = {
                'errors': [],
                'negatives': []
            }
        
        trip_type_errors[trip_type]['errors'].append(error_percentages[i])
        trip_type_errors[trip_type]['negatives'].append(negative_flags[i])
    
    # Calculate statistics for each trip type
    for trip_type, data in trip_type_errors.items():
        if len(data['errors']) >= 2:  # Only analyze types with multiple cases
            categorical_analysis[f"trip_type_{trip_type}"] = {
                'count': len(data['errors']),
                'mean_error': sum(data['errors']) / len(data['errors']),
                'max_error': max(data['errors']),
                'negative_rate': sum(data['negatives']) / len(data['negatives']) * 100,
                'error_variance': calculate_variance(data['errors'])
            }
    
    return categorical_analysis

def identify_error_root_causes(features, error_data, test_cases):
    """Identify primary drivers of calculation errors through correlation analysis."""
    root_causes = {
        'primary_drivers': [],
        'negative_value_causes': [],
        'severe_error_causes': [],
        'systematic_biases': []
    }
    
    # Analyze negative value causes
    negative_cases = [(i, case, err) for i, (case, err) in enumerate(zip(test_cases, error_data)) if err['calculated'] < 0]
    
    if negative_cases:
        negative_analysis = analyze_negative_value_patterns(negative_cases, features)
        root_causes['negative_value_causes'] = negative_analysis
    
    # Analyze severe error causes (>100% error)
    severe_cases = [(i, case, err) for i, (case, err) in enumerate(zip(test_cases, error_data)) if abs(err['percentage_error']) > 100]
    
    if severe_cases:
        severe_analysis = analyze_severe_error_patterns(severe_cases, features)
        root_causes['severe_error_causes'] = severe_analysis
    
    # Identify systematic biases
    bias_analysis = analyze_systematic_biases(features, error_data)
    root_causes['systematic_biases'] = bias_analysis
    
    # Identify primary error drivers through correlation
    primary_drivers = identify_primary_error_drivers(features)
    root_causes['primary_drivers'] = primary_drivers
    
    return root_causes

def analyze_negative_value_patterns(negative_cases, features):
    """Analyze patterns in cases that produce negative reimbursement values."""
    if not negative_cases:
        return {}
    
    negative_indices = [case[0] for case in negative_cases]
    
    # Extract feature values for negative cases
    negative_patterns = {}
    
    for feature_name in ['trip_duration_days', 'miles_per_day', 'receipts_per_day', 'efficiency_ratio']:
        feature_values = [features[feature_name][i] for i in negative_indices]
        
        if feature_values:
            negative_patterns[feature_name] = {
                'mean': sum(feature_values) / len(feature_values),
                'min': min(feature_values),
                'max': max(feature_values),
                'common_range': f"{min(feature_values):.1f} - {max(feature_values):.1f}"
            }
    
    # Identify most common characteristics
    negative_patterns['common_characteristics'] = {
        'most_common_duration_category': most_common([features['duration_category'][i] for i in negative_indices]),
        'most_common_efficiency_category': most_common([features['efficiency_category'][i] for i in negative_indices]),
        'avg_miles_per_day': sum(features['miles_per_day'][i] for i in negative_indices) / len(negative_indices)
    }
    
    return negative_patterns

def analyze_severe_error_patterns(severe_cases, features):
    """Analyze patterns in cases with severe errors (>100%)."""
    if not severe_cases:
        return {}
    
    severe_indices = [case[0] for case in severe_cases]
    
    # Group severe errors by magnitude
    severe_patterns = {
        'extreme_overestimates': [],  # >200% overestimate
        'extreme_underestimates': [], # >200% underestimate
        'moderate_severe': []         # 100-200% error
    }
    
    for idx in severe_indices:
        error_pct = features['percentage_error'][idx]
        
        if error_pct > 200:
            severe_patterns['extreme_overestimates'].append(idx)
        elif error_pct < -200:
            severe_patterns['extreme_underestimates'].append(idx)
        else:
            severe_patterns['moderate_severe'].append(idx)
    
    # Analyze characteristics of each severity group
    characteristics = {}
    for severity, indices in severe_patterns.items():
        if indices and not severity.endswith('_characteristics'):
            characteristics[f"{severity}_characteristics"] = {
                'count': len(indices),
                'avg_miles_per_day': sum(features['miles_per_day'][i] for i in indices) / len(indices),
                'avg_receipts_per_day': sum(features['receipts_per_day'][i] for i in indices) / len(indices),
                'common_trip_type': most_common([features['trip_type'][i] for i in indices])
            }
    
    # Add characteristics to severe_patterns
    severe_patterns.update(characteristics)
    
    return severe_patterns

def analyze_systematic_biases(features, error_data):
    """Identify systematic biases in the calculation model."""
    biases = {}
    
    # Analyze overestimate vs underestimate patterns by feature ranges
    duration_ranges = [(0, 2), (2, 5), (5, 10), (10, float('inf'))]
    
    for min_dur, max_dur in duration_ranges:
        range_indices = [i for i, dur in enumerate(features['trip_duration_days']) 
                        if min_dur <= dur < max_dur]
        
        if len(range_indices) >= 3:  # Only analyze ranges with sufficient data
            overestimate_rate = sum(1 for i in range_indices if features['is_overestimate'][i]) / len(range_indices) * 100
            avg_error = sum(features['percentage_error'][i] for i in range_indices) / len(range_indices)
            
            range_key = f"duration_{min_dur}_{max_dur}_days"
            biases[range_key] = {
                'overestimate_rate': overestimate_rate,
                'avg_signed_error': avg_error,
                'bias_direction': 'overestimate' if overestimate_rate > 60 else 'underestimate' if overestimate_rate < 40 else 'balanced'
            }
    
    return biases

def analyze_threshold_effects(features, error_data):
    """Analyze how errors change at different input thresholds."""
    threshold_analysis = {}
    
    # Define thresholds to analyze
    thresholds = {
        'miles_per_day': [50, 100, 180, 220, 300, 400],
        'receipts_per_day': [75, 120, 150, 200, 300],
        'trip_duration_days': [1, 2, 5, 8, 10],
        'efficiency_ratio': [0.5, 1.0, 2.0, 5.0]
    }
    
    for feature_name, threshold_values in thresholds.items():
        threshold_analysis[feature_name] = analyze_feature_thresholds(
            features[feature_name], features['percentage_error'], 
            features['is_negative'], threshold_values
        )
    
    return threshold_analysis

def analyze_feature_thresholds(feature_values, error_percentages, negative_flags, thresholds):
    """Analyze error patterns at different thresholds for a feature."""
    threshold_results = {}
    
    for threshold in thresholds:
        below_indices = [i for i, val in enumerate(feature_values) if val < threshold]
        above_indices = [i for i, val in enumerate(feature_values) if val >= threshold]
        
        if below_indices and above_indices:
            below_errors = [error_percentages[i] for i in below_indices]
            above_errors = [error_percentages[i] for i in above_indices]
            
            below_negatives = [negative_flags[i] for i in below_indices]
            above_negatives = [negative_flags[i] for i in above_indices]
            
            threshold_results[f"threshold_{threshold}"] = {
                'below_threshold': {
                    'count': len(below_indices),
                    'mean_error': sum(below_errors) / len(below_errors),
                    'negative_rate': sum(below_negatives) / len(below_negatives) * 100
                },
                'above_threshold': {
                    'count': len(above_indices),
                    'mean_error': sum(above_errors) / len(above_errors),
                    'negative_rate': sum(above_negatives) / len(above_negatives) * 100
                },
                'threshold_effect': {
                    'error_change': (sum(above_errors) / len(above_errors)) - (sum(below_errors) / len(below_errors)),
                    'negative_rate_change': (sum(above_negatives) / len(above_negatives) * 100) - (sum(below_negatives) / len(below_negatives) * 100)
                }
            }
    
    return threshold_results

# Helper functions for correlation analysis

def calculate_pearson_correlation(x, y):
    """Calculate Pearson correlation coefficient between two lists."""
    if len(x) != len(y) or len(x) == 0:
        return 0
    
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(x[i] * x[i] for i in range(n))
    sum_y2 = sum(y[i] * y[i] for i in range(n))
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator_x = n * sum_x2 - sum_x * sum_x
    denominator_y = n * sum_y2 - sum_y * sum_y
    
    if denominator_x <= 0 or denominator_y <= 0:
        return 0
    
    denominator = (denominator_x * denominator_y) ** 0.5
    
    return numerator / denominator if denominator != 0 else 0

def categorize_correlation_strength(correlation):
    """Categorize correlation strength based on absolute value."""
    abs_corr = abs(correlation)
    if abs_corr >= 0.7:
        return 'strong'
    elif abs_corr >= 0.5:
        return 'moderate'
    elif abs_corr >= 0.3:
        return 'weak'
    else:
        return 'negligible'

def calculate_quartiles(values):
    """Calculate Q1 and Q3 quartiles for a list of values."""
    if not values:
        return 0, 0
    
    sorted_values = sorted(values)
    n = len(sorted_values)
    
    q1_index = n // 4
    q3_index = 3 * n // 4
    
    q1 = sorted_values[q1_index]
    q3 = sorted_values[q3_index] if q3_index < n else sorted_values[-1]
    
    return q1, q3

def calculate_variance(values):
    """Calculate variance of a list of values."""
    if len(values) <= 1:
        return 0
    
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / (len(values) - 1)

def most_common(items):
    """Find the most common item in a list."""
    if not items:
        return None
    
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    
    return max(counts, key=counts.get)

def identify_primary_error_drivers(features):
    """Identify the primary features driving calculation errors."""
    # Calculate correlation strength with different error metrics
    primary_drivers = []
    
    numeric_features = ['trip_duration_days', 'miles_per_day', 'receipts_per_day', 'efficiency_ratio']
    error_metrics = ['percentage_error', 'is_negative', 'is_severe_error']
    
    for feature in numeric_features:
        total_correlation_strength = 0
        correlations = {}
        
        for error_metric in error_metrics:
            corr = calculate_pearson_correlation(features[feature], features[error_metric])
            correlations[error_metric] = corr
            total_correlation_strength += abs(corr)
        
        primary_drivers.append({
            'feature': feature,
            'total_correlation_strength': total_correlation_strength,
            'correlations': correlations,
            'primary_error_driver': total_correlation_strength > 0.8  # Threshold for primary driver
        })
    
    # Sort by total correlation strength
    primary_drivers.sort(key=lambda x: x['total_correlation_strength'], reverse=True)
    
    return primary_drivers

def test_correlation_analysis():
    """Test the correlation analysis with synthetic data."""
    print("Testing correlation analysis with synthetic data...")
    
    # Create synthetic test data with known correlations
    test_cases = [
        {'input': {'trip_duration_days': 1, 'miles_traveled': 400, 'total_receipts_amount': 100}},  # High miles/day
        {'input': {'trip_duration_days': 1, 'miles_traveled': 200, 'total_receipts_amount': 150}},  # Medium miles/day  
        {'input': {'trip_duration_days': 5, 'miles_traveled': 500, 'total_receipts_amount': 400}},  # Normal trip
        {'input': {'trip_duration_days': 10, 'miles_traveled': 300, 'total_receipts_amount': 800}}, # Low efficiency
    ]
    
    # Create error data with patterns correlated to miles_per_day
    error_data = [
        {'calculated': -100, 'expected': 200, 'absolute_error': -300, 'percentage_error': -150},  # Negative for high miles/day
        {'calculated': 180, 'expected': 180, 'absolute_error': 0, 'percentage_error': 0},
        {'calculated': 420, 'expected': 400, 'absolute_error': 20, 'percentage_error': 5},
        {'calculated': 850, 'expected': 800, 'absolute_error': 50, 'percentage_error': 6.25}
    ]
    
    try:
        correlations = correlate_input_features_with_errors(error_data, test_cases)
        
        # Verify structure
        assert 'feature_correlations' in correlations
        assert 'interaction_analysis' in correlations
        assert 'root_cause_analysis' in correlations
        assert 'threshold_analysis' in correlations
        
        # Check that correlations were calculated
        assert 'ranked_correlations' in correlations['feature_correlations']
        
        # Check that negative value analysis was performed
        assert 'negative_value_causes' in correlations['root_cause_analysis']
        
        print("✅ Correlation analysis test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Correlation analysis test failed: {e}")
        return False

def generate_comprehensive_error_report(test_cases, sample_size=100, output_file=None):
    """
    Generate a comprehensive error analysis report combining all analysis frameworks.
    
    Produces a detailed report that summarizes error metrics, patterns, correlations,
    and actionable insights for refining the calculation logic.
    
    Args:
        test_cases (list): List of test cases to analyze
        sample_size (int): Number of test cases to analyze (default: 100)
        output_file (str): Optional file path to save the report
        
    Returns:
        dict: Complete error analysis report with all findings and recommendations
    """
    print(f"Generating comprehensive error analysis report for {sample_size} test cases...")
    
    # Sample the test cases
    sample_cases = test_cases[:sample_size]
    
    # Calculate predictions and get error metrics
    print("1. Calculating model predictions...")
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
    
    # Perform all analyses
    print("2. Performing error metrics analysis...")
    error_metrics = calculate_error_metrics(calculated, expected)
    error_data = error_metrics['error_data']
    
    print("3. Analyzing error patterns...")
    pattern_analysis = analyze_error_patterns(error_data, sample_cases)
    
    print("4. Identifying error-prone ranges...")
    range_analysis = identify_error_prone_ranges(error_data, sample_cases, num_bins=8)
    
    print("5. Correlating input features with errors...")
    correlation_analysis = correlate_input_features_with_errors(error_data, sample_cases)
    
    # Compile comprehensive report
    print("6. Compiling comprehensive report...")
    report = {
        'executive_summary': generate_executive_summary(error_metrics, pattern_analysis, range_analysis, correlation_analysis),
        'error_metrics': error_metrics,
        'pattern_analysis': pattern_analysis,
        'range_analysis': range_analysis,
        'correlation_analysis': correlation_analysis,
        'critical_findings': extract_critical_findings(error_metrics, pattern_analysis, range_analysis, correlation_analysis),
        'actionable_recommendations': generate_actionable_recommendations(pattern_analysis, range_analysis, correlation_analysis),
        'implementation_roadmap': create_implementation_roadmap(pattern_analysis, range_analysis, correlation_analysis),
        'test_cases_analyzed': sample_size,
        'model_performance_summary': summarize_model_performance(error_metrics)
    }
    
    # Generate narrative report
    narrative_report = format_narrative_report(report)
    
    # Save to file if specified
    if output_file:
        save_report_to_file(narrative_report, output_file)
        print(f"Report saved to: {output_file}")
    
    # Print summary to console
    print_report_summary(report)
    
    return {
        'structured_report': report,
        'narrative_report': narrative_report
    }

def generate_executive_summary(error_metrics, pattern_analysis, range_analysis, correlation_analysis):
    """Generate executive summary of key findings."""
    summary = error_metrics['summary_stats']
    accuracy = error_metrics['accuracy_metrics']
    
    # Identify most critical issues
    critical_issues = []
    
    # Negative values
    negative_count = len(pattern_analysis['critical_issues']['negative_values'])
    if negative_count > 0:
        critical_issues.append(f"Critical bug: {negative_count} cases ({negative_count/summary['total_cases']*100:.1f}%) produce negative reimbursement values")
    
    # Poor accuracy
    if accuracy['exact_match_rate'] < 5:
        critical_issues.append(f"Severe accuracy issue: {accuracy['exact_match_rate']:.1f}% exact matches, {accuracy['close_5_percent_rate']:.1f}% within 5%")
    
    # High error rates
    if summary['mean_percentage_error'] > 40:
        critical_issues.append(f"High average error: {summary['mean_percentage_error']:.1f}% mean percentage error")
    
    # Systematic bias
    if abs(summary['overall_bias']) > 100:
        bias_direction = "overestimation" if summary['overall_bias'] > 0 else "underestimation"
        critical_issues.append(f"Systematic {bias_direction} bias: ${abs(summary['overall_bias']):.2f} average")
    
    return {
        'model_status': 'CRITICAL' if len(critical_issues) >= 3 else 'NEEDS_IMPROVEMENT' if len(critical_issues) >= 1 else 'ACCEPTABLE',
        'critical_issues': critical_issues,
        'total_cases_analyzed': summary['total_cases'],
        'overall_accuracy': accuracy['close_5_percent_rate'],
        'primary_concerns': extract_primary_concerns(pattern_analysis, range_analysis, correlation_analysis)
    }

def extract_critical_findings(error_metrics, pattern_analysis, range_analysis, correlation_analysis):
    """Extract the most critical findings across all analyses."""
    findings = {
        'immediate_fixes_required': [],
        'systematic_issues': [],
        'performance_bottlenecks': [],
        'root_causes_identified': []
    }
    
    # Immediate fixes (negative values, extreme errors)
    if pattern_analysis['critical_issues']['negative_values']:
        findings['immediate_fixes_required'].append({
            'issue': 'Negative reimbursement values',
            'severity': 'CRITICAL',
            'count': len(pattern_analysis['critical_issues']['negative_values']),
            'primary_cause': 'Efficiency penalty calculation in medium-high miles/day range'
        })
    
    if pattern_analysis['critical_issues']['extreme_percentage_errors']:
        findings['immediate_fixes_required'].append({
            'issue': 'Extreme percentage errors (>500%)',
            'severity': 'HIGH',
            'count': len(pattern_analysis['critical_issues']['extreme_percentage_errors']),
            'primary_cause': 'Edge case logic for single-day high-mileage trips'
        })
    
    # Systematic issues
    findings['systematic_issues'] = [
        {
            'issue': 'Single-day trip calculation failure',
            'evidence': 'Worst performing duration category with 66.1% average error',
            'impact': '20 cases in sample, consistent failure pattern'
        },
        {
            'issue': 'Receipt amount scaling problems',
            'evidence': 'Strong positive correlation (0.510) with overestimation',
            'impact': 'Affects all high-receipt cases, systematic bias'
        },
        {
            'issue': 'Efficiency threshold cascade effects',
            'evidence': 'Sharp error increases at 180 and 220 miles/day thresholds',
            'impact': '+32.3% error increase and +12.5% negative rate change'
        }
    ]
    
    # Performance bottlenecks
    worst_ranges = []
    for param, ranges in range_analysis['critical_ranges'].items():
        for range_info in ranges:
            if range_info['error_score'] > 70:  # High error score threshold
                worst_ranges.append({
                    'parameter': param,
                    'range': range_info['range_key'],
                    'error_score': range_info['error_score'],
                    'cases': range_info['stats']['count']
                })
    
    findings['performance_bottlenecks'] = sorted(worst_ranges, key=lambda x: x['error_score'], reverse=True)[:5]
    
    # Root causes
    primary_drivers = correlation_analysis['root_cause_analysis']['primary_drivers']
    findings['root_causes_identified'] = [
        {
            'factor': driver['feature'],
            'correlation_strength': driver['total_correlation_strength'],
            'is_primary_driver': driver['primary_error_driver']
        }
        for driver in primary_drivers[:3]  # Top 3 drivers
    ]
    
    return findings

def generate_actionable_recommendations(pattern_analysis, range_analysis, correlation_analysis):
    """Generate prioritized, actionable recommendations for fixing the model."""
    recommendations = {
        'immediate_actions': [],
        'short_term_improvements': [],
        'long_term_enhancements': []
    }
    
    # Immediate actions (critical bugs)
    recommendations['immediate_actions'] = [
        {
            'priority': 1,
            'action': 'Fix negative value bug in efficiency penalty calculation',
            'target': 'Miles/day range 232.1-344.9 (25% negative rate)',
            'expected_impact': 'Eliminate 3% of cases producing negative values',
            'implementation': 'Review and correct efficiency penalty formula in Edge Case 3'
        },
        {
            'priority': 2,
            'action': 'Redesign single-day trip calculation logic',
            'target': 'Duration 1.0-2.4 days (56.9% avg error)',
            'expected_impact': 'Improve accuracy for 31% of test cases',
            'implementation': 'Create specialized single-day trip handling in Edge Case 1'
        },
        {
            'priority': 3,
            'action': 'Fix threshold cascade at 220 miles/day',
            'target': 'Miles/day threshold causing +12.5% negative rate jump',
            'expected_impact': 'Reduce negative value risk for medium-high efficiency trips',
            'implementation': 'Smooth transition logic around efficiency thresholds'
        }
    ]
    
    # Short-term improvements (systematic issues)
    recommendations['short_term_improvements'] = [
        {
            'priority': 4,
            'action': 'Adjust receipt scaling for high amounts',
            'target': 'Receipts >$300/day (30.5% error increase)',
            'expected_impact': 'Reduce systematic overestimation for high-spend trips',
            'implementation': 'Implement progressive scaling instead of linear multiplication'
        },
        {
            'priority': 5,
            'action': 'Rebalance duration-based biases',
            'target': '10+ day trips (70% overestimate rate)',
            'expected_impact': 'Eliminate systematic overestimation for extended trips',
            'implementation': 'Review base rate reduction formula for long trips'
        },
        {
            'priority': 6,
            'action': 'Optimize efficiency sweet spot logic',
            'target': '180-220 miles/day range performing worse than expected',
            'expected_impact': 'Improve accuracy for supposedly optimal efficiency range',
            'implementation': 'Review sweet spot parameters and edge case conditions'
        }
    ]
    
    # Long-term enhancements
    recommendations['long_term_enhancements'] = [
        {
            'priority': 7,
            'action': 'Implement machine learning calibration',
            'target': 'Overall model accuracy (currently 0% exact matches)',
            'expected_impact': 'Improve overall accuracy to >80% within 5%',
            'implementation': 'Use error patterns to train ML adjustment layer'
        },
        {
            'priority': 8,
            'action': 'Develop comprehensive test suite',
            'target': 'All edge cases and parameter combinations',
            'expected_impact': 'Prevent regression and ensure robustness',
            'implementation': 'Create automated testing based on error analysis insights'
        },
        {
            'priority': 9,
            'action': 'Implement continuous error monitoring',
            'target': 'Real-time detection of calculation drift',
            'expected_impact': 'Early detection of calculation issues in production',
            'implementation': 'Deploy error analysis framework for ongoing monitoring'
        }
    ]
    
    return recommendations

def create_implementation_roadmap(pattern_analysis, range_analysis, correlation_analysis):
    """Create a phased implementation roadmap."""
    return {
        'phase_1_critical_fixes': {
            'duration': '1-2 weeks',
            'goal': 'Eliminate negative values and extreme errors',
            'deliverables': [
                'Fix efficiency penalty calculation bug',
                'Implement single-day trip handling',
                'Smooth threshold transitions at 220 miles/day'
            ],
            'success_criteria': 'Zero negative values, <5% cases with >100% error'
        },
        'phase_2_accuracy_improvements': {
            'duration': '3-4 weeks',
            'goal': 'Achieve 50%+ accuracy within 5%',
            'deliverables': [
                'Optimize receipt scaling logic',
                'Rebalance duration-based calculations',
                'Refine efficiency sweet spot parameters'
            ],
            'success_criteria': '>50% cases within 5% error, <30% mean percentage error'
        },
        'phase_3_systematic_optimization': {
            'duration': '6-8 weeks',
            'goal': 'Achieve production-ready accuracy',
            'deliverables': [
                'ML-based calibration system',
                'Comprehensive test coverage',
                'Continuous monitoring framework'
            ],
            'success_criteria': '>80% cases within 5% error, robust performance monitoring'
        }
    }

def summarize_model_performance(error_metrics):
    """Summarize current model performance."""
    summary = error_metrics['summary_stats']
    accuracy = error_metrics['accuracy_metrics']
    
    return {
        'accuracy_metrics': {
            'exact_matches': f"{accuracy['exact_matches']} ({accuracy['exact_match_rate']:.1f}%)",
            'within_1_dollar': f"{accuracy['close_1_dollar_count']} ({accuracy['close_1_dollar_rate']:.1f}%)",
            'within_5_percent': f"{accuracy['close_5_percent_count']} ({accuracy['close_5_percent_rate']:.1f}%)",
            'within_10_percent': f"{accuracy['close_10_percent_count']} ({accuracy['close_10_percent_rate']:.1f}%)"
        },
        'error_distribution': {
            'mean_absolute_error': f"${summary['mean_absolute_error']:.2f}",
            'mean_percentage_error': f"{summary['mean_percentage_error']:.1f}%",
            'median_absolute_error': f"${summary['median_absolute_error']:.2f}",
            'max_absolute_error': f"${summary['max_absolute_error']:.2f}"
        },
        'bias_analysis': {
            'overall_bias': f"${summary['overall_bias']:.2f}",
            'overestimate_rate': f"{accuracy['overestimate_rate']:.1f}%",
            'underestimate_rate': f"{accuracy['underestimate_rate']:.1f}%"
        },
        'performance_grade': calculate_performance_grade(accuracy['close_5_percent_rate'], summary['mean_percentage_error'])
    }

def calculate_performance_grade(accuracy_within_5_pct, mean_pct_error):
    """Calculate overall performance grade."""
    if accuracy_within_5_pct >= 80 and mean_pct_error <= 10:
        return 'A (Excellent)'
    elif accuracy_within_5_pct >= 60 and mean_pct_error <= 20:
        return 'B (Good)'
    elif accuracy_within_5_pct >= 40 and mean_pct_error <= 30:
        return 'C (Acceptable)'
    elif accuracy_within_5_pct >= 20 and mean_pct_error <= 50:
        return 'D (Needs Improvement)'
    else:
        return 'F (Critical Issues)'

def extract_primary_concerns(pattern_analysis, range_analysis, correlation_analysis):
    """Extract primary concerns from all analyses."""
    concerns = []
    
    # Check for negative values
    negative_count = len(pattern_analysis['critical_issues']['negative_values'])
    if negative_count > 0:
        concerns.append(f"Negative reimbursement bug affecting {negative_count} cases")
    
    # Check for critical ranges
    total_critical_ranges = sum(len(ranges) for ranges in range_analysis['critical_ranges'].values())
    if total_critical_ranges > 10:
        concerns.append(f"Widespread accuracy issues across {total_critical_ranges} parameter ranges")
    
    # Check for strong correlations indicating systematic problems
    strong_correlations = [
        corr for corr in correlation_analysis['feature_correlations']['ranked_correlations'][:5]
        if corr['abs_correlation'] > 0.4
    ]
    if len(strong_correlations) > 2:
        concerns.append("Strong correlations indicate systematic calculation biases")
    
    return concerns

def format_narrative_report(report):
    """Format the structured report as a narrative document."""
    narrative = []
    
    # Title and Executive Summary
    narrative.append("# COMPREHENSIVE ERROR ANALYSIS REPORT")
    narrative.append("## Reimbursement Calculation Model Analysis")
    narrative.append("")
    
    # Executive Summary
    exec_summary = report['executive_summary']
    narrative.append("## EXECUTIVE SUMMARY")
    narrative.append("")
    narrative.append(f"**Model Status:** {exec_summary['model_status']}")
    narrative.append(f"**Cases Analyzed:** {exec_summary['total_cases_analyzed']}")
    narrative.append(f"**Overall Accuracy:** {exec_summary['overall_accuracy']:.1f}% within 5%")
    narrative.append("")
    
    if exec_summary['critical_issues']:
        narrative.append("**Critical Issues Identified:**")
        for issue in exec_summary['critical_issues']:
            narrative.append(f"- {issue}")
        narrative.append("")
    
    # Performance Summary
    performance = report['model_performance_summary']
    narrative.append("## MODEL PERFORMANCE SUMMARY")
    narrative.append("")
    narrative.append(f"**Performance Grade:** {performance['performance_grade']}")
    narrative.append("")
    narrative.append("**Accuracy Metrics:**")
    for metric, value in performance['accuracy_metrics'].items():
        narrative.append(f"- {metric.replace('_', ' ').title()}: {value}")
    narrative.append("")
    
    narrative.append("**Error Distribution:**")
    for metric, value in performance['error_distribution'].items():
        narrative.append(f"- {metric.replace('_', ' ').title()}: {value}")
    narrative.append("")
    
    # Critical Findings
    findings = report['critical_findings']
    narrative.append("## CRITICAL FINDINGS")
    narrative.append("")
    
    if findings['immediate_fixes_required']:
        narrative.append("### Immediate Fixes Required")
        for fix in findings['immediate_fixes_required']:
            narrative.append(f"**{fix['issue']}** ({fix['severity']})")
            narrative.append(f"- Count: {fix['count']} cases")
            narrative.append(f"- Cause: {fix['primary_cause']}")
            narrative.append("")
    
    if findings['systematic_issues']:
        narrative.append("### Systematic Issues")
        for issue in findings['systematic_issues']:
            narrative.append(f"**{issue['issue']}**")
            narrative.append(f"- Evidence: {issue['evidence']}")
            narrative.append(f"- Impact: {issue['impact']}")
            narrative.append("")
    
    # Recommendations
    recommendations = report['actionable_recommendations']
    narrative.append("## ACTIONABLE RECOMMENDATIONS")
    narrative.append("")
    
    narrative.append("### Immediate Actions (Critical)")
    for action in recommendations['immediate_actions']:
        narrative.append(f"{action['priority']}. **{action['action']}**")
        narrative.append(f"   - Target: {action['target']}")
        narrative.append(f"   - Impact: {action['expected_impact']}")
        narrative.append(f"   - Implementation: {action['implementation']}")
        narrative.append("")
    
    narrative.append("### Short-term Improvements")
    for action in recommendations['short_term_improvements']:
        narrative.append(f"{action['priority']}. **{action['action']}**")
        narrative.append(f"   - Target: {action['target']}")
        narrative.append(f"   - Impact: {action['expected_impact']}")
        narrative.append("")
    
    # Implementation Roadmap
    roadmap = report['implementation_roadmap']
    narrative.append("## IMPLEMENTATION ROADMAP")
    narrative.append("")
    
    for phase_name, phase_info in roadmap.items():
        phase_title = phase_name.replace('_', ' ').title()
        narrative.append(f"### {phase_title}")
        narrative.append(f"**Duration:** {phase_info['duration']}")
        narrative.append(f"**Goal:** {phase_info['goal']}")
        narrative.append("")
        narrative.append("**Deliverables:**")
        for deliverable in phase_info['deliverables']:
            narrative.append(f"- {deliverable}")
        narrative.append("")
        narrative.append(f"**Success Criteria:** {phase_info['success_criteria']}")
        narrative.append("")
    
    return "\n".join(narrative)

def save_report_to_file(narrative_report, output_file):
    """Save the narrative report to a file."""
    try:
        with open(output_file, 'w') as f:
            f.write(narrative_report)
    except Exception as e:
        print(f"Warning: Could not save report to {output_file}: {e}")

def print_report_summary(report):
    """Print a summary of the report to console."""
    print("\n" + "="*80)
    print("COMPREHENSIVE ERROR ANALYSIS REPORT SUMMARY")
    print("="*80)
    
    exec_summary = report['executive_summary']
    performance = report['model_performance_summary']
    
    print(f"\n📊 MODEL STATUS: {exec_summary['model_status']}")
    print(f"📈 PERFORMANCE GRADE: {performance['performance_grade']}")
    print(f"🎯 ACCURACY (5%): {exec_summary['overall_accuracy']:.1f}%")
    print(f"📋 CASES ANALYZED: {exec_summary['total_cases_analyzed']}")
    
    print(f"\n🚨 CRITICAL ISSUES:")
    for issue in exec_summary['critical_issues']:
        print(f"  • {issue}")
    
    print(f"\n💡 TOP RECOMMENDATIONS:")
    recommendations = report['actionable_recommendations']['immediate_actions']
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec['action']}")
        print(f"     Impact: {rec['expected_impact']}")
    
    print("\n" + "="*80)

def test_comprehensive_report_generation():
    """Test the comprehensive report generation with synthetic data."""
    print("Testing comprehensive report generation...")
    
    # Create minimal test data with expected outputs
    test_cases = [
        {'input': {'trip_duration_days': 1, 'miles_traveled': 400, 'total_receipts_amount': 100}, 'expected_output': 200.0},
        {'input': {'trip_duration_days': 5, 'miles_traveled': 500, 'total_receipts_amount': 400}, 'expected_output': 450.0},
    ]
    
    try:
        report_result = generate_comprehensive_error_report(test_cases, sample_size=2)
        
        # Verify structure
        assert 'structured_report' in report_result
        assert 'narrative_report' in report_result
        
        structured = report_result['structured_report']
        assert 'executive_summary' in structured
        assert 'actionable_recommendations' in structured
        assert 'implementation_roadmap' in structured
        
        print("✅ Comprehensive report generation test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        return False

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Calculate the reimbursement amount based on input parameters.
    
    REFINED VERSION - Addresses critical issues from error analysis:
    - Fixed negative reimbursement bug with bounded efficiency penalty
    - Added proper single-day trip handling
    - Reduced receipt multipliers to prevent systematic overestimation
    - Smoothed threshold transitions for better calculation stability
    
    Args:
        trip_duration_days (float): Number of days for the trip
        miles_traveled (float): Total miles traveled  
        total_receipts_amount (float): Total amount from receipts
    
    Returns:
        float: Calculated reimbursement amount
    """
    # Calculate efficiency metric
    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0
    receipts_per_day = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else total_receipts_amount
    
    # PRIORITY 1.2: Single-day trip handling with aggressive receipt capping
    # Critical fix: Handle single-day trips properly with receipt limits
    if trip_duration_days <= 1.5:  # Handles 1-day trips with small buffer
        base_single_day = 80  # Lower base for short trips
        
        # Apply aggressive receipt capping for single-day trips too
        if total_receipts_amount > 1000:  # Very high single-day receipts
            receipt_component = 200 + (total_receipts_amount - 1000) * 0.1  # Heavy capping above $1000
        elif total_receipts_amount > 500:  # High single-day receipts
            receipt_component = total_receipts_amount * 0.4  # 40% of receipts above $500
        elif total_receipts_amount > 200:  # Medium single-day receipts
            receipt_component = total_receipts_amount * 0.7  # 70% of medium receipts
        else:
            receipt_component = total_receipts_amount * 1.0  # Full value for low receipts
        
        # Efficiency adjustment for single-day trips (reduced bonuses)
        if miles_per_day > 600:  # Extremely high travel day
            efficiency_bonus = 40  # Reduced bonus
        elif miles_per_day > 300:  # High travel day
            efficiency_bonus = 20  # Reduced bonus
        else:
            efficiency_bonus = 0  # No bonus for local trips
            
        return round(base_single_day + receipt_component + efficiency_bonus, 2)
    
    # Edge Case 1: Very low receipts (refined threshold and handling)
    # Now only applies to multi-day trips with genuinely low receipts
    if total_receipts_amount < 40 and trip_duration_days > 1:  # Lowered threshold, excluded single-day
        base_reimbursement = 100 + (trip_duration_days * 20)  # Scale with trip length
        receipt_bonus = total_receipts_amount * 0.4  # Slightly higher receipt factor
        return round(base_reimbursement + receipt_bonus, 2)
    
    # Edge Case 2: Long-distance business trips (reduced multipliers)
    # PRIORITY 2.1: Calibrated receipt scaling to reduce overestimation
    if trip_duration_days >= 5 and miles_traveled >= 800:
        base = 150 + (trip_duration_days * 35)  # Reduced base rates
        mileage_component = miles_traveled * 0.45  # Reduced from 0.8
        receipt_component = total_receipts_amount * 0.4  # Reduced from 0.6
        return round(base + mileage_component + receipt_component, 2)
    
    # Edge Case 3: Travel day scenarios (smoothed threshold transition)
    # PRIORITY 2.2: Smooth efficiency threshold transitions
    if miles_per_day > 250:  # Lowered and smoothed threshold
        # Gradual transition instead of sharp cutoff
        travel_intensity = min((miles_per_day - 250) / 100, 1.0)  # 0-1 scale over 100 miles/day
        
        if total_receipts_amount > 800:  # Raised threshold
            base_rate = 0.7 + (travel_intensity * 0.1)  # 0.7-0.8 range
            return round(total_receipts_amount * base_rate, 2)
        else:
            base_rate = 1.1 + (travel_intensity * 0.2)  # 1.1-1.3 range instead of 1.5
            minimum_reimbursement = 250 + (travel_intensity * 100)  # 250-350 range
            return round(max(total_receipts_amount * base_rate, minimum_reimbursement), 2)
    
    # Edge Case 4: Extended business trips (heavily reduced multipliers)
    # PRIORITY 2.1: Calibrated receipt scaling - Further reduced based on test results
    if trip_duration_days >= 8 and 50 <= miles_per_day <= 200:  # Expanded range
        # Apply same aggressive receipt capping as default case for high amounts
        receipts_per_day = total_receipts_amount / trip_duration_days
        if receipts_per_day > 300:
            receipt_factor = 0.25  # Heavy capping for very high receipts
        else:
            receipt_factor = 0.6   # Moderate receipt factor
        return round(total_receipts_amount * receipt_factor + (trip_duration_days * 40), 2)  # Further reduced
    
    # Edge Case 5: 5-day trips (refined thresholds)
    # PRIORITY 3.2: Refined edge case thresholds
    if 4.5 <= trip_duration_days <= 5.5:  # Smoothed range
        if miles_per_day < 60:  # Adjusted threshold
            return round(total_receipts_amount * 0.8, 2)  # Increased from 0.7
        else:
            return round(total_receipts_amount * 1.0 + (miles_traveled * 0.3), 2)  # Reduced multipliers
    
    # Default: Refined receipt dominance model with aggressive high-receipt capping
    # PRIORITY 1.1: Fix negative reimbursement bug with bounded efficiency penalty
    base_rate = max(80 - (trip_duration_days - 1) * 8, 40)  # Slightly reduced base rates
    
    # CRITICAL: Implement aggressive receipt capping for high amounts
    # Analysis shows legacy system heavily caps receipts above certain thresholds
    receipts_per_day = total_receipts_amount / trip_duration_days
    
    if receipts_per_day > 400:  # Very high daily receipts
        # Heavy capping - appears legacy system doesn't trust high receipt amounts
        receipt_factor = 0.15  # Only 15% of receipts above $400/day
        capped_amount = (400 * trip_duration_days) + ((total_receipts_amount - (400 * trip_duration_days)) * receipt_factor)
        receipt_component = capped_amount * 0.8  # Further reduction
    elif receipts_per_day > 200:  # High daily receipts  
        # Moderate capping for medium-high receipts
        receipt_factor = 0.4  # 40% of receipts above $200/day
        capped_amount = (200 * trip_duration_days) + ((total_receipts_amount - (200 * trip_duration_days)) * receipt_factor)
        receipt_component = capped_amount * 0.9
    elif receipts_per_day > 100:  # Medium daily receipts
        # Light capping for medium receipts
        receipt_component = total_receipts_amount * 0.7
    else:
        # Low receipts get full value
        receipt_component = total_receipts_amount * 0.95
    
    # PRIORITY 3.1: Implement bounded efficiency penalty
    if miles_per_day > 50:  # Only penalize genuinely inefficient trips
        raw_penalty = (miles_per_day - 50) * 1.5  # Reduced penalty rate
        # Bound penalty to maximum of 30% of total pre-penalty amount
        max_penalty = (base_rate + receipt_component) * 0.3
        efficiency_penalty = -min(raw_penalty, max_penalty)
    else:
        efficiency_penalty = 0  # No penalty for reasonable efficiency
    
    total_reimbursement = base_rate + receipt_component + efficiency_penalty
    
    # Final safety check to prevent negative values
    total_reimbursement = max(total_reimbursement, 20.0)  # Absolute minimum floor
    
    return round(total_reimbursement, 2)

def main():
    """Main function to handle command-line arguments and execute calculation."""
    parser = argparse.ArgumentParser(
        description='Calculate reimbursement amount for business trips',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 calculate_reimbursement.py 3 150 275.50
  python3 calculate_reimbursement.py 1 0 45.25
        """
    )
    
    parser.add_argument('trip_duration_days', type=float,
                        help='Number of days for the trip')
    parser.add_argument('miles_traveled', type=float,
                        help='Total miles traveled')
    parser.add_argument('total_receipts_amount', type=float,
                        help='Total amount from receipts')
    
    try:
        args = parser.parse_args()
        
        # Validate inputs
        is_valid, error_message = validate_inputs(
            args.trip_duration_days, 
            args.miles_traveled, 
            args.total_receipts_amount
        )
        
        if not is_valid:
            print(f"Error: {error_message}", file=sys.stderr)
            sys.exit(1)
        
        # Calculate reimbursement
        reimbursement = calculate_reimbursement(
            args.trip_duration_days,
            args.miles_traveled, 
            args.total_receipts_amount
        )
        
        # Output the result (single number as required)
        print(f"{reimbursement:.2f}")
        
    except ValueError as e:
        print(f"Error: Invalid input - {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Check if we should run analysis mode
    if len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        print("=== REIMBURSEMENT SYSTEM DATA ANALYSIS ===\n")
        
        try:
            results = perform_comprehensive_analysis()
            
            print("\n=== ANALYSIS RESULTS ===\n")
            
            # Basic Statistics
            print("📊 BASIC STATISTICS:")
            basic_stats = results['basic_statistics']
            for param, stats in basic_stats.items():
                print(f"  {param}:")
                print(f"    Count: {stats['count']}")
                print(f"    Range: ${stats['min']:.2f} - ${stats['max']:.2f}")
                print(f"    Average: ${stats['average']:.2f}")
            
            # Correlations
            print("\n🔗 CORRELATIONS WITH REIMBURSEMENT:")
            correlations = results['correlations']
            for correlation, value in correlations.items():
                strength = "Strong" if abs(value) > 0.7 else "Moderate" if abs(value) > 0.3 else "Weak"
                print(f"  {correlation.replace('_', ' ').title()}: {value:.3f} ({strength})")
            
            # Trip Length Analysis
            print("\n📅 TRIP LENGTH ANALYSIS:")
            trip_analysis = results['trip_length_analysis']
            sorted_durations = sorted(trip_analysis['duration_groups'].items())
            
            print("  Average reimbursement per day by trip length:")
            for duration, data in sorted_durations[:10]:  # Show first 10
                print(f"    {duration} days: ${data['avg_per_day']:.2f}/day ({data['count']} trips)")
            
            # Check 5-day sweet spot
            if 5.0 in trip_analysis['duration_groups']:
                five_day_data = trip_analysis['duration_groups'][5.0]
                print(f"\n  📍 5-DAY ANALYSIS (Sweet Spot Check):")
                print(f"    Count: {five_day_data['count']} trips")
                print(f"    Average per day: ${five_day_data['avg_per_day']:.2f}")
                print(f"    Range: ${five_day_data['min']:.2f} - ${five_day_data['max']:.2f}")
            
            # Mileage Efficiency Analysis
            print("\n🚗 MILEAGE EFFICIENCY ANALYSIS:")
            mileage_analysis = results['mileage_analysis']
            efficiency_ranges = mileage_analysis['efficiency_ranges']
            
            print("  Reimbursement by miles-per-day efficiency:")
            for range_name, data in efficiency_ranges.items():
                if data['count'] > 0:
                    range_str = f"{data['range'][0]}-{data['range'][1] if data['range'][1] != float('inf') else '∞'}"
                    print(f"    {range_name} ({range_str} mi/day): ${data['avg_reimbursement']:.2f} avg, ${data['avg_per_mile_rate']:.3f}/mile ({data['count']} trips)")
            
            # Sweet spot validation
            sweet_spot_data = efficiency_ranges.get('sweet_spot', {})
            if sweet_spot_data.get('count', 0) > 0:
                print(f"\n  📍 180-220 MILE/DAY SWEET SPOT:")
                print(f"    Count: {sweet_spot_data['count']} trips")
                print(f"    Average reimbursement: ${sweet_spot_data['avg_reimbursement']:.2f}")
                print(f"    Average per-mile rate: ${sweet_spot_data['avg_per_mile_rate']:.3f}")
            
            # Receipt Analysis
            print("\n🧾 RECEIPT PATTERNS ANALYSIS:")
            receipt_analysis = results['receipt_analysis']
            
            for category, ranges in receipt_analysis['by_trip_category'].items():
                print(f"  {category.title()} trips:")
                for range_name, data in ranges.items():
                    if data['count'] > 0:
                        print(f"    {range_name}: {data['count']} trips, ${data['avg_reimbursement']:.2f} avg reimbursement")
            
            # Pattern Consistency
            print("\n🔍 CALCULATION CONSISTENCY:")
            patterns = results['calculation_patterns']
            print(f"  Total similar trip groups found: {patterns['total_similar_groups']}")
            print(f"  Consistent groups (≤5% variance): {len(patterns['consistent_groups'])}")
            print(f"  Inconsistent groups (>5% variance): {len(patterns['inconsistent_groups'])}")
            
            if patterns['inconsistent_groups']:
                print("\n  Examples of inconsistent reimbursements:")
                count = 0
                for key, data in patterns['inconsistent_groups'].items():
                    if count >= 3:  # Show only first 3 examples
                        break
                    duration, miles, receipts = key
                    print(f"    {duration} days, ~{miles} miles, ~${receipts} receipts: ${data['variance']:.2f} variance ({data['variance_percent']:.1f}%)")
                    count += 1
            
            print(f"\n✅ Analysis complete! Analyzed {results['total_cases_analyzed']} test cases.")
            print("\nKey findings:")
            print("1. Check correlation strengths to identify primary factors")
            print("2. Look for efficiency sweet spots in mileage analysis")
            print("3. Examine trip length patterns for duration bonuses")
            print("4. Review inconsistent groups for calculation complexity")
            
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            sys.exit(1)
    else:
        # Regular calculation mode
        main() 