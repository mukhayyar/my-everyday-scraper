import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Ganti 'YOUR_BING_API_KEY' dengan kunci API Bing Anda
subscription_key = os.getenv("subscription_key") 

search_url = "https://api.bing.microsoft.com/v7.0/images/search"

# Daftar kategori
categories = [
    "Rumah Tangga", "Audio, Kamera & Elektronik Lainnya", "Buku", "Dapur", "Elektronik",
    "Fashion Anak & Bayi", "Fashion Muslim", "Fashion Pria", "Fashion Wanita", "Film & Musik",
    "Gaming", "Handphone & Tablet", "Ibu & Bayi", "Kecantikan", "Kesehatan", "Komputer & Laptop",
    "Logam Mulia", "Mainan & Hobi", "Makanan & Minuman", "Office & Stationery", "Olahraga",
    "Otomotif", "Perawatan Hewan", "Perawatan Tubuh", "Perlengkapan Pesta", "Pertukangan",
    "Properti", "Tiket, Travel, Voucher"
]

# Membuat folder utama
main_folder = 'Gambar_Kategori'
if not os.path.exists(main_folder):
    os.makedirs(main_folder)

# Fungsi untuk mengunduh gambar
def download_image(url, folder, image_num):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder, f'gambar-{image_num}.jpg'), 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"Error downloading image {image_num} from {url}: {e}")

# Iterasi melalui setiap kategori
for category in categories:
    print(f"Mengunduh gambar untuk kategori: {category}")
    # Membuat folder untuk kategori
    category_folder = os.path.join(main_folder, category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
    
    # Parameter pencarian
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": category, "license": "public", "imageType": "photo", "count": 10}
    
    # Permintaan ke Bing Image Search API
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    
    # Mengunduh gambar
    for i, img in enumerate(search_results["value"]):
        img_url = img["contentUrl"]
        download_image(img_url, category_folder, i+1)
