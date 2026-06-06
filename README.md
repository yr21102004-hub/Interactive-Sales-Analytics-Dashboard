# 📊 Smart Sales Analytics Dashboard | لوحة تحليل المبيعات الذكية

An interactive, high-performance sales analytics dashboard built using **Python**, **Streamlit**, and **Plotly**. This project features a premium bilingual interface (Arabic & English) and provides comprehensive data cleaning, KPI tracking, and interactive visualizations.

---

## 🚀 Key Features / المميزات الرئيسية

### 1. Bilingual Interface / واجهة ثنائية اللغة
- Toggle between **English** and **العربية** dynamically with the click of a button in the sidebar.

### 2. Premium Design / تصميم احترافي
- Dark-mode responsive theme.
- Elegant custom metrics layout with interactive hover effects and visual styling.
- Smooth Plotly animations.

### 3. Smart Data Cleaning & Quality Report / تقرير تنظيف وصحة البيانات
- Automatic type resolution (date, price, quantity).
- Handles missing data and removes duplicate transactions.
- Shows side-by-side data statistics (Original vs. Cleaned records).
- Option to preview the raw/cleaned data and download the cleaned dataset as a CSV file.

### 4. Five Key Metrics (KPIs) / مؤشرات الأداء الرئيسية
- **Total Revenue** (إجمالي الإيرادات)
- **Average Transaction Value** (متوسط قيمة الصفقة)
- **Total Units Sold** (إجمالي الوحدات المباعة)
- **Top-Selling Product** (المنتج الأكثر مبيعاً)
- **Top Active City** (المدينة الأكثر نشاطاً)

### 5. Interactive Visualizations / رسوم بيانية تفاعلية
- **Sales Trend & 3-Day Moving Average** (منحنى المبيعات الإجمالي والمعدل المتحرك)
- **Sales Distribution by City** (توزيع المبيعات حسب المدن - Donut Chart)
- **Revenue by Product** (إجمالي الإيرادات لكل منتج)
- **Correlation Heatmap** (مصفوفة الارتباط بين المتغيرات)
- **Category Distribution** (توزيع المبيعات حسب الفئات)

---

## 🛠️ Tech Stack / التقنيات المستخدمة

- **Frontend/App framework**: [Streamlit](https://streamlit.io/)
- **Data manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Interactive charts**: [Plotly Express & Plotly Graph Objects](https://plotly.com/)
- **Basic analysis scripts**: [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)

---

## 📁 Repository Structure / هيكل المشروع

```text
├── Interactive Sales Analytics Dashboard/
│   ├── app.py                             # Advanced Bilingual Streamlit Dashboard
│   ├── Advanced Sales Analytics.py        # Advanced Python script with local charts
│   ├── Sales Analysis.py                  # Basic sales analysis script
│   ├── Creat_Dataset.py                   # Script to generate synthetic sales dataset
│   ├── Advanced Sales Analytics.csv.txt   # Dataset (Advanced Sales)
│   ├── Sales Analysis.csv.txt            # Dataset (Basic Sales)
│   ├── dirty_sales_data.csv               # Dataset (Dirty Sales)
│   ├── Interactive_Data_Dashboard.py      # Basic Streamlit dashboard (Legacy)
│   └── *.png                              # Generated charts (Bar, Heatmap, Line, Pie)
└── README.md                              # Project documentation
```

---

## ▶️ How to Run / كيفية التشغيل

### 1. Clone the repository
```bash
git clone https://github.com/yr21102004-hub/Interactive-Sales-Analytics-Dashboard.git
cd Interactive-Sales-Analytics-Dashboard
```

### 2. Install dependencies
Make sure you have Python installed, then run:
```bash
pip install streamlit pandas numpy plotly matplotlib seaborn
```

### 3. Run the Dashboard
Run the Streamlit application using the command below:
```bash
streamlit run "Interactive Sales Analytics Dashboard/app.py"
```

---

## 💼 Author / المطور

Developed by **[Youssef Ramadan Mohammed](https://github.com/yr21102004-hub)**
