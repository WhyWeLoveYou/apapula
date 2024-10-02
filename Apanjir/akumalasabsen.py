import requests
from bs4 import BeautifulSoup
import schedule
import time
import pytz
from datetime import datetime

def savedCreds():
    return [
        [
            "0079968209@smkn2-solo.net",
            "WW9kaGFBZ2FzdGh5YQ"
        ],
        [
            "0063500607@smkn2-solo.net",
            "ALIFM989"
        ]
    ]

def loginwak():

    session = requests.Session()
    
    url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
    url2 = 'https://siswa.smkn2solo.online/pages/classroom/_hari_ini.php'
    
    for usr in savedCreds():
        data = {
            'username': usr[0],
            'password': usr[1]
        }
        session.post(url, data)

        response = session.get(url2)

        soup = BeautifulSoup(response.text, 'html.parser')

        enroll_links = soup.find_all('a', href=True)
        for link in enroll_links:
            if 'enroll.php' in link['href']:
                enroll_url = 'https://siswa.smkn2solo.online/pages/classroom/' + link['href']
                enroll_response = session.get(enroll_url)
                print(enroll_response.text)

local_tz = pytz.timezone('Asia/Jakarta')

for hour in range(9, 22):
    local_time = datetime.now(local_tz).replace(hour=hour, minute=0, second=0, microsecond=0)
    schedule.every().day.at(local_time.strftime("%H:%M")).do(loginwak)

while True:
    schedule.run_pending()
    time.sleep(1)