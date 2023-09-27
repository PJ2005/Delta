import requests

data = {
    'sentence': 'Bonjour, comment ça va?',
    'dest_lang': 'en'
}

response = requests.post('http://127.0.0.1:5000/translate', json=data)
print(response.text)

data = {
    'sentence': 'Bonjour, comment ça va?'
}

response = requests.post('http://127.0.0.1:5000/detect', json=data)
print(response.text)
