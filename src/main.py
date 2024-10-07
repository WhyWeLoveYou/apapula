import requests
import logging
import json
import schedule
import time
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from message import create_message
import sended

# Mengatur logging
logging.basicConfig(level=logging.INFO)

# Membaca kredensial dari file JSON
with open('user_credentials.json', 'r') as file:
    CREDENSIAL = json.load(file)

# Membaca data yang sudah dikirim
SENDED = [data["link"] for data in sended.get_data()] if sended.get_data() else []

BOT_TOKEN = '7599069172:AAE6ssUUgzJ1Qk4hTrcjZxMrrzpXp2NBrPc'

SESSION = requests.Session()

def loginwak(username, password):
    url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
    loginnya = {
        'userName': username,
        'password': password
    }
    SESSION.post(url, data=loginnya)

    param = {
            "tanggal1": "2024-10-01",
            "tanggal2": "2025-01-06",
            "keyword1": ""
        }
    url2 = 'https://siswa.smkn2solo.online/pages/classroom/_terjadwal.php'
    response = SESSION.post(url2, data=param)
    return response.text

def absen(username, password, chat_id):
    response = loginwak(username, password)
    res = BeautifulSoup(response, 'html.parser')

    enroll_links = res.find_all('tr')
    filter_terjawal = [tr for tr in enroll_links if tr.find('button') and not tr.find('button', string=lambda text: text and 'terjadwal' in text.lower())]
    for row in filter_terjawal:
        td = row.find_all('td')
        link = td[-1].find_all('a', href=True)

        if link:
            link = link[0]['href']
            
            if link not in SENDED:
                date = td[2].get_text(strip=True)
                enroll_link = 'https://siswa.smkn2solo.online/pages/classroom/' + link
                
                response_text = SESSION.get(enroll_link).text
                
                message = create_message(response_text, date, link)
                send_telegram_message(message, chat_id, link, date)            

def send_telegram_message(message, chat_id, link, date):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        logging.info("Pesan berhasil dikirim.")
        sended.save_sended(link, date)
    else:
        logging.error(f"Kesalahan saat mengirim pesan: {response.text}")

def job():
    absen(CREDENSIAL["username"], CREDENSIAL["password"], CREDENSIAL["chat_id"])

def main():
    schedule.every().hour.at(":00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
