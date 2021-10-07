# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.usage_profile.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Usage Profile Views."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView

# RAMSTK Local Imports
from . import UsageProfileTreePanel


class UsageProfileListView(RAMSTKListView):
    """Display Usage Profiles associated with the selected Revision.

    The attributes of a Usage Profile List View are:

    :cvar _module: the name of the module.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private scalar class attributes.
    _module: str = "usage_profile"
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
        self._lst_callbacks[0] = self._do_request_insert_sibling
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_delete)
        self._lst_col_order = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self._lst_icons[0] = "insert_sibling"
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
            _("Save changes to all entities in the usage profile."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = UsageProfileTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        _node_id = _model.get_value(_row, 8)
        _level = _model.get_value(_row, 10)

        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_(
                "You are about to delete {1:s} {0:s} and all data "
                "associated with it.  Is this really what you want to "
                "do?"
            ).format(_node_id, _level)
        )
        _dialog.do_set_message_type(message_type="question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_delete_usage_profile",
                node_id=_node_id,
            )

        _dialog.do_destroy()

    # pylint: disable=unused-argument
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to add an entity to the Usage Profile.

        :return: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        _level = _model.get_value(_row, 10)
        _prow = _model.iter_parent(_row)

        super().do_set_cursor_busy()
        if _level == "mission":
            _mission_id = _model.get_value(_row, 0)
            pub.sendMessage(
                "request_insert_mission_phase",
                mission_id=_mission_id,
            )
        elif _level == "phase":
            _phase_id = _model.get_value(_row, 0)
            _mission_id = _model.get_value(_prow, 0)
            pub.sendMessage(
                "request_insert_environment",
                mission_id=_mission_id,
                phase_id=_phase_id,
            )
        elif _level == "environment":
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

    # pylint: disable=unused-argument
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to add a sibling entity to the Usage Profile.

        :return: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        try:
            _level = _model.get_value(_row, 10)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _level = "mission"
            _prow = None

        super().do_set_cursor_busy()
        if _level == "mission":
            pub.sendMessage(
                "request_insert_mission",
            )
        elif _level == "phase":
            _mission_id = _model.get_value(_prow, 0)
            pub.sendMessage(
                "request_insert_mission_phase",
                mission_id=_mission_id,
            )
        elif _level == "environment":
            _gprow = _model.iter_parent(_prow)
            _mission_id = _model.get_value(_gprow, 0)
            _phase_id = _model.get_value(_prow, 0)
            pub.sendMessage(
                "request_insert_environment",
                mission_id=_mission_id,
                phase_id=_phase_id,
            )

    def __make_ui(self):
        """Build the user interface for the usage profile list view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.dic_units = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        )

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_load_comboboxes()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )
        for _element in ["mission", "phase", "environment"]:
            self._pnlPanel.dic_icons[_element] = self._dic_icons[_element]
