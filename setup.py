#!/usr/bin/env python3
"""
Setup script for Express Wash Laundry Billing System
Automates the installation and initial setup process.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_database():
    """Initialize the database"""
    print("\n🗄️ Initializing database...")
    try:
        import sqlite3
        conn = sqlite3.connect('express_wash.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                mobile_number TEXT,
                order_date DATE NOT NULL,
                regular_clothes_kg REAL DEFAULT 0,
                blankets_kg REAL DEFAULT 0,
                white_clothes_pieces INTEGER DEFAULT 0,
                total_amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def generate_sample_data():
    """Ask user if they want to generate sample data"""
    print("\n🎯 Sample Data Generation")
    choice = input("Would you like to generate sample data for testing? (y/n): ").lower()
    
    if choice in ['y', 'yes']:
        try:
            from sample_data import create_sample_data
            create_sample_data()
            return True
        except Exception as e:
            print(f"❌ Error generating sample data: {e}")
            return False
    else:
        print("⏭️ Skipping sample data generation.")
        return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    try:
        # Create logs directory if needed
        Path("logs").mkdir(exist_ok=True)
        print("✅ Directories created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating directories: {e}")
        return False

def test_installation():
    """Test if the application can be imported"""
    print("\n🧪 Testing installation...")
    try:
        import streamlit
        import pandas
        import plotly
        import sqlite3
        print("✅ All packages imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🧺 Express Wash - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Initialize database
    if not create_database():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    # Generate sample data
    generate_sample_data()
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To start the application, run:")
    print("   streamlit run app.py")
    print("\n📖 For more information, see README.md")
    print("\n🎯 Happy laundering! 🧺")

if __name__ == "__main__":
    main() 