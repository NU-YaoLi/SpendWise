import requests
import os
import json
import re
import time
from PIL import Image
from openai import OpenAI


""" OCR.space API request with local file.
    Python3.5 - not tested on 2.7
:param filename: Your file path & name.
:param overlay: Is OCR.space overlay required in your response.
                Defaults to False.
:param api_key: OCR.space API key.
                Defaults to 'helloworld'.
:param language: Language code to be used in OCR.
                List of available language codes can be found on https://ocr.space/OCRAPI
                Defaults to 'en'.
:return: Result in JSON format.
"""
def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

""" OCR.space API request with remote file.
    Python3.5 - not tested on 2.7
:param url: Image url.
:param overlay: Is OCR.space overlay required in your response.
                Defaults to False.
:param api_key: OCR.space API key.
                Defaults to 'helloworld'.
:param language: Language code to be used in OCR.
                List of available language codes can be found on https://ocr.space/OCRAPI
                Defaults to 'en'.
:return: Result in JSON format.
"""
def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


"""
If `file_path` is larger than max_size_kb, this function compresses
the image until it meets the size requirement or hits a lower quality bound.
"""
# Need more work on this:
def shrink_jpg_if_needed(file_path, max_size_kb=1024):
    max_size_bytes = max_size_kb * 1024  # convert KB to bytes

    # Check current file size
    initial_size = os.path.getsize(file_path)
    if initial_size <= max_size_bytes:
        print(f"File is already under {max_size_kb} KB.\n")
        return

    print(f"Original file size: {initial_size} bytes. Compressing...")

    # Load the image
    img = Image.open(file_path)

    # We'll try decreasing quality in steps until under the limit or quality < 10
    quality = 90
    temp_path = file_path + ".temp"

    while True:
        # Save to a temp file with current quality
        img.save(temp_path, "JPEG", optimize=True, quality=quality)

        # Check the new size
        new_size = os.path.getsize(temp_path)
        if new_size <= max_size_bytes or quality < 10:
            # Replace the original file with the compressed one
            os.replace(temp_path, file_path)
            print(f"Shrunk file to {new_size} bytes (quality={quality}).\n")
            break
        else:
            # Lower the quality further and try again
            quality -= 5

# Replace all space+newline to a space only since there will be a lot of newlines in a receipt.
def replace_newlines(obj):
    if isinstance(obj, str):
        # If it's a string, replace \r\n with whatever you want:
        # e.g. a single space:
        return obj.replace('\\r\\n', ' ')
    else:
        # For any other type (int, float, etc.), just return as is
        return obj


"""-------------------------------------------------------------------------------------------
Below is the first part of code, which extract the plain text from the receipt, using OCRAPI.
----------------------------------------------------------------------------------------------"""

# Input the file path and name
filepath = r'C:\Users\kanto\OneDrive\Desktop\Spring25\AIHackathon\TestPics\pic2.jpg'

# Check if file exists
if os.path.isfile(filepath):
    print(f"File exists at: {filepath}")
else:
    raise Exception(f"File does not exist at: {filepath}")


# Check if file is exceed 1024KB
shrink_jpg_if_needed(filepath, max_size_kb=1024)


# Get the result from API
test_file = ocr_space_file(filename=filepath, language='eng')
test_file = replace_newlines(test_file)

#print(test_file)


# Find the content the following workflow needs.
pattern = r'ParsedText":"(.*?)","ErrorMessage'
#pattern = r'ParsedText\\":\\"(.*?)\\",\\"ErrorMessage'

match = ''
match = re.search(pattern, test_file)
if match:
    extracted_text = match.group(1)
    print("Extracted text:\n", extracted_text)
else:
    raise Exception("No matching text found.")

# The extracted_text is now str datatype
#print(type(extracted_text))
#<class 'str'>


"""----------------------------------------------------------------------------------------------------
Below is the second part of the code, which output a backend consumable json, using google gemini API.
-------------------------------------------------------------------------------------------------------"""

# The chatbot prompt we gonna use in the API request

item_category = """
In all future tasks, item categories must be strictly selected from the predefined list of categories below. No additional categories should be created, and all items must be classified under one of the existing categories.
If an item appears to belong to multiple categories, choose the most relevant one based on its primary function or use. If necessary, provide a brief explanation of the categorization.
1. Food & Drink
2. Household
3. Electronics & Gadgets
4. Clothing & Accessories
5. Beauty & Personal Care
6. Health & Wellness
7. Automotive & Transportation
8. Office & Stationery
9. Sports & Outdoor
10. Toys & Games
11. Pet Supplies
12. Baby & Maternity
13. Books, Media & Entertainment
14. Travel & Luggage
15. Industrial & Construction
16. Real Estate & Property
17. Miscellaneous\n
"""

chatbot_prompt = """
Make sure always generate a json format output in any circumstance.
Extract structured information from the following receipt text and format it as JSON. Ensure the JSON output follows this structure: 
1. **where_I_buy**  
   - Extract and validate the following:  
     - address (use the full address as printed on the receipt).  
     - store_name (Find the store name associated with that precise address via google map; if no match, set `"store_name": "Unknown").  
     - phone_number (if not found, set `"phone_number": Unknown`).  
2. **when_I_buy**  
   - Extract and standardize the following:  
     - date (convert to `mm/dd/yy` format).  
     - time (convert to 24-hour format ).  
3. **what_I_buy** (as a list of items)  
   - Extract and format each item with:  
     - item_name (full name exactly as printed on the receipt).  
     - item_category (if not explicitly stated, categorize using the predefined list of approved categories. The numbers in front of the categories are for reference only and should not be included in the JSON output).  
     - quantity (can be an integer or decimal if measured by weight).  
     - price_for_each (float, representing the price per unit).  
     - total_price (float, calculated as `quantity * price_for_each`).  
4. **how_much_I_spend**  
   - Extract and ensure numerical consistency for:  
     - subtotal (float, sum of all item prices, excluding tax).  
     - tax (float, amount charged as tax).  
     - total (float, final amount paid including tax).  

**JSON Output Format Example:**
{
  "where_I_buy": {
    "address": "302 NE Northgate Way, Seattle, Washington 98125",
    "store_name": "Target",
    "phone_number": "206-494-0897"
  },
  "when_I_buy": {
    "date": "03/02/25",
    "time": "13:00"
  },
  "what_I_buy": [
    {
      "item_name": "BAUSCH & LOMB",
      "item_category": "Health & Beauty",
      "quantity": 2,
      "price_for_each": 5.39,
      "total_price": 10.78
    }
  ],
  "how_much_I_spend": {
    "subtotal": 10.78,
    "tax": 1.12,
    "total": 11.90
  }
}\n"""


# Send the request to chatbot API and get the result


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

start_time = time.time()

while True:
    completion = client.chat.completions.create(
      extra_headers={},
      extra_body={},
      model="google/gemini-2.0-pro-exp-02-05:free",
      messages=[
        {
          "role": "user",
          "content": item_category + chatbot_prompt + extracted_text # Send prompt and the receipt extracted content as an API request 
        }
      ]
    )
    gemini_result = (completion.choices[0].message.content)
    if not all(key in gemini_result for key in ["where_I_buy", "when_I_buy", "what_I_buy", "how_much_I_spend"]):
        print("Error happens during the output generation, retrying...")
    else:
        # Trim the result to strictly follow the json format
        start_index = gemini_result.index("{")
        end_index = gemini_result.rindex("}") + 1  # +1 so we include the '}' itself
        json_result = gemini_result[start_index:end_index]
        break;


running_time = time.time() - start_time
print(f"Total runtime: {running_time:.2f} seconds\n")
# Model running time records:
# deepseek/deepseek-r1:free: 45s; acc 1/1
# google/gemini-2.0-flash-lite-preview-02-05:free: 2s; acc 1/1
# google/gemini-2.0-pro-exp-02-05:free: 3s; acc 1/1

#print(type(json_reult)) #<class 'str'>
print(json_result)