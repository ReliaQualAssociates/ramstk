#!/usr/bin/env python
"""
Contains utility functions for interacting with the RTK application.  Import
this module in other modules that need to interact with the RTK application.
"""

# -*- coding: utf-8 -*-
#
#       rtk.Utilities.py is part of The RTK Project
#
# All rights reserved.

import sys
import os
import os.path
from os import environ, name

# Add localization support.
import gettext

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

# Import other RTK modules.
import Configuration
import gui.gtk.Widgets as Widgets

_ = gettext.gettext

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


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
    conf = Configuration.RTKConf('site')
    #if not file_exists(conf.conf_file):
    #    rtk_warning(_(u"Site configuration file {0:s} not found.  This "
    #                  u"typically indicates RTK was installed improperly or "
    #                  u"RTK files have been corrupted.  You may try to "
    #                  u"uninstall and re-install RTK.").format(conf.conf_file))
    #    return True

    Configuration.COM_BACKEND = conf.read_configuration().get('Backend',
                                                              'type')
    Configuration.SITE_DIR = conf.read_configuration().get('Backend', 'path')
    Configuration.RTK_COM_INFO.append(conf.read_configuration().get('Backend',
                                                                    'host'))
    Configuration.RTK_COM_INFO.append(conf.read_configuration().get('Backend',
                                                                    'socket'))
    Configuration.RTK_COM_INFO.append(
        conf.read_configuration().get('Backend', 'database'))
    Configuration.RTK_COM_INFO.append(conf.read_configuration().get('Backend',
                                                                    'user'))
    Configuration.RTK_COM_INFO.append(
        conf.read_configuration().get('Backend', 'password'))

    # Get a config instance for the user configuration file.
    conf = Configuration.RTKConf('user')

    Configuration.BACKEND = conf.read_configuration().get('Backend', 'type')
    Configuration.RTK_PROG_INFO.append(
        conf.read_configuration().get('Backend', 'host'))
    Configuration.RTK_PROG_INFO.append(
        conf.read_configuration().get('Backend', 'socket'))
    Configuration.RTK_PROG_INFO.append(
        conf.read_configuration().get('Backend', 'database'))
    Configuration.RTK_PROG_INFO.append(
        conf.read_configuration().get('Backend', 'user'))
    Configuration.RTK_PROG_INFO.append(
        conf.read_configuration().get('Backend', 'password'))

    Configuration.FRMULT = float(conf.read_configuration().get('General',
                                                               'frmultiplier'))
    Configuration.PLACES = conf.read_configuration().get('General', 'decimal')
    Configuration.RTK_MODE_SOURCE = conf.read_configuration().get('General',
                                                                  'modesource')
    Configuration.TABPOS[0] = conf.read_configuration().get('General',
                                                            'treetabpos')
    Configuration.TABPOS[1] = conf.read_configuration().get('General',
                                                            'listtabpos')
    Configuration.TABPOS[2] = conf.read_configuration().get('General',
                                                            'booktabpos')

    # Get directory and file information.
    icondir = conf.read_configuration().get('Directories', 'icondir')
    datadir = conf.read_configuration().get('Directories', 'datadir')
    logdir = conf.read_configuration().get('Directories', 'logdir')
    progdir = conf.read_configuration().get('Directories', 'progdir')

    Configuration.CONF_DIR = conf.conf_dir
    if not dir_exists(Configuration.CONF_DIR):
        rtk_warning(_(u"Configuration directory %s does not exist.  "
                      u"Exiting.") % Configuration.CONF_DIR)

    Configuration.ICON_DIR = conf.conf_dir + icondir + '/'
    if not dir_exists(Configuration.ICON_DIR):
        Configuration.ICON_DIR = conf.icon_dir

    Configuration.DATA_DIR = conf.conf_dir + datadir + '/'
    if not dir_exists(Configuration.DATA_DIR):
        Configuration.DATA_DIR = conf.data_dir

    Configuration.LOG_DIR = conf.conf_dir + logdir + '/'
    if not dir_exists(Configuration.LOG_DIR):
        Configuration.LOG_DIR = conf.log_dir

    Configuration.PROG_DIR = progdir
    if not dir_exists(Configuration.PROG_DIR):
        Configuration.PROG_DIR = _homedir + '/Analyses/RTK/'

    # Get list of format files.
    formatfile = conf.read_configuration().get('Files', 'revisionformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'functionformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'requirementformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'hardwareformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'validationformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'rgformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'fracaformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'partformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'siaformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'fmecaformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'stakeholderformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'testformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'mechanismformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'rgincidentformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'incidentformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'softwareformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'datasetformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'riskformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'ffmecaformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'sfmecaformat')
    Configuration.RTK_FORMAT_FILE.append(conf.conf_dir + formatfile)

    # Get color information.
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'revisionbg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'revisionfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'functionbg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'functionfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'requirementbg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'requirementfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'assemblybg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'assemblyfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'validationbg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'validationfg'))
    Configuration.RTK_COLORS.append(conf.read_configuration().get('Colors',
                                                                  'rgbg'))
    Configuration.RTK_COLORS.append(conf.read_configuration().get('Colors',
                                                                  'rgfg'))
    Configuration.RTK_COLORS.append(conf.read_configuration().get('Colors',
                                                                  'fracabg'))
    Configuration.RTK_COLORS.append(conf.read_configuration().get('Colors',
                                                                  'fracafg'))
    Configuration.RTK_COLORS.append(conf.read_configuration().get('Colors',
                                                                  'partbg'))
    Configuration.RTK_COLORS.append(conf.read_configuration().get('Colors',
                                                                  'partfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'overstressbg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'overstressfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'taggedbg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'taggedfg'))
    Configuration.RTK_COLORS.append(
        conf.read_configuration().get('Colors', 'nofrmodelfg'))
    try:
        Configuration.RTK_COLORS.append(
            conf.read_configuration().get('Colors', 'softwarebg'))
    except NoOptionError:
        Configuration.RTK_COLORS.append('#FFFFFF')
    try:
        Configuration.RTK_COLORS.append(
            conf.read_configuration().get('Colors', 'softwarefg'))
    except NoOptionError:
        Configuration.RTK_COLORS.append('#FFFFFF')

    return(icondir, datadir, logdir)


def create_logger(log_name, log_level, log_file, to_tty=False):
    """
    This function creates a logger instance.

    :param str log_name: the name of the log used in the application.
    :param str log_level: the level of messages to log.
    :param str log_file: the full path of the log file for this logger instance
                         to write to.
    :keyword boolean to_tty: boolean indicating whether this logger will also
                             dump messages to the terminal.
    :return: _logger
    :rtype:
    """

    import logging

    _logger = logging.getLogger(log_name)

    _fh = logging.FileHandler(log_file)
    _fh.setLevel(log_level)

    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _fh.setFormatter(_formatter)

    _logger.addHandler(_fh)

    if to_tty:
        _ch = logging.StreamHandler()
        _ch.setLevel(log_level)
        _ch.setFormatter(_formatter)
        _logger.addHandler(_ch)

    return _logger


def date_to_ordinal(date):
    """
    Converts date strings to ordinal dates for use in the database.

    :param str date: the date string to convert.
    :return: ordinal representation of the passed date.
    :rtype: int
    """

    from dateutil.parser import parse

    try:
        return parse(str(date)).toordinal()
    except(ValueError, TypeError):
        return parse('01/01/70').toordinal()


def dir_exists(directory):
    """
    Helper function to check if a directory exists.

    :param str directory: a string representing the directory path to check
                          for.
    :return: False if the directory does not exist, True otherwise.
    :rtype: bool
    """

    return os.path.isdir(directory)


def error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:       # Type error
        _error_code = 10                                            # pragma: no cover
    elif 'invalid literal for int() with base 10' in message[0]:    # Value error
        _error_code = 10
    elif 'could not convert string to float' in message[0]:         # Value error
        _error_code = 10
    elif 'float division by zero' in message[0]:                    # Zero division error
        _error_code = 20
    elif 'index out of range' in message[0]:                        # Index error
        _error_code = 40
    else:                                                           # Unhandled error
        print message
        _error_code = 1000                                          # pragma: no cover

    return _error_code


def file_exists(_file):
    """
    Helper function to check if a file exists.

    :param str _file: a string representing the filepath to check for.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """

    return os.path.isfile(_file)


def missing_to_default(field, default):
    """
    Function to convert missing values into default values.

    :param field: the original, missing, value.
    :param default: the new, default, value.
    :return: field; the new value if field is an empty string, the old value
             otherwise.
    :rtype: any
    """

    if field == '':
        return default
    else:
        return field


def none_to_string(string):
    """
    Converts None types to an empty string.

    :param str string: the string to convert.
    :return: string; the converted string.
    :rtype: str
    """

    if string is None or string == 'None':
        return ''
    else:
        return string


def ordinal_to_date(ordinal):
    """
    Converts ordinal dates to date strings in ISO-8601 format.  Defaults to
    the current date if a bad value is passed as the argument.

    :param int ordinal: the ordinal date to convert.
    :return: the ISO-8601 date representation of the passed ordinal.
    :rtype: date
    """

    from datetime import datetime

    try:
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))
    except ValueError:
        ordinal = datetime.now().toordinal()
        return str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))


def split_string(string):
    """
    Splits a colon-delimited string into its constituent parts.

    :param list string: the colon delimited string that needs to be split into
                        a list.
    :return: _strlist
    :rtype: list of strings
    """

    _strlist = string.rsplit(':')

    return _strlist


def string_to_boolean(string):
    """
    Converts string representations of TRUE/FALSE to an integer value for use
    in the database.

    :param str string: the string to convert.
    :return: _result
    :rtype: int
    """

    _result = 0

    _string = str(string)

    if(_string.lower() == 'true' or _string.lower() == 'yes' or
       _string.lower() == 't' or _string.lower() == 'y'):
        _result = 1

    return _result


def select_source_file(assistant, title):
    """
    Function to select the file containing the data to import to the open RTK
    Program database.

    :param gtk.Assistant assistant: the gtk.Assistant() calling this function.
    :return: _headers, _contents; lists containing the column headings and
             each line from the source file.
    :rtype: lists
    """

    # Get the user's selected file and write the results.
    _dialog = gtk.FileChooserDialog(title, None,
                                    gtk.DIALOG_MODAL |
                                    gtk.DIALOG_DESTROY_WITH_PARENT,
                                    (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                     gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
    _dialog.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
    _dialog.set_current_folder(Configuration.PROG_DIR)

    # Set some filters to select all files or only some text files.
    _filter = gtk.FileFilter()
    _filter.set_name(u"All files")
    _filter.add_pattern("*")
    _dialog.add_filter(_filter)

    _filter = gtk.FileFilter()
    _filter.set_name("Text Files (csv, txt)")
    _filter.add_mime_type("text/csv")
    _filter.add_mime_type("text/txt")
    _filter.add_mime_type("application/xls")
    _filter.add_pattern("*.csv")
    _filter.add_pattern("*.txt")
    _filter.add_pattern("*.xls")
    _dialog.add_filter(_filter)

    # Run the dialog and write the file.
    _headers = []
    _contents = []
    if _dialog.run() == gtk.RESPONSE_ACCEPT:
        _filename = _dialog.get_filename()
        _file = open(_filename, 'r')

        __, _extension = os.path.splitext(_filename)
        if _extension == '.csv':
            _delimiter = ','
        else:
            _delimiter = '\t'

        for _line in _file:
            _contents.append([_line.rstrip('\n')])

        _headers = str(_contents[0][0]).rsplit(_delimiter)
        for i in range(len(_contents) - 1):
            _contents[i] = str(_contents[i + 1][0]).rsplit(_delimiter)

        _dialog.destroy()

    else:
        _dialog.destroy()
        assistant.destroy()

    return _headers, _contents


def cut_copy_paste(__widget, action):
    """
    Cuts, copies, and pastes.

    :param gtk.Widget __widget: the gtk.Widget() that called this function.
    :param int action: whether to cut, copy, or paste
                       0 = cut
                       1 = copy
                       2 = paste
    """

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

    :param gtk.Clipboard clipboard: the gtk.Clipboard() that called this
                                    function.
    :param str contents: the contents of the clipboard.
    :param any user_data: user data.
    """
# TODO: Write copy/cut/paste functions.
    print contents


def select_all(widget):
    """
    Selects all the rows in a treeview.

    :param gtk.Widget widget: the gtk.Widget() that called this function.
    """
# TODO: Write select all function.
    return False


def find(widget, action):
    """
    Finds records in the open project.

    :param gtk.Widget widget: the gtk.Widget() that called this function.
    :param int action: whether to find (0), find next (1), find previous (2),
                       or replace(3).
    """
# TODO: Write find/replace function.
    return False


def undo():
    """
    Undoes the last change.
    """
# TODO: Write undo function.
    return False


def redo():
    """
    Re-does the last change.
    """
# TODO: Write redo function.
    return False


def add_parts_system_hierarchy(__widget, app):
    """
    This function adds parts from the incident reports to the system hierarchy.
    The higher level structure (e.g., sub-systems, assemblies, etc.) must
    already exist.  This function will populate the hierarchy with the parts
    in the program incident data.

    :param gtk.Widget __widget: the gtk.Widget() that called the function.
    :param rtk app: the current instance of the RTK application.
    :return: False if successul or True if an error is encountered.
    :rtype: bool
    """
# TODO: Move this to the Incident class.
    set_cursor(app, gtk.gdk.WATCH)

    # Find the revision id.
    if Configuration.RTK_MODULES[0] == 1:
        _revision_id = app.REVISION.revision_id
    else:
        _revision_id = 0

    # Find the last assembly id being used and increment it by one as the
    # starting assembly id.
    _query = "SELECT MAX(fld_assembly_id) FROM tbl_system"
    _assembly_id = app.DB.execute_query(_query, None, app.ProgCnx)
    _assembly_id = _assembly_id[0][0] + 1

    # Get the list of part numbers to add to the system hierarchy and their
    # associated hardware id's from the incident reports.
    _query = "SELECT DISTINCT(t1.fld_part_num), t2.fld_hardware_id \
              FROM tbl_incident_detail AS t1 \
              INNER JOIN tbl_incident AS t2 \
              ON t1.fld_incident_id=t2.fld_incident_id \
              WHERE t2.fld_revision_id=%d \
              ORDER BY t2.fld_hardware_id" % _revision_id
    _results = app.DB.execute_query(_query, None, app.ProgCnx)

    _n_added = 0
    for __, _part_num in enumerate(_results):
        # Create a description from the part prefix and part index.
        _part_name = str(Configuration.RTK_PREFIX[6]) + ' ' + \
                     str(Configuration.RTK_PREFIX[7])

        _parent = app.HARDWARE.dicPaths[_part_num[1]]

        # Create a tuple of values to pass to the component_add queries.
        _values = (_revision_id, _assembly_id, _part_name, 1,
                   _parent, _part_num[0])

        # Add the new component to each table needing a new entry and increment
        # the count of components added.
        if not component_add(app, _values):
            _n_added += 1

        # Increment the part index and assembly id.
        Configuration.RTK_PREFIX[7] = Configuration.RTK_PREFIX[7] + 1
        _assembly_id += 1

    if _n_added != len(_results):
        rtk_error(_(u"There was an error adding one or more components to the "
                    u"open RTK database."))

    app.REVISION.load_tree()
# TODO: Need to find and select the previously selected revision before loading the hardware tree.
    app.HARDWARE.load_tree()

    set_cursor(app, gtk.gdk.LEFT_PTR)

    return False


def add_failure_modes(app, revision_id, assembly_id, category_id,
                      subcategory_id):
    """
    Function to add default failure modes to the selected component.

    :param rtk app: the running instance of the RTK application.
    :param int revision_id: the component revision ID.
    :param int assembly_id: the component assembly ID.
    :param int category_id: the component category ID.
    :param int subcategory_id: the component subcategory ID.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
# TODO: Move this to the Hardware class.
    _err = False

    # Retrieve the default failure modes for the component from the common
    # database.
    _query = "SELECT fld_mode_id, fld_mode_description, fld_mode_ratio \
              FROM tbl_failure_modes \
              WHERE fld_category_id=%d \
              AND fld_subcategory_id=%d \
              AND fld_source=%d" % (category_id, subcategory_id,
                                    int(Configuration.RTK_MODE_SOURCE))
    _modes = app.COMDB.execute_query(_query, None, app.ComCnx)
    try:
        _n_modes = len(_modes)
    except TypeError:
        _n_modes = 0

    # Add the default failure modes to the open RTK Program database.
    _base_query = "INSERT INTO tbl_fmeca \
                   (fld_revision_id, fld_assembly_id, \
                    fld_mode_description, fld_mode_ratio) \
                   VALUES (%d, %d, '%s', %f)"
    for i in range(_n_modes):
        _query = _base_query % (revision_id, assembly_id, _modes[i][1],
                                _modes[i][2])
        if not app.DB.execute_query(_query, None, app.ProgCnx, commit=True):
            _err = True

    if _err:
        rtk_error(_(u"Problem adding one or more failure modes to the open "
                    u"RTK Program database."))
        return True

    return False
