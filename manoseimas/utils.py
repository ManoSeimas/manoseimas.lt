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

import math
from datetime import datetime

from django.core.urlresolvers import reverse
from django.utils.functional import lazy

reverse_lazy = lazy(reverse, str)


def todate(date_str, date_format='%Y-%m-%d'):
    if date_str:
        return datetime.strptime(date_str, date_format).date()
    else:
        return None


class reify(object):
    """ Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.  An example:

    >>> class Foo(object):
    ...     @reify
    ...     def jammy(self):
    ...         print('jammy called')
    ...         return 1
    >>> f = Foo()
    >>> v = f.jammy
    jammy called
    >>> print(v)
    1
    >>> f.jammy
    1
    >>> # jammy func not called the second time; it replaced itself with 1

    Function taken from Pyramid project
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:  # pragma: no cover
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


def round(number):
    return math.floor(number + 0.5)
