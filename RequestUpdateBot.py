import requests

url = "https://api.telegram.org/bot2132120189:AAFvTPc0MpGBJWbdOecU2i8oUso6bzDCRIw/getUpdates"

payload = {
    "offset": None,
    "limit": None,
    "timeout": None
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)