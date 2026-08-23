"""
E-Commerce Customer & Revenue Analytics — Analysis Pipeline
=============================================================
Reads raw transaction data from ../data/ and produces:
  - ../output/rfm_segments.csv     (per-customer RFM scores & segments)
  - ../output/dashboard_data.json  (aggregated metrics for the dashboard)

Run from the src/ directory:
    cd src
    python analysis_pipeline.py
"""

import pandas as pd
import numpy as np
import json

customers = pd.read_csv("../data/customers.csv", parse_dates=["signup_date"])
orders = pd.read_csv("../data/orders.csv", parse_dates=["order_date"])
items = pd.read_csv("../data/order_items.csv")

completed = orders[orders.status == "Completed"].copy()
completed["order_month"] = completed.order_date.values.astype("datetime64[M]")

# ---------- 1. Monthly revenue trend ----------
monthly = completed.groupby("order_month").agg(
    revenue=("net_revenue", "sum"),
    orders=("order_id", "count"),
    aov=("net_revenue", "mean"),
).reset_index()
monthly["order_month"] = monthly["order_month"].dt.strftime("%Y-%m")

# ---------- 2. Revenue by category ----------
items_full = items.merge(orders[["order_id", "status", "order_date"]], on="order_id")
items_full = items_full[items_full.status == "Completed"]
by_category = items_full.groupby("category").agg(
    revenue=("line_total", "sum"),
    units=("quantity", "sum"),
    orders=("order_id", "nunique"),
).reset_index().sort_values("revenue", ascending=False)

# ---------- 3. Revenue by channel & region ----------
by_channel = completed.groupby("channel").agg(revenue=("net_revenue", "sum"), orders=("order_id", "count")).reset_index().sort_values("revenue", ascending=False)
by_region = completed.groupby("region").agg(revenue=("net_revenue", "sum"), orders=("order_id", "count")).reset_index().sort_values("revenue", ascending=False)

# ---------- 4. RFM segmentation ----------
snapshot_date = orders.order_date.max() + pd.Timedelta(days=1)
rfm = completed.groupby("customer_id").agg(
    last_order=("order_date", "max"),
    frequency=("order_id", "count"),
    monetary=("net_revenue", "sum"),
).reset_index()
rfm["recency"] = (snapshot_date - rfm["last_order"]).dt.days

r_labels = [5, 4, 3, 2, 1]
f_labels = [1, 2, 3, 4, 5]
m_labels = [1, 2, 3, 4, 5]
rfm["R"] = pd.qcut(rfm["recency"], 5, labels=r_labels, duplicates="drop").astype(int)
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=f_labels, duplicates="drop").astype(int)
rfm["M"] = pd.qcut(rfm["monetary"], 5, labels=m_labels, duplicates="drop").astype(int)
rfm["rfm_score"] = rfm["R"] + rfm["F"] + rfm["M"]

def segment(row):
    if row.rfm_score >= 13:
        return "Champions"
    elif row.rfm_score >= 10:
        return "Loyal Customers"
    elif row.rfm_score >= 8:
        return "Potential Loyalists"
    elif row.rfm_score >= 6:
        return "At Risk"
    else:
        return "Hibernating"

rfm["segment"] = rfm.apply(segment, axis=1)
segment_summary = rfm.groupby("segment").agg(
    customers=("customer_id", "count"),
    total_revenue=("monetary", "sum"),
    avg_frequency=("frequency", "mean"),
    avg_recency=("recency", "mean"),
).reset_index().sort_values("total_revenue", ascending=False)
segment_summary["pct_customers"] = (segment_summary.customers / segment_summary.customers.sum() * 100).round(1)
segment_summary["pct_revenue"] = (segment_summary.total_revenue / segment_summary.total_revenue.sum() * 100).round(1)

# ---------- 5. Cohort retention (by signup month) ----------
customers["cohort_month"] = customers.signup_date.values.astype("datetime64[M]")
co = completed.merge(customers[["customer_id", "cohort_month"]], on="customer_id")
co["order_month"] = co.order_date.values.astype("datetime64[M]")
co["cohort_index"] = (
    (co.order_month.dt.year - co.cohort_month.dt.year) * 12 +
    (co.order_month.dt.month - co.cohort_month.dt.month)
)
cohort_data = co.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
cohort_sizes = customers.groupby("cohort_month")["customer_id"].nunique()
retention = cohort_pivot.divide(cohort_sizes, axis=0).round(4)
retention = retention.iloc[:, :12]  # first 12 months
retention.index = retention.index.strftime("%Y-%m")

# ---------- 6. Top customers ----------
top_customers = rfm.merge(customers[["customer_id", "customer_name", "region", "acquisition_channel"]], on="customer_id")
top_customers = top_customers.sort_values("monetary", ascending=False).head(15)[
    ["customer_id", "customer_name", "region", "acquisition_channel", "frequency", "monetary", "segment"]
]

# ---------- 7. Key KPIs ----------
total_revenue = completed.net_revenue.sum()
total_orders = len(completed)
total_customers = customers.customer_id.nunique()
active_customers = rfm.customer_id.nunique()
avg_order_value = completed.net_revenue.mean()
return_rate = (orders.status == "Returned").mean()
repeat_rate = (rfm.frequency > 1).mean()

# customer lifetime value estimate (avg monetary per customer over observed window)
clv_estimate = rfm.monetary.mean()

kpis = {
    "total_revenue": round(float(total_revenue), 2),
    "total_orders": int(total_orders),
    "total_customers": int(total_customers),
    "active_purchasing_customers": int(active_customers),
    "avg_order_value": round(float(avg_order_value), 2),
    "return_rate_pct": round(float(return_rate) * 100, 2),
    "repeat_purchase_rate_pct": round(float(repeat_rate) * 100, 2),
    "avg_customer_ltv": round(float(clv_estimate), 2),
}

output = {
    "kpis": kpis,
    "monthly": monthly.to_dict(orient="records"),
    "by_category": by_category.to_dict(orient="records"),
    "by_channel": by_channel.to_dict(orient="records"),
    "by_region": by_region.to_dict(orient="records"),
    "segment_summary": segment_summary.to_dict(orient="records"),
    "top_customers": top_customers.to_dict(orient="records"),
    "retention": {
        "months": [str(c) for c in retention.columns.tolist()],
        "cohorts": [
            {"cohort": idx, "values": [None if pd.isna(v) else round(v * 100, 1) for v in row]}
            for idx, row in zip(retention.index, retention.values)
        ],
    },
}

with open("../output/dashboard_data.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

rfm.to_csv("../output/rfm_segments.csv", index=False)

print(json.dumps(kpis, indent=2))
print("\nSegments:\n", segment_summary)
