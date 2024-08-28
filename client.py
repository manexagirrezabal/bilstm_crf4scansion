import requests
import sys

from requests.exceptions import ConnectionError

server = "localhost"
port = 8000

payload = {'inp': sys.argv[1]}

try:
	r = requests.get('http://'+server+':'+str(port)+'/get', params=payload)
	print (r.text)
except ConnectionError:
	print ()