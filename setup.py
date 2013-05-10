#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       setup.py is part of The RelKit Project
#
#       Copyright (C) 2007-2011 Andrew "Weibullguy" Rowland <darowland@ieee.org>
#
# All rights reserved
#
# RelKit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RelKit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RelKit.  If not, see <http://www.gnu.org/licenses/>.

""" Setup script for RelKit.

    Run 'python setup.py develop' to set up a development environment,
    including dependencies.

"""

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

_version = "0.3.0"

if(os.name == "posix"):
    _icondir = "/usr/share/pixmaps"
elif(os.name == "nt"):
    _icondir = "icons"

class install_dev_docs(Command):

    description = "builds the developer documents in HTML or PDF format"

    user_options = [
        ('doc-type=', None,
         "whether to install html (default) or pdf documentation."),
        ('doc-path=', None,
         "path to install documentation (defaults to /usr/share/doc/relkit-" + _version + "/developer")
        ]

    def initialize_options(self):
        self.doc_type = "html"
        self.doc_path = "/usr/share/doc/relkit-" + _version + "/developer"

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
            if(self.doc_type == "pdf"):
                files = filter(lambda x: 'pdf' in x, files)
            for f in files:
                distutils.file_util.copy_file(os.path.join(root, f), self.doc_path)

class install_user_docs(Command):

    description = "installs the user documents in HTML or PDF format"

    user_options = [
        ('doc-type=', None,
         "whether to install html (default) or pdf documentation."),
        ('doc-path=', None,
         "path to install documentation (defaults to /usr/share/doc/relkit-" + _version + "/user"),
        ('models', 'm',
         "install documentation related to hazard rate models supported by RelKit."),
        ('specs', 's',
         "install MIL-SPECS for components supported by RelKit.")
        ]

    boolean_options = ['models', 'specs']

    def initialize_options(self):
        self.doc_type = "html"
        self.doc_path = "/usr/share/doc/relkit-" + _version + "/user"

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

_data_files=[("%s/relkit/32x32" % _icondir, ["config/icons/32x32/add.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/assembly.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/calculate.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/charts.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/copy.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/cut.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/db-connected.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/db-disconnected.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/delete.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/edit.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/exit.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/import.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/new.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/open.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/overstress.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/part.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/paste.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/redo.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/remove.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/reports.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/save.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/save-exit.png"]),
             ("%s/relkit/32x32" % _icondir, ["config/icons/32x32/undo.png"]),
             (_icondir, ["config/icons/RelKit.png"]),
             ("/etc/relkit", ["config/site.conf"]),
             ("/etc/relkit", ["config/relkit.conf"]),
             ("/etc/relkit", ["config/fmeca_format.xml"]),
             ("/etc/relkit", ["config/fraca_format.xml"]),
             ("/etc/relkit", ["config/function_format.xml"]),
             ("/etc/relkit", ["config/hardware_format.xml"]),
             ("/etc/relkit", ["config/part_format.xml"]),
             ("/etc/relkit", ["config/requirement_format.xml"]),
             ("/etc/relkit", ["config/revision_format.xml"]),
             ("/etc/relkit", ["config/sia_format.xml"]),
             ("/etc/relkit", ["config/validation_format.xml"]),
             ("share/relkit/examples", ["config/example1.sql"]),
             ("share/relkit", ["config/newprogram_mysql.sql"]),
             ("share/relkit", ["config/newprogram_sqlite3.sql"]),
             ("share/relkit", ["config/relkitcom.sql"]),
             ("share/doc/relkit-" + _version, ["AUTHORS","ChangeLog","COPYING"]),
             ("share/applications", ["RelKit.desktop"]),
             ]

_cmdclass = {'install_dev_docs': install_dev_docs,
             'install_user_docs': install_user_docs,
            }

# Packages needed to install and run RelKit
_requires = ["lxml >= 2.3",
             # "PyGTK > 2.12.0", - Exclude, it doesn't seem to work.
             "mysql-python >= 1.2.3"]

# Classifiers for PyPi
_classifiers=["Development Status :: 3 - Alpha",
              "Environment :: X11 Applications :: GTK",
              "Intended Audience :: End Users/Desktop",
              "Intended Audience :: Science/Research",
              "License :: OSI Approved :: GNU General Public License (GPL)",
              "Operating System :: POSIX :: Linux",
              "Programming Language :: Python :: 2.7",
              "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
             ]

entry_points={
              "gui": [
              "relkit = relkit.main:main"
              ]
}

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

def linux_check():
    return platform.system() == "Linux"

def windows_check():
    return platform.system() in ('Windows', 'Microsoft')

def osx_check():
    return platform.system() == "Darwin"

setup(
    name = "RelKit",
    version = _version,
    author = "Andrew Rowland",
    author_email = "darowland@ieee.org",
    maintainer = "Andrew Rowland",
    maintainer_email = "darowland@ieee.org",
    url = "http://sourceforge.net/apps/mediawiki/relkit/index.php?title=Main_Page",
    description = "RAM Analyses Tools",
    long_description = """RelKit is a Python and PyGTK based suite of tools to
                          assist in Reliability, Availability, Maintainability,
                          and Safety (RAMS) analyses. RelKit is intended to be
                          an Open Source alternative to proprietary RAMS analyses
                          solutions.""",
    download_url = "http://sourceforge.net/projects/relkit/",
    platforms = "Linux",
    license = "GPL3",
    cmdclass = _cmdclass,
    install_requires = _requires,
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    package_data = _package_data,
    data_files = _data_files,
    entry_points = """[console_scripts]
                      relkit = relkit.main:main
                   """,
    classifiers = _classifiers
    )
