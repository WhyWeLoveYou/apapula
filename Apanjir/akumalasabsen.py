import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import schedule
import time

login_data = [
    {'username': '0063500607@smkn2-solo.net', 'password': 'ALIFM989', 'chat_id': '1558047516', 'name': 'Yodha'},
    {'username': '0063500607@smkn2-solo.net', 'password': 'ALIFM989', 'chat_id': '955560398', 'name': 'Alif'},
    # {'username': 'another_user@smkn2-solo.net', 'password': 'ANOTHER_PASSWORD', 'chat_id': '1558047516', 'name': 'Yodha'}
]

def loginwak(username, password, chat_id, name):
    url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
    loginnya = {
        'userName': username,
        'password': password
    }
    url2 = 'https://siswa.smkn2solo.online/pages/classroom/_hari_ini.php'

    session = requests.Session()
    session.post(url, data=loginnya)

    response = session.get(url2)

    soup = BeautifulSoup(response.text, 'html.parser')

    enroll_links = soup.find_all('a', href=True)
    for link in enroll_links:
        if 'enroll.php' in link['href']:
            enroll_url = 'https://siswa.smkn2solo.online/pages/classroom/' + link['href']
            enroll_response = session.get(enroll_url)
            print(f"berhasil absen {name}")
            send_telegram_message(f"Sudah absen {name}", chat_id)

def send_telegram_message(message, chat_id):
    TOKEN = '7599069172:AAE6ssUUgzJ1Qk4hTrcjZxMrrzpXp2NBrPc'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)

local_tz = pytz.timezone('Asia/Jakarta')

for hour in range(9, 22):
    local_time = datetime.now(local_tz).replace(hour=hour, minute=0, second=0, microsecond=0)
    for credentials in login_data:
                schedule.every().day.at(local_time.strftime("%H:%M")).do(loginwak, credentials['username'], credentials['password'], credentials['chat_id'], credentials['name'])

while True:
    schedule.run_pending()
    time.sleep(1)