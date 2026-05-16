import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR.parent / "output"

@st.cache_data
def load_data():
    product_stats = pd.read_csv(OUTPUT_DIR / "task1_product_stats.csv")
    product_forecast = pd.read_csv(OUTPUT_DIR / "task2_product_forecast.csv")
    top_10 = pd.read_csv(OUTPUT_DIR / "task2_top_10_products.csv")
    worst_10 = pd.read_csv(OUTPUT_DIR / "task2_worst_10_products.csv")
    revenue_inventory = pd.read_csv(OUTPUT_DIR / "task3_revenue_inventory.csv")
    daily_revenue = pd.read_csv(OUTPUT_DIR / "task3_daily_revenue.csv")
    revenue_forecast = pd.read_csv(OUTPUT_DIR / "task3_daily_revenue_forecast.csv")

    daily_revenue["order_date"] = pd.to_datetime(daily_revenue["order_date"])
    revenue_forecast["date"] = pd.to_datetime(revenue_forecast["date"])

    return product_stats, product_forecast, top_10, worst_10, revenue_inventory, daily_revenue, revenue_forecast


product_stats, product_forecast, top_10, worst_10, revenue_inventory, daily_revenue, revenue_forecast = load_data()

st.title("Sales Forecasting & Inventory Planning Dashboard")
st.caption("Data Engineering → KPI Analysis → Linear Regression Forecasting → Inventory Recommendation")

st.divider()

total_revenue = product_stats["total_revenue"].sum()
total_quantity = product_stats["total_quantity_sold"].sum()
unique_products = product_stats["product"].nunique()
forecast_revenue = revenue_forecast["predicted_revenue"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"${total_revenue:,.2f}")
c2.metric("Total Units Sold", f"{total_quantity:,.0f}")
c3.metric("Unique Products", f"{unique_products}")
c4.metric("Forecasted 60-Day Revenue", f"${forecast_revenue:,.2f}")

st.divider()

st.subheader("Revenue Trend and 60-Day Forecast")

historical_chart = daily_revenue.rename(
    columns={"order_date": "date", "daily_revenue": "revenue"}
)

forecast_chart = revenue_forecast.rename(
    columns={"predicted_revenue": "revenue"}
)

historical_chart["type"] = "Historical Revenue"
forecast_chart["type"] = "Forecasted Revenue"

combined_revenue = pd.concat(
    [
        historical_chart[["date", "revenue", "type"]],
        forecast_chart[["date", "revenue", "type"]]
    ],
    ignore_index=True
)

fig_revenue = px.line(
    combined_revenue,
    x="date",
    y="revenue",
    color="type",
    markers=True,
    title="Historical Revenue vs Forecasted Revenue"
)

fig_revenue.update_layout(
    xaxis_title="Date",
    yaxis_title="Revenue",
    height=500
)

st.plotly_chart(fig_revenue, use_container_width=True)

st.divider()

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Top 10 Predicted Products")

    fig_top = px.bar(
        top_10,
        x="product",
        y="predicted_60_day_quantity",
        title="Top 10 Products for Next 60 Days",
        text_auto=".0f"
    )

    fig_top.update_layout(
        xaxis_title="Product",
        yaxis_title="Predicted Quantity",
        xaxis_tickangle=-45,
        height=500
    )

    st.plotly_chart(fig_top, use_container_width=True)

with right_col:
    st.subheader("Worst 10 Predicted Products")

    fig_worst = px.bar(
        worst_10,
        x="product",
        y="predicted_60_day_quantity",
        title="Worst 10 Products for Next 60 Days",
        text_auto=".0f"
    )

    fig_worst.update_layout(
        xaxis_title="Product",
        yaxis_title="Predicted Quantity",
        xaxis_tickangle=-45,
        height=500
    )

    st.plotly_chart(fig_worst, use_container_width=True)

st.divider()

st.subheader("Inventory Recommendation")

top_inventory = revenue_inventory.sort_values(
    by="recommended_inventory_order",
    ascending=False
).head(15)

fig_inventory = px.bar(
    top_inventory,
    x="product",
    y="recommended_inventory_order",
    title="Top Recommended Inventory Orders",
    text_auto=".0f",
    hover_data=[
        "projected_60_day_quantity",
        "projected_60_day_revenue",
        "estimated_price_per_unit"
    ]
)

fig_inventory.update_layout(
    xaxis_title="Product",
    yaxis_title="Recommended Inventory Order",
    xaxis_tickangle=-45,
    height=550
)

st.plotly_chart(fig_inventory, use_container_width=True)

st.divider()

st.subheader("Product-Level Forecast Table")

selected_product = st.selectbox(
    "Select a product to inspect",
    sorted(product_forecast["product"].unique())
)

selected_data = revenue_inventory[
    revenue_inventory["product"] == selected_product
]

st.dataframe(selected_data, use_container_width=True)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Product Stats",
        "Product Forecast",
        "Revenue + Inventory",
        "Revenue Forecast"
    ]
)

with tab1:
    st.dataframe(product_stats, use_container_width=True)

with tab2:
    st.dataframe(product_forecast, use_container_width=True)

with tab3:
    st.dataframe(revenue_inventory, use_container_width=True)

with tab4:
    st.dataframe(revenue_forecast, use_container_width=True)

st.divider()

st.markdown(
    """
    ### Method Used

    This dashboard uses cleaned sales data from the notebook output files.

    - Product KPIs are calculated using total quantity sold, total revenue, average quantity sold, and average revenue.
    - Top and worst products are predicted using average quantity sold projected over the next 60 days.
    - Revenue forecasting is done using Linear Regression on daily revenue.
    - Inventory recommendation is based on projected 60-day demand plus 10% safety stock.
    """
)