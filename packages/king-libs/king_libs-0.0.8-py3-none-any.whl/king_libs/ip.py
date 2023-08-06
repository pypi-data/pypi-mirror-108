import requests
from bs4 import BeautifulSoup  as bs
from colorama import init
from colorama import Fore, Back, Style
init()

res = requests.get('https://whatismyip.host/').text
soup = bs(res,'html.parser')
ip = soup.find('p',attrs={'id':'ipv4address'}).text

loc = soup.find('p',attrs={'id':'locationi'}).text

print(Fore.CYAN+"-"*60)
print("\t"*2+Fore.GREEN+"*"*4+ip+"*"*4)
print("\t"*2+Fore.GREEN+"*"*4+loc+"*"*4)

print(Fore.CYAN+"-"*60)
#

