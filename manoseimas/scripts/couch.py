# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

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
