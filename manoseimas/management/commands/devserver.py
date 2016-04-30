from django.contrib.staticfiles.management.commands import runserver
from django.conf import settings

from manoseimas.utils import managed_subprocess


class Command(runserver.Command):
    def handle(self, *args, **kwargs):
        with managed_subprocess(settings.WEBPACK_COMMAND):
            super(Command, self).handle(*args, **kwargs)
