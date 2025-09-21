import mysql.connector as mc
from pickle import dump, load
from os import remove

connection = mc.connect(
    host="localhost",      
    user="root",            
    password="root", 
    database="SMSdb"  
)

cursor = connection.cursor()

from app.employee import *
from app.customer import *
from app.logistics import *
from app.billing import *

user = None

def start():
    global user

    email, password = None, None

    try:
        with open("session.dat", "rb") as f:
            session = load(f)
            
            email = session.get("email")
            password = session.get("password")

    except FileNotFoundError:
        print("🔒  No saved session found. Please log in to continue.")

    except:
        print("⚠️  Error loading session data. Please log in to continue.")

    if email and password:
        user = loginWithEmail(email, password)

        if user:
            print(f"👋  Welcome back, {user[1]} {user[2]}!")
            print("=" * 60)
            print("You are now logged in to the SMS - Shop Management System.\n")

        else:
            print("🔒  Session expired. Please log in to continue.\n" + "=" * 60)

    while not user:
        print("\n" + "=" * 60)
        print(" " * 18 + "🔐  Login  🔐")
        print("=" * 60)
        email = input("📧  Enter email: ").strip()
        password = input("🔑  Enter password: ").strip()
        print("=" * 60)

        user = loginWithEmail(email, password)

        print()

        if user:
            print("✅  Login successful!")
            print("🎉  Welcome to the SMS - Shop Management System! \n")

            save = input("💾  Save session? (y/n): ")

            if save.lower() == 'y':
                with open("session.dat", "wb") as f:
                    dump({"email": email, "password": password}, f)
                    
                print("💾  Session saved successfully! ✅\n" + "=" * 60)

        else:
            print("❌  Login failed! Please try again.\n" + "=" * 60)
    
    while True:
        print("\n" + "=" * 60)
        print(" " * 15 + "🛒  SMS - Shop Management System  🛒")
        print("=" * 60)
        print("  [1] 👤  Employee Management")
        print("  [2] 👥  Customer Management")
        print("  [3] 📦  Product Management")
        print("  [4] 🧾  Billing")
        print("  [5] 🚪  Exit")
        print("=" * 60)
        
        choice = input(">")

        if choice == '1':
            while True:
                print("\n" + "=" * 60)
                print(" " * 15 + "👤  Employee Management")
                print("=" * 60)
                print("  [1] ➕  Create Employee")
                print("  [2] ✏️  Update Employee")
                print("  [3] 👀  View Employees")
                print("  [4] ❌  Delete Employee")
                print("  [5] 🔙  Back")
                print("=" * 60)

                choice = input(">")

                if choice == '1':
                    print("\nPlease enter the following details to create a new employee:")
                    first_name = input("📝  First Name: ").capitalize()
                    last_name = input("📝  Last Name: ").capitalize()
                    email = input("📧  Email: ")
                    phone = input("📞  Phone: ")
                    password = input("🔑  Password: ")

                    createEmployee(first_name, last_name, email, phone, password)

                    print("✅  Employee created successfully! 🎉\n" + "=" * 60)

                elif choice == '2':
                    print("\n" + "=" * 60)
                    print(" " * 15 + "✏️  Update Employee")
                    print("=" * 60)

                    employeeId = input("🆔  Employee ID: ")

                    employee = viewEmployee(employeeId)

                    if not employee:
                        print("❌  Employee not found!")
                        continue

                    print("\nℹ️  Leave empty to keep current value.\n")

                    first_name = input(f"📝  First Name ({employee[1]}): ").capitalize()
                    last_name = input(f"📝  Last Name ({employee[2]}): ").capitalize()
                    email = input(f"📧  Email ({employee[3]}): ")
                    phone = input(f"📞  Phone ({employee[4]}): ")
                    password = input(f"🔑  Password ({employee[5]}): ")

                    updateEmployee(
                        employeeId,
                        first_name if first_name else None,
                        last_name if last_name else None,
                        email if email else None,
                        phone if phone else None,
                        password if password else None,
                    )

                    print("✅  Employee updated successfully! 🎉\n" + "=" * 60)

                elif choice=='3':
                    for i in viewEmployees():
                        print(f"🆔 {i[0]} | 👤 {i[1]} {i[2]} | 📧 {i[3]} | 📱 {i[4]} | 🔑 {i[5]}")
                
                elif choice=='4':
                    employeeId = input("🆔  Employee ID: ")
                    
                    employee = viewEmployee(employeeId)

                    if not employee:
                        print("❌  Employee not found!")
                        continue

                    confirm = input(f"⚠️  Are you sure you want to delete {employee[1]} {employee[2]}? (y/n)> ")
                    
                    if confirm.lower() != 'y':
                        print("ℹ️  Aborting deletion...")
                        continue

                    deleteEmployee(employeeId)
                    
                    print("✅  Employee deleted successfully! 🎉\n" + "=" * 60)

                elif choice=='5':
                    print("🔙  Returning to main menu...")
                    break

        elif choice == '2':
            while True:
                print("\n" + "=" * 60)
                print(" " * 15 + "👥  Customer Management")
                print("=" * 60)
                print("  [1] ➕  Create Customer")
                print("  [2] ✏️  Update Customer")
                print("  [3] 👀  View Customers")
                print("  [4] ❌  Delete Customer")
                print("  [5] 🔙  Back")
                print("=" * 60)

                choice = input(">")

                if choice == '1':
                    print("\nPlease enter the following details to create a new customer:")
                    first_name = input("📝  First Name: ").capitalize()
                    last_name = input("📝  Last Name: ").capitalize()
                    phone = input("📞  Phone: ")

                    createCustomer(first_name, last_name, phone)

                    print("✅  Customer created successfully! 🎉\n" + "=" * 60)

                elif choice == '2':
                    print("\n" + "=" * 60)
                    print(" " * 15 + "✏️  Update Customer")
                    print("=" * 60)

                    customerId = input("🆔  Customer ID: ")

                    customer = viewCustomer(customerId)

                    if not customer:
                        print("❌  Customer not found!")
                        continue

                    print("\nℹ️  Leave empty to keep current value.\n")

                    first_name = input(f"📝  First Name ({customer[1]}): ").capitalize()
                    last_name = input(f"📝  Last Name ({customer[2]}): ").capitalize()
                    phone = input(f"📞  Phone ({customer[3]}): ")

                    updateCustomer(
                        customerId,
                        first_name if first_name else None,
                        last_name if last_name else None,
                        phone if phone else None
                    )

                    print("✅  Customer updated successfully! 🎉\n" + "=" * 60)

                elif choice=='3':
                    for i in viewCustomers():
                        print(f"🆔 {i[0]} | 👤 {i[1]} {i[2]} | 📞 {i[3]}")
                
                elif choice=='4':
                    customerId = input("🆔  Customer ID: ")
                    
                    customer = viewCustomer(customerId)

                    if not customer:
                        print("❌  Customer not found!")
                        continue

                    confirm = input(f"⚠️  Are you sure you want to delete {customer[1]} {customer[2]}? (y/n)> ")
                    
                    if confirm.lower() != 'y':
                        print("ℹ️  Aborting deletion...")
                        continue

                    deleteCustomer(customerId)
                    
                    print("✅  Customer deleted successfully! 🎉\n" + "=" * 60)

                elif choice=='5':
                    print("🔙  Returning to main menu...")
                    break

        elif choice == '3':
            while True:
                print("\n" + "=" * 60)
                print(" " * 15 + "📦  Product Management")
                print("=" * 60)
                print("  [1] ➕  Create Product")
                print("  [2] ✏️  Update Product")
                print("  [3] 👀  View Products")
                print("  [4] ❌  Delete Product")
                print("  [5] 🔙  Back")
                print("=" * 60)

                choice = input(">")

                if choice == '1':
                    print("\nPlease enter the following details to create a new product:")
                    name = input("📝  Name: ")
                    stock = input("📦  Stock: ")
                    cost = input("💲  Cost: ")
                    price = input("🏷️  Price: ")

                    createProduct(name, stock, cost, price)

                    print("✅  Product created successfully! 🎉\n" + "=" * 60)

                elif choice == '2':
                    print("\n" + "=" * 60)
                    print(" " * 15 + "✏️  Update Product")
                    print("=" * 60)

                    productId = input("🆔  Product ID: ")

                    product = viewProduct(productId)

                    if not product:
                        print("❌  Product not found!")
                        continue

                    print("\nℹ️  Leave empty to keep current value.\n")

                    name = input(f"📝  Name ({product[1]}): ")
                    stock = input(f"📦  Stock ({product[2]}): ")
                    cost = input(f"💲  Cost ({product[3]}): ")
                    price = input(f"🏷️  Price ({product[4]}): ")

                    updateProduct(
                        productId,
                        name if name else None,
                        stock if stock else None,
                        cost if cost else None,
                        price if price else None
                    )

                    print("✅  Product updated successfully! 🎉\n" + "=" * 60)

                elif choice == '3':
                    print("\n" + "=" * 60)
                    print(" " * 15 + "👀  View Products")
                    print("=" * 60)
                    for i in viewProducts():
                        print(f"🆔 {i[0]} | 📝 {i[1]} | 📦 {i[2]} | 💲 {i[3]} | 🏷️ {i[4]}")
                    print("=" * 60)

                elif choice == '4':
                    productId = input("🆔  Product ID: ")

                    product = viewProduct(productId)

                    if not product:
                        print("❌  Product not found!")
                        continue

                    confirm = input(f"⚠️  Are you sure you want to delete {product[1]}? (y/n)> ")

                    if confirm.lower() != 'y':
                        print("ℹ️  Aborting deletion...")
                        continue

                    deleteProduct(productId)

                    print("✅  Product deleted successfully! 🎉\n" + "=" * 60)

                elif choice == '5':
                    print("🔙  Returning to main menu...")
                    break

        elif choice == '4':
            while True:
                print("\n" + "=" * 60)
                print(" " * 15 + "🧾  Billing")
                print("=" * 60)
                print("  [1] ➕  Create Bill")
                print("  [2] 👀  View Bill")
                print("  [3] ❌  Delete Bill")
                print("  [4] 🔙  Back")
                print("=" * 60)

                choice = input(">")

                if choice == '1':
                    products = {}

                    while True:
                        productId = input("🆔  Product ID (Leave empty to exit): ")

                        if productId == '':
                            break

                        product = viewProduct(productId)

                        if not product:
                            print("❌  Product not found!")
                            continue

                        print(f"📦  Product: {product[1]}")

                        try:
                            quantity = int(input("🔢  Quantity: "))
                        except ValueError:
                            print("❌  Invalid quantity! Please enter a number.")
                            continue

                        if product[2] < quantity:
                            print(f"⚠️  Insufficient stock! Available stock: {product[2]}")
                            continue

                        products[productId] = {
                            "quantity": quantity,
                        }

                        print(f"✅  {product[1]} x{quantity} added to bill.")

                    subtotal = calculateTotal(products)
                    print(f"💰  Total: ${subtotal:.2f}")

                    method = input("💳  Payment Method (Cash/UPI/Card): ").lower()
                    method = "Cash" if method not in ['cash', 'upi', 'card'] else method.capitalize()

                    phone = input("📞  Customer's phone: ")

                    while not phone:
                        print("❌  Please enter a valid customer phone number.")
                        phone = input("📞  Customer's phone: ")

                    customers = findByPhone(phone)

                    if not customers:
                        print("👤  Customer not found! Please create a new customer.")
                        
                        first_name = input("📝  First Name: ").capitalize()
                        last_name = input("📝  Last Name: ").capitalize()
                        
                        customerId = createCustomer(first_name, last_name, phone)
                        
                        print("✅  Customer created successfully! 🎉")

                    elif len(customers) > 1:
                        print("👥  Multiple customers found with this phone number. Please select one:")
                        
                        for c in customers:
                            print(f"🆔 {c[0]} | 👤 {c[1]} {c[2]} | 📞 {c[3]}")
                        
                        customerId = input("🆔  Customer ID: ")

                        if not any(c[0] == int(customerId) for c in customers):
                            print("❌  Invalid Customer ID! Aborting bill creation.")
                            continue

                    else:
                        customerId = customers[0][0]
                        print(f"✅  Customer found: {customers[0][1]} {customers[0][2]}")

                    # Retrieve available points from user
                    cursor.execute("SELECT points FROM Customers WHERE id = %s", (customerId,))
                    available_points = cursor.fetchone()[0]

                    print(f"⭐  Customer has {available_points} points available.")

                    points_to_redeem = None

                    while points_to_redeem is None:
                        points_input = input("🎁  Points to redeem (Leave empty for 0): ")
                        points_to_redeem = int(points_input) if points_input.isdigit() else 0

                        if points_to_redeem > available_points:
                            print("❌  Insufficient points! Please enter a valid amount.")
                            points_to_redeem = None

                        elif points_to_redeem > subtotal:
                            print("❌  Points exceed bill total! Please enter a valid amount less than or equal to subtotal.")
                            points_to_redeem = None

                    bill = createBill(customerId, products, points_to_redeem, method, user[0])

                    print("🧾  Bill created successfully!")
                    print(bill)

                elif choice == '2':
                    billId = input("🧾  Bill ID: ")

                    bill = viewBill(billId)

                    if not bill:
                        print("❌  Bill not found!")
                        continue

                    print("🧾  Bill Details:")
                    print(bill)

                elif choice == '3':
                    billId = input("🧾  Bill ID: ")
                    
                    bill = viewBill(billId)

                    print("🧾  Bill Details:")
                    print(bill)
                    
                    if bill == "Bill not found.":
                        continue

                    confirm = input(f"⚠️  Are you sure you want to delete bill #{billId}? (y/n)>")
                    
                    if confirm.lower() != 'y':
                        print("ℹ️  Aborting...")
                        continue

                    deleteBill(billId)
                    
                    print("✅  Bill deleted successfully! 🎉")

                elif choice=='4':
                    print("🔙  Returning to main menu...")
                    break

        elif choice == '5':
            print("🚪  Exiting SMS - Shop Management System...")

            logout = input("🔒  Logout and clear session? (y/n): ")

            if logout.lower() == 'y':
                remove("session.dat")
                print("💾  Session cleared! ✅")

            print("👋  Goodbye! Have a great day! 🎉")
            exit()

        else:
            print("❌  Invalid choice! Please select a valid option.")