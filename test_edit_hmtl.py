
from Settings import *

# This is added so that many files can reuse the function get_database()
# from ImportContent import *
from googlesearch import search
import requests
import time
import random
import html
import traceback
from bs4 import BeautifulSoup
from Title_fix import Article
from configuration import Configuration
from urllib.parse import urlparse
from requests import get
import time
from SpinService import *
spinService = SpinService()

def replace_attr(soup, from_attr: str, to_attr: str):
    if from_attr in str(soup):
        soup[to_attr] = soup[from_attr]
        del soup[from_attr]

        return soup
    else:
        return soup

userAgents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36','Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',  # This is another valid field
}
def ColabSimple():

    for i in search("Cách trang điểm", tld="com.vn",start=0, num=10,stop=10,pause=1,lang="vi",country="vn"):
        r = requests.get(i,verify=False,timeout=10,headers=headers).content
        article = Article("",keep_article_html=True)
        try:
            r = r.decode("utf-8")
        except:
            continue
        soups = BeautifulSoup(r)
        soups =str(soups)
        article.download(soups)
        article.parse()
        soups = BeautifulSoup(html.unescape(article.article_html))
        for elem in soups.find_all():
            if elem.name not in ["p","h1","h2","h3","h4","img","table","tr","td","ul","li","ol"]:
                elem.unwrap()
        listp = [{"ptag":m,"keywords":"vutrian","language":"vi"} for m in soups.find_all(["p","li","h1","h2","h3","h4"])]
        resultp= []
        for i in listp:
            if i["language"]== "vi":
                resultp.append(spinService.spin_paragraph(i["ptag"],i["keywords"]))
            else:
                resultp.append(spinService.spin_paragraph_en(i["ptag"],i["keywords"]))
        for k1,k2 in zip(listp,resultp):
            k1["ptag"].replace_with(k2)
        print(soups)

        break
ColabSimple()