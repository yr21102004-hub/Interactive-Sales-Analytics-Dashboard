import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#  Title
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Data Dashboard (Cleaned & Interactive)")
#   uploaded data
@st.cache_data
def load_data():
    df = pd.read_csv("dirty_sales_data.csv")
    return df
df = load_data()
# -----------------------------
#   Data Cleaning
# -----------------------------
st.header("🧹 Data Cleaning")
#   Removal of duplication
df = df.drop_duplicates()
#  Convert Date
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors='coerce')
#   Missing Values
df["City"].fillna("Unknown", inplace=True)
df["Category"].fillna("Unknown", inplace=True)
df["Sales"].fillna(df["Sales"].mean(), inplace=True)
st.success("Data cleaned successfully!")
#  Display Data
with st.expander("Show Cleaned Data"):
    st.dataframe(df)

# -----------------------------
#    Filters
# -----------------------------

st.sidebar.header("🔍 Filters")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# 
filtered_df = df[
    (df["City"].isin(selected_city)) &
    (df["Category"].isin(selected_category))
]
# -----------------------------
#    KPIs
# -----------------------------
st.header("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{int(filtered_df['Sales'].sum())}")
col2.metric("Total Orders", f"{len(filtered_df)}")
col3.metric("Avg Sales", f"{round(filtered_df['Sales'].mean(),2)}")
# -----------------------------
#  Visualizations
# -----------------------------
st.header("📊 Visualizations")
# 1. Sales by City
fig1, ax1 = plt.subplots()
filtered_df.groupby("City")["Sales"].sum().plot(kind="bar", ax=ax1)
ax1.set_title("Total Sales by City")
st.pyplot(fig1)
# 2. Sales by Category
fig2, ax2 = plt.subplots()
sns.barplot(x="Category", y="Sales", data=filtered_df, ax=ax2)
ax2.set_title("Sales by Category")
st.pyplot(fig2)
# 3. Sales Over Time
fig3, ax3 = plt.subplots()
filtered_df.groupby("Order_Date")["Sales"].sum().plot(ax=ax3)
ax3.set_title("Sales Over Time")
st.pyplot(fig3)
# 4. Distribution
fig4, ax4 = plt.subplots()
sns.histplot(filtered_df["Sales"], kde=True, ax=ax4)
ax4.set_title("Sales Distribution")
st.pyplot(fig4)
# -----------------------------
#   Insights Section
# -----------------------------
st.header("🧠 Insights")
st.write(f"""
- Highest total sales: {filtered_df.groupby("City")["Sales"].sum().idxmax()}
- Most selling category: {filtered_df.groupby("Category")["Sales"].sum().idxmax()}
- Average sales value: {round(filtered_df["Sales"].mean(),2)}
""")