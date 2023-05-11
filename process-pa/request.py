import requests

url = "http://localhost:8041/smartapp-api/wrapper/diag-codes/search?term=10"

payload = {}
headers = {
    'Origin': 'http://localhost:3000',
    'Cookie': 'SESSION=NzIwYjA2YTktY2ZhYy00OTAzLWE3NzktNGJjY2U3NjQ1NDRh'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
