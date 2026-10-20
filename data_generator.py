import random
import json

DEPARTMENTS = ["Marketing", "Sales", "Engineering", "Operations", "Customer Success"]

METRIC_DEFINITIONS = [
    {"dept": "Marketing", "name": "Customer Acquisition Cost (CAC)", "base_val": 420.0, "unit": "$", "financial_link": "Operating Expenses", "impact_weight": -0.85},
    {"dept": "Marketing", "name": "Organic Traffic Share", "base_val": 38.5, "unit": "%", "financial_link": "Net Margin Efficiency", "impact_weight": 0.65},
    {"dept": "Sales", "name": "Average Deal Close Cycle", "base_val": 48.0, "unit": "days", "financial_link": "Cashflow Velocity", "impact_weight": -0.75},
    {"dept": "Sales", "name": "Pipeline Win Rate", "base_val": 26.4, "unit": "%", "financial_link": "Gross Revenue", "impact_weight": 0.92},
    {"dept": "Engineering", "name": "Sprint Velocity Realization", "base_val": 84.0, "unit": "%", "financial_link": "Product R&D ROI", "impact_weight": 0.60},
    {"dept": "Engineering", "name": "Critical Bug Escaped Defects", "base_val": 14.0, "unit": "bugs", "financial_link": "Customer Churn Cost", "impact_weight": -0.80},
    {"dept": "Operations", "name": "Order Fulfillment On-Time Rate", "base_val": 91.2, "unit": "%", "financial_link": "Repeat Revenue", "impact_weight": 0.88},
    {"dept": "Operations", "name": "Warehouse Storage Cost / Unit", "base_val": 4.80, "unit": "$", "financial_link": "COGS", "impact_weight": -0.70},
    {"dept": "Customer Success", "name": "Net Revenue Retention (NRR)", "base_val": 108.5, "unit": "%", "financial_link": "LTV & EBITDA", "impact_weight": 0.95},
    {"dept": "Customer Success", "name": "Support Ticket Resolution SLA", "base_val": 94.0, "unit": "%", "financial_link": "CSAT & Renewal Rate", "impact_weight": 0.72}
]

def generate_kpi_dataset():
    random.seed(42)
    # 12 monthly historical points
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_financials = []
    
    # Financial baseline
    base_rev = 1200000.0
    base_ebitda = 280000.0

    kpi_records = []

    for idx, m in enumerate(months):
        fluctuation = random.uniform(-0.06, 0.08)
        current_rev = round(base_rev * (1.0 + (idx * 0.02) + fluctuation), 2)
        current_ebitda = round(base_ebitda * (1.0 + (idx * 0.015) + (fluctuation * 1.5)), 2)

        monthly_financials.append({
            "month": m,
            "revenue": current_rev,
            "ebitda": current_ebitda,
            "ebitda_margin_pct": round((current_ebitda / current_rev) * 100, 1)
        })

        month_kpi_values = {}
        for metric in METRIC_DEFINITIONS:
            # Add realistic variance
            val_variance = random.uniform(-0.15, 0.15)
            val = round(metric["base_val"] * (1.0 + val_variance), 1)
            month_kpi_values[metric["name"]] = val

        kpi_records.append({
            "month": m,
            "revenue": current_rev,
            "ebitda": current_ebitda,
            "metrics": month_kpi_values
        })

    with open("executive_kpis.json", "w", encoding="utf-8") as f:
        json.dump({"metrics_definition": METRIC_DEFINITIONS, "monthly_data": kpi_records, "financials": monthly_financials}, f, indent=2)

    print("Generated 12-month cross-departmental executive KPI telemetry.")

if __name__ == "__main__":
    generate_kpi_dataset()
