import inventory


# Reset state before each test
def setup_function():
    inventory.inventory.clear()
    inventory.current_id = 1


def test_add_item():
    item = inventory.add_item("Milk", "Brookside", 120, 10, "111")

    assert item["id"] == 1
    assert item["name"] == "Milk"
    assert item["brand"] == "Brookside"
    assert item["barcode"] == "111"


def test_get_all_items():
    inventory.add_item("Milk", "Brookside", 120, 10, "111")

    items = inventory.get_all_items()

    assert len(items) == 1
    assert isinstance(items, list)


def test_get_item():
    item = inventory.add_item("Sugar", "Mumias", 200, 5, "222")

    result = inventory.get_item(item["id"])

    assert result["name"] == "Sugar"


def test_update_item():
    item = inventory.add_item("Tea", "Kericho Gold", 150, 3, "333")

    updated = inventory.update_item(item["id"], {"price": 999})

    assert updated["price"] == 999


def test_delete_item():
    item = inventory.add_item("Bread", "Toscana", 50, 2, "444")

    result = inventory.delete_item(item["id"])

    assert result is True
    assert inventory.get_item(item["id"]) is None


def test_add_from_external_api():
    product_data = {
        "name": "Coca Cola",
        "brand": "Coke",
        "barcode": "555"
    }

    item = inventory.add_from_external_api(product_data, 100, 20)

    assert item["name"] == "Coca Cola"
    assert item["brand"] == "Coke"
    assert item["barcode"] == "555"