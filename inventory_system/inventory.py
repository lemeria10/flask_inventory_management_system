# file to simulate a database using a Python list
# Contains helper functions for CRUD operations

# List to store inventory items
inventory = []
# Auto-increment ID for each new item
current_id = 1

#function to return all inventory items
def get_all_items():
    return inventory

#function to return a single item by ID, or None if not found
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

#function to add new inventory item
def add_item(name, brand, price, stock, barcode):
    global current_id
    item = {
        "id": current_id,
        "name": name,
        "brand": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode
    }

    # Add item to inventory list
    # Increment ID for next item
    inventory.append(item)
    current_id += 1  
    return item

#function to update an existing inventory item
def update_item(item_id, updates):
    item = get_item(item_id)
    if not item:
        return None 
    # Update only the provided fields
    for key, value in updates.items():
        if key in item:
            item[key] = value
    return item

#function to delete an item from inventoy by id
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return True
    return False

def add_from_external_api(product_data, price, stock):
    #Save external API product into inventory
    global current_id

    item = {
        "id": current_id,
        "name": product_data.get("name"),
        "brand": product_data.get("brand"),
        "price": price,
        "stock": stock,
        "barcode": product_data.get("barcode")
    }

    inventory.append(item)
    current_id += 1

    return item