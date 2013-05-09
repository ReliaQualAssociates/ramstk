#!/usr/bin/env python
""" utilities contains utility functions for interacting with the RelKit
    application.  Import this module as _util in other modules that need to
    interact with the RelKit application.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       utilities.py is part of The RelKit Project
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

# Import other RelKit modules.
import configuration as _conf
import login as _login
import widgets as _widg


def read_configuration():

    """
    This method reads the site and user configuration files to establish
    settings for The RelKit application.
    """

    # Get a config instance for the site configuration file.
    conf = _conf.RelKitConf('site')

    _conf.COM_BACKEND = conf.read_configuration().get('Backend', 'type')

    _conf.RELIAFREE_COM_INFO.append(conf.read_configuration().get('Backend', 'host'))
    _conf.RELIAFREE_COM_INFO.append(conf.read_configuration().get('Backend', 'socket'))
    _conf.RELIAFREE_COM_INFO.append(conf.read_configuration().get('Backend', 'database'))
    _conf.RELIAFREE_COM_INFO.append(conf.read_configuration().get('Backend', 'user'))
    _conf.RELIAFREE_COM_INFO.append(conf.read_configuration().get('Backend', 'password'))

    # Get a config instance for the user configuration file.
    conf = _conf.RelKitConf('user')
    _conf.BACKEND = conf.read_configuration().get('Backend', 'type')
    _conf.FRMULT = float(conf.read_configuration().get('General', 'frmultiplier'))
    _conf.PLACES = conf.read_configuration().get('General', 'decimal')
    _conf.TABPOS[0] = conf.read_configuration().get('General', 'treetabpos')
    _conf.TABPOS[1] = conf.read_configuration().get('General', 'listtabpos')
    _conf.TABPOS[2] = conf.read_configuration().get('General', 'booktabpos')

    _conf.RELIAFREE_PROG_INFO.append(conf.read_configuration().get('Backend', 'host'))
    _conf.RELIAFREE_PROG_INFO.append(conf.read_configuration().get('Backend', 'socket'))
    _conf.RELIAFREE_PROG_INFO.append(conf.read_configuration().get('Backend', 'database'))
    _conf.RELIAFREE_PROG_INFO.append(conf.read_configuration().get('Backend', 'user'))
    _conf.RELIAFREE_PROG_INFO.append(conf.read_configuration().get('Backend', 'password'))

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
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'functionformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'requirementformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'hardwareformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'validationformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'rgformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'fracaformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'partformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'siaformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'fmecaformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'modeformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'testformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'mechanismformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'rgincidentformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'incidentformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'softwareformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'datasetformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)
    formatfile = conf.read_configuration().get('Files', 'riskformat')
    _conf.RELIAFREE_FORMAT_FILE.append(conf.conf_dir + formatfile)

    # Get color information.
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'revisionbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'revisionfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'functionbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'functionfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'requirementbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'requirementfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'assemblybg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'assemblyfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'validationbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'validationfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'rgbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'rgfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'fracabg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'fracafg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'partbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'partfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'overstressbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'overstressfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'taggedbg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'taggedfg'))
    _conf.RELIAFREE_COLORS.append(conf.read_configuration().get('Colors', 'nofrmodelfg'))

    return(icondir, datadir, logdir)

def create_logger(log_name, log_level, log_file, to_tty=False):

    """ This function creates a logger instance.

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

    """ This function parses the XML configuration file passed as a parameter.

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
    """ Converts string representations of TRUE/FALSE to an integer value for
        use in the database.

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
    """ Converts date strings to oridinal dates for use in the database.

        Keyword Arguments:
        date -- the date string to convert.
    """

    from datetime import datetime

    try:
        results = datetime.strptime(str(date), '%m/%d/%y').toordinal()
    except ValueError:
        results = datetime.strptime('01/01/70', '%m/%d/%y').toordinal()

    return(results)

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

    """ Checks if a file exists.

        Keyword Arguments:
        file -- a string representing the filepath to check for.

    """

    from os import path

    if path.isfile(_file_):
        return True
    else:
        return False

def create_project(widget, app):
    """ Creates a new RelKit Project.

        Keyword Arguments:
        widget -- the widget that called this function.
        app    -- the RelKit application.
    """

    if(_conf.BACKEND == 'mysql'):

        login = _login.Login(_(u"Create a RelKit Program Database"))
        if(login.answer != gtk.RESPONSE_ACCEPT):
            return True

        dialog = _widg.make_dialog(_(u"RelKit - New Program"))

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

        _conf.RELIAFREE_PROG_INFO[2] = None
        query = "CREATE DATABASE IF NOT EXISTS %s"
        cnx = app.DB.get_connection(_conf.RELIAFREE_PROG_INFO)
        results = app.DB.execute_query(query,
                                       new_program,
                                       cnx,
                                       commit=True)
        cnx.close()
        if not results:
            return True

        _conf.RELIAFREE_PROG_INFO[2] = new_program
        cnx = app.DB.get_connection(_conf.RELIAFREE_PROG_INFO)

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

        dialog = gtk.FileChooserDialog(title=_(u"Create a RelKit Program Database"),
                                       action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                       buttons=(gtk.STOCK_NEW, gtk.RESPONSE_ACCEPT,
                                                gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            new_program = dialog.get_filename()
            new_program = new_program + '.rfb'

            _conf.RELIAFREE_PROG_INFO[2] = new_program
            cnx = app.DB.get_connection(_conf.RELIAFREE_PROG_INFO[2])

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
    Shows the RelKit databases available on the selected server and allows the
    user to select the one he/she wishes to use.

    Keyword Arguments:
    widget -- the widget that called this function.
    app    -- the RelKit application.
    dlg    -- whether or not to display a file chooser dialog.  0=No, 1=Yes.
    """

    from time import sleep

    if(_conf.BACKEND == 'mysql'):

        login = _login.Login(_(u"RelKit Program Database Login"))

        if(login.answer != gtk.RESPONSE_ACCEPT):
            return True

        query = "SHOW DATABASES"
        cnx = app.DB.get_connection(_conf.RELIAFREE_PROG_INFO)
        results = app.DB.execute_query(query,
                                       None,
                                       cnx)

        dialog = _widg.make_dialog(_(u"RelKit: Open Program"))

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
               results[i][0] != 'reliafreecom' and
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
            _conf.RELIAFREE_PROG_INFO[2] = model.get_value(row, 0)
            dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            app.load_system()

        dialog.destroy()

        cnx.close()

    elif(_conf.BACKEND == 'sqlite3'):

        if(dlg == 1):
            dialog = gtk.FileChooserDialog(title=_(u"RelKit - Open Program"),
                                           buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                                    gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

            # Set some filters to select all files or only some text files.
            filter = gtk.FileFilter()
            filter.set_name(_(u"RelKit Project Files"))
            #filter.add_mime_type("text/txt")
            filter.add_pattern("*.rfb")
            dialog.add_filter(filter)

            filter = gtk.FileFilter()
            filter.set_name(_(u"All files"))
            filter.add_pattern("*")
            dialog.add_filter(filter)

            response = dialog.run()

            if(response == gtk.RESPONSE_ACCEPT):
                _conf.RELIAFREE_PROG_INFO[2] = dialog.get_filename()
                dialog.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
                app.load_system()

            dialog.destroy()

        else:
            _conf.RELIAFREE_PROG_INFO[2] = filename
            app.load_system()

    return False

def save_project(widget, _app):
    """
    Saves the RelKit information to the project's MySQL database.

    Keyword Arguments:
    widget -- the widget that is calling this function.
    _app   -- the RelKit application.
    """

    if not _app.LOADED:
        return True

    _app.winTree.statusbar.push(2, "Saving")

    _app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    _app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
    _app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))

    _app.REVISION.revision_save()
    _app.FUNCTION.function_save(None)
    _app.REQUIREMENT.requirement_save()
    _app.HARDWARE.hardware_save()
    _app.SOFTWARE.software_save()
    _app.winParts.save_component()

    # Update the next ID for each type of object.
    values = (_conf.RELIAFREE_PREFIX[1], _conf.RELIAFREE_PREFIX[3],
              _conf.RELIAFREE_PREFIX[5], _conf.RELIAFREE_PREFIX[7],
              _conf.RELIAFREE_PREFIX[9], _conf.RELIAFREE_PREFIX[11],
              _conf.RELIAFREE_PREFIX[13], _conf.RELIAFREE_PREFIX[15],
              _conf.RELIAFREE_PREFIX[17], 1)

    if(_conf.BACKEND == 'mysql'):
        query = "UPDATE tbl_program_info \
                 SET fld_revision_next_id=%d, fld_function_next_id=%d, \
                     fld_assembly_next_id=%d, fld_part_next_id=%d, \
                     fld_fmeca_next_id=%d, fld_mode_next_id=%d, \
                     fld_effect_next_id=%d, fld_cause_next_id=%d, \
                     fld_software_next_id=%d \
                 WHERE fld_program_id=%d"
    elif(_conf.BACKEND == 'sqlite3'):
        query = "UPDATE tbl_program_info \
                 SET fld_revision_next_id=?, fld_function_next_id=?, \
                     fld_assembly_next_id=?, fld_part_next_id=?, \
                     fld_fmeca_next_id=?, fld_mode_next_id=?, \
                     fld_effect_next_id=?, fld_cause_next_id=?, \
                     fld_software_next_id=? \
                 WHERE fld_program_id=?"

    results = _app.DB.execute_query(query,
                                    values,
                                    _app.ProgCnx,
                                    commit=True)

    conf = _conf.RelKitConf('user')
    #conf.write_configuration()

    _app.winTree.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
    _app.winWorkBook.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
    _app.winParts.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))

    _app.winTree.statusbar.pop(2)

    return False

def delete_project(widget, _app):
    """
    Deletes an existing RelKit Project.

    Keyword Arguments:
    widget -- the widget that called this function.
    _app   -- the RelKit application.
    """

    if(_conf.BACKEND == 'mysql'):

        query = "SHOW DATABASES"
        cnx = _app.DB.get_connection(_conf.RELIAFREE_PROG_INFO)
        results = _app.DB.execute_query(query,
                                        None,
                                        cnx)

        dialog = _widg.make_dialog(_("RelKit - Delete Program"))

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

        dialog = gtk.FileChooserDialog(_("RelKit - Delete Program"),
                                       None,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        response = dialog.run()
        if(response == gtk.RESPONSE_ACCEPT):
            project = dialog.get_filename()
        else:
            dialog.destroy()

        if(confirm_action(_("Really delete %s?") % project), 'question'):
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
    app    -- the RelKit application object.
    """

    # TODO: Write function to import project information from various other formats; Excel, CSV, other delimited files.
    dialog = gtk.FileChooserDialog(_("Select Project to Import"), None,
                                   gtk.FILE_CHOOSER_ACTION_OPEN,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        print "Importing project."

    dialog.destroy()

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

    dialog = _widg.make_dialog(_("RelKit Error"), _buttons_=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    hbox = gtk.HBox()

    file_image = _conf.ICON_DIR + '32x32/' + _image_ + '.png'
    image = gtk.Image()
    image.set_from_file(file_image)
    hbox.pack_start(image)

    label = _widg.make_label(_prompt_, width=400, height=200)
    hbox.pack_end(label)
    dialog.vbox.pack_start(hbox)
    hbox.show_all()

    dialog.run()

    dialog.destroy()

    return False

def add_items(_class_):
    """
    Adds one or more items to a treeview hierarchy.

    Keyword Arguments:
    _class_ -- the type of item to add (i.e., function, assembly,
               component).
    """

    _title_ = _("RelKit - Add %s") % _class_

    dialog = _widg.make_dialog(_title_)

    fixed = gtk.Fixed()
    fixed.set_size_request(400, 60)

    label = _widg.make_label(_("Add how many %s?") % _class_, 150, 75)
    txtQuantity = _widg.make_entry()
    txtQuantity.set_text("1")

    fixed.put(label, 5, 10)
    fixed.put(txtQuantity, 160, 10)
    fixed.show_all()

    dialog.vbox.pack_start(fixed)

    response = dialog.run()

    if(response == gtk.RESPONSE_ACCEPT):
        numitems = int(txtQuantity.get_text())
    else:
        numitems = 0

    dialog.destroy()

    return(numitems)

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
    app    -- the RelKit application object.
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
    _app   -- the RelKit application.
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


class Options:

    def __init__(self, _app):
        """
        Allows a user to set site-wide options.

        Keyword Arguments:
        app    -- the RelKit application object.
        """

        self.winOptions = gtk.Window()
        self.winOptions.set_title(_("RelKit - Options"))

        notebook = gtk.Notebook()

        # ----- ----- ----- -- RelKit module options - ----- ----- ----- #
        if(_conf.RELIAFREE_PROG_INFO[2] != ''):
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
                            fld_fmeca_active, fld_maintainability_active, \
                            fld_rcm_active, fld_rbd_active, fld_fta_active, \
                            fld_fraca_active, fld_software_active \
                     FROM tbl_program_info"
            results = _app.DB.execute_query(query,
                                            None,
                                            _app.ProgCnx,
                                            commit=False)

            self.chkRevisions.set_active(results[0][0])
            self.chkFunctions.set_active(results[0][1])
            self.chkRequirements.set_active(results[0][2])
            self.chkSoftware.set_active(results[0][3])
            self.chkValidation.set_active(results[0][4])
            self.chkRG.set_active(results[0][5])
            self.chkIncidents.set_active(results[0][6])

            label = gtk.Label(_("RelKit Modules"))
            label.set_tooltip_text(_("Select active RelKit modules."))
            notebook.insert_page(fixed, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- - Create list edit options - ----- ----- ----- #
        fixed = gtk.Fixed()

        self.rdoMeasurement = gtk.RadioButton(group=None, label=_("Edit measurement units"))
        self.rdoRequirementTypes = gtk.RadioButton(group=self.rdoMeasurement, label=_("Edit requirement types"))
        self.rdoRiskCategory = gtk.RadioButton(group=self.rdoMeasurement, label=_("Edit risk categories"))
        self.rdoVandVTasks = gtk.RadioButton(group=self.rdoMeasurement, label=_("Edit V&V activity types"))
        self.rdoUsers = gtk.RadioButton(group=self.rdoMeasurement, label=_("Edit user list"))

        self.btnListEdit = gtk.Button(stock=gtk.STOCK_EDIT)
        self.btnListEdit.connect('clicked', self.edit_lists)

        fixed.put(self.rdoMeasurement, 5, 5)
        fixed.put(self.rdoRequirementTypes, 5, 35)
        fixed.put(self.rdoRiskCategory, 5, 65)
        fixed.put(self.rdoVandVTasks, 5, 95)
        fixed.put(self.rdoUsers, 5, 125)
        fixed.put(self.btnListEdit, 5, 205)

        label = gtk.Label(_("Edit Lists"))
        label.set_tooltip_text(_("Allows editting of lists used in RelKit."))
        notebook.insert_page(fixed, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        # ----- ----- ----- - Create tree edit options - ----- ----- ----- #
        fixed = gtk.Fixed()

        self.rdoRevision = gtk.RadioButton(group=None, label=_("Edit Revision tree layout"))
        self.rdoFunction = gtk.RadioButton(group=self.rdoRevision, label=_("Edit Function tree layout"))
        self.rdoRequirement = gtk.RadioButton(group=self.rdoRevision, label=_("Edit Requirement tree layout"))
        self.rdoHardware = gtk.RadioButton(group=self.rdoRevision, label=_("Edit Hardware tree layout"))
        self.rdoValidation = gtk.RadioButton(group=self.rdoRevision, label=_("Edit V&V tree layout"))

        self.btnTreeEdit = gtk.Button(stock=gtk.STOCK_EDIT)

        fixed.put(self.rdoRevision, 5, 5)
        fixed.put(self.rdoFunction, 5, 35)
        fixed.put(self.rdoRequirement, 5, 70)
        fixed.put(self.rdoHardware, 5, 105)
        fixed.put(self.rdoValidation, 5, 135)
        fixed.put(self.btnTreeEdit, 5, 205)

        label = gtk.Label(_("Edit Tree Layouts"))
        label.set_tooltip_text(_("Allows editting of tree layouts used in RelKit."))
        notebook.insert_page(fixed, tab_label=label, position=-1)
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #

        self.winOptions.add(notebook)
        self.winOptions.show_all()

    def save_options(self, button):

        self.winOptions.destroy()

        return False

    def edit_lists(self, button):

        if(self.rdoMeasurement.get_active()):
            assistant = _widg.Assistant()
