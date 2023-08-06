from bs4 import BeautifulSoup
from scraper.db.models.links_model import LinkModel
from scraper.db.models.domains_model import DomainModel
from typing import Optional
from time import sleep
from itertools import combinations, permutations

import requests


class Domains:
    def add_domains(self):
        for item in LinkModel.get_data():
            domain = self.get_root_domain(item[1])

            if domain:
                status_code = Domains.domain_status_code(domain)
                DomainModel.add(domain, status_code)
                print("done")

    def get_root_domain(self, url: str) -> Optional[str]:
        tlds = self.get_tlds(Domains.list_of_tlds(), Domains.list_of_tlds_combinations(Domains.list_of_tlds()))
        for item in tlds:
            if not url.endswith(item):
                continue

            _name = url.rstrip(item)
            domain_name = _name.split(".")[-1]

            if domain_name != "www":
                root_domain = f"{domain_name}{item}"
                return root_domain
            else:
                root_domain = f"{item}"
                return root_domain[1:len(root_domain)]

    @staticmethod
    def list_of_tlds() -> Optional[list]:
        l = []
        resp = requests.get("https://www.iana.org/domains/root/db")

        soup = BeautifulSoup(resp.text, 'html.parser')

        for p in soup.find_all(class_="domain tld"):
            l.append(p.string)

        return l

    @staticmethod
    def list_of_tlds_combinations(list_of_tlds: list) -> Optional[list]:
        l = []
        for item in list(combinations(list_of_tlds, 2)):
            l += permutations(item)
        return l

    @staticmethod
    def join_tuple_string(tld_combo: tuple) -> Optional[str]:
        return ''.join(tld_combo)

    @staticmethod
    def domain_status_code(domain: str) -> Optional[int]:
        try:
            r = requests.get("https://" + domain)
            sleep(1)
            return r.status_code
        except requests.exceptions.ConnectionError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

    def get_tlds(self, list_of_tlds, list_of_tlds_combination) -> Optional[list]:
        l = []
        for item in list_of_tlds_combination:
            l.append(self.join_tuple_string(item))

        return l + list_of_tlds

    def run(self):
        self.add_domains()


if __name__ == '__main__':
    Domains().add_domains()
