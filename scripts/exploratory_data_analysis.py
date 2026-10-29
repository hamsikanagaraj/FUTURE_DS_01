"""
Exploratory Data Analysis & Visualizations Generator
Business Sales Performance Analytics (Future Interns - Task 1)
Author: Data Science & Analytics Team
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Set style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'semibold'
plt.rcParams['figure.dpi'] = 150

def run_eda(csv_path='data/cleaned_superstore.csv', viz_dir='visualizations', report_dir='reports'):
    os.makedirs(viz_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    print(f"[*] Loading cleaned dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

    # -------------------------------------------------------------
    # 1. CORE KPI CALCULATIONS
    # -------------------------------------------------------------
    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    overall_margin = (total_profit / total_sales) * 100
    total_orders = int(df['Order ID'].nunique())
    total_customers = int(df['Customer ID'].nunique())
    total_quantity = int(df['Quantity'].sum())
    avg_order_value = float(total_sales / total_orders)
    loss_transactions = int((df['Profit'] < 0).sum())
    loss_rate = float((loss_transactions / len(df)) * 100)
    total_loss_amount = float(abs(df[df['Profit'] < 0]['Profit'].sum()))

    print(f"Core KPIs: Sales=${total_sales:,.2f}, Profit=${total_profit:,.2f}, Margin={overall_margin:.2f}%")

    # -------------------------------------------------------------
    # 2. VIZ 1: MONTHLY SALES & PROFIT TREND OVER TIME
    # -------------------------------------------------------------
    print("[*] Generating Chart 1: Monthly Sales & Profit Trend...")
    monthly = df.groupby('Order_Year_Month').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(13, 6))
    x = range(len(monthly))
    
    # Sales Bar
    bars = ax1.bar(x, monthly['Sales'], color='#3B82F6', alpha=0.75, width=0.65, label='Monthly Revenue ($)')
    ax1.set_ylabel('Revenue ($ USD)', color='#1E40AF', fontweight='bold')
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly['Order_Year_Month'], rotation=65, ha='right', fontsize=8.5)
    ax1.set_title('Superstore Monthly Revenue & Profit Trajectory (2015 - 2018)', pad=15)
    
    # Profit Line on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(x, monthly['Profit'], color='#10B981', linewidth=2.8, marker='o', markersize=5, label='Net Profit ($)')
    ax2.set_ylabel('Net Profit ($ USD)', color='#065F46', fontweight='bold')
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax2.grid(False)

    # Highlight Q4 peak season annotation
    max_month_idx = monthly['Sales'].idxmax()
    max_sales_val = monthly.loc[max_month_idx, 'Sales']
    ax1.annotate(f"Peak Season Surge:\n${max_sales_val:,.0f} ({monthly.loc[max_month_idx, 'Order_Year_Month']})",
                 xy=(max_month_idx, max_sales_val),
                 xytext=(max_month_idx - 6, max_sales_val * 0.95),
                 arrowprops=dict(facecolor='#1E3A8A', arrowstyle='->', lw=1.5),
                 fontweight='bold', fontsize=9, bbox=dict(boxstyle="round,pad=0.4", fc="#EFF6FF", ec="#3B82F6"))

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '01_monthly_revenue_profit_trend.png'))
    plt.close()

    # -------------------------------------------------------------
    # 3. VIZ 2: CATEGORY & SUBCATEGORY PERFORMANCE
    # -------------------------------------------------------------
    print("[*] Generating Chart 2: Category & Sub-Category Performance...")
    subcat = df.groupby(['Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Sales', ascending=True)

    fig, (ax_cat, ax_sub) = plt.subplots(1, 2, figsize=(15, 7.5), gridspec_kw={'width_ratios': [1, 2]})

    # Category Level
    cat_summary = df.groupby('Category').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).reset_index()
    cat_summary['Margin'] = (cat_summary['Profit'] / cat_summary['Sales']) * 100
    
    y_pos = range(len(cat_summary))
    ax_cat.barh([p - 0.18 for p in y_pos], cat_summary['Sales'], height=0.35, color='#3B82F6', label='Sales ($)')
    ax_cat.barh([p + 0.18 for p in y_pos], cat_summary['Profit'], height=0.35, color='#10B981', label='Profit ($)')
    ax_cat.set_yticks(y_pos)
    ax_cat.set_yticklabels(cat_summary['Category'], fontweight='bold')
    ax_cat.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax_cat.set_title('Category Revenue vs Profit', pad=12)
    ax_cat.legend(loc='lower right')
    for i, row in cat_summary.iterrows():
        ax_cat.text(row['Sales'] + 15000, i - 0.18, f"${row['Sales']/1000:,.0f}k\n({row['Margin']:.1f}% margin)", 
                    va='center', fontsize=8.5, fontweight='bold', color='#1E40AF')

    # Sub-Category Level
    colors = ['#EF4444' if p < 0 else '#10B981' for p in subcat['Profit']]
    bars_sub = ax_sub.barh(subcat['Sub-Category'], subcat['Sales'], color='#93C5FD', alpha=0.6, label='Sales ($)')
    ax_sub.barh(subcat['Sub-Category'], subcat['Profit'], color=colors, alpha=0.9, label='Profit / Loss ($)')
    ax_sub.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax_sub.set_title('Sub-Category Sales vs Profit (Red = Net Loss)', pad=12)
    ax_sub.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    ax_sub.legend(loc='lower right')
    
    # Annotate loss-making subcategories
    for idx, row in subcat.iterrows():
        if row['Profit'] < 0:
            ax_sub.text(row['Profit'] - 2000, row['Sub-Category'], f"-${abs(row['Profit']):,.0f}", 
                        va='center', ha='right', color='#DC2626', fontweight='bold', fontsize=8)

    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '02_category_subcategory_performance.png'))
    plt.close()

    # -------------------------------------------------------------
    # 4. VIZ 3: REGIONAL PROFITABILITY & SALES
    # -------------------------------------------------------------
    print("[*] Generating Chart 3: Regional Performance Analysis...")
    region_summary = df.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Avg_Discount=('Discount', 'mean')
    ).reset_index()
    region_summary['Profit_Margin'] = (region_summary['Profit'] / region_summary['Sales']) * 100
    region_summary = region_summary.sort_values(by='Sales', ascending=False)

    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    x_reg = np.arange(len(region_summary))
    width = 0.35

    rects1 = ax1.bar(x_reg - width/2, region_summary['Sales'], width, label='Total Sales ($)', color='#3B82F6', alpha=0.85)
    rects2 = ax1.bar(x_reg + width/2, region_summary['Profit'], width, label='Net Profit ($)', color='#10B981', alpha=0.85)
    
    ax1.set_ylabel('Total Amount ($ USD)', fontweight='bold')
    ax1.set_title('Regional Sales & Profitability Comparison (Notice Central Margin Lag)', pad=15)
    ax1.set_xticks(x_reg)
    ax1.set_xticklabels(region_summary['Region'], fontweight='bold', fontsize=11)
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax1.legend(loc='upper right')

    # Add margin % labels on top of bars
    for i, row in region_summary.iterrows():
        pos = list(region_summary['Region']).index(row['Region'])
        ax1.text(pos, row['Sales'] + 20000, 
                 f"Margin: {row['Profit_Margin']:.1f}%\nAvg Disc: {row['Avg_Discount']*100:.1f}%", 
                 ha='center', fontsize=9, fontweight='bold', color='#1E3A8A',
                 bbox=dict(boxstyle="round,pad=0.25", fc="#F8FAFC", ec="#CBD5E1"))

    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '03_regional_sales_margin_heatmap.png'))
    plt.close()

    # -------------------------------------------------------------
    # 5. VIZ 4: DISCOUNT VS PROFIT EROSION (ROOT CAUSE)
    # -------------------------------------------------------------
    print("[*] Generating Chart 4: Discount vs Profit Erosion...")
    disc_summary = df.groupby('Discount_Tier', observed=True).agg(
        Order_Count=('Order ID', 'count'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Profit_Margin=('Profit_Margin', 'mean')
    ).loc[['No Discount (0%)', 'Low (1% - 15%)', 'Moderate (16% - 30%)', 'Deep (> 30%)']].reset_index()

    disc_summary['Net_Margin'] = (disc_summary['Total_Profit'] / disc_summary['Total_Sales']) * 100

    fig, (ax_bar, ax_scatter) = plt.subplots(1, 2, figsize=(14, 6))

    # Bar of Net Margin by Discount Tier
    bar_colors = ['#10B981', '#34D399', '#FBBF24', '#EF4444']
    bars = ax_bar.bar(disc_summary['Discount_Tier'], disc_summary['Net_Margin'], color=bar_colors, width=0.55, edgecolor='#333333', linewidth=0.5)
    ax_bar.axhline(0, color='black', linewidth=1)
    ax_bar.set_ylabel('Net Profit Margin (%)', fontweight='bold')
    ax_bar.set_title('Net Profit Margin by Discount Tier\n(Deep Discounts Destroy Profitability)', pad=12)
    ax_bar.set_xticklabels(disc_summary['Discount_Tier'], rotation=15, ha='right', fontweight='semibold')
    for bar in bars:
        height = bar.get_height()
        va_val = 'bottom' if height < 0 else 'bottom'
        offset = -8 if height < 0 else 1.5
        ax_bar.text(bar.get_x() + bar.get_width()/2., height + offset,
                    f"{height:.1f}%", ha='center', va=va_val, fontweight='bold',
                    color='#DC2626' if height < 0 else '#065F46', fontsize=10)

    # Scatter: Discount % vs Profit Margin
    sample_df = df.sample(min(2000, len(df)), random_state=42)
    scatter_colors = ['#EF4444' if p < 0 else '#3B82F6' for p in sample_df['Profit']]
    ax_scatter.scatter(sample_df['Discount_Percentage'], sample_df['Profit_Margin'], 
                       c=scatter_colors, alpha=0.45, s=20, edgecolors='none')
    ax_scatter.axhline(0, color='red', linestyle='--', linewidth=1.2, label='Breakeven Line (0% Margin)')
    ax_scatter.axvline(20, color='orange', linestyle=':', linewidth=1.5, label='Danger Threshold (20% Discount)')
    ax_scatter.set_xlabel('Discount Applied (%)', fontweight='bold')
    ax_scatter.set_ylabel('Profit Margin (%)', fontweight='bold')
    ax_scatter.set_title('Discount % vs Profit Margin per Transaction\n(Red Points = Financial Losses)', pad=12)
    ax_scatter.legend(loc='lower left')
    ax_scatter.set_ylim(-250, 100)

    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '04_discount_vs_profit_erosion.png'))
    plt.close()

    # -------------------------------------------------------------
    # 6. VIZ 5: TOP 10 STAR PRODUCTS VS BOTTOM 10 BLEEDERS
    # -------------------------------------------------------------
    print("[*] Generating Chart 5: Top 10 Star Products vs Bottom 10 Bleeders...")
    prod_summary = df.groupby('Product Name').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()

    top10_profit = prod_summary.sort_values(by='Profit', ascending=False).head(10).sort_values(by='Profit', ascending=True)
    bottom10_profit = prod_summary.sort_values(by='Profit', ascending=True).head(10).sort_values(by='Profit', ascending=False)

    fig, (ax_top, ax_bot) = plt.subplots(1, 2, figsize=(16, 7.5))

    # Top 10 Profitable
    # Truncate long names for chart readability
    top_names = [name[:35] + '...' if len(name) > 35 else name for name in top10_profit['Product Name']]
    ax_top.barh(top_names, top10_profit['Profit'], color='#10B981', alpha=0.85)
    ax_top.set_title('Top 10 Most Profitable Products (Star Performers)', pad=12, color='#065F46')
    ax_top.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    for i, v in enumerate(top10_profit['Profit']):
        ax_top.text(v + 150, i, f"${v:,.0f}", va='center', fontweight='bold', fontsize=8.5, color='#047857')

    # Bottom 10 Loss-making
    bot_names = [name[:35] + '...' if len(name) > 35 else name for name in bottom10_profit['Product Name']]
    ax_bot.barh(bot_names, bottom10_profit['Profit'], color='#EF4444', alpha=0.85)
    ax_bot.set_title('Bottom 10 Loss-Making Products (Margin Bleeders)', pad=12, color='#991B1B')
    ax_bot.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    for i, v in enumerate(bottom10_profit['Profit']):
        ax_bot.text(v - 150, i, f"-${abs(v):,.0f}", va='center', ha='right', fontweight='bold', fontsize=8.5, color='#B91C1C')

    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '05_top10_and_bottom10_products.png'))
    plt.close()

    # -------------------------------------------------------------
    # 7. VIZ 6: CUSTOMER SEGMENT PROFILE
    # -------------------------------------------------------------
    print("[*] Generating Chart 6: Customer Segment Profile...")
    segment_summary = df.groupby('Segment').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Customer_Count=('Customer ID', 'nunique'),
        Order_Count=('Order ID', 'nunique')
    ).reset_index()
    segment_summary['Margin'] = (segment_summary['Profit'] / segment_summary['Sales']) * 100
    segment_summary['AOV'] = segment_summary['Sales'] / segment_summary['Order_Count']

    fig, (ax_pie, ax_aov) = plt.subplots(1, 2, figsize=(13, 5.5))
    
    # Revenue Share Donut Chart
    colors_seg = ['#3B82F6', '#10B981', '#F59E0B']
    wedges, texts, autotexts = ax_pie.pie(
        segment_summary['Sales'], 
        labels=segment_summary['Segment'], 
        autopct='%1.1f%%',
        startangle=140, 
        colors=colors_seg, 
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_fontweight('bold')
        at.set_fontsize(10)
    ax_pie.set_title('Revenue Share by Customer Segment', pad=12)

    # Average Order Value and Margin Bar
    x_seg = np.arange(len(segment_summary))
    ax_aov.bar(x_seg - 0.2, segment_summary['AOV'], width=0.38, color='#6366F1', label='Avg Order Value ($)')
    ax_aov.set_ylabel('Average Order Value ($ USD)', fontweight='bold')
    ax_aov.set_xticks(x_seg)
    ax_aov.set_xticklabels(segment_summary['Segment'], fontweight='bold')
    ax_aov.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    
    # Secondary axis for profit margin
    ax_aov2 = ax_aov.twinx()
    ax_aov2.plot(x_seg, segment_summary['Margin'], color='#10B981', marker='s', markersize=8, linewidth=2.5, label='Profit Margin (%)')
    ax_aov2.set_ylabel('Profit Margin (%)', fontweight='bold', color='#065F46')
    ax_aov2.set_ylim(10, 16)
    ax_aov2.grid(False)

    lines_a, labels_a = ax_aov.get_legend_handles_labels()
    lines_b, labels_b = ax_aov2.get_legend_handles_labels()
    ax_aov.legend(lines_a + lines_b, labels_a + labels_b, loc='upper right')
    ax_aov.set_title('AOV & Profit Margin by Customer Segment', pad=12)

    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '06_customer_segment_analysis.png'))
    plt.close()

    # -------------------------------------------------------------
    # 8. VIZ 7: SHIPPING EFFICIENCY & TURNAROUND
    # -------------------------------------------------------------
    print("[*] Generating Chart 7: Shipping Mode & Fulfillment Efficiency...")
    ship_summary = df.groupby('Ship Mode').agg(
        Order_Count=('Order ID', 'nunique'),
        Avg_Days=('Days_to_Ship', 'mean'),
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Order_Count', ascending=False)
    ship_summary['Margin'] = (ship_summary['Profit'] / ship_summary['Sales']) * 100

    fig, ax_ship = plt.subplots(figsize=(10, 5))
    bars_ship = ax_ship.bar(ship_summary['Ship Mode'], ship_summary['Order_Count'], color='#8B5CF6', alpha=0.85, width=0.55)
    ax_ship.set_ylabel('Total Number of Orders', fontweight='bold')
    ax_ship.set_title('Order Volume and Fulfillment Lead Times by Shipping Class', pad=15)
    
    for i, row in ship_summary.iterrows():
        pos = list(ship_summary['Ship Mode']).index(row['Ship Mode'])
        ax_ship.text(pos, row['Order_Count'] + 60, 
                     f"Avg: {row['Avg_Days']:.1f} days\nMargin: {row['Margin']:.1f}%\nVol: {row['Order_Count']:,}",
                     ha='center', fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.25", fc="#F5F3FF", ec="#C4B5FD"))

    plt.tight_layout()
    fig.savefig(os.path.join(viz_dir, '07_shipping_efficiency_matrix.png'))
    plt.close()

    # -------------------------------------------------------------
    # 9. EXPORT BUSINESS METRICS JSON
    # -------------------------------------------------------------
    yearly_growth = df.groupby('Order_Year').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).to_dict(orient='index')

    category_metrics = df.groupby('Category').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    category_metrics['Margin'] = (category_metrics['Profit'] / category_metrics['Sales'] * 100).round(2)

    region_metrics = df.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    region_metrics['Margin'] = (region_metrics['Profit'] / region_metrics['Sales'] * 100).round(2)

    insights_data = {
        "kpis": {
            "total_sales": round(total_sales, 2),
            "total_profit": round(total_profit, 2),
            "profit_margin": round(overall_margin, 2),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "avg_order_value": round(avg_order_value, 2),
            "loss_transactions_count": loss_transactions,
            "loss_rate_percentage": round(loss_rate, 2),
            "total_loss_dollars": round(total_loss_amount, 2)
        },
        "yearly_performance": {str(k): {m: round(v, 2) for m, v in vals.items()} for k, vals in yearly_growth.items()},
        "categories": category_metrics.to_dict(orient='records'),
        "regions": region_metrics.to_dict(orient='records'),
        "subcategories_loss_making": subcat[subcat['Profit'] < 0][['Sub-Category', 'Sales', 'Profit']].to_dict(orient='records'),
        "top_5_products_by_revenue": prod_summary.sort_values(by='Sales', ascending=False).head(5)[['Product Name', 'Sales', 'Profit']].to_dict(orient='records'),
        "top_5_products_by_profit": prod_summary.sort_values(by='Profit', ascending=False).head(5)[['Product Name', 'Sales', 'Profit']].to_dict(orient='records'),
        "bottom_5_loss_products": prod_summary.sort_values(by='Profit', ascending=True).head(5)[['Product Name', 'Sales', 'Profit']].to_dict(orient='records')
    }

    json_path = os.path.join(report_dir, 'business_insights_summary.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(insights_data, f, indent=4)
        
    print(f"[+] Business insights exported to: {json_path}")
    print("[+] All 7 visualization charts generated successfully!")

if __name__ == '__main__':
    run_eda()
