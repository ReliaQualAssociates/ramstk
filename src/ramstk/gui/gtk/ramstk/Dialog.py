# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Dialog.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Dialog Module."""

import os

from datetime import datetime

# Import the ramstk.Widget base class.
from .Widget import _, gtk  # pylint: disable=E0401


class RAMSTKDialog(gtk.Dialog):
    """This is the RAMSTK Dialog class."""

    def __init__(self, dlgtitle, **kwargs):
        r"""
        Initialize a RAMSTK Dialog widget.

        :param str dlgtitle: the title text for the gtk.Dialog().
        :param \**kwargs: See below

        :Keyword Arguments:
            * *dlgparent* (tuple) -- the parent window to associate the
                                     gtk.Dialog() with.
            * *dlgflags* (tuple) -- the flags that control the operation of the
                                    gtk.Dialog().
                                    Default is gtk.DIALOG_MODAL
                                    and gtk.DIALOG_DESTROY_WITH_PARENT.
            * *dlgbuttons* (tuple) -- the buttons to display and their response
                                      values.
                                      Default is
                                      gtk.STOCK_OK <==> gtk.RESPONSE_ACCEPT
                                      gtk.STOCK_CANCEL <==> gtk.RESPONSE_REJECT
        :return: _dialog
        :rtype: gtk.Dialog
        """
        try:
            _dlgflags = kwargs['dlgflags']
        except KeyError:
            _dlgflags = (gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        try:
            _dlgbuttons = kwargs['dlgbuttons']
        except KeyError:
            _dlgbuttons = (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL,
                           gtk.RESPONSE_CANCEL)
        try:
            _dlgparent = kwargs['dlgparent']
        except KeyError:
            _dlgparent = None

        gtk.Dialog.__init__(
            self,
            title=dlgtitle,
            parent=_dlgparent,
            flags=_dlgflags,
            buttons=_dlgbuttons)

        self.set_has_separator(True)

    def do_run(self):
        """Run the RAMSTK Message Dialog."""
        return self.run()

    def do_destroy(self):
        """Destroy the RAMSTK Message Dialog."""
        self.destroy()


class RAMSTKMessageDialog(gtk.MessageDialog):
    """
    This is the RAMSTK Message Dialog class.

    It used for RAMSTK error, warning, and information messages.
    """

    def __init__(self, prompt, icon, criticality, parent=None):
        """
        Initialize runtime error, warning, and information dialogs.

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
            # Set the prompt to bold text with a hyperlink to the RAMSTK bugs
            # e-mail address.
            _hyper = "<a href='mailto:bugs@reliaqual.com?subject=RAMSTK BUG " \
                     "REPORT: <ADD SHORT PROBLEM DESCRIPTION>&amp;" \
                     "body=RAMSTK MODULE:%0d%0a%0d%0a" \
                     "RAMSTK VERSION:%20%0d%0a%0d%0a" \
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
        """Run the RAMSTK Message Dialog."""
        return self.run()

    def do_destroy(self):
        """Destroy the RAMSTK Message Dialog."""
        self.destroy()


class RAMSTKDateSelect(gtk.Dialog):
    """The RAMSTK Date Selection Dialog."""

    def __init__(self):
        """Initialize an instance of the RAMSTKDateSelect class."""
        gtk.Dialog.__init__(
            self,
            _(u"Select Date"),
            buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        self._calendar = gtk.Calendar()
        self.vbox.pack_start(self._calendar)  # pylint: disable=E1101
        self.vbox.show_all()  # pylint: disable=E1101

    def do_run(self):
        """Run the RAMSTKDateSelect dialog."""
        if self.run() == gtk.RESPONSE_ACCEPT:
            _date = self._calendar.get_date()
            _date = datetime(_date[0], _date[1] + 1,
                             _date[2]).date().strftime("%Y-%m-%d")
        else:
            _date = "1970-01-01"

        return _date

    def do_destroy(self):
        """Destroy the RAMSTKDateSelect dialog."""
        self.destroy()


class RAMSTKFileChooser(gtk.FileChooserDialog):
    """This is the RAMSTK File Chooser Dialog class."""

    def __init__(self, title, cwd):
        """
        Initialize an instance of the RAMSTKFileChooser dialog.

        :param str title: the title of the dialog.
        :param str cwd: the absolute path to the file to open.
        """
        gtk.FileChooserDialog.__init__(
            self, title, None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL,
             gtk.RESPONSE_REJECT))

        self.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        self.set_current_folder(cwd)

        _filter = gtk.FileFilter()
        _filter.set_name(_(u"Excel Files"))
        _filter.add_pattern('*.xls')
        _filter.add_pattern('*xlsm')
        _filter.add_pattern('*xlsx')
        self.add_filter(_filter)
        _filter = gtk.FileFilter()
        _filter.set_name(_(u"Delimited Text Files"))
        _filter.add_pattern('*.csv')
        _filter.add_pattern('*.txt')
        self.add_filter(_filter)
        _filter = gtk.FileFilter()
        _filter.set_name(u"All files")
        _filter.add_pattern("*")
        self.add_filter(_filter)

    def do_run(self):
        """
        Run the RAMSTKFileChooser dialog.

        :return: (_filename, _extension); the file name and file extension of
                 the selected file.
        :rtype: (str, str) or (None, None)
        """
        _filename = None
        _extension = None

        if self.run() == gtk.RESPONSE_ACCEPT:
            _filename = self.get_filename()
            __, _extension = os.path.splitext(_filename)
        elif self.run() == gtk.RESPONSE_REJECT:
            self.do_destroy()

        return (_filename, _extension)

    def do_destroy(self):
        """Destroy the RAMSTKFileChooser dialog."""
        self.destroy()
