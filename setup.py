from setuptools import setup, find_packages

setup(
    name='manoseimas-lt',
    version='0.1',
    license='AGPLv3+',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'django',
        'django-social-auth',
        'sorl-thumbnail',
        'couchdbkit',
        'django-sboard',
        'Scrapy',
        'CouchDB',
        'twisted',
        'pycrypto',
        'django_compressor',
        'MySQL-python',
        'pylibmc',
        'mock',
        'coverage',
        'django-debug-toolbar',
        'django-extensions',
        'django-test-utils',
        'Werkzeug',
        'ipdb',
        'ipython',
        'django-pdb',
        'django-nose',
        'ipdbplugin',
        'exportrecipe',
        'libsass',
        'django-libsass',
    ],
    entry_points={
        'console_scripts': [
            'couch = manoseimas.scripts.couch:main',
        ],
    }
)
