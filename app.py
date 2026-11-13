"""CloudCost - Streamlit front end. Run with: streamlit run app.py"""
import pandas as pd
import streamlit as st

import calculator as calc

st.set_page_config(page_title="CloudCost", page_icon="☁️", layout="centered")
st.title("☁️ CloudCost")
st.caption("Compare cloud storage costs across AWS, Google Cloud and Microsoft Azure.")

col1, col2 = st.columns([2, 1])
amount = col1.number_input("Storage required", min_value=0.01, value=500.0, step=10.0)
unit = col2.radio("Unit", ["GB", "TB"], horizontal=True)

try:
    storage_gb = calc.to_gb(amount, unit)
    results = calc.compare(storage_gb)
    best = calc.cheapest(results)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.success(f"🏆 Cheapest: **{best.provider}** at **${best.monthly_cost:,.2f}/month**")

df = pd.DataFrame(
    {
        "Provider": [r.provider for r in results],
        "Price / GB": [f"${r.price_per_gb:.3f}" for r in results],
        "Monthly Cost": [f"${r.monthly_cost:,.2f}" for r in results],
        "Yearly Cost": [f"${r.yearly_cost:,.2f}" for r in results],
    }
)
st.dataframe(df, hide_index=True, width="stretch")
st.bar_chart(pd.DataFrame({"Monthly cost (USD)": [r.monthly_cost for r in results]},
                          index=[r.provider for r in results]))

report = calc.generate_report(storage_gb, results)
with st.expander("View report"):
    st.code(report)

d1, d2 = st.columns(2)
d1.download_button("⬇️ Report (.txt)", report, "cloudcost_report.txt", "text/plain")
d2.download_button("⬇️ Data (.csv)", calc.results_to_csv(results),
                   "cloudcost_report.csv", "text/csv")

st.caption("Illustrative prices only, not live provider quotes.")
