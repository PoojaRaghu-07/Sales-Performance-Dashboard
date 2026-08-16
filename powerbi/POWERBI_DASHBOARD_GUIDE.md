# Power BI Dashboard Implementation Guide

## Executive Summary: Sales Performance Executive Summary

This guide provides step-by-step instructions to recreate the single-page Power BI dashboard: **Sales Performance Executive Summary**.

Source Dataset File:
`powerbi/cleaned_sales_data_powerbi.csv`

---

## 1. Overview

The **Sales Performance Executive Summary** is a single-page, dark-blue sales analytics dashboard created in Microsoft Power BI Desktop. It features 6 KPI cards, 5 core visuals, and 5 interactive dropdown slicers to deliver executive-level commercial insights.

---

## 2. Dataset Import

1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Select `powerbi/cleaned_sales_data_powerbi.csv` and click **Open**.
4. In the preview window:
   - **File Origin**: `65001: Unicode (UTF-8)`
   - **Delimiter**: `Comma`
   - **Data Detection**: `Based on first 200 rows`
5. Click **Transform Data** to inspect column data types, then click **Close & Apply**.

*Note: `cleaned_sales_data_powerbi.csv` is the source dataset and must not be modified by this documentation update.*

---

## 3. Theme Import

To import the custom dark-blue theme:
1. Navigate to the **View** tab in Power BI Desktop.
2. Click **Themes** > **Browse for themes**.
3. Select `powerbi/theme.json`.
4. Page canvas background (`#0F172A`), visual container background (`#1E293B`), text colors, and data palettes will apply automatically.

---

## 4. DAX Measures

Create a dedicated measures table named `_Measures` and enter these exact DAX formulas:

```dax
Total Revenue = SUM(cleaned_sales_data_powerbi[Revenue])
```

```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

```dax
Total Estimated Profit = SUM(cleaned_sales_data_powerbi[Estimated_Profit])
```

```dax
Estimated Profit Margin = DIVIDE([Total Estimated Profit], [Total Revenue], 0)
```

```dax
Total Orders = DISTINCTCOUNT(cleaned_sales_data_powerbi[ORDERNUMBER])
```

```dax
Unique Customers = DISTINCTCOUNT(cleaned_sales_data_powerbi[CUSTOMERNAME])
```

```dax
Total Estimated Cost = SUM(cleaned_sales_data_powerbi[Estimated_Cost])
```

---

## 5. KPI Configuration

Configure the 6 visible KPI cards across the top row of the **Executive Summary** page:

1. **Total Revenue**
   - **Visual**: Card
   - **Field**: `[Total Revenue]`
   - **Unfiltered Reference Value**: `10.03M` (`$10,032,628.85`)
   - **Format**: Currency (`$`), Display units = Auto

2. **Average Order Value**
   - **Visual**: Card
   - **Field**: `[Average Order Value]`
   - **Unfiltered Reference Value**: `32.68K` (`$32,679.57`)
   - **Format**: Currency (`$`), Display units = Thousands (`K`)

3. **Total Estimated Profit**
   - **Visual**: Card
   - **Field**: `[Total Estimated Profit]`
   - **Unfiltered Reference Value**: `4.03M` (`$4,034,223.65`)
   - **Format**: Currency (`$`), Display units = Auto

4. **Estimated Profit Margin**
   - **Visual**: Card
   - **Field**: `[Estimated Profit Margin]`
   - **Unfiltered Reference Value**: `40.21%`
   - **Format**: Percentage (`0.00%`)

5. **Total Orders**
   - **Visual**: Card
   - **Field**: `[Total Orders]`
   - **Unfiltered Reference Value**: `307`
   - **Format**: Whole Number (`307`)

6. **Unique Customers**
   - **Visual**: Card
   - **Field**: `[Unique Customers]`
   - **Unfiltered Reference Value**: `92`
   - **Format**: Whole Number (`92`)

*(Note: These numbers represent reference values for the unfiltered dataset. They will update dynamically when slicers are filtered).*

---

## 6. Chart Configuration

Configure the 5 visible charts on the dashboard:

1. **Revenue Trend Over Time**
   - **Visual Type**: Line Chart
   - **X-axis**: `Year` (Displays years: 2003, 2004, 2005)
   - **Y-axis**: `Revenue` (or `[Total Revenue]`)
   - **Title**: "Revenue Trend Over Time"

2. **Revenue by Region / Territory**
   - **Visual Type**: Horizontal Bar Chart
   - **Y-axis / Category**: `Region`
   - **X-axis / Value**: `Revenue` (or `[Total Revenue]`)
   - **Title**: "Revenue by Region / Territory"

3. **Revenue by Deal Size**
   - **Visual Type**: Column Chart
   - **X-axis / Category**: `DEALSIZE` (Medium, Small, Large)
   - **Y-axis / Value**: `Revenue` (or `[Total Revenue]`)
   - **Title**: "Revenue by Deal Size"

4. **Revenue by Product Line**
   - **Visual Type**: Donut Chart
   - **Legend / Category**: `PRODUCTLINE`
   - **Values**: `Revenue` (or `[Total Revenue]`)
   - **Title**: "Revenue by Product Line"

5. **Top 10 Products by Revenue**
   - **Visual Type**: Horizontal Bar Chart
   - **Y-axis / Category**: `PRODUCTCODE`
   - **X-axis / Value**: `Revenue` (or `[Total Revenue]`)
   - **Title**: "Top 10 Products by Revenue"

---

## 7. Top 10 Products Configuration

Follow this exact procedure to configure the Top 10 Products chart:

1. Create a **Horizontal Bar Chart**.
2. Drag `PRODUCTCODE` to the **Y-axis** field well.
3. Drag `Revenue` (or `[Total Revenue]`) to the **X-axis** field well.
4. Open the **Filters** pane on the right side of the canvas.
5. Expand `PRODUCTCODE`.
6. Set **Filter type** to `Top N`.
7. Set **Show items** to `Top`.
8. Enter `10` in the items box.
9. Drag `Revenue` (or `[Total Revenue]`) into the **By value** box.
10. Click **Apply filter**.
11. Sort the chart by `Revenue` descending.

---

## 8. Slicer Configuration

Add 5 dropdown-style slicers to the dashboard:

1. **Year**: Field = `cleaned_sales_data_powerbi[Year]` (Dropdown)
2. **Region**: Field = `cleaned_sales_data_powerbi[Region]` (Dropdown)
3. **PRODUCTLINE**: Field = `cleaned_sales_data_powerbi[PRODUCTLINE]` (Dropdown)
4. **DEALSIZE**: Field = `cleaned_sales_data_powerbi[DEALSIZE]` (Dropdown)
5. **ORDERDATE**: Field = `cleaned_sales_data_powerbi[ORDERDATE]` (Dropdown)

**Default State**: All items selected (`All`). Slicers cross-filter all 6 KPI cards and 5 charts dynamically.

---

## 9. Page Layout

- **Page Name**: `Executive Summary`
- **Header Title**: "Sales Performance Executive Summary"
- **Top Row**: 6 KPI Cards arranged horizontally side-by-side.
- **Middle Section**:
  - `Revenue Trend Over Time` (Line Chart)
  - `Revenue by Region / Territory` (Horizontal Bar Chart)
  - `Revenue by Deal Size` (Column Chart)
- **Bottom Section**:
  - `Revenue by Product Line` (Donut Chart)
  - `Top 10 Products by Revenue` (Horizontal Bar Chart)
- **Sidebar / Header**: 5 Dropdown Slicers (`Year`, `Region`, `PRODUCTLINE`, `DEALSIZE`, `ORDERDATE`).

*(Note: The completed Power BI dashboard contains strictly 1 page: Executive Summary. Do not document Pages 2 or 3).*

---

## 10. Estimated Profit Methodology

The source transaction dataset does not contain actual historical accounting cost or net profit figures.

- **Cost Baseline Assumption**:
  $$\text{Estimated Cost} = \text{QUANTITYORDERED} \times \text{MSRP} \times 60\%$$

- **Estimated Profit**:
  $$\text{Estimated Profit} = \text{Revenue} - \text{Estimated Cost}$$

- **Estimated Profit Margin**:
  $$\text{Estimated Profit Margin} = \frac{\text{Estimated Profit}}{\text{Revenue}}$$

**Strict Wording Requirement**:
Never use "Profit" or "Profit Margin" as standalone labels.
Always use "Estimated Profit" and "Estimated Profit Margin".
Never describe these metrics as Actual Profit, Actual Profit Margin, or Net Profit.

---

## 11. Formatting Guidance & Readability

- **Page Canvas Background**: Dark Navy `#0F172A`
- **Visual Container Background**: Dark Blue `#1E293B`
- **Visual Borders**: Slate `#334155` (Radius = 8)
- **Chart Titles**: Cyan `#38BDF8` (Segoe UI Semibold, 12pt)
- **KPI Values**: White `#F8FAFC` (Segoe UI Bold, 20pt)
- **KPI Labels**: Slate-Gray `#94A3B8` (Segoe UI, 10pt)
- **Slicer Header**: Cyan `#38BDF8`
- **Slicer Input Text**: White `#F8FAFC` on Dark Background `#0F172A`

---

## 12. Verification Checklist

- [x] Documented exactly 1 completed page: **Executive Summary**.
- [x] Dashboard Title set to **Sales Performance Executive Summary**.
- [x] Documented 6 KPI cards (`Total Revenue`, `Average Order Value`, `Total Estimated Profit`, `Estimated Profit Margin`, `Total Orders`, `Unique Customers`).
- [x] Documented 5 charts (`Revenue Trend Over Time`, `Revenue by Region / Territory`, `Revenue by Deal Size`, `Revenue by Product Line`, `Top 10 Products by Revenue`).
- [x] Documented `Revenue Trend Over Time` with Year X-axis (not monthly).
- [x] Step-by-step Top N = 10 filter procedure documented for `PRODUCTCODE`.
- [x] Documented 5 dropdown slicers (`Year`, `Region`, `PRODUCTLINE`, `DEALSIZE`, `ORDERDATE`).
- [x] Slicer default state (`All`) and interactive filter updates documented.
- [x] Profit methodology explicitly explained with 60% MSRP estimated-cost baseline.
- [x] Strict **Estimated Profit** and **Estimated Profit Margin** terminology enforced throughout.
- [x] Dark blue theme colors and contrast readability rules documented.
- [x] Zero company or internship references included.
