#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       setup.py is part of the RTK Project
#
#       Copyright (C) 2007-2013 Andrew "Weibullguy" Rowland <darowland@ieee.org>

"""
Setup script for RTK.

Run 'python setup.py develop' to set up a development environment, including
dependencies.
"""
# TODO: Create a binary installer for Linux.

try:
    from setuptools import setup, find_packages
except ImportError:
    print "Using ez_setup"
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

import getopt
import os
import platform

from pkg_resources import require
from sys import argv, version
from distutils.core import setup, Command
from distutils.sysconfig import get_config_vars
from distutils.command.install import install, INSTALL_SCHEMES

if version < "2.2.3":
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

python_version = platform.python_version()[0:3]

_version = "1.0.0-alpha"

_confdir = "/etc/RTK"
_datadir = "/usr/share/RTK"
_icondir = "/usr/share/pixmaps"

class install_dev_docs(Command):

    description = "Builds the developer documents in HTML or PDF format"

    user_options = [
        ('doc-type=', None,
         "whether to install html (default) or pdf documentation."),
        ('doc-path=', None,
         "path to install documentation (defaults to /usr/share/doc/RTK-" + _version + "/developer")
        ]

    def initialize_options(self):
        self.doc_type = "html"
        self.doc_path = "/usr/share/doc/RTK-" + _version + "/developer"

    def finalize_options(self):
        if(self.doc_type == "pdf"):
            self.doc_type = "pdf"
        elif(self.doc_type == None):
            self.doc_type = "html"
        else:
            print "Unknown documentation type %s.  Installing html documentation." % self.doc_type
            self.doc_type = "html"

        self.doc_path = "%s/%s" % (self.doc_path, self.doc_type)

    def run(self):

        import os
        import distutils.file_util

        cwd = os.getcwd()

        if(not os.path.exists(self.doc_path)):
            os.makedirs(self.doc_path)

        for root, dirs, files in os.walk("%s/docs/developer/%s/" % (cwd, self.doc_type)):
            if '.svn' in dirs:
                dirs.remove('.svn')
            if '.git' in dirs:
                dirs.remove('.git')
            if(self.doc_type == "pdf"):
                files = filter(lambda x: 'pdf' in x, files)
            for f in files:
                distutils.file_util.copy_file(os.path.join(root, f), self.doc_path)

class install_user_docs(Command):

    description = "Installs the user documents in HTML or PDF format"

    user_options = [
        ('doc-type=', None,
         "whether to install html (default) or pdf documentation."),
        ('doc-path=', None,
         "path to install documentation (defaults to /usr/share/doc/RTK-" + _version + "/user"),
        ('models', 'm',
         "install documentation related to hazard rate models supported by RTK."),
        ('specs', 's',
         "install MIL-SPECS for components supported by RTK.")
        ]

    boolean_options = ['models', 'specs']

    def initialize_options(self):
        self.doc_type = "html"
        self.doc_path = "/usr/share/doc/RTK-" + _version + "/user"

        self.models = False
        self.specs = False

    def finalize_options(self):
        if(self.doc_type == "pdf"):
            self.doc_type = "pdf"
        elif(self.doc_type == None):
            self.doc_type = "html"
        else:
            print "Unknown documentation type %s.  Installing html documentation." % self.doc_type
            self.doc_type = "html"

    def run(self):

        import os
        import distutils.file_util

        cwd = os.getcwd()

        docpath = "%s/%s" % (self.doc_path, self.doc_type)

        if(not os.path.exists(docpath)):
            os.makedirs(docpath)

        for root, dirs, files in os.walk("%s/docs/user/%s/" % (cwd, self.doc_type)):
            if '.svn' in dirs:
                dirs.remove('.svn')
            if(self.doc_type == "pdf"):
                files = filter(lambda x: 'pdf' in x, files)
            for f in files:
                distutils.file_util.copy_file(os.path.join(root, f), self.doc_path)

        if(self.models):
            path = "%s/models/" % self.doc_path
            if(not os.path.exists(path)):
                os.makedirs(path)
            for root, dirs, files in os.walk("%s/docs/user/models/" % cwd):
                if '.svn' in dirs:
                    dirs.remove('.svn')
                for d in dirs:
                    if(not os.path.exists("%s/%s" % (path, d))):
                        os.makedirs("%s/%s" % (path, d))
                for f in files:
                    distutils.file_util.copy_file(os.path.join(root, f), "%s/%s" % (path, d))

        if(self.specs):
            path = "%s/specs/" % self.doc_path
            if(not os.path.exists(path)):
                os.makedirs(path)
            for root, dirs, files in os.walk("%s/docs/user/specs/" % cwd):
                if '.svn' in dirs:
                    dirs.remove('.svn')
                for d in dirs:
                    if(not os.path.exists("%s/%s" % (path, d))):
                        os.makedirs("%s/%s" % (path, d))
                for f in files:
                    distutils.file_util.copy_file(os.path.join(root, f), "%s/%s" % (path, d))

_package_data={"relkit": [""],
               "relkit": ["config/*.conf"],
               "relkit": ["config/*.xml"],
               "relkit": ["config/icons/16x16/*.png"],
               "relkit": ["config/icons/32x32/*.png"]}

_data_files = [("%s/RTK/32x32" % _icondir, ["config/icons/32x32/add.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/assembly.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/calculate.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/charts.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/copy.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/cut.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/db-connected.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/db-disconnected.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/delete.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/edit.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/exit.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/import.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/new.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/open.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/overstress.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/part.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/paste.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/redo.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/remove.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/reports.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/save.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/save-exit.png"]),
               ("%s/RTK/32x32" % _icondir, ["config/icons/32x32/undo.png"]),
               (_icondir, ["config/icons/RTK.png"]),
               ("%s" % _confdir, ["config/site.conf"]),
               ("%s" % _confdir, ["config/RTK.conf"]),
               ("%s" % _confdir, ["config/dataset_format.xml"]),
               ("%s" % _confdir, ["config/fmeca_format.xml"]),
               ("%s" % _confdir, ["config/function_format.xml"]),
               ("%s" % _confdir, ["config/hardware_format.xml"]),
               ("%s" % _confdir, ["config/incident_format.xml"]),
               ("%s" % _confdir, ["config/part_format.xml"]),
               ("%s" % _confdir, ["config/requirement_format.xml"]),
               ("%s" % _confdir, ["config/revision_format.xml"]),
               ("%s" % _confdir, ["config/risk_format.xml"]),
               ("%s" % _confdir, ["config/sia_format.xml"]),
               ("%s" % _confdir, ["config/software_format.xml"]),
               ("%s" % _confdir, ["config/testing_format.xml"]),
               ("%s" % _confdir, ["config/validation_format.xml"]),
               ("%s/examples" % _datadir, ["config/example1.sql"]),
               ("%s/data" % _datadir, ["config/newprogram_mysql.sql"]),
               ("%s/data" % _datadir, ["config/newprogram_sqlite3.sql"]),
               ("%s/data" % _datadir, ["config/rtkcom.sql"]),
               ("/usr/share/doc/RTK-" + _version, ["AUTHORS","ChangeLog","COPYING"]),
               ("/usr/share/applications", ["RTK.desktop"]),
              ]

_cmdclass = {'install_dev_docs': install_dev_docs,
             'install_user_docs': install_user_docs,
            }

# Packages needed to install and run RTK.
_requires = ["lxml >= 2.3",
             # "PyGTK > 2.12.0", - Exclude, it doesn't seem to work.
             "matplotlib >= 1.1.1",
             "mysql-python >= 1.2.3",
             "xlrd >= 0.9.0", 'pygtk']

_entry_points = {"gui": ["RTK = rtk.main:main"]}

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

def linux_check():
    return platform.system() == "Linux"

def windows_check():
    return platform.system() in ('Windows', 'Microsoft')

def osx_check():
    return platform.system() == "Darwin"

setup(
    name = "RTK",
    version = _version,
    author = "Andrew Rowland",
    author_email = "andrew.rowland@reliaqual.com",
    maintainer = "Andrew Rowland",
    maintainer_email = "andrew.rowland@reliaqual.com",
    url = "http://rtk.reliaqual.com",
    description = "RAM Analyses Tools",
    long_description = """RTK is a Python and PyGTK based suite of tools to assist in Reliability, Availability, Maintainability, and Safety (RAMS) analyses.""",
    download_url = "",
    platforms = "Linux",
    license = "Proprietary",
    cmdclass = _cmdclass,
    install_requires = _requires,
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    package_data = _package_data,
    data_files = _data_files,
    entry_points = _entry_points
    )
