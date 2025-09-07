from app import connection, cursor

def createCustomer(first_name, last_name, phone):
    cursor.execute(
        "INSERT INTO Customers(first_name, last_name, phone) VALUES (%s, %s, %s)",
        (first_name, last_name, phone)
    )

    connection.commit()

def updateCustomer(uid, first_name=None, last_name=None, phone=None):
    fields = []
    values = []

    if first_name is not None:
        fields.append("first_name = %s")
        values.append(first_name)
    if last_name is not None:
        fields.append("last_name = %s")
        values.append(last_name)
    if phone is not None:
        fields.append("phone = %s")
        values.append(phone)

    if fields:
        query = f"UPDATE Customers SET {', '.join(fields)} WHERE id = %s"
        values.append(uid)
        cursor.execute(query, tuple(values))

        connection.commit()

def deleteCustomer(uid):
    cursor.execute("DELETE FROM Customers WHERE id = %s", (uid,))
    connection.commit()

def viewCustomer(uid):
    cursor.execute("SELECT * FROM Customers WHERE id = %s", (uid,))
    customer = cursor.fetchone()

    return customer

def viewCustomers():
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()

    return customers

def findByPhone(phone):
    cursor.execute(
        "SELECT * FROM Customers WHERE phone = %s",
        (phone,)
    )

    customers = cursor.fetchall()

    return customers