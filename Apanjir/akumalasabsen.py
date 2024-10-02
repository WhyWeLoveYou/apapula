import requests
from bs4 import BeautifulSoup
import schedule
import time
import pytz
from datetime import datetime

def loginwak():
    session = requests.Session()
    
    url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
    loginnya = {
        'userName': '0063500607@smkn2-solo.net',
        'password': 'ALIFM989'
    }
    url2 = 'https://siswa.smkn2solo.online/pages/classroom/_hari_ini.php'

    session.post(url, data=loginnya)

    response = session.get(url2)

    soup = BeautifulSoup(response.text, 'html.parser')

    enroll_links = soup.find_all('a', href=True)
    for link in enroll_links:
        if 'enroll.php' in link['href']:
            enroll_url = 'https://siswa.smkn2solo.online/pages/classroom/' + link['href']
            enroll_response = session.get(enroll_url)
            print("Sudah absen")

local_tz = pytz.timezone('Asia/Jakarta')

for hour in range(9, 22):
    local_time = datetime.now(local_tz).replace(hour=hour, minute=0, second=0, microsecond=0)
    schedule.every().day.at(local_time.strftime("%H:%M")).do(loginwak)

while True:
    schedule.run_pending()
    time.sleep(1)