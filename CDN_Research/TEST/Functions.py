import os
import xlsxwriter
import openpyxl
import urllib.request
import socket
from socket import timeout
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import ssl
import dns.resolver
import time
import multiprocessing

# 함수 정의 부문
def changeDir():
    os.chdir("C:/Users/yjung/Desktop/Personal/Github/AKAMAI/CDN_Research")

# http://www.xxx.com 형식으로 만들어주는 함수
def full_Url(url):
    # URL이 없다면..
    if(url==None):
        print("[ERROR] URL IS NOT PROVIDED.")
        writeExcel(worksheet, counter, 1, "[ERROR] URL UNPROVIDED")
    else:
        if ("http:" in str(url)):
            full = url
        elif ("https:" in str(url)):
            full = url
        else:
            full = "http://" + url
        print(full, "홈페이지에 접근하고 있습니다.")
        return full

# 웹사이트에서 특정 탭 가져오기
def decode(url):
    request = urllib.request.Request(url)
    #print("1 : ", request)
    temp = urllib.request.urlopen(request, timeout=5)
    #print("2 : ", temp)
    data = temp.read()
    #wwprint("3 : ", data)
    soup = BeautifulSoup(data, "lxml")

    link1 = [element.get("href") for element in soup.find_all("a")]
    link2 = [element.get("src") for element in soup.find_all("script")]
    link3 = [element.get("href") for element in soup.find_all("link")]
    link4 = [element.get("content") for element in soup.find_all("meta")]
    link5 = [element.get("value") for element in soup.find_all("option")]
    result = link1 + link2 + link3 + link4 + link5

    return deleteSameDomain(url, trimUrl(result))

# 같은 URL을 제거해주는 함수
def deleteSameDomain(original, list):
    result = []
    # print(list)

    if(list):
        for element in list:
            if (original == element):
                continue
            if(element=="://"):
                continue
            if (element in original):
                continue
            else:
                result.append(element)
    return result

# 이 키워드가 들어간 도메인은 제거.
blacklist = ["javascript",
             "facebook", "twitter", "instagram", "youtube", "youtu.be",
             "goo.gl", "google", "naver", "tistory", "amazon", "aws", "amazonaws"
             "ad.about", "mailto",
             "linkedin", "slideshare", "github", "flickr", "pinterest",
             "cloudfront", "wordpress", "cisco", "citrix", "netapp"
             "hp.com", "microsoft", "apple", "vimeo", "surveymonkey", "maxcdn",
             "jquery", "symantec", "norton", "cdnetworks", "kakao."
             "ad."]

# 특정 키워드를 포함하는 URL을 제거해주는 함수
def trimUrl (list):
    result = []
    for element in list:
        if(element == None):
            continue
        elif ("http" not in element):
            continue
        elif(element=="://"):
            continue
        for keyword in blacklist:
            if(keyword in element):
                break
        else:
            result.append(element)

    # print("3 : ", result)
    return removeExtra(result)

# 크롤링된 주소에서 불필요한 부분을 제거해주는 함수
def removeExtra(list):
    result = []
    i=1
    for element in list:
        # 약간의 노가다성 및 특별성이 있기는 하지만, 예외적인 사이트 html 코드를 타겟.
        if (";" in element):
            for element in list:
                if(" url=" in element):
                    url = re.search("(?P<url>https?://[^\s]+)", element).group("url")
                    if("lotte" in url):
                        result.append(url)
                    else:
                        removeExtra([url])
                if("action-uri=" in element):
                    url = re.search("(?P<url>https?://[^\s]+)", element).group("url")
                    removeExtra([url])

        else:
            url = urlparse(element)
            if(len(url)>1):
                add = url[0] + "://" + url[1]
                if(add in result):
                    continue
                else:
                    result.append(add)
                    # print("{} 가 추가되었습니다.".format(add))
            i += 1
    return removeSame(result)

# 동일한 결과값을 제거해주는 함수
def removeSame(list):
    result = []
    for i in range(len(list)):
        if(list[i] in result):
            continue
        else:
            result.append(list[i])
    return result

# 엑셀에 작성하는 함수
def writeExcel(file, row, column, content):
    file.write(row, column, content)

# CDN Vendor를 찾아주는 함수
def find_Vendor(cDomain):
    category = {
        "Akamai"                        : [".globalredir.akadns.net", ".akadns.net", ".edgekey.net", ".edgesuite.net", ".akamaiedge.net",".akamai.net"],
        "Level3"                        : [".nstatic.net", ".footprint.net"],
        "Microsoft"                     : [".azurewebsites.net", ".cloudapp.net", ".msecnd.net"],
        "Amazon"                        : [".elb.amazonaws.com", ".amazonaws.com", ".cloudfront.net"],
        "Wix"                           : [".wixdns.net", ".wix.com"],
        "OkServer Internet Solution Inc": [".okserver.cn", "okserver.net"],
        "Cdnetworks"                    : [".gccdn.net", ".cdnetworks.net", ".cdngc.net", ".cdngs.net", ".speedcdn.net", ".cdngl.net", ".cdnga.net"],
        "Limelight Networks"            : [".llnwd.net", ".lldns.net"],
        "Verizon - EdgeCast"            : [".v0cdn.net", ".edgecastcdn.net", ".cedexis.net", ".mucdn.net"],
        "Fastly"                        : [".fastly.net"],
        "CloudFlare"                    : [".cloudflare.net"],
        "Highwinds"                     : [".hwcdn.net"],
        "CDN77(onApp)"                  : [".cdn77.org"],
        "ChinaCache"                    : [".lxsvc.cn", ".ccgslb.com", ".ccna.c3cdn.net"],
        "Yahoo"                         : [".yahoo"],
        "Google"                        : [".google.com", ".doubleclick.net", ".firebaseapp.com"],
        "Mirror Image"                  : [".instacontent.net"],
        "Cachefly"                      : [".cachefly.net"],
        "Coral Cache"                   : [".nyucd.net"],
        "MaxCDN"                        : [".netdna-cdn.com"],
        "NHN Corp."                     : [".navercdn.com", ".nheos.com"],
        "GS Neotek"                     : [".gscdn.net", ".gscdn.com"],
        "LG"                            : [".xcdn.com", ".cdn.cloudn.co.kr"],
        "KT"                            : [".ktics.co.kr"],
        "Hyosung"                       : [".hscdn.com"],
        "Penta Security Systems"        : [".cbricdns.com"],
        "NCIA Sheild Service"           : [".nciashield.org"],
        "Redhat"                        : [".rhcloud.com"],
        "G-Core Labs S.A."              : [".core.pw"],
        "SQUARESPACE"                   : [".squarespace.com"],
        "KINX"                          : [".kinxcdn.com"],
        "Whois Web"                     : [".whoisweb.net"]
    }
    cdn_vendor = list(category.keys())

    for i in range(len(cdn_vendor)):
        for element in category.get(cdn_vendor[i]):
            if(element in cDomain):
                return cdn_vendor[i]


# CNAME 검색 함수
def find_Cname_main(domain):
    try:
        for rdata in dns.resolver.query(domain.strip(), "CNAME"):
            print("    CNAME is detected from {} : {}, CDN vendor is {}".format(domain, str(rdata), find_Vendor(str(rdata))))
            print("")
            writeExcel(worksheet, rownum, 3, find_Vendor(str(rdata)))

            # find_Cname(cDomain[0:len(cDomain) - 1])
    except :
        find_ARecord_main(domain)

def find_ARecord_main(domain):
    try:
        for rdata in dns.resolver.query(domain, "A"):
            print("    CNAME is not detected from {}, IP Address is {}".format(domain, rdata.address))
            print("")
            writeExcel(worksheet, rownum, 3, "-")
    except:
        print("    Can't find DNS Lookup : " + domain)
        print("")
        writeExcel(worksheet, rownum, 3, "-")


def find_Cname_sub(domain):
    try:
        for rdata in dns.resolver.query(domain.strip(), "CNAME"):
            cDomain = str(rdata.target)
            print("    CNAME is detected from {} : {}, CDN vendor is {}".format(domain, cDomain, find_Vendor(cDomain)))
            writeExcel(worksheet, rownum, k + 1, find_Vendor(cDomain))

            # find_Cname(cDomain[0:len(cDomain) - 1])
    except :
        find_ARecord_sub(domain)

def find_ARecord_sub(domain):
    try:
        for rdata in dns.resolver.query(domain, "A"):
            print("    CNAME is not detected from {}, IP Address is {}".format(domain, rdata.address))
            writeExcel(worksheet, rownum, k + 1, "-")
    except:
        print("    Can't find DNS Lookup : " + domain)
        writeExcel(worksheet, rownum, k + 1, "-")


def end():
    input("End of Program. Enter any key to exit.....")
