import whois

import re
regex = re.compile(r"https?://(www\.)?")
url = regex.sub("", 'http://www.hyundai-autoever.com')

a = whois.whois(url)
print(a)