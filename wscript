#!/usr/bin/env python
# encoding: utf-8

import os
import shutil

from waflib import Context, Logs
from waflib.Build import BuildContext

top = '.'
out = '.'

DB_FILE = os.path.join('var', 'project.db')


def options(ctx):
    ctx.load('compiler_c python ruby')

    gr = ctx.get_option_group('configure options')
    gr.add_option('--production', action='store_true', default=False,
                  help='build production environment')

    gr.add_option('--server-name', action='store',
                  help='server domain name, example: www.example.com')

    gr.add_option('--server-admin', action='store',
                  help='server admin email address')


def _check_required_options(ctx, options, msg):
    missing = []

    for option in options:
        if not getattr(ctx.options, option, ''):
            missing.append(option)

    if missing:
        Logs.warn(msg)
        for option in options:
            if not getattr(ctx.options, option, ''):
                Logs.warn('\t--%s' % option)
        Logs.warn('See waf --help for more information.')
        ctx.fatal('Some required options are missing.')


def configure(ctx):
    ctx.find_program('buildout', mandatory=False)
    ctx.find_program('hg')

    ctx.load('compiler_c python ruby')

    ctx.check_python_version((2,6))
    ctx.check_python_module('PIL')
    ctx.check_python_headers()

    ctx.check_ruby_version((1,8,0))
    ctx.check_ruby_ext_devel()

    ctx.env.TOP = ctx.path.abspath()
    ctx.env.PRODUCTION = ctx.options.production

    if ctx.env.PRODUCTION:
        options = ['mysql_password']
        required_options = ['server_name', 'server_admin']
        _check_required_options(ctx, required_options,
                                'These options are required when configuring '
                                'with --production option:')
        for opt in required_options + options:
            setattr(ctx.env, opt.upper(), getattr(ctx.options, opt) or '')


def _bootstrap(ctx):
    if 'BUILDOUT' in ctx.env:
        ctx(rule='${BUILDOUT} init', target='bin/buildout',
            update_outputs=True)
    else:
        ctx(rule='${PYTHON} bootstrap.py --distribute', target='bin/buildout',
            update_outputs=True)


def _get_sources_for_django(ctx, *args):
    return (ctx.path.ant_glob('setup.py') +
            ['bin/buildout', 'buildout.cfg'] + list(args))


def _syncdb(ctx):
    ctx(rule='bin/django syncdb --all --noinput && bin/django migrate --fake',
        after='django', name='syncdb', always=True)


def _substitute(ctx, files):
    # s - source, d - destination
    for s, d in files:
        if not os.path.exists(os.path.join(*d.split('/'))):
            ctx(features='subst', target=d, source=s, quiet=True)


def _build_production(ctx):
    Logs.info('Building PRODUCTION environment')

    _substitute(ctx, [
            ('etc/production.py.in', 'manoseimas/production.py'),
            ('etc/apache.conf.in', 'etc/apache.conf'),
        ])

    ctx(rule='bin/buildout -c production.cfg -N', name='django',
        source=_get_sources_for_django(ctx, 'manoseimas/production.py',
                                            'production.cfg'),
        target='bin/django bin/django.wsgi', update_outputs=True)


def _build_development(ctx):
    Logs.info('Building DEVELOPMENT environment')

    ctx(rule='bin/buildout -c development.cfg -N', name='django',
        source=_get_sources_for_django(ctx, 'development.cfg'),
        target='bin/django', update_outputs=True)

    if not os.path.exists(DB_FILE):
        _syncdb(ctx)


def build(ctx):
    _bootstrap(ctx)

    if ctx.env.PRODUCTION:
        _build_production(ctx)
    else:
        _build_development(ctx)

    ctx(rule='bin/django collectstatic --noinput --verbosity=0',
        source=ctx.path.ant_glob('manoseimas/static/**/*'),
        after='django', name='collectstatic', update_outputs=True)

    ctx(rule='bin/sass --update manoseimas/sass:var/build/sass/css',
        source=ctx.path.ant_glob('manoseimas/sass/*.scss'),
        target='var/build/sass/css/style.css', after='collectstatic',
        update_outputs=True)


def distclean(ctx):
    for pth in [
        # buildout generated files
        'bin', 'develop-eggs', '.installed.cfg', '.mr.developer.cfg',

        # waf generated files
        '.lock-wafbuild', 'config.log', 'c4che', Context.DBFILE,

        # project specific generated files
        DB_FILE, 'manoseimas/production.py', 'etc/apache.conf', '.sass-cache',
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
    for pth in ctx.path.ant_glob(['manoseimas/**/*.pyc', 'apps/**/*.pyc']):
        os.unlink(pth.abspath())


def syncdb(ctx):
    "clean and create database, used only in development environment"
    if ctx.env.PRODUCTION:
        ctx.fatal('syncdb command can be used only in development environment')
    if os.path.exists(DB_FILE):
        os.unlink(DB_FILE)
    _syncdb(ctx)


class SyncDbContext(BuildContext):
    cmd = 'syncdb'
    fun = 'syncdb'
