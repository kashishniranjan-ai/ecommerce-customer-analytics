# E-Commerce Customer & Revenue Analytics

An end-to-end analytics project on e-commerce transaction data: revenue trends, RFM customer segmentation, cohort retention, and channel/category performance — packaged as a reproducible pipeline plus an interactive dashboard.

> **Note:** The data in `data/` is synthetically generated (2,500 customers, ~7,700 orders, Feb 2023–Dec 2025) for demonstration purposes. Swap in your own `customers.csv` / `orders.csv` / `order_items.csv` (matching the schema below) to run this on real data.

## Project structure

```
ecommerce-customer-analytics/
│
├── data/                     # Raw input data
│   ├── customers.csv
│   ├── orders.csv
│   └── order_items.csv
│
├── src/
│   └── analysis_pipeline.py  # Reproducible analysis: revenue, RFM, cohorts
│
├── output/
│   ├── rfm_segments.csv      # Per-customer RFM scores & segment labels
│   └── dashboard_data.json   # Aggregated metrics consumed by the dashboard
│
├── dashboard/
│   └── ecommerce_dashboard.html   # Self-contained interactive dashboard
│
├── README.md
└── requirements.txt
```

## Quickstart

```bash
pip install -r requirements.txt
cd src
python analysis_pipeline.py
```

This reads the CSVs in `data/`, and writes `output/rfm_segments.csv` and `output/dashboard_data.json`.

Then open `dashboard/ecommerce_dashboard.html` in a browser to view the results (it loads its data at build time, so re-run the steps in [Updating the dashboard](#updating-the-dashboard-with-new-data) if you regenerate the metrics).

## What the pipeline computes

- **Revenue trend** — monthly net revenue, order count, and average order value
- **Category / channel / region breakdown** — revenue and units by product category, marketing channel, and region
- **RFM segmentation** — each customer scored on Recency, Frequency, and Monetary value (1–5 each), then grouped into: Champions, Loyal Customers, Potential Loyalists, At Risk, Hibernating
- **Cohort retention** — % of each signup-month cohort placing an order in each of the following 12 months
- **Top customers** — ranked by lifetime net revenue

## Data schema

**`data/customers.csv`**
| column | description |
|---|---|
| customer_id | unique customer identifier |
| customer_name, email | contact info |
| signup_date | date customer registered |
| region | North / South / East / West / Central |
| acquisition_channel | how the customer was acquired |

**`data/orders.csv`**
| column | description |
|---|---|
| order_id, customer_id | identifiers |
| order_date | date of order |
| channel, region | order-level channel & region |
| subtotal, discount_amount, shipping_fee | order economics |
| net_revenue | revenue after discount + shipping (0 if returned) |
| gross_revenue | revenue before returns are zeroed out |
| status | Completed / Returned |

**`data/order_items.csv`**
| column | description |
|---|---|
| item_id, order_id | identifiers |
| category | product category |
| unit_price, quantity, line_total | line-item economics |

## Updating the dashboard with new data

1. Replace the files in `data/` with your own (same schema).
2. Run `python src/analysis_pipeline.py` to regenerate `output/dashboard_data.json`.
3. Open `dashboard/ecommerce_dashboard.html` in a text editor, find the `<script id="dashboard-data" type="application/json">` block, and replace its contents with the new `output/dashboard_data.json`.

## Requirements

See `requirements.txt` — pandas and numpy. The dashboard itself is a static HTML file (Chart.js loaded via CDN) and needs no build step or server.
