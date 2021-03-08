import requests
from pprint import pprint
import json

url = 'https://api.vk.com/method/groups.get'
params = {
    'user_id': '375232192',
    'access_token': 'f31ca259862bcc94b9b796b35f916c812cbc36efe11142a7dfb47f0bbfc50221ef72ba8b6a6f5a8df613e',
    'extended': '1',
    'v': '5.130',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Accept': '*/*'
}
response = requests.get(url, params=params, headers=headers)
with open('VK_api.json', 'w') as f:
    json.dump(response.json(), f, indent=4)
pprint(response.json())
