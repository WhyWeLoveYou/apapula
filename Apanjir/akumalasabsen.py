import requests 
from requests.auth import HTTPBasicAuth 
  
x = requests.get('https://siswa.smkn2solo.online/pages/auth/')
  
print(x.text)