# ZOMATO-DATA-ANALYSIS

Project Setup, Column Guide, SQL Notes & Power BI Instructions
1. Project Overview
This project analyzes Zomato's restaurant listing data for Bangalore to uncover dining trends, location-based insights, cuisine popularity, and the impact of online ordering and table booking on customer ratings. The pipeline covers Python EDA, PostgreSQL querying, and Power BI dashboard design.

2. Dataset Information
File
zomato.csv  (Zomato Bangalore Restaurants)

Key Stats
Rows: ~51,717 restaurants   |   Columns: 17

Data Dictionary

Column	Renamed To	Type	Description
url	url	TEXT	Zomato listing URL
address	address	TEXT	Full address
name	name	TEXT	Restaurant name
online_order	online_order	VARCHAR	Yes / No
book_table	book_table	VARCHAR	Yes / No
rate	rate	NUMERIC	Rating /5 (cleaned from '4.1/5' format)
votes	votes	INT	Number of reviews
phone	phone	TEXT	Contact number
location	location	TEXT	Locality in Bangalore
rest_type	rest_type	TEXT	Restaurant format
dish_liked	dish_liked	TEXT	Popular dishes
cuisines	cuisines	TEXT	Comma-separated cuisines
approx_cost(for two people)	cost	INT	Cost for two (INR)
reviews_list	reviews_list	TEXT	Customer reviews
menu_item	menu_item	TEXT	Menu items
listed_in(type)	listed_type	TEXT	Buffet / Cafes / Delivery / etc.
listed_in(city)	listed_city	TEXT	City area

3. Project Structure
zomato-analysis/
   zomato.csv                      <- Raw dataset
   zomato_eda.py                   <- Python EDA & cleaning script
   zomato_sql_queries.sql          <- All PostgreSQL queries
   Zomato_Analysis_Report.docx     <- Full analysis report
   README.docx                     <- This file
   powerbi/
      Zomato_Dashboard.pbix        <- Power BI dashboard

4. Setup & Installation
Python Dependencies
pip install pandas numpy matplotlib seaborn sqlalchemy psycopg2-binary

Database Setup (PostgreSQL)
CREATE DATABASE zomato_db;
\c zomato_db
-- Then run CREATE TABLE from zomato_sql_queries.sql

Load CSV to PostgreSQL via Python
import pandas as pd
from sqlalchemy import create_engine
df = pd.read_csv('zomato.csv', encoding='latin-1')
engine = create_engine('postgresql://user:pass@localhost:5432/zomato_db')
df.to_sql('zomato', engine, if_exists='replace', index=False)

Run EDA
python zomato_eda.py

5. Data Cleaning Notes
•Rate column: strip '/5' suffix and convert to NUMERIC before inserting
•Cost column: remove commas (e.g. '1,000' -> 1000) and cast to INT
•Cuisines column: use UNNEST + STRING_TO_ARRAY in SQL for per-cuisine analysis
•Rename columns with special characters (parentheses) before loading to SQL
•Drop duplicate rows — some restaurants appear multiple times for different listing types

6. SQL Queries Covered

Query #	Question	Key Note
Q1	Top 10 locations by restaurant count	Basic GROUP BY + COUNT
Q2	Avg rating by online order availability	ROUND(AVG(rate)::NUMERIC, 2)
Q3	Top 10 highest voted restaurants	ORDER BY votes DESC
Q4	Avg cost and rating by restaurant type	ROUND(AVG(cost)::NUMERIC, 0)
Q5	Restaurants with both online order + book table	WHERE + AND filter
Q6	Top 10 cuisines (UNNEST split)	LATERAL UNNEST(STRING_TO_ARRAY(...))
Q7	Location-wise avg cost for two	ROUND(AVG(cost)::NUMERIC, 0)
Q8	Rating distribution buckets	CASE WHEN on rate

IMPORTANT — PostgreSQL ROUND() Fix:
Always cast float/double columns before ROUND: ROUND(AVG(rate)::NUMERIC, 2)

7. Power BI Dashboard
DAX Measures
Total Restaurants  = COUNTROWS(zomato)
Avg Rating         = AVERAGE(zomato[rate])
Avg Cost           = AVERAGE(zomato[cost])
Online Order %     = DIVIDE(COUNTROWS(FILTER(zomato,zomato[online_order]="Yes")),COUNTROWS(zomato))*100
Book Table %       = DIVIDE(COUNTROWS(FILTER(zomato,zomato[book_table]="Yes")),COUNTROWS(zomato))*100

Recommended Visuals

Visual	Columns	Insight
KPI Cards	Total Restaurants, Avg Rating, Avg Cost	Summary
Bar Chart	location + COUNT	Top areas by restaurants
Pie Chart	online_order	Online ordering adoption
Donut Chart	book_table	Table booking adoption
Bar Chart	cuisines (split) + COUNT	Top cuisines
Scatter Plot	cost vs rate	Price-quality relationship
Map Visual	location + COUNT	Geographic density
Bar Chart	rest_type + avg rate	Best rated formats
Bar Chart	name + votes (Top 10)	Most popular restaurants
Heatmap Matrix	location vs listed_type	Format distribution by area
Slicers	location, online_order, book_table, listed_type	Interactivity

8. Key Insights Summary
•BTM Layout, Indiranagar, and Koramangala are the top 3 restaurant-dense areas in Bangalore
•Restaurants with table booking score ~0.3 points higher on average than those without
•North Indian and Chinese are the two most common cuisine types across all areas
•Fine Dining format has the highest average rating (~4.2) followed by Casual Dining (~3.9)
•There is a weak positive correlation between price and rating
•Online ordering restaurants generate higher vote counts due to wider customer reach
•Premium localities (MG Road, Lavelle Road) command Rs. 900-1500+ avg cost for two

9. Notes & Limitations
•Dataset scraped from Zomato — may not reflect current restaurant status
•Some restaurants appear multiple times for different listing_type entries — deduplicate before counting
•Ratings distribution is right-skewed; most restaurants cluster between 3.5 and 4.2
•reviews_list column contains raw unstructured text — sentiment analysis is a future extension
•menu_item column is largely empty in many records — not suitable for menu analysis
