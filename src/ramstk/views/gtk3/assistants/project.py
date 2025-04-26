# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.project.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Open Project Assistant module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.models.db import BaseDatabase
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKBaseDialog,
    RAMSTKDatabaseSelectDialog,
    RAMSTKLabel,
    RAMSTKMessageDialog,
)


class CreateProject:
    """The class used to create a new RAMSTK Project database."""

    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

    def __init__(
        self,
        __button: Gtk.ToolButton,
        configuration: RAMSTKUserConfiguration,
        parent: object,
    ) -> None:
        """Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton that launched this class.
        :param configuration: the RAMSTKUserConfiguration class instance.
        :param parent: the parent window associated with the dialog.
        """
        # Initialize private instance attributes.
        self._parent: object = parent

        # Initialize public instance attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self._do_request_create_project()

    def _do_confirm_overwrite(self, database: str) -> None:
        """Raise dialog to confirm overwriting existing RAMSTK database.

        :param database: the name of the existing database that is to be confirmed for
            overwrite.
        """
        _dialog = RAMSTKBaseDialog(
            _("RAMSTK - Confirm Overwrite"),
            self._parent,
            (
                Gtk.STOCK_YES,
                Gtk.ResponseType.YES,
                Gtk.STOCK_NO,
                Gtk.ResponseType.NO,
            ),
        )

        _label = RAMSTKLabel(
            _(
                f"RAMSTK Program database already exists:\n\n\t\t"
                f"{database}\n\nOverwrite?"
            )
        )
        _label.do_set_properties(
            {
                "bold": False,
                "height_request": -1,
                "width_request": -1,
                "wrap": True,
            }
        )
        _dialog.vbox.pack_start(_label, True, True, 0)
        _dialog.show_all()

        if _dialog.run() == Gtk.ResponseType.YES:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO["database"] = database
        else:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO["database"] = ""

        _dialog.destroy()

    def _do_request_create_project(self) -> None:
        """Request to create a new RAMSTK Project Database."""
        _dialog = RAMSTKDatabaseSelectDialog(
            _(
                f"Select RAMSTK Program Database on the "
                f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['dialect']} "
                f"Server"
            ),
            self._parent,
        )

        _dialog.dao = BaseDatabase()
        _dialog.database = self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO
        _dialog.do_set_icons(
            {
                "refresh": self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                + "/icons/32x32/view-refresh.png",
                "save": self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                + "/icons/32x32/save.png",
            },
        )

        if _dialog.do_run() == Gtk.ResponseType.OK:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO = _dialog.database

            if _dialog.exists:
                self._do_confirm_overwrite(_dialog.database["database"])

            pub.sendMessage(
                "request_create_program",
                database=self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO,
                sql_file=f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR}/{self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['dialect']}_program_db.sql",  # noqa
            )

        _dialog.destroy()


class OpenProject:
    """Assistant to guide user through process of creating RAMSTK Project."""

    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

    def __init__(
        self,
        __button: Gtk.ToolButton,
        configuration: RAMSTKUserConfiguration,
        parent: object,
    ) -> None:
        """Initialize an instance of the Create Project Assistant.

        :param __button: the Gtk.ToolButton() that launched an instance of this class.
        :param configuration: the RAMSTKUserConfiguration class instance.
        """
        # Initialize private instance attributes.
        self._parent: object = parent

        # Initialize public instance attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration

        self._do_request_open_project()

    def _do_request_open_project(self) -> None:
        """Open or connect to a RAMSTK Program database."""
        if self.RAMSTK_USER_CONFIGURATION.loaded:
            self.__project_is_open()
        else:
            _dialog = RAMSTKDatabaseSelectDialog(
                (
                    f"Select RAMSTK Program Database on the "
                    f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['dialect']} "
                    f"Server"
                ),
                self._parent,
            )
            _dialog.dao = BaseDatabase()
            _dialog.database = self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO
            _dialog.do_set_icons(
                {
                    "refresh": self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                    + "/icons/32x32/view-refresh.png",
                    "save": self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                    + "/icons/32x32/save.png",
                    "db-disconnected": self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                    + "/icons/32x32/db-disconnected.png",
                }
            )

            _response, _save = _dialog.do_run()
            if _response == Gtk.ResponseType.OK:
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO = _dialog.database

                if _dialog.exists:
                    pub.sendMessage(
                        "request_open_program",
                        database=self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO,
                    )
                else:
                    pub.sendMessage(
                        "request_create_program",
                        database=self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO,
                        sql_file=f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR}/{self.RAMSTK_USER_CONFIGURATION.RAMSTK_PROG_INFO['dialect']}_program_db.sql",  # noqa
                    )

                if _save:
                    self.RAMSTK_USER_CONFIGURATION.set_user_configuration()

            _dialog.do_destroy()

    def __project_is_open(self) -> None:
        """Raise dialog explaining a project is already open."""
        _prompt = _(
            "A database is already open.  Only one database can "
            "be open at a time in RAMSTK.  You must close the "
            "currently open RAMSTK database before a new "
            "database can be opened."
        )
        _dialog = RAMSTKMessageDialog(
            _("Database Currently Open"),
            self._parent,
        )
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type("info")

        if _dialog.run() == Gtk.ResponseType.OK:
            _dialog.destroy()
