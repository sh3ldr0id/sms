from app import connection, cursor

def createProduct(name, stock, cost, price):
    cursor.execute("""
        INSERT INTO Products(name, stock, cost, price)
        VALUES (%s, %s, %s, %s)
    """, (name, stock, cost, price))

    connection.commit()

def updateProduct(uid, name=None, quantity=None, cost=None, price=None):
    cursor.execute("""
        UPDATE Products
        SET name = %s, quantity = %s, cost = %s, price = %s
        WHERE id = %s
    """, (name, quantity, cost, price, uid))

    connection.commit()

def updateProduct(uid, name=None, stock=None, cost=None, price=None):
    fields = []
    values = []

    if name is not None:
        fields.append("name = %s")
        values.append(name)
    if stock is not None:
        fields.append("stock = %s")
        values.append(stock)
    if cost is not None:
        fields.append("cost = %s")
        values.append(cost)
    if price is not None:
        fields.append("price = %s")
        values.append(price)

    if fields:
        query = f"UPDATE Products SET {', '.join(fields)} WHERE id = %s"
        values.append(uid)
        cursor.execute(query, tuple(values))

        connection.commit()

def deleteProduct(uid):
    cursor.execute("DELETE FROM Products WHERE id = %s", (uid,))
    connection.commit()

def viewProduct(uid):
    cursor.execute("SELECT * FROM Products WHERE id = %s", (uid,))
    product = cursor.fetchone()

    return product

def viewProducts():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    return products

def fetchPrice(uid):
    cursor.execute("""
        SELECT price FROM Products WHERE id = %s
    """, (uid,))
    
    price = cursor.fetchone()[0]

    return price