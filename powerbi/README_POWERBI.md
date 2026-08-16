# Power BI Dashboard

## Overview

**Sales Performance Executive Summary** is a dark-blue executive sales analytics dashboard built in Microsoft Power BI Desktop. It provides commercial sales visibility across revenue trends over time, regional territory distribution, deal size categories, product line dominance, top SKUs, and estimated profitability metrics.

---

## Files

1. **`cleaned_sales_data_powerbi.csv`**: Source dataset containing 2,823 transaction records across 37 columns. *Note: `cleaned_sales_data_powerbi.csv` is the dataset and must not be modified by this documentation update.*
2. **`POWERBI_DASHBOARD_GUIDE.md`**: Implementation guide detailing DAX measures, card layouts, chart setups, Top 10 filter steps, and layout specifications.
3. **`README_POWERBI.md`**: Resource overview and documentation index.
4. **`theme.json`**: Dark-blue visual theme file for Power BI Desktop.

---

## Dashboard Contents

### Page: Executive Summary

### KPI Cards (6 Visible Cards)
- **Total Revenue**: Total gross commercial revenue (`10.03M` / `$10,032,628.85`).
- **Average Order Value**: Average revenue per purchase order (`32.68K` / `$32,679.57`).
- **Total Estimated Profit**: Total profit derived from cost assumption (`4.03M` / `$4,034,223.65`).
- **Estimated Profit Margin**: Profit margin percentage (`40.21%`).
- **Total Orders**: Distinct purchase order count (`307`).
- **Unique Customers**: Distinct B2B customer account count (`92`).

*(Note: These values represent reference numbers for the unfiltered dataset).*

### Charts (5 Visible Visuals)
1. **Revenue Trend Over Time**: Line chart tracking Revenue over Year (2003, 2004, 2005).
2. **Revenue by Region / Territory**: Horizontal bar chart analyzing revenue by Region/Territory.
3. **Revenue by Deal Size**: Column chart displaying revenue across Medium, Small, and Large deal sizes.
4. **Revenue by Product Line**: Donut chart illustrating revenue share across product categories.
5. **Top 10 Products by Revenue**: Horizontal bar chart displaying top 10 SKUs by `PRODUCTCODE`.

### Filters (5 Dropdown Slicers)
1. **Year**: Dropdown slicer for filtering by transaction year.
2. **Region**: Dropdown slicer for filtering by geographic region.
3. **PRODUCTLINE**: Dropdown slicer for filtering by product line.
4. **DEALSIZE**: Dropdown slicer for filtering by deal size tier.
5. **ORDERDATE**: Dropdown date range slicer.

*Default state for all slicers: All selected (`All`).*

---

## Estimated Profit Methodology

The raw transaction dataset does not contain actual historical accounting cost or net profit figures.
- **Estimated Cost**: Calculated as `QUANTITYORDERED × MSRP × 60%`.
- **Estimated Profit**: Derived as `Revenue - Estimated_Cost`.
- **Estimated Profit Margin**: Derived as `(Estimated_Profit / Revenue) × 100`.

All profit metrics are strictly presented and labeled as **Estimated Profit** and **Estimated Profit Margin**.

---

## Theme

The dashboard utilizes the **Dark Blue Modern Business** theme (`powerbi/theme.json`):
- **Page Background**: Dark Navy `#0F172A`
- **Visual Containers**: Dark Blue `#1E293B`
- **Borders**: Slate `#334155` (Radius = 8)
- **Chart Titles**: Cyan `#38BDF8`
- **KPI Values**: White `#F8FAFC`
- **KPI Labels**: Slate-Gray `#94A3B8`
- **Slicer Text**: White `#F8FAFC` on Dark Background `#0F172A`
- **Secondary Palette**: Green `#10B981`, Amber `#F59E0B`, Purple `#8B5CF6`, Pink `#EC4899`, Indigo `#6366F1`, Teal `#14B8A6`, Rose `#F43F5E`

---

## Setup Instructions

1. **Get Data**: Open Power BI Desktop, click **Get Data** > **Text/CSV** > Select `powerbi/cleaned_sales_data_powerbi.csv`.
2. **Apply Theme**: Navigate to **View** > **Themes** > **Browse for themes** > Select `powerbi/theme.json`.
3. **Create DAX Measures**: Add the 6 core DAX measures as documented in [`POWERBI_DASHBOARD_GUIDE.md`](./POWERBI_DASHBOARD_GUIDE.md).
4. **Build KPI Cards**: Create the 6 KPI cards across the top row.
5. **Build Charts**: Create the 5 core visuals using exact field mappings and Top N = 10 filter configuration.
6. **Add Slicers**: Add the 5 dropdown slicers.
7. **Verify Dashboard**: Check slicer interactions and visual alignment against reference values.
