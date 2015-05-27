from manoseimas.settings.base import *  # noqa
from manoseimas.settings.development import *  # noqa

INTERNAL_IPS = (
    '127.0.0.1',
    '10.0.2.2',  # Vagrant host IP in default config
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': ('SET storage_engine=INNODB; '
                             'SET GLOBAL sql_mode=STRICT_ALL_TABLES;'),
            'read_default_file': os.path.expanduser('~/.my.cnf'),
        },
    }
}
