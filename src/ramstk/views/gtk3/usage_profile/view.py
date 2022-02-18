# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.usage_profile.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Usage Profile Views."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKWorkView

# RAMSTK Local Imports
from . import UsageProfileTreePanel


class UsageProfileWorkView(RAMSTKWorkView):
    """Display Usage Profiles associated with the selected Revision.

    The attributes of a Usage Profile List View are:

    :cvar _tag: the name of the module.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private scalar class attributes.
    _tag: str = "usage_profile"
    _tablabel: str = "<span weight='bold'>" + _("Usage\nProfiles") + "</span>"
    _tabtooltip: str = _("Displays usage profiles for the selected revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize an instance of the Usage Profile list view.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_insert_sibling)
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_delete)
        self._lst_icons.insert(0, "insert_sibling")
        self._lst_icons.insert(1, "insert_child")
        self._lst_icons.insert(2, "remove")
        self._lst_mnu_labels = [
            _("Add Sibling"),
            _("Add Child"),
            _("Delete Selected"),
            _("Save Selected"),
            _("Save Profile"),
        ]
        self._lst_tooltips = [
            _(
                "Add a new usage profile entity at the same level "
                "as the currently selected entity."
            ),
            _(
                "Add a new usage profile entity one level below the "
                "currently selected entity."
            ),
            _("Delete the currently selected entity from the usage profile."),
            _("Save changes to the currently selected entity in the usage profile."),
            _("Save changes to all entities at the same level in the usage profile."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = UsageProfileTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_record_id, f"selected_{self._tag}")

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_(
                f"You are about to delete {self._tag} {self.dic_pkeys['record_id']} "
                f"and all data associated with it.  Is this really what you want to do?"
            )
        )
        _dialog.do_set_message_type(message_type="question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                f"request_delete_{self._tag}",
                node_id=self.dic_pkeys["record_id"],
            )

        _dialog.do_destroy()

    # pylint: disable=unused-argument
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to add an entity to the Usage Profile.

        :return: None
        """
        super().do_set_cursor_busy()

        _attributes = self.__do_get_usage_profile_ids()

        if self._pnlPanel.level == "mission":
            _level = "mission_phase"
            _no_keys = ["environment_id"]
        elif self._pnlPanel.level == "mission_phase":
            _level = "environment"
            _no_keys = []
        else:
            _error = _("An environmental condition cannot have a child.")
            _parent = (
                self.get_parent().get_parent().get_parent().get_parent().get_parent()
            )
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(message=_error)
            _dialog.do_set_message_type(message_type="error")
            _dialog.do_run()
            _dialog.do_destroy()
            pub.sendMessage(
                "fail_insert_usage_profile",
                error_message=_error,
            )
            return

        for _key in _no_keys:
            _attributes.pop(_key)

        super().do_set_cursor_busy()

        pub.sendMessage(f"request_insert_{_level}", attributes=_attributes)

    # pylint: disable=unused-argument
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to add a sibling entity to the Usage Profile.

        :return: None
        """
        super().do_set_cursor_busy()

        _attributes = self.__do_get_usage_profile_ids()

        if self._tag == "mission":
            _attributes.pop("mission_phase_id")
            _attributes.pop("environment_id")
        elif self._tag == "mission_phase":
            _attributes.pop("environment_id")

        pub.sendMessage(
            f"request_insert_{self._tag}",
            attributes=_attributes,
        )

    def __do_get_usage_profile_ids(self) -> Dict[str, int]:
        """Read each of the ID columns.

        :return: _attributes
        :rtype: dict
        """
        _attributes = {
            "revision_id": self._revision_id,
            "mission_id": 0,
            "mission_phase_id": 0,
            "environment_id": 0,
            "parent_id": 0,
            "record_id": 0,
        }

        (
            _model,
            _row,
        ) = self._pnlPanel.tvwTreeView.get_selection().get_selected()

        _attributes["mission_id"] = _model.get_value(_row, 1)
        _attributes["mission_phase_id"] = _model.get_value(_row, 2)
        _attributes["environment_id"] = _model.get_value(_row, 3)

        return _attributes

    def __make_ui(self) -> None:
        """Build the user interface for the usage profile list view.

        :return: None
        :rtype: None
        """
        super().do_make_layout()
        super().do_embed_treeview_panel()

        self._pnlPanel.dic_units = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        )
        self._pnlPanel.do_load_comboboxes()

        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )
        for _element in ["mission", "mission_phase", "environment"]:
            self._pnlPanel.dic_icons[_element] = self._dic_icons[_element]
