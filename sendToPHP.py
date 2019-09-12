import requests
import time

kode_seri = 'ABCD1234'
massa = 500 

while True:
    ##MENGIRIM DATA KE PHP DENGAN METODE POST
    send = requests.post("http://api-sotrashbin.chiqors.xyz/add_data.php?kode_seri=" + kode_seri + "&massa=" + massa)
