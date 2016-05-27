#!/usr/bin/env python
"""
Contains utility functions for interacting with the RTK application.  Import
this module as _util in other modules that need to interact with the RTK
application.
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

from ConfigParser import SafeConfigParser, NoOptionError

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
import login as _login
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
    if not file_exists(conf.conf_file):
        rtk_warning(_(u"Site configuration file {0:s} not found.  This "
                      u"typically indicates RTK was installed improperly or "
                      u"RTK files have been corrupted.  You may try to "
                      u"uninstall and re-install RTK.").format(conf.conf_file))
        return True

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


def delete_project(__widget, app):
    """
    Deletes an existing RTK Project.

    :param gtk.Widget __widget: the gtk.Widget() that called this function.
    :param rtk app: the current instance of the RTK application.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    if Configuration.BACKEND == 'mysql':
        query = "SHOW DATABASES"
        cnx = app.DB.get_connection(Configuration.RTK_PROG_INFO)
        results = app.DB.execute_query(query,
                                       None,
                                       cnx)

        dialog = Widgets.make_dialog(_("RTK - Delete Program"))

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

    elif Configuration.BACKEND == 'sqlite3':

        dialog = gtk.FileChooserDialog(_(u"RTK - Delete Program"),
                                       None,
                                       gtk.DIALOG_MODAL |
                                       gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        if dialog.run() == gtk.RESPONSE_ACCEPT:
            project = dialog.get_filename()
        else:
            dialog.destroy()

        if(confirm_action(_(u"Really delete {0:s}?").format(project)),
           'question'):
            os.remove(project)
            dialog.destroy()
        else:
            dialog.destroy()

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


def confirm_action(_prompt_, _image_='default', _parent_=None):
    """
    Dialog to confirm user actions such as deleting a Project.

    :param str _prompt_: the prompt to display in the dialog.
    :param str _image_: the icon to display in the dialog.
    :param gtk.Window _parent_: the parent gtk.Window(), if any, for the
                                dialog.
    """

    dialog = Widgets.make_dialog("")

    hbox = gtk.HBox()

    file_image = Configuration.ICON_DIR + '32x32/' + _image_ + '.png'
    image = gtk.Image()
    image.set_from_file(file_image)
    hbox.pack_start(image)

    label = Widgets.make_label(_prompt_)
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

    :param str prompt: the prompt to display in the dialog.
    :param gtk.Window _parent: the parent gtk.Window(), if any, for the dialog.
    """

    _icon = Configuration.ICON_DIR + '32x32/error.png'
    _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
    _image = gtk.Image()
    _image.set_from_pixbuf(_icon)

    prompt = prompt + u"  Check the error log {0:s} for additional " \
                      u"information (if any).  Please e-mail " \
                      u"bugs@reliaqual.com with a description of the " \
                      u"problem, the workflow you are using and the error " \
                      u"log attached if the problem persists.".format(
                          Configuration.LOG_DIR + 'RTK_error.log')

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
                                message_format=prompt)

    _dialog.set_image(_image)

    _dialog.run()
    _dialog.destroy()


def rtk_information(prompt, _parent=None):
    """
    Dialog to display runtime information to the user.

    :param str prompt: the prompt to display in the dialog.
    :param gtk.Window _parent: the parent gtk.Window(), if any, for the dialog.
    """

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                message_format=prompt)
    _dialog.set_markup(prompt)

    _dialog.run()
    _dialog.destroy()


def rtk_question(prompt, _parent=None):
    """
    Dialog to display runtime questions to the user.

    :param str prompt: the prompt to display in the dialog.
    :param gtk.Window _parent: the parent gtk.Window(), if any, for the dialog.
    :return: gtk.RESPONSE_YES or gtk.RESPONSE_NO
    :rtype: GTK response type
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

    :param str prompt: the prompt to display in the dialog.
    :param gtk.Window _parent: the parent gtk.Window(), if any, for the dialog.
    """

    _dialog = gtk.MessageDialog(_parent, gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                message_format=prompt)
    _dialog.run()
    _dialog.destroy()


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


def options(__widget, app):
    """
    Function to launch the user options configuration assistant.

    :param __widget: the gtk.Widget() calling this function.
    :type __widget: gtk.Widget
    :param app: the current instance of the RTK application.
    """

    Options(app)


def date_select(__widget, __event=None, entry=None):
    """
    Function to select a date from a calendar widget.

    :param gtk.Widget __widget: the gtk.Widget() that called this function.
    :param gtk.Entry entry: the gtk.Entry() widget in which to display the
                            date.
    :return: _date
    :rtype: date string (YYYY-MM-DD)
    """

    from datetime import datetime

    _dialog = Widgets.make_dialog(_(u"Select Date"),
                                  dlgbuttons=(gtk.STOCK_OK,
                                              gtk.RESPONSE_ACCEPT))

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


def set_cursor(controller, cursor):
    """
    Function to set the cursor for a gtk.gdk.Window()

    :param controller: the :py:class:`rtk.RTK.RTK` master data controller.
    :param gtk.gdk.Cursor cursor: the gtk.gdk.Cursor() to set.  Only handles
                                  one of the following:
                                  - gtk.gdk.X_CURSOR
                                  - gtk.gdk.ARROW
                                  - gtk.gdk.CENTER_PTR
                                  - gtk.gdk.CIRCLE
                                  - gtk.gdk.CROSS
                                  - gtk.gdk.CROSS_REVERSE
                                  - gtk.gdk.CROSSHAIR
                                  - gtk.gdk.DIAMOND_CROSS
                                  - gtk.gdk.DOUBLE_ARROW
                                  - gtk.gdk.DRAFT_LARGE
                                  - gtk.gdk.DRAFT_SMALL
                                  - gtk.gdk.EXCHANGE
                                  - gtk.gdk.FLEUR
                                  - gtk.gdk.GUMBY
                                  - gtk.gdk.HAND1
                                  - gtk.gdk.HAND2
                                  - gtk.gdk.LEFT_PTR - non-busy cursor
                                  - gtk.gdk.PENCIL
                                  - gtk.gdk.PLUS
                                  - gtk.gdk.QUESTION_ARROW
                                  - gtk.gdk.RIGHT_PTR
                                  - gtk.gdk.SB_DOWN_ARROW
                                  - gtk.gdk.SB_H_DOUBLE_ARROW
                                  - gtk.gdk.SB_LEFT_ARROW
                                  - gtk.gdk.SB_RIGHT_ARROW
                                  - gtk.gdk.SB_UP_ARROW
                                  - gtk.gdk.SB_V_DOUBLE_ARROW
                                  - gtk.gdk.TCROSS
                                  - gtk.gdk.TOP_LEFT_ARROW
                                  - gtk.gdk.WATCH - when application is busy
                                  - gtk.gdk.XTERM - selection bar
    """

    controller.module_book.get_window().set_cursor(gtk.gdk.Cursor(cursor))
    controller.list_book.get_window().set_cursor(gtk.gdk.Cursor(cursor))
    controller.work_book.get_window().set_cursor(gtk.gdk.Cursor(cursor))

    gtk.gdk.flush()

    return False


class Options(gtk.Window):                  # pylint: disable=R0902
    """
    An assistant to provide a GUI to the various configuration files for RTK.
    """

    def __init__(self, application):        # pylint: disable=R0915
        """
        Allows a user to set site-wide options.

        :param rtk application: the current instance of the RTK application.
        """

        import pango

        self._app = application

        gtk.Window.__init__(self)
        self.set_title(_(u"RTK - Options"))

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))

        self.notebook = gtk.Notebook()

        # ----- ----- ----- -- RTK module options - ----- ----- ----- #
        # Only show the active modules page if a RTK Program database is open.
        if Configuration.RTK_PROG_INFO[2] != '':
            _fixed = gtk.Fixed()

            self.chkRevisions = Widgets.make_check_button(_(u"Revisions"))
            self.chkFunctions = Widgets.make_check_button(_(u"Functions"))
            self.chkRequirements = Widgets.make_check_button(_(u"Requirements"))
            self.chkSoftware = Widgets.make_check_button(_(u"Software"))
            self.chkValidation = Widgets.make_check_button(_(u"Validation "
                                                             u"Tasks"))
            self.chkRG = Widgets.make_check_button(_(u"Reliability Tests"))
            self.chkIncidents = Widgets.make_check_button(_(u"Program "
                                                            u"Incidents"))
            self.chkSurvivalAnalysis = Widgets.make_check_button(_(u"Survival "
                                                                   u"Analysis"))

            self.btnSaveModules = gtk.Button(stock=gtk.STOCK_SAVE)

            _fixed.put(self.chkRevisions, 5, 5)
            _fixed.put(self.chkFunctions, 5, 35)
            _fixed.put(self.chkRequirements, 5, 65)
            _fixed.put(self.chkSoftware, 5, 95)
            _fixed.put(self.chkValidation, 5, 125)
            _fixed.put(self.chkRG, 5, 155)
            _fixed.put(self.chkIncidents, 5, 185)
            _fixed.put(self.chkSurvivalAnalysis, 5, 215)

            _fixed.put(self.btnSaveModules, 5, 305)

            self.btnSaveModules.connect('clicked', self._save_modules)

            _query = "SELECT fld_revision_active, fld_function_active, \
                             fld_requirement_active, fld_hardware_active, \
                             fld_software_active, fld_vandv_active, \
                             fld_testing_active, fld_rcm_active, \
                             fld_fraca_active, fld_fmeca_active, \
                             fld_survival_active, fld_rbd_active, \
                             fld_fta_active \
                      FROM tbl_program_info"
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=False)

            self.chkRevisions.set_active(_results[0][0])
            self.chkFunctions.set_active(_results[0][1])
            self.chkRequirements.set_active(_results[0][2])
            self.chkSoftware.set_active(_results[0][4])
            self.chkValidation.set_active(_results[0][5])
            self.chkRG.set_active(_results[0][6])
            self.chkIncidents.set_active(_results[0][8])
            self.chkSurvivalAnalysis.set_active(_results[0][10])

            _label = gtk.Label(_(u"RTK Modules"))
            _label.set_tooltip_text(_(u"Select active RTK modules."))
            self.notebook.insert_page(_fixed, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- Create default value options ----- ----- ----- #
        _fixed = gtk.Fixed()

        self.cmbModuleBookTabPosition = Widgets.make_combo(simple=True)
        self.cmbWorkBookTabPosition = Widgets.make_combo(simple=True)
        self.cmbListBookTabPosition = Widgets.make_combo(simple=True)

        self.txtFRMultiplier = Widgets.make_entry()
        self.txtDecimalPlaces = Widgets.make_entry(width=75)
        self.txtMissionTime = Widgets.make_entry(width=75)

        # Create color selection buttons.
        self.btnRevisionBGColor = gtk.ColorButton()
        self.btnRevisionFGColor = gtk.ColorButton()
        self.btnFunctionBGColor = gtk.ColorButton()
        self.btnFunctionFGColor = gtk.ColorButton()
        self.btnRequirementsBGColor = gtk.ColorButton()
        self.btnRequirementsFGColor = gtk.ColorButton()
        self.btnHardwareBGColor = gtk.ColorButton()
        self.btnHardwareFGColor = gtk.ColorButton()
        self.btnSoftwareBGColor = gtk.ColorButton()
        self.btnSoftwareFGColor = gtk.ColorButton()
        self.btnValidationBGColor = gtk.ColorButton()
        self.btnValidationFGColor = gtk.ColorButton()
        self.btnIncidentBGColor = gtk.ColorButton()
        self.btnIncidentFGColor = gtk.ColorButton()
        self.btnTestingBGColor = gtk.ColorButton()
        self.btnTestingFGColor = gtk.ColorButton()

        for _position in ["Bottom", "Left", "Right", "Top"]:
            self.cmbModuleBookTabPosition.append_text(_position)
            self.cmbWorkBookTabPosition.append_text(_position)
            self.cmbListBookTabPosition.append_text(_position)

        _label = Widgets.make_label(_(u"Module Book tab position:"))
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbModuleBookTabPosition, 310, 5)
        _label = Widgets.make_label(_(u"Work Book tab position:"))
        _fixed.put(_label, 5, 35)
        _fixed.put(self.cmbWorkBookTabPosition, 310, 35)
        _label = Widgets.make_label(_(u"List Book tab position:"))
        _fixed.put(_label, 5, 65)
        _fixed.put(self.cmbListBookTabPosition, 310, 65)
        _label = Widgets.make_label(_(u"Failure rate multiplier:"))
        _fixed.put(_label, 5, 125)
        _fixed.put(self.txtFRMultiplier, 310, 125)
        _label = Widgets.make_label(_(u"Decimal places:"))
        _fixed.put(_label, 5, 155)
        _fixed.put(self.txtDecimalPlaces, 310, 155)
        _label = Widgets.make_label(_(u"Default mission time:"))
        _fixed.put(_label, 5, 185)
        _fixed.put(self.txtMissionTime, 310, 185)

        _label = Widgets.make_label(_(u"Revision Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 225)
        _fixed.put(self.btnRevisionBGColor, 340, 225)
        _label = Widgets.make_label(_(u"Revision Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 255)
        _fixed.put(self.btnRevisionFGColor, 340, 255)
        _label = Widgets.make_label(_(u"Function Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 285)
        _fixed.put(self.btnFunctionBGColor, 340, 285)
        _label = Widgets.make_label(_(u"Function Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 315)
        _fixed.put(self.btnFunctionFGColor, 340, 315)
        _label = Widgets.make_label(_(u"Requirements Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 345)
        _fixed.put(self.btnRequirementsBGColor, 340, 345)
        _label = Widgets.make_label(_(u"Requirements Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 375)
        _fixed.put(self.btnRequirementsFGColor, 340, 375)
        _label = Widgets.make_label(_(u"Hardware Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 405)
        _fixed.put(self.btnHardwareBGColor, 340, 405)
        _label = Widgets.make_label(_(u"Hardware Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 435)
        _fixed.put(self.btnHardwareFGColor, 340, 435)
        _label = Widgets.make_label(_(u"Software Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 465)
        _fixed.put(self.btnSoftwareBGColor, 340, 465)
        _label = Widgets.make_label(_(u"Software Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 495)
        _fixed.put(self.btnSoftwareFGColor, 340, 495)
        _label = Widgets.make_label(_(u"Validation  Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 525)
        _fixed.put(self.btnValidationBGColor, 340, 525)
        _label = Widgets.make_label(_(u"Validation Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 555)
        _fixed.put(self.btnValidationFGColor, 340, 555)
        _label = Widgets.make_label(_(u"Incident Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 585)
        _fixed.put(self.btnIncidentBGColor, 340, 585)
        _label = Widgets.make_label(_(u"Incident Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 615)
        _fixed.put(self.btnIncidentFGColor, 340, 615)
        _label = Widgets.make_label(_(u"Testing Tree Background Color:"),
                                    width=350)
        _fixed.put(_label, 5, 645)
        _fixed.put(self.btnTestingBGColor, 340, 645)
        _label = Widgets.make_label(_(u"Testing Tree Foreground Color:"),
                                    width=350)
        _fixed.put(_label, 5, 675)
        _fixed.put(self.btnTestingFGColor, 340, 675)

        self.btnRevisionBGColor.connect('color-set', self._set_color, 0)
        self.btnRevisionFGColor.connect('color-set', self._set_color, 1)
        self.btnFunctionBGColor.connect('color-set', self._set_color, 2)
        self.btnFunctionFGColor.connect('color-set', self._set_color, 3)
        self.btnRequirementsBGColor.connect('color-set', self._set_color, 4)
        self.btnRequirementsFGColor.connect('color-set', self._set_color, 5)
        self.btnHardwareBGColor.connect('color-set', self._set_color, 6)
        self.btnHardwareFGColor.connect('color-set', self._set_color, 7)
        self.btnSoftwareBGColor.connect('color-set', self._set_color, 21)
        self.btnSoftwareFGColor.connect('color-set', self._set_color, 22)
        self.btnValidationBGColor.connect('color-set', self._set_color, 10)
        self.btnValidationFGColor.connect('color-set', self._set_color, 11)
        self.btnIncidentBGColor.connect('color-set', self._set_color, 12)
        self.btnIncidentFGColor.connect('color-set', self._set_color, 13)
        self.btnTestingBGColor.connect('color-set', self._set_color, 14)
        self.btnTestingFGColor.connect('color-set', self._set_color, 15)

        _label = gtk.Label(_(u"Look & Feel"))
        _label.set_tooltip_text(_(u"Allows setting default values in RTK."))
        self.notebook.insert_page(_fixed, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- - Create list edit options - ----- ----- ----- #
        _vbox = gtk.VBox()

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed)

        self.tvwListEditor = gtk.TreeView()
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.tvwListEditor.set_model(_model)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.tvwListEditor)
        _vbox.pack_end(_scrollwindow)

        self.rdoMeasurement = gtk.RadioButton(group=None,
                                              label=_(u"Edit measurement "
                                                      u"units"))
        self.rdoRequirementTypes = gtk.RadioButton(group=self.rdoMeasurement,
                                                   label=_(u"Edit requirement "
                                                           u"types"))
        self.rdoRiskCategory = gtk.RadioButton(group=self.rdoMeasurement,
                                               label=_(u"Edit risk "
                                                       u"categories"))
        self.rdoVandVTasks = gtk.RadioButton(group=self.rdoMeasurement,
                                             label=_(u"Edit V&V activity "
                                                     u"types"))
        self.rdoUsers = gtk.RadioButton(group=self.rdoMeasurement,
                                        label=_(u"Edit user list"))

        self.btnListEdit = gtk.Button(_(u"Edit List"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/edit.png')
        self.btnListEdit.set_image(_image)
        self.btnListEdit.connect('clicked', self._edit_list)

        self.btnListAdd = gtk.Button(_(u"Add Item"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/add.png')
        self.btnListAdd.set_image(_image)
        self.btnListAdd.connect('clicked', self._add_to_list)

        self.btnListRemove = gtk.Button(_(u"Remove Item"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        self.btnListRemove.set_image(_image)
        self.btnListRemove.connect('clicked', self._remove_from_list)

        _fixed.put(self.rdoMeasurement, 5, 5)
        _fixed.put(self.rdoRequirementTypes, 5, 35)
        _fixed.put(self.rdoRiskCategory, 5, 65)
        _fixed.put(self.rdoVandVTasks, 5, 95)
        _fixed.put(self.rdoUsers, 5, 125)
        _fixed.put(self.btnListEdit, 5, 205)
        _fixed.put(self.btnListAdd, 105, 205)
        _fixed.put(self.btnListRemove, 215, 205)

        for i in range(5):
            _cell = gtk.CellRendererText()
            _cell.set_property('background', '#FFFFFF')
            _cell.set_property('editable', 1)
            _cell.set_property('foreground', '#000000')
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD)
            _cell.connect('edited', self._cell_edit, i, _model)

            _column = gtk.TreeViewColumn()
            _column.set_alignment(0.5)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i)

            self.tvwListEditor.append_column(_column)

        _label = gtk.Label(_(u"Edit Lists"))
        _label.set_tooltip_text(_(u"Allows editing of lists used in RTK."))
        self.notebook.insert_page(_vbox, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- -- Create tree edit options - ----- ----- ----- #
        _fixed = gtk.Fixed()

        self.rdoRevision = gtk.RadioButton(group=None,
                                           label=_(u"Edit Revision tree "
                                                   u"layout"))
        self.rdoFunction = gtk.RadioButton(group=self.rdoRevision,
                                           label=_(u"Edit Function tree "
                                                   u"layout"))
        self.rdoRequirement = gtk.RadioButton(group=self.rdoRevision,
                                              label=_(u"Edit Requirement tree "
                                                      u"layout"))
        self.rdoHardware = gtk.RadioButton(group=self.rdoRevision,
                                           label=_(u"Edit Hardware tree "
                                                   u"layout"))
        self.rdoSoftware = gtk.RadioButton(group=self.rdoRevision,
                                           label=_(u"Edit Software tree "
                                                   u"layout"))
        self.rdoValidation = gtk.RadioButton(group=self.rdoRevision,
                                             label=_(u"Edit V&V tree layout"))
        self.rdoIncident = gtk.RadioButton(group=self.rdoRevision,
                                           label=_(u"Edit Program Incident "
                                                   u"tree layout"))
        self.rdoTesting = gtk.RadioButton(group=self.rdoRevision,
                                          label=_(u"Edit Testing tree layout"))
        self.rdoSurvival = gtk.RadioButton(group=self.rdoRevision,
                                           label=_(u"Edit Survival Analysis "
                                                   u"tree layout"))

        self.rdoPart = gtk.RadioButton(group=self.rdoRevision,
                                       label=_(u"Edit Part list layout"))

        self.rdoAllocation = gtk.RadioButton(group=self.rdoRevision,
                                             label=_(u"Edit Reliability "
                                                     u"Allocation worksheet "
                                                     u"layout"))
        self.rdoRiskAnalysis = gtk.RadioButton(group=self.rdoRevision,
                                               label=_(u"Edit Risk Analysis "
                                                       u"worksheet layout"))
        self.rdoSimilarItem = gtk.RadioButton(group=self.rdoRevision,
                                              label=_(u"Edit Similar Item "
                                                      u"Analysis worksheet "
                                                      u"layout"))
        self.rdoFMECA = gtk.RadioButton(group=self.rdoRevision,
                                        label=_(u"Edit FMEA/FMECA worksheet "
                                                u"layout"))

        self.btnTreeEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        self.btnTreeEdit.connect('button-release-event', self._edit_tree)

        _fixed.put(self.rdoRevision, 5, 5)
        _fixed.put(self.rdoFunction, 5, 35)
        _fixed.put(self.rdoRequirement, 5, 65)
        _fixed.put(self.rdoHardware, 5, 95)
        _fixed.put(self.rdoSoftware, 5, 125)
        _fixed.put(self.rdoValidation, 5, 155)
        _fixed.put(self.rdoTesting, 5, 185)
        _fixed.put(self.rdoIncident, 5, 215)
        _fixed.put(self.rdoSurvival, 5, 245)
        # _fixed.put(self.rdoAllocation, 5, 275)
        _fixed.put(self.rdoPart, 5, 275)
        _fixed.put(self.rdoRiskAnalysis, 5, 305)
        _fixed.put(self.rdoSimilarItem, 5, 335)
        _fixed.put(self.rdoFMECA, 5, 365)
        _fixed.put(self.btnTreeEdit, 5, 405)

        _label = gtk.Label(_(u"Edit Tree Layouts"))
        _label.set_tooltip_text(_(u"Allows editing of tree layouts used in "
                                  u"RTK."))
        self.notebook.insert_page(_fixed, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- Create tree edit gtk.TreeView ----- ----- ----- #
        _labels = [_(u"Default\nTitle"), _(u"User\nTitle"),
                   _(u"Column\nPosition"), _(u"Can\nEdit?"),
                   _(u"Is\nVisible?")]

        _vbox = gtk.VBox()

        self.tvwEditTree = gtk.TreeView()
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.tvwEditTree.set_model(_model)

        for i in range(5):
            if i == 0:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
            elif i > 0 and i < 3:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', '#FFFFFF')
                _cell.set_property('editable', 1)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.connect('edited', self._cell_edit, i, _model)
            elif i > 4:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
            else:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._cell_toggled, i, _model)

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_markup("<span weight='bold'>" + _labels[i] + "</span>")
            _label.show_all()

            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_alignment(0.5)
            _column.pack_start(_cell, True)
            if i < 3:
                _column.set_attributes(_cell, text=i)
            elif i > 4:
                _column.set_visible(0)
            else:
                _column.set_attributes(_cell, active=i)

            self.tvwEditTree.append_column(_column)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.tvwEditTree)

        _vbox.pack_start(_scrollwindow)

        _fixed = gtk.Fixed()

        self.btnSave = gtk.Button(_(u"Save"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        self.btnSave.set_image(_image)
        self.btnSave.connect('clicked', self._save_options)

        self.btnQuit = gtk.Button(_(u"Close"))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/quit.png')
        self.btnQuit.set_image(_image)
        self.btnQuit.connect('clicked', self._quit)

        _vbox.pack_end(_fixed, expand=False)

        _label = gtk.Label(_(u"Editor"))
        _label.set_tooltip_text(_(u"Displays the editor."))
        self.notebook.insert_page(_vbox, tab_label=_label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        _vbox = gtk.VBox()
        _vbox.pack_start(self.notebook)

        _buttonbox = gtk.HButtonBox()
        _buttonbox.set_layout(gtk.BUTTONBOX_END)
        _buttonbox.pack_start(self.btnSave)
        _buttonbox.pack_start(self.btnQuit)
        _vbox.pack_end(_buttonbox, expand=False)

        self.add(_vbox)

        self._load_defaults()

        self.show_all()

    def _load_defaults(self):
        """
        Method to load the current default values from the RTK configuration
        file.
        """

        _tab_pos = {'bottom': 0, 'left': 1, 'right': 2, 'top': 3}

        # Make a backup of the original configuration file.
        Configuration_file = Configuration.CONF_DIR + 'RTK.conf'

        _parser = SafeConfigParser()

        if file_exists(Configuration_file):
            _parser.read(Configuration_file)

            # Set tab positions.
            self.cmbModuleBookTabPosition.set_active(
                _tab_pos[_parser.get('General', 'treetabpos')])
            self.cmbWorkBookTabPosition.set_active(
                _tab_pos[_parser.get('General', 'booktabpos')])
            self.cmbListBookTabPosition.set_active(
                _tab_pos[_parser.get('General', 'listtabpos')])

            # Set numerical values.
            self.txtFRMultiplier.set_text(str(_parser.get('General',
                                                          'frmultiplier')))
            self.txtDecimalPlaces.set_text(str(_parser.get('General',
                                                           'decimal')))
            self.txtMissionTime.set_text(str(_parser.get('General',
                                                         'calcreltime')))

            # Set color options.
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'revisionbg'))
                self.btnRevisionBGColor.set_color(_color)
            except ValueError:
                self.btnRevisionBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'revisionfg'))
                self.btnRevisionFGColor.set_color(_color)
            except ValueError:
                self.btnRevisionFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'functionbg'))
                self.btnFunctionBGColor.set_color(_color)
            except ValueError:
                self.btnFunctionBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'functionfg'))
                self.btnFunctionFGColor.set_color(_color)
            except ValueError:
                self.btnFunctionFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'requirementbg'))
                self.btnRequirementsBGColor.set_color(_color)
            except ValueError:
                self.btnRequirementsBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'requirementfg'))
                self.btnRequirementsFGColor.set_color(_color)
            except ValueError:
                self.btnRequirementsFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'assemblybg'))
                self.btnHardwareBGColor.set_color(_color)
            except ValueError:
                self.btnHardwareBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'assemblyfg'))
                self.btnHardwareFGColor.set_color(_color)
            except(ValueError, NoOptionError):
                self.btnHardwareFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'softwarebg'))
                self.btnSoftwareBGColor.set_color(_color)
            except(ValueError, NoOptionError):
                self.btnSoftwareBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'softwarefg'))
                self.btnSoftwareFGColor.set_color(_color)
            except(ValueError, NoOptionError):
                self.btnSoftwareFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'validationbg'))
                self.btnValidationBGColor.set_color(_color)
            except ValueError:
                self.btnValidationBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors',
                                                          'validationfg'))
                self.btnValidationFGColor.set_color(_color)
            except ValueError:
                self.btnValidationFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'rgbg'))
                self.btnTestingBGColor.set_color(_color)
            except ValueError:
                self.btnTestingBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'rgfg'))
                self.btnTestingFGColor.set_color(_color)
            except ValueError:
                self.btnTestingFGColor.set_color(gtk.gdk.Color('#000000'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'fracabg'))
                self.btnIncidentBGColor.set_color(_color)
            except ValueError:
                self.btnIncidentBGColor.set_color(gtk.gdk.Color('#FFFFFF'))
            try:
                _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'fracafg'))
                self.btnIncidentFGColor.set_color(_color)
            except ValueError:
                self.btnIncidentFGColor.set_color(gtk.gdk.Color('#000000'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'partbg'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'partfg'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors',
            #                                            'overstressbg'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors',
            #                                            'overstressfg'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'taggedbg'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors', 'taggedfg'))
            # _color = gtk.gdk.Color('%s' % _parser.get('Colors',
            #                                            'nofrmodelfg'))

        return False

    def _set_color(self, colorbutton, rtk_colors):
        """
        Method to set the selected color.

        :param gtk.ColorButton colorbutton: the gtk.ColorButton() that called
                                            this method.
        :param int rtk_colors: the position in the RTK_COLORS global variable.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve the six digit hexidecimal version of the selected color.
        _color = colorbutton.get_color()
        try:
            _red = "{0:#0{1}}".format('%X' % int(_color.red / 255), 2)
        except ValueError:
            _red = '%X' % int(_color.red / 255)
        try:
            _green = "{0:#0{1}}".format('%X' % int(_color.green / 255), 2)
        except ValueError:
            _green = '%X' % int(_color.green / 255)
        try:
            _blue = "{0:#0{1}}".format('%X' % int(_color.blue / 255), 2)
        except ValueError:
            _blue = '%X' % int(_color.blue / 255)
        _color = '#%s%s%s' % (_red, _green, _blue)

        # Set the color variable.
        Configuration.RTK_COLORS[rtk_colors] = _color

        return False

    def _edit_tree(self, __button, __event):
        """
        Method to edit gtk.TreeView() layouts.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from lxml import etree

        (_name, _fmt_idx) = self._get_format_info()

        # Retrieve the default heading text from the format file.
        _path = "/root/tree[@name='%s']/column/defaulttitle" % _name
        _default = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve the default heading text from the format file.
        _path = "/root/tree[@name='%s']/column/usertitle" % _name
        _user = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve the column position from the format file.
        _path = "/root/tree[@name='%s']/column/position" % _name
        _position = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve whether or not the column is editable from the format file.
        _path = "/root/tree[@name='%s']/column/editable" % _name
        _editable = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve whether or not the column is visible from the format file.
        _path = "/root/tree[@name='%s']/column/visible" % _name
        _visible = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve datatypes from the format file.
        _path = "/root/tree[@name='%s']/column/datatype" % _name
        _datatype = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        # Retrieve widget types from the format file.
        _path = "/root/tree[@name='%s']/column/widget" % _name
        _widget = etree.parse(Configuration.RTK_FORMAT_FILE[_fmt_idx]).xpath(_path)

        _model = self.tvwEditTree.get_model()
        _model.clear()

        for _index, __ in enumerate(_default):
            _data = [_default[_index].text, _user[_index].text,
                     int(_position[_index].text), int(_editable[_index].text),
                     int(_visible[_index].text), _datatype[_index].text,
                     _widget[_index].text]
            _model.append(_data)

        if Configuration.RTK_PROG_INFO[2] == '':
            self.notebook.set_current_page(3)
        else:
            self.notebook.set_current_page(4)
        _child = self.notebook.get_nth_page(self.notebook.get_current_page())
        self.notebook.set_tab_label_text(_child, _(u"Edit %s Tree" % _name))

        return False

    def _cell_edit(self, __cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView() gtk.CellRenderer() is edited.

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: gtk.CellRenderer
        :param path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                     edited.
        :type path: string
        :param new_text: the new text in the edited gtk.CellRenderer().
        :type new_text: string
        :param position: the column position of the edited gtk.CellRenderer().
        :type position: integer
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: gtk.TreeModel
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
        Called whenever a gtl.TreeView() gtk.CellRenderer() is edited.

        :param cell: the gtk.CellRenderer() that was edited.
        :param path: the gtk.TreeView() path of the gtk.CellRenderer() that
                     was edited.
        :param position: the column position of the edited gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        model[path][position] = not cell.get_active()

        return False

    def _edit_list(self, __button):
        """
        Method to edit drop down list items.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False
        :rtype: bool
        """

        if self.rdoMeasurement.get_active():
            _query = "SELECT fld_measurement_id, fld_measurement_code \
                      FROM tbl_measurement_units"
            _header = ["", "Measurement Unit", "", "", "", ""]
            _pad = ('', '', '', '')
        elif self.rdoRequirementTypes.get_active():
            _query = "SELECT fld_requirement_type_id, \
                             fld_requirement_type_desc, \
                             fld_requirement_type_code \
                      FROM tbl_requirement_type"
            _header = ["", "Requirement Type", "Code", "", "", ""]
            _pad = ('', '', '')
        elif self.rdoRiskCategory.get_active():
            _query = "SELECT fld_category_id, fld_category_noun, \
                             fld_category_value \
                      FROM tbl_risk_category"
            _header = ["", "Risk Category", "Value", "", "", ""]
            _pad = ('', '', '')
        elif self.rdoVandVTasks.get_active():
            _query = "SELECT fld_validation_type_id, \
                             fld_validation_type_desc, \
                             fld_validation_type_code \
                      FROM tbl_validation_type"
            _header = ["", "Validation Type", "Code", "", "", ""]
            _pad = ('', '', '')
        elif self.rdoUsers.get_active():
            _query = "SELECT fld_user_id, fld_user_lname, fld_user_fname, \
                             fld_user_email, fld_user_phone, fld_user_group \
                      FROM tbl_users"
            _header = ["", "User Last Name", "User First Name", "eMail",
                       "Phone", "Work Group"]
            _pad = ()

        _results = self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx)
        try:
            _n_entries = len(_results)
        except TypeError:
            _n_entries = 0

        # Update the column headings and set appropriate columns visible.
        _columns = self.tvwListEditor.get_columns()
        for _index, _column in enumerate(_columns):
            _column.set_title(_header[_index])
            if _header[_index] == '':
                _column.set_visible(False)
            else:
                _column.set_visible(True)

        # Load the results.
        _model = self.tvwListEditor.get_model()
        _model.clear()
        for i in range(_n_entries):
            _model.append(_results[i] + _pad)

        return False

    def _add_to_list(self, __button):
        """
        Method to add a row to the list editor gtk.TreeView().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Add a new row.
        _model = self.tvwListEditor.get_model()
        _row = _model.append([-1, "", "", "", "", ""])

        # Select and activate the new row.
        _path = _model.get_path(_row)
        _column = self.tvwListEditor.get_column(1)
        self.tvwListEditor.row_activated(_path, _column)
        self.tvwListEditor.set_cursor(_path, _column, True)

        return False

    def _remove_from_list(self, __button):
        """
        Method to remove the selected row from the list editor gtk.TreeView().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.tvwListEditor.get_selection().get_selected()

        if self.rdoMeasurement.get_active():
            _query = "DELETE FROM tbl_measurement_units \
                      WHERE fld_measurement_id=%d" % \
                     _model.get_value(_row, 0)
        elif self.rdoRequirementTypes.get_active():
            _query = "DELETE FROM tbl_requirement_type \
                      WHERE fld_requirement_type_id=%d" % \
                     _model.get_value(_row, 0)
        elif self.rdoRiskCategory.get_active():
            _query = "DELETE FROM tbl_risk_category \
                      WHERE fld_category_id=%d" % \
                     _model.get_value(_row, 0)
        elif self.rdoVandVTasks.get_active():
            _query = "DELETE tbl_validation_type \
                      WHERE fld_validation_type_id=%d" % \
                     _model.get_value(_row, 0)
        elif self.rdoUsers.get_active():
            rtk_information(_(u"You cannot remove a user from the RTK Program."
                              u"  Retaining all users, past and present, is "
                              u"necessary to ensure audit trails remain "
                              u"intact."))
            return False

        if not self._app.COMDB.execute_query(_query, None, self._app.ComCnx,
                                             commit=True):
            rtk_error(_(u"Problem removing entry from list."))
            return True

        _model.remove(_row)

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

    def _save_options(self, __button):
        """
        Method to select the proper save function depending on the selected
        page in the gtk.Notebook().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from shutil import copyfile

        # Make a backup of the original configuration file.
        Configuration_file = Configuration.CONF_DIR + 'RTK.conf'
        copyfile(Configuration_file, Configuration_file + '.bak')

        # Find out which page is selected in the gtk.Notebook().
        _page = self.notebook.get_current_page()
        if Configuration.RTK_PROG_INFO[2] == '':
            _page += 1

        # Call the proper save function.
        if _page == 0:
            _error = self._save_modules()
        elif _page == 1:
            _error = self._save_defaults()
        elif _page == 2:
            _error = self._save_list()
        elif _page == 4:
            _error = self._save_tree_layout()

        if _error:
            rtk_warning(_(u"Problem saving your RTK configuration.  "
                          u"Restoring previous configuration values."))
            copyfile(Configuration_file + '.bak', Configuration_file)
            return True

        return False

    def _save_modules(self):
        """
        Method to save the configuration changes made by the user.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Save the active modules for the open RTK Program database.
        if Configuration.RTK_PROG_INFO[2] != '':
            _values = (self.chkRevisions.get_active(),
                       self.chkFunctions.get_active(),
                       self.chkRequirements.get_active(),
                       self.chkSoftware.get_active(),
                       self.chkValidation.get_active(),
                       self.chkRG.get_active(),
                       0, self.chkIncidents.get_active(),
                       0, self.chkSurvivalAnalysis.get_active(), 0, 0)

            _query = "UPDATE tbl_program_info \
                      SET fld_revision_active=%d, fld_function_active=%d, \
                          fld_requirement_active=%d, fld_software_active=%d, \
                          fld_vandv_active=%d, fld_testing_active=%d, \
                          fld_rcm_active=%d, fld_fraca_active=%d, \
                          fld_fmeca_active=%d, fld_survival_active=%d, \
                          fld_rbd_active=%d, fld_fta_active=%d" % _values
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                return True

        return False

    def _save_defaults(self):
        """
        Method to save the default values to the RTK configuration file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        Configuration_file = Configuration.CONF_DIR + 'RTK.conf'

        _parser = SafeConfigParser()

        # Write the new colors to the configuration file.
        if file_exists(Configuration_file):
            _parser.read(Configuration_file)

            try:
                _parser.set('General', 'frmultiplier',
                            str(float(self.txtFRMultiplier.get_text()) / 1.0))
            except ValueError:
                _parser.set('General', 'frmultiplier', '1.0')

            try:
                _parser.set('General', 'calcreltime',
                            str(float(self.txtMissionTime.get_text()) / 1.0))
            except ValueError:
                _parser.set('General', 'calcreltime', '10.0')

            try:
                _parser.set('General', 'decimal',
                            str(int(self.txtDecimalPlaces.get_text()) / 1))
            except ValueError:
                _parser.set('General', 'decimal', '6')

            try:
                _parser.set('General', 'treetabpos',
                            self.cmbModuleBookTabPosition.get_active_text().lower())
            except AttributeError:
                _parser.set('General', 'treetabpos', 'top')

            try:
                _parser.set('General', 'listtabpos',
                            self.cmbListBookTabPosition.get_active_text().lower())
            except AttributeError:
                _parser.set('General', 'listtabpos', 'right')

            try:
                _parser.set('General', 'booktabpos',
                            self.cmbWorkBookTabPosition.get_active_text().lower())
            except AttributeError:
                _parser.set('General', 'booktabpos', 'bottom')

            _parser.set('Colors', 'revisionbg', Configuration.RTK_COLORS[0])
            _parser.set('Colors', 'revisionfg', Configuration.RTK_COLORS[1])
            _parser.set('Colors', 'functionbg', Configuration.RTK_COLORS[2])
            _parser.set('Colors', 'functionfg', Configuration.RTK_COLORS[3])
            _parser.set('Colors', 'requirementbg', Configuration.RTK_COLORS[4])
            _parser.set('Colors', 'requirementfg', Configuration.RTK_COLORS[5])
            _parser.set('Colors', 'assemblybg', Configuration.RTK_COLORS[6])
            _parser.set('Colors', 'assemblyfg', Configuration.RTK_COLORS[7])
            _parser.set('Colors', 'validationbg', Configuration.RTK_COLORS[8])
            _parser.set('Colors', 'validationfg', Configuration.RTK_COLORS[9])
            _parser.set('Colors', 'rgbg', Configuration.RTK_COLORS[10])
            _parser.set('Colors', 'rgfg', Configuration.RTK_COLORS[11])
            _parser.set('Colors', 'fracabg', Configuration.RTK_COLORS[12])
            _parser.set('Colors', 'fracafg', Configuration.RTK_COLORS[13])
            _parser.set('Colors', 'partbg', Configuration.RTK_COLORS[14])
            _parser.set('Colors', 'partfg', Configuration.RTK_COLORS[15])
            _parser.set('Colors', 'overstressbg', Configuration.RTK_COLORS[16])
            _parser.set('Colors', 'overstressfg', Configuration.RTK_COLORS[17])
            _parser.set('Colors', 'taggedbg', Configuration.RTK_COLORS[18])
            _parser.set('Colors', 'taggedfg', Configuration.RTK_COLORS[19])
            _parser.set('Colors', 'nofrmodelfg', Configuration.RTK_COLORS[20])
            _parser.set('Colors', 'softwarebg', Configuration.RTK_COLORS[21])
            _parser.set('Colors', 'softwarefg', Configuration.RTK_COLORS[22])

            try:
                _parser.write(open(Configuration_file, 'w'))
                return False
            except EnvironmentError:
                return True

    def _save_list(self):
        """
        Method for saving the currently active list in the List Editor
        gtk.TreeView().
        """

        def _save_line_item(model, __path, row, self):
            """
            Function to save an individual gtk.TreeIter() in the List Editor
            gtk.TreeView().

            :param gtk.TreeModel model: the List Editor gtk.TreeModel().
            :param str __path: the path of the active gtk.TreeIter() in the
                               List Editor gtk.TreeModel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the List
                                     Editor gtk.TreeModel().
            :return: False if successful or True if an error is encountered.
            :rtype: bool
            """

            if self.rdoMeasurement.get_active():
                _query = "REPLACE INTO tbl_measurement_units \
                          (fld_measurement_id, fld_measurement_code) \
                          VALUES((SELECT fld_measurement_id \
                                  FROM tbl_measurement_units \
                                  WHERE fld_measurement_code='%s'), \
                                 '%s')" % \
                         (model.get_value(row, 1), model.get_value(row, 1))
            elif self.rdoRequirementTypes.get_active():
                _query = "REPLACE INTO tbl_requirement_type \
                          (fld_requirement_type_id, \
                           fld_requirement_type_desc, \
                           fld_requirement_type_code) \
                          VALUES((SELECT fld_requirement_type_id \
                                  FROM tbl_requirement_type \
                                  WHERE fld_requirement_type_desc = '%s'), \
                                '%s', '%s')" % \
                         (model.get_value(row, 1), model.get_value(row, 1),
                          model.get_value(row, 2))
            elif self.rdoRiskCategory.get_active():
                _query = "REPLACE INTO tbl_risk_category \
                          (fld_category_id, fld_category_noun, \
                           fld_category_value) \
                          VALUES((SELECT fld_category_id \
                                  FROM tbl_risk_category \
                                  WHERE fld_category_noun='%s'), '%s', %d)" % \
                         (model.get_value(row, 1), model.get_value(row, 1),
                          int(model.get_value(row, 2)))
            elif self.rdoVandVTasks.get_active():
                _query = "REPLACE INTO tbl_validation_type \
                          (fld_validation_type_id, fld_validation_type_desc, \
                           fld_validation_type_code) \
                          VALUES((SELECT fld_validation_type_id \
                                  FROM tbl_validation_type \
                                  WHERE fld_validation_type_desc='%s'), \
                                 '%s', '%s')" % \
                         (model.get_value(row, 1), model.get_value(row, 1),
                          model.get_value(row, 2))
            elif self.rdoUsers.get_active():
                _query = "INSERT INTO tbl_users \
                          (fld_user_lname, fld_user_fname, \
                           fld_user_email, fld_user_phone, fld_user_group) \
                          VALUES((SELECT fld_user_id \
                                  FROM tbl_users \
                                  WHERE fld_user_lname='%s' \
                                  AND fld_user_fname='%s'), \
                                 '%s', '%s', '%s', '%s', '%s')" % \
                         (model.get_value(row, 1), model.get_value(row, 2),
                          model.get_value(row, 1), model.get_value(row, 2),
                          model.get_value(row, 3), model.get_value(row, 4),
                          model.get_value(row, 5))

            # Update the RTK Common Database table.
            if not self._app.COMDB.execute_query(_query, None,
                                                 self._app.ComCnx,
                                                 commit=True):
                return True

            return False

        set_cursor(self._app, gtk.gdk.WATCH)

        _model = self.tvwListEditor.get_model()
        _model.foreach(_save_line_item, self)

        set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _save_tree_layout(self):
        """
        Method for saving the gtk.TreeView() layout file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_name, _fmt_idx) = self._get_format_info()

        # Get the format file for the gtk.TreeView to be edited.
        _format_file = Configuration.RTK_FORMAT_FILE[_fmt_idx]
        _basename = os.path.basename(_format_file)

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

        _model = self.tvwEditTree.get_model()
        _row = _model.get_iter_first()
        while _row is not None:
            _file.write("\t\t<column>\n")
            _file.write("\t\t\t<defaulttitle>%s</defaulttitle>\n" %
                        _model.get_value(_row, 0))
            _file.write("\t\t\t<usertitle>%s</usertitle>\n" %
                        _model.get_value(_row, 1))
            _file.write("\t\t\t<datatype>%s</datatype>\n" %
                        _model.get_value(_row, 5))
            _file.write('\t\t\t<position>%d</position>\n' %
                        _model.get_value(_row, 2))
            _file.write("\t\t\t<widget>%s</widget>\n" %
                        _model.get_value(_row, 6))
            _file.write("\t\t\t<editable>%d</editable>\n" %
                        _model.get_value(_row, 3))
            _file.write("\t\t\t<visible>%d</visible>\n" %
                        _model.get_value(_row, 4))
            _file.write("\t\t</column>\n")

            _row = _model.iter_next(_row)

        _file.write("\t</tree>\n")
        _file.write("</root>")
        _file.close()

        return False

    def _quit(self, __button):
        """
        Method to quit the options gtk.Assistant().

        :param gtk.Button __button: the gtk.Button() that called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.destroy()

        return False
