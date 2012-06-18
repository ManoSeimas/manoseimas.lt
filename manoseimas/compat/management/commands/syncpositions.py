# coding: utf-8

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

from django.core.management.base import BaseCommand

from sboard.models import couch

from manoseimas.compat.models import update_mps_positions


class Command(BaseCommand):
    help = "calculate all MPs and fraction positions of for all solutions"

    def handle(self, *args, **options):
        for node in couch.iterchunks('sboard/by_type', skey='Solution'):
            print('[ %s ]: %s' % (node.key, node.title))
            update_mps_positions(node.key)
