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
    row_fmt = "{qty:<3} | {name:<24} | {price:<7} | {total:<7} |"
    header_row = row_fmt.format(qty="Qty", name="Product", price="Price", total="Total")
    row_width = len(header_row)
    sep_dash = "-" * row_width
    sep_eq = "=" * row_width

    bill_lines = []
    bill_lines.append(sep_dash)
    bill_lines.append(f"{'SMS Bill:':<{row_width}}")
    bill_lines.append(f"{('Cashier: ' + cashier):<{row_width}}")
    bill_lines.append(sep_eq)
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

    bill_lines.append(sep_dash)
    # Align totals to the right edge of the bill
    label_width = 10
    amount_width = row_width - label_width
    bill_lines.append(f"{'Subtotal:':<{label_width}}{f'${subtotal:.2f}':>{amount_width}}")
    bill_lines.append(f"{'Discount:':<{label_width}}{f'{discount}%':>{amount_width}}")
    bill_lines.append(f"{'Total:':<{label_width}}{f'${total:.2f}':>{amount_width}}")

    return "\n".join(bill_lines)

def deleteBill(uid):
    cursor.execute("DELETE FROM Billing WHERE id = %s", (uid,))
    connection.commit()

def viewBill(uid):
    cursor.execute("SELECT * FROM Billing WHERE id = %s", (uid,))
    bill = cursor.fetchone()

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
    
    row_fmt = "{qty:<3} | {name:<24} | {price:<7} | {total:<7} |"
    header_row = row_fmt.format(qty="Qty", name="Product", price="Price", total="Total")
    row_width = len(header_row)
    sep_dash = "-" * row_width
    sep_eq = "=" * row_width

    bill_lines = []
    bill_lines.append(sep_dash)
    bill_lines.append(f"{'SMS Bill:':<{row_width}}")
    bill_lines.append(f"{('Cashier: ' + cashier):<{row_width}}")
    bill_lines.append(sep_eq)
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

    bill_lines.append(sep_dash)
    # Align totals to the right edge of the bill
    label_width = 10
    amount_width = row_width - label_width
    bill_lines.append(f"{'Subtotal:':<{label_width}}{f'${subtotal:.2f}':>{amount_width}}")
    bill_lines.append(f"{'Discount:':<{label_width}}{f'{discount}%':>{amount_width}}")
    bill_lines.append(f"{'Total:':<{label_width}}{f'${total:.2f}':>{amount_width}}")

    return "\n".join(bill_lines)