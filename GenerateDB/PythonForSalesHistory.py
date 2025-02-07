import mysql.connector
import random
from collections import Counter
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

# **📌 Clear old sales before inserting new ones**
cursor.execute("DELETE FROM sales_history WHERE sale_date >= CURDATE() - INTERVAL 30 DAY")
conn.commit()
print("⚠️ Old sales data cleared for new insertion.")

# Fetch all product IDs
cursor.execute("SELECT id, price FROM products")
products = cursor.fetchall()

# Generate sales history for the last 30 days
current_date = datetime.today()
start_date = current_date - timedelta(days=30)

sales_data = []

# Define special event days
special_event_days = random.sample(range(30), 4)
bad_weather_days = random.sample(range(30), 2)
low_sales_days = random.sample(range(30), 3)

for day in range(31):  # Include Feb 8 and Feb 9
    sale_date = start_date + timedelta(days=day)
    weekday = sale_date.weekday()  # 0 = Monday, 6 = Sunday

    print(f"📅 Processing {sale_date.strftime('%Y-%m-%d')} (Weekday: {weekday})")

    # **📌 Simulating "Store Opening" Growth**
    if day == 0:
        daily_sales_target = random.randint(20, 50)
    elif day == 1:
        daily_sales_target = random.randint(50, 150)
    elif day == 2:
        daily_sales_target = random.randint(100, 250)
    elif day == 3:
        daily_sales_target = random.randint(150, 300)
    elif day == 4:
        daily_sales_target = random.randint(200, 400)
    elif day < 7:
        daily_sales_target = random.randint(300, 600)
    else:
        daily_sales_target = random.randint(500, 1200)

    # **📌 Ensure No Day Drops Below 100 After Day 3**
    if day >= 3:
        daily_sales_target = max(daily_sales_target, 100)

    # **📌 Ensure Any Weekend After Week 1 Has 900+ Sales**
    if day >= 7 and weekday == 5:  # Saturday
        print(f"🔴 Boosting Saturday {sale_date.strftime('%Y-%m-%d')} to at least 900 sales.")
        daily_sales_target = max(daily_sales_target, 900)
    elif day >= 7 and weekday == 6:  # Sunday
        print(f"🔴 Boosting Sunday {sale_date.strftime('%Y-%m-%d')} to at least 900 sales.")
        daily_sales_target = max(daily_sales_target, 900)

    # **📌 Reduce Monday Sales (10-20% lower than Sunday)**
    if weekday == 0 and day >= 7:
        daily_sales_target = int(daily_sales_target * random.uniform(0.9, 0.95))

    if weekday == 1:  # Tuesday (Slight adjustment)
        daily_sales_target = int(daily_sales_target * random.uniform(0.9, 1.0))
    
    if weekday == 3:  # Thursday
        daily_sales_target = int(daily_sales_target * random.uniform(0.9, 0.95))

    if weekday == 4:  # Thursday (Slight boost)
        daily_sales_target = int(daily_sales_target * random.uniform(1.05, 1.2))
    if weekday == 5:  # Friday (Slight boost)
        daily_sales_target = int(daily_sales_target * random.uniform(1.1, 1.2))
    
    # **📌 Thursdays & Fridays Slight Boost (5-15%)**
    if weekday in [3, 4]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.05, 1.15))
    
    # **📌 Payday Spikes (1st & 16th), Gradual Drop-off**
    if sale_date.day in [1, 16]:
        daily_sales_target *= random.uniform(1.2, 1.5)  # Big boost
    elif sale_date.day in [2, 3, 17, 18]:  # Gradual drop-off
        daily_sales_target *= random.uniform(1.1, 1.3)

    # **📌 Holiday Adjustments (e.g., Valentine's Day)**
    if sale_date.strftime('%Y-%m-%d') == "2025-02-14":
        daily_sales_target = int(daily_sales_target * random.uniform(1.2, 1.5))  # Special boost for snacks, gifts

    total_sales = 0

    while total_sales < daily_sales_target:
        for hour in range(24):
            if total_sales >= daily_sales_target:
                break

            # **📌 Adjust Hourly Sales Based on Product Types**
            sales_multiplier = 0.05  # Default low sales
            if 6 <= hour < 10:  # Morning (Breakfast, coffee)
                sales_multiplier = 0.25
            elif 11 <= hour < 14:  # Lunch break (Snacks, ready-to-eat)
                sales_multiplier = 0.5
            elif 16 <= hour < 20:  # Evening (Groceries, essentials)
                sales_multiplier = 0.8
            elif 21 <= hour < 23:  # Late night (Snacks, energy drinks)
                sales_multiplier = 0.3

            # **📌 Simulate stock shortages (~5% chance per day)**
            if random.random() < 0.05:
                continue

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

# **📌 FINAL ENFORCEMENT FOR FEB 9 (Ensure gradual increase)**
final_sales_count = sum(1 for sale in sales_data if sale[3].startswith('2025-02-09'))

# ✅ Use past 5 days' average to calculate Feb 9 sales
daily_sales_counts = Counter(sale[3][:10] for sale in sales_data)
last_5_days = list(daily_sales_counts.values())[-5:]

if last_5_days:
    avg_recent_sales = sum(last_5_days) / len(last_5_days)
    feb9_target = int(avg_recent_sales * random.uniform(1.1, 1.3))  # 10-30% increase
else:
    feb9_target = random.randint(900, 2000)  # Fallback if no prior data

if final_sales_count < feb9_target:
    missing_sales = feb9_target - final_sales_count
    print(f"⚠️ Enforcing extra {missing_sales} sales for Feb 9 (Target: {feb9_target})")

    for _ in range(missing_sales):
        product = random.choice(products)
        product_id, price = product
        quantity_sold = random.randint(1, 5)
        total_price = quantity_sold * float(price)

        random_hour = random.randint(6, 22)  # Favor peak hours
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        final_sale_date = datetime.strptime('2025-02-09', "%Y-%m-%d") + timedelta(
            hours=random_hour, minutes=random_minute, seconds=random_second
        )

        sales_data.append((product_id, quantity_sold, total_price, final_sale_date.strftime('%Y-%m-%d %H:%M:%S')))

# **📌 Batch insert for better performance**
cursor.executemany("""
    INSERT INTO sales_history (product_id, quantity_sold, total_price, sale_date)
    VALUES (%s, %s, %s, %s)
""", sales_data)

conn.commit()
cursor.close()
conn.close()
print("✅ Sales history updated with final refinements!")
