import requests
import sys

server = "localhost"
port = 8000

payload = {'inp': sys.argv[1]}
r = requests.get('http://'+server+':'+str(port)+'/get', params=payload)
print (r.text)