import os
import requests
import json

# Replace with your imgbb API key
API_KEY = "a818e1c105d4ad0fa46f04cf1e30c957"
API_URL = "https://api.imgbb.com/1/upload"

# Main folder containing all category folders
MAIN_FOLDER = "Gambar_Kategori"

# Function to upload an image to imgbb
def upload_image(image_path):
    with open(image_path, "rb") as image_file:
        payload = {
            "key": API_KEY,
            "expiration": 600,
        }
        files = {
            "image": image_file
        }
        response = requests.post(API_URL, data=payload, files=files)
        if response.status_code == 200:
            return response.json().get("data", {}).get("url")
        else:
            print(f"Failed to upload {image_path}: {response.text}")
            return None

# Dictionary to store image URLs for each category
uploaded_images = {}

# Iterate over each category folder
for category in os.listdir(MAIN_FOLDER):
    category_path = os.path.join(MAIN_FOLDER, category)
    if os.path.isdir(category_path):
        print(f"Uploading images for category: {category}")
        uploaded_images[category] = []
        
        # Iterate over images in the category folder
        for image_file in os.listdir(category_path):
            image_path = os.path.join(category_path, image_file)
            if os.path.isfile(image_path) and image_file.lower().endswith((".png", ".jpg", ".jpeg")):
                image_url = upload_image(image_path)
                if image_url:
                    uploaded_images[category].append({"file_name": image_file, "url": image_url})

# Save the uploaded images to a JSON file
output_file = "uploaded_images.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(uploaded_images, json_file, indent=4)

print(f"Upload completed. Results saved to {output_file}.")
