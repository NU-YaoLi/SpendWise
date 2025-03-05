from json_processor import extract_useful_info
from data_storage import init_db, save_to_sqlite

init_db()

ocr_json = {
    "store_name": "Supermart",
    "date": "01/03/2025",
    "items": [
        {"name": "Apple", "quantity": "3", "price": 1.2},
        {"name": "Milk", "quantity": "1", "price": 3.5},
        {"name": "Bread", "quantity": "2", "price": 2.0}
    ],
    "total": "9.9"
}

processed_json = extract_useful_info(ocr_json)

if processed_json:
    save_to_sqlite(processed_json)