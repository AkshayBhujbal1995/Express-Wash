#!/bin/bash

echo "🧺 Express Wash - Laundry Billing System"
echo "========================================"
echo ""
echo "Starting the application..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Please run: pip install -r requirements.txt"
    exit 1
fi

# Run the application
streamlit run app.py 