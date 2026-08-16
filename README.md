# Sales Performance Dashboard

**Kinetrexa Data Analytics Internship Task 1**  
**Author**: Pooja R  

---

## 📌 Project Overview
The **Sales Performance Dashboard** is an enterprise-grade commercial analytics solution built for **Kinetrexa**. This project provides interactive visualization, statistical exploratory analysis, and commercial insights derived from an actual B2B sales dataset spanning orders from January 2003 through May 2005.

The solution equips commercial leaders, sales managers, and executive decision-makers with interactive dashboards (Streamlit & Power BI), an automated ETL pipeline, an exploratory Jupyter Notebook, and a executive PDF insights report.

---

## 🎯 Business Objective
- **Evaluate Enterprise Sales Metrics**: Measure Total Revenue, Total Orders, Units Sold, Average Order Value (AOV), and Customer Account volume.
- **Analyze Demand Seasonality**: Uncover monthly and quarterly revenue fluctuations, identifying high-demand sales cycles.
- **Product Portfolio Optimization**: Assess performance across product lines (Classic Cars, Vintage Cars, Motorcycles, etc.) and individual SKUs.
- **Geographic Sales Breakdown**: Track regional sales distribution across Europe, Middle East & Africa (EMEA), North America (NA), Asia-Pacific (APAC), and Japan.
- **Customer Account & Deal Size Insights**: Evaluate top B2B corporate customers and deal size distributions (Small, Medium, Large).
- **Formulate Data-Grounded Strategies**: Provide actionable business recommendations grounded strictly in empirical calculated results.

---

## 📊 Dataset Description
- **Source File**: `data/sales_data_sample.csv` (2,823 transaction line items × 25 columns)
- **Timeframe**: January 2003 – May 2005
- **Key Columns**:
  - `ORDERNUMBER`: Unique order identifier (307 unique purchase orders)
  - `QUANTITYORDERED`: Number of units purchased per order line item
  - `PRICEEACH`: Unit selling price
  - `SALES`: Total revenue for the line item (`QUANTITYORDERED * price_actual`)
  - `ORDERDATE`: Date of transaction
  - `PRODUCTLINE`: High-level product category (7 categories)
  - `PRODUCTCODE`: Specific item SKU (109 unique SKUs)
  - `MSRP`: Manufacturer's Suggested Retail Price
  - `CUSTOMERNAME`: B2B corporate account name (92 unique accounts)
  - `COUNTRY`, `TERRITORY`, `CITY`: Geographic location fields
  - `DEALSIZE`: Deal scale classification (`Small`, `Medium`, `Large`)

> [!IMPORTANT]
> **Profit Calculation & Cost Baseline Assumption**:  
> The raw dataset does not contain explicit cost or profit records. Cost of Goods Sold (COGS) is estimated at **60% of MSRP** (`QUANTITYORDERED * MSRP * 0.60`). All profit metrics across the project are strictly labeled as **Estimated Profit** and **Estimated Profit Margin**.

---

## 🧹 Data Cleaning & Preprocessing

The preprocessing module (`src/data_cleaning.py`) cleans and transforms raw transactions:

1. **Date Parsing**: Converted string timestamps into pandas `datetime64` format (`YYYY-MM-DD`).
2. **Missing Value Imputation**:
   - Mapped missing `TERRITORY` values for `USA` and `Canada` to `'NA'` (North America).
   - Filled missing string fields (`STATE`, `ADDRESSLINE2`, `POSTALCODE`) with `'N/A'`.
3. **Temporal Feature Engineering**: Derived `Year`, `Month`, `Quarter`, `Month_Name`, `Quarter_Name`, and `Year_Month`.
4. **Financial Metrics Calculation**:
   - `Revenue` = `SALES`
   - `Estimated_Cost` = `QUANTITYORDERED * MSRP * 0.60`
   - `Estimated_Profit` = `Revenue - Estimated_Cost`
   - `Estimated_Profit_Margin` = `(Estimated_Profit / Revenue) * 100`
5. **Data Export**: Saved normalized cleaned dataset to `data/cleaned_sales_data.csv` and `powerbi/cleaned_sales_data_powerbi.csv`.

---

## 📈 Key Performance Indicators (KPI Summary)

| Metric | Empirical Value | Context & Notes |
| :--- | :--- | :--- |
| **Total Revenue** | **$10,032,628.85** | Total sales revenue across 2,823 transaction line items |
| **Total Orders** | **307** | Unique B2B purchase orders processed |
| **Total Units Sold** | **99,067** | Total volume of physical product units delivered |
| **Average Order Value (AOV)** | **$32,679.57** | Revenue generated per unique purchase order |
| **Total Estimated Profit** | **$4,034,223.65** | Derived assuming COGS at 60% of MSRP |
| **Estimated Profit Margin** | **40.21%** | Overall commercial estimated profit margin |
| **Total Unique Customers** | **92** | Corporate B2B purchasing clients |
| **Top Product Line** | **Classic Cars** | **$3,919,615.66** revenue (39.07% market share) |
| **Top Product Code (SKU)** | **S18_3232** | **$288,245.42** revenue across 52 orders |
| **Top Region (Territory)** | **EMEA** | **$4,979,272.41** revenue (49.63% regional share) |
| **Top Country** | **USA** | **$3,627,982.83** revenue (36.16% country share) |

---

## 🖥️ Dashboard Features

### 1. Streamlit Interactive Dashboard (`dashboard/app.py`)
- **Executive Styling**: Glassmorphic dark palette built with custom CSS.
- **Top KPI Cards**: Total Revenue, Total Orders, Units Sold, Average Order Value, Total Estimated Profit, Estimated Profit Margin %, Unique Customers.
- **Interactive Sidebar Filters**:
  - Date Range Picker & Year Filter
  - Territory / Region Multi-select (`EMEA`, `NA`, `APAC`, `Japan`)
  - Product Line Category Multi-select
  - Deal Size Classification Filter (`Small`, `Medium`, `Large`)
- **Plotly Visualizations**:
  - Revenue & Estimated Profit Over Time (Line + Area trend chart)
  - Sales by Region & Territory (Donut Chart)
  - Revenue by Product Category (Horizontal Bar Chart)
  - Top 10 Best-Selling Products (Color-coded Bar Chart)
  - Top 10 Corporate Customers (Horizontal Bar Chart)
  - Deal Size Breakdown (Pie Chart)
- **Dynamic Interactivity**: All charts update in real time when filters change.
- **Data Export**: Integrated CSV dataset viewer and download button.

### 2. Power BI Package (`powerbi/`)
- `cleaned_sales_data_powerbi.csv`: Power BI-optimized clean dataset.
- `README_POWERBI.md`: Complete step-by-step import guide, DAX calculated measures (`Total Revenue`, `Total Orders`, `AOV`, `Estimated Profit`, `Estimated Profit Margin %`), dashboard layout pages, slicer configurations, and visual formatting rules.

---

## 💡 Main Business Insights

1. **November & Q4 Demand Spike**: November is overwhelmingly the highest sales month with **$2,118,885.67** (21.12% of total revenue). Combined Q4 sales generate over 38.6% of annual commercial revenue, reflecting strong holiday distributor pre-stocking.
2. **Classic Cars Portfolio Dominance**: `Classic Cars` is the leading category at **$3,919,615.66** (39.07% share), followed by `Vintage Cars` ($1.90M) and `Motorcycles` ($1.17M). `Trains` represents the lowest category at **$226,243.00** (2.25% share).
3. **Regional Market Concentration**: `EMEA` represents the largest regional market at **$4,979,272.41** (49.63% share), followed by `North America` (`NA`) at **$3,855,873.71** (38.43%). `APAC` ($715K) and `Japan` ($482K) present untapped growth opportunities.
4. **Key Account Concentration**: Top customer `Euro Shopping Channel` generates **$912,294.05** (9.09% of total revenue). The top 5 customers generate **25.76%** of total commercial revenue.
5. **Medium Deal Dominance**: Medium deals ($3,000–$6,000) account for **$6,087,432.24** (60.68% of total sales revenue).

---

## 🛠️ Technologies Used
- **Language**: Python 3.14
- **Data Manipulation**: Pandas, NumPy
- **Data Visualization**: Matplotlib, Seaborn, Plotly Express
- **Web Application Framework**: Streamlit
- **Business Intelligence**: Microsoft Power BI
- **PDF Generation**: ReportLab
- **Environment & Notebook**: Jupyter Notebook, OpenPyXL

---

## 📁 Project Structure

```
sales-performance-dashboard/
│
├── data/
│   ├── sales_data_sample.csv           # Original raw sales dataset
│   └── cleaned_sales_data.csv          # Cleaned, preprocessed CSV dataset
│
├── notebooks/
│   └── Sales_Performance_Analysis.ipynb# Fully executed 13-section analysis notebook
│
├── dashboard/
│   └── app.py                          # Streamlit interactive dashboard application
│
├── src/
│   ├── __init__.py                     # Package initializer
│   ├── data_cleaning.py                # Preprocessing and ETL pipeline module
│   └── analysis.py                     # KPI and analytical calculation module
│
├── powerbi/
│   ├── cleaned_sales_data_powerbi.csv  # Power BI dashboard dataset
│   └── README_POWERBI.md               # Power BI setup, DAX measures & layout guide
│
├── reports/
│   ├── business_insights.md            # Markdown executive insights report
│   └── Business_Insights_Report.pdf    # Multi-page executive PDF report
│
├── requirements.txt                    # Project Python dependencies
├── README.md                           # Master project documentation
└── .gitignore                          # Git tracking exclusions file
```

---

## 🚀 Installation & Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone / Open Workspace
```bash
cd sales-performance-dashboard
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Project

### 1. Run Data Preprocessing & Pipeline Verification
```bash
python src/data_cleaning.py
python src/analysis.py
```

### 2. Run the Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
The dashboard will launch automatically in your default web browser at `http://localhost:8501`.

### 3. Open the Jupyter Notebook
```bash
jupyter notebook notebooks/Sales_Performance_Analysis.ipynb
```

---

## 🔮 Future Enhancements
1. **Predictive Sales Forecasting**: Integrate Prophet or ARIMA time-series models to predict Q4 inventory demand.
2. **Customer Churn & LTV Analysis**: Compute Customer Lifetime Value (CLV) and recency-frequency-monetary (RFM) segmentation models.
3. **Automated Data Pipeline**: Deploy ETL pipeline as an automated Airflow or GitHub Action workflow.

---

**Author**: Pooja R  
**Kinetrexa Data Analytics Internship Task 1**
