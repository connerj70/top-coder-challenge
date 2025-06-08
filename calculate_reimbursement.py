#!/usr/bin/env python3
"""
Reimbursement Calculation Script
This script uses a pre-trained, multi-model architecture to predict reimbursement amounts.
"""

import sys
import argparse
import joblib
import numpy as np

# Load the trained models
try:
    model_per_diem = joblib.load('model_per_diem_trips.joblib')
    model_receipt_driven = joblib.load('model_receipt-driven_trips.joblib')
    model_standard = joblib.load('model_standard_trips.joblib')
except FileNotFoundError as e:
    print(f"Error: A required model file was not found. Please run analysis.py to train all models. Missing file: {e.filename}", file=sys.stderr)
    sys.exit(1)

def create_features(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Creates an expanded feature vector from the raw inputs for the model.
    This must match the feature creation in analysis.py exactly.
    """
    # Base features
    features = [
        trip_duration_days,
        miles_traveled,
        total_receipts_amount,
    ]
    
    # Derived features
    miles_per_day = miles_traveled / trip_duration_days if trip_duration_days > 0 else 0
    receipts_per_day = total_receipts_amount / trip_duration_days if trip_duration_days > 0 else 0
    receipt_per_mile = total_receipts_amount / miles_traveled if miles_traveled > 0 else 0

    features.extend([
        miles_per_day,
        receipts_per_day,
        receipt_per_mile,
        trip_duration_days ** 2,
        miles_traveled ** 2,
        total_receipts_amount ** 2,
        # Interaction features inspired by interview analysis
        trip_duration_days * miles_per_day,
        receipts_per_day * miles_traveled,
        trip_duration_days * total_receipts_amount,
        miles_traveled * total_receipts_amount,
        miles_per_day * receipts_per_day
    ])
    
    return features

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Classifies the trip and uses the appropriate specialist model to predict reimbursement.
    """
    # Create the feature vector
    features = create_features(trip_duration_days, miles_traveled, total_receipts_amount)
    features_array = np.array(features).reshape(1, -1)
    
    # Classify the trip to select the correct model
    is_per_diem_trip = (trip_duration_days >= 7 and total_receipts_amount < (trip_duration_days * 50))
    is_receipt_driven_trip = (trip_duration_days <= 3 and total_receipts_amount > (trip_duration_days * 150))

    if is_per_diem_trip:
        model = model_per_diem
    elif is_receipt_driven_trip:
        model = model_receipt_driven
    else:
        model = model_standard
        
    # Predict the reimbursement
    prediction = model.predict(features_array)
    
    return round(prediction[0], 2)

def validate_inputs(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Validate input parameters to ensure they are valid for reimbursement calculation.
    """
    if trip_duration_days < 0:
        return False, "Trip duration cannot be negative"
    
    if miles_traveled < 0:
        return False, "Miles traveled cannot be negative"
    
    if total_receipts_amount < 0:
        return False, "Total receipts amount cannot be negative"
    
    return True, ""

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
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 