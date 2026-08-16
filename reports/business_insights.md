# Sales Performance & Business Insights Report

**Student Project Report**  
**Author:** Pooja R  
**Project:** Sales Performance Analysis  
**Focus:** Data Analysis & Power BI  

---

## 1. Executive Summary

This project presents an independent sales performance analysis using the commercial transaction dataset `powerbi/cleaned_sales_data_powerbi.csv` spanning historical sales from January 2003 through May 2005. 

The dataset contains:
- **2,823** transaction line items
- **307** unique purchase orders
- **$10,032,628.85** total commercial revenue
- **92** unique corporate customer accounts
- Historical sales from January 2003 through May 2005

The analysis is fully aligned with the finalized Power BI dashboard **“Sales Performance Executive Summary”** (Page: `Executive Summary`).

![Figure 1. Sales Performance Executive Summary dashboard.](dashboard.png)
*Figure 1. Sales Performance Executive Summary dashboard.*

> ℹ️ **Profit Estimation Methodology Notice**: The source dataset does not contain actual historical accounting cost or net profit figures. Cost of Goods Sold (COGS) is estimated at **60% of MSRP** (`QUANTITYORDERED × MSRP × 60%`). 
> 
> Therefore, all profitability values must be explicitly called **Estimated Profit** and **Estimated Profit Margin**. They should not be interpreted as actual accounting profit.

---

## 2. Key Performance Indicators (KPI Summary)

The primary KPI metrics below correspond directly to the 6 visible KPI cards on the **Sales Performance Executive Summary** Power BI dashboard:

| KPI Metric | Unfiltered Value | Metric Explanation / Scope |
| :--- | ---: | :--- |
| **Total Revenue** | **$10,032,628.85** | Cumulative sales revenue generated across all 2,823 transaction records. |
| **Average Order Value** | **$32,679.57** | Average revenue generated per unique purchase order ($10.03M / 307 orders). |
| **Total Estimated Profit** | **$4,034,223.65** | Cumulative estimated profit derived from the 60% MSRP cost baseline assumption. |
| **Estimated Profit Margin** | **40.21%** | Overall estimated commercial profit margin percentage across total revenue. |
| **Total Orders** | **307** | Distinct count of purchase orders processed (`ORDERNUMBER`). |
| **Unique Customers** | **92** | Distinct count of B2B corporate customer accounts (`CUSTOMERNAME`). |

*Additional Supporting Metric:*
- **Total Units Sold**: **99,067** physical product units delivered across all purchase orders (supporting volume metric).

---

## 3. Data-Driven Business Insights

### 4.1 Revenue Trends Over Time
- **2003 Revenue**: **$3,516,979.54**
- **2004 Revenue**: **$4,724,162.60**
- **Growth Rate**: Revenue grew by **34.32%** from 2003 to 2004.
- **2005 Observed Revenue**: **$1,791,486.71** (covering transactions from January through May 2005).
- **November Peak Periods**:
  - November 2003 Revenue: **$1,029,837.66**
  - November 2004 Revenue: **$1,089,048.01**
- **Insight**: November recorded the highest monthly revenue in both 2003 and 2004, standing out as the peak revenue period in the dataset.

### 4.2 Product Line Performance
The commercial revenue contribution across product categories follows this hierarchy:
1. **Classic Cars**: **$3,919,615.66** (39.07% share) — *Highest revenue-generating product line*
2. **Vintage Cars**: **$1,903,150.84** (18.97% share)
3. **Motorcycles**: **$1,166,388.34** (11.63% share)
4. **Trucks and Buses**: **$1,127,789.84** (11.24% share)
5. **Planes**: **$975,003.57** (9.72% share)
6. **Ships**: **$714,437.13** (7.12% share)
7. **Trains**: **$226,243.47** (2.26% share)

### 4.3 Regional / Territory Analysis
Commercial revenue breakdown across geographic territories:
- **EMEA** (Europe, Middle East & Africa): **$4,979,272.41** (49.63% share) — *Largest territory*
- **North America (NA)**: **$3,852,061.39** (38.40% share)
- **APAC** (Asia-Pacific): **$746,121.83** (7.44% share)
- **Japan**: **$455,173.22** (4.54% share)

### 4.4 Deal Size Performance
Revenue distribution by transaction deal size tier:
- **Medium Deals**: **$6,087,432.24** (60.68% share) — *Contributes the largest share of revenue*
- **Small Deals**: **$2,643,077.35** (26.34% share)
- **Large Deals**: **$1,302,119.26** (12.98% share)

### 4.5 Top 10 Products by Revenue
The top 10 individual product SKUs by commercial revenue:
1. **S18_3232** — Classic Cars — **$288,245.42** (*Top product SKU*)
2. **S10_1949** — Classic Cars — **$191,073.03**
3. **S10_4698** — Motorcycles — **$170,401.07**
4. **S12_1108** — Classic Cars — **$168,585.32**
5. **S18_2238** — Classic Cars — **$154,623.95**
6. **S12_3891** — Classic Cars — **$145,332.04**
7. **S24_3856** — Classic Cars — **$140,626.90**
8. **S12_2823** — Motorcycles — **$140,006.16**
9. **S18_1662** — Planes — **$139,421.97**
10. **S12_1099** — Classic Cars — **$137,177.01**

### 4.6 Customer Account Performance
Top revenue-contributing B2B customer accounts:
1. **Euro Shopping Channel** — Spain — **$912,294.11** (*Top customer account*)
2. **Mini Gifts Distributors Ltd.** — USA — **$654,858.06**
3. **Australian Collectors, Co.** — Australia — **$200,995.41**
4. **Muscle Machine Inc** — USA — **$197,736.94**
5. **La Rochelle Gifts** — France — **$180,124.90**

### 4.7 Estimated Profitability Performance
- **Total Estimated Profit**: **$4,034,223.65**
- **Estimated Profit Margin**: **40.21%**
- *Note*: These values are estimates based on the 60% MSRP cost assumption (`QUANTITYORDERED × MSRP × 60%`) and do not represent actual accounting profit.

---

## 4. Strategic Business Recommendations

1. **Prioritize Core Product Categories**  
   Focus inventory planning and sales resources on **Classic Cars** ($3.92M) and **Vintage Cars** ($1.90M), which together drive over 58% of total commercial revenue.

2. **Support Primary Regional Markets**  
   Maintain strong sales, marketing, and distribution coverage in **EMEA** ($4.98M) and **North America (NA)** ($3.85M), which account for over 88% of global sales.

3. **Incentivize Medium Deal Transitions**  
   Develop pricing structures, volume discounts, and sales strategies that encourage customer movement from **Small** deal sizes into **Medium** deal tiers ($6.09M revenue share).

4. **Maintain Top Customer Accounts**  
   Focus key account management efforts on major corporate accounts such as **Euro Shopping Channel** ($912.29K) and **Mini Gifts Distributors Ltd.** ($654.86K) to preserve core revenue streams.

5. **Manage Inventory Around High-Revenue Months**  
   Prepare inventory stocking, fulfillment capacity, and operational workflows ahead of peak revenue demand periods, particularly **November**.

---

## 5. Conclusion

The sales analysis demonstrates strong commercial performance with **$10.03M** in total revenue and a **40.21% Estimated Profit Margin** based on the defined cost-estimation methodology.

The key findings highlight:
- Total commercial revenue reached **$10,032,628.85** across 307 orders.
- **Classic Cars** is the leading product line generating **$3.92M** (39.07% share).
- **EMEA** is the top-performing territory contributing **$4.98M** (49.63% share).
- **Medium** deal sizes contribute the largest share of revenue at **$6.09M** (60.68% share).
- **S18_3232** is the top-performing product SKU generating **$288,245.42**.
- **Euro Shopping Channel** is the leading corporate customer account generating **$912,294.11**.

Overall, this project demonstrates how data analysis and Power BI visualization can be used to evaluate sales performance, identify business patterns, and develop data-driven recommendations.

Remember that profitability figures in this analysis represent **Estimated Profit** based on the defined cost assumption and should not be interpreted as actual accounting profit.
