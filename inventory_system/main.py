import requests
import threading
import time
from app import app
from inventory import add_from_external_api

# Base URL for the flask API
BASE_URL = "http://127.0.0.1:5000"

#Function to run server in background
def run_server():
    app.run(debug=False, use_reloader=False)


#function to display the CLI menu options
def menu():
    print("-"*20)
    print("\nInventory Management")
    print("-"*20)
    print("1. View Inventory")
    print("2. Add Item")
    print("3. Update Item")
    print("4. Delete Item")
    print("5. Search Item (Barcode/Name)")
    print("6. Exit")

# Function to fetch and display all inventory items
def view_inventory():
    # Send GET request to Flask API
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        print(response.json())
    except Exception as e:
        print("Error:", e)

#function to add a product manually via CLI input
def add_item():
    try:
        # Collect product information from user
        name = input("Enter product name: ")
        brand = input("Enter product brand: ")
        price = float(input("Enter product price: "))
        stock = int(input("Enter stock quantity: "))
        barcode = input("Enter product barcode: ")

        data={
            "name": name,
            "brand": brand,
            "price": price,
            "stock": stock,
            "barcode": barcode
        }
        # Send POST request to API to create item
        response = requests.post(f"{BASE_URL}/inventory", json=data)
        print("Item added successfully:", response.json())

    except Exception as e:
        print("Error:", e)

#function to update the price of an existing inventory item
def update_item():
    try:
    # Ask user for item ID
        item_id = input("Enter Product ID: ")
        # Ask for new price
        new_price = float(input("Enter New price: "))
        # Send PATCH request to update the item
        response = requests.patch(
            f"{BASE_URL}/inventory/{item_id}",
            json={"price": new_price}
        )
        print(response.json())
    except Exception as e:
        print("Error:", e)

#function to delete an item from inventory
def delete_item():
    try:
        item_id = input("Enter Product ID: ")
        # Send DELETE request to API
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        print(response.json())
    except Exception as e:
        print("Error:", e)

#function to search for a product using barcode OR product name
def search_product():
    try:
        query = input("Enter barcode OR product name: ").strip()
        # If input is numeric, treat it as a barcode
        if query.isdigit():
            response = requests.get(f"{BASE_URL}/products/barcode/{query}")
            product = response.json()

            if not product or product.get("error"):
                print("Product not found")
                return

            print("\n Product found:")
            print(product)

            price = float(input("Enter price: "))
            stock = int(input("Enter stock quantity: "))

            # Save using clean helper
            saved = add_from_external_api(product, price, stock)

            # Send to Flask API
            requests.post(BASE_URL, json=saved)

            print("\nSaved to inventory:")
            print(saved)
        # treat it as a name search
        else:
            response = requests.get(f"{BASE_URL}/products/search?q={query}")
            results = response.json()

            if not results:
                print("No products found")
                return

            print("\nSearch results:")
            for i, product in enumerate(results):
                print(f"{i+1}. {product['name']} - {product['brand']}")

            choice = int(input("\nSelect product number: ")) - 1
            selected = results[choice]

            print("\nSelected product:")
            print(selected)

            price = float(input("Enter price: "))
            stock = int(input("Enter stock quantity: "))

            # Prepare clean structure
            product_data = {
                "name": selected["name"],
                "brand": selected["brand"],
                "barcode": selected.get("barcode")
            }

            # Save using helper function
            saved = add_from_external_api(product_data, price, stock)

            # Send to Flask API
            requests.post(BASE_URL, json=saved)

            print("\nSaved to inventory:")
            print(saved)

    except Exception as e:
        print("Error:", e)

def run():
    # Start Flask server in background
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    # Wait for server to start
    time.sleep(2)

    while True:
        # Display menu
        menu()
        # Get user choice
        choice = input("Choose option: ")
        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            search_product()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option")


# Start CLI when file runs
if __name__ == "__main__":
    run()