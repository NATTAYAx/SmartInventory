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
cursor.execute("DELETE FROM sales_history WHERE sale_date < CURDATE() - INTERVAL 366 DAY;")
cursor.execute("DELETE FROM transactions WHERE sale_date < CURDATE() - INTERVAL 366 DAY;")
conn.commit()
print("⚠️ Old sales and transactions data cleared for new insertion.")

# Fetch all product IDs with stock details
cursor.execute("""
    SELECT p.id, p.name, p.price, p.stock, p.avg_sales_per_day, p.brand_name, 
           p.min_stock, p.max_stock, p.initial_stock, c.main_category, c.sub_category
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
""")
products = cursor.fetchall()


# **📌 Define Holiday Sales Multipliers**
holiday_sales_boost = {
    "01-01": {"category": ["Snacks", "Beverages", "Party Supplies"], "multiplier": 1.5},  # New Year
    "02-14": {"category": ["Chocolate", "Flowers", "Gift Items"], "multiplier": 2.0},  # Valentine's Day
    "04-13": {"category": ["Beverages", "Water", "Sun Protection"], "multiplier": 1.8},  # Songkran
    "11-xx": {"category": ["Candles", "Decorations", "Traditional Snacks"], "multiplier": 1.7},  # Loy Krathong
    "12-25": {"category": ["Chocolate", "Gift Items", "Decorations"], "multiplier": 1.6}   # Christmas
}

# **📌 Define Stocking Frequency**
def replenish_stock():
    print("🔄 Checking stock levels for replenishment...")
    
    # ✅ Fetch the latest stock values directly from the database
    cursor.execute("""
        SELECT id, name, stock, min_stock, max_stock FROM products
    """)
    products_stock = cursor.fetchall()
    
    for product in products_stock:
        product_id, name, stock, min_stock, max_stock = product
        
        # ✅ Determine the restock threshold
        restock_threshold = min_stock  # Default threshold
        
        # ✅ Check if replenishment is needed
        if stock == 0 or stock <= restock_threshold:
            restock_amount = max_stock  # **Restock to max_stock**
            
            cursor.execute("""
                UPDATE products 
                SET stock = %s 
                WHERE id = %s
            """, (max_stock, product_id))  # ✅ Directly update stock to `max_stock`
            
            print(f"🛒 Restocked {name} (ID: {product_id}) to {max_stock} units.")

    conn.commit()
    print("✅ Stock replenishment completed.")

# Generate sales history for the last 30 days
current_date = datetime.today()
start_date = current_date - timedelta(days=30)

sales_data = []
transactions_data = []

def get_holiday_multiplier(date):
    formatted_date = date.strftime('%m-%d')
    if formatted_date in holiday_sales_boost:
        return holiday_sales_boost[formatted_date]
    if date.strftime('%m') == '11':  # Loy Krathong is full moon in November
        return holiday_sales_boost.get("11-xx", None)
    return None

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

    if day in bad_weather_days:
        daily_sales_target = int(daily_sales_target * random.uniform(0.7, 0.9))  # Reduce sales due to bad weather
    elif day in special_event_days:
        daily_sales_target = int(daily_sales_target * random.uniform(1.2, 1.5))  # Boost sales on special events
    elif day in low_sales_days:
        daily_sales_target = int(daily_sales_target * random.uniform(0.8, 0.95))  # Slightly lower sales
        
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
            product_id, name, price, stock, avg_sales_per_day, brand_name, min_stock, max_stock, initial_stock, main_category, sub_category = product
            quantity_sold = random.randint(1, 5)
            
            if stock < quantity_sold:  # Ensure we don't sell more than available stock
                quantity_sold = stock  # Sell only what's left
                
            total_price = quantity_sold * float(price)
            total_transaction_price += total_price
            total_quantity += quantity_sold

            sales_records.append((product_id, quantity_sold, total_price, transaction_time.strftime('%Y-%m-%d %H:%M:%S')))

            # ✅ **Reduce Stock After Sale**
            cursor.execute("""
                UPDATE products 
                SET stock = GREATEST(stock - %s, 0) 
                WHERE id = %s
            """, (quantity_sold, product_id))

            # ✅ **Debugging: Check stock after sale**
            cursor.execute("SELECT stock FROM products WHERE id = %s", (product_id,))
            new_stock = cursor.fetchone()[0]
            print(f"📉 Sold {quantity_sold} of {name} (ID: {product_id}) - New stock: {new_stock}")


        # Insert the transaction into `transactions` table
        cursor.execute("""
            INSERT INTO transactions (sale_date, total_price, total_quantity)
            VALUES (%s, %s, %s)
        """, (transaction_time.strftime('%Y-%m-%d %H:%M:%S'), total_transaction_price, total_quantity))

        conn.commit()  # ✅ **Commit the stock update**
        transaction_id = cursor.lastrowid  # Get the last inserted transaction ID

        # Add transaction ID to sales data
        for sale in sales_records:
            sales_data.append((*sale, transaction_id))

        total_sales += num_products_in_transaction
        
    replenish_stock()

print("📌 Sample sales data to be inserted:", sales_data[:5])  # Show first 5 records
# **📌 Batch insert into sales_history**
if sales_data:
    cursor.executemany("""
        INSERT INTO sales_history (product_id, quantity_sold, total_price, sale_date, transaction_id)
        VALUES (%s, %s, %s, %s, %s)
    """, sales_data)

    conn.commit()
    print("✅ Sales history inserted successfully!")

conn.commit()
cursor.close()
conn.close()
print("✅ Sales history updated with transaction grouping and correct handling for Feb 9!")
