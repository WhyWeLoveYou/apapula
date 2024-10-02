import requests 
from requests.auth import HTTPBasicAuth 
  
url = 'https://siswa.smkn2solo.online/pages/auth/checkLogin.php'
loginnya = {
    'username': '0063500607@smkn2-solo.net',
    'password': 'ALIFM989'
}
x = requests.post(url, data=loginnya)
print(x.text)