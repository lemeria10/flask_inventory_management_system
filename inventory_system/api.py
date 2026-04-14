import requests

# OpenFoodFacts API endpoints
BARCODE_URL = "https://world.openfoodfacts.org/api/v0/product/"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# Required header
HEADERS = {"User-Agent": "inventory-app/1.0 (test@example.com)"}


# Function to fetch product details using barcode
def get_product_by_barcode(barcode):
    try:
        url = f"{BARCODE_URL}{barcode}.json"

        # Send GET request to API
        response = requests.get(url, headers=HEADERS, timeout=5)

        # If request fails, return None
        if response.status_code != 200:
            return None

        data = response.json()

        # If product not found in API
        if data.get("status") != 1:
            return None

        # Extract product details
        product = data.get("product", {})

        # Return only useful fields
        return {
            "name": product.get("product_name"),
            "brand": product.get("brands"),
            "ingredients": product.get("ingredients_text"),
            "barcode": barcode
        }

    except requests.exceptions.RequestException:
        # Handle network/API errors gracefully
        return None
    except Exception:
        # Catch any unexpected error
        return None


# Function to search products by name
def search_product_by_name(product_name):
    try:
        # Query parameters required by OpenFoodFacts
        params = {
            "search_terms": product_name,
            "search_simple": 1,
            "action": "process",
            "json": 1
        }
        # Send request to the api
        response = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()
        results = []

        # Loop through first 5 results only
        for product in data.get("products", [])[:5]:
            results.append({
                "name": product.get("product_name"),
                "brand": product.get("brands"),
                "ingredients": product.get("ingredients_text"),
                "barcode": product.get("code")
            })

        return results

    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None