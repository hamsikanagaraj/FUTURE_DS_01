"""
Professional Excel Analytics Workbook Generator
Business Sales Performance Analytics (Future Interns - Task 1)
Author: Data Science & Analytics Team
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_excel_report(csv_path='data/cleaned_superstore.csv', output_path='reports/Superstore_Sales_Analytics.xlsx'):
    print(f"[*] Reading cleaned data from {csv_path}...")
    df = pd.read_csv(csv_path)

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    navy_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    dark_blue_fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    light_blue_fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
    gray_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    green_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    red_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

    font_title = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
    font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="E0E7FF")
    font_section = Font(name="Segoe UI", size=12, bold=True, color="1E3A8A")
    font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    font_sub_header = Font(name="Segoe UI", size=10, bold=True, color="1E293B")
    font_data = Font(name="Segoe UI", size=10, color="0F172A")
    font_bold = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
    font_kpi_num = Font(name="Segoe UI", size=15, bold=True, color="1E3A8A")
    font_kpi_label = Font(name="Segoe UI", size=9, bold=True, color="64748B")

    thin_border_side = Side(border_style="thin", color="CBD5E1")
    border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    thick_bottom = Border(bottom=Side(border_style="medium", color="1E3A8A"))
    double_bottom = Border(top=thin_border_side, bottom=Side(border_style="double", color="1E3A8A"))

    # =========================================================================
    # SHEET 1: EXECUTIVE KPI DASHBOARD
    # =========================================================================
    print("[*] Creating Sheet 1: Executive KPI Dashboard...")
    ws_kpi = wb.create_sheet(title="Executive Dashboard")
    ws_kpi.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_kpi.merge_cells("A1:G2")
    title_cell = ws_kpi["A1"]
    title_cell.value = "BUSINESS SALES PERFORMANCE DASHBOARD | EXECUTIVE OVERVIEW"
    title_cell.font = font_title
    title_cell.fill = navy_fill
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws_kpi.merge_cells("A3:G3")
    sub_cell = ws_kpi["A3"]
    sub_cell.value = "Future Interns Data Science & Analytics Internship (2026) • Sample Superstore Analysis (2015-2018)"
    sub_cell.font = font_subtitle
    sub_cell.fill = navy_fill
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")

    # KPI Summary Cards (Row 5 to 7)
    kpis = [
        ("TOTAL REVENUE", df['Sales'].sum(), "$#,##0", "B5", "B7"),
        ("NET PROFIT", df['Profit'].sum(), "$#,##0", "C5", "C7"),
        ("PROFIT MARGIN", (df['Profit'].sum() / df['Sales'].sum()), "0.0%", "D5", "D7"),
        ("TOTAL ORDERS", df['Order ID'].nunique(), "#,##0", "E5", "E7"),
        ("AVG ORDER VALUE", df['Sales'].sum() / df['Order ID'].nunique(), "$#,##0.00", "F5", "F7"),
        ("PROFIT EROSION LOSSES", abs(df[df['Profit'] < 0]['Profit'].sum()), "$#,##0", "G5", "G7")
    ]

    for label, val, num_fmt, start_cell, end_cell in kpis:
        col_letter = start_cell[0]
        # Label cell
        cell_lbl = ws_kpi[f"{col_letter}5"]
        cell_lbl.value = label
        cell_lbl.font = font_kpi_label
        cell_lbl.alignment = Alignment(horizontal="center", vertical="center")
        cell_lbl.fill = light_blue_fill

        # Value cell
        cell_val = ws_kpi[f"{col_letter}6"]
        cell_val.value = val
        cell_val.font = font_kpi_num
        cell_val.number_format = num_fmt
        cell_val.alignment = Alignment(horizontal="center", vertical="center")
        cell_val.fill = light_blue_fill

        for r in range(5, 7):
            ws_kpi[f"{col_letter}{r}"].border = border_cell

    # 1. Performance By Category
    ws_kpi["B9"].value = "1. Performance Summary by Product Category"
    ws_kpi["B9"].font = font_section

    headers_cat = ["Product Category", "Total Sales", "Net Profit", "Profit Margin", "Units Sold", "Loss Share"]
    for c_idx, h in enumerate(headers_cat, start=2):
        cell = ws_kpi.cell(row=10, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = dark_blue_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = border_cell

    cat_grp = df.groupby('Category').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum')
    ).reset_index()

    row_idx = 11
    for _, row in cat_grp.iterrows():
        margin = row['Profit'] / row['Sales']
        ws_kpi.cell(row=row_idx, column=2, value=row['Category']).font = font_bold
        
        c_sales = ws_kpi.cell(row=row_idx, column=3, value=row['Sales'])
        c_sales.number_format = "$#,##0"
        
        c_profit = ws_kpi.cell(row=row_idx, column=4, value=row['Profit'])
        c_profit.number_format = "$#,##0"
        
        c_margin = ws_kpi.cell(row=row_idx, column=5, value=margin)
        c_margin.number_format = "0.0%"
        c_margin.fill = red_fill if margin < 0.05 else (green_fill if margin > 0.15 else light_blue_fill)
        
        c_qty = ws_kpi.cell(row=row_idx, column=6, value=row['Quantity'])
        c_qty.number_format = "#,##0"

        # Share of total loss
        cat_loss = abs(df[(df['Category'] == row['Category']) & (df['Profit'] < 0)]['Profit'].sum())
        c_loss = ws_kpi.cell(row=row_idx, column=7, value=cat_loss)
        c_loss.number_format = "$#,##0"

        for c in range(2, 8):
            ws_kpi.cell(row=row_idx, column=c).border = border_cell
        row_idx += 1

    # Total Row for Category
    ws_kpi.cell(row=row_idx, column=2, value="TOTAL / BLENDED").font = font_bold
    ws_kpi.cell(row=row_idx, column=3, value=f"=SUM(C11:C{row_idx-1})").number_format = "$#,##0"
    ws_kpi.cell(row=row_idx, column=4, value=f"=SUM(D11:D{row_idx-1})").number_format = "$#,##0"
    ws_kpi.cell(row=row_idx, column=5, value=f"=D{row_idx}/C{row_idx}").number_format = "0.0%"
    ws_kpi.cell(row=row_idx, column=6, value=f"=SUM(F11:F{row_idx-1})").number_format = "#,##0"
    ws_kpi.cell(row=row_idx, column=7, value=f"=SUM(G11:G{row_idx-1})").number_format = "$#,##0"
    for c in range(2, 8):
        c_tot = ws_kpi.cell(row=row_idx, column=c)
        c_tot.font = font_bold
        c_tot.fill = gray_fill
        c_tot.border = double_bottom

    # 2. Performance By Region
    row_idx += 3
    ws_kpi.cell(row=row_idx, column=2, value="2. Performance Summary by Geographical Region").font = font_section
    row_idx += 1
    
    headers_reg = ["Region", "Total Sales", "Net Profit", "Profit Margin", "Avg Discount", "Orders"]
    for c_idx, h in enumerate(headers_reg, start=2):
        cell = ws_kpi.cell(row=row_idx, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = dark_blue_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = border_cell

    reg_grp = df.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Discount=('Discount', 'mean'),
        Orders=('Order ID', 'nunique')
    ).reset_index()

    start_reg_row = row_idx + 1
    row_idx += 1
    for _, row in reg_grp.iterrows():
        margin = row['Profit'] / row['Sales']
        ws_kpi.cell(row=row_idx, column=2, value=row['Region']).font = font_bold
        
        c_s = ws_kpi.cell(row=row_idx, column=3, value=row['Sales'])
        c_s.number_format = "$#,##0"
        
        c_p = ws_kpi.cell(row=row_idx, column=4, value=row['Profit'])
        c_p.number_format = "$#,##0"
        
        c_m = ws_kpi.cell(row=row_idx, column=5, value=margin)
        c_m.number_format = "0.0%"
        c_m.fill = red_fill if margin < 0.10 else green_fill
        
        c_d = ws_kpi.cell(row=row_idx, column=6, value=row['Discount'])
        c_d.number_format = "0.0%"
        
        c_o = ws_kpi.cell(row=row_idx, column=7, value=row['Orders'])
        c_o.number_format = "#,##0"

        for c in range(2, 8):
            ws_kpi.cell(row=row_idx, column=c).border = border_cell
        row_idx += 1

    # Regional Total
    ws_kpi.cell(row=row_idx, column=2, value="TOTAL / BLENDED").font = font_bold
    ws_kpi.cell(row=row_idx, column=3, value=f"=SUM(C{start_reg_row}:C{row_idx-1})").number_format = "$#,##0"
    ws_kpi.cell(row=row_idx, column=4, value=f"=SUM(D{start_reg_row}:D{row_idx-1})").number_format = "$#,##0"
    ws_kpi.cell(row=row_idx, column=5, value=f"=D{row_idx}/C{row_idx}").number_format = "0.0%"
    ws_kpi.cell(row=row_idx, column=6, value=f"=AVERAGE(F{start_reg_row}:F{row_idx-1})").number_format = "0.0%"
    ws_kpi.cell(row=row_idx, column=7, value=f"=SUM(G{start_reg_row}:G{row_idx-1})").number_format = "#,##0"
    for c in range(2, 8):
        c_tot = ws_kpi.cell(row=row_idx, column=c)
        c_tot.font = font_bold
        c_tot.fill = gray_fill
        c_tot.border = double_bottom

    # Adjust column widths for Sheet 1
    for col in ws_kpi.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws_kpi.column_dimensions[col_letter].width = max(max_len + 3, 14)
    ws_kpi.column_dimensions['A'].width = 4

    # =========================================================================
    # SHEET 2: CATEGORY & SUBCATEGORY ANALYSIS
    # =========================================================================
    print("[*] Creating Sheet 2: Category & Subcategory Analysis...")
    ws_cat = wb.create_sheet(title="Category Deep Dive")
    ws_cat.views.sheetView[0].showGridLines = True

    ws_cat.merge_cells("A1:G2")
    c2 = ws_cat["A1"]
    c2.value = "PRODUCT CATEGORY & SUB-CATEGORY PROFITABILITY AUDIT"
    c2.font = font_title
    c2.fill = navy_fill
    c2.alignment = Alignment(horizontal="center", vertical="center")

    headers_sub = ["Category", "Sub-Category", "Total Revenue", "Net Profit ($)", "Profit Margin", "Quantity Sold", "Status"]
    for c_idx, h in enumerate(headers_sub, start=1):
        cell = ws_cat.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = dark_blue_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = border_cell

    sub_df = df.groupby(['Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum')
    ).reset_index().sort_values(by=['Category', 'Sales'], ascending=[True, False])

    r_idx = 5
    for _, row in sub_df.iterrows():
        margin = row['Profit'] / row['Sales']
        ws_cat.cell(row=r_idx, column=1, value=row['Category']).font = font_bold
        ws_cat.cell(row=r_idx, column=2, value=row['Sub-Category']).font = font_data
        
        c_s = ws_cat.cell(row=r_idx, column=3, value=row['Sales'])
        c_s.number_format = "$#,##0"
        
        c_p = ws_cat.cell(row=r_idx, column=4, value=row['Profit'])
        c_p.number_format = "$#,##0"
        
        c_m = ws_cat.cell(row=r_idx, column=5, value=margin)
        c_m.number_format = "0.0%"
        c_m.fill = red_fill if margin < 0 else (green_fill if margin > 0.15 else light_blue_fill)
        
        c_q = ws_cat.cell(row=r_idx, column=6, value=row['Quantity'])
        c_q.number_format = "#,##0"

        c_status = ws_cat.cell(row=r_idx, column=7, value="LOSS BLEEDER" if row['Profit'] < 0 else ("HIGH MARGIN" if margin > 0.20 else "STABLE"))
        c_status.font = font_bold
        c_status.fill = red_fill if row['Profit'] < 0 else (green_fill if margin > 0.20 else gray_fill)

        for c in range(1, 8):
            ws_cat.cell(row=r_idx, column=c).border = border_cell
        r_idx += 1

    for col in ws_cat.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws_cat.column_dimensions[col_letter].width = max(max_len + 3, 16)

    # =========================================================================
    # SHEET 3: TOP & BOTTOM PRODUCTS
    # =========================================================================
    print("[*] Creating Sheet 3: Star Products vs Loss Bleeders...")
    ws_prod = wb.create_sheet(title="Product Performance")
    ws_prod.views.sheetView[0].showGridLines = True

    ws_prod.merge_cells("A1:E2")
    p1 = ws_prod["A1"]
    p1.value = "TOP 15 MOST PROFITABLE PRODUCTS (STAR PERFORMERS)"
    p1.font = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
    p1.fill = navy_fill
    p1.alignment = Alignment(horizontal="center", vertical="center")

    prod_df = df.groupby(['Product Name', 'Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum')
    ).reset_index()

    top_prods = prod_df.sort_values(by='Profit', ascending=False).head(15)
    headers_p = ["Product Name", "Category", "Sales", "Net Profit", "Margin"]
    for c_idx, h in enumerate(headers_p, start=1):
        cell = ws_prod.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = dark_blue_fill
        cell.border = border_cell

    r = 4
    for _, row in top_prods.iterrows():
        ws_prod.cell(row=r, column=1, value=row['Product Name']).font = font_data
        ws_prod.cell(row=r, column=2, value=row['Category']).font = font_data
        ws_prod.cell(row=r, column=3, value=row['Sales']).number_format = "$#,##0"
        ws_prod.cell(row=r, column=4, value=row['Profit']).number_format = "$#,##0"
        m = ws_prod.cell(row=r, column=5, value=row['Profit']/row['Sales'] if row['Sales'] > 0 else 0)
        m.number_format = "0.0%"
        m.fill = green_fill
        for c in range(1, 6):
            ws_prod.cell(row=r, column=c).border = border_cell
        r += 1

    # Bottom Products
    r += 2
    ws_prod.merge_cells(f"A{r}:E{r+1}")
    p2 = ws_prod[f"A{r}"]
    p2.value = "BOTTOM 15 LOSS-MAKING PRODUCTS (MARGIN BLEEDERS)"
    p2.font = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF")
    p2.fill = PatternFill(start_color="991B1B", end_color="991B1B", fill_type="solid")
    p2.alignment = Alignment(horizontal="center", vertical="center")
    
    r += 2
    for c_idx, h in enumerate(headers_p, start=1):
        cell = ws_prod.cell(row=r, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = PatternFill(start_color="DC2626", end_color="DC2626", fill_type="solid")
        cell.border = border_cell
    r += 1

    bottom_prods = prod_df.sort_values(by='Profit', ascending=True).head(15)
    for _, row in bottom_prods.iterrows():
        ws_prod.cell(row=r, column=1, value=row['Product Name']).font = font_data
        ws_prod.cell(row=r, column=2, value=row['Category']).font = font_data
        ws_prod.cell(row=r, column=3, value=row['Sales']).number_format = "$#,##0"
        ws_prod.cell(row=r, column=4, value=row['Profit']).number_format = "$#,##0"
        m = ws_prod.cell(row=r, column=5, value=row['Profit']/row['Sales'] if row['Sales'] > 0 else 0)
        m.number_format = "0.0%"
        m.fill = red_fill
        for c in range(1, 6):
            ws_prod.cell(row=r, column=c).border = border_cell
        r += 1

    ws_prod.column_dimensions['A'].width = 45
    ws_prod.column_dimensions['B'].width = 18
    ws_prod.column_dimensions['C'].width = 14
    ws_prod.column_dimensions['D'].width = 14
    ws_prod.column_dimensions['E'].width = 12

    # =========================================================================
    # SHEET 4: CLEANED SALES DATA (PIVOT-READY)
    # =========================================================================
    print("[*] Creating Sheet 4: Cleaned Sales Data...")
    ws_raw = wb.create_sheet(title="Cleaned Sales Data")
    ws_raw.views.sheetView[0].showGridLines = True

    export_cols = [
        'Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer Name', 
        'Segment', 'City', 'State', 'Region', 'Category', 'Sub-Category', 
        'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit', 'Profit_Margin', 'Profit_Status'
    ]
    
    # Write header
    for c_idx, col_name in enumerate(export_cols, start=1):
        cell = ws_raw.cell(row=1, column=c_idx, value=col_name)
        cell.font = font_header
        cell.fill = navy_fill
        cell.border = border_cell
        cell.alignment = Alignment(horizontal="center")

    # Write data rows
    data_values = df[export_cols].values.tolist()
    for row_num, row_data in enumerate(data_values, start=2):
        for col_num, val in enumerate(row_data, start=1):
            cell = ws_raw.cell(row=row_num, column=col_num, value=val)
            col_name = export_cols[col_num - 1]
            if col_name in ['Sales', 'Profit']:
                cell.number_format = "$#,##0.00"
            elif col_name == 'Discount':
                cell.number_format = "0.0%"
            elif col_name == 'Profit_Margin':
                cell.number_format = "0.00"
            elif col_name == 'Quantity':
                cell.number_format = "#,##0"

    # Set column widths
    for col in ws_raw.columns:
        col_letter = get_column_letter(col[0].column)
        ws_raw.column_dimensions[col_letter].width = 14
    ws_raw.column_dimensions['E'].width = 20  # Customer Name
    ws_raw.column_dimensions['L'].width = 30  # Product Name

    # Enable autofilter on data sheet
    ws_raw.auto_filter.ref = f"A1:{get_column_letter(len(export_cols))}{len(df)+1}"

    # Save workbook
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"[+] Master Excel report successfully generated: {output_path}")

if __name__ == '__main__':
    generate_excel_report()
