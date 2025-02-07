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

# Special event days - set on weekends, Fridays, or paydays (1st & 15th)
special_event_days = [day for day in range(30) if day % 15 == 0 or (start_date + timedelta(days=day)).weekday() in [4, 5, 6]]
special_event_days = random.sample(special_event_days, 3)  # Pick 3 days

for day in range(30):  
    sale_date = start_date + timedelta(days=day)  
    weekday = sale_date.weekday()  # 0 = Monday, 6 = Sunday
    
    # **📌 Smoother Growth for First 14 Days**
    if day < 7:
        daily_sales_target = random.randint(50 + (day * 30), 250 + (day * 40))  # Slow increase
    elif day < 14:
        daily_sales_target = random.randint(300 + (day * 20), 500 + (day * 30))  # More gradual
    else:
        daily_sales_target = random.randint(500, 1200)  # Normal range for stable store

    # **📌 Weekend Boost (More Stable)**
    if weekday in [5, 6]:  # Saturday, Sunday (higher sales)
        daily_sales_target = min(int(daily_sales_target * 1.2), 1500)  
    elif weekday == 0:  # Monday (slightly lower sales)
        daily_sales_target = max(int(daily_sales_target * 0.85), 500)
    elif weekday == 2:  # Tuesday (prevent dips)
        daily_sales_target = max(int(daily_sales_target * 1.05), 550)
    elif weekday == 4:  # Friday (higher, but not extreme)
        daily_sales_target = min(int(daily_sales_target * 1.1), 1400)

    # **📌 Special Event Boost (Logical Placement)**
    if day in special_event_days:
        daily_sales_target = min(int(daily_sales_target * 1.3), 1500)  

    total_sales = 0  

    while total_sales < daily_sales_target:
        for hour in range(24):
            if total_sales >= daily_sales_target:
                break  
            
            # **📌 Adjust Hourly Sales Patterns**
            if 6 <= hour < 10:   # Morning (low)
                sales_multiplier = 0.3
            elif 11 <= hour < 15: # Lunch & afternoon (moderate)
                sales_multiplier = 0.6
            elif 16 <= hour < 21: # Evening peak (high)
                sales_multiplier = 1.0
            elif 21 <= hour < 23: # Late-night shopping (low)
                sales_multiplier = 0.3
            else:                 # After 11 PM (almost no sales)
                sales_multiplier = 0.05

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
