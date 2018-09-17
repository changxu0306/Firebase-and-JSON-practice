import requests
import sys

name = sys.argv[1]
for x in name.split():
    x = x.lower()
    url = 'https://inf551-hw1-chang.firebaseio.com/index/'
    url = url + x+ '.json'
    response = requests.get(url)
    print response.text