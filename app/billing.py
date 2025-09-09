from app import connection, cursor
from app.logistics import viewProduct, fetchPrice

from datetime import datetime
from json import dumps, loads

def calculateTotal(products):
    total = 0

    for product in products.values():
        total += product["price"]

    return total

def createBill(customerId, products, discount, method, cashier):
    subtotal = 0

    for productId, details in products.items():
        details["price"] = float(fetchPrice(productId))
        details["total"] = float(details["price"] * details["quantity"])
        subtotal += details["total"]

    total = subtotal - (subtotal * (discount / 100))

    cursor.execute(
        """
        INSERT INTO Billing(customerId, products, discount, method, cashier, date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (customerId, dumps(products), discount/100, method, cashier, datetime.now())
    )

    connection.commit()

    # remove from stock, quantity
    for productId, details in products.items():
        cursor.execute(
            "UPDATE Products SET stock = stock - %s WHERE id = %s",
            (details["quantity"], productId)
        )

        connection.commit()

    # Build bill string
    # Get bill id and date from the last inserted row
    cursor.execute("SELECT LAST_INSERT_ID(), date FROM Billing ORDER BY id DESC LIMIT 1")
    bill_row = cursor.fetchone()
    bill_id = bill_row[0]
    bill_date = bill_row[1].strftime("%d-%m-%Y") if bill_row[1] else datetime.now().strftime("%d-%m-%Y")

    # Fetch customer details
    cursor.execute("SELECT first_name, last_name, phone FROM Customers WHERE id = %s", (customerId,))
    customer_row = cursor.fetchone()
    customer_name = f"{customer_row[0]} {customer_row[1]}" if customer_row else "Unknown"
    customer_phone = customer_row[2] if customer_row else ""

    # Fetch cashier details
    cursor.execute("SELECT first_name, last_name FROM Employees WHERE id = %s", (cashier,))
    cashier_row = cursor.fetchone()
    cashier_name = f"{cashier_row[0]} {cashier_row[1]}" if cashier_row else str(cashier)

    # Bill header art
    bill_lines = [
        "-" * 52,
        " ▄▄▄ ▄▄▄▄   ▄▄▄ ",
        "▀▄▄  █ █ █ ▀▄▄  ",
        "▄▄▄▀ █   █ ▄▄▄▀ ",
        "-" * 52,
        f"Bill ID: {bill_id}",
        f"Date: {bill_date}",
        "=" * 52
    ]

    row_fmt = "{qty:<3} | {name:<24} | {price:<7} | {total:<7} |"
    header_row = row_fmt.format(qty="Qty", name="Product", price="Price", total="Total")
    bill_lines.append(header_row)

    for productId, details in products.items():
        qty = details["quantity"]
        name = details.get("name", str(viewProduct(productId)[1]))[:24]
        price = f"${details['price']:.2f}"
        total_line = f"${details['total']:.2f}"
        bill_lines.append(row_fmt.format(
            qty=str(qty),
            name=name,
            price=price,
            total=total_line
        ))

    bill_lines.append("-" * 52)
    label_width = 10
    amount_width = 52 - label_width
    bill_lines.append(f"{'Subtotal:':<{label_width}}{f'${subtotal:.2f}':>{amount_width}}")
    bill_lines.append(f"{'Discount:':<{label_width}}{f'{discount}%':>{amount_width}}")
    bill_lines.append(f"{'Total:':<{label_width}}{f'${total:.2f}':>{amount_width}}")
    bill_lines.append("")
    bill_lines.append(f"{'Paid by:':<{label_width}}{method:>{amount_width}}")
    bill_lines.append("")
    bill_lines.append(f"{'Customer:':<{label_width}}{f'{customer_name} ({customer_phone})':>{amount_width}}")
    bill_lines.append(f"{'Cashier:':<{label_width}}{f'{cashier_name} ({cashier})':>{amount_width}}")
    bill_lines.append("")
    bill_lines.append("Thankyou for shopping with us. Please visit again.")

    return "\n".join(bill_lines)

def deleteBill(uid):
    cursor.execute("DELETE FROM Billing WHERE id = %s", (uid,))
    connection.commit()

def viewBill(uid):
    cursor.execute("SELECT * FROM Billing WHERE id = %s", (uid,))
    bill = cursor.fetchone()

    if not bill:
        return "Bill not found."

    customerId = bill[1]
    products = loads(bill[2])
    discount = bill[3] * 100
    method = bill[4]
    cashier = bill[5]

    subtotal = 0

    for productId, details in products.items():
        details["price"] = float(fetchPrice(productId))
        details["total"] = float(details["price"] * details["quantity"])
        subtotal += details["total"]

    total = subtotal - (subtotal * (discount / 100))
    
    # Build bill string
    bill_id = bill[0]
    bill_date = bill[6].strftime("%d-%m-%Y") if bill[6] else datetime.now().strftime("%d-%m-%Y")

    # Fetch customer details
    cursor.execute("SELECT first_name, last_name, phone FROM Customers WHERE id = %s", (customerId,))
    customer_row = cursor.fetchone()
    customer_name = f"{customer_row[0]} {customer_row[1]}" if customer_row else "Unknown"
    customer_phone = customer_row[2] if customer_row else ""

    # Fetch cashier details
    cursor.execute("SELECT first_name, last_name FROM Employees WHERE id = %s", (cashier,))
    cashier_row = cursor.fetchone()
    cashier_name = f"{cashier_row[0]} {cashier_row[1]}" if cashier_row else str(cashier)

    # Bill header art
    bill_lines = [
        "-" * 52,
        " ▄▄▄ ▄▄▄▄   ▄▄▄ ",
        "▀▄▄  █ █ █ ▀▄▄  ",
        "▄▄▄▀ █   █ ▄▄▄▀ ",
        "-" * 52,
        f"Bill ID: {bill_id}",
        f"Date: {bill_date}",
        "=" * 52
    ]

    row_fmt = "{qty:<3} | {name:<24} | {price:<7} | {total:<7} |"
    header_row = row_fmt.format(qty="Qty", name="Product", price="Price", total="Total")
    bill_lines.append(header_row)

    for productId, details in products.items():
        qty = details["quantity"]
        name = details.get("name", str(viewProduct(productId)[1]))[:24]
        price = f"${details['price']:.2f}"
        total_line = f"${details['total']:.2f}"
        bill_lines.append(row_fmt.format(
            qty=str(qty),
            name=name,
            price=price,
            total=total_line
        ))

    bill_lines.append("-" * 52)
    label_width = 10
    amount_width = 52 - label_width
    bill_lines.append(f"{'Subtotal:':<{label_width}}{f'${subtotal:.2f}':>{amount_width}}")
    bill_lines.append(f"{'Discount:':<{label_width}}{f'{discount}%':>{amount_width}}")
    bill_lines.append(f"{'Total:':<{label_width}}{f'${total:.2f}':>{amount_width}}")
    bill_lines.append("")
    bill_lines.append(f"{'Paid by:':<{label_width}}{method:>{amount_width}}")
    bill_lines.append("")
    bill_lines.append(f"{'Customer:':<{label_width}}{f'{customer_name} ({customer_phone})':>{amount_width}}")
    bill_lines.append(f"{'Cashier:':<{label_width}}{f'{cashier_name} ({cashier})':>{amount_width}}")
    bill_lines.append("")
    bill_lines.append("Thankyou for shopping with us. Please visit again.")

    return "\n".join(bill_lines)