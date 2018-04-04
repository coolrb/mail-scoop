import requests
import json

r = requests.get("https://api.hunter.io/v2/account?api_key=")
response_parsed = json.loads(r.text)

print json.dumps(response_parsed, indent=4)
