# 📊 E-Commerce Customer & Revenue Analytics

An end-to-end data analytics project that transforms e-commerce transaction data into actionable business insights using **Python, RFM customer segmentation, cohort analysis, and an interactive dashboard**.

🔗 **Live Dashboard:**  
https://kashishniranjan-ai.github.io/ecommerce-customer-analytics/

---

## 🚀 Project Overview

This project analyzes e-commerce customer and transaction data to understand:

- Revenue and order trends
- Customer purchasing behaviour
- Customer segmentation
- Repeat purchase patterns
- Customer lifetime value
- Customer retention and cohort behaviour
- Product/category performance
- Return behaviour

The project follows an end-to-end analytics workflow, from raw data processing to business insights and interactive visualization.

---

## 🎯 Business Problem

E-commerce businesses generate large amounts of customer and transaction data, but raw data alone does not provide meaningful business insights.

This project aims to answer questions such as:

- How is revenue changing over time?
- Who are the most valuable customers?
- Which customers are likely to make repeat purchases?
- Which customer segments generate the most revenue?
- How well are customers being retained?
- Which products or categories perform best?
- What is the average customer lifetime value?
- What percentage of orders are returned?

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| 🐍 Python | Data processing and analysis |
| 🐼 Pandas | Data manipulation |
| 🔢 NumPy | Numerical computation |
| 📊 Data Visualization | Charts and business insights |
| 🧠 RFM Analysis | Customer segmentation |
| 📅 Cohort Analysis | Customer retention analysis |
| 🌐 HTML/CSS/JavaScript | Interactive dashboard |
| 📦 CSV/JSON | Data storage and dashboard data |

---

## 📂 Project Structure

```text
ecommerce-customer-analytics/
│
├── dashboard/
│   └── ecommerce_dashboard.html
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   └── order_items.csv
│
├── output/
│   ├── dashboard_data.json
│   └── rfm_segments.csv
│
├── src/
│   └── analysis scripts
│
├── index.html
├── requirements.txt
└── README.md
🔄 Analytics Workflow
Raw E-Commerce Data
        ↓
Data Cleaning & Preparation
        ↓
Exploratory Data Analysis
        ↓
Revenue & Order Analysis
        ↓
RFM Customer Segmentation
        ↓
Cohort & Retention Analysis
        ↓
Business Metrics
        ↓
Interactive Dashboard
        ↓
Business Insights
📈 Key Metrics

The dashboard provides important business KPIs including:

Total Revenue
Average Order Value (AOV)
Active Customers
Repeat Purchase Rate
Average Customer Lifetime Value (LTV)
Return Rate
Total Orders
Revenue Trends
👥 RFM Customer Segmentation

RFM analysis is used to understand customer behaviour based on three dimensions:

Recency

How recently a customer made a purchase.

Frequency

How frequently a customer purchases.

Monetary

How much revenue a customer generates.

Customers are then grouped into meaningful segments that can help businesses develop targeted marketing strategies.

📅 Cohort Analysis

Cohort analysis tracks customers based on when they first made a purchase.

It helps analyze:

Customer retention
Repeat purchasing behaviour
Retention trends over time
Customer lifecycle patterns
📊 Dashboard

The interactive dashboard provides a centralized view of the project's major business metrics.

Dashboard Highlights
Revenue trend analysis
Customer segmentation
RFM analysis
Customer retention
Cohort analysis
Order behaviour
Business KPI tracking
🌐 Live Demo

👉 Open the Interactive Dashboard

💡 Business Insights

The analysis helps businesses identify:

High-value customer segments
Customers with strong repeat-purchase behaviour
Revenue growth patterns
Customer retention trends
Potential opportunities for targeted marketing
Categories and channels contributing to business performance
Areas where customer returns may require attention
⚙️ How to Run the Project
1. Clone the repository
git clone https://github.com/kashishniranjan-ai/ecommerce-customer-analytics.git
2. Navigate to the project
cd ecommerce-customer-analytics
3. Install dependencies
pip install -r requirements.txt
4. Run the analysis

Run the Python scripts inside the src/ directory.

5. Open the dashboard

Open:

dashboard/ecommerce_dashboard.html

in a web browser.

📊 Dataset

The project uses e-commerce customer, order, and order-item data.

The included dataset is synthetically generated for demonstration purposes and follows a realistic e-commerce transaction structure.

This makes the project reproducible while avoiding exposure of real customer information.

🔮 Future Improvements

Possible future improvements include:

Add predictive customer churn analysis
Build a customer lifetime value prediction model
Add sales forecasting
Add product recommendation functionality
Connect the dashboard to a live database
Add automated data pipelines
Deploy the analytics pipeline using cloud services
Add role-based dashboard views for business teams
👩‍💻 Author

Kashish Niranjan

B.Tech Computer Science Engineering | Data Analytics & Python

Connect With Me
💼 LinkedIn: https://www.linkedin.com/in/kashishniranjan/
🐙 GitHub: https://github.com/kashishniranjan-ai
