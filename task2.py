"""
Simple Sales Report Generator
-----------------------------

This script:
1. Reads sales data from a CSV file
2. Calculates some summary statistics
3. Creates simple charts (bar + line)
4. Generates a PDF report with text, tables, and charts

Libraries used: pandas, matplotlib, reportlab
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# STEP 1: Load Data
def load_data(file_path):
    """Reads a CSV file into a pandas DataFrame"""
    df = pd.read_csv(file_path, parse_dates=["date"])
    return df

# STEP 2: Analyze Data
def analyze_data(df):
    """Returns some simple statistics from the sales data"""
    total_revenue = df["revenue"].sum()
    avg_price = df["price"].mean()
    top_product = df.groupby("product")["revenue"].sum().idxmax()

    revenue_by_category = df.groupby("category")["revenue"].sum()
    monthly_revenue = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()

    return {
        "total_revenue": total_revenue,
        "avg_price": avg_price,
        "top_product": top_product,
        "revenue_by_category": revenue_by_category,
        "monthly_revenue": monthly_revenue,
    }

# STEP 3: Make Charts
def make_charts(analysis, out_dir="charts"):
    """Creates and saves bar and line charts"""
    os.makedirs(out_dir, exist_ok=True)
    charts = {}

    # Bar chart: revenue by category
    plt.figure(figsize=(6,4))
    analysis["revenue_by_category"].plot(kind="bar")
    plt.title("Revenue by Category")
    plt.ylabel("Revenue")
    cat_chart = os.path.join(out_dir, "revenue_by_category.png")
    plt.tight_layout()
    plt.savefig(cat_chart)
    plt.close()
    charts["category"] = cat_chart

    # Line chart: monthly revenue
    plt.figure(figsize=(6,4))
    analysis["monthly_revenue"].plot(marker="o")
    plt.title("Monthly Revenue Trend")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    month_chart = os.path.join(out_dir, "monthly_revenue.png")
    plt.tight_layout()
    plt.savefig(month_chart)
    plt.close()
    charts["monthly"] = month_chart

    return charts

# STEP 4: Generate PDF
def create_pdf(analysis, charts, output="sales_report.pdf"):
    """Generates a PDF with text, a table, and charts"""
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("📊 Sales Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary text
    elements.append(Paragraph(f"Total Revenue: {analysis['total_revenue']:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"Average Price: {analysis['avg_price']:.2f}", styles["Normal"]))
    elements.append(Paragraph(f"Top Product: {analysis['top_product']}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table: revenue by category
    table_data = [["Category", "Revenue"]]
    for cat, val in analysis["revenue_by_category"].items():
        table_data.append([cat, f"{val:.2f}"])
    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Insert charts
    elements.append(Paragraph("Charts", styles["Heading2"]))
    for name, path in charts.items():
        elements.append(Paragraph(name.replace("_"," ").title(), styles["Heading3"]))
        elements.append(Image(path, width=400, height=250))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    print(f"Report saved as {output}")

# STEP 5: Run Everything
def main():
    file_path = "sales_data.csv"   # <-- put your CSV here
    df = load_data(file_path)
    analysis = analyze_data(df)
    charts = make_charts(analysis)
    create_pdf(analysis, charts)

if __name__ == "__main__":
    main()

