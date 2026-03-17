# Import libraries
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# Session
session = get_active_session()

st.set_page_config(layout="wide")

st.title("🛒 SmartMart Retail Analytics Dashboard")

# -----------------------------
# Load Data
# -----------------------------

region_df = session.sql("SELECT * FROM REGION_REVENUE").to_pandas()
monthly_df = session.sql("SELECT * FROM MONTHLY_SALES").to_pandas()
category_df = session.sql("SELECT * FROM CATEGORY_REVENUE").to_pandas()
products_df = session.sql("SELECT * FROM TOP_10_PRODUCTS").to_pandas()
channel_df = session.sql("SELECT * FROM CHANNEL_PERFORMANCE").to_pandas()

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(region_df["REGION"].unique())
)

selected_channel = st.sidebar.selectbox(
    "Sales Channel",
    ["All"] + list(channel_df["SALES_CHANNEL"].unique())
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + list(category_df["CATEGORY"].unique())
)

# -----------------------------
# Apply Filters
# -----------------------------

if selected_region != "All":
    region_df = region_df[region_df["REGION"] == selected_region]

if selected_channel != "All":
    channel_df = channel_df[channel_df["SALES_CHANNEL"] == selected_channel]

if selected_category != "All":
    category_df = category_df[category_df["CATEGORY"] == selected_category]

# -----------------------------
# KPI Section
# -----------------------------

total_revenue = region_df["TOTAL_REVENUE"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Products", len(products_df))
col3.metric("🛍 Channels", channel_df["SALES_CHANNEL"].nunique())

st.divider()

# -----------------------------
# Charts Layout (2 Columns)
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Region")
    st.bar_chart(region_df.set_index("REGION")["TOTAL_REVENUE"])

with col2:
    st.subheader("Online vs Offline Sales")
    st.bar_chart(channel_df.set_index("SALES_CHANNEL")["TOTAL_REVENUE"])

# -----------------------------
# Monthly Trend (Full Width)
# -----------------------------

st.subheader("Monthly Sales Trend")
st.line_chart(monthly_df.set_index("SALES_MONTH")["MONTHLY_REVENUE"])

# -----------------------------
# Bottom Section
# -----------------------------

col3, col4 = st.columns(2)

with col3:
    st.subheader("Category Revenue")
    st.bar_chart(category_df.set_index("CATEGORY")["TOTAL_REVENUE"])

with col4:
    st.subheader("Top 10 Products")
    st.bar_chart(products_df.set_index("PRODUCT_NAME")["TOTAL_REVENUE"])

# -----------------------------
# Data Viewer
# -----------------------------

st.subheader("📊 Explore Data")

table_option = st.selectbox(
    "Select Table",
    ["Region Revenue","Monthly Sales","Category Revenue","Top Products"]
)

if table_option == "Region Revenue":
    st.dataframe(region_df)

elif table_option == "Monthly Sales":
    st.dataframe(monthly_df)

elif table_option == "Category Revenue":
    st.dataframe(category_df)

elif table_option == "Top Products":
    st.dataframe(products_df)