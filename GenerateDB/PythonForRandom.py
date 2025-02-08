#This code is for random the value of stock and avg_sales_per_day for the project.

import random
import logging

# Setup logging to track stock assignments
logging.basicConfig(filename="stock_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

products = [
    (8852023672021, "Koh-Kae Coated Broad Beans - Shrimp Flavour", 10, "Snack", "Koh-Kae"),
    (8850291111006, "Tong Garden Brand Flavour Broad Beans - Crab Curry", 10, "Snack", "Tong Garden"),
    (8852023664644, "Koh-Kae Honey Roasted Peanuts", 12, "Snack", "Koh-Kae"),
    (8850718801213, "Lays Classic Potato Chips - Original (69g)", 31, "Snack", "Lays"),
    (8850718801121, "Lays Rock Ridged Potato Chips - Original Flavor (69g)", 31, "Snack", "Lays"),
    (6924513906175, "Halls - Mentholyptus Flavored Candy Stick", 15, "Candy", "Halls"),
    (8858729257333, "Horse Correction Tape H-950", 15, "Stationery", "Horse"),
    (8820999320007, "Singha Drinking Water (1500ml)", 14, "Beverage", "Singha"),
    (8850007850229, "Tylenol Paracetamol (500mg)", 17, "Medicine", "Tylenol"),
    (8852914101401, "BL HUA Chlorpheniramine Maleate Tablets (10 tabs/2mg)", 15, "Medicine", "BL HUA"),
    (9300807046418, "Smooth E Anti Acne Hydrogel (10g)", 250, "Beauty", "Smooth E"),
    (6932177474756, "Kadio Calculator KD-350MS", 120, "Electronics", "Kadio"),
    (8850309150058, "JACK 'n JILL Presto Cream-O - Chocolate Sandwich Cookies With Vanilla Flavoured Cream", 120, "Snack", "JACK 'n JILL"),
    (4984824089198, "Panasonic Alkaline AA 1.5V (2 pieces/pack)", 45, "Electronics", "Panasonic"),
    (4971850900726, "Casio Calculator fx-991ES Plus", 320, "Electronics", "Casio"),
    (8857127692647, "Love Potion Buddy Magic Lip Oil - Barbie Roses", 259, "Beauty", "Love Potion"),
    (8850080277722, "Oriental Princess Beneficial Cherish - Lip Sheer SPF 15", 195, "Beauty", "Oriental Princess"),
    (8852612000099, "Neo-Lyte Electrolyte Beverage", 5, "Beverage", "Neo-Lyte"),
    (8852294358013, "Greater Pharma Ca-R-Bon Activated Charcoal Capsules (10 Capsules)", 25, "Medicine", "Greater Pharma"),
    (8854060000010, "IZE jelli balm (7g)", 29, "Medicine", "IZE"),
    (8850773620156, "DOI KHAM Natural Honey 100% (120g)", 42, "Food", "DOI KHAM"),
    (8851959142011, "Coca Cola Original Taste Less Sugar (2L)", 44, "Beverage", "Coca-Cola"),
    (8851959182017, "Coca Cola Original Taste Less Sugar (1.6L)", 38, "Beverage", "Coca-Cola"),
    (8854698010405, "Oishi Green Tea Japanese Green Tea Flavour (800ml)", 30, "Beverage", "Oishi"),
    (8854698010443, "Oishi Green Tea Japanese Green Tea With Honey Lemon (800ml)", 30, "Beverage", "Oishi"),
    (8859015705996, "VIT-A-DAY Vitamin Water C 1000 Kyoho Grape (480ml)", 20, "Beverage", "VIT-A-DAY"),
    (8853474076123, "Favory Brand Natural Sesame Oil (100ml)", 42, "Food", "Favory"),
    (8858973399995, "5 Stars Korat Noodles (230g)", 41, "Instant Noodles", "5 Stars"),
    (8859411300719, "ARO Pop-up Napkin (90 sheet)", 12, "Household", "ARO"),
    (8850250002345, "Ajinomoto Lite Sugar Low Calorie (80g)", 20, "Food", "Ajinomoto"),
    (5000167329421, "Soap&Glory Magnifi-coco - Nourishing Body Lotion (550ml)", 323, "Beauty", "Soap & Glory"),
    (8850999015434, "M-150 Energy Drink (150ml)", 10, "Beverage", "M-150"),
    (8850999015441, "Sponsor Original Energy Drink (250ml)", 15, "Beverage", "Sponsor"),
    (8850127088812, "Dutch Mill Yogurt Drink - Strawberry (180ml)", 12, "Beverage", "Dutch Mill"),
    (8850127088829, "Dutch Mill Yogurt Drink - Mixed Fruits (180ml)", 12, "Beverage", "Dutch Mill"),
    (8850987654321, "Mama Cup Noodles - Shrimp Tom Yum (60g)", 16, "Instant Noodles", "Mama"),
    (8850987654338, "Mama Cup Noodles - Pork Flavor (60g)", 16, "Instant Noodles", "Mama"),
    (8858891303015, "Tesco Lotus Kitchen Paper Towel (2 rolls)", 35, "Household", "Tesco"),
    (8858891303022, "Tesco Lotus Bathroom Tissue (12 rolls)", 109, "Household", "Tesco"),
    (8851932388888, "Colgate Total Professional Clean Toothpaste (150g)", 55, "Personal Care", "Colgate"),
    (8851932388895, "Colgate Max Fresh Cool Mint Toothpaste (150g)", 45, "Personal Care", "Colgate"),
    (8850722800115, "Sunsilk Smooth & Manageable Shampoo (450ml)", 159, "Personal Care", "Sunsilk"),
    (8850722800122, "Sunsilk Strong & Long Shampoo (450ml)", 159, "Personal Care", "Sunsilk"),
    (8850206000135, "Mistine Super Model Miracle Mascara", 129, "Beauty", "Mistine"),
    (8850206000142, "Mistine Wings Extra Long Mascara", 139, "Beauty", "Mistine"),
    (8858842003517, "Siang Pure Oil (3ml)", 25, "Medicine", "Siang Pure"),
    (8858842003524, "Siang Pure Oil (7ml)", 45, "Medicine", "Siang Pure"),
    (8850999123456, "Double A A4 Paper (500 sheets)", 135, "Stationery", "Double A"),
    (8850999123463, "Double A A4 Paper (80 sheets)", 35, "Stationery", "Double A"),
    (8850325012345, "Faber-Castell 2B Pencil (12pcs)", 75, "Stationery", "Faber-Castell"),
    (8858729257340, "Horse Correction Tape H-955", 20, "Stationery", "Horse"),
    (8850718802012, "Lays Nori Seaweed (75g)", 35, "Snack", "Lays"),
    (8850718802029, "Lays Hot Chili Squid (75g)", 35, "Snack", "Lays"),
    (8850987600123, "Bento Squid Snack - Original (24g)", 20, "Snack", "Bento"),
    (8850987600130, "Bento Squid Snack - Spicy (24g)", 20, "Snack", "Bento"),
    (8851959142028, "Sprite (1.25L)", 26, "Beverage", "Coca-Cola"),
    (8851959142035, "Fanta Orange (1.25L)", 26, "Beverage", "Coca-Cola"),
    (8850879100222, "est Cola (1.25L)", 22, "Beverage", "est"),
    (8850879100239, "est Cola Light (1.25L)", 22, "Beverage", "est"),
    (8850999777123, "100 Plus Original (325ml)", 15, "Beverage", "100 Plus"),
    (8850999777130, "100 Plus Lemon Lime (325ml)", 15, "Beverage", "100 Plus"),
    (8858736800123, "Lactasoy Soy Milk Original (300ml)", 12, "Beverage", "Lactasoy"),
    (8858736800130, "Lactasoy Soy Milk Chocolate (300ml)", 12, "Beverage", "Lactasoy"),
    (8850325099887, "Scotch Magic Tape (3/4 inch)", 45, "Stationery", "Scotch"),
    (8850325099894, "Scotch Double Sided Tape (1/2 inch)", 65, "Stationery", "Scotch"),
    (8858891304012, "Post-it Notes (3x3 inch, 100 sheets)", 55, "Stationery", "Post-it"),
    (8858891304029, "Post-it Flags (5 colors)", 75, "Stationery", "Post-it"),
    (8850206099887, "Pond's White Beauty Day Cream (50g)", 129, "Beauty", "Pond's"),
    (8850206099894, "Pond's Age Miracle Day Cream (50g)", 299, "Beauty", "Pond's"),
    (8850722899887, "Nivea Sun Protect & Light Feel SPF50+ (75ml)", 299, "Beauty", "Nivea"),
    (8850722899894, "Nivea Extra White Repair & Protect (400ml)", 259, "Beauty", "Nivea"),
    (8858842099887, "Paracetamol (500mg) GPO (100 tablets)", 35, "Medicine", "GPO"),
    (8858842099894, "Ibuprofen (400mg) GPO (30 tablets)", 45, "Medicine", "GPO"),
    (8850999888123, "Band-Aid Flexible Fabric (20 pieces)", 55, "Medicine", "Band-Aid"),
    (8850999888130, "Band-Aid Water Block (10 pieces)", 65, "Medicine", "Band-Aid"),
    (8858891305012, "Systema Toothbrush - Soft", 35, "Personal Care", "Systema"),
    (8858891305029, "Systema Toothbrush - Medium", 35, "Personal Care", "Systema"),
    (8850325077123, "Safeguard Pure White Bath Soap (135g)", 35, "Personal Care", "Safeguard"),
    (8850325077130, "Safeguard Lemon Fresh Bath Soap (135g)", 35, "Personal Care", "Safeguard"),
    (8850987622222, "Mama Instant Noodles - Pork (55g)", 6, "Instant Noodles", "Mama"),
    (8850987622239, "Mama Instant Noodles - Shrimp Tom Yum (55g)", 6, "Instant Noodles", "Mama"),
    (8851932366666, "Knorr Cup Porridge - Pork (35g)", 20, "Food", "Knorr"),
    (8851932366673, "Knorr Cup Porridge - Chicken (35g)", 20, "Food", "Knorr"),
    (8850722833333, "UFC Sweet Chili Sauce (340g)", 35, "Food", "UFC"),
    (8850722833340, "UFC Sriracha Chili Sauce (340g)", 35, "Food", "UFC"),
    (8858842077777, "MaMa Soy Sauce (700ml)", 45, "Food", "MaMa"),
    (8858842077784, "MaMa Oyster Sauce (300ml)", 55, "Food", "MaMa"),
    (8850999555123, "Tesco Lotus Jasmine Rice (5kg)", 159, "Food", "Tesco"),
    (8850999555130, "Tesco Lotus Brown Rice (2kg)", 89, "Food", "Tesco"),
    (8858891307123, "Breeze Excel Liquid Detergent (3.6L)", 219, "Household", "Breeze"),
    (8858891307130, "Breeze Color Care Liquid Detergent (3.6L)", 219, "Household", "Breeze"),
    (8850325044123, "Vim Dishwashing Liquid - Lemon (750ml)", 75, "Household", "Vim"),
    (8850325044130, "Vim Dishwashing Liquid - Tea Tree Oil (750ml)", 75, "Household", "Vim"),
    (8850987644444, "Kleenex Facial Tissue (170 sheets)", 55, "Household", "Kleenex"),
    (8850987644451, "Kleenex Kitchen Towel (60 sheets)", 65, "Household", "Kleenex"),
    (8851932355555, "Scotch-Brite Scrub Sponge (2 pieces)", 35, "Household", "Scotch-Brite"),
    (8851932355562, "Scotch-Brite Steel Wool (2 pieces)", 25, "Household", "Scotch-Brite"),
    (8850722811111, "Fresh & Soft Bathroom Tissue (12 rolls)", 99, "Household", "Fresh & Soft"),
    (8850722811128, "Fresh & Soft Kitchen Towel (2 rolls)", 45, "Household", "Fresh & Soft"),
    (8858842066666, "Mr. Muscle Glass Cleaner (500ml)", 65, "Household", "Mr. Muscle"),
    (8858842066673, "Mr. Muscle Bathroom Cleaner (500ml)", 65, "Household", "Mr. Muscle"),
    (8850999444123, "Baygon Mosquito Spray (600ml)", 159, "Household", "Baygon"),
    (8850999444130, "Baygon Cockroach Spray (600ml)", 159, "Household", "Baygon"),
    (8858891308123, "Zebra Sarasa Clip Gel Pen 0.5mm - Black", 25, "Stationery", "Zebra"),
    (8858891308130, "Zebra Sarasa Clip Gel Pen 0.5mm - Blue", 25, "Stationery", "Zebra"),
    (8850325033123, "Stabilo Boss Original Highlighter - Yellow", 35, "Stationery", "Stabilo"),
    (8850325033130, "Stabilo Boss Original Highlighter - Green", 35, "Stationery", "Stabilo"),
    (8850987633333, "Pentel EnerGel Pen 0.5mm - Black", 45, "Stationery", "Pentel"),
    (8850987633340, "Pentel EnerGel Pen 0.5mm - Blue", 45, "Stationery", "Pentel"),
    (8851932344444, "3M Post-it Super Sticky Notes (3x3 inch)", 65, "Stationery", "3M"),
    (8851932344451, "3M Post-it Page Markers (5 colors)", 75, "Stationery", "3M"),
    (8850722822222, "Plus Correction Tape (5mm x 6m)", 35, "Stationery", "Plus"),
    (8850722822239, "Plus Glue Stick (22g)", 45, "Stationery", "Plus"),
    (8858842055555, "Artline Drawing Pen 0.1mm - Black", 55, "Stationery", "Artline"),
    (8858842055562, "Artline Drawing Pen 0.3mm - Black", 55, "Stationery", "Artline"),
    (8850999333123, "GEOS Drawing Compass Set", 129, "Stationery", "GEOS"),
    (8850999333130, "GEOS Protractor Set", 49, "Stationery", "GEOS"),
    (8858891309123, "Taro Fish Snack - Original (25g)", 15, "Snack", "Taro"),
    (8858891309130, "Taro Fish Snack - Spicy (25g)", 15, "Snack", "Taro"),
    (8850325022123, "Hanami Prawn Crackers - Original (75g)", 35, "Snack", "Hanami"),
    (8850325022130, "Hanami Prawn Crackers - Hot & Spicy (75g)", 35, "Snack", "Hanami"),
    (8850987622123, "Euro Cake Chocolate (144g)", 25, "Snack", "Euro"),
    (8850987622130, "Euro Cake Vanilla (144g)", 25, "Snack", "Euro"),
    (8851932333123, "Pocky Chocolate (40g)", 25, "Snack", "Pocky"),
    (8851932333130, "Pocky Strawberry (40g)", 25, "Snack", "Pocky"),
    (8850722833123, "Snakku Rice Crackers - Original (100g)", 45, "Snack", "Snakku"),
    (8850722833130, "Snakku Rice Crackers - Seaweed (100g)", 45, "Snack", "Snakku"),
    (8858842044123, "Fun-O Sandwich Cookies - Chocolate (90g)", 20, "Snack", "Fun-O"),
    (8858842044130, "Fun-O Sandwich Cookies - Vanilla (90g)", 20, "Snack", "Fun-O"),
    (8850999222123, "Birdy Robusta Coffee (180ml)", 15, "Beverage", "Birdy"),
    (8850999222130, "Birdy Espresso Coffee (180ml)", 15, "Beverage", "Birdy"),
    (8858891310123, "Ichitan Green Tea - Original (420ml)", 20, "Beverage", "Ichitan"),
    (8858891310130, "Ichitan Green Tea - Honey Lemon (420ml)", 20, "Beverage", "Ichitan"),
    (8850325011123, "Nescafe Red Cup Coffee (360ml)", 25, "Beverage", "Nescafe"),
    (8850325011130, "Nescafe Mocha (360ml)", 25, "Beverage", "Nescafe"),
    (8850987611123, "Crystal Drinking Water (600ml)", 7, "Beverage", "Crystal"),
    (8850987611130, "Crystal Drinking Water (1500ml)", 13, "Beverage", "Crystal"),
    (8851932322123, "Purra Mineral Water (500ml)", 12, "Beverage", "Purra"),
    (8851932322130, "Purra Mineral Water (1500ml)", 20, "Beverage", "Purra"),
    (8850722844123, "Lipton Ice Tea Lemon (445ml)", 20, "Beverage", "Lipton"),
    (8850722844130, "Lipton Ice Tea Peach (445ml)", 20, "Beverage", "Lipton"),
    (8858842033123, "Pepsi (1.5L)", 26, "Beverage", "Pepsi"),
    (8858842033130, "Pepsi Max (1.5L)", 26, "Beverage", "Pepsi"),
    (8850999111123, "Mirinda Orange (1.5L)", 26, "Beverage", "Mirinda"),
    (8850999111130, "Mirinda Strawberry (1.5L)", 26, "Beverage", "Mirinda"),
    (8858891311123, "7-Up (1.5L)", 26, "Beverage", "7-Up"),
    (8858891311130, "7-Up Light (1.5L)", 26, "Beverage", "7-Up"),
    (8850325000123, "Schweppes Manao Soda (325ml)", 15, "Beverage", "Schweppes"),
    (8850325000130, "Schweppes Ginger Ale (325ml)", 15, "Beverage", "Schweppes"),
    (8850987600456, "Ovaltine UHT Chocolate Malt (180ml)", 12, "Beverage", "Ovaltine"),
    (8851932311234, "Milo UHT Chocolate Malt (180ml)", 12, "Beverage", "Milo"),
    (8850722855555, "Wai Wai Quick Zabb Tom Yum Shrimp (60g)", 10, "Food", "Wai Wai"),
    (8858842022222, "Srithai Dried Sweet Basil (15g)", 35, "Food", "Srithai"),
    (8850999000123, "Mae Pranom Chili Paste in Oil (134g)", 45, "Food", "Mae Pranom"),
    (8858891312123, "Tra Chang Fish Sauce (750ml)", 34, "Food", "Tra Chang")
]

# Define bulk purchase sizes for each category
default_bulk_sizes = {
    "Beverage": [48, 72, 96],  
    "Snack": [48, 72, 96],  
    "Candy": [24, 36, 48],  
    "Food": [36, 48, 72],  
    "Instant Noodles": [48, 72, 96, 120],  
    "Household": [12, 24, 36],  
    "Stationery": [12, 24],  
    "Electronics": [3, 5, 10],  
    "Beauty": [12, 24, 36],  
    "Medicine": [5, 10, 15],  
    "Personal Care": [24, 36, 48],  
}

# **Handling perishability for food & beverages**
# ✅ Comprehensive Perishable Keywords
highly_perishable = ["Yogurt", "Milk", "Fresh Juice", "Salad", "Dairy", "Cheese", "Butter", "Egg", "Cream", "Fresh Meat", "Seafood"]
moderately_perishable = ["Cup Porridge", "Ready Meal", "Frozen", "Bread", "Cooked", "Pasta Sauce", "Jam", "Tofu", "Nut Butter"]
long_shelf_life = ["Canned", "Dried", "Powdered", "Instant"]

def get_stock(category, name):
    if any(keyword in name for keyword in highly_perishable):
        stock_value = random.choice([12, 24, 36])  # Small stock to avoid spoilage
    elif any(keyword in name for keyword in moderately_perishable):
        stock_value = random.choice([24, 36, 48])  # Moderate stock
    elif any(keyword in name for keyword in long_shelf_life):
        stock_value = random.choice([48, 72])  # Standard bulk purchase
    else:
        stock_value = random.choice(default_bulk_sizes.get(category, [24, 36]))  # Default for non-perishables

    # ✅ Log the assigned stock for debugging
    logging.info(f"Assigned stock {stock_value} for {name} ({category})")
    
    return stock_value

# Open SQL file to write data.
with open("FirstVersionOfProductsDB.sql", "w", encoding="utf-8") as f_sql, \
     open("FirstVersionOfProductsDB.pydata", "w", encoding="utf-8") as f_py:
         
    f_sql.write("INSERT INTO products (id, name, price, stock, avg_sales_per_day, category, brand_name) VALUES\n")

    values_sql = []
    values_py = []
    
    for product in products:
        product_id, name, price, category, brand_name = product
        stock = get_stock(category, name)  # ✅ This actually assigns stock!

        # Fix single quotes for SQL
        name_sql = name.replace("'", "''")
        brand_sql = brand_name.replace("'", "''")

        # Format SQL row with avg_sales_per_day as NULL
        values_sql.append(f"({product_id}, '{name_sql}', {price}, {stock}, NULL, '{category}', '{brand_sql}')")

        # Format Python-compatible row with avg_sales_per_day as None
        values_py.append(f"({product_id}, '{name}', {price}, {stock}, None, '{category}', '{brand_name}')")

    # ✅ Write to SQL file
    f_sql.write(",\n".join(values_sql) + ";\n")

    # ✅ Write to Python data file
    f_py.write("[\n" + ",\n".join(values_py) + "\n]\n")

print("'FirstVersionOfProductsDB.sql' and 'FirstVersionOfProductsDB.pydata' generated complete")