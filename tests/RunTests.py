#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    tools/StaticChecks.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
"""
Helper script for executing static checks on source code.

Invocation:

    python tools/StaticChecks.py <CHECKS> <OPTIONS> -f, --file [FILE(S)]

    where <CHECKS> are:

        --format    check (and optionally fix) the formatting of the code
                    using yapf
        --import    check (and optionally fix) the order/grouping of imports
                    using isort
        --manifest  check the MANIFEST.in file for proper content using
                    check-manifest
        --quality   check the quality/style of the code using one or more of
                    flake8, pycodestyle, pydocstyle, and pylint.  Default is
                    to use all.
        --security  check for potential security vulnerabilities using bandit

    and <OPTIONS> are:

        -a, --auto      automatically (in-line) apply recommended changes
        -b, --benchmark benchmark the code
        -c, --color     colorize the output if the tool supports it
        -d, --diff      just print a diff for the fixed source code
        --files-output
        -i, --ignore    ignore files and directories explicitly or those
                        matching a pattern
        --output-format
        -q, --quiet     provide very little output from each tool
        -r, --recursive run recursively over directories
        --reports=<y/n> print or suppress the pylint reports
        -v, --verbose   provide verbose output from each tool


    and [FILE(s)] is a comma-separated list of files to check
"""

from __future__ import print_function

import os
import sys
import subprocess
import glob
from optparse import OptionParser

# We prefer to use the tools in the virtual environment.
try:
    VIRTBIN = glob.glob(os.environ['VIRTUAL_ENV'] + '/bin')[0]
except KeyError:
    # This is hardcoded to the virtual environment I use.
    VIRTBIN = glob.glob(os.environ['WORKON_HOME'] + '/rtk-python2.7-pygtk/bin')[0]
LOCALBIN = os.environ['HOME'] + '/.local/bin'
SYSBIN = '/usr/bin'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFGFILE = ROOT + '/setup.cfg'
PYLINTRC = ROOT + '/.pylintrc'


def do_parse_args():
    """Parse command line arguments."""
    parser = OptionParser()

    # Set default checks.
    parser.set_defaults(formats=False)
    parser.set_defaults(imports=False)
    parser.set_defaults(manifest=False)
    parser.set_defaults(quality=False)
    parser.set_defaults(checkers=[])
    parser.set_defaults(security=False)

    # Set default output options.
    parser.set_defaults(auto=False)
    parser.set_defaults(benchmark=False)
    parser.set_defaults(color=False)
    parser.set_defaults(report=False)
    parser.set_defaults(verbose=True)

    # Which file(s) to check.
    parser.add_option(
        "-f",
        "--file",
        action='append',
        dest="filename",
        help="comma-separated list of files to check",
        metavar="FILE[S]")

    # How much to poop out to the screen.
    parser.add_option(
        "-v",
        "--verbose",
        action='store_true',
        dest='verbose',
        help="provide verbose output",
        default=True)
    parser.add_option(
        "-q",
        "--quiet",
        action='store_false',
        dest='verbose',
        help="provide less verbose output")

    # Which checkers to run.
    parser.add_option(
        "--format",
        action='store_true',
        dest='formats',
        help="check (and optionally fix) the formatting of the "
        "code using yapf")
    parser.add_option(
        "--import",
        action='store_true',
        dest='imports',
        help="check (and optionally fix) the order/grouping of "
        "imports using isort")
    parser.add_option(
        "--manifest",
        action='store_true',
        dest='manifest',
        help="check the MANIFEST.in file for proper content "
        "using check-manifest")
    parser.add_option(
        "--quality",
        action='store_true',
        dest='quality',
        help="check the quality/style of the code using one "
        "or more checkers from flake8, pycodestyle, "
        "pydocstyle, pylint")
    parser.add_option(
        "--checkers",
        action='append',
        dest='checkers',
        help="comma-separated list of checkers to use for "
        "quality checks",
        metavar="<flake8,pycodestyle,pydocstyle,pylint>")
    parser.add_option(
        "--security",
        action='store_true',
        dest='security',
        help="check for potential security vulnerabilities "
        "using bandit")

    # Which files to (not) check.
    parser.add_option(
        "-i",
        "--ignore",
        action='append',
        type='string',
        dest='ignore',
        help="comma-separated list of files or directories to "
        "exclude (bandit, flake8, pycodestyle, pylint, "
        "yapf)",
        metavar="<file[,file...]> or <patterns>")

    # How to present the output.
    parser.add_option(
        "-c",
        "--color",
        action='store_true',
        dest='color',
        help="colorize outputs if color is supported (pylint)")
    parser.add_option(
        "-d",
        "--diff",
        action='store_false',
        dest='auto',
        help="just print a diff for the fixed source code "
        "(flake8, isort, pycodestyle, yapf)")
    parser.add_option(
        "--output-format",
        action='store',
        type='string',
        dest='output_format',
        help="select output format "
        "(csv,html,json,screen,txt,xml) (bandit), "
        "(default, pylint) (flake8), "
        "(colorized, json, text) (pylint)",
        metavar="<format>")

    # Where to put the output.
    parser.add_option(
        "--files-output",
        action='store',
        type='string',
        dest='files_output',
        help="redirect report to OUTPUT_FILE (bandit, flake8) "
        "or into files rather than stdout (pylint)",
        default="n",
        metavar="=<OUTPUT_FILE> or <y_or_n>")
    parser.add_option(
        "--reports",
        action='store_true',
        dest='reports',
        help="display full report or only a summary (pylint)")

    # How to run the checkers.
    parser.add_option(
        "-a",
        "--auto",
        action='store_true',
        dest='auto',
        help="automatically (in-line) apply recommended "
        "changes (isort, yapf)")
    parser.add_option(
        "-b",
        "--benchmark",
        action='store_false',
        dest='benchmark',
        help="benchmark code (flake8, pycodestyle)")
    parser.add_option(
        "--python3",
        action='store_false',
        dest='python3',
        help="analyze code for python3 required fixes")
    parser.add_option(
        "--parallel=<num>",
        action='store',
        type="int",
        dest='parallel',
        help="use <num> sub-processes (flake8, pylint, yapf)",
        default=1)
    parser.add_option(
        "-r",
        "--recursive",
        action='store_true',
        dest='recurse',
        help="run recursively over directories (bandit, isort, pylint, yapf)")

    parser.set_usage("StaticCheck <checks> <options ...> [file(s) ...]")
    parser.epilog = """\
    <checks> are one or more of the following
        |--format|--import|--manifest|--quality|--security|
    <options ...> are one or more options above.\
    """

    options, args = parser.parse_args()

    return options, args


def do_find_files():
    """Search under cwd for all python files."""
    modules = []
    scripts = []

    print("Finding python (*.py) files...")
    skipdirs = ["./.git", "./.tox"]
    for root, dirs, files in os.walk("."):
        if root in modules:
            continue

        if root != "." and ".git" in dirs:
            # Don't descend into other git repos
            skipdirs.append(root)

        do_skip = False
        for skip in skipdirs:
            if root == skip or root.startswith(skip + "/"):
                do_skip = True
                break
        if do_skip:
            continue

        if "__init__.py" in files:
            modules.append(root)
            continue

        for filename in [os.path.join(root, f) for f in files]:
            if os.path.islink(filename):
                continue
            if "Python script" in subprocess.check_output(
                ["/usr/bin/file", filename]):
                scripts.append(filename)

    files = [(f.startswith("./") and f[2:] or f) for f in scripts + modules]

    return files


def get_default_apps():
    """
    Try to determine the default executable paths.

    :returns: (yapf bin name, isort bin name, bandit bin name, flake8 bin name,
               pycodestyle bin name, pydocstyle bin name, pylint bin name,
               check-manifest bin name)
    """

    def which(exe):
        """
        Find the absolute path to the executable.

        :param str exe: the name of the executable file to find.
        """
        # First check the virtualenv for the executable.
        for path in VIRTBIN.split(os.pathsep):
            if os.path.exists(os.path.join(path, exe)):
                return os.path.join(path, exe)

        # Next, check the user's local install (if any).
        for path in LOCALBIN.split(os.pathsep):
            if os.path.exists(os.path.join(path, exe)):
                return os.path.join(path, exe)

        # Finally, check for a system-level executable.
        for path in SYSBIN.split(os.pathsep):
            if os.path.exists(os.path.join(path, exe)):
                return os.path.join(path, exe)

        return None

    yapf = which("yapf")
    isort = which("isort")
    bandit = which("bandit")
    flake8 = which("flake8")
    pycodestyle = which("pycodestyle")
    pydocstyle = which("pydocstyle")
    pylint = which("pylint")
    check_manifest = which("check-manifest")

    return (yapf, isort, bandit, flake8, pycodestyle, pydocstyle, pylint,
            check_manifest)


def _do_yapf(yapf, files, options):
    """
    Execute yapf.

    Uses setup.cfg in RTK's root directory.  Command line options override the
    configuration settings in setup.cfg.

    Default commandline options from setup.cfg for yapf are:
        --style pep8

    Exit codes for yapf...

    :param str yapf: the absolute path to the yapf executable
    :param str files: list of files to yapf.
    :param options: the options passed on the command line
    :return:
    :rtype:
    """
    _yapf = "{0:s} --style=pep8 ".format(yapf)

    # Build up the options for yapf.
    if options.verbose:
        _yapf += "-vv "
    if options.auto:
        _yapf += "--in-place "
    else:
        _yapf += "--diff "
    if options.ignore:
        _yapf += "--exclude {0:s} ".format(options.ignore)
    if options.parallel:
        _yapf += "--parallel "
    if options.recurse:
        _yapf += "--recursive "

    _yapf += " ".join(files)

    os.system(_yapf)


def _do_isort(isort, files, options):
    """
    Execute isort.

    Uses setup.cfg in RTK's root directory.  Command line options override the
    configuration settings in setup.cfg.

    isort puts all import statements at the top of the file grouped as follows:
        Future
        Python Standard Library
        Third Party
        Current Python Project
        Explicitly Local (. before import, as in: from . import x)
        Custom Separate Sections (Defined by forced_separate list in
                                  configuration file)
        Custom Sections (Defined by sections list in configuration file)

    Default commandline options from setup.cfg for isort are:
        -e (balanced wrapping)

    Exit codes for isort...
        0    no error

    :param str isort: the absolute path to the isort executable
    :param str files: list of files to isort.
    :param options: the options passed on the command line.
    :return:
    :rtype:
    """
    _isort = "{0:s} ".format(isort)

    # Build up the options for isort.
    if options.verbose:
        _isort += "-v "
    if options.auto:
        _isort += "--atomic "
    else:
        _isort += "--diff "
    if options.recurse:
        _isort += "-rc "

    _isort += " ".join(files)

    os.system(_isort)


def _do_bandit(bandit, files, options):
    """
    Execute bandit.

    Uses setup.cfg in RTK's root directory.  Command line options override the
    configuration settings in setup.cfg.

    Default commandline options from setup.cfg for bandit are:
        --exclude /tests, /icons

    Exit codes for isort...
        0    no error

    :param str bandit: the absolute path to the bandit executable
    :param str files: list of files to bandit.
    :param options: the options passed on the command line.
    :return:
    :rtype:
    """
    _bandit = "{0:s} ".format(bandit)

    # Build up the options for bandit.
    if options.verbose:
        _bandit += "-s B307 --verbose "
    if options.files_output != "n":
        _bandit += "--output {0:s} ".format(options.files_output)
    if options.ignore:
        _bandit += "--exclude {0:s} ".format(options.ignore)
    if options.output_format is not None:
        _bandit += "--format {0:s} ".format(options.output_format)
    else:
        _bandit += "--format txt "
    if options.recurse:
        _bandit += "--recursive "

    _bandit += " ".join(files)

    os.system(_bandit)


def _do_flake8(flake8, files, options):
    """
    Execute flake8.

    Uses setup.cfg in RTK's root directory.  Command line options override the
    configuration settings in setup.cfg.

    Default commandline options from setup.cfg for flake8 are:
        --count
        --exclude=.git,.tox,*.pyc,*.pyo,build,dist,docs
        --format=pylint
        --ignore=D203
        --max-complexity=10
        --statistics

    Exit codes for flake8...

    :param str flake8: the absolute path to the flake8 executable
    :param str files: list of files to flake8.
    :param options: the options passed on the command line
    :return:
    :rtype:
    """
    _flake8 = "{0:s} --statistics ".format(flake8)

    # Build up the options for flake8.
    if options.verbose:
        _flake8 += "-v "
    else:
        _flake8 += "-q "
    if options.benchmark:
        _flake8 += "--benchmark "
    if not options.auto:
        _flake8 += "--diff "
    if options.files_output != "n":
        _flake8 += "--output-files={0:s} ".format(options.files_output)
    if options.ignore is not None:
        _flake8 += "--exclude={0:s} ".format(options.ignore)
    if options.parallel > 1:
        _flake8 += "--jobs={0:d} ".format(options.parallel)

    _flake8 += " ".join(files)

    os.system(_flake8)


def _do_pycodestyle(pycodestyle, files, options):
    """
    Execute pycodestyle.

    Uses setup.cfg in RTK's root directory.  Command line options override the
    configuration settings in setup.cfg.

    Default commandline options from setup.cfg for pycodestyle are:
        --count
        --exclude=.git,.tox,*.pyc,*.pyo
        --ignore=E0121,E0123,E0133,E0242,W0503
        --max-line-length=79
        --statistics

    Exit codes for pycodestyle...
         0    no error

    :param str pycodestyle: the absolute path to the pycodestyle executable.
    :param str files: list of files to pycodestyle.
    :param options: the options passed on the command line.
    :return:
    :rtype:
    """
    _pycodestyle = "{0:s} ".format(pycodestyle)

    # Build up the options for pycodestyle.
    if options.verbose:
        _pycodestyle += "-v "
    else:
        _pycodestyle += "-q "
    if options.benchmark:
        _pycodestyle += "--benchmark "
    if not options.auto:
        _pycodestyle += "--diff "
    if options.ignore is not None:
        _pycodestyle += "--exclude={0:s} ".format(options.ignore)

    _pycodestyle += " ".join(files)

    os.system(_pycodestyle)


def _do_pydocstyle(pydocstyle, files, options):
    """
    Execute pydocstyle.

    Uses setup.cfg in RTK's root directory.  Command line options override the
    configuration settings in setup.cfg.

    Exit codes for pydocstyle...
         0    no error
         1    some code violations were found
         2    illegal usage

    :param str pydocstyle: the absolute path to the pydocstyle executable.
    :param str files: list of files to pydocstyle.
    :param options: the options passed on the command line.
    :return:
    :rtype:
    """
    _pydocstyle = "{0:s} --count ".format(pydocstyle)

    # Build up the options for pydocstyle.
    if options.verbose:
        _pydocstyle += "-v "

    _pydocstyle += " ".join(files)

    os.system(_pydocstyle)


def _do_pylint(pylint, files, options):
    """
    Execute pylint.

    Uses .pylintrc in RTK's root directory.  Command line options override the
    configuration settings in .pyltintrc.

    Exit codes for pylint...
         0    no error
         1    fatal message issued
         2    error message issued
         4    warning message issued
         8    refactor message issued
        16    convention message issued
        32    usage error

    :param str pylint: the absolute path to the pylint executable.
    :param str files: list of files to pylint.
    :param options: the options passed on the command line.
    :return:
    :rtype:
    """
    _pylint = "{0:s} --rcfile={1:s} ".format(pylint, PYLINTRC)

    # Build up the options for pylint.
    if options.color:
        _pylint += "--output-format=colorized "
    elif options.output_format is not None:
        _pylint += "--output-format={0:s} ".format(options.output_format)
    if options.files_output != "n":
        _pylint += "--files-output=y "
    if options.ignore is not None:
        _pylint += "--ignore={0:s} ".format(options.ignore)
    if options.parallel > 1:
        _pylint += "--jobs={0:d} ".format(options.parallel)
    if not options.reports:
        _pylint += "--reports=no "

    _pylint += " ".join(files)

    os.system(_pylint)


def _do_check_manifest(check_manifest, options):
    """Execute check-manifest."""
    _check_manifest = "{0:s} ".format(check_manifest)

    if options.auto:
        _check_manifest += "-u "
    if options.verbose:
        _check_manifest += "-v "

    _check_manifest += " "
    _check_manifest += ROOT

    os.system(_check_manifest)


def main():
    """
    Entry for executing static checks.

    Formatting:
      yapf
      isort

    Security vulnerabilities:
      bandit

    Code quality/style checks:
      flake8
      pylint  # Also allows creation of UML diagrams with pyreverse
      pycodestyle
      pydocstyle

    MANIFEST checks:
      check-manifest

    1. Format the code (yapf and/or isort)
    2. Check code for potential security vulnerabilities (bandit)
    3. Check the quality/style of the code (flake8, pycodestyle, pydocstyle,
       and/or pylint)
    4. Verify the MANIFEST.in file (check-manifest)
    """
    options, __ = do_parse_args()

    # Get the list of files to check.
    files = options.filename
    if not files and (options.formats or options.imports or options.quality
                      or options.security):
        files = do_find_files()

    # Find the absolute path to the executables.
    (yapf, isort, bandit, flake8, pycodestyle, pydocstyle, pylint,
     manifest) = get_default_apps()

    # Execute the checks.
    if options.formats:
        _do_yapf(yapf, files, options)

    if options.imports:
        _do_isort(isort, files, options)

    if options.security:
        _do_bandit(bandit, files, options)

    if options.quality:
        for checker in options.checkers:
            if checker == "flake8":
                _do_flake8(flake8, files, options)
            if checker == "pylint":
                _do_pylint(pylint, files, options)
            if checker == "pycodestyle":
                _do_pycodestyle(pycodestyle, files, options)
            if checker == "pydocstyle":
                _do_pydocstyle(pydocstyle, files, options)

    if options.manifest:
        _do_check_manifest(manifest, options)


if __name__ == '__main__':
    sys.exit(main())
