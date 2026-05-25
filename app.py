import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Adidas Sales Dashboard", page_icon="👟", layout="wide")

st.title("Adidas Sales Dashboard 👟")
st.markdown("### Interactive Project Analytics & Insights")

df = pd.read_excel('Adidas Data.xlsx', skiprows=4)

st.sidebar.header("Filter Options")
sales_method = st.sidebar.multiselect(
    "Select Sales Method:",
    options=df["Sales Method"].unique(),
    default=df["Sales Method"].unique()
)

df_filtered = df[df["Sales Method"].isin(sales_method)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Rows Available", len(df_filtered))
col2.metric("Total Sales ($)", f"{df_filtered['Total Sales'].sum():,.0f}")
col3.metric("Total Profit ($)", f"{df_filtered['Operating Profit'].sum():,.0f}")

st.markdown("---")

st.subheader("📊 Data Preview")
st.dataframe(df_filtered.head(10), use_container_width=True)

st.subheader("📈 Visualizations")
fig, ax = plt.subplots(figsize=(6, 4))
df_filtered['Sales Method'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#ff9999','#66b3ff','#99ff99'])
ax.set_ylabel('')
st.pyplot(fig)
