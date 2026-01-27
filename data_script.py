import os
import django
from raw_data import products, customers, suppliers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datas.models import Product, Customer, Supplier

def clear_raw_data():
    try:
        Supplier.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()
        
        print("Clear finish")
        return True
    except Exception as e:
        print(f"Clearing fail: {e}")
        return False

def format_data(raw_data, data_type):
    formated_dataset = []
    try:
        for item in raw_data:
            formated_item = {}
            if data_type == "product":
                formated_item["name"] = item["name"]
                formated_item["price"] = item["price"]
                formated_item["cost"] = item["cost"]
                formated_item["stock"] = int(item["stock"])

            elif data_type == "customer":
                formated_item["name"] = item["name"]
                formated_item["phone"] = item["phone"]
                formated_item["email"] = item["email"]
            
            elif data_type == "supplier":
                formated_item["name"] = item["name"]
                formated_item["phone"] = item["phone"]
                formated_item["email"] = item["email"]
            
            formated_dataset.append(formated_item)
    except Exception:
            print("formated fail")
    return formated_dataset

def import_data(products, customers, suppliers):
    for product in products:
        try:
            Product.objects.get_or_create(
                name=product["name"],
                defaults={"price": product["price"], "cost": product["cost"], "stock": product["stock"]},
            )
        except Exception :
            print("Products import fail")

    for customer in customers:
        try:
            Customer.objects.get_or_create(
                name=customer["name"],
                defaults={'phone':customer["phone"],'email':customer["email"]},
            )
        except Exception:
            print("Customers import fail")

    for supplier in suppliers:
        try:
            Supplier.objects.get_or_create(
                name = supplier["name"],
                defaults={'phone' : supplier["phone"], 'email' : supplier["email"]},
            )
        except Exception:
            print("Suppliers import fail")

def export_data():
    products = Product.objects.all()
    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()


    with open("exported_data.txt", "w", encoding="utf-8") as f:
        f.write("products=[\n")
        for product in products:
            f.write("{"f"Name: {product.name}, Price: {product.price}, Cost: {product.cost}, Stock: {product.stock}""}\n")
        f.write(']\n')
        f.write("customers=[\n")
        for customer in customers:
            f.write("{"f"Name: {customer.name}, Phone: {customer.phone}, Email: {customer.email}""}\n")
        f.write(']\n')
        f.write("suppliers=[\n")
        for supplier in suppliers:
            f.write("{"f"Name: {supplier.name}, Phone: {supplier.phone}, Email: {supplier.email}""}\n")
        f.write(']\n')
    print("Export finish")


if __name__ == "__main__":

    clear_raw_data()
    formated_products = format_data(products, "product")
    formated_customers = format_data(customers, "customer")
    formated_suppliers = format_data(suppliers, "supplier")
    import_data(formated_products,formated_customers,formated_suppliers)
    export_data()