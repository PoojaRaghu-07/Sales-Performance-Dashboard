import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, 755, "Sales Performance & Business Insights Report")
            self.drawRightString(572, 755, "Author: Pooja R")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(40, 748, 572, 748)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 42, 572, 42)
        
        self.drawString(40, 30, "Student Project Report — Sales Performance Analysis (Data Analysis & Power BI)")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 30, page_text)
        self.restoreState()

img_path = os.path.join("reports", "dashboard.png")
pdf_path = os.path.join("reports", "Business_Insights_Report.pdf")

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=45,
    bottomMargin=52
)

styles = getSampleStyleSheet()

# Custom Styles
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=22,
    leading=26,
    textColor=colors.HexColor('#0F172A'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11.5,
    leading=15,
    textColor=colors.HexColor('#0284C7'),
    spaceAfter=6
)

meta_style = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#334155'),
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13.5,
    leading=17.5,
    textColor=colors.HexColor('#0284C7'),
    spaceBefore=12,
    spaceAfter=5,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=14.5,
    textColor=colors.HexColor('#0369A1'),
    spaceBefore=9,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#1E293B'),
    spaceAfter=5
)

bullet_style = ParagraphStyle(
    'BulletItem',
    parent=body_style,
    leftIndent=15,
    spaceAfter=4
)

callout_style = ParagraphStyle(
    'CalloutText',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8.8,
    leading=12.5,
    textColor=colors.HexColor('#0F172A'),
    backColor=colors.HexColor('#F1F5F9'),
    borderColor=colors.HexColor('#0284C7'),
    borderWidth=1,
    borderPadding=7,
    spaceBefore=5,
    spaceAfter=8
)

caption_style = ParagraphStyle(
    'ImgCaption',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#475569'),
    alignment=1, # Centered
    spaceAfter=8
)

table_header_style = ParagraphStyle(
    'TableHeader',
    fontName='Helvetica-Bold',
    fontSize=9,
    leading=12,
    textColor=colors.white,
    alignment=0
)

table_body_style = ParagraphStyle(
    'TableBody',
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor('#1E293B'),
    alignment=0
)

story = []

# Title Block
story.append(Paragraph("Sales Performance &amp; Business Insights Report", title_style))
story.append(Paragraph("Student Project Report &nbsp;|&nbsp; Focus: Data Analysis &amp; Power BI", subtitle_style))
story.append(Paragraph("<b>Author:</b> Pooja R &nbsp;&nbsp;|&nbsp;&nbsp; <b>Project:</b> Sales Performance Analysis", meta_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284C7'), spaceBefore=2, spaceAfter=8))

# 1. Executive Summary
story.append(Paragraph("1. Executive Summary", h1_style))
exec_text = (
    "This project presents an independent sales performance analysis using the commercial transaction dataset "
    "<code>powerbi/cleaned_sales_data_powerbi.csv</code> spanning historical sales from January 2003 through May 2005.<br/><br/>"
    "The dataset contains:<br/>"
    "• <b>2,823</b> transaction line items<br/>"
    "• <b>307</b> unique purchase orders<br/>"
    "• <b>$10,032,628.85</b> total commercial revenue<br/>"
    "• <b>92</b> unique corporate customer accounts<br/>"
    "• Historical sales from January 2003 through May 2005<br/><br/>"
    "The analysis is fully aligned with the finalized Power BI dashboard <b>“Sales Performance Executive Summary”</b> "
    "(Page: <code>Executive Summary</code>)."
)
story.append(Paragraph(exec_text, body_style))

# Dashboard Image (dashboard.png)
if os.path.exists(img_path):
    img_w = 532
    img_h = 532 * (9.0 / 16.0) # 299.25 pt
    story.append(Spacer(1, 4))
    story.append(Image(img_path, width=img_w, height=img_h))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Figure 1. Sales Performance Executive Summary dashboard.", caption_style))

callout_text = (
    "<b>ℹ️ Profit Estimation Methodology Notice:</b> The source dataset does not contain actual historical accounting "
    "cost or net profit figures. Cost of Goods Sold (COGS) is estimated at <b>60% of MSRP</b> "
    "(<code>QUANTITYORDERED × MSRP × 60%</code>). Therefore, all profitability values must be explicitly called "
    "<b>Estimated Profit</b> and <b>Estimated Profit Margin</b>. They should not be interpreted as actual accounting profit."
)
story.append(Paragraph(callout_text, callout_style))

# 2. Key Performance Indicators
story.append(Paragraph("2. Key Performance Indicators (KPI Summary)", h1_style))

kpi_data = [
    [Paragraph("<b>KPI Metric</b>", table_header_style), Paragraph("<b>Unfiltered Value</b>", table_header_style), Paragraph("<b>Metric Explanation / Scope</b>", table_header_style)],
    [Paragraph("Total Revenue", table_body_style), Paragraph("<b>$10,032,628.85</b>", table_body_style), Paragraph("Cumulative sales revenue generated across all 2,823 transaction records.", table_body_style)],
    [Paragraph("Average Order Value", table_body_style), Paragraph("<b>$32,679.57</b>", table_body_style), Paragraph("Average revenue generated per unique purchase order ($10.03M / 307 orders).", table_body_style)],
    [Paragraph("Total Estimated Profit", table_body_style), Paragraph("<b>$4,034,223.65</b>", table_body_style), Paragraph("Cumulative estimated profit derived from the 60% MSRP cost baseline assumption.", table_body_style)],
    [Paragraph("Estimated Profit Margin", table_body_style), Paragraph("<b>40.21%</b>", table_body_style), Paragraph("Overall estimated commercial profit margin percentage across total revenue.", table_body_style)],
    [Paragraph("Total Orders", table_body_style), Paragraph("<b>307</b>", table_body_style), Paragraph("Distinct count of purchase orders processed (<code>ORDERNUMBER</code>).", table_body_style)],
    [Paragraph("Unique Customers", table_body_style), Paragraph("<b>92</b>", table_body_style), Paragraph("Distinct count of B2B corporate customer accounts (<code>CUSTOMERNAME</code>).", table_body_style)]
]

t_kpi = Table(kpi_data, colWidths=[130, 95, 307])
t_kpi.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284C7')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))

story.append(t_kpi)
story.append(Spacer(1, 4))
story.append(Paragraph("<i>Additional Supporting Metric:</i> <b>Total Units Sold</b>: <b>99,067</b> physical product units delivered across all purchase orders (supporting volume metric).", body_style))

# 3. Data-Driven Business Insights
story.append(Paragraph("3. Data-Driven Business Insights", h1_style))

insights = [
    ("4.1 Revenue Trends Over Time", (
        "• <b>2003 Revenue</b>: $3,516,979.54<br/>"
        "• <b>2004 Revenue</b>: $4,724,162.60<br/>"
        "• <b>Growth Rate</b>: Revenue grew by <b>34.32%</b> from 2003 to 2004.<br/>"
        "• <b>2005 Observed Revenue</b>: $1,791,486.71 (covering transactions from January through May 2005).<br/>"
        "• <b>November Peak Periods</b>: November 2003 revenue reached $1,029,837.66 and November 2004 revenue reached $1,089,048.01.<br/>"
        "• <b>Insight</b>: November recorded the highest monthly revenue in both 2003 and 2004, standing out as the peak revenue period in the dataset."
    )),
    ("4.2 Product Line Performance", (
        "1. <b>Classic Cars</b>: $3,919,615.66 (39.07% share) — <i>Highest revenue-generating product line</i><br/>"
        "2. <b>Vintage Cars</b>: $1,903,150.84 (18.97% share)<br/>"
        "3. <b>Motorcycles</b>: $1,166,388.34 (11.63% share)<br/>"
        "4. <b>Trucks and Buses</b>: $1,127,789.84 (11.24% share)<br/>"
        "5. <b>Planes</b>: $975,003.57 (9.72% share)<br/>"
        "6. <b>Ships</b>: $714,437.13 (7.12% share)<br/>"
        "7. <b>Trains</b>: $226,243.47 (2.26% share)"
    )),
    ("4.3 Regional / Territory Analysis", (
        "• <b>EMEA</b> (Europe, Middle East & Africa): $4,979,272.41 (49.63% share) — <i>Largest territory</i><br/>"
        "• <b>North America (NA)</b>: $3,852,061.39 (38.40% share)<br/>"
        "• <b>APAC</b> (Asia-Pacific): $746,121.83 (7.44% share)<br/>"
        "• <b>Japan</b>: $455,173.22 (4.54% share)"
    )),
    ("4.4 Deal Size Performance", (
        "• <b>Medium Deals</b>: $6,087,432.24 (60.68% share) — <i>Contributes the largest share of revenue</i><br/>"
        "• <b>Small Deals</b>: $2,643,077.35 (26.34% share)<br/>"
        "• <b>Large Deals</b>: $1,302,119.26 (12.98% share)"
    )),
    ("4.5 Top 10 Products by Revenue", (
        "1. <b>S18_3232</b> — Classic Cars — $288,245.42 (<i>Top product SKU</i>)<br/>"
        "2. <b>S10_1949</b> — Classic Cars — $191,073.03<br/>"
        "3. <b>S10_4698</b> — Motorcycles — $170,401.07<br/>"
        "4. <b>S12_1108</b> — Classic Cars — $168,585.32<br/>"
        "5. <b>S18_2238</b> — Classic Cars — $154,623.95<br/>"
        "6. <b>S12_3891</b> — Classic Cars — $145,332.04<br/>"
        "7. <b>S24_3856</b> — Classic Cars — $140,626.90<br/>"
        "8. <b>S12_2823</b> — Motorcycles — $140,006.16<br/>"
        "9. <b>S18_1662</b> — Planes — $139,421.97<br/>"
        "10. <b>S12_1099</b> — Classic Cars — $137,177.01"
    )),
    ("4.6 Customer Account Performance", (
        "1. <b>Euro Shopping Channel</b> — Spain — $912,294.11 (<i>Top customer account</i>)<br/>"
        "2. <b>Mini Gifts Distributors Ltd.</b> — USA — $654,858.06<br/>"
        "3. <b>Australian Collectors, Co.</b> — Australia — $200,995.41<br/>"
        "4. <b>Muscle Machine Inc</b> — USA — $197,736.94<br/>"
        "5. <b>La Rochelle Gifts</b> — France — $180,124.90"
    )),
    ("4.7 Estimated Profitability Performance", (
        "• <b>Total Estimated Profit</b>: $4,034,223.65<br/>"
        "• <b>Estimated Profit Margin</b>: 40.21%<br/>"
        "• <i>Note</i>: These values are estimates based on the 60% MSRP cost assumption (<code>QUANTITYORDERED × MSRP × 60%</code>) "
        "and do not represent actual accounting profit."
    ))
]

for sub_title, text in insights:
    story.append(Paragraph(sub_title, h2_style))
    story.append(Paragraph(text, body_style))

# 4. Strategic Business Recommendations
story.append(Paragraph("4. Strategic Business Recommendations", h1_style))

recs = [
    "<b>Prioritize Core Product Categories:</b> Focus inventory planning and sales resources on <b>Classic Cars</b> ($3.92M) and <b>Vintage Cars</b> ($1.90M), which together drive over 58% of total commercial revenue.",
    "<b>Support Primary Regional Markets:</b> Maintain strong sales, marketing, and distribution coverage in <b>EMEA</b> ($4.98M) and <b>North America (NA)</b> ($3.85M), which account for over 88% of global sales.",
    "<b>Incentivize Medium Deal Transitions:</b> Develop pricing structures, volume discounts, and sales strategies that encourage customer movement from <b>Small</b> deal sizes into <b>Medium</b> deal tiers ($6.09M revenue share).",
    "<b>Maintain Top Customer Accounts:</b> Focus key account management efforts on major corporate accounts such as <b>Euro Shopping Channel</b> ($912.29K) and <b>Mini Gifts Distributors Ltd.</b> ($654.86K) to preserve core revenue streams.",
    "<b>Manage Inventory Around High-Revenue Months:</b> Prepare inventory stocking, fulfillment capacity, and operational workflows ahead of peak revenue demand periods, particularly <b>November</b>."
]

for idx, rec in enumerate(recs, 1):
    story.append(Paragraph(f"{idx}. {rec}", bullet_style))

# 5. Conclusion
story.append(Paragraph("5. Conclusion", h1_style))
conclusion_p1 = (
    "The sales analysis demonstrates strong commercial performance with <b>$10.03M</b> in total revenue and a "
    "<b>40.21% Estimated Profit Margin</b> based on the defined cost-estimation methodology.<br/><br/>"
    "The key findings highlight:<br/>"
    "• Total commercial revenue reached <b>$10,032,628.85</b> across 307 orders.<br/>"
    "• <b>Classic Cars</b> is the leading product line generating <b>$3.92M</b> (39.07% share).<br/>"
    "• <b>EMEA</b> is the top-performing territory contributing <b>$4.98M</b> (49.63% share).<br/>"
    "• <b>Medium</b> deal sizes contribute the largest share of revenue at <b>$6.09M</b> (60.68% share).<br/>"
    "• <b>S18_3232</b> is the top-performing product SKU generating <b>$288,245.42</b>.<br/>"
    "• <b>Euro Shopping Channel</b> is the leading corporate customer account generating <b>$912,294.11</b>.<br/><br/>"
    "Overall, this project demonstrates how data analysis and Power BI visualization can be used to evaluate sales "
    "performance, identify business patterns, and develop data-driven recommendations.<br/><br/>"
    "Remember that profitability figures in this analysis represent <b>Estimated Profit</b> based on the defined cost "
    "assumption and should not be interpreted as actual accounting profit."
)
story.append(Paragraph(conclusion_p1, body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Professional PDF Report generated successfully at: {pdf_path}")
