from flask import Flask, request, jsonify
import inventory
from api import get_product_by_barcode, search_product_by_name
# Initialize Flask app
app = Flask(__name__)
app.json.compact = False  

# Route: GET /inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory.get_all_items())

# Route: GET /inventory/<id>
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    try:
        item = inventory.get_item(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: POST /inventory
@app.route("/inventory", methods=["POST"])
def create_item():
    try:
        data = request.json
        item = inventory.add_item(
            data["name"],
            data["brand"],
            data["price"],
            data["stock"],
            data["barcode"]
        )
        return jsonify(item), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route: PATCH /inventory/<id>
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    try:
        updates = request.json
        item = inventory.update_item(item_id, updates)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route: DELETE /inventory/<id>
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    try:
        success = inventory.delete_item(item_id)
        if not success:
            return jsonify({"error": "Item not found"}), 404
        return jsonify({"message": "Item deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Route: Get Inventory by search
@app.route("/products/search", methods=["GET"])
def search_products():
    try:
        query = request.args.get("q")

        if not query:
            return jsonify({"error": "Missing query"}), 400

        results = search_product_by_name(query)

        if results is None:
            return jsonify({"error": "API error"}), 500

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get product by barcode
@app.route("/products/barcode/<barcode>", methods=["GET"])
def get_by_barcode(barcode):
    try:
        product = get_product_by_barcode(barcode)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(product)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add product to inventory using barcode
@app.route("/inventory/from-barcode/<barcode>", methods=["POST"])
def add_from_barcode(barcode):
    try:
        # Fetch product from external API
        product = get_product_by_barcode(barcode)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.json or {}

        # Add item to local inventory
        item = inventory.add_item(
            product["name"],
            product["brand"],
            data.get("price", 0),
            data.get("stock", 0),
            barcode
        )

        return jsonify(item), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)