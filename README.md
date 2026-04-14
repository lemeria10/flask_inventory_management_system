📦 Inventory Management System

A simple Flask-based Inventory Management System that allows you to manage products, search items using barcode or name, and integrate with the Open Food Facts API.

🚀 Features
➕ Add inventory items
📋 View all inventory items
🔍 Search items by barcode or product name
✏️ Update inventory items
❌ Delete inventory items
🌍 Fetch product details from Open Food Facts API
🧪 Automated tests using pytest
🏗 Project Structure
inventory_system/
│
├── app.py                  # Flask API routes
├── api.py                  # Open Food Facts API integration
├── inventory.py            # Core inventory logic (in-memory DB)
├── main.py                 # CLI menu (optional interface)
│
├── tests/
│   ├── test_api.py         # Tests for Flask routes
│   ├── test_inventory.py   # Tests for inventory logic
│
├── Pipfile                 # Pipenv environment
├── requirements.txt        # Python dependencies
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/your-username/inventory-system.git
cd inventory-system
2. Create virtual environment (pipenv recommended)
pipenv install
pipenv shell

OR using pip:

pip install -r requirements.txt
3. Run the Flask app
python app.py

Server runs at:

http://127.0.0.1:5000
📡 API Endpoints
📦 Inventory Routes
Get all items
GET /inventory
Get single item
GET /inventory/<id>
Add item
POST /inventory
Update item
PATCH /inventory/<id>
Delete item
DELETE /inventory/<id>
🌍 Product Routes (Open Food Facts)
Search product by name
GET /products/search?q=milk
Get product by barcode
GET /products/barcode/<barcode>
Add product from barcode
POST /inventory/from-barcode/<barcode>
🧪 Running Tests

Run all tests using pytest:

pytest

Expected output:

collected 7 items
tests/test_api.py .
tests/test_inventory.py ......
🧠 How it works
1. Inventory system
Uses a Python list as a temporary database
Each item has:
id
name
brand
price
stock
barcode
2. Open Food Facts API
Fetches real product data using barcode
Example:
https://world.openfoodfacts.org/api/v0/product/5449000000996.json
3. Testing system
Uses pytest
Tests both:
Flask API routes
Inventory logic functions
🛠 Tech Stack
Python 3.8+
Flask
Requests
Pytest
Open Food Facts API
📌 Example Usage
Add item
POST /inventory
{
  "name": "Milk",
  "brand": "Brookside",
  "price": 120,
  "stock": 10,
  "barcode": "123456"
}
Search product
GET /products/search?q=milk
📚 Learning Goals

This project helps you understand:

REST API development with Flask
CRUD operations
External API integration
Unit testing with pytest
Basic backend architecture
🚀 Future Improvements
Use SQLite or PostgreSQL instead of in-memory list
Add authentication (login system)
Add frontend UI (React or HTML)
Dockerize the application
Deploy to cloud (Render / Railway)
👨‍💻 Author
Nicholas Shayo

Built as a learning project for mastering:

Backend development
APIs
Testing
Git workflows
⭐ If you like this project

Feel free to:

⭐ Star the repo
🍴 Fork it
🚀 Improve it
