# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Dialog.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module in other modules that
create, populate, destroy, or interact with pyGTK widgets in the RTK
application.  This module is specific to RTK dialog widgets.
"""

import os

from datetime import datetime

# Import the rtk.Widget base class.
from .Widget import _, gtk                          # pylint: disable=E0401


class RTKDialog(gtk.Dialog):
    """
    This is the RTK Dialog class.
    """

    def __init__(self, dlgtitle, dlgparent=None,
                 dlgflags=(gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT),
                 dlgbuttons=(gtk.STOCK_OK, gtk.RESPONSE_OK,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)):
        """
        Method to create a RTK Dialog widget.

        :param str dlgtitle: the title text for the gtk.Dialog().
        :keyword gtk.Window dlgparent: the parent window to associate the
                                       gtk.Dialog() with.
        :keyword tuple dlgflags: the flags that control the operation of the
                                 gtk.Dialog().  Defaults to gtk.DIALOG_MODAL
                                 and gtk.DIALOG_DESTROY_WITH_PARENT.
        :keyword tuple dlgbuttons: the buttons to display and their response
                                   values.  Defaults to:
                                   gtk.STOCK_OK <==> gtk.RESPONSE_ACCEPT
                                   gtk.STOCK_CANCEL <==> gtk.RESPONSE_REJECT
        :return: _dialog
        :rtype: gtk.Dialog
        """

        gtk.Dialog.__init__(self, title=dlgtitle, parent=dlgparent,
                            flags=dlgflags, buttons=dlgbuttons)

        self.set_has_separator(True)

    def do_run(self):
        """
        Method to run the RTK Message Dialog.
        """

        return self.run()

    def do_destroy(self):
        """
        Method to destroy the RTK Message Dialog.
        """

        self.destroy()


class RTKMessageDialog(gtk.MessageDialog):
    """
    This is the RTK Message Dialog class.  It used for RTK error, warning, and
    information messages.
    """

    def __init__(self, prompt, icon, criticality, parent=None):
        """
        Method to initialize runtime error, warning, and information dialogs.

        :param str prompt: the prompt to display in the dialog.
        :param str icon: the absolute path to the icon to display on the
                         dialog.
        :param str criticality: the criticality level of the dialog.
                                Criticality is one of:

                                * 'error'
                                * 'warning'
                                * 'information'

        :keyword gtk.Window _parent: the parent gtk.Window(), if any, for the
                                     dialog.
        """

        _image = gtk.Image()
        _image.set_from_file(icon)

        if criticality == 'error':
            # Set the prompt to bold text with a hyperlink to the RTK bugs
            # e-mail address.
            _hyper = "<a href='mailto:bugs@reliaqual.com?subject=RTK BUG " \
                     "REPORT: <ADD SHORT PROBLEM DESCRIPTION>&amp;" \
                     "body=RTK MODULE:%0d%0a%0d%0a" \
                     "RTK VERSION:%20%0d%0a%0d%0a" \
                     "YOUR HARDWARE:%20%0d%0a%0d%0a" \
                     "YOUR OS:%20%0d%0a%0d%0a" \
                     "DETAILED PROBLEM DESCRIPTION:%20%0d%0a'>"
            prompt = '<b>' \
                     + prompt \
                     + _(u"  Check the error log for additional information "
                         u"(if any).  Please e-mail <span foreground='blue' "
                         u"underline='single'>") \
                     + _hyper \
                     + _(u"bugs@reliaqual.com</a></span> with a detailed "
                         u"description of the problem, the workflow you are "
                         u"using and the error log attached if the problem "
                         u"persists.</b>")
            _criticality = gtk.MESSAGE_ERROR
            _buttons = gtk.BUTTONS_OK
        elif criticality == 'warning':
            _criticality = gtk.MESSAGE_WARNING
            _buttons = gtk.BUTTONS_OK
        elif criticality == 'information':
            _criticality = gtk.MESSAGE_INFO
            _buttons = gtk.BUTTONS_OK
        elif criticality == 'question':
            _criticality = gtk.MESSAGE_QUESTION
            _buttons = gtk.BUTTONS_YES_NO

        gtk.MessageDialog.__init__(self, parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT,
                                   _criticality, _buttons)

        self.set_markup(prompt)
        self.set_image(_image)
        self.show_all()

    def do_run(self):
        """
        Method to run the RTK Message Dialog.
        """

        return self.run()

    def do_destroy(self):
        """
        Method to destroy the RTK Message Dialog.
        """

        self.destroy()


class RTKFileChooser(gtk.FileChooserDialog):
    """
    This is the RTK File Chooser Dialog class.
    """

    def __init__(self, title, cwd):
        """
        Method to initialize an instance of the RTKFileChooser dialog.

        :param str cwd: the absolute path to the file to open.
        """

        gtk.FileChooserDialog.__init__(self, title, None,
                                       gtk.DIALOG_MODAL |
                                       gtk.DIALOG_DESTROY_WITH_PARENT,
                                       (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                                        gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        self.set_current_folder(cwd)

        # Set some filters to select all files or only some text files.
        _filter = gtk.FileFilter()
        _filter.set_name(u"All files")
        _filter.add_pattern("*")
        self.add_filter(_filter)

        _filter = gtk.FileFilter()
        _filter.set_name("Text Files (csv, txt)")
        _filter.add_mime_type("text/csv")
        _filter.add_mime_type("text/txt")
        _filter.add_mime_type("application/xls")
        _filter.add_pattern("*.csv")
        _filter.add_pattern("*.txt")
        _filter.add_pattern("*.xls")
        self.add_filter(_filter)

    def do_run(self):
        """
        Method to run the RTKFileChooser dialog.
        """

        if self.run() == gtk.RESPONSE_ACCEPT:
            _filename = self.get_filename()
            __, _extension = os.path.splitext(_filename)

        if _extension == '.csv' or _extension == '.txt':
            self._do_read_text_file(_filename)

        return False

    def _do_read_text_file(self, filename):
        """
        Method to read the contents of a text file.

        :param str filename: the file to be read.
        :return:
        :rtype:
        """

        # Run the dialog and write the file.
        _headers = []
        _contents = []

        __, _extension = os.path.splitext(filename)
        _file = open(filename, 'r')
        if _extension == '.csv':
            _delimiter = ','
        else:
            _delimiter = '\t'

        for _line in _file:
            _contents.append([_line.rstrip('\n')])

        _headers = str(_contents[0][0]).rsplit(_delimiter)
        for i in range(len(_contents) - 1):
            _contents[i] = str(_contents[i + 1][0]).rsplit(_delimiter)

        self.destroy()

        return _headers, _contents

    def do_destroy(self):
        """
        Method to destroy the RTKFileChooser dialog.
        """

        self.destroy()


class RTKDateSelect(gtk.Dialog):
    """
    This is the RTK Date Select Dialog class.
    """

    def __init__(self, entry=None):
        """
        Method to initialize an instance of the RTKDateSelect class.

        :param entry: the gtk.Entry() in which to place the date, if any.
        :type entry: :py:class:`gtk.Entry`
        """

        gtk.Dialog.__init__(self, _(u"Select Date"),
                            dlgbuttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        self._entry = entry
        self._calendar = gtk.Calendar()
        self.vbox.pack_start(self._calendar)    # pylint: disable=E1101
        self.vbox.show_all()                    # pylint: disable=E1101

    def do_run(self):
        """
        Method to run the RTKDateSelect dialog.
        """

        if self.run() == gtk.RESPONSE_ACCEPT:
            _date = self._calendar.get_date()
            _date = datetime(_date[0], _date[1] + 1,
                             _date[2]).date().strftime("%Y-%m-%d")
        else:
            _date = "1970-01-01"

        if self._entry is not None:
            self._entry.set_text(_date)
            self._entry.grab_focus()

        return _date

    def do_destroy(self):
        """
        Method to destroy the RTKDateSelect dialog.
        """

        self.destroy()
