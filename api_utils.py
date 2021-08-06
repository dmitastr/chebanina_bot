import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AnecdotRuApi:
    def __init__(self):
        self.random_url = "https://www.anekdot.ru/random/anekdot/"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.api = requests.Session()
        self.api.headers.update(headers)

    def get_random_anecdote(self, offset=1):
        page = self.api.get(self.random_url)
        page_parsed = BeautifulSoup(page.text, "html.parser")
        try:
            anecdote = (
                page_parsed.find_all("div", {"class": "topicbox"})[offset]
                .find("div", {"class": "text"})
                .get_text(separator="\n").strip()
            )
            return anecdote
        except IndexError:
            raise IndexError


class BaneksApi:
    def __init__(self):
        self.random_url = "https://baneks.site/random"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.api = requests.Session()
        self.api.headers.update(headers)

    def get_random_anecdote(self):
        page = self.api.get(self.random_url)
        page_parsed = BeautifulSoup(page.text, "html.parser")
        try:
            anecdote = (
                page_parsed.find("div", {"class": "joke"})
                .find("section", {"itemprop": "description"})
                .find("p")
                .get_text(separator="\n").strip()
            )
            return anecdote
        except:
            raise ValueError


class PiroshkiApi:
    def __init__(self):
        self.random_url = "https://poetory.ru/pir/"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.api = requests.Session()
        self.api.headers.update(headers)

    def get_random_anecdote(self, offset, page_num):
        page = self.api.get(self.random_url+str(page_num))
        page_parsed = BeautifulSoup(page.text, "html.parser")
        try:
            anecdote = (
                page_parsed.find_all("div", {"data-react-class": "Content"})[offset%30]
                .find("div", {"class": "item-text"})
                .get_text(separator="\n").strip()
            )
            return anecdote
        except:
            raise ValueError

if __name__=="__main__":
    logger.info(PiroshkiApi().get_random_anecdote(3, 24))