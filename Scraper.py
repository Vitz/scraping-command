import time

import requests
from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup


class Scraper():
    def __init__(self, keywords, website):
        self.keywords = keywords
        self.website = website
        self.headers = self._get_headers()
        self.keywords_total_results = []

    def get_urls(self,sleep_time):
        res = self._loop_over_keywords(sleep_time)
        return res

    def get_total_for_keywords(self):
        return self.keywords_total_results

    def _get_headers(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml; q = 0.9, image / webp, * / *;q = 0.8 "}
        return headers

    def _loop_over_keywords(self, sleep_time = 5):
        result = []
        for keyword in self.keywords:
            total, urls = self._google_query(keyword, self.website, self.headers)
            result = result + urls
            self.keywords_total_results.append([keyword, total])
            time.sleep(sleep_time)
        return result

    def _google_query(self, keyword, website, headers):
        from requests_html import HTMLSession
        query = "{} {}".format("site:"+website, keyword)
        q = '+'.join(query.split())
        url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
        print("Connecting:" + url)
        page = ""
        try:
            session = HTMLSession()
            request = session.get(url, headers=headers)
            page = request
        except requests.exceptions.Timeout:
            print("Timeout")
        except requests.exceptions.TooManyRedirects:
            print("Url is incorrect")
        except requests.exceptions.RequestException as e:
            print("Unknown error")
        if page != "":
            return self._parse_results(page)

    def _parse_results(self, res):
        output = []
        total = "none"
        soup = BeautifulSoup(res.text, "html.parser")
        for x in soup.findAll('div', {"class": "tF2Cxc"}):
            url = x.find('a')['href']
            if url and str(self.website).rstrip('/') in url:
                output.append([url])
        try:
            total = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False)
        except Exception as e:
            print("Cant find total, none was received", str(e))
        return total, output
