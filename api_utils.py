import logging
import requests
import json
from bs4 import BeautifulSoup
import random
import re

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
            tags = page_parsed.find("div", {"class": "joke"}).find("section", {"itemprop": "description"}).find_all()
            anecdote = "\n".join(
                tag.get_text(separator="\n").strip() for tag in tags
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


class RedditMemeApi:
    def __init__(self):
        self.random_url = "https://meme-api.herokuapp.com/gimme/"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.api = requests.Session()
        self.api.headers.update(headers)
    
    def get_random_meme(self, subreddit="dankmemes"):
        meme = self.api.get(self.random_url+subreddit).json()
        return meme.get("url")


class DemotivationMeApi:
    def __init__(self):
        self.random_url = "/random.php"
        self.base_url = "https://demotivation.me"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.api = requests.Session()
        self.api.headers.update(headers)

    def get_random_demotivator(self, offset=None):
        page = self.api.get(self.base_url+self.random_url)
        page_parsed = BeautifulSoup(page.text, "html.parser")
        pat = re.compile(r'javascript:set_vote\("([\w\d]+)"\)')
        try:
            demotivators = [
                tag.find("a")["href"] for tag in
                (
                    page_parsed
                    .find("table", {"align": "center", "border": "1"})
                    .find_all("td", {"align": "center"})
                )
            ]
            demotivators_parsed = []
            for dem in demotivators:
                url = pat.search(dem)
                if url:
                    demotivators_parsed.append(url.group(1))
            demotivator_url = demotivators_parsed[offset%len(demotivators_parsed)] if offset else random.choice(demotivators_parsed)
            logger.info(demotivator_url)
            demotivator_page = self.api.get(self.base_url+"/"+demotivator_url+"pic.html")
            page_parsed = BeautifulSoup(demotivator_page.text, "html.parser")
            demotivator_pic = self.base_url+page_parsed.find("img", {"name": "DEMOTIVATOR"})["src"]
            return demotivator_pic
        except:
            raise ValueError


if __name__=="__main__":
    logger.info(
        DemotivationMeApi().get_random_demotivator(0)
    )