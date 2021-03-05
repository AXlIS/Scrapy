import requests
import json
from pprint import pprint

# url = 'https://www.google.ru/'
# response = requests.get(url)


url = 'https://api.github.com/users/BRODYAGA88/repos'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Accept': '*/*'
}
response = requests.get(url, headers=headers)

with open('git_hub.json', 'w') as f:
    json.dump(response.json(), f, indent=4)
