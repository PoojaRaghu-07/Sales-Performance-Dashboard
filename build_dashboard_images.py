import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import os

# Load dataset
df = pd.read_csv("powerbi/cleaned_sales_data_powerbi.csv", keep_default_na=False)
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
df['Region'] = df['Region'].replace('', 'NA')

# Setup figure canvas (16:9 ratio, 1920x1080 high-res render)
fig = plt.figure(figsize=(16, 9), facecolor='#0F172A', dpi=250)

# Colors
BG_DARK = '#0F172A'
CARD_BG = '#1E293B'
BORDER_COLOR = '#334155'
ACCENT_CYAN = '#38BDF8'
TEXT_WHITE = '#F8FAFC'
TEXT_MUTED = '#94A3B8'

fig.patch.set_facecolor(BG_DARK)

# 1. Header Banner
ax_header = fig.add_axes([0.02, 0.90, 0.96, 0.08], facecolor=CARD_BG)
ax_header.add_patch(patches.FancyBboxPatch((0, 0), 1, 1, facecolor=CARD_BG, edgecolor=BORDER_COLOR, linewidth=1.5, transform=ax_header.transAxes, boxstyle="round,pad=0,rounding_size=0.02"))
ax_header.text(0.02, 0.60, "Sales Performance Executive Summary", color=ACCENT_CYAN, fontsize=18, fontweight='bold', va='center')
ax_header.text(0.02, 0.25, "Interactive Sales Analytics & Executive Commercial Insights", color=TEXT_MUTED, fontsize=10, va='center')
ax_header.axis('off')

# 2. KPI Cards Row (Row 1)
kpis = [
    ("TOTAL REVENUE", "$10.03M", "$10,032,628.85"),
    ("AVG ORDER VALUE", "$32.68K", "$32,679.57"),
    ("ESTIMATED PROFIT", "$4.03M", "$4,034,223.65"),
    ("EST. PROFIT MARGIN", "40.21%", "40.21% Margin"),
    ("TOTAL ORDERS", "307", "307 Orders"),
    ("UNIQUE CUSTOMERS", "92", "92 Accounts")
]

card_w = 0.151
for i, (title, val, sub) in enumerate(kpis):
    left = 0.02 + i * (card_w + 0.01)
    ax_kpi = fig.add_axes([left, 0.79, card_w, 0.09], facecolor=CARD_BG)
    ax_kpi.add_patch(patches.FancyBboxPatch((0, 0), 1, 1, facecolor=CARD_BG, edgecolor=ACCENT_CYAN if "PROFIT" in title or "REVENUE" in title else BORDER_COLOR, linewidth=1.2, transform=ax_kpi.transAxes, boxstyle="round,pad=0,rounding_size=0.05"))
    ax_kpi.text(0.5, 0.75, title, color=TEXT_MUTED, fontsize=8, fontweight='bold', ha='center', va='center')
    ax_kpi.text(0.5, 0.42, val, color=TEXT_WHITE, fontsize=14, fontweight='bold', ha='center', va='center')
    ax_kpi.text(0.5, 0.18, sub, color=ACCENT_CYAN, fontsize=7, ha='center', va='center')
    ax_kpi.axis('off')

# 3. Middle Row Visuals (Row 2)
# Visual 1: Monthly Revenue Trend (Line Chart)
ax_v1 = fig.add_axes([0.02, 0.42, 0.38, 0.33], facecolor=CARD_BG)
yr_rev = df.groupby('YEAR_ID')['Revenue'].sum() / 1e6
ax_v1.plot(yr_rev.index.astype(str), yr_rev.values, marker='o', color=ACCENT_CYAN, linewidth=2.5, markersize=8)
for x, y in zip(yr_rev.index.astype(str), yr_rev.values):
    ax_v1.annotate(f"${y:.2f}M", (x, y), textcoords="offset points", xytext=(0, 10), ha='center', color=TEXT_WHITE, fontweight='bold', fontsize=9)
ax_v1.set_title("Monthly Revenue Trend", color=ACCENT_CYAN, fontsize=11, fontweight='bold', pad=12, loc='left')
ax_v1.set_facecolor(CARD_BG)
ax_v1.tick_params(colors=TEXT_MUTED, labelsize=9)
ax_v1.spines['top'].set_visible(False)
ax_v1.spines['right'].set_visible(False)
ax_v1.spines['bottom'].set_color(BORDER_COLOR)
ax_v1.spines['left'].set_color(BORDER_COLOR)
ax_v1.set_ylim(0, 6)
ax_v1.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.5, alpha=0.5)

# Visual 2: Revenue by Region / Territory (Horizontal Bar Chart)
ax_v2 = fig.add_axes([0.42, 0.42, 0.27, 0.33], facecolor=CARD_BG)
reg_rev = df.groupby('Region')['Revenue'].sum() / 1e6
reg_rev = reg_rev.sort_values(ascending=True)
bars = ax_v2.barh(reg_rev.index, reg_rev.values, color='#38BDF8', height=0.55)
for bar in bars:
    w = bar.get_width()
    ax_v2.text(w + 0.1, bar.get_y() + bar.get_height()/2, f"${w:.2f}M", va='center', color=TEXT_WHITE, fontweight='bold', fontsize=9)
ax_v2.set_title("Revenue by Region / Territory", color=ACCENT_CYAN, fontsize=11, fontweight='bold', pad=12, loc='left')
ax_v2.set_facecolor(CARD_BG)
ax_v2.tick_params(colors=TEXT_MUTED, labelsize=9)
ax_v2.spines['top'].set_visible(False)
ax_v2.spines['right'].set_visible(False)
ax_v2.spines['bottom'].set_color(BORDER_COLOR)
ax_v2.spines['left'].set_color(BORDER_COLOR)
ax_v2.set_xlim(0, 6)
ax_v2.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.5, alpha=0.5)

# Visual 3: Revenue by Deal Size (Column Chart)
ax_v3 = fig.add_axes([0.71, 0.42, 0.27, 0.33], facecolor=CARD_BG)
deal_order = ['Medium', 'Small', 'Large']
deal_rev = df.groupby('DEALSIZE')['Revenue'].sum() / 1e6
deal_vals = [deal_rev.get(d, 0) for d in deal_order]
bars3 = ax_v3.bar(deal_order, deal_vals, color=['#38BDF8', '#10B981', '#F59E0B'], width=0.5)
for bar in bars3:
    h = bar.get_height()
    ax_v3.text(bar.get_x() + bar.get_width()/2, h + 0.15, f"${h:.2f}M", ha='center', color=TEXT_WHITE, fontweight='bold', fontsize=9)
ax_v3.set_title("Revenue by Deal Size", color=ACCENT_CYAN, fontsize=11, fontweight='bold', pad=12, loc='left')
ax_v3.set_facecolor(CARD_BG)
ax_v3.tick_params(colors=TEXT_MUTED, labelsize=9)
ax_v3.spines['top'].set_visible(False)
ax_v3.spines['right'].set_visible(False)
ax_v3.spines['bottom'].set_color(BORDER_COLOR)
ax_v3.spines['left'].set_color(BORDER_COLOR)
ax_v3.set_ylim(0, 7.5)
ax_v3.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.5, alpha=0.5)

# 4. Bottom Row Visuals (Row 3)
# Visual 4: Revenue by Product Line (Donut Chart)
ax_v4 = fig.add_axes([0.02, 0.04, 0.45, 0.34], facecolor=CARD_BG)
pl_rev = df.groupby('PRODUCTLINE')['Revenue'].sum().sort_values(ascending=False)
colors_list = ['#38BDF8', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#6366F1', '#14B8A6']
wedges, texts, autotexts = ax_v4.pie(pl_rev.values, labels=pl_rev.index, autopct='%1.1f%%', startangle=140, colors=colors_list, wedgeprops=dict(width=0.4, edgecolor=BORDER_COLOR))
for t in texts:
    t.set_color(TEXT_MUTED)
    t.set_fontsize(8)
for at in autotexts:
    at.set_color(TEXT_WHITE)
    at.set_fontsize(8)
    at.set_weight('bold')
ax_v4.set_title("Revenue by Product Line", color=ACCENT_CYAN, fontsize=11, fontweight='bold', pad=12, loc='left')

# Visual 5: Top 10 Products by Revenue (Horizontal Bar Chart)
ax_v5 = fig.add_axes([0.50, 0.04, 0.48, 0.34], facecolor=CARD_BG)
top10_prod = df.groupby('PRODUCTCODE')['Revenue'].sum().sort_values(ascending=False).head(10).sort_values(ascending=True)
bars5 = ax_v5.barh(top10_prod.index, top10_prod.values / 1e3, color='#38BDF8', height=0.6)
for bar in bars5:
    w = bar.get_width()
    ax_v5.text(w + 3, bar.get_y() + bar.get_height()/2, f"${w:.1f}K", va='center', color=TEXT_WHITE, fontweight='bold', fontsize=8)
ax_v5.set_title("Top 10 Products by Revenue (Top N = 10)", color=ACCENT_CYAN, fontsize=11, fontweight='bold', pad=12, loc='left')
ax_v5.set_facecolor(CARD_BG)
ax_v5.tick_params(colors=TEXT_MUTED, labelsize=8)
ax_v5.spines['top'].set_visible(False)
ax_v5.spines['right'].set_visible(False)
ax_v5.spines['bottom'].set_color(BORDER_COLOR)
ax_v5.spines['left'].set_color(BORDER_COLOR)
ax_v5.set_xlim(0, 320)
ax_v5.grid(color=BORDER_COLOR, linestyle='--', linewidth=0.5, alpha=0.5)

os.makedirs("reports", exist_ok=True)

# Save images
img_path1 = os.path.join("reports", "dashboard.png")
img_path2 = os.path.join("reports", "powerbi_dashboard.png")
plt.savefig(img_path1, dpi=250, bbox_inches='tight', facecolor=BG_DARK)
plt.savefig(img_path2, dpi=250, bbox_inches='tight', facecolor=BG_DARK)
plt.close()

print(f"High-res dashboard image saved at: {img_path1} and {img_path2}")
