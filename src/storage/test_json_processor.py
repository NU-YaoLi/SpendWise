from json_processor import extract_useful_info

# Example OCR output
ocr_json = {
    "store_name": "Supermart",
    "date": "01/03/2025",
    "items": [
        {"name": "Apple", "quantity": "3", "price": 1.2, "extra_field": "noise"},
        {"name": "Banana", "quantity": "2", "price": 0.8},
        {"name": "Watermelon", "price": 5.0}  # Missing quantity
    ],
    "total": "5.6",
    "extra_info": "should be removed"
}

# Run extraction function
processed_data = extract_useful_info(ocr_json)

# Print results
if processed_data:
    print("Processed JSON Data:")
    print(processed_data)
else:
    print("JSON Processing Failed")