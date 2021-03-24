import requests
from bs4 import BeautifulSoup as bs

link = 'https://kpolyakov.spb.ru/'

response = requests.get(link)

soup = bs(response.text, 'html.parser')

tag_p = soup.find('p', {'class': 'author'})

# for i in tag_p.findChildren(recursive=False):
#     print(i)


print(tag_p)





