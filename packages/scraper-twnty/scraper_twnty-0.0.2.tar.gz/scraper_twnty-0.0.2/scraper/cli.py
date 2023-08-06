import argparse
from os import getenv
from yoyo import get_backend
from yoyo import read_migrations
from scraper.dir_reader import FileReader
from scraper.db.domains import Domains
from scraper.directories import Directories


def migration(args):
    backend = get_backend("postgres://domains:domains@localhost/domains")
    migrations = read_migrations("scraper/migrations")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


def create_directories(args):
    dirs = Directories(args.froot, args.ftrash)
    dirs.run()


def dir_reader(args):
    fr = FileReader(args.froot, args.ftrash)
    fr.run()


def domains(args):
    dns = Domains()
    dns.run()


def execute():
    parser = argparse.ArgumentParser(prog="scraper", description='Scraper CLI manager')
    parser.add_argument("-r", "--froot", type=str, default=getenv("HOME") + "/in_data", help='folder root')
    parser.add_argument("-t", "--ftrash", type=str, default=getenv("HOME") + "/out_data", help='folder trash')
    parser.set_defaults()

    subparsers = parser.add_subparsers(help='sub-command help')

    migration_parser = subparsers.add_parser('migration', help='App migrations')
    migration_parser.set_defaults(func=migration)

    directories_parser = subparsers.add_parser('directories', help="create directories")
    directories_parser.set_defaults(func=create_directories)

    dir_parser = subparsers.add_parser('dir_reader', help='Dir reader')
    dir_parser.set_defaults(func=dir_reader)

    domains_parser = subparsers.add_parser('domains', help='Domains table filler')
    domains_parser.set_defaults(func=domains)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    execute()
