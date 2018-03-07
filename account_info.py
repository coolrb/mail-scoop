import requests
import json

r = requests.get("https://api.hunter.io/v2/account?api_key=ae4f979860e00b77649e67369a77064e75f58fff")
response_parsed = json.loads(r.text)

print json.dumps(response_parsed, indent=4)
