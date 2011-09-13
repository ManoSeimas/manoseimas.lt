#!/usr/bin/env python
# encoding: utf-8

import codecs
import os
import shutil

from Cheetah.Template import Template

from waflib import Context, Logs

top = '.'
out = '.'


def options(ctx):
    ctx.load('compiler_c python ruby')

    gr = ctx.get_option_group('configure options')
    gr.add_option('--production', action='store_true', default=False,
                  help='build production environment')

    gr.add_option('--server-name', action='store',
                  help='server domain name, example: www.example.com')

    gr.add_option('--server-admin', action='store',
                  help='server admin email address')

    gr.add_option('--couchdb-url', action='store',
                  default='http://127.0.0.1:5984/manoseimas',
                  help='couchdb url, example: '
                       'http://127.0.0.1:5984/manoseimas')


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
    ctx.find_program('git')

    ctx.load('compiler_c python ruby')

    ctx.check_python_version((2,6))
    ctx.check_python_module('PIL')
    ctx.check_python_module('Cheetah')
    ctx.check_python_headers()

    ctx.check_ruby_version((1,8,0))
    ctx.check_ruby_ext_devel()

    ctx.env.TOP = ctx.path.abspath()
    ctx.env.PRODUCTION = ctx.options.production
    ctx.env.COUCHDB_URL = ctx.options.couchdb_url

    if ctx.env.PRODUCTION:
        options = ['mysql_password']
        required_options = ['server_name', 'server_admin']
        _check_required_options(ctx, required_options,
                                'These options are required when configuring '
                                'with --production option:')
        for opt in required_options + options:
            setattr(ctx.env, opt.upper(), getattr(ctx.options, opt) or '')
    else:
        ctx.env.DEVELOPMENT = True


def _bootstrap(ctx):
    if 'BUILDOUT' in ctx.env:
        ctx(rule='${BUILDOUT} init', target='bin/buildout',
            update_outputs=True)
    else:
        ctx(rule='${PYTHON} bootstrap.py --distribute', target='bin/buildout',
            update_outputs=True)


def _subst(task):
    for i in range(len(task.inputs)):
        infilename = task.inputs[i].abspath()
        outfilename = task.outputs[i].abspath()

        c = {
            'NOTE': 'DO NOT MODIFY! This file is generated from %s template. '
                    'Do not edit this file, if you want to make changes, make '
                    'them in template files.' % infilename,
        }
        t = Template(file=infilename, searchList=[c, dict(task.generator.env)])

        outfile = codecs.open(outfilename, encoding='utf-8', mode='w')
        outfile.write(unicode(t))
        outfile.close()


def build(ctx):
    _bootstrap(ctx)

    ctx(rule=_subst, source='config/buildout.cfg', target='buildout.cfg')

    if ctx.env.PRODUCTION:
        ctx(rule=_subst, source='config/apache.conf',
            target='var/etc/apache.conf')

    ctx(rule=_subst, source='config/settings.py',
        target='manoseimas/settings.py')

    ctx(rule='bin/buildout -N', name='django',
        source='bin/buildout buildout.cfg manoseimas/settings.py',
        target='bin/django', update_outputs=True)

    ctx(rule='bin/django syncdb --all --noinput && bin/django migrate --fake',
        source='bin/django manoseimas/settings.py')

    ctx(rule='bin/sass --update manoseimas/sass:var/sass/css',
        source=ctx.path.ant_glob('manoseimas/sass/*.scss'),
        target='var/sass/css/style.css', name='sass', after='django',
        update_outputs=True)

    ctx(rule='bin/django collectstatic --noinput --verbosity=0',
        source=ctx.path.ant_glob('manoseimas/static/**/*'),
        after='sass', update_outputs=True)


def distclean(ctx):
    for pth in [
        # buildout generated files
        'bin', 'develop-eggs', '.installed.cfg', '.mr.developer.cfg',

        # waf generated files
        '.lock-wafbuild', 'config.log', 'c4che', Context.DBFILE,

        # project specific generated files
        '.sass-cache', 'buildout.cfg', 'manoseimas/settings.py', 'var',
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
    for pth in ctx.path.ant_glob('manoseimas/**/*.pyc'):
        os.unlink(pth.abspath())
