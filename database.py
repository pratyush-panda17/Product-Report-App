import sqlite3

def checkProductName(prod_name):
    conn=sqlite3.connect('product_details.db')
    cur=conn.cursor()

    cur.execute("SELECT * FROM products WHERE product = (?)",(prod_name,))

    product = cur.fetchone()

    conn.commit()
    conn.close()
    if product == None:
         return False
    
    return True

def addOne(v):
    conn=sqlite3.connect('product_details.db')
    cur=conn.cursor()

    cur.execute("INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?,?)",(v[0],v[1],v[2],v[3],v[4],v[5],
                                                                    v[6],v[7],v[8],v[9],v[10]))

    conn.commit()
    conn.close()

def deleteOne(prod_name):
    conn=sqlite3.connect('product_details.db')
    cur=conn.cursor()

    cur.execute("DELETE FROM products WHERE product=(?)",(prod_name,))

    conn.commit()
    conn.close()

def showAll():
    conn=sqlite3.connect('product_details.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    formatted_products = []
    for product in products:
            ingredients = product[9].split(",")
            weights = product[10].split(",")
            formatted_products.append((product[0],product[1],product[2],product[3],product[4],
                                       product[5],product[6],product[7],product[8],ingredients,weights))
    conn.commit()
    conn.close()

    return formatted_products

def search(product_name):
    conn=sqlite3.connect('product_details.db')
    cur=conn.cursor()
    cur.execute("SELECT * FROM products WHERE product = (?)",(product_name,))
    product = cur.fetchone()
    if product != None:
        ingredients = product[9].split(",")
        weights = product[10].split(",")
        conn.commit()
        conn.close()
        return ((product[0],product[1],product[2],product[3],product[4],
                product[5],product[6],product[7],product[8],ingredients,weights))
    
    conn.commit()
    conn.close()

    return product

