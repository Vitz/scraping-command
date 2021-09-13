import time

from bs4 import BeautifulSoup


"""
Scraper class is provided for collecting data from Google Search service. 
keywords - keywords to use in query
website - website to use in query
"""
class Scraper():
    def __init__(self, keywords, website):
        self.keywords = keywords
        self.website = website
        self.headers = self._get_headers()
        self.keywords_total_results = []

    """
    Return single list of urls for every keyword. 
    """
    def get_urls(self,sleep_time):
        res = self._loop_over_keywords(sleep_time)
        return res

    """
    Return total quantity for each keyword as list. 
    """
    def get_total_for_keywords(self):
        return self.keywords_total_results

    """
    Return headers for HTTP methods.  
    """
    def _get_headers(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml; q = 0.9, image / webp, * / *;q = 0.8 "}
        return headers

    """
    Get urls for each keywords and given website. Main loop of class. 
    Returns single list of urls of each keywords.
    """
    def _loop_over_keywords(self, sleep_time = 5):
        result = []
        for keyword in self.keywords:
            total, urls = self._google_query(keyword, self.website, self.headers)
            result = result + urls
            self.keywords_total_results.append([keyword, total])
            time.sleep(sleep_time)
        return result

    """
    GET method for Google Search.
    keyword - single keyword
    website - desired website 
    headers - headers with useragent
    Returns single batch of urls (for single keyword).
    """
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
        except Exception as e:
            print("Cant get() method", str(e))
        if page != "":
            return self._parse_results(page)

    """
    Parser HTML to get URLS
    res - result of GET method
    Returns total result and available urls for single keyword. 
    """
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
