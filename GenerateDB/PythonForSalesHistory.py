import mysql.connector
import random
from datetime import datetime, timedelta

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hawks2710Dante_",
    database="smart_inventory",
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

# Fetch all product IDs
cursor.execute("SELECT id, price FROM products")
products = cursor.fetchall()

# Generate sales history for the last 30 days
start_date = datetime.today() - timedelta(days=30)

sales_data = []

# Define special event days
special_event_days = random.sample(range(30), 4)  # Pick 4 random event days
bad_weather_days = random.sample(range(30), 3)  # Pick 3 random days with fewer sales

for day in range(30):  
    sale_date = start_date + timedelta(days=day)  
    weekday = sale_date.weekday()  # 0 = Monday, 6 = Sunday
    
    # **📌 Base sales target per day**
    if day < 7:
        daily_sales_target = random.randint(50 + (day * 30), 250 + (day * 40))  # Slow increase
    elif day < 14:
        daily_sales_target = random.randint(300 + (day * 20), 500 + (day * 30))  # More gradual
    else:
        daily_sales_target = random.randint(500, 1200)  # Normal range for stable store

    # **📌 Weekend Sales Boost**
    if weekday in [5, 6]:  # Saturday, Sunday
        daily_sales_target = min(int(daily_sales_target * random.uniform(1.1, 1.4)), 1500)

    # **📌 Monday Slight Drop**
    if weekday == 0:  
        daily_sales_target = max(int(daily_sales_target * random.uniform(0.8, 0.95)), 400)

    # **📌 Payday Spikes**
    if sale_date.day in [1, 16]:  # Payday on the 1st and 16th
        daily_sales_target = int(daily_sales_target * random.uniform(1.3, 1.6))

    # **📌 Special Event Days**
    if day in special_event_days:
        daily_sales_target = int(daily_sales_target * random.uniform(1.4, 1.8))  

    # **📌 Bad Weather Days (Reduce Sales by 30-50%)**
    if day in bad_weather_days:
        daily_sales_target = int(daily_sales_target * random.uniform(0.5, 0.7))

    # **📌 Random Bad Sales Days (~10% chance)**
    if random.random() < 0.1:
        daily_sales_target = int(daily_sales_target * random.uniform(0.5, 0.8))  

    total_sales = 0  

    while total_sales < daily_sales_target:
        for hour in range(24):
            if total_sales >= daily_sales_target:
                break  

            # **📌 Hourly Sales Distribution**
            if 6 <= hour < 10:   # Morning (low sales)
                sales_multiplier = 0.25
            elif 11 <= hour < 15: # Lunch & afternoon (moderate sales)
                sales_multiplier = 0.5
            elif 16 <= hour < 21: # Evening peak (high sales)
                sales_multiplier = 0.8
            elif 21 <= hour < 23: # Late-night shopping (very low)
                sales_multiplier = 0.2
            else:                 # After 11 PM (almost no sales)
                sales_multiplier = 0.05

            # **📌 Simulate stock shortages (~5% chance per day)**
            if random.random() < 0.05:
                continue  # Skip adding sales due to stockout

            if random.random() < sales_multiplier:
                product = random.choice(products)
                product_id, price = product
                
                quantity_sold = random.randint(1, 5)  
                total_price = quantity_sold * float(price)
                
                random_minute = random.randint(0, 59)
                random_second = random.randint(0, 59)
                final_sale_date = sale_date + timedelta(hours=hour, minutes=random_minute, seconds=random_second)
                
                sales_data.append((product_id, quantity_sold, total_price, final_sale_date.strftime('%Y-%m-%d %H:%M:%S')))
                total_sales += 1  

# **📌 Batch insert for better performance**
cursor.executemany("""
    INSERT INTO sales_history (product_id, quantity_sold, total_price, sale_date)
    VALUES (%s, %s, %s, %s)
""", sales_data)

conn.commit()  

# Close connection
cursor.close()
conn.close()
print("✅ Sales history has been adjusted & regenerated successfully.") 
