import urllib.request
from bs4 import BeautifulSoup
url = "www.goodjoon.com"
full = "https://www.whois.com/whois/" + url
request = urllib.request.Request(full)
data = urllib.request.urlopen(request).read()
#print(data)
soup = BeautifulSoup(data, "lxml")
content = soup.select('div > pre.df-raw')[0].text


for i in range(len(content)):
    print(content[i], end="")


