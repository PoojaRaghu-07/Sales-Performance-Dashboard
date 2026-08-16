"""
Analysis and KPI Calculation Engine for Sales Performance Dashboard.

This module provides data-driven functions to calculate key business metrics:
1. Sales KPIs (Revenue, Orders, Units Sold, AOV, Estimated Profit, Estimated Margin, Customers)
2. Time-series Sales Trends (Monthly, Quarterly, Yearly)
3. Product Category & Top Product Performance
4. Regional Sales & Country Breakdown
5. Customer Purchasing & Concentration Analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate all core business KPIs from the cleaned sales dataframe.
    
    Returns:
        dict containing key performance indicators with exact values.
    """
    total_revenue = float(df['Revenue'].sum())
    total_orders = int(df['ORDERNUMBER'].nunique())
    total_units_sold = int(df['QUANTITYORDERED'].sum())
    
    # Average Order Value (Total Revenue divided by unique orders)
    aov = float(total_revenue / total_orders) if total_orders > 0 else 0.0
    
    # Estimated Profit & Margin (Cost baseline: 60% of MSRP)
    total_est_profit = float(df['Estimated_Profit'].sum())
    est_profit_margin = float((total_est_profit / total_revenue) * 100) if total_revenue > 0 else 0.0
    
    unique_customers = int(df['CUSTOMERNAME'].nunique())
    
    # Top Performing Category
    cat_sales = df.groupby('PRODUCTLINE')['Revenue'].sum()
    top_category = cat_sales.idxmax() if not cat_sales.empty else "N/A"
    top_category_rev = float(cat_sales.max()) if not cat_sales.empty else 0.0
    
    # Top Product Code
    prod_sales = df.groupby('PRODUCTCODE')['Revenue'].sum()
    top_product_code = prod_sales.idxmax() if not prod_sales.empty else "N/A"
    top_product_rev = float(prod_sales.max()) if not prod_sales.empty else 0.0
    
    # Top Performing Region (Territory)
    region_sales = df.groupby('Region')['Revenue'].sum()
    top_region = region_sales.idxmax() if not region_sales.empty else "N/A"
    top_region_rev = float(region_sales.max()) if not region_sales.empty else 0.0
    
    # Top Country
    country_sales = df.groupby('COUNTRY')['Revenue'].sum()
    top_country = country_sales.idxmax() if not country_sales.empty else "N/A"
    top_country_rev = float(country_sales.max()) if not country_sales.empty else 0.0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_units_sold": total_units_sold,
        "average_order_value": aov,
        "total_estimated_profit": total_est_profit,
        "estimated_profit_margin": est_profit_margin,
        "unique_customers": unique_customers,
        "top_category": top_category,
        "top_category_revenue": top_category_rev,
        "top_product_code": top_product_code,
        "top_product_revenue": top_product_rev,
        "top_region": top_region,
        "top_region_revenue": top_region_rev,
        "top_country": top_country,
        "top_country_revenue": top_country_rev
    }


def get_monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Group revenue and estimated profit by Year-Month for temporal analysis."""
    trend = df.groupby(['Year', 'Month', 'Year_Month']).agg(
        Revenue=('Revenue', 'sum'),
        Estimated_Profit=('Estimated_Profit', 'sum'),
        Units_Sold=('QUANTITYORDERED', 'sum'),
        Orders=('ORDERNUMBER', 'nunique'),
        Line_Items=('ORDERNUMBER', 'count')
    ).reset_index()
    
    trend['Estimated_Profit_Margin'] = (trend['Estimated_Profit'] / trend['Revenue']) * 100
    trend['AOV'] = trend['Revenue'] / trend['Orders']
    return trend.sort_values(by=['Year', 'Month'])


def get_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze performance grouped by Product Line category."""
    cat_df = df.groupby('PRODUCTLINE').agg(
        Revenue=('Revenue', 'sum'),
        Units_Sold=('QUANTITYORDERED', 'sum'),
        Orders=('ORDERNUMBER', 'nunique'),
        Estimated_Profit=('Estimated_Profit', 'sum')
    ).reset_index()
    
    cat_df['Estimated_Profit_Margin'] = (cat_df['Estimated_Profit'] / cat_df['Revenue']) * 100
    cat_df['Revenue_Share'] = (cat_df['Revenue'] / df['Revenue'].sum()) * 100
    return cat_df.sort_values(by='Revenue', ascending=False)


def get_regional_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze performance grouped by Region (Territory) and Country."""
    region_df = df.groupby(['Region', 'COUNTRY']).agg(
        Revenue=('Revenue', 'sum'),
        Units_Sold=('QUANTITYORDERED', 'sum'),
        Orders=('ORDERNUMBER', 'nunique'),
        Estimated_Profit=('Estimated_Profit', 'sum')
    ).reset_index()
    
    region_df['Estimated_Profit_Margin'] = (region_df['Estimated_Profit'] / region_df['Revenue']) * 100
    return region_df.sort_values(by='Revenue', ascending=False)


def get_top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Get Top N best-selling products by Revenue."""
    top_prod = df.groupby(['PRODUCTCODE', 'PRODUCTLINE']).agg(
        Revenue=('Revenue', 'sum'),
        Units_Sold=('QUANTITYORDERED', 'sum'),
        Avg_Price=('PRICEEACH', 'mean'),
        Estimated_Profit=('Estimated_Profit', 'sum')
    ).reset_index()
    
    top_prod['Estimated_Profit_Margin'] = (top_prod['Estimated_Profit'] / top_prod['Revenue']) * 100
    return top_prod.sort_values(by='Revenue', ascending=False).head(n)


def get_customer_analysis(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Analyze top customers by total revenue, order count, and AOV."""
    cust_df = df.groupby(['CUSTOMERNAME', 'COUNTRY', 'Region']).agg(
        Total_Revenue=('Revenue', 'sum'),
        Order_Count=('ORDERNUMBER', 'nunique'),
        Total_Units=('QUANTITYORDERED', 'sum'),
        Estimated_Profit=('Estimated_Profit', 'sum')
    ).reset_index()
    
    cust_df['AOV'] = cust_df['Total_Revenue'] / cust_df['Order_Count']
    cust_df['Estimated_Profit_Margin'] = (cust_df['Estimated_Profit'] / cust_df['Total_Revenue']) * 100
    cust_df['Revenue_Share'] = (cust_df['Total_Revenue'] / df['Revenue'].sum()) * 100
    return cust_df.sort_values(by='Total_Revenue', ascending=False).head(n)


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    try:
        from src.data_cleaning import load_raw_data, clean_sales_data
    except ImportError:
        from data_cleaning import load_raw_data, clean_sales_data
    
    df = clean_sales_data(load_raw_data())
    kpis = calculate_kpis(df)
    print("=== TEST KPI RESULTS ===")
    for k, v in kpis.items():
        if isinstance(v, float):
            print(f"  {k}: {v:,.2f}")
        else:
            print(f"  {k}: {v}")
