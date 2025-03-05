import uuid
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any
from datetime import datetime

# Define receipt structure
class Item(BaseModel):
    name: str
    quantity: int = Field(..., gt=0)  # Ensure quantity > 0
    price: float = Field(..., gt=0)   # Ensure price > 0

class ProcessedReceipt(BaseModel):
    receipt_id: str  # New unique ID
    store_name: str
    date: str
    items: List[Item]
    total: float

def generate_receipt_id() -> str:
    """Generate a unique receipt ID."""
    return f"RCPT-{uuid.uuid4().hex[:8].upper()}"  # Example: RCPT-3F2A1B4C

def clean_date(date_str: str) -> str:
    """ Standardize date format to YYYY-MM-DD """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return "Unknown Date"

def extract_useful_info(json_data: Dict[str, Any]) -> Dict[str, Any]:
    """ Process OCR JSON data, extract and format key fields """
    try:
        # Generate unique receipt ID
        receipt_id = generate_receipt_id()

        # Standardize date format
        json_data["date"] = clean_date(json_data.get("date", "Unknown"))

        # Ensure store_name is not empty
        store_name = json_data.get("store_name", "").strip()
        store_name = store_name if store_name else "Unknown Store"

        # Filter invalid item data
        filtered_items = []
        for item in json_data.get("items", []):
            if "name" in item and "quantity" in item and "price" in item:
                try:
                    filtered_items.append({
                        "name": item["name"].strip(),
                        "quantity": int(item["quantity"]),
                        "price": float(item["price"])
                    })
                except ValueError:
                    continue  # Skip invalid items

        # Calculate total if missing
        total_price = float(json_data.get("total", 0))
        if not total_price:
            total_price = sum(item["quantity"] * item["price"] for item in filtered_items)

        # Construct final structured JSON
        processed_data = {
            "receipt_id": receipt_id,  # Add unique ID
            "store_name": store_name,
            "date": json_data["date"],
            "items": filtered_items,
            "total": round(total_price, 2)
        }

        # Validate final structure using Pydantic
        validated_data = ProcessedReceipt(**processed_data)
        return validated_data.dict()

    except ValidationError as e:
        print("OCR Data Format Error:", e)
        return None