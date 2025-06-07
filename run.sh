#!/bin/bash

# Black Box Challenge - Reimbursement Calculation Implementation
# This script takes three parameters and outputs the reimbursement amount
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Check if the correct number of arguments is provided
if [ $# -ne 3 ]; then
    echo "Error: This script requires exactly 3 arguments" >&2
    echo "Usage: $0 <trip_duration_days> <miles_traveled> <total_receipts_amount>" >&2
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not available" >&2
    exit 1
fi

# Check if the Python script exists
if [ ! -f "calculate_reimbursement.py" ]; then
    echo "Error: calculate_reimbursement.py not found" >&2
    exit 1
fi

# Execute the Python script with the provided arguments
python3 calculate_reimbursement.py "$1" "$2" "$3" 