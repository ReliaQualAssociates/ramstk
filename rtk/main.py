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

# from time import sleep

import configuration as _conf
import mysql as _mysql
import notebook as _note
import partlist as _parts
import sqlite as _sqlite
import tree as _tree
import utilities as _util

from dataset import Dataset
from function import Function
from hardware import Hardware
from incident import Incident
from requirement import Requirement
from revision import Revision
from software import Software
from testing import Testing
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
    """
    This is the main function for the RTK application.
    """

    # splScr = SplashScreen()

    # If you don't do this, the splash screen will show, but wont render it's
    # contents
    # while gtk.events_pending():
    #     gtk.main_iteration()

    # sleep(3)

    RTK()

    # splScr.window.destroy()

    gtk.main()

    return 0


class SplashScreen(object):
    """
    This is the splash screen class.
    """

    def __init__(self):

        # DO NOT connect 'destroy' event here!
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        _color = gtk.gdk.color_parse('#234fdb')
        self.window.modify_bg(gtk.STATE_NORMAL, _color)

        self.window.set_title('The Reliability ToolKit (RTK)')
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_resizable(True)
        self.window.set_deletable(False)
        self.window.set_decorated(False)
        self.window.set_skip_pager_hint(True)
        self.window.set_skip_taskbar_hint(True)

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.window.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.window.set_border_width(5)

        _vbox = gtk.VBox(False, 1)
        self.window.add(_vbox)

        # _image = gtk.Image()
        # _image.set_from_file("/home/andrew/.config/RTK/icons/ReliaFree.png")
        # _vbox.pack_start(_image, True, True)

        _label = gtk.Label(_(u"Copyright 2007 - 2014, Andrew Rowland"))
        _label.set_alignment(0, 0.5)
        _vbox.pack_start(_label, True, True)

        self.window.show_all()


class RTK(object):
    """
    This is the RTK class.
    """

    def __init__(self):

        self.ProgCnx = None
        self.LOADED = False
        self.partlist = {}

        self._read_configuration()

        (self.debug_log,
         self.user_log,
         self.import_log) = self._initialize_loggers()

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
            _database = _conf.SITE_DIR + '/' + _conf.RTK_COM_INFO[2] + '.rfb'
            self.ComCnx = self.COMDB.get_connection(_database)

        if self._validate_license():
            sys.exit(2)

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
        # self.ASSEMBLY = Assembly(self)
        # self.COMPONENT = Component(self)
        self.SOFTWARE = Software(self)
        self.VALIDATION = Validation(self)
        self.INCIDENT = Incident(self)
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

    def _read_configuration(self):
        """
        Method to read the site configuration and RTK configuration files.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

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

        # Import the test data file if we are executing in developer mode.
        if len(sys.argv) > 1 and sys.argv[1] == 'devmode':
            _conf.MODE = 'developer'

        # Read the configuration file.
        _util.read_configuration()

        if os.name == 'posix':
            _conf.OS = 'Linux'
        elif os.name == 'nt':
            _conf.OS = 'Windows'

        return False

    def _initialize_loggers(self):
        """
        Method to create loggers for the RTK application.

        :return: _debug_log, _user_log, _import_log
        :rtype: tuple
        """

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

        _debug_log = _util.create_logger("RTK.debug", logging.DEBUG,
                                         __error_log)
        _user_log = _util.create_logger("RTK.user", logging.WARNING,
                                        __user_log)
        _import_log = _util.create_logger("RTK.import", logging.WARNING,
                                          __import_log)

        return(_debug_log, _user_log, _import_log)

    def _validate_license(self):
        """
        Method to validate the license and the license expiration date.

        :return: False if successful or true if an error is encountered.
        :rtype: boolean
        """

        # Read the license file and compare to the product key in the site
        # database.  If they are not equal, quit the application.
        _license_file = _conf.DATA_DIR + '/license.key'
        try:
            _license_file = open(_license_file, 'r')
        except IOError:
            _util.rtk_warning(_(u"Cannot find license file %s.  "
                                u"If your license file is elsewhere, "
                                u"please place it in %s." %
                                (_license_file, _conf.DATA_DIR)))
            return True

        _license_key = _license_file.readline().rstrip('\n')
        _license_file.close()

        _query = "SELECT fld_product_key, fld_expire_date \
                  FROM tbl_site_info"
        _results = self.COMDB.execute_query(_query, None, self.ComCnx)

        if _license_key != _results[0][0]:
            _util.rtk_error(_(u"Invalid license (Invalid key).  Your license "
                              u"key is incorrect.  Closing the RTK "
                              u"application."))
            return True

        if datetime.datetime.today().toordinal() > _results[0][1]:
            _expire_date = str(datetime.datetime.fromordinal(int(
                _results[0][1])).strftime('%Y-%m-%d'))
            _util.rtk_error(_(u"Invalid license (Expired).  Your license "
                              u"expired on %s.  Closing RTK application." %
                              _expire_date))
            return True

        return False

    def load_system(self):
        """
        This method loads the RTK development program database the
        user opens.
        """

        _util.set_cursor(self, gtk.gdk.WATCH)
        self.winTree.statusbar.push(2, _(u"Opening Program Database..."))

        # Get a connection to the program database and then retrieve the
        # program information.
        _query = "SELECT * FROM tbl_program_info"
        if _conf.BACKEND == 'mysql':
            self.ProgCnx = self.DB.get_connection(_conf.RTK_PROG_INFO)
        elif _conf.BACKEND == 'sqlite3':
            self.ProgCnx = self.DB.get_connection(_conf.RTK_PROG_INFO[2])

        results = self.DB.execute_query(_query, None, self.ProgCnx)

        _query = "SELECT fld_revision_prefix, fld_revision_next_id, \
                         fld_function_prefix, fld_function_next_id, \
                         fld_assembly_prefix, fld_assembly_next_id, \
                         fld_part_prefix, fld_part_next_id, \
                         fld_fmeca_prefix, fld_fmeca_next_id, \
                         fld_mode_prefix, fld_mode_next_id, \
                         fld_effect_prefix, fld_effect_next_id, \
                         fld_cause_prefix, fld_cause_next_id, \
                         fld_software_prefix, fld_software_next_id \
                  FROM tbl_program_info"
        _results_ = self.DB.execute_query(_query, None, self.ProgCnx)

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

# TODO: Loading these trees is a hack.  Need to fix this once I understand WTF is going on.
        _query = "SELECT t1.*, t2.fld_part_number, t2.fld_ref_des \
                  FROM tbl_prediction AS t1 \
                  INNER JOIN tbl_system AS t2 \
                  ON t1.fld_assembly_id=t2.fld_assembly_id \
                  WHERE t2.fld_revision_id=%d" % self.REVISION.revision_id
        self.winParts.load_part_tree(_query)

        _query = "SELECT * FROM tbl_incident \
                  WHERE fld_revision_id=%d" % self.REVISION.revision_id
        self.winParts.load_incident_tree(_query)

        self.LOADED = True

        self.winTree.statusbar.pop(2)

        _util.set_cursor(self, gtk.gdk.LEFT_PTR)

if __name__ == '__main__':

    main()
