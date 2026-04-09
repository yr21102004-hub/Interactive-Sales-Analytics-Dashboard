import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# عدد الصفوف
n_rows = 5000

# بيانات عشوائية
cities = ["Cairo", "Alex", "Giza", "Mansoura", "Tanta"]
categories = ["Electronics", "Clothing", "Food", "Books"]

data = []

start_date = datetime(2022, 1, 1)

for i in range(n_rows):
    row = {
        "Order_ID": i,
        "City": random.choice(cities),
        "Category": random.choice(categories),
        "Sales": random.randint(50, 1000),
        "Quantity": random.randint(1, 10),
        # التاريخ String مش datetime
        "Order_Date": (start_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    }
    data.append(row)

df = pd.DataFrame(data)

# 🔥 1. إدخال Missing Values
for col in ["City", "Category", "Sales"]:
    df.loc[df.sample(frac=0.1).index, col] = np.nan

# 🔥 2. إدخال Duplicate Rows
duplicates = df.sample(frac=0.1)
df = pd.concat([df, duplicates], ignore_index=True)

# 🔥 3. خلط البيانات
df = df.sample(frac=1).reset_index(drop=True)

# حفظ الملف
df.to_csv("dirty_sales_data.csv", index=False)

print("Dataset generated successfully!")