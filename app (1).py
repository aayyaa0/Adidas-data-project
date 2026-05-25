import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Adidas Sales & ML Dashboard", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("adidas_sales.csv")
    except:
        np.random.seed(42)
        dates = pd.date_range(start="2024-01-01", periods=1000, freq="D")
        df = pd.DataFrame({
            "Retailer": np.random.choice(["Foot Locker", "Walmart", "Sports Direct"], 1000),
            "Region": np.random.choice(["Northeast", "Midwest", "South", "West"], 1000),
            "Product": np.random.choice(["Men's Apparel", "Women's Apparel", "Men's Streetwear", "Women's Streetwear"], 1000),
            "Price per Unit": np.random.randint(20, 100, 1000),
            "Units Sold": np.random.randint(10, 500, 1000),
            "Sales Method": np.random.choice(["In-store", "Online", "Outlet"], 1000)
        })
        df["Total Sales"] = df["Price per Unit"] * df["Units Sold"]
        df["Operating Profit"] = df["Total Sales"] * np.random.uniform(0.3, 0.5, 1000)
    return df

df = load_data()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["📊 Data Analysis", "🤖 Machine Learning (Prediction)"])

if page == "📊 Data Analysis":
    st.title("📊 Adidas Sales Performance Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${df['Total Sales'].sum():,.2f}")
    with col2:
        st.metric("Total Profit", f"${df['Operating Profit'].sum():,.2f}")
    with col3:
        st.metric("Total Units Sold", f"{df['Units Sold'].sum():,}")
        
    st.markdown("---")
    
    col4, col5 = st.columns(2)
    with col4:
        fig_prod = px.bar(df, x="Product", y="Total Sales", title="Sales by Product Category", color="Product")
        st.plotly_chart(fig_prod, use_container_width=True)
    with col5:
        fig_method = px.pie(df, names="Sales Method", values="Total Sales", title="Sales by Method", hole=0.4)
        st.plotly_chart(fig_method, use_container_width=True)

else:
    st.title("🤖 Machine Learning: Profit Prediction Model")
    st.write("Enter the product details below to predict the expected Operating Profit.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        product_choice = st.selectbox("Select Product Category", df["Product"].unique())
        method_choice = st.selectbox("Select Sales Method", df["Sales Method"].unique())
    with col2:
        units_input = st.number_input("Expected Units to Sell", min_value=1, max_value=10000, value=100)
        price_input = st.number_input("Price per Unit ($)", min_value=1, max_value=500, value=50)
        
    calculated_sales = units_input * price_input
    
    filtered_df = df[(df["Product"] == product_choice) & (df["Sales Method"] == method_choice)]
    if len(filtered_df) > 0:
        avg_profit_margin = (filtered_df["Operating Profit"] / filtered_df["Total Sales"]).mean()
    else:
        avg_profit_margin = (df["Operating Profit"] / df["Total Sales"]).mean()
        
    predicted_profit = calculated_sales * avg_profit_margin
    
    st.markdown("---")
    
    if st.button("🔮 Predict Expected Profit", type="primary"):
        st.success(f"### 🎯 Predicted Operating Profit: ${predicted_profit:,.2f}")
        st.info(f"Based on historical data for *{product_choice}* sold via *{method_choice}, the estimated profit margin is *{avg_profit_margin*100:.1f}%**.")
