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
#       RTK.py is part of the RTK Project
#
# All rights reserved.

import datetime
import gettext
import logging
import os
import sys

try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)

from gui.gtk.mwi.ModuleBook import ModuleView
from gui.gtk.mwi.ListBook import ListView
from gui.gtk.mwi.WorkBook import WorkView

import configuration as _conf
import utilities as _util

from dao.DAO import DAO
from revision.Revision import Revision
from revision.ModuleBook import ModuleView as mvwRevision

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


def _read_configuration():
    """
    Method to read the site configuration and RTK configuration files.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
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


def _initialize_loggers():
    """
    Method to create loggers for the RTK application.

    :return: (_debug_log, _user_log, _import_log)
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


class RTK(object):
    """
    This is the RTK controller class.
    """

    def __init__(self):
        """
        Method to initialize the RTK controller.
        """
        RTK_INTERFACE = 1
        # Read the site configuration file.
        _read_configuration()

        # Connect to the site database.
        _database = _conf.SITE_DIR + '/' + _conf.RTK_COM_INFO[2] + '.rfb'
        self.dao = DAO(_database)

        # Create loggers.
        (self.debug_log,
         self.user_log,
         self.import_log) = _initialize_loggers()

        # Validate the license.
        if self._validate_license():
            sys.exit(2)

        # Create data controllers.
        self.dtcRevision = Revision()

        # Initialize RTK views.
        if RTK_INTERFACE == 0:       # Single window.
            pass
        else:                               # Multiple windows.
            self.module_book = ModuleView()
            self.list_book = self.module_book.create_listview()
            self.work_book = self.module_book.create_workview()

        # Plug-in each of the RTK module views.
        _modview = self.module_book.create_module_page(mvwRevision,
                                                       self.dtcRevision)
        _conf.RTK_MODULES.append(_modview)

        self.icoStatus = gtk.StatusIcon()
        _icon = _conf.ICON_DIR + '32x32/db-disconnected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 16, 16)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is not currently connected to a "
                                     u"program database."))
        self.open_project()
        self.module_book.present()

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
        (_results, _error_code, __) = self.dao.execute(_query, None)

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

    def open_project(self):
        """
        Method to open an RTK Prooject database and load it into the views.
        """

        self.module_book.statusbar.push(2, _(u"Opening Program Database..."))

        # Connect to the project database.
        _database = '/home/andrew/Analyses/RTK/AGCO/AxialCombine/AxialCombine.rtk'
        self.project_dao = DAO(_database)

        # Get a connection to the program database and then retrieve the
        # program information.
        _query = "SELECT * FROM tbl_program_info"

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
        (_results, _error_code, __) = self.project_dao.execute(_query,
                                                               commit=None)
        _conf.RTK_PREFIX = [_element for _element in _results[0]]

        _icon = _conf.ICON_DIR + '32x32/db-connected.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 16, 16)
        self.icoStatus.set_from_pixbuf(_icon)
        self.icoStatus.set_tooltip(_(u"RTK is connected to program database "
                                     u"%s." % _conf.RTK_PROG_INFO[2]))
        self.module_book.set_title(_(u"RTK - Analyzing %s" %
                                   _conf.RTK_PROG_INFO[2]))

        # Find which modules are active in this project.
        _query = "SELECT fld_revision_active, fld_function_active, \
                         fld_requirement_active, fld_hardware_active, \
                         fld_software_active, fld_vandv_active, \
                         fld_testing_active, fld_fraca_active, \
                         fld_survival_active, fld_rcm_active, \
                         fld_rbd_active, fld_fta_active\
                  FROM tbl_program_info"
        (_results, _error_code, __) = self.project_dao.execute(_query, None)

        # For the active RTK modules, load the data.  For the RTK modules
        # that aren't active in the project, remove the page from the
        # RTK Module view.
        i = 0
        for _module in _results:
            if _module[0] == 1:
                self.module_book.load_module_page(_conf.RTK_MODULES[i],
                                                  self.project_dao)
                _conf.RTK_PAGE_NUMBER.append(i)
            else:
                self.module_book.notebook.remove_page(i)
            i += 1

        #_conf.METHOD = results[0][36]

        self.module_book.statusbar.pop(2)

if __name__ == '__main__':

    main()
