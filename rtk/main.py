#!/usr/bin/env python
"""
This is the main program for the RTK application.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       main.py is part of the RTK Project
#
# All rights reserved.

import datetime
import getpass
import gettext
import logging
import os
import sys

import configuration as _conf
from dataset import Dataset
from function import Function
from hardware import Hardware
from incident import Incident
import mysql as _mysql
import notebook as _note
import partlist as _parts
from requirement import Requirement
from revision import Revision
from software import Software
import sqlite as _sqlite
from testing import Testing
import tree as _tree
import utilities as _util
from validation import Validation


# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)


# We need to explicitly import the following module otherwise pyinstaller
# won't pick it up and add it to the executable on Windows.
if os.name == 'nt':
    from scipy.sparse.csgraph import _validation    # pylint: disable=W0611

# Add localization support.
_ = gettext.gettext


def main():
    """ This is the main function for the RTK application. """

    RTK()

    gtk.main()

    return 0


class RTK(object):
    """ This is the RTK class. """

    def __init__(self):

        # Set the gtk+ theme on Windows.
        if sys.platform.startswith('win'):
            # These themes perform well on Windows.
            # Amaranth
            # Aurora
            # Bluecurve
            # Blueprint
            # Blueprint-Green
            # Candido-Calm
            # CleanIce
            # CleanIce - Dark
            # Clearlooks
            # Metal
            # MurrinaBlue
            # Nodoka-Midnight
            # Rezlooks-Snow

            # These themes perform poorly.
            # Bluecurve-BerriesAndCream
            # MurrinaChrome
            gtk.rc_parse("C:\\Program Files (x86)\\Common Files\\GTK\\2.0\\share\\themes\\MurrinaBlue\\gtk-2.0\\gtkrc")

        self.ProgCnx = None

        # Import the test data file if we are executing in developer mode.
        if len(sys.argv) > 1 and sys.argv[1] == 'devmode':
            _conf.MODE = 'developer'

        # Read the configuration file.
        _util.read_configuration()

        if os.name == 'posix':
            _conf.OS = 'Linux'
        elif os.name == 'nt':
            _conf.OS = 'Windows'

        # Create loggers for the application.  The first is to store log
        # information for RTK developers.  The second is to log errors for the
        # user.  The user can use these errors to help find problems with their
        # inputs and sich.
        __user_log = _conf.LOG_DIR + '/RTK_user.log'
        __error_log = _conf.LOG_DIR + '/RTK_error.log'
        __import_log = _conf.LOG_DIR + '/RTK_import.log'

        if not _util.dir_exists(_conf.LOG_DIR):
            os.makedirs(_conf.LOG_DIR)

        if _util.file_exists(__user_log):
            os.remove(__user_log)
        if _util.file_exists(__error_log):
            os.remove(__error_log)
        if _util.file_exists(__import_log):
            os.remove(__import_log)

        self.debug_log = _util.create_logger("RTK.debug", logging.DEBUG,
                                             __error_log)
        self.user_log = _util.create_logger("RTK.user", logging.WARNING,
                                            __user_log)
        self.import_log = _util.create_logger("RTK.import", logging.WARNING,
                                              __import_log)

        self.LOADED = False
        self.partlist = {}

        # Find out who is using RTK and when.
        self._UID = getpass.getuser()
        self._TODAY = datetime.datetime.now()
        self.DATE = "1970-01-01"

        # Get a connection to the common database.
        if _conf.COM_BACKEND == 'mysql':
            self.COMDB = _mysql.MySQLInterface(self)
            self.ComCnx = self.COMDB.get_connection(_conf.RTK_COM_INFO)

        elif _conf.COM_BACKEND == 'sqlite3':
            self.COMDB = _sqlite.SQLite3Interface(self)
            _database = _conf.CONF_DIR + _conf.RTK_COM_INFO[2] + '.rfb'
            self.ComCnx = self.COMDB.get_connection(_database)

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = _conf.DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            _util.rtk_error(_(u"Cannot find your license file in %s.  If "
                              u"your license file is elsewhere, please place "
                              u"it in %s." % (_conf.DATA_DIR, _conf.DATA_DIR)))
            quit()

        _license_key = _license_file.readline().rstrip('\n')
        _license_file.close()

        _query = "SELECT fld_product_key, fld_expire_date \
                  FROM tbl_site_info"
        _results = self.COMDB.execute_query(_query,
                                            None,
                                            self.ComCnx)
        if _license_key != _results[0][0]:
            _util.rtk_error(_(u"Invalid license (Invalid key).  Your license "
                              u"key is incorrect.  Closing the RTK "
                              u"application."))
            quit()

        if datetime.datetime.today().toordinal() > _results[0][1]:
            _expire_date = str(datetime.datetime.fromordinal(int(
                _results[0][1])).strftime('%Y-%m-%d'))
            _util.rtk_error(_(u"Invalid license (Expired).  Your license "
                              u"expired on %s.  Closing RTK application." %
                              _expire_date))
            quit()

        # Get a connection to the program database.
        if _conf.BACKEND == 'mysql':
            self.DB = _mysql.MySQLInterface(self)

        elif _conf.BACKEND == 'sqlite3':
            self.DB = _sqlite.SQLite3Interface(self)

        # Create the GUI and objects for each of the RTK classes.
        self.winWorkBook = _note.WorkBookWindow(self)

        # Create each of the modules.
        self.REVISION = Revision(self)
        self.REQUIREMENT = Requirement(self)
        self.FUNCTION = Function(self)
        self.HARDWARE = Hardware(self)
        self.SOFTWARE = Software(self)
        self.VALIDATION = Validation(self)
        self.INCIDENT = Incident(self)
        #self.COMPONENT = Component(self)
        self.DATASET = Dataset(self)
        self.TESTING = Testing(self)

        self.winTree = _tree.TreeWindow(self)
        self.winParts = _parts.ListWindow(self)

        self.icoStatus = gtk.StatusIcon()
        icon = _conf.ICON_DIR + '32x32/db-disconnected.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        self.icoStatus.set_from_pixbuf(icon)
        self.icoStatus.set_tooltip(_(u"RTK is not currently connected to a "
                                     u"program database."))

        self.winTree.present()

    def load_system(self):
        """
        This method loads the RTK development program database the
        user opens.
        """

        _util.set_cursor(self, gtk.gdk.WATCH)
        self.winTree.statusbar.push(2, _(u"Opening Program Database..."))

        # Get a connection to the program database and then retrieve the
        # program information.
        query = "SELECT * FROM tbl_program_info"
        if _conf.BACKEND == 'mysql':
            self.ProgCnx = self.DB.get_connection(_conf.RTK_PROG_INFO)
        elif _conf.BACKEND == 'sqlite3':
            self.ProgCnx = self.DB.get_connection(_conf.RTK_PROG_INFO[2])

        results = self.DB.execute_query(query, None, self.ProgCnx)

        _query_ = "SELECT fld_revision_prefix, fld_revision_next_id, \
                          fld_function_prefix, fld_function_next_id, \
                          fld_assembly_prefix, fld_assembly_next_id, \
                          fld_part_prefix, fld_part_next_id, \
                          fld_fmeca_prefix, fld_fmeca_next_id, \
                          fld_mode_prefix, fld_mode_next_id, \
                          fld_effect_prefix, fld_effect_next_id, \
                          fld_cause_prefix, fld_cause_next_id, \
                          fld_software_prefix, fld_software_next_id \
                   FROM tbl_program_info"
        _results_ = self.DB.execute_query(_query_, None, self.ProgCnx)

        _conf.RTK_PREFIX = [_element_ for _element_ in _results_[0]]

        # Find which modules are active in this project.
        _query = "SELECT fld_revision_active, fld_function_active, \
                         fld_requirement_active, fld_hardware_active, \
                         fld_software_active, fld_vandv_active, \
                         fld_testing_active, fld_fraca_active, \
                         fld_survival_active, fld_rcm_active, \
                         fld_rbd_active, fld_fta_active\
                  FROM tbl_program_info"
        _results = self.DB.execute_query(_query, None, self.ProgCnx)[0]

        for i in range(len(_results)):
            _conf.RTK_MODULES.append(_results[i])
            if _results[i] == 1:
                _conf.RTK_PAGE_NUMBER.append(i)

        _conf.METHOD = results[0][36]

        icon = _conf.ICON_DIR + '32x32/db-connected.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        self.icoStatus.set_from_pixbuf(icon)
        self.icoStatus.set_tooltip(_(u"RTK is connected to program database "
                                     u"%s." % _conf.RTK_PROG_INFO[2]))
        self.winTree.set_title(_(u"RTK - Analyzing %s" %
                                 _conf.RTK_PROG_INFO[2]))

        self.winTree.load_trees(self)

        if _conf.RTK_MODULES[0] == 1:       # Revisions
            self.REVISION.treeview.grab_focus()
        elif _conf.RTK_MODULES[1] == 1:     # Functions
            self.FUNCTION.treeview.grab_focus()
        elif _conf.RTK_MODULES[2] == 1:     # Requirements
            self.REQUIREMENT.treeview.grab_focus()
        elif _conf.RTK_MODULES[3] == 1:     # Hardware
            self.HARDWARE.load_tree()
        elif _conf.RTK_MODULES[4] == 1:     # Software
            self.SOFTWARE.load_tree()
        elif _conf.RTK_MODULES[5] == 1:     # V&V Tracking
            self.VALIDATION.treeview.grab_focus()
        elif _conf.RTK_MODULES[6] == 1:     # Reliability Testing
            self.TESTING.treeview.grab_focus()
        elif _conf.RTK_MODULES[7] == 1:     # Field incident tracking
            self.INCIDENT.treeview.grab_focus()
        elif _conf.RTK_MODULES[8] == 1:     # Survival analysis
            self.DATASET.treeview.grab_focus()

        self.LOADED = True

        self.winTree.statusbar.pop(2)

        _util.set_cursor(self, gtk.gdk.LEFT_PTR)

if __name__ == '__main__':

    main()
