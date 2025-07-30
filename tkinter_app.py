#!/usr/bin/env python3
"""
Express Wash - Professional Tkinter Desktop Application
Modern GUI with CRUD operations, beautiful styling, and professional design
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import pandas as pd
from datetime import datetime, date
import json
import os
from PIL import Image, ImageTk
import threading

class ExpressWashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧺 Express Wash - Smart Laundry Billing System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # Database configuration
        self.DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': '16021995',
            'database': 'express_wash'
        }
        
        # Pricing configuration
        self.PRICING = {
            'regular_clothes': 50,  # ₹50/kg
            'blankets': 100,        # ₹100/kg
            'white_clothes': 40     # ₹40/piece
        }
        
        # Initialize database
        self.init_database()
        
        # Create main interface
        self.create_widgets()
        
        # Load initial data
        self.load_orders()
        
    def init_database(self):
        """Initialize MySQL database connection"""
        try:
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor()
            # Add receipt_number column if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    receipt_number VARCHAR(32) UNIQUE,
                    customer_name VARCHAR(255) NOT NULL,
                    mobile_number VARCHAR(20),
                    order_date DATE NOT NULL,
                    regular_clothes_kg DECIMAL(5,2) DEFAULT 0,
                    blankets_kg DECIMAL(5,2) DEFAULT 0,
                    white_clothes_pieces INT DEFAULT 0,
                    total_amount DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Add receipt_number column if upgrading
            try:
                cursor.execute('ALTER TABLE orders ADD COLUMN receipt_number VARCHAR(32) UNIQUE')
            except Exception:
                pass
            conn.commit()
            conn.close()
            print("✅ Database initialized successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#1e3a8a', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🧺 Express Wash", 
                              font=('Arial', 24, 'bold'), 
                              fg='white', bg='#1e3a8a')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(title_frame, text="Smart Laundry Billing System", 
                                 font=('Arial', 12), 
                                 fg='#e5e7eb', bg='#1e3a8a')
        subtitle_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f8ff')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Order Form
        self.create_order_form(main_container)
        
        # Right panel - Order History
        self.create_order_history(main_container)
        
    def create_order_form(self, parent):
        """Create the order form panel"""
        form_frame = tk.LabelFrame(parent, text="📝 New Order", 
                                  font=('Arial', 14, 'bold'),
                                  bg='white', fg='#1e3a8a',
                                  padx=15, pady=15)
        form_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Customer Information
        customer_frame = tk.LabelFrame(form_frame, text="👤 Customer Information", 
                                      font=('Arial', 12, 'bold'),
                                      bg='white', fg='#374151')
        customer_frame.pack(fill='x', pady=(0, 15))
        
        # Customer Name
        tk.Label(customer_frame, text="Customer Name *:", 
                font=('Arial', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.customer_name_var = tk.StringVar()
        self.customer_name_entry = tk.Entry(customer_frame, textvariable=self.customer_name_var,
                                           font=('Arial', 10), width=25)
        self.customer_name_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')
        
        # Mobile Number
        tk.Label(customer_frame, text="Mobile Number:", 
                font=('Arial', 10, 'bold'), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.mobile_var = tk.StringVar()
        self.mobile_entry = tk.Entry(customer_frame, textvariable=self.mobile_var,
                                    font=('Arial', 10), width=25)
        self.mobile_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')
        
        # Order Date
        tk.Label(customer_frame, text="Order Date *:", 
                font=('Arial', 10, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.order_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        self.order_date_entry = tk.Entry(customer_frame, textvariable=self.order_date_var,
                                        font=('Arial', 10), width=25)
        self.order_date_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')
        
        # Service Details
        service_frame = tk.LabelFrame(form_frame, text="🧺 Service Details", 
                                     font=('Arial', 12, 'bold'),
                                     bg='white', fg='#374151')
        service_frame.pack(fill='x', pady=(0, 15))
        
        # Regular Clothes
        tk.Label(service_frame, text="Regular Clothes (₹50/kg):", 
                font=('Arial', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.regular_kg_var = tk.DoubleVar(value=0.0)
        self.regular_kg_entry = tk.Entry(service_frame, textvariable=self.regular_kg_var,
                                        font=('Arial', 10), width=15)
        self.regular_kg_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')
        tk.Label(service_frame, text="kg", bg='white').grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Blankets
        tk.Label(service_frame, text="Blankets/Bedsheets (₹100/kg):", 
                font=('Arial', 10, 'bold'), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.blankets_kg_var = tk.DoubleVar(value=0.0)
        self.blankets_kg_entry = tk.Entry(service_frame, textvariable=self.blankets_kg_var,
                                         font=('Arial', 10), width=15)
        self.blankets_kg_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')
        tk.Label(service_frame, text="kg", bg='white').grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # White Clothes
        tk.Label(service_frame, text="White Clothes (₹40/piece):", 
                font=('Arial', 10, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        self.white_pieces_var = tk.IntVar(value=0)
        self.white_pieces_entry = tk.Entry(service_frame, textvariable=self.white_pieces_var,
                                          font=('Arial', 10), width=15)
        self.white_pieces_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')
        tk.Label(service_frame, text="pieces", bg='white').grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Bill Summary
        self.bill_frame = tk.LabelFrame(form_frame, text="💰 Bill Summary", 
                                       font=('Arial', 12, 'bold'),
                                       bg='white', fg='#059669')
        self.bill_frame.pack(fill='x', pady=(0, 15))
        
        self.bill_text = tk.Text(self.bill_frame, height=6, width=40, 
                                font=('Arial', 10), bg='#f0fdf4', fg='#065f46')
        self.bill_text.pack(padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=(0, 10))
        
        # Calculate Button
        self.calc_button = tk.Button(button_frame, text="🧮 Calculate Bill", 
                                    command=self.calculate_bill,
                                    font=('Arial', 11, 'bold'),
                                    bg='#3b82f6', fg='white',
                                    relief='raised', bd=2,
                                    padx=20, pady=8)
        self.calc_button.pack(side='left', padx=(0, 10))
        
        # Save Button
        self.save_button = tk.Button(button_frame, text="💾 Save Order", 
                                    command=self.save_order,
                                    font=('Arial', 11, 'bold'),
                                    bg='#10b981', fg='white',
                                    relief='raised', bd=2,
                                    padx=20, pady=8)
        self.save_button.pack(side='left', padx=(0, 10))
        
        # Clear Button
        self.clear_button = tk.Button(button_frame, text="🗑️ Clear Form", 
                                     command=self.clear_form,
                                     font=('Arial', 11, 'bold'),
                                     bg='#ef4444', fg='white',
                                     relief='raised', bd=2,
                                     padx=20, pady=8)
        self.clear_button.pack(side='left')
        
    def create_order_history(self, parent):
        """Create the order history panel"""
        history_frame = tk.LabelFrame(parent, text="📊 Order History", 
                                     font=('Arial', 14, 'bold'),
                                     bg='white', fg='#1e3a8a',
                                     padx=15, pady=15)
        history_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Search and Filter
        search_frame = tk.Frame(history_frame, bg='white')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=('Arial', 10, 'bold'), bg='white').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                    font=('Arial', 10), width=20)
        self.search_entry.pack(side='left', padx=(5, 10))
        self.search_var.trace('w', self.filter_orders)
        
        # CRUD Buttons
        crud_frame = tk.Frame(history_frame, bg='white')
        crud_frame.pack(fill='x', pady=(0, 10))
        
        self.edit_button = tk.Button(crud_frame, text="✏️ Edit", 
                                    command=self.edit_order,
                                    font=('Arial', 10, 'bold'),
                                    bg='#f59e0b', fg='white',
                                    relief='raised', bd=2,
                                    padx=15, pady=5)
        self.edit_button.pack(side='left', padx=(0, 5))
        
        self.delete_button = tk.Button(crud_frame, text="🗑️ Delete", 
                                      command=self.delete_order,
                                      font=('Arial', 10, 'bold'),
                                      bg='#ef4444', fg='white',
                                      relief='raised', bd=2,
                                      padx=15, pady=5)
        self.delete_button.pack(side='left', padx=(0, 5))
        
        self.refresh_button = tk.Button(crud_frame, text="🔄 Refresh", 
                                       command=self.load_orders,
                                       font=('Arial', 10, 'bold'),
                                       bg='#3b82f6', fg='white',
                                       relief='raised', bd=2,
                                       padx=15, pady=5)
        self.refresh_button.pack(side='left', padx=(0, 5))
        
        self.export_button = tk.Button(crud_frame, text="📥 Export", 
                                      command=self.export_data,
                                      font=('Arial', 10, 'bold'),
                                      bg='#8b5cf6', fg='white',
                                      relief='raised', bd=2,
                                      padx=15, pady=5)
        self.export_button.pack(side='left')
        
        # Treeview for orders
        tree_frame = tk.Frame(history_frame, bg='white')
        tree_frame.pack(fill='both', expand=True)
        
        # Create Treeview
        columns = ('ID', 'Customer', 'Mobile', 'Date', 'Regular', 'Blankets', 'White', 'Total', 'Created')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Customer', text='Customer Name')
        self.tree.heading('Mobile', text='Mobile')
        self.tree.heading('Date', text='Order Date')
        self.tree.heading('Regular', text='Regular (kg)')
        self.tree.heading('Blankets', text='Blankets (kg)')
        self.tree.heading('White', text='White (pcs)')
        self.tree.heading('Total', text='Total (₹)')
        self.tree.heading('Created', text='Created At')
        
        # Define columns
        self.tree.column('ID', width=50)
        self.tree.column('Customer', width=120)
        self.tree.column('Mobile', width=100)
        self.tree.column('Date', width=100)
        self.tree.column('Regular', width=80)
        self.tree.column('Blankets', width=80)
        self.tree.column('White', width=80)
        self.tree.column('Total', width=80)
        self.tree.column('Created', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
    def generate_receipt_number(self):
        """Generate a unique, sequential receipt number for today"""
        today_str = date.today().strftime('%Y%m%d')
        prefix = f"RW-{today_str}-"
        conn = mysql.connector.connect(**self.DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT receipt_number FROM orders WHERE receipt_number LIKE %s ORDER BY id DESC LIMIT 1", (prefix+'%',))
        last = cursor.fetchone()
        conn.close()
        if last and last[0]:
            last_num = int(last[0].split('-')[-1])
            next_num = last_num + 1
        else:
            next_num = 1
        return f"{prefix}{next_num:04d}"
    
    def calculate_bill(self):
        """Calculate and display bill"""
        try:
            regular_kg = self.regular_kg_var.get()
            blankets_kg = self.blankets_kg_var.get()
            white_pieces = self.white_pieces_var.get()
            regular_cost = regular_kg * self.PRICING['regular_clothes']
            blankets_cost = blankets_kg * self.PRICING['blankets']
            white_cost = white_pieces * self.PRICING['white_clothes']
            total = regular_cost + blankets_cost + white_cost
            self.bill_text.delete(1.0, tk.END)
            lines = ["🧺 Express Wash - Bill Summary\n"]
            # Only show nonzero services
            if regular_kg > 0:
                lines.append(f"Regular Clothes: {regular_kg}kg × ₹{self.PRICING['regular_clothes']} = ₹{regular_cost:.2f}")
            if blankets_kg > 0:
                lines.append(f"Blankets/Bedsheets: {blankets_kg}kg × ₹{self.PRICING['blankets']} = ₹{blankets_cost:.2f}")
            if white_pieces > 0:
                lines.append(f"White Clothes: {white_pieces} pieces × ₹{self.PRICING['white_clothes']} = ₹{white_cost:.2f}")
            lines.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            lines.append(f"💵 TOTAL AMOUNT: ₹{total:.2f}\n")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            self.bill_text.insert(1.0, '\n'.join(lines))
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating bill: {str(e)}")
    
    def save_order(self):
        """Save order to database"""
        try:
            customer_name = self.customer_name_var.get().strip()
            mobile_number = self.mobile_var.get().strip()
            order_date = self.order_date_var.get().strip()
            if not customer_name or not order_date:
                messagebox.showerror("Error", "Please fill in customer name and order date!")
                return
            regular_kg = self.regular_kg_var.get()
            blankets_kg = self.blankets_kg_var.get()
            white_pieces = self.white_pieces_var.get()
            total = (regular_kg * self.PRICING['regular_clothes'] + 
                    blankets_kg * self.PRICING['blankets'] + 
                    white_pieces * self.PRICING['white_clothes'])
            receipt_number = self.generate_receipt_number()
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO orders (receipt_number, customer_name, mobile_number, order_date, 
                                   regular_clothes_kg, blankets_kg, white_clothes_pieces, total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (receipt_number, customer_name, mobile_number, order_date, regular_kg, blankets_kg, white_pieces, total))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"✅ Order saved successfully!\nReceipt Number: {receipt_number}")
            self.clear_form()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving order: {str(e)}")
    
    def clear_form(self):
        """Clear the order form"""
        self.customer_name_var.set("")
        self.mobile_var.set("")
        self.order_date_var.set(date.today().strftime('%Y-%m-%d'))
        self.regular_kg_var.set(0.0)
        self.blankets_kg_var.set(0.0)
        self.white_pieces_var.set(0)
        self.bill_text.delete(1.0, tk.END)
    
    def load_orders(self):
        """Load orders from database"""
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute('SELECT id, receipt_number, customer_name, mobile_number, order_date, regular_clothes_kg, blankets_kg, white_clothes_pieces, total_amount, created_at FROM orders ORDER BY created_at DESC')
            orders = cursor.fetchall()
            for order in orders:
                self.tree.insert('', 'end', values=(
                    order[1],  # Receipt Number (shown instead of ID)
                    order[2],  # Customer Name
                    order[3] or "",  # Mobile
                    order[4],  # Order Date
                    f"{order[5]:.1f}",  # Regular kg
                    f"{order[6]:.1f}",  # Blankets kg
                    order[7],  # White pieces
                    f"₹{order[8]:.2f}",  # Total
                    order[9].strftime('%Y-%m-%d %H:%M') if order[9] else ""  # Created
                ))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading orders: {str(e)}")
    
    def filter_orders(self, *args):
        """Filter orders based on search term"""
        search_term = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            customer_name = values[1].lower() if values[1] else ""
            
            if search_term in customer_name:
                self.tree.reattach(item, '', 'end')
            else:
                self.tree.detach(item)
    
    def on_select(self, event):
        """Handle order selection"""
        selection = self.tree.selection()
        if selection:
            # Enable edit and delete buttons
            self.edit_button.config(state='normal')
            self.delete_button.config(state='normal')
        else:
            # Disable edit and delete buttons
            self.edit_button.config(state='disabled')
            self.delete_button.config(state='disabled')
    
    def edit_order(self):
        """Edit selected order"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order to edit!")
            return
        
        # Get selected order data
        item = self.tree.item(selection[0])
        values = item['values']
        
        # Create edit window
        self.create_edit_window(values)
    
    def create_edit_window(self, order_data):
        """Create edit order window"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("✏️ Edit Order")
        edit_window.geometry("500x600")
        edit_window.configure(bg='#f0f8ff')
        
        # Order ID
        order_id = order_data[0]
        
        # Create form similar to main form
        form_frame = tk.LabelFrame(edit_window, text="Edit Order Details", 
                                  font=('Arial', 12, 'bold'),
                                  bg='white', fg='#1e3a8a',
                                  padx=15, pady=15)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Customer Information
        tk.Label(form_frame, text="Customer Name:", font=('Arial', 10, 'bold'), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        customer_name_var = tk.StringVar(value=order_data[1])
        customer_name_entry = tk.Entry(form_frame, textvariable=customer_name_var, font=('Arial', 10), width=25)
        customer_name_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky='w')
        
        tk.Label(form_frame, text="Mobile Number:", font=('Arial', 10, 'bold'), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        mobile_var = tk.StringVar(value=order_data[2] or "")
        mobile_entry = tk.Entry(form_frame, textvariable=mobile_var, font=('Arial', 10), width=25)
        mobile_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky='w')
        
        tk.Label(form_frame, text="Order Date:", font=('Arial', 10, 'bold'), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        order_date_var = tk.StringVar(value=order_data[3])
        order_date_entry = tk.Entry(form_frame, textvariable=order_date_var, font=('Arial', 10), width=25)
        order_date_entry.grid(row=2, column=1, padx=(10, 0), pady=5, sticky='w')
        
        # Service Details
        tk.Label(form_frame, text="Regular Clothes (kg):", font=('Arial', 10, 'bold'), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        regular_kg_var = tk.DoubleVar(value=float(order_data[4]))
        regular_kg_entry = tk.Entry(form_frame, textvariable=regular_kg_var, font=('Arial', 10), width=15)
        regular_kg_entry.grid(row=3, column=1, padx=(10, 0), pady=5, sticky='w')
        
        tk.Label(form_frame, text="Blankets (kg):", font=('Arial', 10, 'bold'), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        blankets_kg_var = tk.DoubleVar(value=float(order_data[5]))
        blankets_kg_entry = tk.Entry(form_frame, textvariable=blankets_kg_var, font=('Arial', 10), width=15)
        blankets_kg_entry.grid(row=4, column=1, padx=(10, 0), pady=5, sticky='w')
        
        tk.Label(form_frame, text="White Clothes (pieces):", font=('Arial', 10, 'bold'), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        white_pieces_var = tk.IntVar(value=int(order_data[6]))
        white_pieces_entry = tk.Entry(form_frame, textvariable=white_pieces_var, font=('Arial', 10), width=15)
        white_pieces_entry.grid(row=5, column=1, padx=(10, 0), pady=5, sticky='w')
        
        # Update button
        def update_order():
            try:
                # Calculate new total
                total = (regular_kg_var.get() * self.PRICING['regular_clothes'] + 
                        blankets_kg_var.get() * self.PRICING['blankets'] + 
                        white_pieces_var.get() * self.PRICING['white_clothes'])
                
                # Update database
                conn = mysql.connector.connect(**self.DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE orders 
                    SET customer_name = %s, mobile_number = %s, order_date = %s,
                        regular_clothes_kg = %s, blankets_kg = %s, white_clothes_pieces = %s,
                        total_amount = %s
                    WHERE id = %s
                ''', (customer_name_var.get(), mobile_var.get(), order_date_var.get(),
                     regular_kg_var.get(), blankets_kg_var.get(), white_pieces_var.get(),
                     total, order_id))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "✅ Order updated successfully!")
                edit_window.destroy()
                self.load_orders()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error updating order: {str(e)}")
        
        update_button = tk.Button(form_frame, text="💾 Update Order", 
                                 command=update_order,
                                 font=('Arial', 11, 'bold'),
                                 bg='#10b981', fg='white',
                                 relief='raised', bd=2,
                                 padx=20, pady=8)
        update_button.grid(row=6, column=0, columnspan=2, pady=20)
    
    def delete_order(self):
        """Delete selected order"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order to delete!")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", 
                                   "Are you sure you want to delete this order?\nThis action cannot be undone!")
        if not result:
            return
        
        try:
            # Get order ID
            item = self.tree.item(selection[0])
            order_id = item['values'][0]
            
            # Delete from database
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "✅ Order deleted successfully!")
            self.load_orders()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting order: {str(e)}")
    
    def export_data(self):
        """Export data to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Orders to CSV"
            )
            
            if filename:
                conn = mysql.connector.connect(**self.DB_CONFIG)
                df = pd.read_sql_query('SELECT * FROM orders ORDER BY created_at DESC', conn)
                conn.close()
                
                df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"✅ Data exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting data: {str(e)}")

def main():
    """Main function"""
    root = tk.Tk()
    app = ExpressWashApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 