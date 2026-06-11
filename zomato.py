import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import warnings
warnings.filterwarnings('ignore')

# ── 1. LOAD DATA ──────────────────────────────────────────────
df = pd.read_csv('D:/zomato.csv', encoding='latin-1')
print("Shape:", df.shape)
print(df.head(2))

# ── 2. BASIC CLEANING ─────────────────────────────────────────

# Rename column for easier access
df.rename(columns={'approx_cost(for two people)': 'cost',
                   'listed_in(type)': 'listed_type',
                   'listed_in(city)': 'listed_city'}, inplace=True)

# Clean 'rate' column: "4.1/5" → 4.1
df['rate'] = df['rate'].astype(str).str.replace('/5', '', regex=False).str.strip()
df['rate'] = pd.to_numeric(df['rate'], errors='coerce')

# Clean 'cost' column: remove commas → numeric
df['cost'] = df['cost'].astype(str).str.replace(',', '', regex=False).str.strip()
df['cost'] = pd.to_numeric(df['cost'], errors='coerce')

# Clean 'votes'
df['votes'] = pd.to_numeric(df['votes'], errors='coerce')

# Clean yes/no columns
df['online_order'] = df['online_order'].str.strip()
df['book_table']   = df['book_table'].str.strip()

# Drop duplicates
df.drop_duplicates(inplace=True)

print("\nNull values:\n", df.isnull().sum())
print("\nData types:\n", df.dtypes)

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:aryan@localhost:5432/postgres')
# Store DataFrame to SQL table
df.to_sql(
    name='zomato',        # Table name
    con=engine,             # Database connection
    if_exists='replace',    # Options: 'fail', 'replace', 'append'
    index=False             # Don't write DataFrame index as a column
)

# ── 3. UNIVARIATE ANALYSIS ────────────────────────────────────

# 3a. Rating distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['rate'].dropna(), bins=20, kde=True, color='coral')
plt.title('Distribution of Restaurant Ratings')
plt.xlabel('Rating')
plt.tight_layout()
plt.show()

# 3b. Cost distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['cost'].dropna(), bins=30, kde=True, color='steelblue')
plt.title('Distribution of Approx Cost for Two')
plt.xlabel('Cost (INR)')
plt.tight_layout()
plt.show()

# 3c. Online order vs Book table counts
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
df['online_order'].value_counts().plot(kind='bar', ax=axes[0], color=['#2ecc71','#e74c3c'])
axes[0].set_title('Online Order Availability')
df['book_table'].value_counts().plot(kind='bar', ax=axes[1], color=['#3498db','#e67e22'])
axes[1].set_title('Table Booking Availability')
plt.tight_layout()
plt.show()

# ── 4. BIVARIATE ANALYSIS ─────────────────────────────────────

# 4a. Online order vs Average Rating
plt.figure(figsize=(6, 4))
sns.boxplot(x='online_order', y='rate', data=df, palette='Set2')
plt.title('Online Order vs Rating')
plt.tight_layout()
plt.show()

# 4b. Book table vs Average Rating
plt.figure(figsize=(6, 4))
sns.boxplot(x='book_table', y='rate', data=df, palette='Set3')
plt.title('Table Booking vs Rating')
plt.tight_layout()
plt.show()

# 4c. Cost vs Rating scatter
plt.figure(figsize=(7, 4))
sns.scatterplot(x='cost', y='rate', data=df, alpha=0.4, color='purple')
plt.title('Cost vs Rating')
plt.tight_layout()
plt.show()

# ── 5. TOP ANALYSIS ───────────────────────────────────────────

# 5a. Top 10 locations by restaurant count
plt.figure(figsize=(10, 5))
df['location'].value_counts().head(10).plot(kind='bar', color='teal')
plt.title('Top 10 Locations by Number of Restaurants')
plt.xlabel('Location')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5b. Top 10 restaurant types
plt.figure(figsize=(10, 5))
df['rest_type'].value_counts().head(10).plot(kind='bar', color='salmon')
plt.title('Top 10 Restaurant Types')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5c. Top 10 cuisines
cuisine_series = df['cuisines'].dropna().str.split(',').explode().str.strip()
plt.figure(figsize=(10, 5))
cuisine_series.value_counts().head(10).plot(kind='bar', color='orchid')
plt.title('Top 10 Cuisines in Bangalore')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ── 6. LOCATION-WISE AVERAGE RATING ──────────────────────────
plt.figure(figsize=(12, 5))
loc_rating = df.groupby('location')['rate'].mean().sort_values(ascending=False).head(15)
loc_rating.plot(kind='bar', color='dodgerblue')
plt.title('Top 15 Locations by Average Rating')
plt.ylabel('Avg Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ── 7. HEATMAP — Location vs Listed Type ─────────────────────
pivot = df.groupby(['location', 'listed_type']).size().unstack(fill_value=0)
top_locations = df['location'].value_counts().head(10).index
plt.figure(figsize=(12, 6))
sns.heatmap(pivot.loc[top_locations], annot=True, fmt='d', cmap='YlOrRd')
plt.title('Restaurant Type Distribution Across Top 10 Locations')
plt.tight_layout()
plt.show()

# ── 8. CORRELATION HEATMAP ────────────────────────────────────
plt.figure(figsize=(6, 4))
sns.heatmap(df[['rate', 'votes', 'cost']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation: Rate, Votes, Cost')
plt.tight_layout()
plt.show()

print("\n── Summary Stats ──")
print(df[['rate', 'votes', 'cost']].describe())