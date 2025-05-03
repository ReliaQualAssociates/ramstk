# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.dialogs.database_select_dialog.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKDatabaseSelectDialog module."""

# Standard Library Imports
from typing import Any, Dict, List, Optional, Tuple

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase
from ramstk.views.gtk3 import Gdk, GdkPixbuf, Gtk, Pango, _

# RAMSTK Local Imports
from ..buttons import RAMSTKButton, RAMSTKCheckButton
from ..combo import RAMSTKComboBox
from ..entry import RAMSTKEntry
from ..panels import RAMSTKFixedPanel, RAMSTKTreePanel
from ..treeviews import RAMSTKCellRendererText
from ..widget import WidgetConfig
from . import RAMSTKBaseDialog


class RAMSTKDatabaseSelectDialog(RAMSTKBaseDialog):
    """The RAMSTKDatabaseSelectDialog class."""

    def __init__(
        self,
        title: str,
        parent: object,
        buttons: Optional[Tuple[Any, Any, Any, Any]] = None,
    ) -> None:
        """Initialize an instance of the RAMSTKDatabaseSelectDialog widget.

        :param title: the title text for the RAMSTKDatabaseSelectDialog.
        :param parent: the parent window for the RAMSTKDatabaseSelectDialog.
        :param buttons: a tuple containing the buttons and their associated response
            type.
        """
        RAMSTKBaseDialog.__init__(self, title, parent, buttons)

        # Initialize widgets.
        self._pnlSelectPanel = RAMSTKDatabaseSelectPanel()
        self._pnlTreePanel = RAMSTKDatabaseSelectTreePanel()

        # Initialize private instance attributes.
        self._lst_databases: List[str] = []
        self._dao: Optional[BaseDatabase] = None
        self._db_icon: Optional[GdkPixbuf.Pixbuf] = None
        self._old_host: str = ""

        # Initialize public instance attributes.
        self.database: Dict[str, str] = {}
        self.exists: bool = False

        self._make_ui()
        self.do_set_widget_callbacks()

    # ----- ----- Standard dialog methods. ----- ----- #
    def do_set_widget_callbacks(self):
        """Set the callback method for the RAMSTKDatabaseSelectDialog widgets."""
        self._pnlSelectPanel.btnRefresh.connect(
            "clicked", self._request_load_database_list
        )
        self._pnlTreePanel.tvwTreeView.selection.connect("changed", self._on_row_change)

    def do_run(self) -> Tuple[Gtk.ResponseType, bool]:
        """Run the RAMSTKDatabaseSelectDialog.

        :return: _return, _save
        :rtype: Gtk.ResponseType and bool
        """
        _return = Gtk.ResponseType.CANCEL
        _save = False

        if self.run() == Gtk.ResponseType.OK:
            self._get_database()
            self.exists = self.database["database"] in self._lst_databases
            _return = Gtk.ResponseType.OK
            _save = self._pnlSelectPanel.btnSave.get_active()

        return _return, _save

    # ----- ----- RAMSTKDatabaseSelectDialog specific methods. ----- ----- #
    def do_load_database_parameters(self) -> None:
        """Load the database connection parameter widgets."""
        self._pnlSelectPanel.do_load_panel(self.database)

    def do_load_databases(self) -> None:
        """Read the database server and load the database list."""
        self._old_host = self.database["host"]
        _dialect = 0

        if self._dao is None:
            # RAMSTK Package Imports
            from ramstk.models.db import (  # pylint: disable=import-outside-toplevel
                RAMSTKCommonDB,
            )

            self._dao = RAMSTKCommonDB()
            self._dao.do_connect(self.database)

        _model = self._pnlTreePanel.tvwTreeView.get_model()
        _model.clear()

        if (
            self.database["dialect"] == "postgres"
            and self.database["user"] != "first_run"
        ):
            _dialect = 1
            _stored_db = self.database["database"]
            self.database["database"] = "postgres"
            for _db in self._dao.get_database_list(self.database):
                _model.append([_db, self._db_icon])
                self._lst_databases.append(_db)

            self.database["database"] = _stored_db

    def do_set_icons(self, icons: Dict[str, str]) -> None:
        """Set the button icons.

        :param icons: a dict containing the name of the button as key and the absolute
            path to the image file used for the button icon.
        """
        _image = Gtk.Image()
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(icons["refresh"], 22, 22)
        _image.set_from_pixbuf(_icon)
        self._pnlSelectPanel.btnRefresh.set_image(_image)

        _image = Gtk.Image()
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(icons["save"], 22, 22)
        _image.set_from_pixbuf(_icon)
        self._pnlSelectPanel.btnSave.set_image(_image)

        self._db_icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icons["db-disconnected"], 22, 22
        )

    def _get_database(self) -> None:
        """Get the database connection parameters."""
        self.database["dialect"] = self._pnlSelectPanel.cmbDialect.get_value()
        self.database["host"] = str(self._pnlSelectPanel.txtHost.do_get_text())
        self.database["port"] = str(self._pnlSelectPanel.txtPort.do_get_text())
        self.database["database"] = str(self._pnlSelectPanel.txtDatabase.do_get_text())
        self.database["user"] = str(self._pnlSelectPanel.txtUser.do_get_text())
        self.database["password"] = str(self._pnlSelectPanel.txtPassword.do_get_text())

        # If the host was changed, reload the database list.
        if self.database["host"] != self._old_host:
            self.do_load_databases()

    def _make_ui(self) -> None:
        """Build the RAMSTKDatabaseSelectDialog."""
        self._pnlTreePanel.tvwTreeView.do_make_model(
            ["gchararray", GdkPixbuf.Pixbuf], "list"
        )
        self.vbox.pack_start(self._pnlSelectPanel, True, True, 10)
        self.vbox.pack_end(self._pnlTreePanel, True, True, 0)
        self.set_property("height-request", 850)
        self.set_property("width-request", 500)
        self.vbox.show_all()

    def _request_load_database_list(self, __button: RAMSTKButton) -> None:
        """Reload the database list.

        :param __button: the RAMSTKButton that called this method on 'clicked'.
        """
        self._get_database()
        self.do_load_databases()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Respond to changes in database selection."""
        _database = self._pnlTreePanel.on_row_change(selection)
        self._pnlSelectPanel.txtDatabase.do_update({"database": _database})


class RAMSTKDatabaseSelectPanel(RAMSTKFixedPanel):
    """The RAMSTKDatabaseSelectPanel class."""

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKDatabaseSelectPanel widget."""
        super().__init__()

        # Initialize widgets.
        self.btnRefresh: RAMSTKButton = RAMSTKButton(label="Refresh Database List")
        self.btnSave: RAMSTKCheckButton = RAMSTKCheckButton(
            label="Save Connection Parameters"
        )
        self.cmbDialect: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHost: RAMSTKEntry = RAMSTKEntry()
        self.txtPort: RAMSTKEntry = RAMSTKEntry()
        self.txtDatabase: RAMSTKEntry = RAMSTKEntry()
        self.txtUser: RAMSTKEntry = RAMSTKEntry()
        self.txtPassword: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.cmbDialect,
                "attributes": {
                    "datatype": "gchararray",
                    "field": "dialect",
                    "index": 0,
                    "label_text": _("Database Dialect:"),
                    "send_topic": "null",
                },
                "properties": {
                    "tooltip": _("Select SQL server dialect for this connection."),
                    "width_request": 300,
                },
            },
            {
                "widget": self.txtHost,
                "attributes": {
                    "datatype": "gchararray",
                    "field": "host",
                    "index": 1,
                    "label_text": _("Database Server:"),
                    "send_topic": "null",
                },
                "properties": {
                    "tooltip": _("Enter the database server hostname."),
                    "width_request": 300,
                },
            },
            {
                "widget": self.txtPort,
                "attributes": {
                    "datatype": "gchararray",
                    "field": "port",
                    "index": 2,
                    "label_text": _("Server Port:"),
                    "send_topic": "null",
                },
                "properties": {
                    "tooltip": _(
                        "Enter the port number the database server listens on."
                    ),
                    "width_request": 300,
                },
            },
            {
                "widget": self.txtDatabase,
                "attributes": {
                    "datatype": "gchararray",
                    "field": "database",
                    "index": 3,
                    "label_text": _("Database Name:"),
                    "send_topic": "null",
                },
                "properties": {
                    "tooltip": _("Enter the name of the database to connect."),
                    "width_request": 300,
                },
            },
            {
                "widget": self.txtUser,
                "attributes": {
                    "datatype": "gchararray",
                    "field": "user",
                    "index": 4,
                    "label_text": _("RAMSTK User:"),
                    "send_topic": "null",
                },
                "properties": {
                    "tooltip": _("Enter the user name for the database server."),
                    "width_request": 300,
                },
            },
            {
                "widget": self.txtPassword,
                "attributes": {
                    "datatype": "gchararray",
                    "field": "password",
                    "index": 5,
                    "label_text": _("RAMSTK Password:"),
                    "send_topic": "null",
                },
                "properties": {
                    "input_purpose": Gtk.InputPurpose.PASSWORD,
                    "invisible_char": "*",
                    "tooltip": _("Enter the user password for the database server."),
                    "width_request": 300,
                },
            },
            {
                "widget": self.btnSave,
                "attributes": {
                    "field": "",
                    "index": 6,
                    "label_text": "",
                },
                "properties": {
                    "tooltip": _("Save connection information to configuration file."),
                    "width_request": 50,
                },
            },
            {
                "widget": self.btnRefresh,
                "attributes": {
                    "field": "",
                    "index": 7,
                    "label_text": "",
                },
                "properties": {
                    "tooltip": _("Refresh server database list."),
                    "width_request": 50,
                },
            },
        ]

        # Set up the panel.
        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()
        self._do_load_dialects()
        self.txtPassword.set_visibility(False)

    # ----- ----- RAMSTKFixedPanel specific methods. ----- ----- #
    def do_load_panel(self, attributes):
        """Load the panel widgets with database connection parameters.

        :param attributes: the dict containing the database connection parameters.
        """
        self.cmbDialect.do_update({"dialect": 1})
        self.txtHost.do_update({"host": attributes["host"]})
        self.txtPort.do_update({"port": attributes["port"]})
        self.txtDatabase.do_update({"database": attributes["database"]})
        self.txtUser.do_update({"user": attributes["user"]})
        self.txtPassword.do_update({"password": attributes["password"]})

    # ----- ----- RAMSTKDatabaseSelectPanel specific methods. ----- ----- #
    def _do_load_dialects(self) -> None:
        """Load the dialect RAMSTKComboBox."""
        self.cmbDialect.do_load_combo([["postgres", "", ""]])


class RAMSTKDatabaseSelectTreePanel(RAMSTKTreePanel):
    """The RAMSTKDatabaseSelectTreePanel class."""

    def __init__(self):
        """Initialize an instance of the RAMSTKDatabaseSelectTreePanel widget."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "",
                    "index": 0,
                    "label_text": _("Database"),
                },
                "properties": {
                    "cell_background_rgba": Gdk.RGBA(
                        red=211.0, green=211.0, blue=211.0, alpha=0.8
                    ),
                    "cell_foreground_rgba": Gdk.RGBA(
                        red=0.0, green=0.0, blue=0.0, alpha=1.0
                    ),
                    "editable": False,
                    "wrap_width": 250,
                    "wrap_mode": Pango.WrapMode.WORD_CHAR,
                    "xalign": 0.1,
                    "yalign": 0.5,
                    "visible": True,
                },
            }
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()

    # ----- ----- Standard RAMSTKTreePanel methods. ----- ----- #
    def on_row_change(self, selection) -> str:
        """Get the value of the selected row.

        :param selection: the Gtk.TreeSelection that is active.
        """
        _model, _row = selection.get_selected()
        return _model.get_value(_row, 0)
