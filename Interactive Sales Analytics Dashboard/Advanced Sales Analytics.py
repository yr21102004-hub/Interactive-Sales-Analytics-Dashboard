import random as rn
import datetime as dt
from datetime import datetime as dat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def load_file(file_path):# open the CSV File
   try:
      df = pd.read_csv(file_path)
      return df
   except FileNotFoundError:
        print("File not found! Check path.")
        return None
def clean_data(df):# Data Cleaning
   if df is None:
      return None
   if  df["date"].dtype == "object":
      df["date"] = pd.to_datetime(df["date"])
   if df.isnull().sum().sum() > 0 or df.duplicated().sum()>0:
      df.dropna(inplace=True)
      df.drop_duplicates(inplace=True)
   return df
def add_total_column(df):
    if df is None:
       return None
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["total"] = df["price"] * df["quantity"]
    return df
""" Calculating Matrix"""
def get_total_revenue(df):# For Calculating Revenue
    total_revenue = df["total"].sum()
    return f"The Total Revenue = {total_revenue}"
def get_mean_sales(df):# For Calculating the Mean Sales
   mean_sales = np.mean(df["total"])
   return mean_sales
def get_best_product(df):# To find the best product in terms of total revenue.
   best_product = df.groupby("product")["total"].sum().idxmax() # Will give me the name of the row with the largest total value. 
   return best_product
def get_best_city(df):# To find the best city in terms of total revenue.
   best_city = df.groupby("city")["total"].sum().idxmax() # Will give me the name of the row with the largest total value.
   return best_city
def sales_by_product(df):
   sales_per_product = df.groupby("product")["total"].sum()
   return  sales_per_product
def sales_by_city(df):
   sales_per_city = df.groupby("city")["total"].sum()
   return  sales_per_city
"""Visualization"""
def plot_bar(df):
   product_sales = df.groupby("product")["total"].sum().reset_index()
   sns.barplot(x="product", y="total", data=product_sales)
   plt.savefig("Bar Chart.png")
   plt.show()
def plot_line(df):
   date_sales = df.groupby("date")["total"].sum().reset_index()
   sns.lineplot(x="date", y="total", data =date_sales)
   plt.savefig("Line Chart.png")
   plt.show()
def plot_pie(df):
    city_sales = df.groupby("city")["total"].sum()
    plt.pie(city_sales, labels=city_sales.index, autopct='%1.1f%%')
    plt.savefig("Pie Chart.png")
    plt.show()
def plot_heatmap(df):
    corr = df[["price", "quantity", "total"]].corr()
    sns.heatmap(corr, annot=True)
    plt.title("Correlation Heatmap")
    plt.savefig("Heatmap Chart.png")
    plt.show()
def main():
    file_path = r"E:\Computer Scienes\My Projects\My Teskes\Sales Analysis\Advanced Sales Analytics.csv.txt"
    df = load_file(file_path)
    if df is None:
        return
    df = clean_data(df)
    df = add_total_column(df)
    if df.empty:
        print("Dataset is empty!")
        return
    print(f"Total Revenue: {get_total_revenue(df)}")
    print(f"Mean Sales: {get_mean_sales(df):.2f}")
    print(f"Best Product: {get_best_product(df)}")
    print(f"Best City: {get_best_city(df)}")
    plot_bar(df)
    plot_line(df)
    plot_pie(df)
    plot_heatmap(df)
if __name__ == "__main__": # For Operation The Code
    main()