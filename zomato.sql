-- Create table
CREATE TABLE zomato (
    url            TEXT,
    address        TEXT,
    name           TEXT,
    online_order   VARCHAR(3),
    book_table     VARCHAR(3),
    rate           NUMERIC(3,1),
    votes          INT,
    phone          TEXT,
    location       TEXT,
    rest_type      TEXT,
    dish_liked     TEXT,
    cuisines       TEXT,
    cost           INT,
    reviews_list   TEXT,
    menu_item      TEXT,
    listed_type    TEXT,
    listed_city    TEXT
);
SELECT * FROM zomato

-- Q1: Top 10 locations with most restaurants
SELECT location, COUNT(*) AS total_restaurants
FROM zomato
GROUP BY location
ORDER BY total_restaurants DESC
LIMIT 10;

-- Q2: Average rating by online order availability
SELECT online_order,
       ROUND(AVG(rate)::NUMERIC, 2) AS avg_rating
FROM zomato
WHERE rate IS NOT NULL
GROUP BY online_order;

-- Q3: Top 10 highest voted restaurants
SELECT name, location, votes, rate
FROM zomato
ORDER BY votes DESC
LIMIT 10;

-- Q4: Average cost and rating by restaurant type
SELECT rest_type,
       ROUND(AVG(cost)::NUMERIC, 0)  AS avg_cost,
       ROUND(AVG(rate)::NUMERIC, 2)  AS avg_rating,
       COUNT(*)                      AS total
FROM zomato
WHERE cost IS NOT NULL AND rate IS NOT NULL
GROUP BY rest_type
ORDER BY avg_rating DESC
LIMIT 10;

-- Q5: Restaurants that accept both online order and table booking
SELECT name, location, rate, votes, cost
FROM zomato
WHERE online_order = 'Yes' AND book_table = 'Yes'
ORDER BY rate DESC
LIMIT 10;

-- Q6: Most common cuisines
SELECT TRIM(cuisine_name) AS cuisine, COUNT(*) AS count
FROM zomato,
     LATERAL UNNEST(STRING_TO_ARRAY(cuisines, ',')) AS cuisine_name
GROUP BY cuisine
ORDER BY count DESC
LIMIT 10;

-- Q7: Location-wise average cost for two
SELECT location,
       ROUND(AVG(cost)::NUMERIC, 0) AS avg_cost,
       COUNT(*)                     AS restaurants
FROM zomato
WHERE cost IS NOT NULL
GROUP BY location
ORDER BY avg_cost DESC
LIMIT 10;

-- Q8: Rating distribution buckets
SELECT
    CASE
        WHEN rate < 3.0 THEN 'Poor (<3)'
        WHEN rate < 3.5 THEN 'Average (3–3.5)'
        WHEN rate < 4.0 THEN 'Good (3.5–4)'
        WHEN rate < 4.5 THEN 'Very Good (4–4.5)'
        ELSE 'Excellent (4.5+)'
    END AS rating_bucket,
    COUNT(*) AS count
FROM zomato
WHERE rate IS NOT NULL
GROUP BY rating_bucket
ORDER BY count DESC;