"""
Data Cleaning and Preprocessing Module for Sales Performance Dashboard.

This module handles:
1. Loading raw dataset (data/sales_data_sample.csv)
2. Handling missing values (e.g. mapping USA/Canada to 'NA' territory)
3. Date conversions and derived temporal columns (Year, Month, Quarter)
4. Derived financial columns (Revenue, Estimated Cost, Estimated Profit, Estimated Profit Margin)
   NOTE: Cost baseline is estimated at 60% of MSRP. These metrics are strictly labeled
   as Estimated Profit and Estimated Profit Margin.
5. Exporting processed dataset to data/cleaned_sales_data.csv and powerbi/cleaned_sales_data_powerbi.csv.
"""

import pandas as pd
import numpy as np
import os


def load_raw_data(file_path: str = "data/sales_data_sample.csv") -> pd.DataFrame:
    """Load the raw sales dataset with fallback encoding handling and deployment-safe path resolution."""
    if not os.path.isabs(file_path):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        possible_path = os.path.join(base_dir, file_path)
        if os.path.exists(possible_path):
            file_path = possible_path

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found at path: {file_path}")
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
    
    return df


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw sales dataframe, handle missing values, and compute derived columns.
    
    Returns:
        pd.DataFrame: Processed clean sales dataset.
    """
    df = df.copy()
    
    # 1. Clean Date Column
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
    
    # 2. Derived Temporal Columns
    df['Year'] = df['ORDERDATE'].dt.year
    df['Month'] = df['ORDERDATE'].dt.month
    df['Quarter'] = df['ORDERDATE'].dt.quarter
    df['Month_Name'] = df['ORDERDATE'].dt.strftime('%B')
    df['Quarter_Name'] = 'Q' + df['Quarter'].astype(str)
    df['Year_Month'] = df['ORDERDATE'].dt.to_period('M').astype(str)
    
    # 3. Standardize Missing Location Values
    # USA and Canada missing territory values are assigned 'NA' (North America)
    country_territory_map = {
        'USA': 'NA',
        'Canada': 'NA'
    }
    df['TERRITORY'] = df['TERRITORY'].fillna(df['COUNTRY'].map(country_territory_map))
    df['TERRITORY'] = df['TERRITORY'].fillna('Other')
    df['Region'] = df['TERRITORY']
    
    df['ADDRESSLINE2'] = df['ADDRESSLINE2'].fillna('N/A')
    df['STATE'] = df['STATE'].fillna('N/A')
    df['POSTALCODE'] = df['POSTALCODE'].fillna('N/A')
    
    # 4. Derived Financial Columns
    # Revenue is given by SALES
    df['Revenue'] = df['SALES']
    
    # Cost Baseline Assumption: COGS estimated at 60% of MSRP * QUANTITYORDERED
    # Strictly labeled as Estimated_Cost, Estimated_Profit, and Estimated_Profit_Margin
    df['Estimated_Cost'] = df['QUANTITYORDERED'] * df['MSRP'] * 0.60
    df['Estimated_Profit'] = df['Revenue'] - df['Estimated_Cost']
    df['Estimated_Profit_Margin'] = np.where(
        df['Revenue'] > 0,
        (df['Estimated_Profit'] / df['Revenue']) * 100,
        0.0
    )
    
    # 5. Derived Categorical Columns
    # Sales Category / Deal Classification
    conditions = [
        (df['SALES'] < 3000),
        (df['SALES'] >= 3000) & (df['SALES'] < 6000),
        (df['SALES'] >= 6000)
    ]
    choices = ['Low', 'Medium', 'High']
    df['SALES_CATEGORY'] = np.select(conditions, choices, default='Medium')
    
    return df


def save_cleaned_datasets(df: pd.DataFrame, 
                          clean_path: str = "data/cleaned_sales_data.csv",
                          powerbi_path: str = "powerbi/cleaned_sales_data_powerbi.csv") -> None:
    """Save cleaned dataset to target paths."""
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    os.makedirs(os.path.dirname(powerbi_path), exist_ok=True)
    
    # Standard format with string dates for maximum portability
    df_export = df.copy()
    df_export['ORDERDATE'] = df_export['ORDERDATE'].dt.strftime('%Y-%m-%d')
    
    df_export.to_csv(clean_path, index=False)
    df_export.to_csv(powerbi_path, index=False)
    print(f"Saved cleaned dataset ({len(df_export)} rows) to:\n  - {clean_path}\n  - {powerbi_path}")


if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df = clean_sales_data(raw_df)
    save_cleaned_datasets(cleaned_df)
