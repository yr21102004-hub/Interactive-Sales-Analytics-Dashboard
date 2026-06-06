import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard | لوحة تحليل المبيعات",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS
st.markdown("""
    <style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Tajawal:wght@400;500;700;900&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', 'Tajawal', sans-serif;
    }
    
    /* Metrics design */
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border-color: #4CAF50;
    }
    .metric-title {
        font-size: 14px;
        color: #888888;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #1E88E5;
    }
    
    /* Top title styling */
    .dashboard-title {
        font-size: 38px;
        font-weight: 800;
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 50%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to load and clean data
def load_and_preprocess_data(file_path):
    try:
        if isinstance(file_path, str) and not os.path.isabs(file_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            resolved_path = os.path.join(script_dir, file_path)
            if os.path.exists(resolved_path):
                file_path = resolved_path
        df = pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None, None
    
    # Track cleaning actions
    initial_shape = df.shape
    
    # 1. Normalize column names
    col_mapping = {
        'Sale_Date': 'date', 'Date': 'date',
        'Product_Name': 'product', 'Product': 'product',
        'Quantity_Sold': 'quantity', 'Quantity': 'quantity',
        'Unit_Price': 'price', 'Price': 'price',
        'City': 'city', 'City_Name': 'city',
        'Category': 'category'
    }
    # Case-insensitive mapping
    rename_dict = {}
    for col in df.columns:
        col_lower = col.strip().lower()
        for k, v in col_mapping.items():
            if col_lower == k.lower():
                rename_dict[col] = v
                break
    df = df.rename(columns=rename_dict)
    
    # Standardize columns to ensure key fields exist
    required_cols = ['date', 'product', 'quantity', 'price', 'city']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.warning(f"Missing essential columns mapping to: {missing_cols}. Attempting to proceed.")
        
    # Convert types
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
    # Data Cleaning
    num_missing_before = df.isnull().sum().sum()
    num_duplicates_before = df.duplicated().sum()
    
    df = df.dropna(subset=[c for c in required_cols if c in df.columns])
    df = df.drop_duplicates()
    
    # Recalculate total/revenue
    df['total'] = df['price'] * df['quantity']
    
    final_shape = df.shape
    
    cleaning_report = {
        'initial_rows': initial_shape[0],
        'final_rows': final_shape[0],
        'missing_removed': initial_shape[0] - final_shape[0] - num_duplicates_before,
        'duplicates_removed': num_duplicates_before
    }
    
    return df, cleaning_report

# Sidebar Setup
st.sidebar.markdown("## ⚙️ Settings / الإعدادات")

# Language toggle
lang = st.sidebar.selectbox(
    "Select Language / اختر اللغة",
    ["العربية", "English"]
)

# Text dictionary for localization
t = {
    "العربية": {
        "title": "📊 لوحة تحليل المبيعات الذكية",
        "subtitle": "تحليل أداء المبيعات، المنتجات الأكثر مبيعاً، والمبيعات الجغرافية",
        "data_source": "اختر مصدر البيانات",
        "upload": "تحميل ملف CSV خاص بك",
        "preloaded": "البيانات الافتراضية المتاحة",
        "advanced_sales": "تحليلات مبيعات متقدمة (Advanced Sales)",
        "basic_sales": "تحليل مبيعات أساسي (Sales Analysis)",
        "filters": "تصفية البيانات",
        "city_filter": "المدينة",
        "product_filter": "المنتج",
        "date_filter": "الفترة الزمنية",
        "kpi_total_revenue": "إجمالي الإيرادات",
        "kpi_mean_sales": "متوسط قيمة الصفقة",
        "kpi_best_prod": "المنتج الأكثر مبيعاً",
        "kpi_best_city": "المدينة الأكثر نشاطاً",
        "kpi_units_sold": "إجمالي الوحدات المباعة",
        "tab_overview": "📈 نظرة عامة",
        "tab_deep_dive": "🔬 تحليل متعمق",
        "tab_data_details": "📋 تفاصيل البيانات",
        "chart_sales_over_time": "منحنى المبيعات الإجمالي والمعدل المتحرك",
        "chart_top_products": "إجمالي الإيرادات لكل منتج",
        "chart_city_sales": "توزيع المبيعات حسب المدن",
        "chart_heatmap": "مصفوفة الارتباط بين المتغيرات",
        "raw_preview": "معاينة البيانات الخام",
        "cleaning_status": "تقرير تنظيف البيانات وصحتها",
        "download_clean": "تحميل البيانات النظيفة (CSV)",
        "all": "الكل"
    },
    "English": {
        "title": "📊 Smart Sales Analytics Dashboard",
        "subtitle": "Analyze sales performance, top-selling products, and geographic sales",
        "data_source": "Select Data Source",
        "upload": "Upload your own CSV file",
        "preloaded": "Preloaded Default Datasets",
        "advanced_sales": "Advanced Sales Analytics",
        "basic_sales": "Basic Sales Analysis",
        "filters": "Data Filters",
        "city_filter": "City",
        "product_filter": "Product",
        "date_filter": "Date Range",
        "kpi_total_revenue": "Total Revenue",
        "kpi_mean_sales": "Average Transaction",
        "kpi_best_prod": "Top Product",
        "kpi_best_city": "Top City",
        "kpi_units_sold": "Total Units Sold",
        "tab_overview": "📈 Overview",
        "tab_deep_dive": "🔬 Deep Dive",
        "tab_data_details": "📋 Data Details",
        "chart_sales_over_time": "Sales Trend & Moving Average",
        "chart_top_products": "Revenue by Product",
        "chart_city_sales": "Sales Distribution by City",
        "chart_heatmap": "Correlation Heatmap",
        "raw_preview": "Raw Data Preview",
        "cleaning_status": "Data Cleaning & Quality Report",
        "download_clean": "Download Clean Data (CSV)",
        "all": "All"
    }
}[lang]

# Main Dashboard Title
st.markdown(f'<div class="dashboard-title">{t["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<p style="color:#666666; font-size:16px;">{t["subtitle"]}</p>', unsafe_allow_html=True)
st.markdown("---")

# Data Source Selection
data_option = st.sidebar.radio(
    t["data_source"],
    ["Preloaded Datasets", "Upload CSV"]
)

file_path = None
df = None
uploaded_file = None

if data_option == "Preloaded Datasets":
    dataset_choice = st.sidebar.selectbox(
        t["preloaded"],
        [t["advanced_sales"], t["basic_sales"]]
    )
    if dataset_choice == t["advanced_sales"]:
        file_path = "Advanced Sales Analytics.csv.txt"
    else:
        file_path = "Sales Analysis.csv.txt"
else:
    uploaded_file = st.sidebar.file_uploader(t["upload"], type=["csv", "txt"])

# Load dataset
if file_path:
    df, clean_report = load_and_preprocess_data(file_path)
elif uploaded_file is not None:
    df, clean_report = load_and_preprocess_data(uploaded_file)
else:
    st.info("Please upload a file or select a preloaded dataset in the sidebar. / يرجى اختيار مصدر للبيانات من القائمة الجانبية.")

if df is not None:
    # ------------------ Sidebar Filters ------------------
    st.sidebar.markdown(f"### 🔍 {t['filters']}")
    
    # City Filter
    cities = [t["all"]] + sorted(df['city'].dropna().unique().tolist())
    selected_city = st.sidebar.selectbox(t["city_filter"], cities)
    
    # Product Filter
    products = [t["all"]] + sorted(df['product'].dropna().unique().tolist())
    selected_product = st.sidebar.selectbox(t["product_filter"], products)
    
    # Date Range Filter
    min_date = df['date'].min().to_pydatetime()
    max_date = df['date'].max().to_pydatetime()
    selected_date_range = st.sidebar.date_input(
        t["date_filter"],
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply Filters
    df_filtered = df.copy()
    if selected_city != t["all"]:
        df_filtered = df_filtered[df_filtered['city'] == selected_city]
    if selected_product != t["all"]:
        df_filtered = df_filtered[df_filtered['product'] == selected_product]
    
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        df_filtered = df_filtered[
            (df_filtered['date'].dt.date >= start_date) & 
            (df_filtered['date'].dt.date <= end_date)
        ]
        
    # If filtered dataframe is empty
    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your criteria. / لا توجد بيانات مطابقة للتصفية المختارة.")
    else:
        # Calculate KPIs
        total_revenue = df_filtered['total'].sum()
        mean_sales = df_filtered['total'].mean()
        total_units = df_filtered['quantity'].sum()
        
        # Best product & city
        best_product_series = df_filtered.groupby("product")["total"].sum()
        best_product = best_product_series.idxmax() if not best_product_series.empty else "N/A"
        
        best_city_series = df_filtered.groupby("city")["total"].sum()
        best_city = best_city_series.idxmax() if not best_city_series.empty else "N/A"
        
        # ------------------ KPI Metrics Cards Layout ------------------
        kpi_cols = st.columns(5)
        
        kpis = [
            (t["kpi_total_revenue"], f"${total_revenue:,.2f}", "#1E88E5"),
            (t["kpi_mean_sales"], f"${mean_sales:,.2f}", "#4CAF50"),
            (t["kpi_units_sold"], f"{int(total_units):,}", "#FF9800"),
            (t["kpi_best_prod"], f"{best_product}", "#E91E63"),
            (t["kpi_best_city"], f"{best_city}", "#9C27B0")
        ]
        
        for col, (title, value, color) in zip(kpi_cols, kpis):
            with col:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">{title}</div>
                        <div class="metric-value" style="color: {color};">{value}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ------------------ Main Panel Tabs ------------------
        tab_overview, tab_deep_dive, tab_data_details = st.tabs([
            t["tab_overview"],
            t["tab_deep_dive"],
            t["tab_data_details"]
        ])
        
        # --- TAB 1: OVERVIEW ---
        with tab_overview:
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.markdown(f"#### {t['chart_sales_over_time']}")
                # Sales trend over time (daily/weekly aggregation)
                df_time = df_filtered.groupby('date')['total'].sum().reset_index().sort_values('date')
                df_time['rolling_mean'] = df_time['total'].rolling(window=3, min_periods=1).mean()
                
                fig_time = go.Figure()
                fig_time.add_trace(go.Scatter(
                    x=df_time['date'], y=df_time['total'],
                    mode='lines+markers', name='Daily Sales',
                    line=dict(color='#1E88E5', width=2),
                    marker=dict(size=6)
                ))
                fig_time.add_trace(go.Scatter(
                    x=df_time['date'], y=df_time['rolling_mean'],
                    mode='lines', name='3-Day Trend',
                    line=dict(color='#FF9800', width=3, dash='dash')
                ))
                fig_time.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                )
                st.plotly_chart(fig_time, width='stretch')
                
            with col_right:
                st.markdown(f"#### {t['chart_city_sales']}")
                city_summary = df_filtered.groupby('city')['total'].sum().reset_index()
                fig_city = px.pie(
                    city_summary, values='total', names='city',
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_city.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_city, width='stretch')
                
            # Product Performance Chart
            st.markdown(f"#### {t['chart_top_products']}")
            product_summary = df_filtered.groupby('product')['total'].sum().reset_index().sort_values('total', ascending=False)
            fig_prod = px.bar(
                product_summary, x='product', y='total',
                color='total',
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={'total': 'Revenue ($)', 'product': 'Product'}
            )
            fig_prod.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=25, b=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_prod, width='stretch')
            
        # --- TAB 2: DEEP DIVE ---
        with tab_deep_dive:
            col_dd_left, col_dd_right = st.columns(2)
            
            with col_dd_left:
                st.markdown(f"#### {t['chart_heatmap']}")
                # Correlation Heatmap between price, quantity, and total
                numerical_cols = ['price', 'quantity', 'total']
                corr_cols = [c for c in numerical_cols if c in df_filtered.columns]
                corr_matrix = df_filtered[corr_cols].corr()
                
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1
                )
                fig_corr.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_corr, width='stretch')
                
            with col_dd_right:
                st.markdown("#### 🛍️ Category Distribution / توزيع الفئات" if lang == "العربية" else "#### 🛍️ Category Distribution")
                if 'category' in df_filtered.columns:
                    category_summary = df_filtered.groupby('category')['total'].sum().reset_index().sort_values('total', ascending=False)
                    fig_cat = px.bar(
                        category_summary, y='category', x='total',
                        orientation='h',
                        color='total',
                        color_continuous_scale=px.colors.sequential.Plasma
                    )
                    fig_cat.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    st.plotly_chart(fig_cat, width='stretch')
                else:
                    st.info("Category column not available in this dataset. / عمود الفئة غير متوفر في هذه البيانات.")
                    
        # --- TAB 3: DATA DETAILS & CLEANING ---
        with tab_data_details:
            # Display cleaning statistics
            st.markdown(f"#### {t['cleaning_status']}")
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric(
                    label="Original Row Count / الصفوف الأصلية",
                    value=f"{clean_report['initial_rows']}"
                )
            with stat_col2:
                st.metric(
                    label="Duplicates Removed / التكرارات المزالة",
                    value=f"{clean_report['duplicates_removed']}"
                )
            with stat_col3:
                st.metric(
                    label="Cleaned Row Count / الصفوف النظيفة",
                    value=f"{clean_report['final_rows']}"
                )
                
            # Preview and Download
            st.markdown(f"#### {t['raw_preview']}")
            st.dataframe(df_filtered, width='stretch')
            
            # Download Button
            csv_data = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=t["download_clean"],
                data=csv_data,
                file_name="cleaned_sales_data.csv",
                mime="text/csv"
            )
