import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dateutil.parser import parse
from requests.adapters import HTTPAdapter, Retry


class Scraper:
    """_summary_
    """    

    BASE = 'https://cryptonews.com'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
    }

    def __init__(self):
        self.news = []

    def run(self):
        """_summary_
        """        

        url = f'{self.BASE}/news'
        response = self._request(url)

        if response.status_code != 200:
            return False

        self._extract(response.content)
        print(self.news)

    def _request(self, url):
        """_summary_

        Args:
            url (str): _description_
        """ 
        
        return self._get_session().get(url)   

    def _extract(self, content): 
        """extract fields from html content

        Args:
            content
        """   

        def _extract_content(article):
            data = {
                'title': None,
                'url': None,
                'timestamp': None
            }

            rgx = re.compile('article__title article__title*')
            atag = article.find('a', {'class': rgx})
            divtag = article.find('div', {'class': 'article__badge-date'})

            if not atag or not divtag:
                return False

            data['title'] = atag.text.strip()
            data['url'] = atag['href']
            data['timestamp'] = parse(divtag['data-utctime'])
            return data
        
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
        articles = soup.find_all('article')

        if len(articles) == 0:
            return False

        for article in articles:
            data = _extract_content(article)
            if not data:
                continue

            self.news.append(data)
        
    def _get_session(
            self,
            retries=3,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            session=None,
    ):
        """Creating a customized requests' session to retry request on a certain condition

        Args:
            retries (int, optional): _description_. Defaults to 3.
            backoff_factor (float, optional): _description_. Defaults to 0.3.
            status_forcelist (tuple, optional): _description_. Defaults to (500, 502, 504).
            session (_type_, optional): _description_. Defaults to None.

        Returns:
            requests.Session()
        """

        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)

        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update(self.HEADERS)
        return session


if __name__ == '__main__':
    obj = Scraper()
    obj.run()