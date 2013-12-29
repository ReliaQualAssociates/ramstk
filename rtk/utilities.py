#!/usr/bin/env python
"""
utilities contains utility functions for interacting with the RTK
application.  Import this module as _util in other modules that need to
interact with the RTK application.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       utilities.py is part of The RTK Project
#
# All rights reserved.

import sys

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

    _conf.CONF_DIR = conf.conf_dir
    if(not dir_exists(_conf.CONF_DIR)):
        application_error(_("Configuration directory %s does not exist.  Exiting.") % _conf.CONF_DIR)

    _conf.ICON_DIR = conf.conf_dir + icondir + '/'
    if(not dir_exists(_conf.ICON_DIR)):
        _conf.ICON_DIR = conf.icon_dir

    _conf.DATA_DIR = conf.conf_dir + datadir + '/'
    if(not dir_exists(_conf.DATA_DIR)):
        _conf.DATA_DIR = conf.data_dir

    _conf.LOG_DIR = conf.conf_dir + logdir + '/'
    if(not dir_exists(_conf.LOG_DIR)):
        _conf.LOG_DIR = conf.log_dir

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

    return(logger)


def parse_config(configfile):
    """
    This function parses the XML configuration file passed as a parameter.

    Keyword Arguments:
    configfile -- the configuration file that needs to be parsed.
    """

    from lxml import etree

    tree = etree.parse(configfile)

    return(tree)


def split_string(string):
    """
    Splits a colon-delimited string into its constituent parts.

    Keyword Arguments:
    string -- the colon delimited string that needs to be split into a
              list.
    """

    strlist = string.rsplit(':')

    return(strlist)


def none_to_string(string):
    """ Converts None types to an empty string. """

    if string is None:
        return('')
    else:
        return(string)


def string_to_boolean(string):
    """
    Converts string representations of TRUE/FALSE to an integer value for use
    in the database.

    Keyword Arguments:
    string -- the string to convert.
    """

    result = 0

    string = str(string)

    if(string.lower() == 'true' or string.lower() == 'yes' or
       string.lower() == 't' or string.lower() == 'y'):
        result = 1

    return(result)


def date_to_ordinal(date):
    """
    Converts date strings to oridinal dates for use in the database.

    Keyword Arguments:
    date -- the date string to convert.
    """

    from dateutil.parser import parse

    try:
        _results_ = parse(str(date)).toordinal()
    except ValueError:
        _results_ = parse('01/01/70').toordinal()

    return(_results_)


def ordinal_to_date(ordinal):
    """
    Converts ordinal dates to date strings in ISO 8601 format.

    Keyword Arguments:
    ordinal -- the ordinal date to convert.
    """

    from datetime import datetime

    try:
        results = str(datetime.fromordinal(int(ordinal)).strftime('%Y-%m-%d'))
    except ValueError:
        results = str(datetime.fromordinal(719163).strftime('%Y-%m-%d')),

    return(results)


def tuple_to_list(_tuple_, _list_):
    """
    Appends a tuple to a list.

    Keyword Arguments:
    _tuple_ -- the tuple to add to the list.
    _list_  -- the existing list to add the tuple elements to.
    """

    for i in range(len(_tuple_)):
        _list_.append(_tuple_[i])

    return(_list_)


def dir_exists(_directory_):
    """
    Checks for the existence of a directory.

    Keyword Arguments:
    directory -- a string representing the directory path to check for.
    """

    from os import path

    if path.isdir(_directory_):
        return True
    else:
        return False


def file_exists(_file_):
    """
    Checks if a file exists.

    Keyword Arguments:
    file -- a string representing the filepath to check for.
    """

    from os import path

    if path.isfile(_file_):
        return True
    else:
        return False


def create_project(widget, app):
    """
    Creates a new RTK Project.

    Keyword Arguments:
    widget -- the widget that called this function.
    app    -- the RTK application.
    """

    if(_conf.BACKEND == 'mysql'):

        login = _login.Login(_(u"Create a RTK Program Database"))
        if(login.answer != gtk.RESPONSE_ACCEPT):
            return True

        dialog = _widg.make_dialog(_(u"RTK - New Program"))

        label = _widg.make_label(_(u"New Program Name"))
        txtProgName = _widg.make_entry()
        dialog.vbox.pack_start(label)
        dialog.vbox.pack_start(txtProgName)
        label.show()
        txtProgName.show()

        label = _widg.make_label(_(u"Assigned User"))
        txtUser = _widg.make_entry()
        dialog.vbox.pack_start(label)
        dialog.vbox.pack_start(txtUser)
        label.show()
        txtUser.show()

        label = _widg.make_label(_(u"Using Password"))
        txtPasswd = _widg.make_entry()
        txtPasswd.set_invisible_char("*")
        dialog.vbox.pack_start(label)
        dialog.vbox.pack_start(txtPasswd)
        label.show()
        txtPasswd.show()

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
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

    elif(_conf.BACKEND == 'sqlite3'):
        dialog = gtk.FileChooserDialog(title=_(u"Create a RTK Program Database"),
                                       action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                       buttons=(gtk.STOCK_NEW, gtk.RESPONSE_ACCEPT,
                                                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            new_program = dialog.get_filename()
            new_program = new_program + '.rfb'

            _conf.RTK_PROG_INFO[2] = new_program
            cnx = app.DB.get_connection(_conf.RTK_PROG_INFO[2])

            sqlfile = open(_conf.DATA_DIR + 'newprogram_sqlite3.sql', 'r')
            queries = sqlfile.read().split(';')

            for i in range(len(queries)):
                results = app.DB.execute_query(queries[i],
                                               None,
                                               cnx,
                                               commit=True)

            cnx.close()

            open_project(widget, app, dlg=0, filename=new_program)

        dialog.destroy()

    return False


def open_project(widget, app, dlg=1, filename=''):
    """
    Shows the RTK databases available on the selected server and allows the
    user to select the one he/she wishes to use.

    Keyword Arguments:
    widget -- the widget that called this function.
    app    -- the RTK application.
    dlg    -- whether or not to display a file chooser dialog.  0=No, 1=Yes.
    """

    from time import sleep

    if(_conf.BACKEND == 'mysql'):

        login = _login.Login(_(u"RTK Program Database Login"))

        if(login.answer != gtk.RESPONSE_ACCEPT):
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

        numprograms = len(results)
        for i in range(numprograms):
            # Don't display the MySQL administrative/test databases.
            if(results[i][0] != 'information_schema' and \
               results[i][0] != 'test' and \
               results[i][0] != 'mysql' and \
               results[i][0] != 'RTKcom' and
               results[i][0] != '#mysql50#lost+found'):
                iter_ = model.append(None, [results[i][0]])

        dialog.vbox.pack_start(scrollwindow)
        treeview.show()
        scrollwindow.show()

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            selection = treeview.get_selection()
            (model, treerow) = selection.get_selected()
            path = model.get_path(treerow)
            row = model.get_iter(path)
            _conf.RTK_PROG_INFO[2] = model.get_value(row, 0)
            dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            app.load_system()

        dialog.destroy()

        cnx.close()

    elif(_conf.BACKEND == 'sqlite3'):

        if(dlg == 1):
            dialog = gtk.FileChooserDialog(title=_(u"RTK - Open Program"),
                                           buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                                    gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

            # Set some filters to select all files or only some text files.
            filter = gtk.FileFilter()
            filter.set_name(_(u"RTK Project Files"))
            #filter.add_mime_type("text/txt")
            filter.add_pattern("*.rfb")
            dialog.add_filter(filter)

            filter = gtk.FileFilter()
            filter.set_name(_(u"All files"))
            filter.add_pattern("*")
            dialog.add_filter(filter)

            response = dialog.run()

            if(response == gtk.RESPONSE_ACCEPT):
                _conf.RTK_PROG_INFO[2] = dialog.get_filename()
                dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                app.load_system()

            dialog.destroy()

        else:
            _conf.RTK_PROG_INFO[2] = filename
            app.load_system()

    return False


def save_project(widget, _app):
    """
    Saves the RTK information to the project's MySQL database.

    Keyword Arguments:
    widget -- the widget that is calling this function.
    _app   -- the RTK application.
    """

    if not _app.LOADED:
        return True

    _app.winTree.statusbar.push(2, _(u"Saving"))

    _app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    _app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    _app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

    _app.REVISION.revision_save()
    _app.FUNCTION.function_save()
    _app.REQUIREMENT.requirement_save(None)
    _app.HARDWARE.hardware_save()
    _app.SOFTWARE.software_save()
    _app.winParts.save_component()

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
    results = _app.DB.execute_query(query,
                                    None,
                                    _app.ProgCnx,
                                    commit=True)

    conf = _conf.RTKConf('user')
    #conf.write_configuration()

    _app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
    _app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
    _app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    _app.winTree.statusbar.pop(2)

    return False


def delete_project(widget, _app):
    """
    Deletes an existing RTK Project.

    Keyword Arguments:
    widget -- the widget that called this function.
    _app   -- the RTK application.
    """

    if(_conf.BACKEND == 'mysql'):
        query = "SHOW DATABASES"
        cnx = _app.DB.get_connection(_conf.RTK_PROG_INFO)
        results = _app.DB.execute_query(query,
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
            if(results[i][0] != 'information_schema' and results[i][0] != 'test'):
                iter_ = model.append(None, [results[i][0]])

        dialog.vbox.pack_start(scrollwindow)
        treeview.show()
        scrollwindow.show()

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            selection = treeview.get_selection()
            (model, treerow) = selection.get_selected()
            path = model.get_path(treerow)
            iter = model.get_iter(path)
            project = model.get_value(iter, 0)
        else:
            dialog.destroy()

        if(confirm_action(_("Really delete %s?") % project, 'question')):
            query = "DROP DATABASE IF EXISTS %s"
            results = _app.DB.execute_query(query,
                                            project,
                                            cnx)

            dialog.destroy()
        else:
            dialog.destroy()

        cnx.close()

    elif(_conf.BACKEND == 'sqlite3'):

        import os

        dialog = gtk.FileChooserDialog(_("RTK - Delete Program"),
                                       None,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            project = dialog.get_filename()
        else:
            dialog.destroy()

        if(confirm_action(_(u"Really delete %s?") % project), 'question'):
            os.remove(project)
            dialog.destroy()
        else:
            dialog.destroy()


def import_project(widget, app):
    """
    Imports project information from external files such as Excel, CVS, other
    delimited text files, etc.

    Keyword Arguments:
    widget -- the GTK widget that called the function.
    app    -- the RTK application object.
    """

# TODO: Write function to import project information from various other formats; Excel, CSV, other delimited files.
    _dialog_ = gtk.FileChooserDialog(_("Select Project to Import"), None,
                                     gtk.FILE_CHOOSER_ACTION_OPEN,
                                     (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    _response_ = _dialog_.run()
    if(_response_ == gtk.RESPONSE_ACCEPT):
        print "Importing project."

    _dialog_.destroy()


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
    dialog.vbox.pack_start(hbox)
    hbox.show_all()

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()
        return True
    else:
        dialog.destroy()
        return False


def application_error(_prompt_, _image_='important', _parent_=None):
    """
    Dialog to display runtime errors to the user.

    Keyword Arguments:
    _prompt_ -- the prompt to display in the dialog.
    _image_  -- the icon to display in the dialog.
    _parent_ -- the parent window, if any, for the dialog.
    """

    dialog = _widg.make_dialog(_(u"RTK Error"), _buttons_=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    hbox = gtk.HBox()

    file_image = _conf.ICON_DIR + '32x32/' + _image_ + '.png'
    image = gtk.Image()
    image.set_from_file(file_image)
    hbox.pack_start(image)

    label = _widg.make_label(_prompt_, width=400, height=200)
    label.set_justify(gtk.JUSTIFY_LEFT)
    hbox.pack_end(label)
    dialog.vbox.pack_start(hbox)
    hbox.show_all()

    dialog.run()

    dialog.destroy()

    return False


def add_items(title, prompt=""):
    """
    Adds one or more items to a treeview hierarchy.

    Keyword Arguments:
    title -- the string to put in the title bar of the dialog.
    prompt -- the prompt to put on the dialog.
    """

    _dialog_ = _widg.make_dialog(title)

    _fixed_ = gtk.Fixed()
    _fixed_.set_size_request(600, 80)

    _label_ = _widg.make_label(prompt, 150, 80)
    txtQuantity = _widg.make_entry(_width_=100)
    txtQuantity.set_text("1")

    _fixed_.put(_label_, 5, 10)
    _fixed_.put(txtQuantity, 160, 38)
    _fixed_.show_all()

    _dialog_.vbox.pack_start(_fixed_)

    _response_ = _dialog_.run()

    if(_response_ == gtk.RESPONSE_ACCEPT):
        _numitems_ = int(txtQuantity.get_text())
    else:
        _numitems_ = 0

    _dialog_.destroy()

    return(_numitems_)


def cut_copy_paste(widget, action):
    """
    Cuts, copies, and pastes.

    Keyword Arguments:
    widget -- the widget that called this function.
    action -- whether to cut (0), copy (1), or paste (2).
    """

    # TODO: Write code to cut/copy/paste.
    clipboard = gtk.Clipboard(gtk.gdk.display_manager_get().get_default_display(),
                              "CLIPBOARD")

    if(action == 0):
        print "Cutting."
    elif(action == 1):
        print clipboard.set_text("I copied this.")
        print "Copying."
    elif(action == 2):
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


def find_all_in_list(list, value, start=0):
    """
    Finds all instances of value in the list starting at position start.

    Keyword Arguments:
    list  -- the list to search.
    value -- the value to search for.
    start -- the position in the list to start the search.
    """

    positions = []
    i = start - 1
    try:
        i = list.index(value, i+1)
        positions.append(i)
        return(positions)
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


def create_comp_ref_des(widget, app):
    """
    Iterively creates composite reference designators.

    Keyword Arguments:
    widget -- the GTK widget that called the function.
    app    -- the RTK application object.
    """

    treemodel = app.HARDWARE.model
    row = treemodel.get_iter_root()

    build_comp_ref_des(treemodel, row)


def build_comp_ref_des(treemodel, row):
    """
    Creates the composite reference designator for the currently selected row
    in the System gtk.Treemodel.

    Keyword Arguments:
    treemodel -- the HARDWARE gtk.Treemodel.
    row       -- the currently selected row in the HARDWARE gtk.Treemodel.
    """

    ref_des = treemodel.get_value(row, 68)

    if(treemodel.iter_has_child(row)):
        for i in range(treemodel.iter_n_children(row)):
            build_comp_ref_des(treemodel, treemodel.iter_nth_child(row, i))

        if(not treemodel.iter_parent(row)):
            comp_ref_des = ref_des
        else:
            p_row = treemodel.iter_parent(row)
            p_comp_ref_des = treemodel.get_value(p_row, 12)
            comp_ref_des = p_comp_ref_des + ":" + ref_des

    else:
        p_row = treemodel.iter_parent(row)
        p_comp_ref_des = treemodel.get_value(p_row, 12)
        comp_ref_des = p_comp_ref_des + ":" + ref_des

    treemodel.set_value(row, 12, comp_ref_des)

    return False


def add_parts_system_hierarchy(widget, app):
    """
    This function adds parts from the incident reports to the system hierarchy.
    The higher level structure (e.g., sub-systesm, assemblies, etc.) must
    already exist.  This function will populate the hierarchy with the parts
    in the program incident data.

    Keyword Arguments:
    widget -- the GTK widget that called the function.
    app    -- the RTK application object.
    """

# Find the revision id.
    if(_conf.RTK_MODULES[0] == 1):
        _revision_id_ = app.REVISION.revision_id
    else:
        _revision_id_ = 0

# Find the last assembly id being used and increment it by one as the starting
# assembly id.
    _query_ = "SELECT MAX(fld_assembly_id) FROM tbl_system"
    _assembly_id_ = app.DB.execute_query(_query_,
                                         None,
                                         app.ProgCnx)
    _assembly_id_ = _assembly_id_[0][0] + 1

# Get the list of part numbers to add to the system hierarchy and their
# associated hardware id's from the incident reports.
    _query_ = "SELECT DISTINCT(t1.fld_part_num), t2.fld_hardware_id \
               FROM tbl_incident_detail AS t1 \
               INNER JOIN tbl_incident AS t2 \
               ON t1.fld_incident_id=t2.fld_incident_id \
               WHERE t2.fld_revision_id=%d \
               ORDER BY t2.fld_hardware_id" % _revision_id_
    _results_ = app.DB.execute_query(_query_,
                                     None,
                                     app.ProgCnx)

    _n_added_ = 0
    for i in range(len(_results_)):
        _tmp_ = app.HARDWARE.dicHARDWARE[_results_[i][1]]

# Create a description from the part prefix and part index.
        _part_name_ = str(_conf.RTK_PREFIX[6]) + ' ' + \
                      str(_conf.RTK_PREFIX[7])

# Create a tuple of values to pass to the component_add queries.  The values
# are:
#   Revision ID
#   Assembly ID
#   Name
#   Part?
#   Parent Assembly
#   Part Number
        _values_ = (_revision_id_, _assembly_id_, _part_name_, 1,
                    _tmp_[len(_tmp_) - 1], _results_[i][0])

# Add the new component to each table needing a new entry and increment the
# count of components added.
        _added_ = component_add(app, _values_)

        if not _added_:
            _n_added_ += 1

# Increment the part index and assembly id.
        _conf.RTK_PREFIX[7] = _conf.RTK_PREFIX[7] + 1
        _assembly_id_ += 1

    if _n_added_ != len(_results_):
        application_error(_(u"There was an error adding one or more components to the database.  Check the RTK error log for more details."))

    app.REVISION.load_tree()
#TODO: Need to find and select the previously selected revision before loading the hardware tree.
    app.HARDWARE.load_tree()

    return False


def component_add(app, _values_):
    """
    Function to add a component to the RTK Program database.

    Keyword Arguments:
    app     -- the running instances of the RTK application.
    _values -- tuple containing the values to pass to the queries.
    """

# Insert the new part into tbl_system.
    _query_ = "INSERT INTO tbl_system (fld_revision_id, fld_assembly_id, \
                                       fld_name, fld_part, \
                                       fld_parent_assembly, \
                                       fld_part_number) \
               VALUES (%d, %d, '%s', %d, '%s', '%s')" % _values_
    _inserted_ = app.DB.execute_query(_query_,
                                      None,
                                      app.ProgCnx,
                                      commit=True)

    if not _inserted_:
        app.debug_log.error("utilities.py:component_add - Failed to add new component to system table.")
        pass

# Insert the new component into tbl_prediction.
    _query = "INSERT INTO tbl_prediction \
              (fld_revision_id, fld_assembly_id) \
              VALUES (%d, %d)" % (_values[0], _values[1])
    _inserted = app.DB.execute_query(_query,
                                     None,
                                     app.ProgCnx,
                                     commit=True)
    if not _inserted:
        app.debug_log.error("utilities.py:component_add - Failed to add new component to prediction table.")
        pass

# Insert the new component into tbl_fmeca.
    _query = "INSERT INTO tbl_fmeca \
              (fld_assembly_id) \
              VALUES (%d)" % _values[1]
    _inserted = app.DB.execute_query(_query,
                                     None,
                                     app.ProgCnx,
                                     commit=True)
    if not _inserted:
        app.debug_log.error("utilities.py:component_add - Failed to add new component to FMECA table.")
        pass

    return False


def set_part_model(category, subcategory):
    """
    This functions sets the COMPONENT part model based on the category
    and subcategory.

    Keyword Arguments:
    category    --
    subcategory --
    """

    if(category == 0 or subcategory == 0):  # No category or subcategory
        part = None

    elif(category == 1):                    # Capacitor
        if(subcategory == 1):
            from capacitors.fixed import CeramicGeneral
            part = CeramicGeneral()
        elif(subcategory == 2):
            from capacitors.fixed import CeramicChip
            part = CeramicChip()
        elif(subcategory == 3):
            from capacitors.electrolytic import AluminumDry
            part = AluminumDry()
        elif(subcategory == 4):
            from capacitors.electrolytic import Aluminum
            part = Aluminum()
        elif(subcategory == 5):
            from capacitors.electrolytic import TantalumNonSolid
            part = TantalumNonSolid()
        elif(subcategory == 6):
            from capacitors.electrolytic import TantalumSolid
            part = TantalumSolid()
        elif(subcategory == 7):
            from capacitors.fixed import PaperFeedthrough
            part = PaperFeedthrough()
        elif(subcategory == 8):
            from capacitors.fixed import Glass
            part = Glass()
        elif(subcategory == 9):
            from capacitors.fixed import MetallizedPaper
            part = MetallizedPaper()
        elif(subcategory == 10):
            from capacitors.fixed import Mica
            part = Mica()
        elif(subcategory == 11):
            from capacitors.fixed import MicaButton
            part = MicaButton()
        elif(subcategory == 12):
            from capacitors.fixed import PlasticFilm
            part = PlasticFilm()
        elif(subcategory == 13):
            from capacitors.fixed import PaperBypass
            part = PaperBypass()
        elif(subcategory == 14):
            from capacitors.fixed import Plastic
            part = Plastic()
        elif(subcategory == 15):
            from capacitors.fixed import SuperMetallizedPlastic
            part = SuperMetallizedPlastic()
        elif(subcategory == 16):
            from capacitors.variable import Gas
            part = Gas()
        elif(subcategory == 17):
            from capacitors.variable import AirTrimmer
            part = AirTrimmer()
        elif(subcategory == 18):
            from capacitors.variable import Ceramic
            part = Ceramic()
        elif(subcategory == 19):
            from capacitors.variable import Piston
            part = Piston()
    elif(category == 2):                    # Connection
        if(subcategory == 4):
            from connections.socket import ICSocket
            part = ICSocket()
        elif(subcategory == 5):
            from connections.multipin import Multipin
            part = Multipin()
        elif(subcategory == 6):
            from connections.pcb import PCBEdge
            part = PCBEdge()
        elif(subcategory == 7):
            from connections.solder import PTH
            part = PTH()
        else:
            from connections.solder import Solder
            part = Solder(subcategory)

    elif(category == 3):                    # Inductive Device
        if(subcategory == 1):
            from inductors.coil import Coil
            part = Coil()
        elif(subcategory == 2):
            from inductors.transformer import Audio
            part = Audio()
        elif(subcategory == 3):
            from inductors.transformer import Power
            part = Power()
        elif(subcategory == 4):
            from inductors.transformer import LowPowerPulse
            part = LowPowerPulse()
        elif(subcategory == 5):
            from inductors.transformer import RF
            part = RF()

    elif(category == 4):                    # Integrated circuit
        if(subcategory == 1):
            from integrated_circuits.gaas import GaAsDigital
            part = GaAsDigital()
        elif(subcategory == 2):
            from integrated_circuits.gaas import GaAsMMIC
            part = GaAsMMIC()
        elif(subcategory == 3):
            from integrated_circuits.linear import Linear
            part = Linear()
        elif(subcategory == 4):
            from integrated_circuits.logic import Logic
            part = Logic()
        elif(subcategory == 5):
            from integrated_circuits.memory import MemoryDRAM
            part = MemoryDRAM()
        elif(subcategory == 6):
            from integrated_circuits.memory import MemoryEEPROM
            part = MemoryEEPROM()
        elif(subcategory == 7):
            from integrated_circuits.memory import MemoryROM
            part = MemoryROM()
        elif(subcategory == 8):
            from integrated_circuits.memory import MemorySRAM
            part = MemorySRAM()
        elif(subcategory == 9):
            from integrated_circuits.microprocessor import Microprocessor
            part = Microprocessor()
        elif(subcategory == 10):
            from integrated_circuits.palpla import PALPLA
            part = PALPLA()
        elif(subcategory == 11):
            from integrated_circuits.vlsi import VLSI
            part = VLSI()

    elif(category == 5):              # Meter
        if(subcategory == 1):
            from meters.meter import ElapsedTime
            part = ElapsedTime()
        elif(subcategory == 2):
            from meters.meter import Panel
            part = Panel()

    elif(category == 6):              # Miscellaneous
        if(subcategory == 1):
            from miscellaneous.crystal import Crystal
            part = Crystal()
        elif(subcategory == 2):
            from miscellaneous.fuse import Fuse
            part = Fuse()
        elif(subcategory == 3):
            from miscellaneous.lamp import Lamp
            part = Lamp()

    elif(category == 7):              # Relay
        if(subcategory == 1):
            from relays.relay import Mechanical
            part = Mechanical()
        elif(subcategory == 2):
            from relays.relay import SolidState
            part = SolidState()

    elif(category == 8):              # Resistor
        if(subcategory == 1):
            from resistors.fixed import Composition
            part = Composition()
        elif(subcategory == 2):
            from resistors.fixed import Film
            part = Film()
        elif(subcategory == 3):
            from resistors.fixed import FilmNetwork
            part = FilmNetwork()
        elif(subcategory == 4):
            from resistors.fixed import FilmPower
            part = FilmPower()
        elif(subcategory == 5):
            from resistors.fixed import Wirewound
            part = Wirewound()
        elif(subcategory == 6):
            from resistors.fixed import WirewoundPower
            part = WirewoundPower()
        elif(subcategory == 7):
            from resistors.fixed import WirewoundPowerChassis
            part = WirewoundPowerChassis()
        elif(subcategory == 8):
            from resistors.thermistor import Thermistor
            part = Thermistor()
        elif(subcategory == 9):
            from resistors.variable import Composition
            part = Composition()
        elif(subcategory == 10):
            from resistors.variable import NonWirewound
            part = NonWirewound()
        elif(subcategory == 11):
            from resistors.variable import VarFilm
            part = VarFilm()
        elif(subcategory == 12):
            from resistors.variable import VarWirewound
            part = VarWirewound()
        elif(subcategory == 13):
            from resistors.variable import VarWirewoundPower
            part = VarWirewoundPower()
        elif(subcategory == 14):
            from resistors.variable import WirewoundPrecision
            part = WirewoundPrecision()
        elif(subcategory == 15):
            from resistors.variable import WirewoundSemiPrecision
            part = WirewoundSemiPrecision()

    elif(category == 9):              # Semiconductor
        if(subcategory == 1):
            from semiconductors.diode import HighFrequency
            part = HighFrequency()
        elif(subcategory == 2):
            from semiconductors.diode import LowFrequency
            part = LowFrequency()
        elif(subcategory == 3):
            from semiconductors.optoelectronics import Display
            part = Display()
        elif(subcategory == 4):
            from semiconductors.optoelectronics import Detector
            part = Detector()
        elif(subcategory == 5):
            from semiconductors.optoelectronics import LaserDiode
            part = LaserDiode()
        elif(subcategory == 6):
            from semiconductors.thyristor import Thyristor
            part = Thyristor()
        elif(subcategory == 7):
            from semiconductors.transistor import HFGaAsFET
            part = HFGaAsFET()
        elif(subcategory == 8):
            from semiconductors.transistor import HFHPBipolar
            part = HFHPBipolar()
        elif(subcategory == 9):
            from semiconductors.transistor import HFLNBipolar
            part = HFLNBipolar()
        elif(subcategory == 10):
            from semiconductors.transistor import HFSiFET
            part = HFSiFET()
        elif(subcategory == 11):
            from semiconductors.transistor import LFBipolar
            part = LFBipolar()
        elif(subcategory == 12):
            from semiconductors.transistor import LFSiFET
            part = LFSiFET()
        elif(subcategory == 13):
            from semiconductors.transistor import Unijunction
            part = Unijunction()

    elif(category == 10):             # Switching Device
        if(subcategory == 1):
            from switches.breaker import Breaker
            part = Breaker()
        elif(subcategory == 2):
            from switches.rotary import Rotary
            part = Rotary()
        elif(subcategory == 3):
            from switches.sensitive import Sensitive
            part = Sensitive()
        elif(subcategory == 4):
            from switches.thumbwheel import Thumbwheel
            part = Thumbwheel()
        elif(subcategory == 5):
            from switches.toggle import Toggle
            part = Toggle()

    return(part)


def calculate_max_text_width(text, font):
    """
    Function to calculate the maximum width of the text string that is using a
    particular font.

    Keyword Arguments:
    text -- the text string to calculate.
    font -- the font being used.
    """

    max_ = 0
    lines = text.split('\n')
    for line in lines:
        max_ = max(max_, font.width(line))

    return max_ + 50


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
        if(model.iter_has_child(chrow)):
            trickledown(model, chrow, index_, value_)

    return False


def options(widget, _app):
    """
    Function to launch the user options configuration assistant.

    Keyword Arguments:
    widget -- the pyGTK widget calling this function.
    _app   -- the RTK application.
    """

    opts = Options(_app)


def date_select(widget, entry):
    """
    Function to select a date from a calendar widget.

    Keyword Arguments:
    widget -- the pyGTK widget calling this function.
    entry  -- the gtk.Entry() widget to display the date.
    """

    from datetime import date, datetime

    dialog = _widg.make_dialog(_("Select Date"), _buttons_=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    calendar = gtk.Calendar()
    dialog.vbox.pack_start(calendar)
    dialog.vbox.show_all()

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        _date_ = calendar.get_date()
        _date_ = datetime(_date_[0], _date_[1] + 1, _date_[2]).date().strftime("%Y-%m-%d")
    else:
        _date_ = "1970-01-01"

    dialog.destroy()

    entry.set_text(_date_)


def set_cursor(_app_, _cursor_):
    """
    Function to set the cursor for a gtk.gdk.Window()

    Keyword Araguments:
    _app_    -- the running instance of the RTK application.
    _cursor_ -- the gtk.gdk.Cursor() to set.  Only handles one of the following:
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

    _app_.winTree.window.set_cursor(gtk.gdk.Cursor(_cursor_))
    _app_.winParts.window.set_cursor(gtk.gdk.Cursor(_cursor_))
    _app_.winWorkBook.window.set_cursor(gtk.gdk.Cursor(_cursor_))

    gtk.gdk.flush()

    return False

def long_call(_app_):
    """
    Function for restoring the cursor to normal after a long call.

    Keyword Arguments:
    _app_ -- the running instance of the RTK application.
    """

    _app_.winTree.window.set_cursor(None)
    _app_.winParts.window.set_cursor(None)
    _app_.winWorkBook.window.set_cursor(None)


class Options:

    _edit_tree_labels = [_(u"Default\nTitle"), _(u"User\nTitle"),
                         _(u"Column\nPosition"), _(u"Can\nEdit?"),
                         _(u"Is\nVisible?")]

    def __init__(self, _app):
        """
        Allows a user to set site-wide options.

        Keyword Arguments:
        app    -- the RTK application object.
        """

        import pango

        self.winOptions = gtk.Window()
        self.winOptions.set_title(_("RTK - Options"))

        notebook = gtk.Notebook()

        # ----- ----- ----- -- RTK module options - ----- ----- ----- #
        if(_conf.RTK_PROG_INFO[2] != ''):
            fixed = gtk.Fixed()

            self.chkRevisions = _widg.make_check_button(_("Revisions"))
            self.chkFunctions = _widg.make_check_button(_("Functions"))
            self.chkRequirements = _widg.make_check_button(_("Requirements"))
            self.chkSoftware = _widg.make_check_button(_("Software Reliability"))
            self.chkValidation = _widg.make_check_button(_("Validation Tasks"))
            self.chkRG = _widg.make_check_button(_("Reliability Growth"))
            self.chkIncidents = _widg.make_check_button(_("Field Incidents"))

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

        label = gtk.Label(_("Edit Lists"))
        label.set_tooltip_text(_("Allows editting of lists used in RTK."))
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
        vbox = gtk.VBox()

        self.tvwEditTree = gtk.TreeView()
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        self.tvwEditTree.set_model(model)

        for i in range(5):

            if(i == 0):
                cell = gtk.CellRendererText()
                cell.set_property('background', 'light gray')
                cell.set_property('editable', 0)
                cell.set_property('foreground', '#000000')
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
            elif(i > 0 and i < 3):
                cell = gtk.CellRendererText()
                cell.set_property('background', '#FFFFFF')
                cell.set_property('editable', 1)
                cell.set_property('foreground', '#000000')
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD)
                cell.connect('edited', self._cell_edit, i, model)
            elif(i > 4):
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
            label.set_markup("<span weight='bold'>" +
                             self._edit_tree_labels[i] + "</span>")
            label.show_all()

            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_alignment(0.5)
            column.pack_start(cell, True)
            if(i < 3):
                column.set_attributes(cell, text=i)
            elif(i > 4):
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

    def _edit_tree(self, button):
        """
        Method to edit gtk.TreeView layouts
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

    def _cell_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        type = gobject.type_name(model.get_column_type(position))

        if(type == 'gchararray'):
            model[path][position] = str(new_text)
        elif(type == 'gint'):
            model[path][position] = int(new_text)
        elif(type == 'gfloat'):
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

    def _save_tree_layout(self, button):
        """
        Method for saving the gtk.TreeView layout file.

        Keyword Arguments:
        button --
        """

        import os
        from lxml import etree
        from shutil import copyfile

        (_name, _fmt_idx) = self._get_format_info()

# Get the format file for the gtk.TreeView to be edited.
        _format_file = _conf.RTK_FORMAT_FILE[_fmt_idx]
        _basename = os.path.basename(_format_file)

# Make a copy of the original format file.
        copyfile(_format_file, _format_file + '.bak')

# Open the format file for writing.
        f = open(_format_file, 'w')

# Create the new format file.
        f.write("<!--\n")
        f.write("-*- coding: utf-8 -*-\n\n")
        f.write("%s is part of the RTK Project\n\n" % _basename)
        f.write('Copyright 2011-2013 Andrew "Weibullguy" Rowland <andrew DOT rowland AT reliaqual DOT com>\n\n')
        f.write("All rights reserved.-->\n\n")
        f.write("<!-- This file contains information used by the RTK application to draw\n")
        f.write("various widgets.  These values can be changed by the user to personalize\n")
        f.write("their experience. -->\n\n")

        f.write("<root>\n")
        f.write('\t<tree name="%s">\n' % _name)

        model = self.tvwEditTree.get_model()
        row = model.get_iter_first()
        while row is not None:
            f.write("\t\t<column>\n")
            f.write("\t\t\t<defaulttitle>%s</defaulttitle>\n" % model.get_value(row, 0))
            f.write("\t\t\t<usertitle>%s</usertitle>\n"% model.get_value(row, 1))
            f.write("\t\t\t<datatype>%s</datatype>\n" % model.get_value(row, 5))
            f.write('\t\t\t<position>%d</position>\n' % model.get_value(row, 2))
            f.write("\t\t\t<widget>%s</widget>\n" % model.get_value(row, 6))
            f.write("\t\t\t<editable>%d</editable>\n" % model.get_value(row, 3))
            f.write("\t\t\t<visible>%d</visible>\n" % model.get_value(row, 4))
            f.write("\t\t</column>\n")

            row = model.iter_next(row)

        f.write("\t</tree>\n")
        f.write("</root>")
        f.close()

        self.winOptions.destroy()

        return False

    def _get_format_info(self):
        """
        Method to retrieve the name and index of the selected format file.
        """

        if(self.rdoRevision.get_active()):
            _name = 'Revision'
            _fmt_idx = 0
        elif(self.rdoFunction.get_active()):
            _name = 'Function'
            _fmt_idx = 1
        elif(self.rdoRequirement.get_active()):
            _name = 'Requirement'
            _fmt_idx = 2
        elif(self.rdoHardware.get_active()):
            _name = 'Hardware'
            _fmt_idx = 3
        elif(self.rdoSoftware.get_active()):
            _name = 'Software'
            _fmt_idx = 15
        elif(self.rdoValidation.get_active()):
            _name = 'Validation'
            _fmt_idx = 4
        elif(self.rdoTesting.get_active()):
            _name = 'Testing'
            _fmt_idx = 11
        elif(self.rdoIncident.get_active()):
            _name = 'Incidents'
            _fmt_idx = 14
        elif(self.rdoSurvival.get_active()):
            _name = 'Dataset'
            _fmt_idx = 16
        elif(self.rdoPart.get_active()):
            _name = 'Parts'
            _fmt_idx = 7
        elif(self.rdoRiskAnalysis.get_active()):
            _name = 'Risk'
            _fmt_idx = 17
        elif(self.rdoSimilarItem.get_active()):
            _name = 'SIA'
            _fmt_idx = 8
        elif(self.rdoFMECA.get_active()):
            _name = 'FMECA'
            _fmt_idx = 9

        return(_name, _fmt_idx)

    def save_options(self, button):

        self.winOptions.destroy()

        return False

    def edit_lists(self, button):

        if(self.rdoMeasurement.get_active()):
            assistant = _widg.Assistant()
