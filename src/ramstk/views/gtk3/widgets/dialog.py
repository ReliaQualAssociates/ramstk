# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.dialog.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Dialog Module."""

# Standard Library Imports
import os
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject, Gtk, Pango, _


class RAMSTKDialog(Gtk.Dialog):
    """This is the RAMSTK Dialog class."""
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        r"""
        Initialize a RAMSTK Dialog widget.

        :param str dlgtitle: the title text for the Gtk.Dialog().
        :param \**kwargs: See below

        :Keyword Arguments:
            * *dlgparent* (tuple) -- the parent window to associate the
                Gtk.Dialog() with.
            * *dlgflags* (tuple) -- the flags that control the operation of the
                Gtk.Dialog().  Default is Gtk.DialogFlags.MODAL and
                Gtk.DialogFlags.DESTROY_WITH_PARENT.
            * *dlgbuttons* (tuple) -- the buttons to display and their response
                values.  Default is Gtk.STOCK_OK <==> Gtk.ResponseType.ACCEPT
                Gtk.STOCK_CANCEL <==> Gtk.ResponseType.CANCEL
        """
        try:
            _dlgparent = kwargs['dlgparent']
        except KeyError:
            _dlgparent = None

        super().__init__()

        self.set_title(dlgtitle)
        self.set_transient_for(_dlgparent)
        try:
            self.add_buttons(kwargs['dlgbuttons'])
        except KeyError:
            self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK,
                             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        self.set_destroy_with_parent(True)
        self.set_modal(True)

    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTK Dialog."""
        self.destroy()

    def do_run(self) -> Any:
        """Run the RAMSTK Dialog."""
        return self.run()


class RAMSTKDatabaseSelect(RAMSTKDialog):
    """The RAMSTK Database Selection Dialog."""
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        """Initialize an instance of the RAMSTKdatabaseSelect class."""
        super().__init__(dlgtitle, **kwargs)

        # Initialize private dict attributes.
        self._dao = kwargs['dao']

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        self.__make_ui()

        self.__do_load_databases(database=kwargs['database'])

    def __do_load_databases(self, database: Dict[str, str]) -> None:
        """
        Read the database server and load the database list.

        :param dict database: a dict containing the connection information
            for the RAMSTK program databases.
        :return: None
        :rtype: None
        """
        _model = self._treeview.get_model()
        _model.clear()

        if database['dialect'] == 'postgres':
            database['database'] = 'postgres'

        for _db in self._dao.get_database_list(database):
            _model.append([_db])

    def __make_ui(self) -> None:
        """Build the GUI."""
        self.set_modal(True)

        self._treeview = Gtk.TreeView()

        _model = Gtk.ListStore(GObject.TYPE_STRING)
        self._treeview.set_model(_model)

        _cell = Gtk.CellRendererText()
        _cell.set_alignment(0.1, 0.5)
        _cell.set_property('background', 'light gray')
        _cell.set_property('editable', False)
        _cell.set_property('foreground', '#000000')
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)

        _column = Gtk.TreeViewColumn("RAMSTK Databases")
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        self._treeview.append_column(_column)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_min_content_height(200)
        _scrollwindow.set_min_content_width(500)
        _scrollwindow.add(self._treeview)

        self.vbox.pack_start(_scrollwindow, True, True, 0)
        self.vbox.show_all()

    def _get_database(self) -> str:
        """
        Get the name of the selected database.

        :return: the name of the selected database.
        :rtype: str
        """
        (_model, _row) = self._treeview.get_selection().get_selected()

        return _model.get_value(_row, 0)

    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTKDateSelect dialog."""
        self.destroy()

    def do_run(self) -> str:
        """
        Run the RAMSTKFileChooser dialog.

        :return: _dbname; the selected database name or empty string if none
            selected.
        :rtype: str
        """
        _dbname = ''

        if self.run() == Gtk.ResponseType.OK:
            _dbname = self._get_database()
        elif self.run() == Gtk.ResponseType.CANCEL:
            self.do_destroy()

        return _dbname


class RAMSTKDateSelect(Gtk.Dialog):
    """The RAMSTK Date Selection Dialog."""
    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKDateSelect class."""
        GObject.GObject.__init__(self)

        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        self.set_title(_("Select Date"))

        self._calendar = Gtk.Calendar()
        self.vbox.pack_start(self._calendar, True, True, 0)
        self.vbox.show_all()

    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTKDateSelect dialog."""
        self.destroy()

    def do_run(self) -> Any:
        """
        Run the RAMSTKDateSelect dialog.

        :return: the selected date or the default date if the dialog is
            cancelled.
        :rtype: str
        """
        if self.run() == Gtk.ResponseType.ACCEPT:
            _date = self._calendar.get_date()
            _date = datetime(
                _date[0],
                _date[1] + 1,
                _date[2],
            ).date().strftime("%Y-%m-%d")
        else:
            _date = "1970-01-01"

        return _date


class RAMSTKFileChooser(Gtk.FileChooserDialog):
    """This is the RAMSTK File Chooser Dialog class."""
    def __init__(self, title: str, parent: object) -> None:
        """
        Initialize an instance of the RAMSTKFileChooser dialog.

        :param str title: the title of the dialog.
        :param object parent: the parent window for the dialog.
        """
        Gtk.FileChooserDialog.__init__(self)

        self.add_buttons(
            Gtk.STOCK_OK,
            Gtk.ResponseType.ACCEPT,
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.REJECT
        )

        self.set_title(title)
        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_modal(True)

        self.set_action(Gtk.FileChooserAction.SAVE)

        _filter = Gtk.FileFilter()
        _filter.set_name(_("RAMSTK Databases"))
        _filter.add_pattern('*.ramstk')
        _filter.add_pattern('*.rtk')
        self.add_filter(_filter)
        _filter = Gtk.FileFilter()
        _filter.set_name(_("Excel Files"))
        _filter.add_pattern('*.xls')
        _filter.add_pattern('*xlsm')
        _filter.add_pattern('*xlsx')
        self.add_filter(_filter)
        _filter = Gtk.FileFilter()
        _filter.set_name(_("Delimited Text Files"))
        _filter.add_pattern('*.csv')
        _filter.add_pattern('*.txt')
        self.add_filter(_filter)
        _filter = Gtk.FileFilter()
        _filter.set_name("All files")
        _filter.add_pattern("*")
        self.add_filter(_filter)

    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTKFileChooser dialog."""
        self.destroy()

    def do_run(self) -> Tuple[Optional[Any], Optional[Any]]:
        """
        Run the RAMSTKFileChooser dialog.

        :return: (_filename, _extension); the file name and file extension of
                 the selected file.
        :rtype: (str, str) or (None, None)
        """
        _filename = None
        _extension = None

        if self.run() == Gtk.ResponseType.ACCEPT:
            _filename = self.get_filename()
            # pylint: disable=unused-variable
            __, _extension = os.path.splitext(_filename)
        elif self.run() == Gtk.ResponseType.REJECT:
            self.do_destroy()

        return (_filename, _extension)


class RAMSTKMessageDialog(Gtk.MessageDialog):
    """
    This is the RAMSTK Message Dialog class.

    It used for RAMSTK error, warning, and information messages.
    """
    def __init__(self, parent: Gtk.Window = None) -> None:
        """
        Initialize runtime error, warning, and information dialogs.

        :keyword Gtk.Window _parent: the parent Gtk.Window(), if any, for the
            dialog.
        """
        Gtk.MessageDialog.__init__(self)

        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_modal(True)

        self.show_all()

    def do_set_message(self, message: str) -> None:
        """
        Set the message to display in the dialog.

        :param str message: the message to display.
        :return: None
        :rtype: None
        """
        self.set_markup(message)

    def do_set_message_type(self, message_type: str = 'error') -> None:
        """
        Set RAMSTKMessageDialog message type.

        :param str message_type: the RAMSTKMessageDialog message type.
            Options are error, warning, information, or question.  Default
            is error.
        :return: None
        :rtype: None
        """
        if message_type == 'error':
            _prompt = self.get_property('text')
            # Set the prompt to bold text with a hyperlink to the RAMSTK bugs
            # e-mail address.
            _hyper = "<a href='mailto:bugs@reliaqual.com?subject=RAMSTK BUG " \
                     "REPORT: <ADD SHORT PROBLEM DESCRIPTION>&amp;" \
                     "body=RAMSTK MODULE:%0d%0a%0d%0a" \
                     "RAMSTK VERSION:%20%0d%0a%0d%0a" \
                     "YOUR HARDWARE:%20%0d%0a%0d%0a" \
                     "YOUR OS:%20%0d%0a%0d%0a" \
                     "DETAILED PROBLEM DESCRIPTION:%20%0d%0a'>"
            _prompt = '<b>' \
                     + _prompt \
                     + _(
                         "  Check the error log for additional information "
                         "(if any).  Please e-mail <span foreground='blue' "
                         "underline='single'>",
                     ) \
                     + _hyper \
                     + _(
                         "bugs@reliaqual.com</a></span> with a detailed "
                         "description of the problem, the workflow you are "
                         "using and the error log attached if the problem "
                         "persists.</b>",
                     )
            self.set_markup(_prompt)
            _message_type = Gtk.MessageType.ERROR
            self.add_buttons("_OK", Gtk.ResponseType.OK)
        elif message_type == 'warning':
            _message_type = Gtk.MessageType.WARNING
            self.add_buttons("_OK", Gtk.ResponseType.OK)
        elif message_type == 'information':
            _message_type = Gtk.MessageType.INFO
            self.add_buttons("_OK", Gtk.ResponseType.OK)
        elif message_type == 'question':
            _message_type = Gtk.MessageType.QUESTION
            self.add_buttons("_Yes", Gtk.ResponseType.YES, "_No",
                             Gtk.ResponseType.NO)

        self.set_property('message-type', _message_type)

    def do_run(self) -> Any:
        """Run the RAMSTK Message Dialog."""
        return self.run()

    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTK Message Dialog."""
        self.destroy()
