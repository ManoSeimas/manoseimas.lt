#!/usr/bin/env python

import sys
import argparse
import subprocess
import os
import os.path
import json


def repeat(func, arg, n):
    result = arg
    for i in range(n):
        result = func(result)
    return result


def get_cover_package(path):
    if ':' in path:
        path = path[:path.index(':')]

    base = os.path.abspath(repeat(os.path.dirname, __file__, 2))
    path = os.path.abspath(path)
    path = os.path.relpath(path, base)
    parts = path.split(os.sep)
    if len(parts) > 1:
        return '.'.join(parts[:2])
    else:
        return parts[0]


def get_paths(paths):
    if paths:
        for path in paths:
            if ':' in path:
                path = path[:path.index(':')]
            yield path
    else:
        yield 'manoseimas'


def is_coverage_enabled(args):
    if args.nocoverage or args.profile:
        return False
    else:
        return True


def run_tests(args):
    if args.fast:
        settings = 'manoseimas.settings.fasttesting'
    else:
        settings = 'manoseimas.settings.testing'

    cmd = [
        'bin/django', 'test',
        '--settings=%s' % settings,
        '--nocapture',
        '--nologcapture',
        '--all-modules',
        '--with-doctest',
        '--doctest-tests',
        '--noinput',
    ] + args.paths

    if args.profile:
        cmd = [
            'bin/kernprof',
            '--line-by-line',
            '--builtin',
            '--outfile=/dev/null',
            '--view',
        ] + cmd
    elif is_coverage_enabled(args):
        coverage_modules = list(set(map(get_cover_package, args.paths)))
        subprocess.call(['bin/coverage', 'erase'])
        cmd = [
            'bin/coverage', 'run',
            '--source=%s' % ','.join(coverage_modules),
        ] + cmd

    return subprocess.call(cmd)


def run_flake8(args):
    cmd = [
        'bin/flake8',
        '--exclude=migrations',
        '--ignore=E501,E241',
    ] + list(get_paths(args.paths))
    return subprocess.call(cmd)


def run_pylint(args):
    cmd = [
        'bin/pylint',
        '--msg-template="%s"' % (
            '{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}',
        )
    ] + list(get_paths(args.paths))
    return subprocess.call(cmd)


def run_coverage_report(args):
    # Also see .coveragerc
    return subprocess.call(['bin/coverage', 'report', '--show-missing'])


def main(args=None):
    buildout_dir = os.path.abspath(repeat(os.path.dirname, __file__, 2))

    with open(os.path.join(buildout_dir, 'settings.json')) as f:
        config = json.load(f)

    parts_dir = config['buildout-parts-dir']
    django_sboard_path = os.path.join(parts_dir, 'django-sboard')

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'paths', nargs='*', default=['manoseimas', django_sboard_path],
        help='paths to test files',
    )
    parser.add_argument(
        '--fast', action='store_true', default=False,
        help='run tests with adlt.settings.fasttests settings',
    )
    parser.add_argument(
        '--profile', action='store_true', default=False,
        help='run tests with line profiler',
    )
    parser.add_argument(
        '--nocoverage', action='store_true', default=False,
        help='run tests without test coverage report',
    )
    args = parser.parse_args(args)

    retcode = run_tests(args)

    # if retcode == 0:
    #     retcode = run_flake8(args)

    # if retcode == 0:
    #     retcode = run_pylint(args)

    if retcode == 0 and is_coverage_enabled(args):
        run_coverage_report(args)

    sys.exit(retcode)


if __name__ == '__main__':
    main()
