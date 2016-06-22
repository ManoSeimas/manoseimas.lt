from setuptools import setup, find_packages

setup(
    name='manoseimas-lt',
    version='0.2',
    license='AGPLv3+',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'django',
        'python-social-auth',
        'sorl-thumbnail',
        'Scrapy',
        'django_compressor',
        'MySQL-python',
        'pylibmc',
        'mock',
        'coverage',
        'django-debug-toolbar',
        'django-extensions',
        'django-test-utils',
        'django-webpack-loader',
        'Werkzeug',
        'ipdb',
        'ipython',
        'django-pdb',
        'django-nose',
        'ipdbplugin',
        'exportrecipe',
        'libsass',
        'django-libsass',
        'pyjade',
        'django-autoslug',
        'six',
        'leveldb',
        'tqdm',
        'roman',
        'toposort',
        'django-jsonfield',
        'PyReact',
        'djangorestframework',
        'markdown',
        'unidecode',
        'webtest',
        'django-webtest',
        'whoosh',
        'django-haystack',
        'django-lazysignup',
        'factory_boy',
        'pytz',
    ],
)
