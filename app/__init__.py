import mysql.connector as mc

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

def start():
    email = input("Enter email: ")
    password = input("Enter password: ")

    if loginWithEmail(email, password):
        print("Login successful!")

        print("Welcome to the SMS - Shop Management System! \n")
        
        while True:
            print('''
[1] Employee Management
[2] Customer Management
[3] Product Management
[4] Billing
[5] Exit
            ''')
            
            choice = input(">")

            if choice == '1':
                while True:
                    print('''
[1] Create Employee
[2] Update Employee
[3] View Employees
[4] Delete Employee
[5] Back
                    ''')

                    choice = input(">")

                    if choice == '1':
                        first_name = input("First Name: ").capitalize()
                        last_name = input("Last Name: ").capitalize()
                        email = input("Email: ")
                        phone = input("Phone: ")
                        password = input("Password: ")

                        createEmployee(first_name, last_name, email, phone, password)

                        print("Employee created successfully!")

                    elif choice == '2':
                        print("Leave empty to keep current value.")

                        employeeId = input("Employee ID: ")

                        employee = viewEmployee(employeeId)

                        if not employee:
                            print("Employee not found!")
                            continue

                        print("Leave empty to keep current value.\n")

                        first_name = input(f"First Name ({employee[1]}): ").capitalize()
                        last_name = input(f"Last Name ({employee[2]}): ").capitalize()
                        email = input(f"Email ({employee[3]}): ")
                        phone = input(f"Phone ({employee[4]}): ")
                        password = input(f"Password ({employee[5]}): ")
                        rating = input(f"Rating ({employee[6]}): ")

                        updateEmployee(
                            employeeId,
                            first_name if first_name else None,
                            last_name if last_name else None,
                            email if email else None,
                            phone if phone else None,
                            password if password else None,
                            rating if rating else None
                        )

                        print("Employee updated successfully!")

                    elif choice=='3':
                        for i in viewEmployees():
                            print(i)
                    
                    elif choice=='4':
                        employeeId = input("Employee ID: ")
                        
                        employee = viewEmployee(employeeId)

                        if not employee:
                            print("Employee not found!")
                            continue

                        confirm = input(f"Are you sure you want to delete {employee[1]} {employee[2]}? (y/n)>")
                        
                        if confirm.lower() != 'y':
                            print("Aborting...")
                            continue

                        deleteEmployee(employeeId)
                        
                        print("Employee deleted successfully!")

                    elif choice=='5':
                        print("Returning to main menu...")
                        break

            elif choice == '2':
                while True:
                    print('''
[1] Create Customer
[2] Update Customer
[3] View Customers
[4] Delete Customer
[5] Back
                    ''')

                    choice = input(">")

                    if choice == '1':
                        first_name = input("First Name: ").capitalize()
                        last_name = input("Last Name: ").capitalize()
                        phone = input("Phone: ")

                        createCustomer(first_name, last_name, phone)

                        print("Customer created successfully!")

                    elif choice == '2':
                        print("Leave empty to keep current value.")

                        customerId = input("Customer ID: ")

                        customer = viewCustomer(customerId)

                        if not customer:
                            print("Customer not found!")
                            continue

                        print("Leave empty to keep current value.\n")

                        first_name = input(f"First Name ({customer[1]}): ").capitalize()
                        last_name = input(f"Last Name ({customer[2]}): ").capitalize()
                        phone = input(f"Phone ({customer[3]}): ")

                        updateCustomer(
                            customerId,
                            first_name if first_name else None,
                            last_name if last_name else None,
                            phone if phone else None
                        )

                        print("Customer updated successfully!")

                    elif choice=='3':
                        for i in viewCustomers():
                            print(i)
                    
                    elif choice=='4':
                        customerId = input("Customer ID: ")
                        
                        customer = viewCustomer(customerId)

                        if not customer:
                            print("Customer not found!")
                            continue

                        confirm = input(f"Are you sure you want to delete {customer[1]} {customer[2]}? (y/n)>")
                        
                        if confirm.lower() != 'y':
                            print("Aborting...")
                            continue

                        deleteCustomer(customerId)
                        
                        print("Customer deleted successfully!")

                    elif choice=='5':
                        print("Returning to main menu...")
                        break

            elif choice == '3':
                while True:
                    print('''
[1] Create Product
[2] Update Product
[3] View Product
[4] Delete Product
[5] Back
                    ''')

                    choice = input(">")

                    if choice == '1':
                        name = input("First Name: ")
                        stock = input("Stock: ")
                        cost = input("Cost: ")
                        price = input("Price: ")

                        createProduct(name, stock, cost, price)

                        print("Product created successfully!")

                    elif choice == '2':
                        print("Leave empty to keep current value.")

                        productId = input("Product ID: ")

                        product = viewProduct(productId)

                        if not product:
                            print("Product not found!")
                            continue

                        print("Leave empty to keep current value.\n")

                        name = input(f"Name ({product[1]}): ")
                        stock = input(f"Stock ({product[2]}): ")
                        cost = input(f"Cost ({product[3]}): ")
                        price = input(f"Price ({product[3]}): ")

                        updateProduct(
                            productId,
                            name if name else None,
                            stock if stock else None,
                            cost if cost else None,
                            price if price else None
                        )

                        print("Product updated successfully!")

                    elif choice=='3':
                        for i in viewProducts():
                            print(i)
                    
                    elif choice=='4':
                        productId = input("Product ID: ")
                        
                        product = viewProduct(productId)

                        if not product:
                            print("Product not found!")
                            continue

                        confirm = input(f"Are you sure you want to delete {product[1]}? (y/n)>")
                        
                        if confirm.lower() != 'y':
                            print("Aborting...")
                            continue

                        deleteProduct(productId)
                        
                        print("Product deleted successfully!")

                    elif choice=='5':
                        print("Returning to main menu...")
                        break

            elif choice == '4':
                while True:
                    print('''
[1] Create Bill
[2] View Bill
[3] Delete Bill
[4] Back
                    ''')

                    choice = input(">")

                    if choice == '1':
                        products = {}

                        while True:
                            productId = input("Product ID (Leave empty to exit): ")

                            if productId == '':
                                break

                            product = viewProduct(productId)

                            if not product:
                                print("Product not found!")
                                continue

                            print(f"Product: {product[1]}")

                            quantity = int(input("Quantity: "))

                            if product[2] < quantity:
                                print("Insufficient stock! Available stock:", product["stock"])
                                continue

                            products[productId] = {
                                "quantity": quantity,
                            }

                            print(product[1], f"x{quantity}", "added to bill.")
                        
                        discount = float(input("Discount (%): "))
                        method = input("Payment Method (Cash/UPI/Card): ")
                        customerId = input("Customer ID: ")

                        bill = createBill(customerId, products, discount, method, "sheldon sinu")

                        print(bill)

                    elif choice == '2':
                        billId = input("Bill ID: ")

                        bill = viewBill(billId)

                        if not bill:
                            print("Bill not found!")
                            continue

                        print(bill)

                    elif choice == '3':
                        billId = input("Bill ID: ")
                        
                        bill = viewBill(billId)

                        if not bill:
                            print("Bill not found!")
                            continue

                        confirm = input(f"Are you sure you want to delete bill #{bill[0]}? (y/n)>")
                        
                        if confirm.lower() != 'y':
                            print("Aborting...")
                            continue

                        deleteBill(billId)
                        
                        print("Bill deleted successfully!")

                    elif choice=='4':
                        print("Returning to main menu...")
                        break

            elif choice == '5':
                print("Exiting...")
                exit()
                
            else:
                print("Invalid choice!")

    else:
        print("Login failed!")