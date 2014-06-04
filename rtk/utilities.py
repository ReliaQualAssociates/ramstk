#!/usr/bin/env python
"""
utilities contains utility functions for interacting with the RTK
application.  Import this module as _util in other modules that need to
interact with the RTK application.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       utilities.py is part of The RTK Project
#
# All rights reserved.

import sys
import os
import os.path
from os import environ, name

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
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Add localization support.
import gettext
_ = gettext.gettext

# Import other RTK modules.
import configuration as _conf
import login as _login
import widgets as _widg


def read_configuration():
    """
    This method reads the site and user configuration files to establish
    settings for The RTK application.
    """

    if name == 'posix':
        _homedir = environ['HOME']

    elif name == 'nt':
        _homedir = environ['USERPROFILE']

# Get a config instance for the site configuration file.
    conf = _conf.RTKConf('site')

    _conf.COM_BACKEND = conf.read_configuration().get('Backend', 'type')

    _conf.RTK_COM_INFO.append(conf.read_configuration().get('Backend', 'host'))
    _conf.RTK_COM_INFO.append(conf.read_configuration().get('Backend', 'socket'))
    _conf.RTK_COM_INFO.append(conf.read_configuration().get('Backend', 'database'))
    _conf.RTK_COM_INFO.append(conf.read_configuration().get('Backend', 'user'))
    _conf.RTK_COM_INFO.append(conf.read_configuration().get('Backend', 'password'))

# Get a config instance for the user configuration file.
    conf = _conf.RTKConf('user')
    _conf.BACKEND = conf.read_configuration().get('Backend', 'type')
    _conf.FRMULT = float(conf.read_configuration().get('General', 'frmultiplier'))
    _conf.PLACES = conf.read_configuration().get('General', 'decimal')
    _conf.TABPOS[0] = conf.read_configuration().get('General', 'treetabpos')
    _conf.TABPOS[1] = conf.read_configuration().get('General', 'listtabpos')
    _conf.TABPOS[2] = conf.read_configuration().get('General', 'booktabpos')

    _conf.RTK_PROG_INFO.append(conf.read_configuration().get('Backend', 'host'))
    _conf.RTK_PROG_INFO.append(conf.read_configuration().get('Backend', 'socket'))
    _conf.RTK_PROG_INFO.append(conf.read_configuration().get('Backend', 'database'))
    _conf.RTK_PROG_INFO.append(conf.read_configuration().get('Backend', 'user'))
    _conf.RTK_PROG_INFO.append(conf.read_configuration().get('Backend', 'password'))

    # Get directory and file information.
    icondir = conf.read_configuration().get('Directories', 'icondir')
    datadir = conf.read_configuration().get('Directories', 'datadir')
    logdir = conf.read_configuration().get('Directories', 'logdir')
    progdir = conf.read_configuration().get('Directories', 'progdir')

    _conf.CONF_DIR = conf.conf_dir
    if not dir_exists(_conf.CONF_DIR):
        rtk_error(_("Configuration directory %s does not exist.  Exiting.") % _conf.CONF_DIR)

    _conf.ICON_DIR = conf.conf_dir + icondir + '/'
    if not dir_exists(_conf.ICON_DIR):
        _conf.ICON_DIR = conf.icon_dir

    _conf.DATA_DIR = conf.conf_dir + datadir + '/'
    if not dir_exists(_conf.DATA_DIR):
        _conf.DATA_DIR = conf.data_dir

    _conf.LOG_DIR = conf.conf_dir + logdir + '/'
    if not dir_exists(_conf.LOG_DIR):
        _conf.LOG_DIR = conf.log_dir

    _conf.PROG_DIR = _homedir + '/' + progdir + '/'
    if not dir_exists(_conf.PROG_DIR):
        _conf.PROG_DIR = conf.prog_dir

    # Get list of format files.
    formatfile = conf.read_configuration().get('Files', 'revisionformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'functionformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'requirementformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'hardwareformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'validationformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'rgformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'fracaformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'partformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'siaformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'fmecaformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'stakeholderformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'testformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'mechanismformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'rgincidentformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'incidentformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'softwareformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'datasetformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'riskformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'ffmecaformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'sfmecaformat')
    _conf.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)

# Get color information.
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'revisionbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'revisionfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'functionbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'functionfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'requirementbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'requirementfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'assemblybg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'assemblyfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'validationbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'validationfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'rgbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'rgfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'fracabg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'fracafg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'partbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'partfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'overstressbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'overstressfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'taggedbg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'taggedfg'))
    _conf.RTK_COLORS.append(conf.read_configuration().get('Colors', 'nofrmodelfg'))

    return(icondir, datadir, logdir)


def create_logger(log_name, log_level, log_file, to_tty=False):
    """
    This function creates a logger instance.

    Keyword Arguments:
    log_name  -- the name of the log used in the application.
    log_level -- the level of messages to log.
    log_file  -- the full path of the log file for this logger instance
                 to write to.
    to_tty    -- boolean indicating whether this logger will also dump
                 messages to the terminal.
    """

    import logging

    logger = logging.getLogger(log_name)

    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    if to_tty:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def parse_config(configfile):
    """
    This function parses the XML configuration file passed as a parameter.

    @param configfile: the configuration file that needs to be parsed.
    """

    from lxml import etree

    tree = etree.parse(configfile)

    return tree


def split_string(string):
    """
    Splits a colon-delimited string into its constituent parts.

    @param string: the colon delimited string that needs to be split into a
                   list.
    @type string: list of strings
    """

    strlist = string.rsplit(':')

    return strlist


def none_to_string(string):
    """
    Converts None types to an empty string.

    @param string: the string to convert.
    """

    if string is None:
        return ''
    else:
        return string


def string_to_boolean(string):
    """
    Converts string representations of TRUE/FALSE to an integer value for use
    in the database.

    @param string: the string to convert.
    @type string: string
    """

    result = 0

    string = str(string)

    if(string.lower() == 'true' or string.lower() == 'yes' or
       string.lower() == 't' or string.lower() == 'y'):
        result = 1

    return result


def date_to_ordinal(date):
    """
    Converts date strings to ordinal dates for use in the database.

    @param date: the date string to convert.
    @type date: string
    """

    from dateutil.parser import parse

    try:
        return parse(str(date)).toordinal()
    except ValueError:
        return parse('01/01/70').toordinal()


def ordinal_to_date(ordinal):
    """
    Converts ordinal dates to date strings in ISO 8601 format.

    @param ordinal: the ordinal date to convert.
    @type ordinal: date
    """

    from datetime import datetime

    try:
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))
    except ValueError:
        return str(datetime.fromordinal(719163).strftime('%Y-%m-%d')),


def tuple_to_list(_tuple, _list):
    """
    Appends a tuple to a list.

    @param _tuple: the tuple to add to the list.
    @param _list: the existing list to add the tuple elements to.
    """

    for i in range(len(_tuple)):
        _list.append(_tuple[i])

    return _list


def dir_exists(directory):
    """
    Helper function to check if a directory exists.

    @param directory: a string representing the directory path to check for.
    @type directory: string
    """

    return os.path.isdir(directory)


def file_exists(_file):
    """
    Helper function to check if a file exists.

    @param _file: a string representing the filepath to check for.
    @type _file: string
    @return: True if the file exists or False if not.
    @rtype: boolean
    """

    return os.path.isfile(_file)


def create_project(widget, app):
    """
    Creates a new RTK Project.

    @param widget: the gtk.Widget() that called this function.
    @type widget: gtk.Widget
    @param app: the current instance of the RTK application.
    @return: False if successful or True if an error is encountered.
    """

    if _conf.BACKEND == 'mysql':

        login = _login.Login(_(u"Create a RTK Program Database"))
        if login.answer != gtk.RESPONSE_ACCEPT:
            return True

        dialog = _widg.make_dialog(_(u"RTK - New Program"))

        label = _widg.make_label(_(u"New Program Name"))
        txtProgName = _widg.make_entry()
        dialog.vbox.pack_start(label)       # pylint: disable=E1101
        dialog.vbox.pack_start(txtProgName) # pylint: disable=E1101
        label.show()
        txtProgName.show()

        label = _widg.make_label(_(u"Assigned User"))
        txtUser = _widg.make_entry()
        dialog.vbox.pack_start(label)       # pylint: disable=E1101
        dialog.vbox.pack_start(txtUser)     # pylint: disable=E1101
        label.show()
        txtUser.show()

        label = _widg.make_label(_(u"Using Password"))
        txtPasswd = _widg.make_entry()
        txtPasswd.set_invisible_char("*")
        dialog.vbox.pack_start(label)       # pylint: disable=E1101
        dialog.vbox.pack_start(txtPasswd)   # pylint: disable=E1101
        label.show()
        txtPasswd.show()

        if dialog.run() == gtk.RESPONSE_ACCEPT:
            new_program = txtProgName.get_text()
            user = txtUser.get_text()
            passwd = txtPasswd.get_text()

        dialog.destroy()

        _conf.RTK_PROG_INFO[2] = None
        query = "CREATE DATABASE IF NOT EXISTS %s"
        cnx = app.DB.get_connection(_conf.RTK_PROG_INFO)
        results = app.DB.execute_query(query,
                                       new_program,
                                       cnx,
                                       commit=True)
        cnx.close()
        if not results:
            return True

        _conf.RTK_PROG_INFO[2] = new_program
        cnx = app.DB.get_connection(_conf.RTK_PROG_INFO)

        sqlfile = open(_conf.DATA_DIR + 'newprogram_mysql.sql', 'r')

        queries = sqlfile.read().split(';')
        program = "USE '%s'"
        results = app.DB.execute_query(program,
                                       new_program,
                                       cnx,
                                       commit=True)
        for i in range(len(queries)):
            results = app.DB.execute_query(queries[i], cnx, commit=True)

        values = (new_program, user, passwd)
        query = "GRANT DELETE, INSERT, SELECT, UPDATE \
                 ON %s.* TO '%s'@'%%' \
                 IDENTIFIED BY '%s'"
        results = app.DB.execute_query(query,
                                       values,
                                       cnx,
                                       commit=False)

        query = "FLUSH PRIVILEGES"
        results = app.DB.execute_query(query,
                                       None,
                                       cnx,
                                       commit=False)

        cnx.close()

    elif _conf.BACKEND == 'sqlite3':
        _dialog = gtk.FileChooserDialog(title=_(u"Create a RTK Program "
                                                u"Database"),
                                       action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                       buttons=(gtk.STOCK_NEW,
                                                gtk.RESPONSE_ACCEPT,
                                                gtk.STOCK_CANCEL,
                                                gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(_conf.PROG_DIR)

        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _new_program = _dialog.get_filename()
            _new_program = _new_program.rsplit('.')[0]
            _new_program = _new_program + '.rtk'

            if file_exists(_new_program):
                _dlgConfirm = _widg.make_dialog(_(u"RTK - Confirm Overwrite"),
                                                dlgbuttons=(gtk.STOCK_YES,
                                                            gtk.RESPONSE_YES,
                                                            gtk.STOCK_NO,
                                                            gtk.RESPONSE_NO))

                _label = _widg.make_label(_(u"RTK Program database already "
                                            u"exists.\n\n%s\n\n"
                                            u"Overwrite?") %
                                          _new_program, width=-1, height=-1,
                                          bold=False, wrap=True)
                _dlgConfirm.vbox.pack_start(_label)       # pylint: disable=E1101
                _label.show()

                if _dlgConfirm.run() == gtk.RESPONSE_YES:
                    _dlgConfirm.destroy()
                    os.remove(_new_program)
                else:
                    _dlgConfirm.destroy()
                    _dialog.destroy()
                    return True

            _conf.RTK_PROG_INFO[2] = _new_program
            _cnx = app.DB.get_connection(_conf.RTK_PROG_INFO[2])

            _sqlfile = open(_conf.DATA_DIR + 'newprogram_sqlite3.sql', 'r')
            for _query in _sqlfile.read().split(';'):
                app.DB.execute_query(_query, None, _cnx, commit=True)

            _cnx.close()

            open_project(widget, app, dlg=0, filename=_new_program)

        _dialog.destroy()

    return False


def open_project(__widget, app, dlg=1, filename=''):
    """
    Shows the RTK databases available on the selected server and allows the
    user to select the one he/she wishes to use.

    @param __widget: the gtk.Widget() that called this function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    @param dlg: whether or not to display a file chooser dialog.
                0=No
                1=Yes (default)
    @type dlg: integer
    @param filename: the full path to the RTK Program database to open.
    @type filename: string
    """

    if _conf.BACKEND == 'mysql':

        login = _login.Login(_(u"RTK Program Database Login"))

        if login.answer != gtk.RESPONSE_ACCEPT:
            return True

        query = "SHOW DATABASES"
        cnx = app.DB.get_connection(_conf.RTK_PROG_INFO)
        results = app.DB.execute_query(query,
                                       None,
                                       cnx)

        dialog = _widg.make_dialog(_(u"RTK: Open Program"))

        model = gtk.TreeStore(gobject.TYPE_STRING)
        treeview = gtk.TreeView(model)

        column = gtk.TreeViewColumn(_(u"Program"))
        treeview.append_column(column)
        cell = gtk.CellRendererText()
        cell.set_property('editable', False)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 0)

        scrollwindow = gtk.ScrolledWindow()
        width, height = gtk.gdk.get_default_root_window().get_size()
        scrollwindow.set_size_request((width / 6), (height / 6))
        scrollwindow.add(treeview)

        for i in range(len(results)):
            # Don't display the MySQL administrative/test databases.
            if(results[i][0] != 'information_schema' and \
               results[i][0] != 'test' and \
               results[i][0] != 'mysql' and \
               results[i][0] != 'RTKcom' and
               results[i][0] != '#mysql50#lost+found'):
                model.append(None, [results[i][0]])

        dialog.vbox.pack_start(scrollwindow)    # pylint: disable=E1101
        scrollwindow.show_all()

        if dialog.run() == gtk.RESPONSE_ACCEPT:
            (_model, _row) = treeview.get_selection().get_selected()
            _conf.RTK_PROG_INFO[2] = _model.get_value(_row, 0)
            dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH)) # pylint: disable=E1101
            app.load_system()

        dialog.destroy()

        cnx.close()

    elif _conf.BACKEND == 'sqlite3':

        if dlg == 1:
            _dialog = gtk.FileChooserDialog(title=_(u"RTK - Open Program"),
                                            buttons=(gtk.STOCK_OK,
                                                     gtk.RESPONSE_ACCEPT,
                                                     gtk.STOCK_CANCEL,
                                                     gtk.RESPONSE_REJECT))
            _dialog.set_current_folder(_conf.PROG_DIR)

            # Set some filters to select all files or only some text files.
            _filter = gtk.FileFilter()
            _filter.set_name(_(u"RTK Project Files"))
            #_filter.add_mime_type("text/txt")
            _filter.add_pattern("*.rfb")
            _filter.add_pattern("*.rtk")
            _dialog.add_filter(_filter)

            _filter = gtk.FileFilter()
            _filter.set_name(_(u"All files"))
            _filter.add_pattern("*")
            _dialog.add_filter(_filter)

            if _dialog.run() == gtk.RESPONSE_ACCEPT:
                _conf.RTK_PROG_INFO[2] = _dialog.get_filename()
                _dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))    # pylint: disable=E1101
                app.load_system()

            _dialog.destroy()

        else:
            _conf.RTK_PROG_INFO[2] = filename
            app.load_system()

    return False


def save_project(__widget, app):
    """
    Saves the RTK information to the open RTK Program database.

    @param __widget: the gtk.Widget() that called this function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    """
# TODO: Only save the active module in the Tree Book.
    if not app.LOADED:
        return True

    app.winTree.statusbar.push(2, _(u"Saving"))

    app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

    app.REVISION.save_revision()
    app.REQUIREMENT.save_requirement()
    app.FUNCTION.save_function()
    app.HARDWARE.save_hardware()
    app.SOFTWARE.save_software()
    #app.winParts.save_component()

# Update the next ID for each type of object.
    _values = (_conf.RTK_PREFIX[1], _conf.RTK_PREFIX[3],
               _conf.RTK_PREFIX[5], _conf.RTK_PREFIX[7],
               _conf.RTK_PREFIX[9], _conf.RTK_PREFIX[11],
               _conf.RTK_PREFIX[13], _conf.RTK_PREFIX[15],
               _conf.RTK_PREFIX[17], 1)


    query = "UPDATE tbl_program_info \
             SET fld_revision_next_id=%d, fld_function_next_id=%d, \
                 fld_assembly_next_id=%d, fld_part_next_id=%d, \
                 fld_fmeca_next_id=%d, fld_mode_next_id=%d, \
                 fld_effect_next_id=%d, fld_cause_next_id=%d, \
                 fld_software_next_id=%d \
             WHERE fld_program_id=%d" % _values
    app.DB.execute_query(query, None, app.ProgCnx, commit=True)

    #conf = _conf.RTKConf('user')
    #conf.write_configuration()

    app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
    app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
    app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    app.winTree.statusbar.pop(2)

    return False


def delete_project(__widget, app):
    """
    Deletes an existing RTK Project.

    @param __widget: the gtk.Widget() that called this function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    """

    if _conf.BACKEND == 'mysql':
        query = "SHOW DATABASES"
        cnx = app.DB.get_connection(_conf.RTK_PROG_INFO)
        results = app.DB.execute_query(query,
                                       None,
                                       cnx)

        dialog = _widg.make_dialog(_("RTK - Delete Program"))

        model = gtk.TreeStore(gobject.TYPE_STRING)
        treeview = gtk.TreeView(model)

        column = gtk.TreeViewColumn('Program')
        treeview.append_column(column)
        cell = gtk.CellRendererText()
        cell.set_property('editable', False)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 0)

        scrollwindow = gtk.ScrolledWindow()
        width, height = gtk.gdk.get_default_root_window().get_size()
        scrollwindow.set_size_request((width / 6), (height / 6))
        scrollwindow.add(treeview)

        numprograms = len(results)
        for i in range(numprograms):
            # Don't display the MySQL administrative/test databases.
            if(results[i][0] != 'information_schema' and
               results[i][0] != 'test'):
                model.append(None, [results[i][0]])

        dialog.vbox.pack_start(scrollwindow)    # pylint: disable=E1101
        treeview.show()
        scrollwindow.show()

        if dialog.run() == gtk.RESPONSE_ACCEPT:
            (_model, _row) = treeview.get_selection().get_selected()
            project = _model.get_value(_row, 0)
        else:
            dialog.destroy()

        if confirm_action(_("Really delete %s?") % project, 'question'):
            query = "DROP DATABASE IF EXISTS %s"
            results = app.DB.execute_query(query,
                                           project,
                                           cnx)

            dialog.destroy()
        else:
            dialog.destroy()

        cnx.close()

    elif _conf.BACKEND == 'sqlite3':

        dialog = gtk.FileChooserDialog(_(u"RTK - Delete Program"),
                                       None,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        if dialog.run() == gtk.RESPONSE_ACCEPT:
            project = dialog.get_filename()
        else:
            dialog.destroy()

        if(confirm_action(_(u"Really delete %s?") % project), 'question'):
            os.remove(project)
            dialog.destroy()
        else:
            dialog.destroy()


def import_project(__widget, app):
    """
    Imports project information from external files such as Excel, CVS, other
    delimited text files, etc.

    @param __widget: the gtk.Widget() that called this function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    """

# TODO: Write function to import project information from various other formats; Excel, CSV, other delimited files.
    _dialog = gtk.FileChooserDialog(_(u"Select Project to Import"), None,
                                    gtk.FILE_CHOOSER_ACTION_OPEN,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                     gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    if _dialog.run() == gtk.RESPONSE_ACCEPT:
        print "Importing project."

    _dialog.destroy()

    return False


def confirm_action(_prompt_, _image_='default', _parent_=None):
    """
    Dialog to confirm user actions such as deleting a Project.

    Keyword Arguments:
    _prompt_ -- the prompt to display in the dialog.
    _image_  -- the icon to display in the dialog.
    _parent_ -- the parent window, if any, for the dialog.
    """

    dialog = _widg.make_dialog("")

    hbox = gtk.HBox()

    file_image = _conf.ICON_DIR + '32x32/' + _image_ + '.png'
    image = gtk.Image()
    image.set_from_file(file_image)
    hbox.pack_start(image)

    label = _widg.make_label(_prompt_)
    hbox.pack_end(label)
    dialog.vbox.pack_start(hbox)            # pylint: disable=E1101
    hbox.show_all()

    if dialog.run() == gtk.RESPONSE_ACCEPT:
        dialog.destroy()
        return True
    else:
        dialog.destroy()
        return False


def rtk_error(prompt, _parent=None):
    """
    Dialog to display runtime errors to the user.

    @param prompt: the prompt to display in the dialog.
    @type prompt: string
    @param _parent: the parent gtk.Window(), if any, for the dialog.
    @type _parent: gtk.Window
    """

    prompt = prompt + u"  Check the error log %s for additional information " \
                      u"(if any).  Please e-mail bugs@reliaqual.com with a " \
                      u"description of the problem, the workflow you are " \
                      u"using and the error log attached if the problem " \
                      u"persists." % (_conf.LOG_DIR + 'RTK_error.log')

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
                                message_format=prompt)
    _dialog.run()
    _dialog.destroy()


def rtk_information(prompt, _parent=None):
    """
    Dialog to display runtime information to the user.

    @param prompt: the prompt to display in the dialog.
    @type prompt: string
    @param _parent: the parent gtk.Window(), if any, for the dialog.
    @type _parent: gtk.Window
    """

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                                message_format=prompt)
    _dialog.run()
    _dialog.destroy()


def rtk_question(prompt, _parent=None):
    """
    Dialog to display runtime questions to the user.

    @param prompt: the prompt to display in the dialog.
    @type prompt: string
    @param _parent: the parent gtk.Window(), if any, for the dialog.
    @type _parent: gtk.Window
    @return: gtk.RESPONSE_YES or gtk.RESPONSE_NO
    @rtype: GTK response type
    """

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                message_format=prompt)
    _response = _dialog.run()
    _dialog.destroy()

    return _response


def rtk_warning(prompt, _parent=None):
    """
    Dialog to display runtime warnings to the user.

    @param prompt: the prompt to display in the dialog.
    @type prompt: string
    @param _parent: the parent gtk.Window(), if any, for the dialog.
    @type _parent: gtk.Window
    """

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE,
                                message_format=prompt)
    _dialog.run()
    _dialog.destroy()


def add_items(title, prompt=""):
    """
    Adds one or more items to a treeview hierarchy.

    @param title: the string to put in the title bar of the dialog.
    @type title: string
    @param prompt: the prompt to put on the dialog.
    @type prompt: string
    """

    _dialog = _widg.make_dialog(title)

    _fixed = gtk.Fixed()
    _fixed.set_size_request(600, 80)

    _label = _widg.make_label(prompt, -1, -1)
    _x_pos = _label.size_request()[0] + 50
    txtQuantity = _widg.make_entry(width=50)
    txtQuantity.set_text("1")

    _fixed.put(_label, 5, 10)
    _fixed.put(txtQuantity, _x_pos, 10)
    _fixed.show_all()

    _dialog.vbox.pack_start(_fixed)         # pylint: disable=E1101

    _n_items = 0
    if _dialog.run() == gtk.RESPONSE_ACCEPT:
        _n_items = int(txtQuantity.get_text())

    _dialog.destroy()

    return _n_items


def cut_copy_paste(__widget, action):
    """
    Cuts, copies, and pastes.

    @param __widget: the gtk.Widget() that called this function.
    @type __widget: gtk.Widget
    @param action: whether to cut, copy, or paste
                   0 = cut
                   1 = copy
                   2 = paste
    """

    # TODO: Write code to cut/copy/paste.
    clipboard = gtk.Clipboard(gtk.gdk.display_manager_get().get_default_display(),
                              "CLIPBOARD")

    if action == 0:
        print "Cutting."
    elif action == 1:
        print clipboard.set_text("I copied this.")
        print "Copying."
    elif action == 2:
        clipboard.request_text(paste)

    return False


def paste(clipboard, contents, user_data):
    """
    Callback function to paste text from the clipboard.

    Keyword Arguments:
    clipboard -- the gtk.Clipboard that called this function.
    contents  -- the contents of the clipboard.
    user_data -- user data.
    """

    print contents


def select_all(widget):
    """
    Selects all the rows in a treeview.

    Keyword Arguments:
    widget -- the widget that called this function.
    """

    # TODO: Write code to select all items in treeviews.
    return False


def find(widget, action):
    """
    Finds records in the open project.

    Keyword Arguments:
    widget -- the widget that called this function.
    action -- whether to find (0), find next (1), find previous (2),
              or replace(3).
    """

    # TODO: Write code to find, find next, find previous, and replace search terms.
    return False


def find_all_in_list(_list, value, start=0):
    """
    Finds all instances of value in the list starting at position start.

    @param _list: the list to search.
    @type _list: list
    @param value: the value to search for in the list.
    @type value: any of same type found in list
    @param start: the position in the list to start the search.
    @type start: integer
    """

    positions = []
    i = start - 1
    try:
        i = _list.index(value, i+1)
        positions.append(i)
        return positions
    except ValueError:
        pass


def undo():
    """ Undoes the last chamge. """

    # TODO: Write code to undo changes.

    return False


def redo():
    """ Redoes the last change. """

    # TODO: Write code to redo changes.

    return False


def create_comp_ref_des(__widget, app):
    """
    Iterively creates composite reference designators.

    @param __widget: the gtk.Widget() that called this function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    """

    _model = app.HARDWARE.treeview.get_model()
    _model.foreach(build_comp_ref_des)

    return False

def build_comp_ref_des(model, __path, row):
    """
    Creates the composite reference designator for the currently selected row
    in the System gtk.Treemodel.

    @param model: the Hardware class gtk.TreeModel().
    @type model: gtk.TreeModel
    @param __path: the path of the currently selected gtk.TreeIter() in the
                   Hardware class gtk.TreeModel().
    @param __path: tuple
    @param row: the currently selected gtk.TreeIter() in the Hardware class
                gtk.TreeModel().
    @type row: gtk.TreeIter
    """

    _ref_des = model.get_value(row, 68)

    # If the currently selected row has no parent, the composite reference
    # designator is the same as the reference designator.  Otherwise, build the
    # composite reference designator by appending the current row's reference
    # designator to the parent's composite reference designator.
    if not model.iter_parent(row):
        _comp_ref_des = _ref_des
    else:
        _p_row = model.iter_parent(row)
        _p_comp_ref_des = model.get_value(_p_row, 12)
        _comp_ref_des = _p_comp_ref_des + ":" + _ref_des

    model.set_value(row, 12, _comp_ref_des)

    return False


def add_parts_system_hierarchy(__widget, app):
    """
    This function adds parts from the incident reports to the system hierarchy.
    The higher level structure (e.g., sub-systems, assemblies, etc.) must
    already exist.  This function will populate the hierarchy with the parts
    in the program incident data.

    @param __widget: the gtk.Widget() that called the function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    """

    # Find the revision id.
    if _conf.RTK_MODULES[0] == 1:
        _revision_id = app.REVISION.revision_id
    else:
        _revision_id = 0

    # Find the last assembly id being used and increment it by one as the
    # starting assembly id.
    _query = "SELECT MAX(fld_assembly_id) FROM tbl_system"
    _assembly_id = app.DB.execute_query(_query,
                                        None,
                                        app.ProgCnx)
    _assembly_id = _assembly_id[0][0] + 1

    # Get the list of part numbers to add to the system hierarchy and their
    # associated hardware id's from the incident reports.
    _query = "SELECT DISTINCT(t1.fld_part_num), t2.fld_hardware_id \
              FROM tbl_incident_detail AS t1 \
              INNER JOIN tbl_incident AS t2 \
              ON t1.fld_incident_id=t2.fld_incident_id \
              WHERE t2.fld_revision_id=%d \
              ORDER BY t2.fld_hardware_id" % _revision_id
    _results = app.DB.execute_query(_query,
                                    None,
                                    app.ProgCnx)

    _n_added = 0
    for i in range(len(_results)):
        _tmp = app.HARDWARE.dicHARDWARE[_results[i][1]]

        # Create a description from the part prefix and part index.
        _part_name = str(_conf.RTK_PREFIX[6]) + ' ' + \
                     str(_conf.RTK_PREFIX[7])

        # Create a tuple of values to pass to the component_add queries.  The
        # values are:
        #   Revision ID
        #   Assembly ID
        #   Name
        #   Part?
        #   Parent Assembly
        #   Part Number
        _values = (_revision_id, _assembly_id, _part_name, 1,
                   _tmp[len(_tmp) - 1], _results[i][0])

        # Add the new component to each table needing a new entry and increment
        # the count of components added.
        _added = component_add(app, _values)

        if not _added:
            _n_added += 1

        # Increment the part index and assembly id.
        _conf.RTK_PREFIX[7] = _conf.RTK_PREFIX[7] + 1
        _assembly_id += 1

    if _n_added != len(_results):
        rtk_error(_(u"There was an error adding one or more "
                            u"components to the database.  Check the RTK "
                            u"error log for more details."))

    app.REVISION.load_tree()
    #TODO: Need to find and select the previously selected revision before loading the hardware tree.
    app.HARDWARE.load_tree()

    return False


def component_add(app, values):
    """
    Function to add a component to the RTK Program database.

    Keyword Arguments:
    app     -- the running instances of the RTK application.
    values -- tuple containing the values to pass to the queries.
    """

    # Insert the new part into tbl_system.
    _query = "INSERT INTO tbl_system (fld_revision_id, fld_assembly_id, \
                                      fld_name, fld_part, \
                                      fld_parent_assembly, \
                                      fld_part_number) \
              VALUES (%d, %d, '%s', %d, '%s', '%s')" % values
    _inserted = app.DB.execute_query(_query,
                                     None,
                                     app.ProgCnx,
                                     commit=True)

    if not _inserted:
        app.debug_log.error("utilities.py:component_add - Failed to add new "
                            "component to system table.")

    # Insert the new component into tbl_prediction.
    _query = "INSERT INTO tbl_prediction \
              (fld_revision_id, fld_assembly_id) \
              VALUES (%d, %d)" % (values[0], values[1])
    _inserted = app.DB.execute_query(_query,
                                     None,
                                     app.ProgCnx,
                                     commit=True)
    if not _inserted:
        app.debug_log.error("utilities.py:component_add - Failed to add new "
                            "component to prediction table.")

    # Insert the new component into tbl_fmeca.
    _query = "INSERT INTO tbl_fmeca \
              (fld_assembly_id) \
              VALUES (%d)" % values[1]
    _inserted = app.DB.execute_query(_query,
                                     None,
                                     app.ProgCnx,
                                     commit=True)
    if not _inserted:
        app.debug_log.error("utilities.py:component_add - Failed to add new "
                            "component to FMECA table.")

    return False


def set_part_model(category, subcategory):
    """
    This functions sets the Component class part model based on the category
    and subcategory.

    @param category: the component category for part.
    @type category: integer
    @param subcategory: the component sub-category for the part.
    @type subcategory: integer
    @return: _part
    @rtype: Component class instance
    """

    if category == 0 or subcategory == 0:  # No category or subcategory
        _part = None

    elif category == 1:                    # Capacitor
        if subcategory == 1:
            from capacitors.fixed import CeramicGeneral
            _part = CeramicGeneral()
        elif subcategory == 2:
            from capacitors.fixed import CeramicChip
            _part = CeramicChip()
        elif subcategory == 3:
            from capacitors.electrolytic import AluminumDry
            _part = AluminumDry()
        elif subcategory == 4:
            from capacitors.electrolytic import Aluminum
            _part = Aluminum()
        elif subcategory == 5:
            from capacitors.electrolytic import TantalumNonSolid
            _part = TantalumNonSolid()
        elif subcategory == 6:
            from capacitors.electrolytic import TantalumSolid
            _part = TantalumSolid()
        elif subcategory == 7:
            from capacitors.fixed import PaperFeedthrough
            _part = PaperFeedthrough()
        elif subcategory == 8:
            from capacitors.fixed import Glass
            _part = Glass()
        elif subcategory == 9:
            from capacitors.fixed import MetallizedPaper
            _part = MetallizedPaper()
        elif subcategory == 10:
            from capacitors.fixed import Mica
            _part = Mica()
        elif subcategory == 11:
            from capacitors.fixed import MicaButton
            _part = MicaButton()
        elif subcategory == 12:
            from capacitors.fixed import PlasticFilm
            _part = PlasticFilm()
        elif subcategory == 13:
            from capacitors.fixed import PaperBypass
            _part = PaperBypass()
        elif subcategory == 14:
            from capacitors.fixed import Plastic
            _part = Plastic()
        elif subcategory == 15:
            from capacitors.fixed import SuperMetallizedPlastic
            _part = SuperMetallizedPlastic()
        elif subcategory == 16:
            from capacitors.variable import Gas
            _part = Gas()
        elif subcategory == 17:
            from capacitors.variable import AirTrimmer
            _part = AirTrimmer()
        elif subcategory == 18:
            from capacitors.variable import Ceramic
            _part = Ceramic()
        elif subcategory == 19:
            from capacitors.variable import Piston
            _part = Piston()
    elif category == 2:                    # Connection
        if subcategory == 4:
            from connections.socket import ICSocket
            _part = ICSocket()
        elif subcategory == 5:
            from connections.multipin import Multipin
            _part = Multipin()
        elif subcategory == 6:
            from connections.pcb import PCBEdge
            _part = PCBEdge()
        elif subcategory == 7:
            from connections.solder import PTH
            _part = PTH()
        else:
            from connections.solder import Solder
            _part = Solder(subcategory)
    elif category == 3:                    # Inductive Device
        if subcategory == 1:
            from inductors.coil import Coil
            _part = Coil()
        elif subcategory == 2:
            from inductors.transformer import Audio
            _part = Audio()
        elif subcategory == 3:
            from inductors.transformer import Power
            _part = Power()
        elif subcategory == 4:
            from inductors.transformer import LowPowerPulse
            _part = LowPowerPulse()
        elif subcategory == 5:
            from inductors.transformer import RF
            _part = RF()

    elif category == 4:                    # Integrated circuit
        if subcategory == 1:
            from integrated_circuits.gaas import GaAsDigital
            _part = GaAsDigital()
        elif subcategory == 2:
            from integrated_circuits.gaas import GaAsMMIC
            _part = GaAsMMIC()
        elif subcategory == 3:
            from integrated_circuits.linear import Linear
            _part = Linear()
        elif subcategory == 4:
            from integrated_circuits.logic import Logic
            _part = Logic()
        elif subcategory == 5:
            from integrated_circuits.memory import MemoryDRAM
            _part = MemoryDRAM()
        elif subcategory == 6:
            from integrated_circuits.memory import MemoryEEPROM
            _part = MemoryEEPROM()
        elif subcategory == 7:
            from integrated_circuits.memory import MemoryROM
            _part = MemoryROM()
        elif subcategory == 8:
            from integrated_circuits.memory import MemorySRAM
            _part = MemorySRAM()
        elif subcategory == 9:
            from integrated_circuits.microprocessor import Microprocessor
            _part = Microprocessor()
        elif subcategory == 10:
            from integrated_circuits.palpla import PALPLA
            _part = PALPLA()
        elif subcategory == 11:
            from integrated_circuits.vlsi import VLSI
            _part = VLSI()

    elif category == 5:              # Meter
        if subcategory == 1:
            from meters.meter import ElapsedTime
            _part = ElapsedTime()
        elif subcategory == 2:
            from meters.meter import Panel
            _part = Panel()

    elif category == 6:              # Miscellaneous
        if subcategory == 1:
            from miscellaneous.crystal import Crystal
            _part = Crystal()
        elif subcategory == 2:
            from miscellaneous.fuse import Fuse
            _part = Fuse()
        elif subcategory == 3:
            from miscellaneous.lamp import Lamp
            _part = Lamp()

    elif category == 7:              # Relay
        if subcategory == 1:
            from relays.relay import Mechanical
            _part = Mechanical()
        elif subcategory == 2:
            from relays.relay import SolidState
            _part = SolidState()

    elif category == 8:              # Resistor
        if subcategory == 1:
            from resistors.fixed import Composition
            _part = Composition()
        elif subcategory == 2:
            from resistors.fixed import Film
            _part = Film()
        elif subcategory == 3:
            from resistors.fixed import FilmNetwork
            _part = FilmNetwork()
        elif subcategory == 4:
            from resistors.fixed import FilmPower
            _part = FilmPower()
        elif subcategory == 5:
            from resistors.fixed import Wirewound
            _part = Wirewound()
        elif subcategory == 6:
            from resistors.fixed import WirewoundPower
            _part = WirewoundPower()
        elif subcategory == 7:
            from resistors.fixed import WirewoundPowerChassis
            _part = WirewoundPowerChassis()
        elif subcategory == 8:
            from resistors.thermistor import Thermistor
            _part = Thermistor()
        elif subcategory == 9:
            from resistors.variable import Composition
            _part = Composition()
        elif subcategory == 10:
            from resistors.variable import NonWirewound
            _part = NonWirewound()
        elif subcategory == 11:
            from resistors.variable import VarFilm
            _part = VarFilm()
        elif subcategory == 12:
            from resistors.variable import VarWirewound
            _part = VarWirewound()
        elif subcategory == 13:
            from resistors.variable import VarWirewoundPower
            _part = VarWirewoundPower()
        elif subcategory == 14:
            from resistors.variable import WirewoundPrecision
            _part = WirewoundPrecision()
        elif subcategory == 15:
            from resistors.variable import WirewoundSemiPrecision
            _part = WirewoundSemiPrecision()

    elif category == 9:              # Semiconductor
        if subcategory == 1:
            from semiconductors.diode import HighFrequency
            _part = HighFrequency()
        elif subcategory == 2:
            from semiconductors.diode import LowFrequency
            _part = LowFrequency()
        elif subcategory == 3:
            from semiconductors.optoelectronics import Display
            _part = Display()
        elif subcategory == 4:
            from semiconductors.optoelectronics import Detector
            _part = Detector()
        elif subcategory == 5:
            from semiconductors.optoelectronics import LaserDiode
            _part = LaserDiode()
        elif subcategory == 6:
            from semiconductors.thyristor import Thyristor
            _part = Thyristor()
        elif subcategory == 7:
            from semiconductors.transistor import HFGaAsFET
            _part = HFGaAsFET()
        elif subcategory == 8:
            from semiconductors.transistor import HFHPBipolar
            _part = HFHPBipolar()
        elif subcategory == 9:
            from semiconductors.transistor import HFLNBipolar
            _part = HFLNBipolar()
        elif subcategory == 10:
            from semiconductors.transistor import HFSiFET
            _part = HFSiFET()
        elif subcategory == 11:
            from semiconductors.transistor import LFBipolar
            _part = LFBipolar()
        elif subcategory == 12:
            from semiconductors.transistor import LFSiFET
            _part = LFSiFET()
        elif subcategory == 13:
            from semiconductors.transistor import Unijunction
            _part = Unijunction()

    elif category == 10:             # Switching Device
        if subcategory == 1:
            from switches.breaker import Breaker
            _part = Breaker()
        elif subcategory == 2:
            from switches.rotary import Rotary
            _part = Rotary()
        elif subcategory == 3:
            from switches.sensitive import Sensitive
            _part = Sensitive()
        elif subcategory == 4:
            from switches.thumbwheel import Thumbwheel
            _part = Thumbwheel()
        elif subcategory == 5:
            from switches.toggle import Toggle
            _part = Toggle()

    return _part


def calculate_max_text_width(text, font):
    """
    Function to calculate the maximum width of the text string that is using a
    particular font.

    @param text: the text string to calculate.
    @type text: string
    @param font: the font being used.
    @type font: string
    @return: _max
    @rtype: integer
    """

    _max = 0
    _lines = text.split('\n')
    for _line in _lines:
        _max = max(_max, font.width(_line))

    return _max + 50


def trickledown(model, row, index_, value_):
    """
    Iteratively trickles down a particular parameter value from a parent to
    it's children.

    Keyword Arguments:
    model  -- the gtkTreemodel containing the information to trickle down.
    row    -- the selected row in the model containing the information to
              trickle down.
    index_ -- the column in the model containing the information to
              trickle down.
    value_ -- the value of the parameter to trickle down.
    """

    _n_children = model.iter_n_children(row)

    for i in range(_n_children):
        chrow = model.iter_nth_child(row, i)
        model.set_value(chrow, index_, value_)
        if model.iter_has_child(chrow):
            trickledown(model, chrow, index_, value_)

    return False


def options(__widget, app):
    """
    Function to launch the user options configuration assistant.

    @param __widget: the gtk.Widget() calling this function.
    @type __widget: gtk.Widget
    @param app: the current instance of the RTK application.
    """

    Options(app)


def date_select(__widget, entry=None):
    """
    Function to select a date from a calendar widget.

    @param __widget: the gtk.Widget() calling this function.
    @type __widget: gtk.Widget
    @param entry: the gtk.Entry() widget in which to display the date.
    @type entry: gtk.Entry
    @return: _date
    @rtype: date string (YYYY-MM-DD)
    """

    from datetime import datetime

    _dialog = _widg.make_dialog(_(u"Select Date"),
                                dlgbuttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    _calendar = gtk.Calendar()
    _dialog.vbox.pack_start(_calendar)      # pylint: disable=E1101
    _dialog.vbox.show_all()                 # pylint: disable=E1101

    if _dialog.run() == gtk.RESPONSE_ACCEPT:
        _date = _calendar.get_date()
        _date = datetime(_date[0], _date[1] + 1,
                         _date[2]).date().strftime("%Y-%m-%d")
    else:
        _date = "1970-01-01"

    _dialog.destroy()

    if entry is not None:
        entry.set_text(_date)
        entry.grab_focus()

    return _date


def set_cursor(app, cursor):
    """
    Function to set the cursor for a gtk.gdk.Window()

    @param app: the running instance of the RTK application.
    @param cursor: the gtk.gdk.Cursor() to set.  Only handles one of the
                   following:
                   gtk.gdk.X_CURSOR
                   gtk.gdk.ARROW
                   gtk.gdk.CENTER_PTR
                   gtk.gdk.CIRCLE
                   gtk.gdk.CROSS
                   gtk.gdk.CROSS_REVERSE
                   gtk.gdk.CROSSHAIR
                   gtk.gdk.DIAMOND_CROSS
                   gtk.gdk.DOUBLE_ARROW
                   gtk.gdk.DRAFT_LARGE
                   gtk.gdk.DRAFT_SMALL
                   gtk.gdk.EXCHANGE
                   gtk.gdk.FLEUR
                   gtk.gdk.GUMBY
                   gtk.gdk.HAND1
                   gtk.gdk.HAND2
                   gtk.gdk.LEFT_PTR - used for non-busy cursor
                   gtk.gdk.PENCIL
                   gtk.gdk.PLUS
                   gtk.gdk.QUESTION_ARROW
                   gtk.gdk.RIGHT_PTR
                   gtk.gdk.SB_DOWN_ARROW
                   gtk.gdk.SB_H_DOUBLE_ARROW
                   gtk.gdk.SB_LEFT_ARROW
                   gtk.gdk.SB_RIGHT_ARROW
                   gtk.gdk.SB_UP_ARROW
                   gtk.gdk.SB_V_DOUBLE_ARROW
                   gtk.gdk.TCROSS
                   gtk.gdk.TOP_LEFT_ARROW
                   gtk.gdk.WATCH - used when application is busy
                   gtk.gdk.XTERM - selection bar
    """

    app.winTree.window.set_cursor(gtk.gdk.Cursor(cursor))
    app.winParts.window.set_cursor(gtk.gdk.Cursor(cursor))
    app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(cursor))

    gtk.gdk.flush()

    return False

def long_call(app):
    """
    Function for restoring the cursor to normal after a long call.

    @param app: the running instance of the RTK application.
    """

    app.winTree.window.set_cursor(None)
    app.winParts.window.set_cursor(None)
    app.winWorkBook.window.set_cursor(None)


class Options(object):
    """
    An assistant to provide a GUI to the various configuration files for RTK.
    """

    def __init__(self, _app):
        """
        Allows a user to set site-wide options.

        Keyword Arguments:
        app    -- the RTK application object.
        """

        import pango

        self._app = _app

        self.winOptions = gtk.Window()
        self.winOptions.set_title(_(u"RTK - Options"))

        notebook = gtk.Notebook()

        # ----- ----- ----- -- RTK module options - ----- ----- ----- #
        if _conf.RTK_PROG_INFO[2] != '':
            fixed = gtk.Fixed()

            self.chkRevisions = _widg.make_check_button(_(u"Revisions"))
            self.chkFunctions = _widg.make_check_button(_(u"Functions"))
            self.chkRequirements = _widg.make_check_button(_(u"Requirements"))
            self.chkSoftware = _widg.make_check_button(_(u"Software Reliability"))
            self.chkValidation = _widg.make_check_button(_(u"Validation Tasks"))
            self.chkRG = _widg.make_check_button(_(u"Reliability Tests"))
            self.chkIncidents = _widg.make_check_button(_(u"Field Incidents"))

            self.btnSaveOptions = gtk.Button(stock=gtk.STOCK_SAVE)
            self.btnSaveOptions.connect('clicked', self.save_options)

            fixed.put(self.chkRevisions, 5, 5)
            fixed.put(self.chkFunctions, 5, 35)
            fixed.put(self.chkRequirements, 5, 65)
            fixed.put(self.chkSoftware, 5, 95)
            fixed.put(self.chkValidation, 5, 125)
            fixed.put(self.chkRG, 5, 155)
            fixed.put(self.chkIncidents, 5, 185)

            fixed.put(self.btnSaveOptions, 5, 215)

            query = "SELECT fld_revision_active, fld_function_active, \
                            fld_requirement_active, fld_hardware_active, \
                            fld_software_active, fld_vandv_active, \
                            fld_testing_active, fld_rcm_active, \
                            fld_fraca_active, fld_fmeca_active, \
                            fld_survival_active, fld_rbd_active, \
                            fld_fta_active \
                     FROM tbl_program_info"
            results = _app.DB.execute_query(query,
                                            None,
                                            _app.ProgCnx,
                                            commit=False)

            self.chkRevisions.set_active(results[0][0])
            self.chkFunctions.set_active(results[0][1])
            self.chkRequirements.set_active(results[0][2])
            self.chkSoftware.set_active(results[0][4])
            self.chkValidation.set_active(results[0][5])
            self.chkRG.set_active(results[0][6])
            self.chkIncidents.set_active(results[0][8])

            label = gtk.Label(_("RTK Modules"))
            label.set_tooltip_text(_("Select active RTK modules."))
            notebook.insert_page(fixed, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- - Create list edit options - ----- ----- ----- #
        fixed = gtk.Fixed()

        self.rdoMeasurement = gtk.RadioButton(group=None, label=_(u"Edit measurement units"))
        self.rdoRequirementTypes = gtk.RadioButton(group=self.rdoMeasurement, label=_(u"Edit requirement types"))
        self.rdoRiskCategory = gtk.RadioButton(group=self.rdoMeasurement, label=_(u"Edit risk categories"))
        self.rdoVandVTasks = gtk.RadioButton(group=self.rdoMeasurement, label=_(u"Edit V&V activity types"))
        self.rdoUsers = gtk.RadioButton(group=self.rdoMeasurement, label=_(u"Edit user list"))

        self.btnListEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        self.btnListEdit.connect('clicked', self.edit_lists)

        fixed.put(self.rdoMeasurement, 5, 5)
        fixed.put(self.rdoRequirementTypes, 5, 35)
        fixed.put(self.rdoRiskCategory, 5, 65)
        fixed.put(self.rdoVandVTasks, 5, 95)
        fixed.put(self.rdoUsers, 5, 125)
        fixed.put(self.btnListEdit, 5, 205)

        label = gtk.Label(_(u"Edit Lists"))
        label.set_tooltip_text(_(u"Allows editting of lists used in RTK."))
        notebook.insert_page(fixed, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- - Create tree edit options - ----- ----- ----- #
        fixed = gtk.Fixed()

        self.rdoRevision = gtk.RadioButton(group=None, label=_(u"Edit Revision tree layout"))
        self.rdoFunction = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Function tree layout"))
        self.rdoRequirement = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Requirement tree layout"))
        self.rdoHardware = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Hardware tree layout"))
        self.rdoSoftware = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Software tree layout"))
        self.rdoValidation = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit V&V tree layout"))
        self.rdoIncident = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Program Incident tree layout"))
        self.rdoTesting = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Testing tree layout"))
        self.rdoSurvival = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Survival Analysis tree layout"))

        self.rdoPart = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Part list layout"))

        self.rdoAllocation = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Reliability Allocation worksheet layout"))
        self.rdoRiskAnalysis = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Risk Analysis worksheet layout"))
        self.rdoSimilarItem = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit Similar Item Analysis worksheet layout"))
        self.rdoFMECA = gtk.RadioButton(group=self.rdoRevision, label=_(u"Edit FMEA/FMECA worksheet layout"))

        self.btnTreeEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        self.btnTreeEdit.connect('released', self._edit_tree)

        fixed.put(self.rdoRevision, 5, 5)
        fixed.put(self.rdoFunction, 5, 35)
        fixed.put(self.rdoRequirement, 5, 65)
        fixed.put(self.rdoHardware, 5, 95)
        fixed.put(self.rdoSoftware, 5, 125)
        fixed.put(self.rdoValidation, 5, 155)
        fixed.put(self.rdoTesting, 5, 185)
        fixed.put(self.rdoIncident, 5, 215)
        fixed.put(self.rdoSurvival, 5, 245)
        #fixed.put(self.rdoAllocation, 5, 275)
        fixed.put(self.rdoPart, 5, 275)
        fixed.put(self.rdoRiskAnalysis, 5, 305)
        fixed.put(self.rdoSimilarItem, 5, 335)
        fixed.put(self.rdoFMECA, 5, 365)
        fixed.put(self.btnTreeEdit, 5, 405)

        label = gtk.Label(_(u"Edit Tree Layouts"))
        label.set_tooltip_text(_(u"Allows editting of tree layouts used in RTK."))
        notebook.insert_page(fixed, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- Create tree edit gtk.TreeView ----- ----- ----- #
        _labels = [_(u"Default\nTitle"), _(u"User\nTitle"),
                   _(u"Column\nPosition"), _(u"Can\nEdit?"),
                   _(u"Is\nVisible?")]

        vbox = gtk.VBox()

        self.tvwEditTree = gtk.TreeView()
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        self.tvwEditTree.set_model(model)

        for i in range(5):

            if i == 0:
                cell = gtk.CellRendererText()
                cell.set_property('background', 'light gray')
                cell.set_property('editable', 0)
                cell.set_property('foreground', '#000000')
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
            elif i > 0 and i < 3:
                cell = gtk.CellRendererText()
                cell.set_property('background', '#FFFFFF')
                cell.set_property('editable', 1)
                cell.set_property('foreground', '#000000')
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
                cell.connect('edited', self._cell_edit, i, model)
            elif i > 4:
                cell = gtk.CellRendererText()
                cell.set_property('editable', 0)
            else:
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 1)
                cell.connect('toggled', self._cell_toggled, i, model)

            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_markup("<span weight='bold'>" + _labels[i] + "</span>")
            label.show_all()

            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_alignment(0.5)
            column.pack_start(cell, True)
            if i < 3:
                column.set_attributes(cell, text=i)
            elif i > 4:
                column.set_visible(0)
            else:
                column.set_attributes(cell, active=i)

            self.tvwEditTree.append_column(column)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.add(self.tvwEditTree)

        vbox.pack_start(scrollwindow)

        fixed = gtk.Fixed()

        self.btnSaveTree = gtk.Button(_(u"Save Layout"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveTree.set_image(image)
        self.btnSaveTree.connect('clicked', self._save_tree_layout)

        fixed.put(self.btnSaveTree, 5, 5)

        vbox.pack_end(fixed, expand=False)

        label = gtk.Label(_(u"Editor"))
        label.set_tooltip_text(_(u"Displays the editor."))
        notebook.insert_page(vbox, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        self.winOptions.add(notebook)
        self.winOptions.show_all()

    def _edit_tree(self, __button):
        """
        Method to edit gtk.TreeView() layouts.

        @param __button: the gtk.Button() that called this method.
        @type __button: gtk.Button()
        """

        from lxml import etree

        (_name, _fmt_idx) = self._get_format_info()

        # Retrieve the default heading text from the format file.
        path = "/root/tree[@name='%s']/column/defaulttitle" % _name
        default = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        # Retrieve the default heading text from the format file.
        path = "/root/tree[@name='%s']/column/usertitle" % _name
        user = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='%s']/column/position" % _name
        position = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        # Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='%s']/column/editable" % _name
        editable = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        # Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='%s']/column/visible" % _name
        visible = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        # Retrieve datatypes from the format file.
        path = "/root/tree[@name='%s']/column/datatype" % _name
        datatype = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        # Retrieve widget types from the format file.
        path = "/root/tree[@name='%s']/column/widget" % _name
        widget = etree.parse(_conf.RTK_FORMAT_FILE[_fmt_idx]).xpath(path)

        model = self.tvwEditTree.get_model()
        model.clear()

        for i in range(len(default)):
            _data = [default[i].text, user[i].text, int(position[i].text),
                     int(editable[i].text), int(visible[i].text),
                     datatype[i].text, widget[i].text]
            model.append(_data)

        notebook = self.winOptions.get_children()
        notebook[0].set_current_page(2)
        _child = notebook[0].get_nth_page(notebook[0].get_current_page())
        notebook[0].set_tab_label_text(_child, _(u"Edit %s Tree" % _name))

        return False

    def _cell_edit(self, __cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView() gtk.CellRenderer() is edited.

        @param __cell: the gtk.CellRenderer() that was edited.
        @type __cell: gtk.CellRenderer
        @param path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                     edited.
        @type path: string
        @param new_text: the new text in the edited gtk.CellRenderer().
        @type new_text: string
        @param position: the column position of the edited gtk.CellRenderer().
        @type position: integer
        @param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        @type model: gtk.TreeModel
        """

        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        return False

    def _cell_toggled(self, cell, path, position, model):
        """
        Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        model[path][position] = not cell.get_active()

        return False

    def _save_tree_layout(self, __button):
        """
        Method for saving the gtk.TreeView layout file.

        @param __button: the gtk.Button() that called this method.
        @type __button: gtk.Button
        """

        from shutil import copyfile

        (_name, _fmt_idx) = self._get_format_info()

# Get the format file for the gtk.TreeView to be edited.
        _format_file = _conf.RTK_FORMAT_FILE[_fmt_idx]
        _basename = os.path.basename(_format_file)

# Make a copy of the original format file.
        copyfile(_format_file, _format_file + '.bak')

        # Open the format file for writing.
        _file = open(_format_file, 'w')

# Create the new format file.
        _file.write("<!--\n")
        _file.write("-*- coding: utf-8 -*-\n\n")
        _file.write("%s is part of the RTK Project\n\n" % _basename)
        _file.write('Copyright 2011-2014 Andrew "Weibullguy" Rowland '
                    '<andrew DOT rowland AT reliaqual DOT com>\n\n')
        _file.write("All rights reserved.-->\n\n")
        _file.write("<!-- This file contains information used by the RTK "
                    "application to draw\n")
        _file.write("various widgets.  These values can be changed by the "
                    "user to personalize\n")
        _file.write("their experience. -->\n\n")

        _file.write("<root>\n")
        _file.write('\t<tree name="%s">\n' % _name)

        model = self.tvwEditTree.get_model()
        row = model.get_iter_first()
        while row is not None:
            _file.write("\t\t<column>\n")
            _file.write("\t\t\t<defaulttitle>%s</defaulttitle>\n" % model.get_value(row, 0))
            _file.write("\t\t\t<usertitle>%s</usertitle>\n"% model.get_value(row, 1))
            _file.write("\t\t\t<datatype>%s</datatype>\n" % model.get_value(row, 5))
            _file.write('\t\t\t<position>%d</position>\n' % model.get_value(row, 2))
            _file.write("\t\t\t<widget>%s</widget>\n" % model.get_value(row, 6))
            _file.write("\t\t\t<editable>%d</editable>\n" % model.get_value(row, 3))
            _file.write("\t\t\t<visible>%d</visible>\n" % model.get_value(row, 4))
            _file.write("\t\t</column>\n")

            row = model.iter_next(row)

        _file.write("\t</tree>\n")
        _file.write("</root>")
        _file.close()

        self.winOptions.destroy()

        return False

    def _get_format_info(self):
        """
        Method to retrieve the name and index of the selected format file.
        """

        if self.rdoRevision.get_active():
            _name = 'Revision'
            _fmt_idx = 0
        elif self.rdoFunction.get_active():
            _name = 'Function'
            _fmt_idx = 1
        elif self.rdoRequirement.get_active():
            _name = 'Requirement'
            _fmt_idx = 2
        elif self.rdoHardware.get_active():
            _name = 'Hardware'
            _fmt_idx = 3
        elif self.rdoSoftware.get_active():
            _name = 'Software'
            _fmt_idx = 15
        elif self.rdoValidation.get_active():
            _name = 'Validation'
            _fmt_idx = 4
        elif self.rdoTesting.get_active():
            _name = 'Testing'
            _fmt_idx = 11
        elif self.rdoIncident.get_active():
            _name = 'Incidents'
            _fmt_idx = 14
        elif self.rdoSurvival.get_active():
            _name = 'Dataset'
            _fmt_idx = 16
        elif self.rdoPart.get_active():
            _name = 'Parts'
            _fmt_idx = 7
        elif self.rdoRiskAnalysis.get_active():
            _name = 'Risk'
            _fmt_idx = 17
        elif self.rdoSimilarItem.get_active():
            _name = 'SIA'
            _fmt_idx = 8
        elif self.rdoFMECA.get_active():
            _name = 'FMECA'
            _fmt_idx = 9

        return _name, _fmt_idx

    def save_options(self, __button):
        """
        Method to save the configuration changes made by the user.

        @param __button: the gtk.Button() that called this method.
        @type __button: gtk.Button
        @return: False if successful or True if an error is encountered.
        """

        self.winOptions.destroy()

        _values = (self.chkRevisions.get_active(),
                   self.chkFunctions.get_active(),
                   self.chkRequirements.get_active(),
                   self.chkSoftware.get_active(),
                   self.chkValidation.get_active(),
                   self.chkRG.get_active(),
                   0,
                   self.chkIncidents.get_active(),
                   0, 0, 0, 0)

        _query = "UPDATE tbl_program_info \
                  SET fld_revision_active=%d, fld_function_active=%d, \
                      fld_requirement_active=%d, fld_software_active=%d, \
                      fld_vandv_active=%d, fld_testing_active=%d, \
                      fld_rcm_active=%d, fld_fraca_active=%d, \
                      fld_fmeca_active=%d, fld_survival_active=%d, \
                      fld_rbd_active=%d, fld_fta_active=%d" % _values
        return self._app.DB.execute_query(_query, None,
                                          self._app.ProgCnx, commit=True)

    def edit_lists(self, __button):
        """

        @param __button: the gtk.Button() that called this method.
        @type __button: gtk.Button
        @return:
        """

        #if self.rdoMeasurement.get_active():
        #    assistant = gtk.Assistant()
        return False
