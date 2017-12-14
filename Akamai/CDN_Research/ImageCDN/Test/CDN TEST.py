import os
import xlsxwriter
import openpyxl
import urllib.request
import socket
from socket import timeout
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import ssl
import dns.resolver
import whois
import re

try:
    for rdata in dns.resolver.query("image.gmarket.co.kr", "CNAME"):
        cDomain = str(rdata)
        print("    [CNAME 발견] {}".format(cDomain))
except:
    pass