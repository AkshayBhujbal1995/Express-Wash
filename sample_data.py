"""
Sample Data Generator for Express Wash Laundry Billing System
This script creates realistic sample data for testing the application.
"""

import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import random

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '16021995',
    'database': 'express_wash'
}

def create_sample_data():
    """Generate and insert sample data into the database"""
    
    # Connect to database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Sample customer names
    customers = [
        "Rahul Sharma", "Priya Patel", "Amit Kumar", "Neha Singh", "Rajesh Verma",
        "Sita Devi", "Mohan Das", "Anjali Gupta", "Vikram Malhotra", "Pooja Reddy",
        "Sanjay Joshi", "Kavita Iyer", "Deepak Mehta", "Sunita Rao", "Arun Khanna",
        "Meera Nair", "Suresh Menon", "Lakshmi Pillai", "Ganesh Krishnan", "Radha Venkat"
    ]
    
    # Sample mobile numbers
    mobile_numbers = [
        "9876543210", "8765432109", "7654321098", "6543210987", "5432109876",
        "9876543211", "8765432110", "7654321109", "6543211098", "5432109877",
        "9876543212", "8765432111", "7654321110", "6543211109", "5432109878",
        "9876543213", "8765432112", "7654321111", "6543211110", "5432109879"
    ]
    
    # Generate orders for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    sample_orders = []
    
    for i in range(50):  # Generate 50 sample orders
        # Random date within the last 30 days
        random_days = random.randint(0, 30)
        order_date = start_date + timedelta(days=random_days)
        
        # Random customer
        customer_idx = random.randint(0, len(customers) - 1)
        customer_name = customers[customer_idx]
        mobile_number = mobile_numbers[customer_idx]
        
        # Random service quantities
        regular_kg = round(random.uniform(0, 5), 1)  # 0-5 kg
        blankets_kg = round(random.uniform(0, 3), 1)  # 0-3 kg
        white_pieces = random.randint(0, 10)  # 0-10 pieces
        
        # Calculate total amount
        pricing = {
            'regular_clothes': 50,
            'blankets': 100,
            'white_clothes': 40
        }
        
        total_amount = (regular_kg * pricing['regular_clothes'] + 
                       blankets_kg * pricing['blankets'] + 
                       white_pieces * pricing['white_clothes'])
        
        # Create order record
        order = {
            'customer_name': customer_name,
            'mobile_number': mobile_number,
            'order_date': order_date.strftime('%Y-%m-%d'),
            'regular_clothes_kg': regular_kg,
            'blankets_kg': blankets_kg,
            'white_clothes_pieces': white_pieces,
            'total_amount': total_amount,
            'created_at': order_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        sample_orders.append(order)
    
    # Insert sample data
    for order in sample_orders:
        cursor.execute('''
            INSERT INTO orders (customer_name, mobile_number, order_date, 
                               regular_clothes_kg, blankets_kg, white_clothes_pieces, 
                               total_amount, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            order['customer_name'],
            order['mobile_number'],
            order['order_date'],
            order['regular_clothes_kg'],
            order['blankets_kg'],
            order['white_clothes_pieces'],
            order['total_amount'],
            order['created_at']
        ))
    
    # Commit changes
    conn.commit()
    
    # Create CSV backup
    df = pd.read_sql_query('SELECT * FROM orders ORDER BY created_at DESC', conn)
    df.to_csv('orders.csv', index=False)
    
    conn.close()
    
    print("✅ Sample data generated successfully!")
    print(f"📊 Created {len(sample_orders)} sample orders")
    print(f"👥 Used {len(set([order['customer_name'] for order in sample_orders]))} unique customers")
    print(f"💰 Total revenue: ₹{sum([order['total_amount'] for order in sample_orders]):,.2f}")
    print(f"📅 Date range: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
    print("\n🎯 You can now run 'streamlit run app.py' to see the sample data!")

def clear_sample_data():
    """Clear all data from the database"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM orders')
    conn.commit()
    conn.close()
    
    print("🗑️ All sample data cleared from database!")

if __name__ == "__main__":
    print("🧺 Express Wash - Sample Data Generator")
    print("=" * 50)
    
    choice = input("Choose an option:\n1. Generate sample data\n2. Clear all data\nEnter choice (1 or 2): ")
    
    if choice == "1":
        create_sample_data()
    elif choice == "2":
        clear_sample_data()
    else:
        print("❌ Invalid choice. Please run the script again.") 