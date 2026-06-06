# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Load data
df = pd.read_csv("sales_data.csv")
# Data cleaning
df = df.dropna()              # remove missing values
df = df.drop_duplicates()     # remove duplicates
df['date'] = pd.to_datetime(df['date'])  # convert to datetime
# Create revenue column
df['revenue'] = df['quantity'] * df['price']
# Analysis
total_revenue = df['revenue'].sum()
top_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
top_cities = df.groupby('city')['revenue'].sum().sort_values(ascending=False)
# NumPy stats
mean_revenue = np.mean(df['revenue'])
std_revenue = np.std(df['revenue'])
# Visualization
top_products.head(5).plot(kind='bar', title='Top Products')
plt.show()
sales_over_time = df.groupby('date')['revenue'].sum()
sales_over_time.plot(kind='line', title='Sales Over Time')
plt.show()
plt.figure(figsize=(8,5))
sns.barplot(x=top_cities.index, y=top_cities.values)
plt.title("Sales by City")
plt.xticks(rotation=45)
plt.show()
# Trend (moving average)
sales_over_time.rolling(window=3).mean().plot(title="Trend")
plt.show()