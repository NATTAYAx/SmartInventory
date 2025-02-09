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

# **📌 Determine Start Date for the New Sales Data**
cursor.execute("SELECT MAX(sale_date) FROM sales_history;")
last_sale_date = cursor.fetchone()[0]

if last_sale_date:
    start_date = last_sale_date + timedelta(days=1)  # Start from the next day after the last sale
else:
    start_date = datetime.today() - timedelta(days=30)  # Default: Start from 30 days ago

end_date = start_date + timedelta(days=30)  # Extend by one more month

print(f"📆 Generating sales data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

# **📌 Fetch All Active Products (Excluding Discontinued)**
cursor.execute("""
    SELECT p.id, p.name, p.price, p.stock, p.avg_sales_per_day, p.brand_name, 
           p.min_stock, p.max_stock, p.initial_stock, c.main_category, c.sub_category
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.id
    WHERE p.is_discontinued = FALSE
""")
products = cursor.fetchall()

# ✅ **Define Restock Frequency & Lead Time Per Category**
RESTOCK_CYCLE = {
    "Dairy": 1,           # Daily restock (next day)
    "Meat": 1,            # Daily restock (next day)
    "Vegetables": 1,      # Daily restock (next day)
    "Water": 2,           # Every 2 days
    "Beverages": 5,       # Weekly (3-7 days variation)
    "Snacks": 5,          # Weekly (3-7 days variation)
    "Instant Noodles": 7, # Weekly (4-7 days variation)
    "Medicine": 10,       # Bi-weekly (7-12 days variation)
    "Household": 12,      # Bi-weekly (8-14 days variation)
    "Electronics": 15,    # Monthly (10-15 days variation)
    "Beauty": 10,         # Bi-weekly (7-12 days variation)
    "Personal Care": 10   # Bi-weekly (7-12 days variation)
}

# ✅ **Minimum Order Quantities (MOQ)**
MOQ = {
    "Fresh Food": 20, "Dairy": 20, "Vegetables": 30, "Meat": 40,
    "Beverages": 12, "Snacks": 12, "Instant Noodles": 24,
    "Medicine": 5, "Household": 6, "Electronics": 3,
    "Beauty": 5, "Personal Care": 12
}

# ✅ **Pending Restock Orders Dictionary**
pending_restocks = {}

# ✅ **Rare Events for Long-Term Shortages**
LONG_TERM_SHORTAGE_PROBABILITY = 0.0005  # chance a product will not restock for months
GLOBAL_SUPPLY_CRISIS_PROBABILITY = 0.000001  # chance a product is removed permanently

long_term_shortages = {}
# ✅ High-priority categories that should trigger emergency restocks
CRITICAL_CATEGORIES = {"Dairy", "Meat", "Vegetables", "Water", "Medicine", "Personal Care", "Household"}
last_emergency_restock = {}

# **📌 Define Holiday Sales Multipliers**
holiday_sales_boost = {
    "01-01": {"category": ["Snacks", "Beverages", "Party Supplies"], "multiplier": 1.5},  # New Year
    "02-14": {"category": ["Chocolate", "Flowers", "Gift Items"], "multiplier": 2.0},  # Valentine's Day
    "04-13": {"category": ["Beverages", "Water", "Sun Protection"], "multiplier": 1.8},  # Songkran
    "11-xx": {"category": ["Candles", "Decorations", "Traditional Snacks"], "multiplier": 1.7},  # Loy Krathong
    "12-25": {"category": ["Chocolate", "Gift Items", "Decorations"], "multiplier": 1.6}   # Christmas
}

def check_for_long_term_shortages(product_id, category, current_date):
    """Randomly applies long-term shortages to make the simulation realistic."""
    global long_term_shortages
    products_dict = {p[0]: p for p in products}
    ESSENTIAL_CATEGORIES = {"Dairy", "Meat", "Vegetables", "Water", "Rice"}

    # Get number of existing shortages
    current_shortages = len(long_term_shortages)

    # Set a limit for shortages (5% normal, 10% during crisis)
    crisis_mode = random.random() < 0.03  # 3% chance of a supply crisis
    max_shortages = int(len(products) * (0.10 if crisis_mode else 0.05))

    if current_shortages >= max_shortages:
        return False  # Don't allow new shortages

    # Limit shortages per category (2 normally, 4 in crisis)
    category_shortages = sum(1 for p in long_term_shortages if products_dict.get(p, ["Unknown"] * 10)[9] == category)
    max_category_shortages = 4 if crisis_mode else 2

    if category_shortages >= max_category_shortages:
        return False  # Don't add more shortages in this category

    # Reduce shortage probability for essential items
    if category in ESSENTIAL_CATEGORIES and random.random() > 0.02:
        return False  # Skip shortage for essentials

    shortage_probability = LONG_TERM_SHORTAGE_PROBABILITY * (0.5 if category in ESSENTIAL_CATEGORIES else 1.0)

    if random.random() < shortage_probability:
        shortage_duration = random.randint(30, 90)  # Lasts 1-3 months
        shortage_end_date = current_date + timedelta(days=shortage_duration)
        long_term_shortages[product_id] = shortage_end_date

        print(f"⚠️ {product_id} ({category}) is now in a long-term shortage until {shortage_end_date.strftime('%Y-%m-%d')} (Crisis Mode: {crisis_mode})")
        return True  

    return False

# **📌 Realistic Daily Sales Target Function**
def get_daily_sales_target(day, sale_date, weekday):
    """Dynamically determines daily sales with realistic peaks, dips, and events."""

    # 📌 Gradual Growth in First Month
    if day == 0:
        daily_sales_target = random.randint(150, 250)
    elif day == 1:
        daily_sales_target = random.randint(250, 350)
    elif day == 2:
        daily_sales_target = random.randint(350, 500)
    elif day == 3:
        daily_sales_target = random.randint(450, 700)
    elif day == 4:
        daily_sales_target = random.randint(600, 800)
    elif day < 7:
        daily_sales_target = random.randint(700, 1100)
    else:
        daily_sales_target = random.randint(900, 1300)  # Normal range

    # 📌 Weekend Boost (Sat-Sun)
    if weekday in [5, 6]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.15, 1.3))  # +15% to +30%

    # 📌 Monday Drop (After Weekend)
    if weekday == 0:
        daily_sales_target = int(daily_sales_target * random.uniform(0.8, 0.95))  # -5% to -20%

    if weekday == 5:  # Saturday
        daily_sales_target = int(daily_sales_target * random.uniform(1.2, 1.4))  # Strongest day
    elif weekday == 6:  # Sunday
        daily_sales_target = int(daily_sales_target * random.uniform(1.15, 1.3))  # Slightly lower than Sat
    elif weekday == 4:  # Friday (People shopping for weekend)
        daily_sales_target = int(daily_sales_target * random.uniform(1.05, 1.15))  


    # 📌 Pre-Weekend Boost (Thursday & Friday)
    if weekday in [3, 4]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.05, 1.15))  # +5% to +15%

    # 📌 Payday Boost (1st & 16th of Every Month)
    if sale_date.day in [1, 16]:
        daily_sales_target = int(daily_sales_target * random.uniform(1.3, 1.6))  # +30% to +60%

    # 📌 Super High-Sales Day (Once Every 40 Days, NOT Near Payday)
    if day % 40 == 0 and sale_date.day not in [1, 16]:
        daily_sales_target = int(daily_sales_target * random.uniform(2.5, 3.5))  # +150% to +250%
        print(f"🚀 SUPER SALES DAY on {sale_date.strftime('%Y-%m-%d')}! Huge spike!")

    # 🚀 After a Super Sales Day, next 1-2 days should drop slightly
    if day > 0 and sales_data[-1][1] > 1800:  # If previous day had super high sales
        daily_sales_target = int(daily_sales_target * random.uniform(0.8, 0.95))  # Reduce by 5-20%
        print(f"⬇️ POST-HIGH SALES DAY on {sale_date.strftime('%Y-%m-%d')}, adjusting demand down slightly.")
        
    # 🔥 Unpredictable High Sales Day (~3% chance, but now linked to logical reasons)
    if random.random() < 0.03 and day % 7 != 0:
        reason = random.choice(["Local Event", "Hot Weather", "Flash Sale", "Panic Buying"])
        daily_sales_target = int(daily_sales_target * random.uniform(1.5, 2.5))  
        print(f"🚀 HIGH SALES DAY on {sale_date.strftime('%Y-%m-%d')} due to {reason}!")

    # 📌 Random Low-Sales Day (~8% chance, But Never Consecutive)
    if random.random() < 0.08 and day % 3 != 0:
        daily_sales_target = int(daily_sales_target * random.uniform(0.5, 0.8))  # -20% to -50%
        print(f"🔻 LOW SALES DAY on {sale_date.strftime('%Y-%m-%d')}! Sales dropped.")

    return max(200, int(daily_sales_target))  # Ensure sales never drop below 200

def apply_pending_restocks(current_date):
    """Applies any scheduled restocks that have arrived at the store before sales processing."""
    if current_date in pending_restocks:
        print(f"📦 Applying restocks scheduled for {current_date.strftime('%Y-%m-%d')}...")

        for product_id, restock_amount in pending_restocks[current_date]:
            # Update stock immediately in the database
            cursor.execute(
                "UPDATE products SET stock = stock + %s WHERE id = %s",
                (restock_amount, product_id)
            )
            print(f"✅ Restocked {restock_amount} units for product ID {product_id}")

        conn.commit()  # Save changes
        del pending_restocks[current_date]  # Remove processed restocks
        
# **📌 Restocking Function**

def replenish_stock(current_date):
    print(f"🔄 Checking stock levels for {current_date.strftime('%Y-%m-%d')}")

    # ✅ Fetch sales trends from the last 30 days
    cursor.execute("""
        SELECT p.id, 
            COALESCE(SUM(s.quantity_sold) / 30, 0) AS avg_daily_sales
        FROM products p
        LEFT JOIN sales_history s ON p.id = s.product_id
        GROUP BY p.id
    """)
    product_sales_data = {row[0]: float(row[1]) for row in cursor.fetchall()}

    # ✅ Fetch product stock details
    cursor.execute("""
        SELECT p.id, p.name, p.stock, p.min_stock, p.max_stock, c.main_category 
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
    """)
    products_stock = cursor.fetchall()

    for product_id, name, stock, min_stock, max_stock, category in products_stock:
        avg_daily_sales = product_sales_data.get(product_id, 0)

        # ✅ **Set Restock Timing Based on Demand**
        if avg_daily_sales > 10:
            restock_days = 3  # High-demand products restock every 3 days
        elif avg_daily_sales > 5:
            restock_days = 5  # Medium-demand products restock every 5 days
        else:
            restock_days = RESTOCK_CYCLE.get(category, 10)  # Default category cycle

        # ✅ **Set max_safe_stock to prevent overstocking**
        max_safe_stock = avg_daily_sales * 10  # Ensure only 10 days' worth of stock
        max_safe_stock = min(max_safe_stock, max_stock)  # Cap at product's max_stock limit

        # ✅ **If stock exceeds safe limit, skip restocking**
        if stock > max_safe_stock:
            print(f"🚫 Skipping restock for {name} (ID: {product_id}) - Overstocked (Stock: {stock}, Safe Max: {max_safe_stock})")
            continue  # Skip this product

        # ✅ **If stock is 0 but high demand, prioritize restock**
        if stock == 0 and avg_daily_sales > 10:
            restock_days = 1  # Urgent next-day restock

        # ✅ **Random Variation to Simulate Real Supply Chain Delays**
        lead_time = random.randint(restock_days - 1, restock_days + 2)
        lead_time = max(1, lead_time)  # Ensure at least 1-day lead time

        # ✅ **Calculate Restock Amount with Integer Precision**
        base_restock = max(avg_daily_sales * 7, MOQ.get(category, 10))  # Ensure 7+ days' worth of stock
        restock_amount = int(round(min(base_restock, max_safe_stock - stock)))  # Convert to integer to avoid float precision issues

        # ✅ **Schedule Restock**
        arrival_date = current_date + timedelta(days=lead_time)
        if arrival_date not in pending_restocks:
            pending_restocks[arrival_date] = []
        pending_restocks[arrival_date].append((product_id, int(restock_amount)))

        print(f"📦 {restock_amount} units of {name} (ID: {product_id}) scheduled - Arriving on {arrival_date.strftime('%Y-%m-%d')}")

    print(f"✅ Smart Restocking Orders Scheduled.")
    conn.commit()

# **📌 Sales Data Generation**
sales_data = []
transactions_data = []

for day in range(31):
    sale_date = start_date + timedelta(days=day)
    weekday = sale_date.weekday()

    print(f"📅 Processing {sale_date.strftime('%Y-%m-%d')} (Weekday: {weekday})")

    # **📌 Apply Holiday Effects**
    base_sales = get_daily_sales_target(day, sale_date, weekday)

    # 🎉 General Holiday Boost (Affects all sales)
    if sale_date.strftime('%m-%d') in holiday_sales_boost:
        base_sales *= holiday_sales_boost[sale_date.strftime('%m-%d')]["multiplier"]
        print(f"🎉 HOLIDAY EFFECT on {sale_date.strftime('%Y-%m-%d')}! Increased store traffic!")

    daily_sales_target = int(base_sales)
    total_sales = 0

    while total_sales < daily_sales_target:
        num_products_in_transaction = random.randint(1, 5)
        transaction_time = sale_date + timedelta(
            hours=random.randint(6, 22), minutes=random.randint(0, 59), seconds=random.randint(0, 59)
        )

        transaction_products = random.sample(products, min(num_products_in_transaction, len(products)))
        total_transaction_price = 0
        total_quantity = 0
        sales_records = []

        for product in transaction_products:
            product_id, name, price, stock, avg_sales_per_day, *_ = product
            quantity_sold = random.randint(1, 5)

            if stock < quantity_sold:
                quantity_sold = min(stock, 1)  # Prevent negative stock

            total_price = quantity_sold * float(price)
            total_transaction_price += total_price
            total_quantity += quantity_sold

            sales_records.append((product_id, quantity_sold, total_price, transaction_time.strftime('%Y-%m-%d %H:%M:%S')))

            if quantity_sold > 0:
                cursor.execute("UPDATE products SET stock = GREATEST(stock - %s, 0) WHERE id = %s", (quantity_sold, product_id))

        cursor.execute("INSERT INTO transactions (sale_date, total_price, total_quantity) VALUES (%s, %s, %s)",
                       (transaction_time.strftime('%Y-%m-%d %H:%M:%S'), total_transaction_price, total_quantity))

        conn.commit()
        transaction_id = cursor.lastrowid

        for sale in sales_records:
            sales_data.append((*sale, transaction_id))

        total_sales += num_products_in_transaction
    
    # **📌 Run Restocking AFTER Sales Are Processed**
    replenish_stock(sale_date)
    
# **📌 Insert Sales Data**
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
print("✅ Sales history updated with transaction grouping and correct handling for current date")
