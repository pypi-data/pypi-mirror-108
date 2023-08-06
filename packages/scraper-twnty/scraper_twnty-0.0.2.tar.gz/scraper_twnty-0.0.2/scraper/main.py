from scraper.db.models.domains_model import DomainModel
from scraper.db.models.links_model import LinkModel


if __name__ == '__main__':
    print("Links table")
    for row in LinkModel.get_data().iterator():
        print(row)

    print("Amount of data\n", LinkModel.amount_of_data())

    print("Domains table")
    for row in DomainModel.get_data().iterator():
        print(row)

    print("Amount of data\n", DomainModel.amount_of_data())

    print("Domains with 200 status code from domains table")
    for row in DomainModel.get_data().where(DomainModel.status_code == 200).iterator():
        print(row)




