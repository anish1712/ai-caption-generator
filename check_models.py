import requests
import urllib3
urllib3.disable_warnings()

api_key = "AQ.Ab8RN6K-uBIW8zBpgAWXwsuEEm8E6EK9Aoj7EEslJ_qouHZvxA"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
res = requests.get(url, verify=False)
import json
print(json.dumps(res.json(), indent=2))
