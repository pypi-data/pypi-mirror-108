from scraper.db.domains import Domains


class TestDomains:
    def test_get_root_domain(self):
        domain = "subdomain.subdomain.domain.com.ua"
        domain2 = "subdomain.domain.com.ua"
        domain3 = "domain.com.ua"
        domain4 = "domain.com"
        domain5 = "domain.com:fkkdldl"
        domain6 = "fkkdldl^7k/com.ua"
        domain7 = "subdomain.domain.com"
        domain8 = "www.law.by"
        domain9 = "www.flickr.com"

        assert "domain.com.ua" == Domains().get_root_domain(domain)
        assert "domain.com.ua" == Domains().get_root_domain(domain2)
        assert "domain.com.ua" == Domains().get_root_domain(domain3)
        assert "domain.com" == Domains().get_root_domain(domain4)
        assert None is Domains().get_root_domain(domain5)
        assert "fkkdldl^7k/com.ua" == Domains().get_root_domain(domain6)
        assert "domain.com" == Domains().get_root_domain(domain7)
        assert "law.by" == Domains().get_root_domain(domain8)
        assert "flickr.com" == Domains().get_root_domain(domain9)

    def test_list_of_tlds(self):
        assert type(Domains.list_of_tlds()) == list
        assert len(Domains.list_of_tlds()) > 0

    def test_list_of_tlds_combinations(self):
        list_of_tlds = [".com", ".uk"]
        tlds_combinations = [(".com", ".uk"), (".uk", ".com")]

        assert Domains.list_of_tlds_combinations(list_of_tlds) == tlds_combinations

    def test_join_tuple_string(self):
        str = ".com.uk"

        assert str == Domains.join_tuple_string((".com", ".uk"))

    def test_domain_status_code(self):
        domain = "test.com"
        domain2 = "volcano.und.edu"
        domain3 = "bedfordva.gov"
        domain4 = "gp.gov"
        domain5 = "census.gov"
        domain6 = "uky.edu"

        assert Domains.domain_status_code(domain) == 200
        assert Domains.domain_status_code(domain2) is None
        assert Domains.domain_status_code(domain3) == 200
        assert Domains.domain_status_code(domain4) is None
        assert Domains.domain_status_code(domain5) == 403
        assert Domains.domain_status_code(domain6) is None

    def test_get_tlds(self):
        list_of_tlds = [".com", ".uk"]
        tlds_combinations = [(".com", ".uk"), (".uk", ".com")]

        res = [".com.uk", ".uk.com", ".com", ".uk"]

        assert res == Domains().get_tlds(list_of_tlds, tlds_combinations)


if __name__ == '__main__':
    list_of_tlds = [".com", ".uk"]
    tlds_combinations = [(".com", ".uk"), (".uk", ".com")]

    print(list(Domains.list_of_tlds_combinations(list_of_tlds)))
