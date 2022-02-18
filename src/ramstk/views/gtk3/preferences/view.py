# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.preferences.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Preferences Views."""

# Standard Library Imports
from datetime import datetime
from shutil import copyfile
from typing import Any, Dict

# Third Party Imports
import toml
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import integer_to_boolean
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKBaseView, RAMSTKLabel

# RAMSTK Local Imports
from . import (
    GeneralPreferencesPanel,
    LookFeelPreferencesPanel,
    TreeLayoutPreferencesPanel,
)


class PreferencesDialog(RAMSTKBaseView):
    """Assistant to provide a GUI to set various RAMSTK config preferences.

    RAMSTK preferences are stored in the RAMSTK Site database and the user's Site
    configuration file and Program configuration file. Configurations preferences
    are stored in Site.conf or RAMSTK.conf in each user's $HOME/.config/RAMSTK
    directory and are applicable only to that specific user.  Configuration
    preferences are edited with the Preferences assistant.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "preferences"
    _pixbuf: bool = True
    _tablabel: str = _("")
    _tabtooltip: str = _("")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize an instance of the Preferences assistant.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [self._do_request_update, self._cancel]
        self._lst_icons = ["save", "cancel"]
        self._lst_tooltips = [
            _(
                f"Save changes to RAMSTK program configuration file "
                f"{configuration.RAMSTK_CONF_DIR}/RAMSTK.toml."
            ),
            _("Quit the RAMSTK preferences assistant without saving."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralPreferences: GeneralPreferencesPanel = GeneralPreferencesPanel()
        self._pnlLookFeel: LookFeelPreferencesPanel = LookFeelPreferencesPanel()
        self._pnlTreeViewLayout: TreeLayoutPreferencesPanel = (
            TreeLayoutPreferencesPanel()
        )

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        pub.sendMessage(
            "request_load_preferences",
            configuration=self.RAMSTK_USER_CONFIGURATION,
        )

    def _cancel(self, __button: Gtk.Button) -> None:
        """Quit the preferences Gtk.Assistant().

        :param __button: the Gtk.Button() that called this method.
        :return: None
        """
        _parent = self.get_parent()
        _parent.destroy()

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """Request to update the user and program preferences.

        :param __button: the Gtk.Button() that called this method.
        :return: None
        """
        _conf_file = self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + "/RAMSTK.toml"
        copyfile(_conf_file, _conf_file + "_bak")
        self.RAMSTK_USER_CONFIGURATION.set_user_configuration()

        try:
            self._do_save_tree_layout()
        # This happens when no format file was edited.
        except FileNotFoundError:
            pass

    def _do_save_tree_layout(self) -> None:
        """Save the Module View RAMSTKTreeView() layout file.

        :return: None
        """
        _layout: Dict[str, Any] = {
            "pixbuf": "False",
            "defaulttitle": {},
            "usertitle": {},
            "datatype": {},
            "position": {},
            "widget": {},
            "editable": {},
            "visible": {},
            "key": {},
        }

        copyfile(
            self._pnlTreeViewLayout.fmt_file,
            self._pnlTreeViewLayout.fmt_file + "_bak",
        )

        # Get the format file for the Gtk.TreeView to be edited.  Make a
        # backup copy by appending the current date.
        _now = datetime.today().strftime("%Y%m%d")
        _bak_file = f"{self._pnlTreeViewLayout.fmt_file[:-5]}_bak_{_now}.toml"
        copyfile(self._pnlTreeViewLayout.fmt_file, _bak_file)

        # Open the format file for writing.
        with open(self._pnlTreeViewLayout.fmt_file, "w", encoding="utf-8") as _file:
            _model = self._pnlTreeViewLayout.tvwTreeView.get_model()
            _row = _model.get_iter_first()
            while _row is not None:
                _key = _model.get_value(_row, 8)
                _layout["defaulttitle"][_key] = _model.get_value(_row, 0)
                _layout["usertitle"][_key] = _model.get_value(_row, 1)
                _layout["position"][_key] = _model.get_value(_row, 2)
                _layout["editable"][_key] = integer_to_boolean(
                    _model.get_value(_row, 3)
                )
                _layout["visible"][_key] = integer_to_boolean(_model.get_value(_row, 4))
                _layout["datatype"][_key] = _model.get_value(_row, 5)
                _layout["widget"][_key] = _model.get_value(_row, 6)
                _layout["key"][_key] = _model.get_value(_row, 7)

                _row = _model.iter_next(_row)

            toml.dump(_layout, _file)

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        _label = RAMSTKLabel(_("General &amp; Directories"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Allows setting general preferences for the open RAMSTK program."
            ),
        )
        self._notebook.insert_page(
            self._pnlGeneralPreferences, tab_label=_label, position=-1
        )

        _label = RAMSTKLabel(_("Look &amp; Feel"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting color and other preferences."),
        )
        self._notebook.insert_page(self._pnlLookFeel, tab_label=_label, position=-1)

        _label = RAMSTKLabel(_("Tree View Layout"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting tree view layout preferences."),
        )
        self._notebook.insert_page(
            self._pnlTreeViewLayout, tab_label=_label, position=-1
        )

        self.pack_end(self._notebook, True, True, 0)

        self.show_all()
