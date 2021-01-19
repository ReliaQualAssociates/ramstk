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
from typing import Any, Dict, List, Optional, Tuple

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, Pango, _
from ramstk.views.gtk3.widgets.button import RAMSTKButton, RAMSTKCheckButton
from ramstk.views.gtk3.widgets.combo import RAMSTKComboBox
from ramstk.views.gtk3.widgets.entry import RAMSTKEntry
from ramstk.views.gtk3.widgets.label import do_make_label_group


class RAMSTKDialog(Gtk.Dialog):
    """The RAMSTK Dialog class."""
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        """Initialize a RAMSTK Dialog widget.

        Accepts the following keyword arguments:
            * *dlgparent* (tuple) -- the parent window to associate the
                Gtk.Dialog() with.
            * *dlgflags* (tuple) -- the flags that control the operation of the
                Gtk.Dialog().  Default is Gtk.DialogFlags.MODAL and
                Gtk.DialogFlags.DESTROY_WITH_PARENT.
            * *dlgbuttons* (tuple) -- the buttons to display and their response
                values.  Default is Gtk.STOCK_OK <==> Gtk.ResponseType.ACCEPT
                Gtk.STOCK_CANCEL <==> Gtk.ResponseType.CANCEL

        :param dlgtitle: the title text for the Gtk.Dialog().
        """
        _dlgbuttons = kwargs.get('dlgbuttons',
                                 (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                  Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        _dlgparent = kwargs.get('dlgparent', None)

        super().__init__()

        self.set_title(dlgtitle)
        self.set_transient_for(_dlgparent)
        self.add_buttons(*_dlgbuttons)

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
        self._dao: BaseDatabase = kwargs.get('dao', BaseDatabase)
        self._dic_icons = kwargs.get('icons', {})

        # Initialize private list attributes.
        self._lst_databases: List[str] = []
        self._lst_labels: List[str] = [
            _('Database Dialect:'),
            _('Database Server:'),
            _('Server Port:'),
            _('Database Name:'),
            _('RAMSTK User:'),
            _('RAMSTK Password:')
        ]

        # Initialize private scalar attributes.
        self._old_host: str = ''

        # Initialize public scalar attributes.
        self.btnRefresh: RAMSTKButton = RAMSTKButton(label='')
        self.btnSave: RAMSTKCheckButton = RAMSTKCheckButton(
            label='Save Connection Parameters')
        self.cmbDialect: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHost: RAMSTKEntry = RAMSTKEntry()
        self.txtPort: RAMSTKEntry = RAMSTKEntry()
        self.txtDatabase: RAMSTKEntry = RAMSTKEntry()
        self.txtUser: RAMSTKEntry = RAMSTKEntry()
        self.txtPassword: RAMSTKEntry = RAMSTKEntry()
        self.tvwTreeView: Gtk.TreeView = Gtk.TreeView()

        self._lst_widgets = [
            self.cmbDialect, self.txtHost, self.txtPort, self.txtDatabase,
            self.txtUser, self.txtPassword
        ]

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.database: Dict[str, str] = kwargs.get('database', {})
        self.exists: bool = False

        self.__do_set_properties()
        self.__make_ui()
        self.__do_load_combobox()
        self.__do_set_callbacks()

        self.__do_load_databases()

    def do_run(self) -> Gtk.ResponseType:
        """Run the RAMSTKFileChooser dialog.

        :return: _return
        :rtype: Gtk.ResponseType
        """
        _return = Gtk.ResponseType.CANCEL

        if self.run() == Gtk.ResponseType.OK:
            self._get_database()
            self.exists = self.database['database'] in self._lst_databases
            _return = Gtk.ResponseType.OK
        elif self.run() == Gtk.ResponseType.CANCEL:
            _return = Gtk.ResponseType.CANCEL

        return _return

    def _get_database(self):
        """Get the name of the selected database.

        :return: the database connection parameters.
        :rtype: dict
        """
        self.database['dialect'] = self.cmbDialect.get_value()
        self.database['host'] = self.txtHost.do_get_text()
        self.database['port'] = self.txtPort.do_get_text()
        self.database['database'] = self.txtDatabase.do_get_text()
        self.database['user'] = self.txtUser.do_get_text()
        self.database['password'] = self.txtPassword.do_get_text()

        # IF the host was changed, reload the database list, otherwise keep
        # going.
        if self.database['host'] != self._old_host:
            self.__do_load_databases()

    def _request_load_databases(self, __button: RAMSTKButton) -> None:
        """Re-load the database list.

        :param __button: the RAMSTKButton() that called this method on
            'clicked'.
        :return: None
        :rtype: None
        """
        self.database['dialect'] = self.cmbDialect.get_value()
        self.database['host'] = self.txtHost.do_get_text()
        self.database['port'] = self.txtPort.do_get_text()
        self.database['database'] = self.txtDatabase.do_get_text()
        self.database['user'] = self.txtUser.do_get_text()
        self.database['password'] = self.txtPassword.do_get_text()

        self.__do_load_databases()

    def __do_load_combobox(self) -> None:
        """Load the dialect RAMSTKComboBox."""
        self.cmbDialect.do_load_combo([['postgres', '', '']])

    def __do_load_databases(self) -> None:
        """Read the database server and load the database list.

        :return: None
        :rtype: None
        """
        _dialect = 0

        self._old_host = self.database['host']

        self.txtHost.do_update(self.database['host'])
        self.txtPort.do_update(self.database['port'])
        self.txtDatabase.do_update(self.database['database'])
        self.txtUser.do_update(self.database['user'])
        self.txtPassword.do_update(self.database['password'])

        _model = self.tvwTreeView.get_model()
        _model.clear()

        if (self.database['dialect'] == 'postgres'
                and self.database['user'] != 'first_run'):
            _dialect = 1
            _stored_db = self.database['database']
            self.database['database'] = 'postgres'

            for _db in self._dao.get_database_list(self.database):
                _model.append([_db])
                self._lst_databases.append(_db)

            self.database['database'] = _stored_db

        self.cmbDialect.do_update(_dialect)

    def __do_set_callbacks(self) -> None:
        """Set widget callback methods."""
        self.btnRefresh.connect('clicked', self._request_load_databases)
        self.tvwTreeView.selection.connect('changed', self.__on_row_change)

    def __do_set_properties(self) -> None:
        """Set the properties of the widgets."""
        _image = Gtk.Image()
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['refresh'], 22, 22)
        _image.set_from_pixbuf(_icon)
        self.btnRefresh.set_image(_image)
        self.btnRefresh.do_set_properties(
            tooltip=_('Refresh server database list.'), width=50)
        self.btnSave.do_set_properties(
            tooltip=_('Save connection information to configuration file.'))
        self.cmbDialect.do_set_properties(
            tooltip=_('Select SQL server dialect for this connection.'),
            width=300)
        self.txtHost.do_set_properties(
            tooltip=_('Enter the database server hostname.'), width=300)
        self.txtPort.do_set_properties(
            tooltip=_('Enter the port number the database server listens on.'),
            width=300)
        self.txtDatabase.do_set_properties(
            tooltip=_('Enter the name of the database to connect.'), width=300)
        self.txtUser.do_set_properties(
            tooltip=_('Enter the user name for the database server.'),
            width=300)
        self.txtPassword.do_set_properties(
            tooltip=_('Enter the user password for the database server.'),
            width=300)

        self.tvwTreeView.selection = self.tvwTreeView.get_selection()

    def __make_ui(self) -> None:
        """Build the GUI."""
        self.set_modal(True)

        _fixed = Gtk.Fixed()

        (_x_pos, _labels) = do_make_label_group(self._lst_labels)
        _y_pos = 5
        for _idx, _label in enumerate(_labels):
            _fixed.put(_label, 5, _y_pos)
            _fixed.put(self._lst_widgets[_idx], _x_pos + 10, _y_pos)
            _y_pos += 35

        # Add the refresh and save buttons.
        _fixed.put(self.btnRefresh, _x_pos + 315, 40)
        _fixed.put(self.btnSave, _x_pos + 315, 180)
        self.vbox.pack_start(_fixed, True, True, 10)

        _model = Gtk.ListStore(GObject.TYPE_STRING)
        self.tvwTreeView.set_model(_model)

        _cell = Gtk.CellRendererText()
        _cell.set_alignment(0.1, 0.5)
        _cell.set_property('background', 'light gray')
        _cell.set_property('editable', False)
        _cell.set_property('foreground', '#000000')
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)

        _column = Gtk.TreeViewColumn("Available Databases")
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        self.tvwTreeView.append_column(_column)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_min_content_height(200)
        _scrollwindow.set_min_content_width(500)
        _scrollwindow.add(self.tvwTreeView)

        self.vbox.pack_end(_scrollwindow, True, True, 0)
        self.vbox.show_all()

    def __on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Respond to changes in database list selection."""
        _model, _row = selection.get_selected()
        self.txtDatabase.do_update(_model.get_value(_row, 0))


class RAMSTKDateSelect(Gtk.Dialog):
    """The RAMSTK Date Selection Dialog."""
    def __init__(self, **kwargs) -> None:
        """Initialize an instance of the RAMSTKDateSelect class."""
        _dlgparent = kwargs.get('dlgparent', None)

        super().__init__(self)

        self.set_transient_for(_dlgparent)
        self.set_destroy_with_parent(True)
        self.set_modal(True)

        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT)
        self.set_title(_("Select Date"))

        self._calendar = Gtk.Calendar()
        self.vbox.pack_start(self._calendar, True, True, 0)
        self.vbox.show_all()

    def do_destroy(self) -> None:  # pylint: disable=arguments-differ
        """Destroy the RAMSTKDateSelect dialog."""
        self.destroy()

    def do_run(self) -> Any:
        """Run the RAMSTKDateSelect dialog.

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
    """The RAMSTK File Chooser Dialog class."""
    def __init__(self, title: str, parent: object) -> None:
        """Initialize an instance of the RAMSTKFileChooser dialog.

        :param title: the title of the dialog.
        :param object parent: the parent window for the dialog.
        """
        Gtk.FileChooserDialog.__init__(self)

        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,
                         Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)

        self.set_title(title)
        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_modal(True)

        self.set_action(Gtk.FileChooserAction.SAVE)

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
        """Run the RAMSTKFileChooser dialog.

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

        return _filename, _extension


class RAMSTKMessageDialog(Gtk.MessageDialog):
    """The RAMSTK Message Dialog class.

    It used for RAMSTK error, warning, and information messages.
    """
    def __init__(self, parent: Gtk.Window = None) -> None:
        """Initialize runtime error, warning, and information dialogs.

        :param parent: the parent Gtk.Window(), if any, for the dialog.
        """
        Gtk.MessageDialog.__init__(self)

        self.set_transient_for(parent)
        self.set_destroy_with_parent(True)
        self.set_modal(True)

        self.show_all()

    def do_set_message(self, message: str) -> None:
        """Set the message to display in the dialog.

        :param message: the message to display.
        :return: None
        :rtype: None
        """
        self.set_markup(message)

    def do_set_message_type(self, message_type: str = 'error') -> None:
        """Set RAMSTKMessageDialog message type.

        :param message_type: the RAMSTKMessageDialog message type.
            Options are error, warning, information, or question.  Default
            is error.
        :return: None
        :rtype: None
        """
        _message_type = Gtk.MessageType.INFO

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
            _prompt = '<b>' + _prompt + _(
                "  Check the error log for additional information "
                "(if any).  Please e-mail <span foreground='blue' "
                "underline='single'>", ) + _hyper + _(
                    "bugs@reliaqual.com</a></span> with a detailed "
                    "description of the problem, the workflow you are "
                    "using and the error log attached if the problem "
                    "persists.</b>", )
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
