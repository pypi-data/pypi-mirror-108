from bs4 import BeautifulSoup
from scraper.db.models.links_model import LinkModel
from typing import Optional
from itertools import combinations
import requests


class Parser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> bool:
        try:
            parsed_file = BeautifulSoup(open(self.file_path, encoding='latin-1'), 'html.parser')

            for a in parsed_file.find_all('a', href=True):
                link = str(a['href'])
                domain = self.domain_preparing(link)

                if domain != "":
                    LinkModel.add(domain)  # saving a domain into db

            return True

        except FileNotFoundError as e:
            print(str(e))
            return False
        except TypeError as e:
            print(str(e))
            return False
        except OSError as e:
            print(str(e))
            return False

    @staticmethod
    def link_check(link: str) -> Optional[bool]:
        try:
            if 'http://' in link or 'https://' in link:
                return True
            else:
                return False
        except TypeError as e:
            return False

    @staticmethod
    def domain_preparing(link: str) -> Optional[str]:
        domain = ""

        if Parser.link_check(link):
            domain_els = link.split("/")[2].split("www.")[-1].split("//")[-1].split(".")

            if ":" in domain_els[len(domain_els) - 1]:
                l = domain_els[len(domain_els) - 1].find(':')
                domain_els[len(domain_els) - 1] = domain_els[len(domain_els) - 1][:l]

            domain = '.'.join(domain_els)

        return domain

