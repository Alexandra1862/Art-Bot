

import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('RIJKS_API_KEY')

print(f"🔑 API Key: {api_key[:10]}...")  # Показываем первые 10 символов

# Тестовый запрос
url = "https://www.rijksmuseum.nl/api/en/collection"
params = {
    'key': api_key,
    'q': 'Rembrandt',
    'imgonly': True,
    'ps': 1
}

print("📡 Sending request to Rijksmuseum API...")

response = requests.get(url, params=params)

print(f"📊 Status Code: {response.status_code}")
print(f"📄 Response: {response.text[:500]}...")  # Первые 500 символов

# Попробуем распарсить JSON
try:
    data = response.json()
    print(f"\n✅ Total artworks found: {data.get('count', 0)}")
    if data.get('artObjects'):
        print(f"✅ First artwork: {data['artObjects'][0].get('title')}")
except Exception as e:
    print(f"\n❌ Error parsing JSON: {e}")