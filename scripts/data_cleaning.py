"""
Data Cleaning & Preprocessing Pipeline
Business Sales Performance Analytics (Future Interns - Task 1)
Author: Data Science & Analytics Team
"""

import os
import pandas as pd
import numpy as np

def clean_sales_data(raw_path='data/raw_superstore.csv', output_path='data/cleaned_superstore.csv'):
    print(f"[*] Loading raw dataset from: {raw_path}")
    
    # Load dataset with robust encoding
    encodings_to_try = ['latin1', 'windows-1252', 'utf-8']
    df = None
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(raw_path, encoding=enc)
            print(f"    Successfully loaded with encoding: {enc}")
            break
        except UnicodeDecodeError:
            continue
            
    if df is None:
        raise ValueError("Failed to load dataset with tested encodings.")

    initial_shape = df.shape
    print(f"[*] Initial Shape: {initial_shape[0]} rows, {initial_shape[1]} columns")

    # 1. Clean column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # 2. Handle missing critical rows (trailing empty rows)
    critical_cols = ['Order ID', 'Order Date', 'Sales', 'Profit']
    nulls_in_critical = df[critical_cols].isnull().any(axis=1).sum()
    print(f"[*] Rows missing critical sales info: {nulls_in_critical}")
    df = df.dropna(subset=critical_cols).copy()
    print(f"    Rows remaining after dropping empty sales records: {len(df)}")

    # 3. Handle duplicates
    dup_count = df.duplicated().sum()
    print(f"[*] Duplicate rows detected: {dup_count}")
    if dup_count > 0:
        df = df.drop_duplicates().copy()
        print(f"    Rows remaining after removing duplicates: {len(df)}")

    # 4. Clean and strip string fields
    string_cols = ['Customer Name', 'Segment', 'Country', 'City', 'State', 
                   'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name', 'Ship Mode']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 5. Handle Postal Code imputation
    # Postal Code for Burlington, Vermont is 05401
    if 'Postal Code' in df.columns:
        df.loc[(df['City'] == 'Burlington') & (df['State'] == 'Vermont') & (df['Postal Code'].isnull()), 'Postal Code'] = 5401.0
        # For any remaining missing postal codes, forward fill or mark 0
        df['Postal Code'] = df['Postal Code'].fillna(0).astype(int).astype(str).str.zfill(5)

    # 6. Parse and format Date fields
    print("[*] Parsing datetime fields...")
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', errors='coerce')

    # Validate shipping dates (Ship Date must not be earlier than Order Date)
    invalid_dates = df[df['Ship Date'] < df['Order Date']]
    if len(invalid_dates) > 0:
        print(f"    Warning: Found {len(invalid_dates)} records where Ship Date < Order Date. Adjusting to Order Date.")
        df.loc[df['Ship Date'] < df['Order Date'], 'Ship Date'] = df['Order Date']

    # 7. Convert Numeric Columns
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 8. Feature Engineering for Business Analytics
    print("[*] Engineering business analytics features...")
    df['Order_Year'] = df['Order Date'].dt.year
    df['Order_Month'] = df['Order Date'].dt.month
    df['Order_Month_Name'] = df['Order Date'].dt.strftime('%B')
    df['Order_Year_Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Order_Quarter'] = 'Q' + df['Order Date'].dt.quarter.astype(str)
    df['Order_Day_of_Week'] = df['Order Date'].dt.day_name()
    
    # Days to ship (Fulfillment cycle time)
    df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

    # Financial KPIs
    # Profit Margin (%)
    df['Profit_Margin'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)
    df['Profit_Margin'] = df['Profit_Margin'].round(2)

    # Unit Economics
    df['Unit_Price'] = np.where(df['Quantity'] > 0, (df['Sales'] / df['Quantity']), df['Sales']).round(2)
    df['Unit_Cost'] = np.where(df['Quantity'] > 0, ((df['Sales'] - df['Profit']) / df['Quantity']), 0).round(2)

    # Discount Percentage
    df['Discount_Percentage'] = (df['Discount'] * 100).round(1)

    # Discount Tier
    def categorize_discount(disc):
        if disc == 0:
            return 'No Discount (0%)'
        elif disc <= 0.15:
            return 'Low (1% - 15%)'
        elif disc <= 0.30:
            return 'Moderate (16% - 30%)'
        else:
            return 'Deep (> 30%)'

    df['Discount_Tier'] = df['Discount'].apply(categorize_discount)

    # Profitability Status
    def categorize_profit(profit):
        if profit > 0:
            return 'Profitable'
        elif profit < 0:
            return 'Loss-Making'
        else:
            return 'Breakeven'

    df['Profit_Status'] = df['Profit'].apply(categorize_profit)

    # Sort deterministically
    df = df.sort_values(by=['Order Date', 'Order ID']).reset_index(drop=True)

    # 9. Summary Statistics
    total_revenue = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    overall_margin = (total_profit / total_revenue) * 100
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    loss_orders = (df['Profit'] < 0).sum()
    loss_share = (loss_orders / len(df)) * 100

    print("\n" + "="*50)
    print("CLEANED DATASET SUMMARY METRICS")
    print("="*50)
    print(f"Total Clean Records:        {len(df):,}")
    print(f"Total Unique Orders:        {total_orders:,}")
    print(f"Total Customers:            {total_customers:,}")
    print(f"Date Range:                 {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")
    print(f"Total Revenue ($):          ${total_revenue:,.2f}")
    print(f"Total Net Profit ($):       ${total_profit:,.2f}")
    print(f"Overall Profit Margin:      {overall_margin:.2f}%")
    print(f"Loss-Making Transactions:   {loss_orders:,} ({loss_share:.2f}%)")
    print("="*50 + "\n")

    # 10. Save Cleaned Dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[+] Cleaned dataset successfully exported to: {output_path}")
    return df

if __name__ == '__main__':
    clean_sales_data()
