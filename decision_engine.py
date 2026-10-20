import json
import math

class DecisionIntelligenceEngine:
    def __init__(self, data_path="executive_kpis.json"):
        with open(data_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)
        self.definitions = self.dataset["metrics_definition"]
        self.months = self.dataset["monthly_data"]
        self.financials = self.dataset["financials"]

    def analyze(self):
        latest_month = self.months[-1]
        prev_month = self.months[-2]

        # Calculate correlation of each KPI against EBITDA to find true drivers
        ebitda_series = [m["ebitda"] for m in self.months]
        mean_ebitda = sum(ebitda_series) / len(ebitda_series)

        driver_rankings = []
        for d in self.definitions:
            m_name = d["name"]
            kpi_series = [m["metrics"][m_name] for m in self.months]
            mean_kpi = sum(kpi_series) / len(kpi_series)

            # Pearson Correlation
            numerator = sum((kpi_series[i] - mean_kpi) * (ebitda_series[i] - mean_ebitda) for i in range(len(self.months)))
            denom_kpi = math.sqrt(sum((x - mean_kpi) ** 2 for x in kpi_series))
            denom_ebitda = math.sqrt(sum((y - mean_ebitda) ** 2 for y in ebitda_series))
            
            corr = (numerator / (denom_kpi * denom_ebitda)) if (denom_kpi * denom_ebitda) != 0 else 0.0

            curr_val = latest_month["metrics"][m_name]
            prev_val = prev_month["metrics"][m_name]
            mom_change = round(((curr_val - prev_val) / (prev_val or 1)) * 100, 1)

            # Classify strategic importance
            abs_corr = abs(corr)
            impact_tier = "PRIMARY BOTTOM-LINE DRIVER" if abs_corr > 0.65 else "SECONDARY CONTRIBUTOR" if abs_corr > 0.4 else "OPERATIONAL NOISE / WEAK COUPLING"

            driver_rankings.append({
                "metric": m_name,
                "department": d["dept"],
                "unit": d["unit"],
                "latest_value": curr_val,
                "mom_change_pct": mom_change,
                "financial_link": d["financial_link"],
                "correlation_with_ebitda": round(corr, 2),
                "impact_tier": impact_tier
            })

        driver_rankings.sort(key=lambda x: abs(x["correlation_with_ebitda"]), reverse=True)

        # Executive Strategic Briefing
        top_driver = driver_rankings[0]
        executive_takeaway = (
            f"The primary driver governing quarterly EBITDA variance is {top_driver['metric']} ({top_driver['department']}), "
            f"exhibiting an empirical correlation of {top_driver['correlation_with_ebitda']}. "
            f"Senior leadership should deprioritize vanity operational indicators and tie departmental reviews directly to {top_driver['financial_link']}."
        )

        return {
            "financial_summary": {
                "latest_month_revenue": f"${latest_month['revenue']:,.0f}",
                "latest_month_ebitda": f"${latest_month['ebitda']:,.0f}",
                "ebitda_margin": f"{round((latest_month['ebitda'] / latest_month['revenue']) * 100, 1)}%",
                "monitored_kpis_count": len(self.definitions)
            },
            "executive_briefing": executive_takeaway,
            "drivers": driver_rankings,
            "financial_trend": self.financials
        }

if __name__ == "__main__":
    eng = DecisionIntelligenceEngine()
    print(eng.analyze()["financial_summary"])
