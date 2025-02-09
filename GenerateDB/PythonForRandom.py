#This code is for random the value of stock and avg_sales_per_day for the project.

import random
import logging
import mysql.connector

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hawks2710Dante_",
    database="smart_inventory",
    auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

# Fetch all categories dynamically
cursor.execute("SELECT id, main_category, sub_category FROM categories")
categories = cursor.fetchall()

# Setup logging to track stock assignments
logging.basicConfig(filename="stock_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Create a dictionary to store category ID mappings
category_map = {(main, sub): cat_id for cat_id, main, sub in categories}

# Function to fetch category ID dynamically
def get_category_id(main_category, sub_category):
    return category_map.get((main_category, sub_category), None)  # Return None if not found

# Define stock levels
stock_levels = {
    # Essential daily items - higher stock due to frequent purchases
    "Beverage": [72, 96, 120],  # Popular items like water, soda
    "Snack": [72, 96, 120],     # High turnover items
    
    # Moderate turnover items
    "Candy": [36, 48, 72],      # Good shelf life, moderate demand
    "Food": [48, 72, 96],       # Shelf-stable foods
    "Household": [36, 48, 72],  # Essential items like tissue, detergent
    
    # Quick meal solutions
    "Instant Noodles": [48, 72, 96],  # Popular quick meals
    
    # Lower turnover but essential items
    "Stationery": [24, 36, 48],     # Stable demand
    "Electronics": [12, 24, 36],     # Higher value items
    "Beauty": [24, 36, 48],         # Personal care items
    "Medicine": [24, 36, 48],       # Essential but controlled items
    "Personal Care": [48, 72, 96],  # Daily necessities
}

# Perishability categories with shelf life considerations
highly_perishable = [
    "Yogurt", "Milk", "Fresh Juice",  # 1-2 weeks shelf life
    "Salad", "Dairy", "Cheese",       # Refrigerated items
    "Butter", "Egg", "Cream",         # Temperature sensitive
    "Fresh Meat", "Seafood"           # Very short shelf life
]

moderately_perishable = [
    "Cup Porridge", "Ready Meal",     # 1-2 months shelf life
    "Frozen", "Bread",                # Medium term storage
    "Cooked", "Pasta Sauce",          # Processed foods
    "Jam", "Tofu", "Nut Butter"       # Preserved foods
]

long_shelf_life = [
    "Canned", "Dried", "Powdered",    # 6+ months shelf life
    "Instant", "Preserved"            # Stable products
]

# Seasonal adjustments
seasonal_factors = {
    "Summer": {
        "Beverage": 1.3,        # Higher drink sales
        "Ice Cream": 1.5,       # More frozen treats
        "Snack": 1.2           # More snacking
    },
    "Rainy": {
        "Instant Noodles": 1.3, # More indoor cooking
        "Medicine": 1.2,        # More health items
        "Household": 1.2       # More cleaning supplies
    }
}

def get_stock(category, name, season=None):
    """
    Determine optimal stock levels based on multiple factors.
    
    Args:
        category (str): Product category
        name (str): Product name
        season (str, optional): Current season for adjustments
    
    Returns:
        int: Recommended stock level
    """
    category = str(category).strip()
    
    # Base stock level
    if category not in stock_levels:
        print(f"⚠️ Warning: Category '{category}' not found. Using default range 36-48.")
        base_stock = random.choice([36, 48])
    else:
        base_stock = random.choice(stock_levels[category])
    
    # Perishability adjustments
    if any(keyword in name for keyword in highly_perishable):
        base_stock = min(base_stock, random.choice([24, 36, 48]))
    elif any(keyword in name for keyword in moderately_perishable):
        base_stock = min(base_stock, random.choice([36, 48, 72]))
    elif any(keyword in name for keyword in long_shelf_life):
        base_stock = random.choice([48, 72, 96])
    
    # Popular brand adjustments
    if "Coca Cola" in name or "Lays" in name:
        base_stock = random.choice([96, 120, 144])
    
    # Seasonal adjustments
    if season and season in seasonal_factors:
        for key, factor in seasonal_factors[season].items():
            if key in name or key == category:
                base_stock = int(base_stock * factor)
    
    # Minimum stock levels for essential items
    if category in ["Medicine", "Personal Care", "Household"]:
        base_stock = max(base_stock, 24)  # Ensure minimum stock for essentials
    
    return base_stock

products = [
    (8852023672021, "Koh-Kae Coated Broad Beans - Shrimp Flavour", 10, "Snack", "Broad Beans", "Koh-Kae"),
    (8850291111006, "Tong Garden Brand Flavour Broad Beans - Crab Curry", 10, "Snack", "Broad Beans", "Tong Garden"),
    (8852023664644, "Koh-Kae Honey Roasted Peanuts", 12, "Snack", "Nuts & Seeds", "Koh-Kae"),
    (8850718801213, "Lays Classic Potato Chips - Original (69g)", 31, "Snack", "Potato Chips", "Lays"),
    (8850718801121, "Lays Rock Ridged Potato Chips - Original Flavor (69g)", 31, "Snack", "Potato Chips", "Lays"),
    (6924513906175, "Halls - Mentholyptus Flavored Candy Stick", 15, "Candy", "Hard Candy", "Halls"),
    (8858729257333, "Horse Correction Tape H-950", 15, "Stationery", "Correction Supplies", "Horse"),
    (8820999320007, "Singha Drinking Water (1500ml)", 14, "Beverage", "Water", "Singha"),
    (8850007850229, "Tylenol Paracetamol (500mg)", 17, "Medicine", "Pain Relievers", "Tylenol"),
    (8852914101401, "BL HUA Chlorpheniramine Maleate Tablets (10 tabs/2mg)", 15, "Medicine", "Allergy Medication", "BL HUA"),
    (9300807046418, "Smooth E Anti Acne Hydrogel (10g)", 250, "Beauty", "Skincare", "Smooth E"),
    (6932177474756, "Kadio Calculator KD-350MS", 120, "Stationery", "Office Supplies", "Kadio"),
    (8850309150058, "JACK 'n JILL Presto Cream-O - Chocolate Sandwich Cookies With Vanilla Flavoured Cream", 120, "Snack", "Biscuits & Cookies", "JACK 'n JILL"),
    (4984824089198, "Panasonic Alkaline AA 1.5V (2 pieces/pack)", 45, "Household", "Batteries & Power Accessories", "Panasonic"),
    (4971850900726, "Casio Calculator fx-991ES Plus", 320, "Stationery", "Office Supplies", "Casio"),
    (8857127692647, "Love Potion Buddy Magic Lip Oil - Barbie Roses", 259, "Beauty", "Cosmetics", "Love Potion"),
    (8850080277722, "Oriental Princess Beneficial Cherish - Lip Sheer SPF 15", 195, "Beauty", "Cosmetics", "Oriental Princess"),
    (8852612000099, "Neo-Lyte Electrolyte Beverage", 5, "Beverage", "Sports Drinks", "Neo-Lyte"),
    (8852294358013, "Greater Pharma Ca-R-Bon Activated Charcoal Capsules (10 Capsules)", 25, "Medicine", "Digestive Aids", "Greater Pharma"),
    (8854060000010, "IZE jelli balm (7g)", 29, "Medicine", "First Aid", "IZE"),
    (8850773620156, "DOI KHAM Natural Honey 100% (120g)", 42, "Food", "Cooking Essentials", "DOI KHAM"),
    (8851959142011, "Coca Cola Original Taste Less Sugar (2L)", 44, "Beverage", "Soft Drinks", "Coca-Cola"),
    (8851959182017, "Coca Cola Original Taste Less Sugar (1.6L)", 38, "Beverage", "Soft Drinks", "Coca-Cola"),
    (8854698010405, "Oishi Green Tea Japanese Green Tea Flavour (800ml)", 30, "Beverage", "Tea & Coffee", "Oishi"),
    (8854698010443, "Oishi Green Tea Japanese Green Tea With Honey Lemon (800ml)", 30, "Beverage", "Tea & Coffee", "Oishi"),
    (8859015705996, "VIT-A-DAY Vitamin Water C 1000 Kyoho Grape (480ml)", 20, "Beverage", "Vitamin Drinks", "VIT-A-DAY"),
    (8853474076123, "Favory Brand Natural Sesame Oil (100ml)", 42, "Food", "Cooking Essentials", "Favory"),
    (8858973399995, "5 Stars Korat Noodles (230g)", 41, "Instant Noodles", "Packaged Noodles", "5 Stars"),
    (8859411300719, "ARO Pop-up Napkin (90 sheet)", 12, "Household", "Paper Products", "ARO"),
    (8850250002345, "Ajinomoto Lite Sugar Low Calorie (80g)", 20, "Food", "Cooking Essentials", "Ajinomoto"),
    (5000167329421, "Soap&Glory Magnifi-coco - Nourishing Body Lotion (550ml)", 323, "Beauty", "Skincare", "Soap & Glory"),
    (8851123212021, "M-150 Energy Drink (150ml)", 10, "Beverage", "Energy Drinks", "M-150"),
    (8850228000403, "SPONSOR Original Electrolyte Beverage (250ml)", 12, "Beverage", "Energy Drinks", "Sponsor"),
    (8851717030147, "Dutch Mill Yogurt Drink - Strawberry (830cc)", 40, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717030123, "Dutch Mill Yogurt Drink - Orange (830cc)", 40, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717030161, "Dutch Mill Yogurt Drink - Mixed Fruits (830cc)", 40, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717030192, "Dutch Mill Yogurt Drink - Blueberry (830cc)", 40, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717904578, "Dutch Mill Life Plus 2percent Sugar - Mixed Fruits and Vegetables Flavour (830cc)", 40, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717030154, "Dutch Mill Yogurt Drink - Mixed Fruits (400cc)", 25, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717901874, "Dutch Mill Pasteurized Milk Plain (400cc)", 26.50, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717901881, "Dutch Mill Pasteurized Milk Non Fat (400cc)", 26.50, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8851717901195, "Dutch Mill Pasteurized Milk Non Fat (830cc)", 48.50, "Beverage", "Milk & Fresh Juice", "Dutch Mill"),
    (8850987654321, "Mama Cup Noodles - Shrimp Tom Yum (60g)", 16, "Instant Noodles", "Cup Noodles", "Mama"),
    (8850987654338, "Mama Cup Noodles - Pork Flavor (60g)", 16, "Instant Noodles", "Cup Noodles", "Mama"),
    (8850987101205, "Mama Instant Noodles - Shrimp Tom Yum Flavour (55g) (1 Pack/10 units)", 16, "Instant Noodles", "Packaged Noodles", "Mama"),
    (8858891303015, "Tesco LOTUSS MULTI PURPOSE TOWEL (2 rolls)", 57, "Household", "Paper Products", "LOTUSS"),
    (8850046338344, "LOTUSS SOFT TOILET TISSUE (12 rolls)", 34, "Household", "Paper Products", "LOTUSS"),
    (8850046337668, "Cellox Toilet Tissue 2ply Double Roll Pack (32 rolls)", 375, "Household", "Paper Products", "Cellox"),
    (8888336006093, "Scott Paper Towel Big Roll (2 rolls)", 63, "Household", "Paper Products", "Scott"),
    (8888336024196, "Scott Clean Care Toilet Tissue 3 ply (24 rolls)", 315, "Household", "Paper Products", "Scott"),
    (8888336027760, "Scott Clean Care Toilet Tissue Super Jumbo 2XL (24 rolls)", 399, "Household", "Paper Products", "Scott"),
    (8888336032061, "Scott Clean Care Toilet Tissue 3XL (6 rolls)", 135, "Household", "Paper Products", "Scott"),
    (6920354806032, "Colgate Total Professional Clean Jel Toothpaste (80g)", 59, "Personal Care", "Toothbrush & Toothpaste", "Colgate"),
    (6920354806063, "Colgate Total Professional Clean Gel Toothpaste (150g) (Pack 2)", 209, "Personal Care", "Toothbrush & Toothpaste", "Colgate"),
    (8850006232569, "Colgate Regular Toothpaste (150g) (Pack 2)", 119, "Personal Care", "Toothbrush & Toothpaste", "Colgate"),
    (8851007105111, "Sensodyne Sensitivity&Gum Toothpaste (100g)", 217, "Personal Care", "Toothbrush & Toothpaste", "Sensodyne"),
    (8851007197925, "Sensodyne Repair and Protect Whitening Toothpaste (100g)", 215, "Personal Care", "Toothbrush & Toothpaste", "Sensodyne"),
    (8851007199172, "Sensodyne Multi Care Toothpaste (160g) (Pack 2)", 339, "Personal Care", "Toothbrush & Toothpaste", "Sensodyne"),
    (8850082000236, "Fluocaril Original Toothpaste (150g) (Pack 2)", 339, "Personal Care", "Toothbrush & Toothpaste", "Fluocaril"),
    (8851932354905, "Sunsilk Smooth & Manageable Shampoo (520ml)", 199, "Personal Care", "Shampoo & Conditioner", "Sunsilk"),
    (8851932354615, "Sunsilk Smooth & Manageable Hair Conditioner (490ml)", 199, "Personal Care", "Shampoo & Conditioner", "Sunsilk"),
    (8851932430753, "Sunsilk Smooth&Manageable Shampoo (475ml), Bonus Pack Shampoo&Conditioner (450ml)", 249, "Personal Care", "Shampoo & Conditioner", "Sunsilk"),
    (4902430565585, "Head&Shoulders Clean&Balanced Shampoo (370ml)", 199, "Personal Care", "Shampoo & Conditioner", "Head&Shoulders"),
    (4902430430999, "Head&Shoulders Smooth and Silky Shampoo (370ml)", 199, "Personal Care", "Shampoo & Conditioner", "Head&Shoulders"),
    (4902430565578, "Head&Shoulders Apple Fresh Shampoo (370ml)", 199, "Personal Care", "Shampoo & Conditioner", "Head&Shoulders"),
    (4902430281331, "Head&Shoulders Cool Menthol Shampoo (370ml)", 199, "Personal Care", "Shampoo & Conditioner", "Head&Shoulders"),
    (4987176172624, "Head and Shoulders Anti Hairfall with Ginseng Shampoo (370ml)", 199, "Personal Care", "Shampoo & Conditioner", "Head&Shoulders"),
    (8855629006108, "Mistine Super Model Miracle Mascara", 105, "Beauty", "Cosmetics", "Mistine"),
    (8859178705086, "Mistine Pro Long Big Eye Waterproof Mascara (4g)", 195, "Beauty", "Cosmetics", "Mistine"),
    (8850109001130, "Siang Pure Oil Formula I (3ml)", 23, "Medicine", "First Aid", "Siang Pure"),
    (8850109051111, "Siang Pure Oil Formula1 (25ml) (1 Pack/6 unit)", 740, "Medicine", "First Aid", "Siang Pure"),
    (8851306008977, "Double A A4 Paper (500 sheets)", 165, "Stationery", "Paper Products", "Double A"),
    (8850999123463, "Double A Paper 80gram (100 sheets)", 45, "Stationery", "Paper Products", "Double A"),
    (8850325012345, "Faber-Castell 2B Pencil (12pcs)", 75, "Stationery", "Writing Instruments", "Faber-Castell"),
    (8858729257340, "Horse Correction Tape H-955", 20, "Stationery", "Correction Supplies", "Horse"),
    (8850718802012, "Lays Nori Seaweed (75g)", 35, "Snack", "Potato Chips", "Lays"),
    (8850718802029, "Lays Hot Chili Squid (75g)", 35, "Snack", "Potato Chips", "Lays"),
    (8850987600123, "Bento Squid Snack - Original (24g)", 20, "Snack", "Squid Snack", "Bento"),
    (8850987600130, "Bento Squid Snack - Spicy (24g)", 20, "Snack", "Squid Snack", "Bento"),
    (8851959142028, "Sprite (1.25L)", 26, "Beverage", "Soft Drinks", "Coca-Cola"),
    (8851959142035, "Fanta Orange (1.25L)", 26, "Beverage", "Soft Drinks", "Coca-Cola"),
    (8850879100222, "est Cola (1.25L)", 22, "Beverage", "Soft Drinks", "est"),
    (8850879100239, "est Cola Light (1.25L)", 22, "Beverage", "Soft Drinks", "est"),
    (8850999777123, "100 Plus Original (325ml)", 15, "Beverage", "Sports Drinks", "100 Plus"),
    (8850999777130, "100 Plus Lemon Lime (325ml)", 15, "Beverage", "Sports Drinks", "100 Plus"),
    (8858736800123, "Lactasoy Soy Milk Original (300ml)", 12, "Beverage", "Milk & Fresh Juice", "Lactasoy"),
    (8858736800130, "Lactasoy Soy Milk Chocolate (300ml)", 12, "Beverage", "Milk & Fresh Juice", "Lactasoy"),
    (8850325099887, "Scotch Magic Tape (3/4 inch)", 45, "Stationery", "Office Supplies", "Scotch"),
    (8850325099894, "Scotch Double Sided Tape (1/2 inch)", 65, "Stationery", "Office Supplies", "Scotch"),
    (8858891304012, "Post-it Notes (3x3 inch, 100 sheets)", 55, "Stationery", "Paper Products", "Post-it"),
    (8858891304029, "Post-it Flags (5 colors)", 75, "Stationery", "Paper Products", "Post-it"),
    (8850206099887, "Pond's White Beauty Day Cream (50g)", 129, "Beauty", "Skincare", "Pond's"),
    (8850206099894, "Pond's Age Miracle Day Cream (50g)", 299, "Beauty", "Skincare", "Pond's"),
    (8850722899887, "Nivea Sun Protect & Light Feel SPF50+ (75ml)", 299, "Beauty", "Skincare", "Nivea"),
    (8850722899894, "Nivea Extra White Repair & Protect (400ml)", 259, "Beauty", "Skincare", "Nivea"),
    (8858842099887, "Paracetamol (500mg) GPO (100 tablets)", 35, "Medicine", "Pain Relievers", "GPO"),
    (8858842099894, "Ibuprofen (400mg) GPO (30 tablets)", 45, "Medicine", "Pain Relievers", "GPO"),
    (8850999888123, "Band-Aid Flexible Fabric (20 pieces)", 55, "Medicine", "First Aid", "Band-Aid"),
    (8850999888130, "Band-Aid Water Block (10 pieces)", 65, "Medicine", "First Aid", "Band-Aid"),
    (8858891305012, "Systema Toothbrush - Soft", 35, "Personal Care", "Toothbrush & Toothpaste", "Systema"),
    (8858891305029, "Systema Toothbrush - Medium", 35, "Personal Care", "Toothbrush & Toothpaste", "Systema"),
    (8850325077123, "Safeguard Pure White Bath Soap (135g)", 35, "Personal Care", "Soap & Body Wash", "Safeguard"),
    (8850325077130, "Safeguard Lemon Fresh Bath Soap (135g)", 35, "Personal Care", "Soap & Body Wash", "Safeguard"),
    (8850987622222, "Mama Instant Noodles - Pork (55g)", 6, "Instant Noodles", "Packaged Noodles", "Mama"),
    (8850987622239, "Mama Instant Noodles - Shrimp Tom Yum (55g)", 6, "Instant Noodles", "Packaged Noodles", "Mama"),
    (8851932366666, "Knorr Cup Porridge - Pork (35g)", 20, "Food", "Instant Meals", "Knorr"),
    (8851932366673, "Knorr Cup Porridge - Chicken (35g)", 20, "Food", "Instant Meals", "Knorr"),
    (8850722833333, "UFC Sweet Chili Sauce (340g)", 35, "Food", "Condiments & Sauces", "UFC"),
    (8850722833340, "UFC Sriracha Chili Sauce (340g)", 35, "Food", "Condiments & Sauces", "UFC"),
    (8858842077777, "MaMa Soy Sauce (700ml)", 45, "Food", "Condiments & Sauces", "MaMa"),
    (8858842077784, "MaMa Oyster Sauce (300ml)", 55, "Food", "Condiments & Sauces", "MaMa"),
    (8850999555123, "Tesco Lotus Jasmine Rice (5kg)", 159, "Food", "Cooking Essentials", "Tesco"),
    (8850999555130, "Tesco Lotus Brown Rice (2kg)", 89, "Food", "Cooking Essentials", "Tesco"),
    (8858891307123, "Breeze Excel Liquid Detergent (3.6L)", 219, "Household", "Laundry & Detergents", "Breeze"),
    (8858891307130, "Breeze Color Care Liquid Detergent (3.6L)", 219, "Household", "Laundry & Detergents", "Breeze"),
    (8850325044123, "Vim Dishwashing Liquid - Lemon (750ml)", 75, "Household", "Cleaning Products", "Vim"),
    (8850325044130, "Vim Dishwashing Liquid - Tea Tree Oil (750ml)", 75, "Household", "Cleaning Products", "Vim"),
    (8850987644444, "Kleenex Facial Tissue (170 sheets)", 55, "Household", "Paper Products", "Kleenex"),
    (8850987644451, "Kleenex Kitchen Towel (60 sheets)", 65, "Household", "Paper Products", "Kleenex"),
    (8851932355555, "Scotch-Brite Scrub Sponge (2 pieces)", 35, "Household", "Cleaning Products", "Scotch-Brite"),
    (8851932355562, "Scotch-Brite Steel Wool (2 pieces)", 25, "Household", "Cleaning Products", "Scotch-Brite"),
    (8850722811111, "Fresh & Soft Bathroom Tissue (12 rolls)", 99, "Household", "Paper Products", "Fresh & Soft"),
    (8850722811128, "Fresh & Soft Kitchen Towel (2 rolls)", 45, "Household", "Paper Products", "Fresh & Soft"),
    (8858842066666, "Mr. Muscle Glass Cleaner (500ml)", 65, "Household", "Cleaning Products", "Mr. Muscle"),
    (8858842066673, "Mr. Muscle Bathroom Cleaner (500ml)", 65, "Household", "Cleaning Products", "Mr. Muscle"),
    (8850999444123, "Baygon Mosquito Spray (600ml)", 159, "Household", "Pest Control", "Baygon"),
    (8850999444130, "Baygon Cockroach Spray (600ml)", 159, "Household", "Pest Control", "Baygon"),
    (8858891308123, "Zebra Sarasa Clip Gel Pen 0.5mm - Black", 25, "Stationery", "Writing Instruments", "Zebra"),
    (8858891308130, "Zebra Sarasa Clip Gel Pen 0.5mm - Blue", 25, "Stationery", "Writing Instruments", "Zebra"),
    (8850325033123, "Stabilo Boss Original Highlighter - Yellow", 35, "Stationery", "Writing Instruments", "Stabilo"),
    (8850325033130, "Stabilo Boss Original Highlighter - Green", 35, "Stationery", "Writing Instruments", "Stabilo"),
    (8850987633333, "Pentel EnerGel Pen 0.5mm - Black", 45, "Stationery", "Writing Instruments", "Pentel"),
    (8850987633340, "Pentel EnerGel Pen 0.5mm - Blue", 45, "Stationery", "Writing Instruments", "Pentel"),
    (8851932344444, "3M Post-it Super Sticky Notes (3x3 inch)", 65, "Stationery", "Paper Products", "3M"),
    (8851932344451, "3M Post-it Page Markers (5 colors)", 75, "Stationery", "Paper Products", "3M"),
    (8850722822222, "Plus Correction Tape (5mm x 6m)", 35, "Stationery", "Correction Supplies", "Plus"),
    (8850722822239, "Plus Glue Stick (22g)", 45, "Stationery", "Office Supplies", "Plus"),
    (8858842055555, "Artline Drawing Pen 0.1mm - Black", 55, "Stationery", "Art Supplies", "Artline"),
    (8858842055562, "Artline Drawing Pen 0.3mm - Black", 55, "Stationery", "Art Supplies", "Artline"),
    (8850999333123, "GEOS Drawing Compass Set", 129, "Stationery", "Art Supplies", "GEOS"),
    (8850999333130, "GEOS Protractor Set", 49, "Stationery", "Art Supplies", "GEOS"),
    (8858891309123, "Taro Fish Snack - Original (25g)", 15, "Snack", "Squid Snack", "Taro"),
    (8858891309130, "Taro Fish Snack - Spicy (25g)", 15, "Snack", "Squid Snack", "Taro"),
    (8850325022123, "Hanami Prawn Crackers - Original (75g)", 35, "Snack", "Rice Crackers", "Hanami"),
    (8850325022130, "Hanami Prawn Crackers - Hot & Spicy (75g)", 35, "Snack", "Rice Crackers", "Hanami"),
    (8850987622123, "Euro Cake Chocolate (144g)", 25, "Snack", "Biscuits & Cookies", "Euro"),
    (8850987622130, "Euro Cake Vanilla (144g)", 25, "Snack", "Biscuits & Cookies", "Euro"),
    (8851932333123, "Pocky Chocolate (40g)", 25, "Snack", "Biscuits & Cookies", "Pocky"),
    (8851932333130, "Pocky Strawberry (40g)", 25, "Snack", "Biscuits & Cookies", "Pocky"),
    (8850722833123, "Snakku Rice Crackers - Original (100g)", 45, "Snack", "Rice Crackers", "Snakku"),
    (8850722833130, "Snakku Rice Crackers - Seaweed (100g)", 45, "Snack", "Rice Crackers", "Snakku"),
    (8850309200173, "Fun-O Sandwich Cookies - Chocolate (90g)", 20, "Snack", "Biscuits & Cookies", "Fun-O"),
    (8850309212602, "Fun-O Sandwich Cookies - Vanilla (90g)", 20, "Snack", "Biscuits & Cookies", "Fun-O"),
    (8850250000365, "Birdy Robusta Coffee (180ml)", 15, "Beverage", "Tea & Coffee", "Birdy"),
    (8850250006015, "Birdy Espresso Coffee (180ml)", 15, "Beverage", "Tea & Coffee", "Birdy"),
    (8858891300110, "Ichitan Green Tea - Original (420ml)", 20, "Beverage", "Tea & Coffee", "Ichitan"),
    (8858891300073, "Ichitan Green Tea - Honey Lemon (420ml)", 20, "Beverage", "Tea & Coffee", "Ichitan"),
    (8850128030074, "Nescafe Red Cup Coffee (360ml)", 25, "Beverage", "Tea & Coffee", "Nescafe"),
    (8852099010819, "Khao Shong Agglomerated Instant Coffee (100% Coffee) 360g", 330, "Beverage", "Tea & Coffee", "Khao Shong"),
    (8851530160038, "Mont Fleur Natural Mineral Water (1L)", 6, "Beverage", "Water", "Mont Fleur"),
    (8851952350789, "Crystal Drinking Water (600ml) (1 Pack/12 bottles)", 13, "Beverage", "Water", "Crystal"),
    (8850999001449, "Purra Mineral Water (600ml)", 10, "Beverage", "Water", "Purra"),
    (8850999001463, "Purra Mineral Water (1500ml)", 20, "Beverage", "Water", "Purra"),
    (8858998585076, "Lipton Ice Tea Lemon (445ml)", 20, "Beverage", "Tea & Coffee", "Lipton"),
    (8858998585090, "Lipton Ice Tea Peach (445ml)", 20, "Beverage", "Tea & Coffee", "Lipton"),
    (8858998581061, "Pepsi (1.45L)", 28, "Beverage", "Soft Drinks", "Pepsi"),
    (8858998581177, "Pepsi Max (1.45L)", 28, "Beverage", "Soft Drinks", "Pepsi"),
    (8858998582051, "Mirinda Orange (1.45L)", 30, "Beverage", "Soft Drinks", "Mirinda"),
    (8858998582105, "Mirinda Strawberry (1.45L)", 30, "Beverage", "Soft Drinks", "Mirinda"),
    (8858998583140, "7-Up Free Sugar(440ml)", 16, "Beverage", "Soft Drinks", "7-Up"),
    (8858998583157, "7-Up Free Sugar (1.45L)", 30, "Beverage", "Soft Drinks", "7-Up"),
    (8851959132678, "Schweppes Manao Soda (325ml)", 17, "Beverage", "Soft Drinks", "Schweppes"),
    (8851959132661, "Schweppes Ginger Ale (325ml)", 17, "Beverage", "Soft Drinks", "Schweppes"),
    (8850086161728, "Ovaltine UHT Chocolate Malt (170ml) (1 Pack/12 Carton)", 129, "Beverage", "Milk & Fresh Juice", "Ovaltine"),
    (8850086161704, "Ovaltine UHT Chocolate Malt (170ml) (1 Pack/4 Carton)", 48, "Beverage", "Milk & Fresh Juice", "Ovaltine"),
    (8850125091542, "Milo UHT Chocolate Malt Flavoured UHT Milk No Sucrose (180ml) (1 Pack/4 units)", 45, "Beverage", "Milk & Fresh Juice", "Milo"),
    (8850250014683, "YUM YUM Sood-Ded Instant Noodles Stir-Fry Spicy Scallop in XO Sauce Flavor (75g)", 11, "Instant Noodles", "Packaged Noodles", "Ajinomoto"),
    (8850250014706, "YUM YUM Sood-Ded Instant Noodles Stir-Fry Spicy Scallop in XO Sauce Flavor (75g) (1 Pack/5 units)", 51, "Instant Noodles", "Packaged Noodles", "Ajinomoto"),
    (8850487005126, "Mae Pranom Na Rog Chilli Paste (134g)", 100, "Food", "Condiments & Sauces", "Mae Pranom"),
    (8850180050027, "TRA CHANG Fish Sauce (750cc)", 48, "Food", "Condiments & Sauces", "Tra Chang")
]

# Open SQL file to write data.
with open("FirstVersionOfProductsDB.sql", "w", encoding="utf-8") as f_sql, \
     open("FirstVersionOfProductsDB.pydata", "w", encoding="utf-8") as f_py:
    
    f_sql.write("INSERT INTO products (id, name, price, stock, initial_stock, avg_sales_per_day, category_id, brand_name) VALUES\n")

    values_sql = []
    values_py = []
    
    for product in products:
        product_id, name, price, main_category, sub_category, brand_name = product
        category_id = get_category_id(main_category, sub_category)

        if category_id is None:
            print(f"⚠️ Warning: Category ({main_category} > {sub_category}) not found for product {name}. Skipping entry.")
            continue

        stock = get_stock(main_category, name)
        initial_stock = stock
        
        # Fix single quotes for SQL
        name_sql = name.replace("'", "''")
        brand_sql = brand_name.replace("'", "''")

        # Format SQL row
        values_sql.append(f"({product_id}, '{name_sql}', {price}, {stock}, {initial_stock}, NULL, {category_id}, '{brand_sql}')")

        # Format Python-compatible row
        values_py.append(f"({product_id}, '{name}', {price}, {stock}, {initial_stock}, None, {category_id}, '{brand_name}')")

    # Write to SQL file
    f_sql.write(",\n".join(values_sql) + ";\n")

    # Write to Python data file
    f_py.write("[\n" + ",\n".join(values_py) + "\n]\n")

print("'FirstVersionOfProductsDB.sql' and 'FirstVersionOfProductsDB.pydata' generated complete")