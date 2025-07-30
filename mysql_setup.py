#!/usr/bin/env python3
"""
MySQL Setup Script for Express Wash Laundry Billing System
This script initializes the MySQL database and creates the required tables.
"""

import mysql.connector
from mysql.connector import Error
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '16021995',
    'database': 'express_wash'
}

def test_connection():
    """Test MySQL connection"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        print("✅ MySQL connection successful!")
        conn.close()
        return True
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def create_database():
    """Create the express_wash database"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"✅ Database '{DB_CONFIG['database']}' created/verified successfully!")
        
        conn.close()
        return True
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create the orders table"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create orders table
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(255) NOT NULL,
                mobile_number VARCHAR(20),
                order_date DATE NOT NULL,
                regular_clothes_kg DECIMAL(5,2) DEFAULT 0,
                blankets_kg DECIMAL(5,2) DEFAULT 0,
                white_clothes_pieces INT DEFAULT 0,
                total_amount DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        
        cursor.execute(create_table_query)
        print("✅ Orders table created/verified successfully!")
        
        # Show table structure
        cursor.execute("DESCRIBE orders")
        print("\n📋 Table Structure:")
        print("-" * 80)
        for row in cursor.fetchall():
            print(f"{str(row[0]):<20} {str(row[1]):<20} {str(row[2]):<10} {str(row[3]):<10} {str(row[4]):<10}")
        
        conn.close()
        return True
    except Error as e:
        print(f"❌ Error creating table: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Sample data
        sample_orders = [
            ("Rahul Sharma", "9876543210", "2024-01-15", 2.5, 0.0, 3, 225.00),
            ("Priya Patel", "8765432109", "2024-01-16", 1.0, 1.5, 0, 200.00),
            ("Amit Kumar", "7654321098", "2024-01-17", 3.0, 0.0, 5, 350.00),
            ("Neha Singh", "6543210987", "2024-01-18", 0.0, 2.0, 2, 280.00),
            ("Rajesh Verma", "5432109876", "2024-01-19", 1.5, 0.5, 1, 135.00)
        ]
        
        insert_query = '''
            INSERT INTO orders (customer_name, mobile_number, order_date, 
                               regular_clothes_kg, blankets_kg, white_clothes_pieces, total_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        
        cursor.executemany(insert_query, sample_orders)
        conn.commit()
        
        print(f"✅ Inserted {len(sample_orders)} sample orders successfully!")
        
        # Show sample data
        cursor.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT 5")
        print("\n📊 Sample Data:")
        print("-" * 80)
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Customer: {row[1]}, Amount: ₹{row[7]}, Date: {row[3]}")
        
        conn.close()
        return True
    except Error as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("🧺 Express Wash - MySQL Database Setup")
    print("=" * 50)
    
    # Test connection
    if not test_connection():
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Verify username and password")
        print("3. Check if MySQL is accessible on localhost")
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        sys.exit(1)
    
    # Ask if user wants sample data
    choice = input("\n🎯 Would you like to insert sample data for testing? (y/n): ").lower()
    if choice in ['y', 'yes']:
        insert_sample_data()
    
    print("\n🎉 MySQL setup completed successfully!")
    print("\n🚀 You can now run the Express Wash application:")
    print("   streamlit run app.py")
    print("\n📖 The application will use MySQL database instead of SQLite.")

if __name__ == "__main__":
    main() 