import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import schedule
import time
import threading

login_data = [
    {'username': '0063500607@smkn2-solo.net', 'password': 'ALIFM989', 'chat_id': '955560398', 'name': 'Alif'},
    {'username': '0079968209@smkn2-solo.net', 'password': 'WW9kaGFBZ2FzdGh5YQ', 'chat_id': '1558047516', 'name': 'Yodha'},
]

sent_mapel = {}
sent_file = {}

def download_file(url, session):
    response = session.get(url)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def send_file_to_telegram(file_path, chat_id):
    TOKEN = '7599069172:AAE6ssUUgzJ1Qk4hTrcjZxMrrzpXp2NBrPc'
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    with open(file_path, 'rb') as file:
        data = {'chat_id': chat_id}
        files = {'document': file}
        response = requests.post(url, data=data, files=files)
    if response.status_code != 200:
        print(f"Failed to send file: {response.text}")
    else:
        print(f"File sent successfully: {response.text}")

def send_telegram_message(message, chat_id):
    TOKEN = '7599069172:AAE6ssUUgzJ1Qk4hTrcjZxMrrzpXp2NBrPc'
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print(f"Message sent successfully: {response.text}")

def reset_sent_mapel():
    global sent_mapel
    global sent_file
    for user in sent_mapel:
        sent_mapel[user] = set()

    for user in sent_file:
        sent_file[user] = set()
    print("Reset sent_mapel at 6 AM")

def loginwak(username, password, chat_id, name):
    global sent_mapel
    global sent_file

    if username not in sent_mapel and username not in sent_file:
        sent_mapel[username] = set()
        sent_file[username] = set()

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
    print(f"Sedang Mencoba")
    for link in enroll_links:
        if 'enroll.php' in link['href']:
            enroll_url = 'https://siswa.smkn2solo.online/pages/classroom/' + link['href']
            enroll_response = session.get(enroll_url)

            # materi
            materi = BeautifulSoup(enroll_response.text, 'html.parser')
            materi_links = materi.find_all('a', href=True)
            mapel = ""
            title_div = materi.find('div', class_='card-header')
            if title_div:
                mapel = title_div.get_text(strip=True)
            for link in materi_links:
                if 'class' in link.attrs and 'fr-file' in link['class']:
                    filemateri = link['href']
                    file_path = download_file(filemateri, session)
                    if mapel not in sent_mapel[username]:
                        send_telegram_message(f"Mapel {mapel} ada materi baru nih {name}", chat_id)
                        sent_mapel[username].add(mapel)
                    if filemateri not in sent_file[username]:
                        send_file_to_telegram(file_path, chat_id)
                        sent_file[username].add(filemateri)
            send_telegram_message(f"Sudah absen {name}", chat_id)

local_tz = pytz.timezone('Asia/Jakarta')
# for hour in range(7, 22):
#     local_time = datetime.now(local_tz).replace(hour=hour, minute=0, second=0, microsecond=0)
#     for i in login_data:
#         schedule.every().day.at(local_time.strftime("%H:%M")).do(loginwak, i['username'], i['password'], i['chat_id'], i['name'])

# schedule.every().day.at("06:58").do(reset_sent_mapel)


for hour in range(7, 22):
    for minute in range(0, 60, 5):
        local_time = datetime.now(local_tz).replace(hour=hour, minute=minute, second=0, microsecond=0)
        for i in login_data:
            schedule.every().day.at(local_time.strftime("%H:%M")).do(loginwak, i['username'], i['password'], i['chat_id'], i['name'])

schedule.every().day.at("06:58").do(reset_sent_mapel)

while True:
    schedule.run_pending()
    time.sleep(1)

# Debug
# for credentials in login_data:
#     loginwak(credentials['username'], credentials['password'], credentials['chat_id'], credentials['name'])