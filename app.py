# -----------------------------
# Import libraries
# -----------------------------
import streamlit as st
import pandas as pd
import snowflake.connector

# -----------------------------
# Snowflake Connection
# -----------------------------
conn = snowflake.connector.connect(
    user=st.secrets["SNOWFLAKE_USER"],
    password=st.secrets["SNOWFLAKE_PASSWORD"],
    account=st.secrets["SNOWFLAKE_ACCOUNT"],
    warehouse="RETAIL_WH",
    database="RETAIL_DB",
    schema="RETAIL_SCHEMA"
)

def run_query(query):
    return pd.read_sql(query, conn)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(layout="wide")

st.title("🛒 SmartMart Retail Analytics Dashboard")
st.markdown("Interactive sales analytics powered by Snowflake")

# -----------------------------
# Load Data
# -----------------------------
region_df = run_query("SELECT * FROM REGION_REVENUE")
monthly_df = run_query("SELECT * FROM MONTHLY_SALES")
category_df = run_query("SELECT * FROM CATEGORY_REVENUE")
products_df = run_query("SELECT * FROM TOP_10_PRODUCTS")
channel_df = run_query("SELECT * FROM CHANNEL_PERFORMANCE")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Region Filter
selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(region_df["REGION"].unique())
)

# Channel Filter
selected_channel = st.sidebar.selectbox(
    "Sales Channel",
    ["All"] + list(channel_df["SALES_CHANNEL"].unique())
)

# Category Filter (Multi-select = checkbox style)
selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=list(category_df["CATEGORY"].unique()),
    default=list(category_df["CATEGORY"].unique())
)

# -----------------------------
# Apply Filters
# -----------------------------
if selected_region != "All":
    region_df = region_df[region_df["REGION"] == selected_region]

if selected_channel != "All":
    channel_df = channel_df[channel_df["SALES_CHANNEL"] == selected_channel]

if selected_categories:
    category_df = category_df[category_df["CATEGORY"].isin(selected_categories)]

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
# Charts Layout
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Region")
    st.bar_chart(region_df.set_index("REGION")["TOTAL_REVENUE"])

with col2:
    st.subheader("Online vs Offline Sales")
    st.bar_chart(channel_df.set_index("SALES_CHANNEL")["TOTAL_REVENUE"])

# -----------------------------
# Monthly Trend
# -----------------------------
st.subheader("Monthly Sales Trend")
st.line_chart(monthly_df.set_index("SALES_MONTH")["MONTHLY_REVENUE"])

# -----------------------------
# Bottom Charts
# -----------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Category Revenue")
    st.bar_chart(category_df.set_index("CATEGORY")["TOTAL_REVENUE"])

with col4:
    st.subheader("Top 10 Products")
    st.bar_chart(products_df.set_index("PRODUCT_NAME")["TOTAL_REVENUE"])

# -----------------------------
# Explore Data Section
# -----------------------------
st.divider()

st.subheader("📊 Explore Data")

table_option = st.selectbox(
    "Select Table",
    ["Region Revenue","Monthly Sales","Category Revenue","Top Products"]
)

if table_option == "Region Revenue":
    st.dataframe(region_df, use_container_width=True)

elif table_option == "Monthly Sales":
    st.dataframe(monthly_df, use_container_width=True)

elif table_option == "Category Revenue":
    st.dataframe(category_df, use_container_width=True)

elif table_option == "Top Products":
    st.dataframe(products_df, use_container_width=True)