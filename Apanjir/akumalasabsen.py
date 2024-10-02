import requests 
from requests.auth import HTTPBasicAuth 

session = requests.Session()
  
url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
loginnya = {
    'userName': '0063500607@smkn2-solo.net',
    'password': 'ALIFM989'
}
url2 = 'https://siswa.smkn2solo.online/pages/classroom/_hari_ini.php'

x = session.post(url, data=loginnya)
x2 = session.get(url2)
print(x2.text)