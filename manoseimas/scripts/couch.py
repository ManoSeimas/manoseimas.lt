import argparse

from couchdbkit import Server

from django.core.management import setup_environ
from manoseimas import settings
setup_environ(settings)

from django.conf import settings


def replicate(args):
    server = Server(settings.COUCHDB_SERVER)
    server.replicate(args.source, args.target)


def shell(args):
    import IPython
    shell = IPython.Shell.IPShellEmbed()
    shell()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # replicate
    p = subparsers.add_parser('replicate')
    p.add_argument('source')
    p.add_argument('target')
    p.set_defaults(func=replicate)

    # shell
    p = subparsers.add_parser('shell')
    p.set_defaults(func=shell)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
