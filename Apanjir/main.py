from flask import Flask
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import schedule
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import logging
from markdownify import markdownify as md

# Mengatur logging
logging.basicConfig(level=logging.INFO)

materi_sent = {}


CREDENSIAL = [
    {'username': '0063500607@smkn2-solo.net', 'password': 'ALIFM989', 'chat_id': '955560398', 'name': 'Alif'},#955560398
    {'username': '0079968209@smkn2-solo.net', 'password': 'WW9kaGFBZ2FzdGh5YQ', 'chat_id': '1558047516', 'name': 'Yodha'}
]
BOT_TOKEN = '7599069172:AAE6ssUUgzJ1Qk4hTrcjZxMrrzpXp2NBrPc'

SESSION = requests.Session()

def reset_sent_mapel():
    global materi_sent
    materi_sent = {}
    logging.info("Reset materi_sent at 6 AM")

def loginwak(username, password):
    url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
    loginnya = {
        'userName': username,
        'password': password
    }
    url2 = 'https://siswa.smkn2solo.online/pages/classroom/_hari_ini.php'

    SESSION.post(url, data=loginnya)

    response = SESSION.get(url2)
    return response.text

def getMateri(response):
    soup = BeautifulSoup(response, 'html.parser')
    
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1 and cells[0].get_text(strip=True) == "Isi Materi":
            isi_materi = cells[1].decode_contents()
            return isi_materi

def getTitle(response):
    soup = BeautifulSoup(response, 'html.parser')
    title = soup.find('div', class_='card-header')
    
    return title.get_text(strip=True)

def getAssignment(response):
    soup = BeautifulSoup(response, 'html.parser')
    
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1 and cells[0].get_text(strip=True) == "Tugas Dari Guru":
            isi_materi = cells[1].decode_contents()
            return isi_materi

def absen(username, password, chat_id, name):
    global materi_sent
    response = loginwak(username, password)
    res = BeautifulSoup(response, 'html.parser')
    if username not in materi_sent:
        materi_sent[username] = set() 

    message = ""
    enroll_links = res.find_all('a', href=True)
    for link in enroll_links:
        if 'enroll.php' in link['href']:
            enroll = 'https://siswa.smkn2solo.online/pages/classroom/' + link['href']
            enroll_response = SESSION.get(enroll)
            
            materi = getMateri(enroll_response.text)
            title = getTitle(enroll_response.text)
            assignment = getAssignment(enroll_response.text)
            if materi not in materi_sent[username]:
                materi_sent[username].add(materi)
                message = f"*{title}*\n{'=' * 20}\n{md(materi)}{'=' * 20}\nTugas :\n{md(assignment)}"
                message = message.replace("`","").replace('Powered by [Froala Editor](https://www.froala.com/wysiwyg-editor?pb=1 "Froala Editor")', "")
            else:
                message = "Berhasil Absen"

            send_telegram_message(message, chat_id)    
            logging.info(f"Berhasil absen {name}")
            

def send_telegram_message(message, chat_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message, 'parse_mode' : 'Markdown'}
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        logging.info("Pesan berhasil dikirim.")
    else:
        logging.error(f"Kesalahan saat mengirim pesan: {response.text}")

if __name__ == '__main__':
    schedule.every().day.at("06:00").do(reset_sent_mapel)
    local_tz = pytz.timezone('Asia/Jakarta')
    for hour in range(7, 22):
        for minute in range(0, 60, 1):
            local_time = datetime.now(local_tz).replace(hour=hour, minute=minute, second=0, microsecond=0)
            for i in CREDENSIAL:
                schedule.every().day.at(local_time.strftime("%H:%M")).do(absen, i['username'], i['password'], i['chat_id'], i['name'])
    print("=============================")
    while True:
        schedule.run_pending()
        time.sleep(1)

    # for i in CREDENSIAL:
    #     absen(i['username'], i['password'], i['chat_id'], i['name'])
    #     print("=============================")