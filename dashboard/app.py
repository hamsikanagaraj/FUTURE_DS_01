"""
Interactive Business Sales Performance Analytics Dashboard
Future Interns - Data Science & Analytics Internship (Task 1)
Built with Streamlit & Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Page Configuration
st.set_page_config(
    page_title="Superstore Sales Performance Analytics",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        border-top: 4px solid #3B82F6;
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0.3rem 0;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #10B981;
        font-weight: 600;
    }
    .kpi-sub-neg {
        font-size: 0.8rem;
        color: #EF4444;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_superstore.csv')
    if not os.path.exists(data_path):
        data_path = 'data/cleaned_superstore.csv'
    df = pd.read_csv(data_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df

df = load_data()

# -------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=70)
st.sidebar.title("Analytics Filters")
st.sidebar.markdown("Slice and drill down into sales metrics:")

# Date Range Filter
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Region Filter
all_regions = ['All Regions'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox("Geographic Region", all_regions)

# Category Filter
all_categories = ['All Categories'] + sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.selectbox("Product Category", all_categories)

# Customer Segment Filter
all_segments = ['All Segments'] + sorted(df['Segment'].unique().tolist())
selected_segment = st.sidebar.selectbox("Customer Segment", all_segments)

# Discount Bracket Filter
all_discount_tiers = ['All Discount Tiers'] + sorted(df['Discount_Tier'].unique().tolist())
selected_discount = st.sidebar.selectbox("Discount Strategy Tier", all_discount_tiers)

# Filter Dataset
filtered_df = df.copy()
if len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = filtered_df[(filtered_df['Order Date'].dt.date >= start_d) & (filtered_df['Order Date'].dt.date <= end_d)]

if selected_region != 'All Regions':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]

if selected_category != 'All Categories':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]

if selected_segment != 'All Segments':
    filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]

if selected_discount != 'All Discount Tiers':
    filtered_df = filtered_df[filtered_df['Discount_Tier'] == selected_discount]

# -------------------------------------------------------------
# HEADER & EXECUTIVE KPI CARDS
# -------------------------------------------------------------
st.markdown('<div class="main-header">Business Sales Performance Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive Decision-Support Dashboard | Future Interns Data Science & Analytics (Task 1)</div>', unsafe_allow_html=True)

# Metrics calculation
tot_sales = filtered_df['Sales'].sum()
tot_profit = filtered_df['Profit'].sum()
margin_pct = (tot_profit / tot_sales * 100) if tot_sales > 0 else 0
tot_orders = filtered_df['Order ID'].nunique()
aov = (tot_sales / tot_orders) if tot_orders > 0 else 0
loss_records = filtered_df[filtered_df['Profit'] < 0]
tot_loss_amount = abs(loss_records['Profit'].sum())
loss_rate = (len(loss_records) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #3B82F6;">
        <div class="kpi-title">Total Revenue</div>
        <div class="kpi-value">${tot_sales:,.0f}</div>
        <div class="kpi-sub">Gross Sales</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    profit_color = "#10B981" if tot_profit >= 0 else "#EF4444"
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: {profit_color};">
        <div class="kpi-title">Net Profit</div>
        <div class="kpi-value">${tot_profit:,.0f}</div>
        <div class="kpi-sub">Bottom-Line Return</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    margin_color = "#10B981" if margin_pct >= 12 else ("#F59E0B" if margin_pct >= 5 else "#EF4444")
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: {margin_color};">
        <div class="kpi-title">Profit Margin</div>
        <div class="kpi-value">{margin_pct:.1f}%</div>
        <div class="kpi-sub">Benchmark: 12.5%</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #8B5CF6;">
        <div class="kpi-title">Total Orders</div>
        <div class="kpi-value">{tot_orders:,}</div>
        <div class="kpi-sub">{len(filtered_df):,} line items</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #06B6D4;">
        <div class="kpi-title">Avg Order Value</div>
        <div class="kpi-value">${aov:,.0f}</div>
        <div class="kpi-sub">Per unique order</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #EF4444;">
        <div class="kpi-title">Profit Bleed (Losses)</div>
        <div class="kpi-value" style="color: #DC2626;">${tot_loss_amount:,.0f}</div>
        <div class="kpi-sub-neg">{loss_rate:.1f}% loss transactions</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN DASHBOARD TABS
# -------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Revenue & Profit Trends", 
    "📦 Category & Sub-Category Diagnostics", 
    "🗺️ Regional Performance", 
    "⚠️ Discount & Profit Leaks", 
    "💡 Strategic Recommendations",
    "🔍 Raw Data Explorer"
])

# -------------------------------------------------------------
# TAB 1: REVENUE TRENDS
# -------------------------------------------------------------
with tab1:
    st.subheader("Revenue & Profit Dynamics Over Time")
    
    monthly_trend = filtered_df.groupby('Order_Year_Month').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=monthly_trend['Order_Year_Month'], 
        y=monthly_trend['Sales'],
        name='Gross Revenue ($)',
        marker_color='#3B82F6',
        opacity=0.75
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_trend['Order_Year_Month'], 
        y=monthly_trend['Profit'],
        name='Net Profit ($)',
        yaxis='y2',
        line=dict(color='#10B981', width=3),
        mode='lines+markers'
    ))

    fig_trend.update_layout(
        title="Monthly Sales Volume vs Net Profit Trajectory",
        xaxis=dict(title="Month (YYYY-MM)", tickangle=-45),
        yaxis=dict(title="Revenue ($ USD)", tickprefix="$"),
        yaxis2=dict(
            title="Net Profit ($ USD)", 
            overlaying='y', 
            side='right', 
            tickprefix="$"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=480,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### Yearly Performance Comparison")
        yearly = filtered_df.groupby('Order_Year').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Orders=('Order ID', 'nunique')
        ).reset_index()
        yearly['Margin %'] = (yearly['Profit'] / yearly['Sales'] * 100).round(2)
        yearly['Sales ($)'] = yearly['Sales'].apply(lambda x: f"${x:,.2f}")
        yearly['Profit ($)'] = yearly['Profit'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(yearly[['Order_Year', 'Sales ($)', 'Profit ($)', 'Margin %', 'Orders']], use_container_width=True)

    with col_t2:
        st.markdown("#### Seasonal Q4 Surge Pattern")
        st.info("""
        **Executive Finding:**
        - Sales consistently peak in **Q4 (September - December)**, accounting for **38%+ of annual volume**.
        - Revenue grew consistently year-over-year from **$484k (2015)** to **$733k (2018)** (+51.4% expansion).
        - However, net margins remained capped between **10.2% - 13.4%** due to unoptimized promotional discounting during holiday peaks.
        """)

# -------------------------------------------------------------
# TAB 2: CATEGORY & SUBCATEGORY
# -------------------------------------------------------------
with tab2:
    st.subheader("Category & Sub-Category Diagnostics")
    
    col_c1, col_c2 = st.columns([1, 1])
    with col_c1:
        cat_agg = filtered_df.groupby('Category').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).reset_index()
        cat_agg['Margin'] = (cat_agg['Profit'] / cat_agg['Sales'] * 100).round(1)

        fig_cat = px.bar(
            cat_agg, x='Category', y='Sales', color='Margin',
            color_continuous_scale=['#EF4444', '#FBBF24', '#10B981'],
            title="Revenue by Product Category (Color = Margin %)",
            labels={'Sales': 'Revenue ($)', 'Margin': 'Margin (%)'},
            text=cat_agg['Margin'].apply(lambda m: f"{m:.1f}% margin")
        )
        fig_cat.update_traces(textposition='outside')
        fig_cat.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_c2:
        sub_agg = filtered_df.groupby(['Category', 'Sub-Category']).agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).reset_index().sort_values(by='Sales', ascending=True)
        sub_agg['Status'] = np.where(sub_agg['Profit'] < 0, 'Loss-Making', 'Profitable')

        fig_sub = px.bar(
            sub_agg, y='Sub-Category', x='Sales', color='Status',
            color_discrete_map={'Profitable': '#3B82F6', 'Loss-Making': '#EF4444'},
            title="Sub-Category Revenue vs Profitability Status",
            orientation='h',
            labels={'Sales': 'Revenue ($)'}
        )
        fig_sub.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig_sub, use_container_width=True)

    st.markdown("#### High-Value vs Bleeding Sub-Categories")
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.success("""
        **Top Profit Drivers:**
        - **Copiers:** $55,617 profit on $149,528 sales (**37.2% margin**)
        - **Phones:** $44,515 profit on $330,007 sales (**13.5% margin**)
        - **Accessories:** $41,936 profit on $167,380 sales (**25.1% margin**)
        - **Paper:** $34,053 profit on $78,479 sales (**43.4% margin**)
        """)
    with col_sub2:
        st.error("""
        **Major Margin Bleeders (Require Urgent Intervention):**
        - **Tables:** -$17,725 net loss on $206,965 sales (**-8.6% margin**)
        - **Bookcases:** -$3,473 net loss on $114,880 sales (**-3.0% margin**)
        - **Supplies:** -$1,189 net loss on $46,674 sales (**-2.5% margin**)
        *Cause: Deep discounting (>30%) coupled with high freight/handling fees.*
        """)

# -------------------------------------------------------------
# TAB 3: REGIONAL PERFORMANCE
# -------------------------------------------------------------
with tab3:
    st.subheader("Geographical Sales & Profitability Breakdown")

    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        reg_agg = filtered_df.groupby('Region').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Discount=('Discount', 'mean'),
            Orders=('Order ID', 'nunique')
        ).reset_index()
        reg_agg['Margin'] = (reg_agg['Profit'] / reg_agg['Sales'] * 100).round(1)

        fig_reg = px.bar(
            reg_agg, x='Region', y=['Sales', 'Profit'],
            barmode='group',
            title="Regional Sales vs Profit ($ USD)",
            color_discrete_map={'Sales': '#3B82F6', 'Profit': '#10B981'}
        )
        fig_reg.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_r2:
        # State Level Profit
        state_agg = filtered_df.groupby('State').agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum')
        ).reset_index().sort_values(by='Profit', ascending=False)

        top_states = pd.concat([state_agg.head(5), state_agg.tail(5)])
        top_states['Type'] = np.where(top_states['Profit'] >= 0, 'Top 5 Most Profitable', 'Bottom 5 Least Profitable')

        fig_states = px.bar(
            top_states, y='State', x='Profit', color='Type',
            orientation='h',
            title="State-Level Profit Leaders & Loss Centers",
            color_discrete_map={'Top 5 Most Profitable': '#10B981', 'Bottom 5 Least Profitable': '#EF4444'}
        )
        fig_states.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_states, use_container_width=True)

    st.markdown("#### Regional Strategic Analysis")
    st.markdown("""
    | Region | Revenue ($) | Profit ($) | Margin (%) | Key Characteristic | Action Required |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | **West** | $725,458 | $108,418 | **14.9%** | Star Region (California is top profit driver) | Scale marketing and enterprise accounts |
    | **East** | $678,781 | $91,523 | **13.5%** | Strong performer (New York leads volume) | Protect pricing; expand accessory attach rates |
    | **South** | $391,722 | $46,749 | **11.9%** | Moderate volume, healthy unit margins | Target corporate expansion in Florida/NC |
    | **Central** | $501,240 | $39,706 | **7.9%** | Severe margin compression (Texas/Illinois heavy losses) | Immediate price floor & discount restructuring |
    """)

# -------------------------------------------------------------
# TAB 4: DISCOUNT & PROFIT LEAKS
# -------------------------------------------------------------
with tab4:
    st.subheader("Root-Cause Diagnosis: Discount Sensitivity & Profit Erosion")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        disc_tier = filtered_df.groupby('Discount_Tier', observed=True).agg(
            Sales=('Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Transactions=('Order ID', 'count')
        ).loc[['No Discount (0%)', 'Low (1% - 15%)', 'Moderate (16% - 30%)', 'Deep (> 30%)']].reset_index()
        disc_tier['Margin %'] = (disc_tier['Profit'] / disc_tier['Sales'] * 100).round(1)

        fig_disc_bar = px.bar(
            disc_tier, x='Discount_Tier', y='Margin %',
            title="Net Profit Margin by Discount Tier",
            color='Margin %',
            color_continuous_scale=['#EF4444', '#FBBF24', '#10B981'],
            text=disc_tier['Margin %'].apply(lambda x: f"{x:.1f}%")
        )
        fig_disc_bar.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_disc_bar.update_traces(textposition='outside')
        fig_disc_bar.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_disc_bar, use_container_width=True)

    with col_d2:
        sample_pts = filtered_df.sample(min(1500, len(filtered_df)), random_state=42)
        fig_scatter = px.scatter(
            sample_pts, x='Discount_Percentage', y='Profit_Margin',
            color='Profit_Status',
            color_discrete_map={'Profitable': '#3B82F6', 'Loss-Making': '#EF4444', 'Breakeven': '#9CA3AF'},
            title="Discount Rate vs Profit Margin per Order Item",
            labels={'Discount_Percentage': 'Discount Applied (%)', 'Profit_Margin': 'Profit Margin (%)'}
        )
        fig_scatter.add_vline(x=20, line_dash="dot", line_color="orange", annotation_text="20% Warning Limit")
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Breakeven")
        fig_scatter.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.warning("""
    ### 🚨 The Core Profit Leak Revealed:
    - Transactions with **0% discount** generate an exceptional **+30.2% profit margin**.
    - Transactions with **1-15% discount** maintain a healthy **+14.8% margin**.
    - When discount exceeds **20%**, profit margins plunge into negative territory (**average -46.5% for >30% discount**).
    - In total, **$156,131 of accumulated profits were wiped out** by uncurbed discounting across 1,871 transactions!
    """)

# -------------------------------------------------------------
# TAB 5: STRATEGIC RECOMMENDATIONS
# -------------------------------------------------------------
with tab5:
    st.subheader("Executive Recommendations & Growth Playbook")
    
    st.markdown("""
    Based on our quantitative analysis, here is the 4-pillar actionable turnaround strategy for the executive leadership team:
    """)

    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        st.markdown("""
        #### 1. Implement Strict Discount Guardrails
        * **Problem:** Sales reps currently apply up to 80% discounts, causing $156k in direct profit destruction.
        * **Action:**
          - Set a hard automated cap of **15% maximum discount** at checkout without Director-level authorization.
          - Eliminate automatic discounts on low-margin furniture items (Tables and Bookcases).
        * **Financial Impact:** Recovering just 50% of discount losses adds **+$78,000 to annual net profit** (+27.2% bottom-line boost).
        """)

        st.markdown("""
        #### 2. Product Portfolio Restructuring (80/20 Rule)
        * **Problem:** Tables subcategory is losing -$17.7k and bleeding money on every unit sold.
        * **Action:**
          - Renegotiate supplier manufacturing contracts or discontinue loss-making SKUs (e.g. *Chromcraft Conference Tables*, *Bush Racetrack Table*).
          - Bundle low-margin furniture with high-margin technology/accessories (Copiers at 37% margin, Paper at 43% margin).
        * **Financial Impact:** Eradication of negative-margin lines prevents **-$22,387 annual loss**.
        """)

    with col_rec2:
        st.markdown("""
        #### 3. Regional Pricing & Freight Optimization
        * **Problem:** Central region generates $501k in sales but only 7.9% profit margin, primarily dragged down by Texas (-$25.7k) and Illinois (-$12.6k).
        * **Action:**
          - Introduce localized freight surcharge or minimum order quantities (MOQ) for bulky goods shipped to Texas and Illinois.
          - Replicate West and East operational playbooks where regional margins exceed 13.5%.
        * **Financial Impact:** Raising Central region margins from 7.9% to 12.0% yields **+$20,500 additional profit**.
        """)

        st.markdown("""
        #### 4. High-Value Customer Retention (AOV Expansion)
        * **Problem:** Corporate and Home Office customer segments exhibit higher Average Order Value ($470+) and lower price sensitivity than general Consumers.
        * **Action:**
          - Launch a B2B Loyalty & Corporate Account Manager program for top-tier enterprise clients.
          - Implement cross-sell prompts for high-margin office supplies (Paper, Envelopes, Binders).
        * **Financial Impact:** +10% increase in Corporate AOV creates **+$71,000 incremental revenue** at 17% net margin.
        """)

# -------------------------------------------------------------
# TAB 6: DATA EXPLORER
# -------------------------------------------------------------
with tab6:
    st.subheader("Cleaned Dataset Explorer")
    st.write(f"Showing {len(filtered_df):,} matching transactions based on active sidebar filters.")
    
    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp2:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )
    
    st.dataframe(
        filtered_df[['Order ID', 'Order Date', 'Customer Name', 'Segment', 'Region', 'Category', 
                     'Sub-Category', 'Product Name', 'Sales', 'Profit', 'Profit_Margin', 'Discount_Percentage']],
        use_container_width=True,
        height=500
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
    "Data Science & Analytics Internship (2026) • Task 1: Business Sales Performance Analytics • Created with Streamlit & Plotly"
    "</div>", 
    unsafe_allow_html=True
)
