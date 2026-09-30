import requests
import json
import urllib3
urllib3.disable_warnings()

api_key = "AQ.Ab8RN6K-uBIW8zBpgAWXwsuEEm8E6EK9Aoj7EEslJ_qouHZvxA"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
models = []

while url:
    res = requests.get(url, verify=False)
    data = res.json()
    if 'models' in data:
        for m in data['models']:
            models.append(m['name'])
    
    if 'nextPageToken' in data:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}&pageToken={data['nextPageToken']}"
    else:
        break

print(json.dumps(models, indent=2))
