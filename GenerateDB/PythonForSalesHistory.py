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
cursor.execute("DELETE FROM sales_history WHERE sale_date < CURDATE() - INTERVAL 90 DAY;")
cursor.execute("DELETE FROM transactions WHERE sale_date < CURDATE() - INTERVAL 90 DAY;")
conn.commit()
print("⚠️ Old sales and transactions data cleared for new insertion.")

# Fetch all product IDs
cursor.execute("SELECT id, price FROM products")
products = cursor.fetchall()

# Generate sales history for the last 30 days
current_date = datetime.today()
start_date = current_date - timedelta(days=30)

sales_data = []
transactions_data = []

# Define special event days
special_event_days = random.sample(range(30), 4)
bad_weather_days = random.sample(range(30), 2)
low_sales_days = random.sample(range(30), 3)

for day in range(31):  # Include Feb 8 and Feb 9
    sale_date = start_date + timedelta(days=day)
    weekday = sale_date.weekday()  # 0 = Monday, 6 = Sunday

    print(f"📅 Processing {sale_date.strftime('%Y-%m-%d')} (Weekday: {weekday})")

    # **📌 Existing Logic for Daily Sales Target**
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

    if day >= 3:
        daily_sales_target = max(daily_sales_target, 100)

    if day >= 7 and weekday == 5:
        print(f"🔴 Boosting Saturday {sale_date.strftime('%Y-%m-%d')} to at least 900 sales.")
        daily_sales_target = max(daily_sales_target, 900)
    elif day >= 7 and weekday == 6:
        print(f"🔴 Boosting Sunday {sale_date.strftime('%Y-%m-%d')} to at least 900 sales.")
        daily_sales_target = max(daily_sales_target, 900)

    if weekday == 0 and day >= 7:
        daily_sales_target = int(daily_sales_target * random.uniform(0.9, 0.95))

    if weekday in [3, 4]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.05, 1.15))

    if sale_date.day in [1, 16]:
        daily_sales_target *= random.uniform(1.2, 1.5)

    total_sales = 0

    while total_sales < daily_sales_target:
        num_products_in_transaction = random.randint(1, 5)  # 1 to 5 products per transaction
        transaction_time = sale_date + timedelta(
            hours=random.randint(6, 22), minutes=random.randint(0, 59), seconds=random.randint(0, 59)
        )

        transaction_products = random.sample(products, num_products_in_transaction)
        total_transaction_price = 0
        total_quantity = 0  # Track total items in transaction

        sales_records = []  # Temporary storage for sales to be linked to the transaction

        for product in transaction_products:
            product_id, price = product
            quantity_sold = random.randint(1, 5)
            total_price = quantity_sold * float(price)
            total_transaction_price += total_price
            total_quantity += quantity_sold

            sales_records.append((product_id, quantity_sold, total_price, transaction_time.strftime('%Y-%m-%d %H:%M:%S')))

        # Insert the transaction into `transactions` table
        cursor.execute("""
            INSERT INTO transactions (sale_date, total_price, total_quantity)
            VALUES (%s, %s, %s)
        """, (transaction_time.strftime('%Y-%m-%d %H:%M:%S'), total_transaction_price, total_quantity))

        conn.commit()  # Commit to generate auto-increment ID
        transaction_id = cursor.lastrowid  # Get the last inserted transaction ID

        # Add transaction ID to sales data
        for sale in sales_records:
            sales_data.append((*sale, transaction_id))

        total_sales += num_products_in_transaction
        

# **📌 FINAL ENFORCEMENT FOR FEB 9 (Ensure gradual increase)**
final_sales_count = sum(1 for sale in sales_data if sale[3].startswith('2025-02-09'))

daily_sales_counts = Counter(sale[3][:10] for sale in sales_data)
last_5_days = list(daily_sales_counts.values())[-5:]

if last_5_days:
    avg_recent_sales = sum(last_5_days) / len(last_5_days)
    feb9_target = int(avg_recent_sales * random.uniform(1.1, 1.3))  # 10-30% increase
else:
    feb9_target = random.randint(900, 2000)

if final_sales_count < feb9_target:
    missing_sales = feb9_target - final_sales_count
    print(f"⚠️ Enforcing extra {missing_sales} sales for Feb 9 (Target: {feb9_target})")

    for _ in range(missing_sales):
        product = random.choice(products)
        product_id, price = product
        quantity_sold = random.randint(1, 5)
        total_price = quantity_sold * float(price)

        final_sale_date = datetime.strptime('2025-02-09', "%Y-%m-%d") + timedelta(
            hours=random.randint(6, 22), minutes=random.randint(0, 59), seconds=random.randint(0, 59)
        )

        # Insert missing transaction
        cursor.execute("""
            INSERT INTO transactions (sale_date, total_price, total_quantity)
            VALUES (%s, %s, %s)
        """, (final_sale_date.strftime('%Y-%m-%d %H:%M:%S'), total_price, quantity_sold))

        conn.commit()
        transaction_id = cursor.lastrowid  # Get new transaction ID

        sales_data.append((product_id, quantity_sold, total_price, final_sale_date.strftime('%Y-%m-%d %H:%M:%S'), transaction_id))

# **📌 Batch insert into sales_history**
cursor.executemany("""
    INSERT INTO sales_history (product_id, quantity_sold, total_price, sale_date, transaction_id)
    VALUES (%s, %s, %s, %s, %s)
""", sales_data)

conn.commit()
cursor.close()
conn.close()
print("✅ Sales history updated with transaction grouping and correct handling for Feb 9!")
