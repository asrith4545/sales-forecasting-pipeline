import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Forecast Dashboard",
    layout="wide"
)

st.title("Sales Forecasting and Inventory Analytics Dashboard")

product_stats = pd.read_csv(
    "../output/task1_product_stats.csv"
)

product_forecast = pd.read_csv(
    "../output/task2_product_forecast.csv"
)

top_10_products = pd.read_csv(
    "../output/task2_top_10_products.csv"
)

worst_10_products = pd.read_csv(
    "../output/task2_worst_10_products.csv"
)

revenue_inventory = pd.read_csv(
    "../output/task3_revenue_inventory.csv"
)

daily_revenue_forecast = pd.read_csv(
    "../output/task3_daily_revenue_forecast.csv"
)

total_revenue = product_stats["total_revenue"].sum()

total_quantity = product_stats["total_quantity_sold"].sum()

total_products = product_stats["product"].nunique()

forecasted_revenue = (
    daily_revenue_forecast["predicted_revenue"].sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "Total Quantity Sold",
    f"{total_quantity:,.0f}"
)

col3.metric(
    "Total Products",
    total_products
)

col4.metric(
    "Forecasted 60-Day Revenue",
    f"${forecasted_revenue:,.2f}"
)

st.divider()

st.header("Task 1 — Sales Statistics")

fig_revenue = px.bar(
    product_stats.head(10),
    x="product",
    y="total_revenue",
    title="Top Revenue Generating Products"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)

st.dataframe(
    product_stats.head(10)
)

st.divider()

st.header("Task 2 — Product Forecasting")

fig_top_products = px.bar(
    top_10_products,
    x="product",
    y="predicted_60_day_quantity",
    title="Top 10 Predicted Products"
)

st.plotly_chart(
    fig_top_products,
    use_container_width=True
)

st.dataframe(
    top_10_products
)

fig_worst_products = px.bar(
    worst_10_products,
    x="product",
    y="predicted_60_day_quantity",
    title="Worst 10 Predicted Products"
)

st.plotly_chart(
    fig_worst_products,
    use_container_width=True
)

st.dataframe(
    worst_10_products
)

st.divider()

st.header("Task 3 — Revenue Forecasting")

daily_revenue_forecast["date"] = pd.to_datetime(
    daily_revenue_forecast["date"]
)

fig_forecast = px.line(
    daily_revenue_forecast,
    x="date",
    y="predicted_revenue",
    title="60-Day Revenue Forecast"
)

st.plotly_chart(
    fig_forecast,
    use_container_width=True
)

st.dataframe(
    daily_revenue_forecast.head(20)
)

st.divider()

st.header("Inventory Recommendation")

top_inventory = revenue_inventory.sort_values(
    by="recommended_inventory_order",
    ascending=False
).head(10)

fig_inventory = px.bar(
    top_inventory,
    x="product",
    y="recommended_inventory_order",
    title="Top Inventory Orders"
)

st.plotly_chart(
    fig_inventory,
    use_container_width=True
)

st.dataframe(
    top_inventory
)

st.divider()

st.header("Download CSV Reports")

st.download_button(
    label="Download Product Statistics",
    data=product_stats.to_csv(index=False),
    file_name="task1_product_stats.csv",
    mime="text/csv"
)

st.download_button(
    label="Download Product Forecast",
    data=product_forecast.to_csv(index=False),
    file_name="task2_product_forecast.csv",
    mime="text/csv"
)

st.download_button(
    label="Download Revenue Forecast",
    data=daily_revenue_forecast.to_csv(index=False),
    file_name="task3_daily_revenue_forecast.csv",
    mime="text/csv"
)

st.download_button(
    label="Download Inventory Recommendation",
    data=revenue_inventory.to_csv(index=False),
    file_name="task3_revenue_inventory.csv",
    mime="text/csv"
)