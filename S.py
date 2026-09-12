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
]

BASE_COOKIES = {
    'wp_ga4_customerGroup': 'NOT%20LOGGED%20IN',
}

BASE_HEADERS = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://eshop.umniah.com',
    'referer': 'https://eshop.umniah.com/ar/vendic/index/checkotp/',
}

# معلومات البوت
TELEGRAM_BOT_TOKEN = '7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4'
TELEGRAM_CHAT_ID = '6873334348'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# الإعدادات
NUM_THREADS = 1  # خيط واحد (آمن)

def get_random_user_agent():
    """الحصول على User-Agent عشوائي"""
    return random.choice(USER_AGENTS)

def get_headers():
    """الحصول على headers"""
    headers = BASE_HEADERS.copy()
    headers['user-agent'] = get_random_user_agent()
    return headers

def check_phone(phone_number, index, total):
    """فحص رقم واحد"""
    try:
        time.sleep(random.uniform(2, 4))
        
        json_data = {
            'phone_number': phone_number,
            'request': 'generate',
            'orderid': '727165',
        }
        
        headers = get_headers()
        
        response = requests.post(
            'https://eshop.umniah.com/ar/vendic/index/checkotp/', 
            cookies=BASE_COOKIES,
            headers=headers, 
            json=json_data, 
            timeout=15
        )
        
        print(f"[{index}/{total}] {phone_number} - Status: {response.status_code}")
        print(f"[{index}/{total}] {phone_number} - Response: {response.text[:100]}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(f"[{index}/{total}] ✅ JSON صحيح: {response_data}")
                
                # التحقق من النتائج
                if response_data.get('data1') == 'success':
                    print(f"[{index}/{total}] ✅ {phone_number} - يوجد رصيد")
                    return ('success', phone_number, response_data)
                elif 'balance' in str(response_data.get('data2', '')).lower():
                    print(f"[{index}/{total}] ⚠️ {phone_number} - لا يوجد رصيد")
                    return ('no_balance', phone_number, response_data)
                else:
                    print(f"[{index}/{total}] ❓ {phone_number} - رد غير واضح")
                    return ('unknown', phone_number, response_data)
            
            except Exception as e:
                print(f"[{index}/{total}] ❌ {phone_number} - خطأ في JSON: {str(e)}")
                print(f"[{index}/{total}] {phone_number} - Raw: {response.text}")
                return ('json_error', phone_number, None)
        else:
            print(f"[{index}/{total}] ❌ {phone_number} - HTTP {response.status_code}")
            return ('error', phone_number, None)
    
    except Exception as e:
        print(f"[{index}/{total}] ❌ {phone_number} - {str(e)}")
        return ('error', phone_number, None)

def remove_from_file(phone_number):
    """حذف الرقم من الملف"""
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = [line for line in lines if line.strip() != phone_number]
        
        with open('lu1.txt', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return True
    except:
        return False

def main():
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            phone_numbers = [line.strip() for line in f.readlines() if line.strip()]
        
        total = len(phone_numbers)
        
        if total == 0:
            print("ℹ️ لا توجد أرقام!")
            return
        
        print(f"✅ عدد الأرقام: {total}")
        print(f"🔄 خيط واحد فقط (آمن من الحظر)\n")
        
        success_count = 0
        no_balance_count = 0
        failed_count = 0
        
        start_time = time.time()
        
        for idx, phone in enumerate(phone_numbers, 1):
            print(f"\n{'='*50}\n")
            status, phone_num, data = check_phone(phone, idx, total)
            
            if status == 'success':
                success_count += 1
                remove_from_file(phone_num)
            elif status == 'no_balance':
                no_balance_count += 1
                remove_from_file(phone_num)
            else:
                failed_count += 1
                remove_from_file(phone_num)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*50}")
        print(f"✅ يوجد رصيد: {success_count}")
        print(f"❌ لا يوجد رصيد: {no_balance_count}")
        print(f"⚠️ فشل: {failed_count}")
        print(f"⏱️ الوقت: {elapsed_time:.2f} ثانية")
        print(f"{'='*50}\n")

    except FileNotFoundError:
        print("❌ ملف lu1.txt غير موجود!")
    except KeyboardInterrupt:
        print("\n⛔ توقف البرنامج")

if __name__ == "__main__":
    main()
