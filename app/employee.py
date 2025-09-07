from app import connection, cursor

def createEmployee(first_name, last_name, email, phone, password):
    cursor.execute(
        "INSERT INTO Employees(first_name, last_name, email, phone, password) VALUES (%s, %s, %s, %s, %s)",
        (first_name, last_name, email, phone, password)
    )

    connection.commit()

def updateEmployee(uid, first_name=None, last_name=None, email=None, phone=None, password=None, rating=None):
    fields = []
    values = []

    if first_name is not None:
        fields.append("first_name = %s")
        values.append(first_name)
    if last_name is not None:
        fields.append("last_name = %s")
        values.append(last_name)
    if email is not None:
        fields.append("email = %s")
        values.append(email)
    if phone is not None:
        fields.append("phone = %s")
        values.append(phone)
    if password is not None:
        fields.append("password = %s")
        values.append(password)
    if rating is not None:
        fields.append("rating = %s")
        values.append(rating)

    if fields:
        query = f"UPDATE Employees SET {', '.join(fields)} WHERE id = %s"
        values.append(uid)
        cursor.execute(query, tuple(values))

        connection.commit()

def deleteEmployee(uid):
    cursor.execute("DELETE FROM Employees WHERE id = %s", (uid,))
    connection.commit()

def viewEmployee(uid):
    cursor.execute("SELECT * FROM Employees WHERE id = %s", (uid,))
    employee = cursor.fetchone()

    return employee

def viewEmployees():
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()

    return employees

# Authentication 
def loginWithEmail(email, password):
    cursor.execute(
        "SELECT * FROM Employees WHERE email = %s AND password = %s",
        (email, password)
    )
    loggedIn = cursor.fetchone()

    if loggedIn:
        return True
    
    return False