#This code is for random the value of stock and avg_sales_per_day for the project.
import random

products = [
    (8852023672021, 'Koh-Kae Coated Broad Beans - Shrimp Flavour', 10, 'Snack', 'Koh-Kae'),
    (8850291111006, 'Tong Garden Brand Flavour Broad Beans - Crab Curry', 10, 'Snack', 'Tong Garden'),
    (8852023664644, 'Koh-Kae Honey Roasted Peanuts', 12, 'Snack', 'Koh-Kae'),
    (8850718801213, 'Lays Classic Potato Chips - Original (69g)', 31, 'Snack', 'Lays'),
    (8850718801121, 'Lays Rock Ridged Potato Chips - Original Flavor (69g)', 31, 'Snack', 'Lays'),
    (6924513906175, 'Halls - Mentholyptus Flavored Candy Stick', 15, 'Candy', 'Halls'),
    (8858729257333, 'Horse Correction Tape H-950', 15, 'Stationery', 'Horse'),
    (8820999320007, 'Singha Drinking Water (1500ml)', 14, 'Beverage', 'Singha'),
    (8850007850229, 'Tylenol Paracetamol (500mg)', 17, 'Medicine', 'Tylenol'),
    (8852914101401, 'BL HUA Chlorpheniramine Maleate Tablets (10 tabs/2mg)', 15, 'Medicine', 'BL HUA'),
    (9300807046418, 'Smooth E Anti Acne Hydrogel (10g)', 250, 'Beauty', 'Smooth E'),
    (6932177474756, 'Kadio Calculator KD-350MS', 120, 'Electronics', 'Kadio'),
    (8850309150058, 'JACK \'n JILL Presto Cream-O - Chocolate Sandwich Cookies With Vanilla Flavoured Cream', 120, 'Snack', 'JACK \'n JILL'),
    (4984824089198, 'Panasonic Alkaline AA 1.5V (2 pieces/pack)', 45, 'Electronics', 'Panasonic'),
    (4971850900726, 'Casio Calculator fx-991ES Plus', 320, 'Electronics', 'Casio'),
    (8857127692647, 'Love Potion Buddy Magic Lip Oil - Barbie Roses', 259, 'Beauty', 'Love Potion'),
    (8850080277722, 'Oriental Princess Beneficial Cherish - Lip Sheer SPF 15', 195, 'Beauty', 'Oriental Princess'),
    (8852612000099, 'Neo-Lyte Electrolyte Beverage', 5, 'Beverage', 'Neo-Lyte'),
    (8852294358013, 'Greater Ca-R-Bon Activated Charcoal Capsules (10 Capsules)', 25, 'Medicine', 'Greater Pharma'),
    (8854060000010, 'IZE jelli balm (7g)', 29, 'Medicine', 'IZE'),
    (8850773620156, 'DOI KHAM Natural Honey 100% (120g)', 42, 'Food', 'DOI KHAM'),
    (8851959142011, 'Coca Cola Original Taste Less Sugar (2L)', 44, 'Beverage', 'Coca-Cola'),
    (8851959182017, 'Coca Cola Original Taste Less Sugar (1.6L)', 38, 'Beverage', 'Coca-Cola'),
    (8854698010405, 'Oishi Green Tea Japanese Green Tea Flavour (800ml)', 30, 'Beverage', 'Oishi'),
    (8854698010443, 'Oishi Green Tea Japanese Green Tea With Honey Lemon (800ml)', 30, 'Beverage', 'Oishi'),
    (8859015705996, 'VIT-A-DAY Vitamin Water C 1000 Kyoho Grape (480ml)', 20, 'Beverage', 'VIT-A-DAY'),
    (8853474076123, 'Favory Brand Natural Sesame Oil (100ml)', 42, 'Food', 'Favory'),
    (8858973399995, '5 Stars Korat Noodles (230g)', 41, 'Food', '5 Stars'),
    (8859411300719, 'ARO Pop-up Napkin (90 sheet)', 12, 'Household', 'ARO'),
    (8850250002345, 'Ajinomoto Lite Sugar Low Calorie (80g)', 20, 'Food', 'Ajinomoto'),
    (5000167329421, 'Soap&Glory Magnifi-coco - Nourishing Body Lotion (550ml)', 323, 'Beauty', 'Soap & Glory'),
]

#Open SQL file to write data.
with open("insert_products.sql", "w", encoding="utf-8") as f:
    f.write("INSERT INTO products (id, name, price, stock, avg_sales_per_day, category, brand_name) VALUES\n")

    values = []
    for product in products:
        product_id, name, price, category, brand = product

        #Stock Logic Based on Product's Price
        if price > 200:
            stock = 20  #Expensive items, low stock
        elif 50 <= price <= 199:
            stock = 35  #Mid-range items, medium stock
        else:
            stock = 40  #Cheap items, high stock

        # Append SQL value row
        values.append(f"({product_id}, '{name}', {price}, {stock}, NULL, '{category}', '{brand}')")

    #Write values to file
    f.write(",\n".join(values) + ";\n")

print("'insert_products.sql' generated complete")