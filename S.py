import requests

cookies = {
    'wp_ga4_customerGroup': 'NOT%20LOGGED%20IN',
    '_gcl_au': '1.1.1488191976.1788724682',
    '_ga': 'GA1.1.1652587676.1788724683',
    '_twpid': 'tw.1788724682629.93328193554679845',
    '_fbp': 'fb.1.1788724682843.15328305795544321',
    'user_allowed_save_cookie': '%7B%221%22%3A1%7D',
    '_gcl_gs': '2.1.k1$i1789060528$u207372039',
    '_gcl_aw': 'GCL.1789060530.CjwKCAjwqonVBhA4EiwA9wYJ3YyDIZw8E10dFgetOqbavQ2J1CzjVz19a-B2WHYqpU-C1ymf6qSXNhoCDbkQAvD_BwE',
    '_ga_2HVEQ4PV6S': 'GS2.1.s1789060530$o10$g1$t1789060626$j31$l0$h919553035',
    '_twsid': '1789060529974-544044261.2.1789060636866',
    'PHPSESSID': 'dogassif0s45n2oif4pholfr9d',
    'X-Magento-Vary': '1c509789687d89a3ada9558f1a9d067ac5aaca38',
    'TS01a52733': '01c9d2e4aee2703320abd06da036a0c62995d45725c66e9914c7e54165d6c0582bfa062601ccd0cb41c6e8ad1a7cc4ece5cd4ed24da2b894934030b616263683de94c84e03347fcbd7aaf2fc68e3e33639f254253bc553a27200258dba6fe063c0d2e9354104dda4e10e0e256191ef32d4c74af2c9',
    'private_content_version': 'f50d67241a05d5cb0479f6a833809efa',
    'TS01131384': '01c9d2e4ae05c090765b48e20a95690eedf87bdf2ace6867d77091690120a8290b61803b8824edfcbd44fd5933813bc3d35be22a0a97fcaf5709d21b6618e59e2aa734969ae7d467d06ebe68c9e3c610c35fd238c196bde6321fe6c27464959191dbe31db06ba1c5cd9a5e9ddae0f67ca830bda8c7',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://eshop.umniah.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
}

# ⚙️ ScraperAPI Configuration
SCRAPER_API_KEY = 'e42b050dcb697cf3ccd3d663edf43aea'
SCRAPER_API_URL = 'https://api.scraperapi.com/'

json_data = {
    'phone_number': '0795087682',
    'request': 'generate',
    'orderid': '727165',
}

# الطريقة 1: استخدام ScraperAPI
print("🔄 جاري الاتصال عبر ScraperAPI...")
payload = {
    'api_key': SCRAPER_API_KEY,
    'url': 'https://eshop.umniah.com/ar/vendic/index/checkotp/',
}

try:
    response = requests.post(
        SCRAPER_API_URL,
        params=payload,
        headers=headers,
        json=json_data,
        timeout=15
    )
    print(f"✅ Status: {response.status_code}")
    print(f"📄 Response:\n{response.text}\n")
except Exception as e:
    print(f"❌ خطأ: {str(e)}\n")

# الطريقة 2: بدون Proxy (للمقارنة)
print("🔄 جاري الاتصال بدون Proxy...")
try:
    response = requests.post(
        'https://eshop.umniah.com/ar/vendic/index/checkotp/', 
        cookies=cookies, 
        headers=headers, 
        json=json_data,
        timeout=15
    )
    print(f"✅ Status: {response.status_code}")
    print(f"📄 Response:\n{response.text}")
except Exception as e:
    print(f"❌ خطأ: {str(e)}")
