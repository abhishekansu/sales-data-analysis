# 📊 Sales Intelligence Dashboard

An end-to-end **Sales Analytics Dashboard** built with Python, Pandas, Plotly, and Streamlit.  
Demonstrates real-world data wrangling, KPI computation, and interactive business visualisations.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple?logo=plotly)

---

## 🚀 Live Demo

> Run locally in 3 commands — see setup below.

---

## 📌 Features

| Area | What's included |
|------|----------------|
| **KPI Cards** | Total Revenue, Profit, Avg Margin, Orders, AOV |
| **Time Series** | Monthly Revenue vs Profit trend with fill |
| **Category Mix** | Donut chart — revenue share by category |
| **Regional Perf** | Horizontal bar — revenue & profit by region |
| **Channel Analysis** | Bar chart coloured by margin % |
| **Product Matrix** | Scatter — Revenue vs Margin, sized by order volume |
| **Rep Leaderboard** | Horizontal bar, colour-coded by performance tier |
| **Discount Analysis** | Dual-axis: discount volume vs margin degradation |
| **Margin Heatmap** | Category × Region profitability matrix |
| **Smart Insights** | Auto-generated bullet insights from the data |
| **Data Explorer** | Filterable raw data table + CSV download |

---

## 🗂️ Project Structure

```
sales_dashboard/
│
├── app.py               # Main Streamlit dashboard
├── generate_data.py     # Synthetic data generator (2,000 rows)
├── requirements.txt     # Python dependencies
├── data/
│   └── sales_data.csv   # Auto-generated on first run
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/abhishekansu/sales-dashboard.git
cd sales-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate sample data
python generate_data.py

# 4. Launch the dashboard
streamlit run app.py
```

The app opens at **http://localhost:8501** 🎉

---

## 📦 Dataset

Synthetically generated (~2,000 orders) with realistic patterns:

- **Products**: 12 SKUs across Electronics, Accessories, Office furniture  
- **Date range**: Jan 2023 – Dec 2024 (with seasonal trends)  
- **Regions**: North, South, East, West, Central  
- **Channels**: Online, Retail, B2B, Reseller  
- **Sales Reps**: 10 reps with varied performance  
- **Features**: Revenue, Cost, Profit, Discount %, Margin %

---

## 🧠 Key Analytical Skills Demonstrated

- **Data Wrangling** — date parsing, feature engineering, groupby aggregations
- **KPI Design** — defining and computing business metrics from raw transactional data
- **Statistical Thinking** — margin analysis, discount impact, seasonal trends
- **Data Visualisation** — 8+ chart types using Plotly (time series, scatter, heatmap, pie, bar)
- **Dashboard UX** — multi-filter sidebar, responsive layout, insight callouts
- **Python Best Practices** — caching, modular functions, clean code

---

## 📸 Dashboard Sections

1. **Header KPIs** — five summary cards at a glance  
2. **Revenue Trends** — time series + category donut  
3. **Regional & Channel** — where revenue is coming from  
4. **Product & Rep** — what and who is driving growth  
5. **Discount & Margin** — pricing strategy health check  
6. **Insights Panel** — auto-generated business observations  

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `Python 3.9+` | Core language |
| `Pandas` | Data manipulation & aggregation |
| `NumPy` | Numerical operations |
| `Plotly` | Interactive charts |
| `Streamlit` | Web app framework |

---

## 🔭 Future Improvements

- [ ] Connect to a live SQL database (PostgreSQL / SQLite)
- [ ] Add YoY comparison toggle
- [ ] Forecast next-quarter revenue with Prophet
- [ ] Export dashboard as PDF report
- [ ] Deploy to Streamlit Cloud

---

## 👨‍💻 Author

**Abhishek Ansu**  
[GitHub](https://github.com/abhishekansu) · [LinkedIn](https://www.linkedin.com/in/abhishek-ansu-404468190/)

---

*Built as part of a Data Analytics portfolio. Open to feedback and contributions!*
