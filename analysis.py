import json
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
import joblib

def create_features(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Creates an expanded feature vector from the raw inputs for the model.
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

def train_and_tune_model(X_train, y_train, model_name):
    """
    Performs GridSearchCV to find the best model for a given dataset.
    """
    print(f"\\n--- Tuning model for: {model_name} ---")
    param_grid = {
        'n_estimators': [500, 700],
        'learning_rate': [0.01, 0.05],
        'max_depth': [4, 5],
        'min_samples_split': [4],
        'loss': ['huber']
    }
    gbr = GradientBoostingRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=gbr, param_grid=param_grid, 
                               cv=3, n_jobs=-1, verbose=1, scoring='neg_mean_squared_error')
    
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters for {model_name}: {grid_search.best_params_}")
    best_model = grid_search.best_estimator_
    
    # Save the best model
    model_filename = f"model_{model_name.lower().replace(' ', '_')}.joblib"
    joblib.dump(best_model, model_filename)
    print(f"Saved best model to {model_filename}")

def train_multi_model():
    """
    Categorizes trips and trains a separate, tuned model for each category.
    """
    print("Loading public cases for training...")
    try:
        with open('public_cases.json', 'r') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print("Error: public_cases.json not found.")
        return

    # Prepare datasets for each model
    datasets = {
        "Per Diem Trips": {'X': [], 'y': []},
        "Receipt-Driven Trips": {'X': [], 'y': []},
        "Standard Trips": {'X': [], 'y': []}
    }

    print("Creating feature sets and categorizing trips...")
    for case in test_cases:
        inputs = case['input']
        trip_duration_days = inputs['trip_duration_days']
        miles_traveled = inputs['miles_traveled']
        total_receipts_amount = inputs['total_receipts_amount']
        
        features = create_features(
            trip_duration_days,
            miles_traveled,
            total_receipts_amount
        )
        
        is_per_diem_trip = (trip_duration_days >= 7 and total_receipts_amount < (trip_duration_days * 50))
        is_receipt_driven_trip = (trip_duration_days <= 3 and total_receipts_amount > (trip_duration_days * 150))

        if is_per_diem_trip:
            datasets["Per Diem Trips"]['X'].append(features)
            datasets["Per Diem Trips"]['y'].append(case['expected_output'])
        elif is_receipt_driven_trip:
            datasets["Receipt-Driven Trips"]['X'].append(features)
            datasets["Receipt-Driven Trips"]['y'].append(case['expected_output'])
        else:
            datasets["Standard Trips"]['X'].append(features)
            datasets["Standard Trips"]['y'].append(case['expected_output'])

    # Train a model for each category
    for model_name, data in datasets.items():
        if data['X']:
            train_and_tune_model(data['X'], data['y'], model_name)
    
    print("\\nMulti-model training complete.")

if __name__ == "__main__":
    train_multi_model() 