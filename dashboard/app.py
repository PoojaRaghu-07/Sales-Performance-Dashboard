import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as px_go
from plotly.subplots import make_subplots
import sys
import os

# Ensure src modules are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from src.data_cleaning import load_raw_data, clean_sales_data
    from src.analysis import calculate_kpis
except ImportError:
    pass

# Page Configuration
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Executive Dark Glassmorphism Styling & High Contrast Sidebar
st.markdown("""
<style>
    /* Dark Executive Palette */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* ================= SIDEBAR VISIBILITY & CONTRAST FIXES ================= */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155 !important;
    }
    
    /* Sidebar Titles and Headings */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] [data-testid="stSidebarTitle"] {
        color: #38BDF8 !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar Descriptive Text & Paragraphs */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #CBD5E1 !important;
    }
    
    /* Sidebar Widget Labels */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] .stWidgetLabel p {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Input Boxes, Selectboxes, Multiselect & Date Input Containers */
    section[data-testid="stSidebar"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-baseweb="input"],
    section[data-testid="stSidebar"] div[data-baseweb="base-input"],
    section[data-testid="stSidebar"] .stMultiSelect div[role="combobox"],
    section[data-testid="stSidebar"] .stSelectbox div[role="combobox"],
    section[data-testid="stSidebar"] .stDateInput div[data-baseweb="input"] {
        background-color: #0F172A !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    
    /* Focus and Hover State for Inputs */
    section[data-testid="stSidebar"] div[data-baseweb="select"]:hover,
    section[data-testid="stSidebar"] div[data-baseweb="input"]:hover,
    section[data-testid="stSidebar"] .stMultiSelect div[role="combobox"]:focus-within {
        border-color: #38BDF8 !important;
    }
    
    /* Input Text & Selected Options Text */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div,
    section[data-testid="stSidebar"] .stDateInput input {
        color: #F8FAFC !important;
    }
    
    /* Placeholders */
    section[data-testid="stSidebar"] input::placeholder,
    section[data-testid="stSidebar"] div[data-baseweb="select"] [aria-placeholder="true"] {
        color: #94A3B8 !important;
    }
      /* Selected Multiselect Tags - Compact & Subtle */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 4px !important;
        padding: 1px 6px !important;
        height: 22px !important;
        margin: 2px !important;
    }
    
    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #38BDF8 !important;
        font-weight: 500 !important;
        font-size: 11px !important;
    }
    
    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
        fill: #94A3B8 !important;
        width: 10px !important;
        height: 10px !important;
    }
    
    /* Icons, Dropdown Arrows, and Buttons */
    section[data-testid="stSidebar"] svg,
    section[data-testid="stSidebar"] [data-baseweb="icon"] {
        fill: #94A3B8 !important;
        color: #94A3B8 !important;
    }
    
    /* Dropdown Popups & Menus */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #1E293B !important;
        border: 1px solid #475569 !important;
    }
    
    div[data-baseweb="popover"] li,
    ul[data-baseweb="menu"] li,
    div[data-baseweb="menu"] div {
        color: #F8FAFC !important;
        background-color: #1E293B !important;
    }
    
    div[data-baseweb="popover"] li:hover,
    ul[data-baseweb="menu"] li:hover,
    ul[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #334155 !important;
        color: #38BDF8 !important;
    }

    /* Date Picker Calendar Popup */
    div[data-baseweb="calendar"] {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
    }
    
    div[data-baseweb="calendar"] button {
        color: #F8FAFC !important;
    }
    
    div[data-baseweb="calendar"] div {
        color: #CBD5E1 !important;
    }

    /* Sidebar Reset Button Styling */
    section[data-testid="stSidebar"] button {
        background-color: #0F172A !important;
        color: #38BDF8 !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        margin-top: 4px !important;
        margin-bottom: 12px !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3) !important;
    }
    
    /* ================= HEADER BANNER & MAIN APP ================= */
    .dashboard-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    
    .dashboard-title {
        color: #38BDF8;
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .dashboard-subtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 500;
        margin-top: 4px;
    }

    /* Profit Disclaimer Box */
    .profit-disclaimer {
        background: rgba(30, 41, 59, 0.7);
        border-left: 4px solid #38BDF8;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 24px;
        color: #CBD5E1;
        font-size: 13px;
    }

    /* Equal-Height Columns for KPI Row */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
    }

    /* KPI Cards - Modern Equal Height Glassmorphic Layout */
    .kpi-card {
        background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px 8px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
        width: 100%;
        height: 100% !important;
        min-height: 112px !important;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #38BDF8;
    }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 28px;
        height: 28px;
    }

    .kpi-label {
        font-size: 11px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        line-height: 1.2;
        text-align: center;
        word-break: normal;
        white-space: normal;
        margin: 0;
        padding: 0;
    }

    .kpi-value-container {
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin: 4px 0;
    }

    .kpi-value {
        font-size: clamp(15px, 1.2vw, 21px);
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1;
        white-space: nowrap;
        text-align: center;
        letter-spacing: -0.3px;
    }

    .kpi-subtext {
        font-size: 10px;
        color: #38BDF8;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():
    """Load and clean dataset with caching using deployment-safe relative path resolution."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    clean_path = os.path.join(base_dir, "data", "cleaned_sales_data.csv")
    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path, keep_default_na=False)
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
        df['Region'] = df['Region'].replace('', 'NA')
        df['TERRITORY'] = df['TERRITORY'].replace('', 'NA')
    else:
        df = clean_sales_data(load_raw_data())
    return df


df_raw = get_data()

# ================= SIDEBAR FILTERS =================
st.sidebar.image("https://img.icons8.com/color/96/000000/dashboard-layout.png", width=64)
st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("Filter sales performance across key dimensions:")

# Date / Filter Options Base Values
min_date = df_raw['ORDERDATE'].min().date()
max_date = df_raw['ORDERDATE'].max().date()
years_available = sorted([int(y) for y in df_raw['YEAR_ID'].dropna().unique()])
regions_available = sorted([str(r) for r in df_raw['Region'].unique() if r != ""])
categories_available = sorted([str(c) for c in df_raw['PRODUCTLINE'].unique() if c != ""])
deals_available = sorted([str(d) for d in df_raw['DEALSIZE'].unique() if d != ""])

# Initialize session_state defaults if not present (ALL selected by default)
if "filter_date" not in st.session_state:
    st.session_state["filter_date"] = (min_date, max_date)
if "filter_years" not in st.session_state:
    st.session_state["filter_years"] = years_available
if "filter_regions" not in st.session_state:
    st.session_state["filter_regions"] = regions_available
if "filter_categories" not in st.session_state:
    st.session_state["filter_categories"] = categories_available
if "filter_deals" not in st.session_state:
    st.session_state["filter_deals"] = deals_available

# Reset Callback Function for Clear Filters Button
def reset_all_filters():
    st.session_state["filter_date"] = (min_date, max_date)
    st.session_state["filter_years"] = years_available
    st.session_state["filter_regions"] = regions_available
    st.session_state["filter_categories"] = categories_available
    st.session_state["filter_deals"] = deals_available

# Clear Filters Button
st.sidebar.button("🔄 Clear Filters", on_click=reset_all_filters, use_container_width=True)

# 1. Date Range Filter Widget
date_range = st.sidebar.date_input(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    key="filter_date"
)

# 2. Year Multi-select Widget
selected_years = st.sidebar.multiselect(
    "Filter by Year",
    options=years_available,
    key="filter_years"
)

# 3. Region / Territory Filter Widget
selected_regions = st.sidebar.multiselect(
    "Filter by Region / Territory",
    options=regions_available,
    key="filter_regions"
)

# 4. Product Line Filter Widget
selected_categories = st.sidebar.multiselect(
    "Filter by Product Line",
    options=categories_available,
    key="filter_categories"
)

# 5. Deal Size Filter Widget
selected_deals = st.sidebar.multiselect(
    "Filter by Deal Size",
    options=deals_available,
    key="filter_deals"
)

# ================= SEQUENTIAL FILTER PIPELINE =================
filtered_df = df_raw.copy()

# Step 1: Apply Date Filter (Inclusive)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_dt = pd.to_datetime(date_range[0])
    end_dt = pd.to_datetime(date_range[1]) + pd.Timedelta(hours=23, minutes=59, seconds=59)
    filtered_df = filtered_df[
        (filtered_df['ORDERDATE'] >= start_dt) &
        (filtered_df['ORDERDATE'] <= end_dt)
    ]
elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
    start_dt = pd.to_datetime(date_range[0])
    end_dt = pd.to_datetime(date_range[0]) + pd.Timedelta(hours=23, minutes=59, seconds=59)
    filtered_df = filtered_df[
        (filtered_df['ORDERDATE'] >= start_dt) &
        (filtered_df['ORDERDATE'] <= end_dt)
    ]

# Step 2: Apply Year Filter
if selected_years:
    filtered_df = filtered_df[
        filtered_df['YEAR_ID'].astype(int).isin([int(y) for y in selected_years])
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Step 3: Apply Region / Territory Filter
if selected_regions:
    filtered_df = filtered_df[
        filtered_df['Region'].astype(str).isin([str(r) for r in selected_regions])
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Step 4: Apply Product Line Filter
if selected_categories:
    filtered_df = filtered_df[
        filtered_df['PRODUCTLINE'].astype(str).isin([str(c) for c in selected_categories])
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

# Step 5: Apply Deal Size Filter
if selected_deals:
    filtered_df = filtered_df[
        filtered_df['DEALSIZE'].astype(str).isin([str(d) for d in selected_deals])
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

df_filtered = filtered_df

# ================= DYNAMIC BUSINESS INSIGHTS ENGINE =================
def generate_dynamic_insights(df):
    """Generate 6 dynamic, data-driven business insight cards from filtered_df."""
    insights = []
    
    # 1. Sales Performance
    tot_rev = df['Revenue'].sum()
    tot_orders = df['ORDERNUMBER'].nunique()
    tot_profit = df['Estimated_Profit'].sum()
    margin = (tot_profit / tot_rev * 100) if tot_rev > 0 else 0
    
    insights.append({
        "icon": "💵",
        "title": "Revenue Performance",
        "text": f"Selected sales generated <strong>${tot_rev:,.2f}</strong> in gross revenue across <strong>{tot_orders:,}</strong> orders, with an estimated profit of <strong>${tot_profit:,.2f}</strong> ({margin:.1f}% profit margin)."
    })
    
    # 2. Top Product Line
    prod_summary = df.groupby('PRODUCTLINE')['Revenue'].sum().reset_index()
    if not prod_summary.empty:
        top_prod = prod_summary.sort_values(by='Revenue', ascending=False).iloc[0]
        top_p_name = top_prod['PRODUCTLINE']
        top_p_rev = top_prod['Revenue']
        p_pct = (top_p_rev / tot_rev * 100) if tot_rev > 0 else 0
        insights.append({
            "icon": "🏎️",
            "title": "Top Product Line",
            "text": f"<strong>{top_p_name}</strong> generated the highest revenue among selected products at <strong>${top_p_rev:,.2f}</strong>, contributing <strong>{p_pct:.1f}%</strong> of total sales."
        })
    else:
        insights.append({
            "icon": "🏎️",
            "title": "Top Product Line",
            "text": "No product line data available for the current selection."
        })
        
    # 3. Regional Leader
    reg_summary = df.groupby('Region')['Revenue'].sum().reset_index()
    if not reg_summary.empty:
        top_reg = reg_summary.sort_values(by='Revenue', ascending=False).iloc[0]
        top_r_name = top_reg['Region']
        top_r_rev = top_reg['Revenue']
        r_pct = (top_r_rev / tot_rev * 100) if tot_rev > 0 else 0
        insights.append({
            "icon": "🌍",
            "title": "Regional Leader",
            "text": f"<strong>{top_r_name}</strong> is the strongest region in the selected data, generating <strong>${top_r_rev:,.2f}</strong> in revenue (<strong>{r_pct:.1f}%</strong> share)."
        })
    else:
        insights.append({
            "icon": "🌍",
            "title": "Regional Leader",
            "text": "No regional data available for the current selection."
        })
        
    # 4. Deal Size Dominance
    deal_summary = df.groupby('DEALSIZE')['Revenue'].sum().reset_index()
    if not deal_summary.empty:
        top_deal = deal_summary.sort_values(by='Revenue', ascending=False).iloc[0]
        top_d_name = top_deal['DEALSIZE']
        top_d_rev = top_deal['Revenue']
        d_pct = (top_d_rev / tot_rev * 100) if tot_rev > 0 else 0
        insights.append({
            "icon": "💼",
            "title": "Deal Size Dominance",
            "text": f"<strong>{top_d_name}</strong> deal sizes contribute the largest share of revenue (<strong>${top_d_rev:,.2f}</strong>, or <strong>{d_pct:.1f}%</strong> of selected total)."
        })
    else:
        insights.append({
            "icon": "💼",
            "title": "Deal Size Dominance",
            "text": "No deal size data available for the current selection."
        })
        
    # 5. Customer Performance
    unique_cust = df['CUSTOMERNAME'].nunique()
    avg_rev_per_cust = (tot_rev / unique_cust) if unique_cust > 0 else 0
    top_cust_series = df.groupby('CUSTOMERNAME')['Revenue'].sum()
    top_cust_name = top_cust_series.idxmax() if not top_cust_series.empty else "N/A"
    top_cust_rev = top_cust_series.max() if not top_cust_series.empty else 0
    
    insights.append({
        "icon": "🏬",
        "title": "Customer Performance",
        "text": f"<strong>{unique_cust:,}</strong> unique customers generated selected sales (averaging <strong>${avg_rev_per_cust:,.2f}</strong> / client). Top client: <strong>{top_cust_name}</strong> (${top_cust_rev:,.2f})."
    })
    
    # 6. Sales Trend Analysis
    df_temp = df.copy()
    df_temp['Year_Month'] = df_temp['ORDERDATE'].dt.to_period('M').astype(str)
    ts_summary = df_temp.groupby('Year_Month')['Revenue'].sum().reset_index()
    
    if len(ts_summary) >= 2:
        peak_month = ts_summary.sort_values(by='Revenue', ascending=False).iloc[0]
        p_m_name = peak_month['Year_Month']
        p_m_rev = peak_month['Revenue']
        first_rev = ts_summary.iloc[0]['Revenue']
        last_rev = ts_summary.iloc[-1]['Revenue']
        trend_str = "increased" if last_rev > first_rev else ("declined" if last_rev < first_rev else "remained stable")
        insights.append({
            "icon": "📈",
            "title": "Sales Trend",
            "text": f"Across <strong>{len(ts_summary)}</strong> monthly periods, revenue peak occurred in <strong>{p_m_name}</strong> at <strong>${p_m_rev:,.2f}</strong>, with overall trend showing period revenue <strong>{trend_str}</strong>."
        })
    elif len(ts_summary) == 1:
        single_m = ts_summary.iloc[0]['Year_Month']
        single_rev = ts_summary.iloc[0]['Revenue']
        insights.append({
            "icon": "📈",
            "title": "Sales Trend",
            "text": f"Selected period covers <strong>{single_m}</strong> with a total monthly revenue of <strong>${single_rev:,.2f}</strong>."
        })
    else:
        insights.append({
            "icon": "📈",
            "title": "Sales Trend",
            "text": "Insufficient time series data to compute trend analysis."
        })
        
    return insights


# ================= HEADER BANNER =================
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">Sales Performance Dashboard</h1>
    <div class="dashboard-subtitle">Interactive Sales Analytics & Business Insights</div>
</div>
""", unsafe_allow_html=True)

# Profit Disclaimer Banner
st.markdown("""
<div class="profit-disclaimer">
    ℹ️ <strong>Cost Baseline Assumption Notice:</strong> Cost of Goods Sold (COGS) is estimated at 60% of MSRP (<code>Quantity × MSRP × 60%</code>). 
    All profit metrics are strictly presented as <strong>Estimated Profit</strong> and <strong>Estimated Profit Margin</strong>.
</div>
""", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ No records match the selected filter criteria. Please adjust your filters.")
else:
    # ================= KPI CARDS =================
    tot_rev = df_filtered['Revenue'].sum()
    tot_orders = df_filtered['ORDERNUMBER'].nunique()
    tot_units = df_filtered['QUANTITYORDERED'].sum()
    aov = tot_rev / tot_orders if tot_orders > 0 else 0
    tot_est_profit = df_filtered['Estimated_Profit'].sum()
    est_margin = (tot_est_profit / tot_rev * 100) if tot_rev > 0 else 0
    tot_cust = df_filtered['CUSTOMERNAME'].nunique()

    # Compact formatting functions for KPI cards
    def _fmt_curr(val):
        if abs(val) >= 1e6:
            return f"${val/1e6:.2f}M"
        elif abs(val) >= 1e3:
            return f"${val/1e3:.2f}K"
        else:
            return f"${val:,.0f}"

    def _fmt_vol(val):
        if abs(val) >= 1e6:
            return f"{val/1e6:.2f}M"
        elif abs(val) >= 1e3:
            return f"{val/1e3:.1f}K"
        else:
            return f"{val:,}"

    k_rev = _fmt_curr(tot_rev)
    k_orders = _fmt_vol(tot_orders)
    k_units = _fmt_vol(tot_units)
    k_aov = _fmt_curr(aov)
    k_profit = _fmt_curr(tot_est_profit)
    k_margin = f"{est_margin:.1f}%"
    k_cust = _fmt_vol(tot_cust)

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        st.markdown(f"""
        <div class="kpi-card" title="Total Revenue: ${tot_rev:,.2f}">
            <div class="kpi-header">
                <div class="kpi-label">TOTAL<br>REVENUE</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_rev}</div>
            </div>
            <div class="kpi-subtext">Gross Revenue</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card" title="Total Orders: {tot_orders:,}">
            <div class="kpi-header">
                <div class="kpi-label">TOTAL<br>ORDERS</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_orders}</div>
            </div>
            <div class="kpi-subtext">Unique Orders</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card" title="Units Sold: {tot_units:,}">
            <div class="kpi-header">
                <div class="kpi-label">UNITS<br>SOLD</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_units}</div>
            </div>
            <div class="kpi-subtext">Items Volume</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card" title="Average Order Value: ${aov:,.2f}">
            <div class="kpi-header">
                <div class="kpi-label">AVERAGE<br>ORDER</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_aov}</div>
            </div>
            <div class="kpi-subtext">AOV / Order</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-card" title="Total Estimated Profit: ${tot_est_profit:,.2f}">
            <div class="kpi-header">
                <div class="kpi-label">EST.<br>PROFIT</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_profit}</div>
            </div>
            <div class="kpi-subtext">Estimated Profit</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="kpi-card" title="Estimated Profit Margin: {est_margin:.2f}%">
            <div class="kpi-header">
                <div class="kpi-label">EST.<br>MARGIN</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_margin}</div>
            </div>
            <div class="kpi-subtext">Estimated Margin</div>
        </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="kpi-card" title="Unique Customers: {tot_cust:,}">
            <div class="kpi-header">
                <div class="kpi-label">UNIQUE<br>CUSTOMERS</div>
            </div>
            <div class="kpi-value-container">
                <div class="kpi-value">{k_cust}</div>
            </div>
            <div class="kpi-subtext">Unique Clients</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= CHARTS ROW 1: TIME SERIES & REGIONAL =================
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 12px; padding: 20px 20px 10px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 20px;">
            <div style="color: #38BDF8; font-size: 22px; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">Revenue & Estimated Profit Over Time</div>
        """, unsafe_allow_html=True)
        
        df_filtered['Year_Month'] = df_filtered['ORDERDATE'].dt.to_period('M').astype(str)
        ts_df = df_filtered.groupby('Year_Month').agg(
            Revenue=('Revenue', 'sum'),
            Estimated_Profit=('Estimated_Profit', 'sum')
        ).reset_index()
        
        fig_ts = px_go.Figure()
        fig_ts.add_trace(px_go.Scatter(
            x=ts_df['Year_Month'], y=ts_df['Revenue'],
            name='Revenue', mode='lines+markers',
            line=dict(color='#38BDF8', width=2.5),
            fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.08)'
        ))
        fig_ts.add_trace(px_go.Scatter(
            x=ts_df['Year_Month'], y=ts_df['Estimated_Profit'],
            name='Estimated Profit', mode='lines+markers',
            line=dict(color='#10B981', width=2, dash='dash')
        ))
        fig_ts.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=15, r=15, t=10, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color="#CBD5E1")),
            xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8")),
            yaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8"))
        )
        st.plotly_chart(fig_ts, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with row1_col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 12px; padding: 20px 20px 10px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 20px;">
            <div style="color: #38BDF8; font-size: 22px; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">Revenue by Region / Territory</div>
        """, unsafe_allow_html=True)
        
        reg_df = df_filtered.groupby('Region')['Revenue'].sum().reset_index()
        fig_reg = px.pie(
            reg_df, names='Region', values='Revenue',
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_reg.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=10, r=10, t=10, b=30),
            legend=dict(font=dict(size=11, color="#CBD5E1"))
        )
        st.plotly_chart(fig_reg, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= CHARTS ROW 2: PRODUCTS & CATEGORIES =================
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 12px; padding: 20px 20px 10px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 20px;">
            <div style="color: #38BDF8; font-size: 22px; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">Revenue by Product Category</div>
        """, unsafe_allow_html=True)
        
        cat_df = df_filtered.groupby('PRODUCTLINE').agg(
            Revenue=('Revenue', 'sum'),
            Estimated_Profit=('Estimated_Profit', 'sum')
        ).reset_index().sort_values(by='Revenue', ascending=True)
        
        fig_cat = px.bar(
            cat_df, y='PRODUCTLINE', x='Revenue',
            orientation='h',
            text_auto='.2s',
            color='Revenue',
            color_continuous_scale='Viridis'
        )
        fig_cat.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=15, r=15, t=10, b=30),
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8")),
            yaxis=dict(tickfont=dict(size=10, color="#94A3B8"))
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with row2_col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 12px; padding: 20px 20px 10px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 20px;">
            <div style="color: #38BDF8; font-size: 22px; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">Top 10 Best-Selling Products (SKUs)</div>
        """, unsafe_allow_html=True)
        
        top_prod_df = df_filtered.groupby(['PRODUCTCODE', 'PRODUCTLINE'])['Revenue'].sum().reset_index()
        top_prod_df = top_prod_df.sort_values(by='Revenue', ascending=False).head(10)
        top_prod_df = top_prod_df.sort_values(by='Revenue', ascending=True)
        
        fig_prod = px.bar(
            top_prod_df, y='PRODUCTCODE', x='Revenue',
            color='PRODUCTLINE', orientation='h',
            text_auto='.2s'
        )
        fig_prod.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=15, r=15, t=10, b=30),
            legend=dict(font=dict(size=10, color="#CBD5E1")),
            xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8")),
            yaxis=dict(tickfont=dict(size=10, color="#94A3B8"))
        )
        st.plotly_chart(fig_prod, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= CHARTS ROW 3: CUSTOMERS & DEAL SIZES =================
    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 12px; padding: 20px 20px 10px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 20px;">
            <div style="color: #38BDF8; font-size: 22px; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">Top 10 Customers by Revenue</div>
        """, unsafe_allow_html=True)
        
        cust_df = df_filtered.groupby(['CUSTOMERNAME', 'COUNTRY'])['Revenue'].sum().reset_index()
        cust_df = cust_df.sort_values(by='Revenue', ascending=False).head(10).sort_values(by='Revenue', ascending=True)
        
        fig_cust = px.bar(
            cust_df, y='CUSTOMERNAME', x='Revenue',
            color='COUNTRY', orientation='h',
            text_auto='.2s'
        )
        fig_cust.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=15, r=15, t=10, b=30),
            legend=dict(font=dict(size=10, color="#CBD5E1")),
            xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8")),
            yaxis=dict(tickfont=dict(size=10, color="#94A3B8"))
        )
        st.plotly_chart(fig_cust, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with row3_col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 12px; padding: 20px 20px 10px 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); margin-bottom: 20px;">
            <div style="color: #38BDF8; font-size: 22px; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">Deal Size Breakdown</div>
        """, unsafe_allow_html=True)
        
        deal_df = df_filtered.groupby('DEALSIZE')['Revenue'].sum().reset_index()
        fig_deal = px.pie(
            deal_df, names='DEALSIZE', values='Revenue',
            color_discrete_sequence=px.colors.sequential.Electric
        )
        fig_deal.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=10, r=10, t=10, b=30),
            legend=dict(font=dict(size=11, color="#CBD5E1"))
        )
        st.plotly_chart(fig_deal, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ================= DYNAMIC BUSINESS INSIGHTS CARDS =================
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 Business Insights")
    insights = generate_dynamic_insights(df_filtered)
    
    b_col1, b_col2, b_col3 = st.columns(3)
    for idx, ins in enumerate(insights):
        target_col = [b_col1, b_col2, b_col3][idx % 3]
        with target_col:
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%); border: 1px solid #334155; border-radius: 10px; padding: 16px; margin-bottom: 16px; min-height: 135px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 20px;">{ins['icon']}</span>
                    <span style="color: #38BDF8; font-weight: 700; font-size: 15px;">{ins['title']}</span>
                </div>
                <div style="color: #CBD5E1; font-size: 13px; line-height: 1.5;">
                    {ins['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ================= DATA TABLE & EXPORT =================
    st.subheader("📋 Filtered Transaction Data Explorer")
    with st.expander("View Filtered Data Table & Export CSV", expanded=False):
        st.dataframe(df_filtered, use_container_width=True)
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Dataset (CSV)",
            data=csv_data,
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )
