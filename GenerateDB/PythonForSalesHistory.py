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

# **📌 Clear old sales before inserting new ones**
cursor.execute("DELETE FROM sales_history WHERE sale_date BETWEEN '2025-01-09' AND '2025-02-09'")
conn.commit()
print("⚠️ Old sales data cleared for new insertion.")

# Fetch all product IDs
cursor.execute("SELECT id, price FROM products")
products = cursor.fetchall()

# Generate sales history for the last 30 days
start_date = datetime.today() - timedelta(days=30)

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

    # **📌 Handling Bad Weather Days (Lower Sales, But Not Dead)**
    if day in bad_weather_days:
        daily_sales_target = int(daily_sales_target * random.uniform(0.6, 0.8))
        daily_sales_target = max(daily_sales_target, 250)

    # **📌 Adding Some Random Slow Days (~3 Total)**
    if day in low_sales_days:
        daily_sales_target = int(daily_sales_target * random.uniform(0.7, 0.9))
        daily_sales_target = max(daily_sales_target, 200)

    # **📌 Prevent Monday from Being Too High**
    if weekday == 0 and day >= 7:
        daily_sales_target = min(daily_sales_target, int(sum([random.randint(600, 1200) for _ in range(5)]) / 5 * 1.5))

    # **📌 Thursdays & Fridays Slight Boost**
    if weekday in [3, 4]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.1, 1.2))

    # **📌 Payday Spikes (1st & 16th)**
    if sale_date.day in [1, 16]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.3, 1.6))

    total_sales = 0

    while total_sales < daily_sales_target:
        for hour in range(24):
            if total_sales >= daily_sales_target:
                break

            # **📌 Ensure Even Distribution of Sales**
            sales_multiplier = 0.05
            if 6 <= hour < 10:
                sales_multiplier = 0.25
            elif 11 <= hour < 15:
                sales_multiplier = 0.5
            elif 16 <= hour < 21:
                sales_multiplier = 0.8
            elif 21 <= hour < 23:
                sales_multiplier = 0.2

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

# **📌 FINAL ENFORCEMENT FOR FEB 9 (ENSURE IT STAYS 900+)**
final_sales_count = sum(1 for sale in sales_data if sale[3].startswith('2025-02-09'))
random_target_for_feb9 = random.randint(900, 2000)  # Set the target range

if final_sales_count < random_target_for_feb9:
    missing_sales = random_target_for_feb9 - final_sales_count
    print(f"⚠️ Enforcing extra {missing_sales} sales for Feb 9 (Target: {random_target_for_feb9})")

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

# Close connection
cursor.close()
conn.close()
print("✅ Sales history updated with final refinements!")
