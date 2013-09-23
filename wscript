#!/usr/bin/env python
# encoding: utf-8

import codecs
import functools
import os
import random
import re
import shutil
import subprocess
import sys

from waflib import Context, Logs

top = '.'
out = '.'

def options(ctx):
    ctx.load('compiler_c python')
    PROJECT_NAME = 'manoseimas'

    gr = ctx.get_option_group('configure options')
    gr.add_option('--project-name', action='store', default=PROJECT_NAME,
                  help='project name')

    gr.add_option('--production', action='store_true', default=False,
                  help='build production environment')

    gr.add_option('--server-name', action='store',
                  default='127.0.0.1:8000',
                  help='server domain name, example: www.example.com')

    gr.add_option('--server-admin', action='store', default='admin@example.com',
                  help='server admin email address')

    gr.add_option('--use-sqlite', action='store_true',
                  help='force Sqlite database in production')

    gr.add_option('--wsgi-user', action='store',
                  help='the user that the daemon processes should be run as')

    gr.add_option('--wsgi-group', action='store',
                  help='the primary group that the daemon processes should be run as')

    gr.add_option('--use-htpasswd', action='store_true', default=False,
                  help='use http authenticaiton')

    gr.add_option('--languages', action='store', default='lt',
                  help='comma separated list of two letter languages codes')

    gr.add_option('--use-jquery', action='store', default='1.7',
                  help='jQuery version, or empty if you don\'t want to use it')

    gr.add_option('--secret-key', action='store',
                  help='set this to a random string -- the longer, the better')

    gr.add_option('--mysql-username', action='store', default='root',
                  help='MySQL database user name.')

    gr.add_option('--mysql-password', action='store', default='',
                  help='MySQL database user password.')

    gr.add_option('--mysql-dbname', action='store', default=PROJECT_NAME,
                  help='MySQL database name.')

    gr.add_option('--facebook-app-id', action='store', default='',
                  help='Facebook App ID.')

    gr.add_option('--facebook-api-secret', action='store', default='',
                  help='Facebook API secret.')

    gr.add_option('--google-analytics-key', action='store', default='',
                  help='Google Analytics key.')

    gr.add_option('--twitter-bootstrap', action='store_true', default=True,
                  help='Use Twitter bootstrap framework.')

    gr.add_option('--less', action='store_true', default=False,
                  help='Use LESS, CSS processor.')

    gr = ctx.add_option_group('setup options')
    gr.add_option("--use-pkg-add", action="store_true", dest="use_pkg_add",
                  default=False, help="use pkg_add in BSD systems")

    gr.add_option("--dry-run", action="store_true", dest="dry_run", default=False,
                  help="print commands, but do net execute")

    gr.add_option('--couchdb-url', action='store',
                  default='http://127.0.0.1:5984',
                  help='couchdb url, example: '
                       'http://127.0.0.1:5984')

    gr.add_option('--couchdb-server-name', action='store',
                  default='127.0.0.1:5984',
                  help='pulbic couchdb domain name, example: couchdb.example.com')


def _get_secret_key(length=50):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join([random.choice(chars) for i in range(length)])


def _create_configure_file(ctx):
    """Store all configuration options to 'configure' file.

    Next time, if you want to to modify some configuration options, you simple
    can change configure file and and execute it using this command::

        ./configure

    """
    import pipes

    configure = sys.argv[2:]
    if not ctx.options.secret_key:
        configure.append("--secret-key=%s" % ctx.env.SECRET_KEY)

    configure = (['%s' % ' '.join(sys.argv[:2])] +
                 [pipes.quote(c) for c in configure])

    f = open('configure', 'w')
    f.write('#!/bin/sh\n')
    f.write(' \\\n    '.join(configure) + '\n')
    f.close()

    os.chmod('configure', 0700)


def configure(ctx):
    ctx.find_program('buildout', mandatory=False)
    ctx.find_program('hg')
    ctx.find_program('git')
    ctx.find_program('virtualenv')
    ctx.find_program('java')

    ctx.load('compiler_c python')

    ctx.check_python_version((2,6))
    ctx.check_python_headers()

    ctx.env.TOP = ctx.path.abspath()
    ctx.env.PROJECT_NAME = ctx.options.project_name
    ctx.env.PRODUCTION = ctx.options.production
    ctx.env.USE_SQLITE = ctx.options.use_sqlite
    ctx.env.LANGUAGES = ctx.options.languages.split(',') or ['lt']
    ctx.env.LANGUAGE_CODE = ctx.env.LANGUAGES[0]
    ctx.env.SERVER_ADMIN = ctx.options.server_admin
    ctx.env.SERVER_NAME = ctx.options.server_name
    ctx.env.JQUERY_VERSION = ctx.options.use_jquery
    ctx.env.SECRET_KEY = ctx.options.secret_key or _get_secret_key()

    ctx.env.WSGI_USER = ctx.options.wsgi_user
    ctx.env.WSGI_GROUP = ctx.options.wsgi_group
    ctx.env.USE_HTPASSWD = ctx.options.use_htpasswd

    ctx.env.MYSQL_USERNAME = ctx.options.mysql_username
    ctx.env.MYSQL_PASSWORD = ctx.options.mysql_password
    ctx.env.MYSQL_DBNAME = ctx.options.mysql_dbname

    ctx.env.FACEBOOK_APP_ID = ctx.options.facebook_app_id
    ctx.env.FACEBOOK_API_SECRET = ctx.options.facebook_api_secret

    ctx.env.GOOGLE_ANALYTICS_KEY = ctx.options.google_analytics_key

    ctx.env.TWITTER_BOOTSTRAP = ctx.options.twitter_bootstrap
    ctx.env.LESS = ctx.options.less or ctx.env.TWITTER_BOOTSTRAP

    ctx.env.DJANGO_PIPELINE = ctx.env.LESS

    ctx.env.COUCHDB_URL = ctx.options.couchdb_url
    ctx.env.COUCHDB_SERVER_NAME = ctx.options.couchdb_server_name

    if ctx.env.PRODUCTION:
        ctx.env.DEVELOPMENT = False
    else:
        ctx.env.DEVELOPMENT = True

    if not os.path.exists('configure'):
        _create_configure_file(ctx)


def _subst(task):
    from Cheetah.Template import Template

    infilename = task.inputs[0].abspath()
    outfilename = task.outputs[0].abspath()

    c = {
        'NOTE': 'DO NOT MODIFY! This file is generated from %s '
                'template.' % infilename,
    }
    t = Template(file=infilename, searchList=[c, dict(task.generator.env)])

    outfile = codecs.open(outfilename, encoding='utf-8', mode='w')
    outfile.write(unicode(t))
    outfile.close()


def build(ctx):
    import babel

    ctx.env.LANG_NAMES = {}
    for lang in ctx.env.LANGUAGES:
        ctx.env.LANG_NAMES[lang] = babel.Locale(lang).english_name

    p = ctx.env.PROJECT_NAME
    glob = ctx.path.ant_glob
    bld = functools.partial(ctx, update_outputs=True)

    if ctx.env.PRODUCTION:
        bld(rule=_subst, source='config/apache.conf c4che/_cache.py',
            target='var/etc/apache.conf')

        if ctx.env.COUCHDB_SERVER_NAME:
            bld(rule=_subst, source='config/apache.couchdb.conf c4che/_cache.py',
                target='var/etc/apache.couchdb.conf')

        bld(rule=_subst, source='config/my.cnf',
            target='var/etc/my.cnf')

    bld(rule=_subst, source='config/buildout.cfg c4che/_cache.py',
        target='buildout.cfg')

    bld(rule=_subst, source='config/settings.py c4che/_cache.py',
        target='%s/settings.py' % p)

    bld(rule=_subst, source='config/scrapy_settings.py c4che/_cache.py',
        target='%s/scrapy/settings.py' % p)

    bld(rule=_subst, source='config/urls.py c4che/_cache.py',
        target='%s/urls.py' % p)

    bld(rule=_subst, source='config/initial_data.json c4che/_cache.py',
        target='initial_data.json')

    bld(rule='env/bin/python bootstrap.py --distribute', target='bin/buildout')

    bld(rule='bin/buildout -N', name='buildout',
        target='bin/django',
        source='bin/buildout buildout.cfg %s/settings.py' % p)

    bld(rule=('bin/django syncdb --all --noinput && '
              'bin/django migrate --fake && '
              'touch ${TGT}'),
        after='buildout', target='var/db')

    if ctx.env.LESS:
        bld(rule='mkdir -p parts/node_modules && npm --prefix parts install less@1.3.3 && ln -s ../parts/node_modules/less/bin/lessc bin',
            target='bin/lessc')

    bld(rule='bin/django collectstatic --noinput --verbosity=0',
        source=(glob('%s/static/**/*' % p)), after='buildout')

    for lang in ctx.env.LANGUAGES:
        s = (p, lang)
        if os.path.exists('%s/locale/%s' % s):

            bld(rule='cd %s ; ../bin/django compilemessages -l %s' % s,
                source='%s/locale/%s/LC_MESSAGES/django.po' % s,
                target='%s/locale/%s/LC_MESSAGES/django.mo' % s,
                after='buildout')


def makemessages(ctx):
    for lang in ctx.env.LANGUAGES:
        s = (ctx.env.PROJECT_NAME, lang)
        if os.path.exists('%s/locale/%s' % s):
            _sh('cd %s ; ../bin/django makemessages -l %s '
                '-e html,txt' % s)


def distclean(ctx):
    for pth in [
        # buildout generated files
        'bin', 'develop-eggs', '.installed.cfg', '.mr.developer.cfg',

        # waf generated files
        '.lock-wafbuild', 'config.log', 'c4che', Context.DBFILE,

        # project specific generated files
        'buildout.cfg', '%s/settings.py' % ctx.env.PROJECT_NAME,
    ]:
        if os.path.exists(pth):
            Logs.info('cleaning: %s' % pth)
            if os.path.isdir(pth):
                shutil.rmtree(pth, ignore_errors=True)
            else:
                os.unlink(pth)

    cleanpyc(ctx)


def cleanpyc(ctx):
    "Clean *.pyc files from sources."
    Logs.info('cleaning: *.pyc')
    for pth in ctx.path.ant_glob('%s/**/*.pyc' % ctx.env.PROJECT_NAME):
        os.unlink(pth.abspath())


def _get_platform():
    import platform

    python_version = sys.version[:3]
    uname = os.uname()[0].lower()
    if uname == 'linux':
        if python_version > '2.6':
            name, release = platform.linux_distribution()[:2]
        else:
            name, release = platform.linux_distribution()[:2]
        if name and release:
            return (uname, name.lower(), release)
    return (uname, '', '')


def _sh(cmd, dry_run=False):
    print(cmd)
    if not dry_run:
        rcode = subprocess.call(cmd, shell=True)
        if rcode > 0:
            sys.exit(rcode)


def virtualenv(ctx):
    """initialize virtualenv environment"""
    uname, name, release = _get_platform()
    sh = functools.partial(_sh, dry_run=ctx.options.dry_run)
    if uname == 'darwin':
        pyver = sys.version[:3]
        sh('virtualenv-%s --no-site-packages env' % pyver)
    else:
        sh('virtualenv --no-site-packages env')
    sh('env/bin/pip install Cheetah Babel')


class PackageSet(set):
    def replace(self, *args):
        if not isinstance(args[0], tuple):
            args = (args[0:2],)
        for old, new in args:
            self.remove(old)
            self.add(new)

    def replace_all(self, search, replace):
        repl = re.compile(search)
        for old in self:
            new = repl.sub(replace, old)
            if old != new:
                self.replace(old, new)


def setup(ctx):
    """install all required dependencies"""

    sh = functools.partial(_sh, dry_run=ctx.options.dry_run)

    if not ctx.options.dry_run and not os.geteuid() == 0:
        sys.exit("Only root can run this script.")

    uname, name, release = _get_platform()

    packages = PackageSet([
        # Build
        'build-essential',

        # Gettext
        'gettext',

        # VCS
        'git',
        'mercurial',

        # Python
        'python-dev',
        'python-virtualenv',

        # Other development headers
        'libfreetype6-dev',
        'libicu-dev',
        'libjpeg62-dev',
        'libxslt1-dev',
    ])

    if ctx.options.production:
        packages.add('libmysqlclient-dev')

    if name == 'ubuntu' or name == 'debian':
        packages.replace('git', 'git-core')
        sh('apt-get install %s' % ' '.join(packages))

    elif name == 'fedora':
        packages.remove('build-essential')
        packages.replace(
                ('libfreetype6-dev', 'freetype-devel'),
                ('libjpeg62-dev', 'libjpeg-turbo-devel'),
                ('libxslt1-dev', 'libxslt-devel')
            )
        packages.replace_all('-dev$', '-devel')
        sh('yum groupinstall "Development Tools"')
        sh('yum install %s' % ' '.join(packages))

    elif uname == 'darwin':
        pyver = sys.version[:3].replace('.', '')
        packages.remove('build-essential')
        packages.remove('python-dev')
        packages.replace(
                ('git', 'git-core'),
                ('python-virtualenv', 'py%s-virtualenv' % pyver),
                ('libfreetype6-dev', 'freetype'),
                ('libicu-dev', 'icu'),
                ('libjpeg62-dev', 'jpeg'),
                ('libxslt1-dev', 'libxslt')
        )

        sh('port select --set python python%s' % pyver)
        sh('port -v install %s' % ' '.join(packages))
        sh('ln -s /opt/local/bin/virtualenv-%s /opt/local/bin/virtualenv' % pyver)

    elif uname == 'freebsd':
        if ctx.options.use_pkg_add:
            sh('pkg_add -r %s' % ' '.join(packages))
        else:
            for pkg in packages:
                sh('cd /usr/ports/%s && make install clean' % pkg)




    else:
        sys.exit('Sorry, your platform is not supported...')

# --------
# Hack to pass ``BuildContext`` to commands other than ``build``.
from waflib.Build import BuildContext
def use_build_context_for(*cmds):
    for cmd in cmds:
        type('BldCtx_' + cmd, (BuildContext,), {'cmd': cmd, 'fun': cmd})
use_build_context_for('makemessages', 'distclean', 'cleanpyc')
# --------
