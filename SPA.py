#Sales Performance Analysis (Descriptive Analytics) SPA
#To be renamed as project_1_sales_analysis

'''
Business Context
A small retail business wants to understand:
    - Which products sell best
    - Seasonal trends
    - Revenue contributions by category / highlight strong vs weak regions

Skills practiced
    - Data cleaning
    - Exploratory Data Analysis (EDA)
    - Visualization
    - Business insight generation

Dataset
    - Superstore Sales Dataset (CSV)
    - Columns : Order Date, Product, Category, Sales, Quantity, Region
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Improve plot appearance
sns.set(style='darkgrid')

# Load data
df = pd.read_csv("data/sales.csv")

# print(df.head(15))
# print(df.info())
# print(df.describe())

plt.figure(figsize=(8,5))
sns.histplot(df['Sales'], bins=20)
plt.title('Distribution of Sales')
plt.tight_layout()
# plt.savefig('output/figures/sales_distribution.png')
# plt.show()
# plt.close()

'''Step 2
Ensure the dataset is :
    - correct
    - consistent
    -ready for analysis
    
changed order date from str to datetime object
'''
df["Order Date"] = pd.to_datetime(df["Order Date"])
print(df.dtypes)

#Check missing values, if 0 no action required
print(df.isnull().sum())

#Check duplicate rows
duplicate_count = df.duplicated().sum()
print(f"There are {duplicate_count} duplicate rows")
#if exist, drop, but if theres a chance someone buys two times or more the same item on the same day, its best to make sure if its valid or an err
df.drop_duplicates(inplace=True)

#Validate sales calculation
df["CalculatedSales"] = df["Quantity"] * df["UnitPrice"]

#Check mismatches
mismatch = df[df["Sales"] != df["CalculatedSales"]]
print(mismatch)

#Expected empty dataFrame, means no duplicate rows
#double checked after theres mismatches
df["Sales"] = df["CalculatedSales"]
#then drop helper column
df.drop(columns=["CalculatedSales"], inplace=True)
#this demonstrates data trustworthiness checks

#Validate numerical ranges, quantity, unitprice, sales < 0
# print(df[["Quantity", "UnitPrice", "Sales"]].describe())

#Standardize
df["Category"] = df["Category"].str.strip().str.title()
df["Region"] = df["Region"].str.strip().str.title()

#final check
# print(df.head())
# print(df.info())

'''
Step 3
Exploratory Data analysis
Transform cleaned data into business insight by answering specific questions
'''

#How does total sales change over time? answer, monthly sales aggregation
df["Month"] = df["Order Date"].dt.to_period("M")
monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()
monthly_sales["Month"] = monthly_sales["Month"].astype(str)

print(monthly_sales)
print()

#trend
#sns.lineplot
plt.figure(figsize=(10,5))
mst = sns.lineplot(data=monthly_sales, x="Month", y="Sales", marker="o")
for x, y in zip(monthly_sales["Month"], monthly_sales["Sales"]):
    mst.text(x, y + 27, f'{y}', ha='center', fontsize='8', color='black')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("output/figures/monthly_sales_trend.png")
# plt.show()

#Which product categories generate the most revenue? answer, sales by category
#sns.barplot
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

print(category_sales)
print()

plt.figure(figsize=(8,5))
sns.barplot(data=category_sales, x="Category", y="Sales")
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("output/figures/category_sales.png")
# plt.show()

#which regions perform best? answer sales by region
region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

print(region_sales)

plt.figure(figsize=(12,5))
sbr = sns.barplot(data=region_sales, x="Region", y="Sales")
for p in sbr.patches:
    sbr.annotate(f'{p.get_height():.0f}',
                (p.get_x() + p.get_width() / 2., p.get_height() / 2.),
                ha='center', va='top', fontsize=10, color='white')
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig("output/figures/region_sales.png")
# plt.show()

#What does a typical order look like
plt.figure(figsize=(10,5))
sns.histplot(df["Sales"], bins=20)
plt.title('Distribution of Sales per order')
plt.xlabel('Sales Amount')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.savefig("output/figures/sales_distribution.png")
# plt.show()

#top products by revenue
top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

print(top_products)

plt.figure(figsize=(9,5))
tpp = sns.barplot(data=top_products, x="Product", y="Sales")
for p in tpp.patches:
    tpp.annotate(f'{p.get_height():.0f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black')
plt.title('Top 5 Products')
plt.xlabel('Product')
plt.ylabel('Sales Amount')
plt.tight_layout()
plt.savefig("output/figures/top_products.png")
plt.show()

'''
Step 4
insights, recommendations and reporting
we will transform it into
    - clear business insights
    - actionable recommendations
    - a clean, recruiter-friendly README
'''

'''
Insight 1 - sales trend over time
    - Observation, overall upward trend from Jan to Mar
    Jan records the highest total monthly sales
    - Interpretation, 
    
Insight 2 - Category performance
    - Technology generates the highest revenue
    - Furniture is second
    - Office Supplies contributes smaller but consistent revenue
    
Insight 3 - Regional performance
    - Observation, west and east outperform others while central region shows weaker sales
    - Interpretation, market strength varies significantly by geography, targeted regional campaigns
'''

