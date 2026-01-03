# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panels.base_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBasePanel module."""


# Standard Library Imports
from typing import List

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
from pubsub import pub

# RAMSTK Local Imports
from ..frame import RAMSTKFrame
from ..widget import RAMSTKBaseWidget, WidgetConfig


def do_log_message(
    method_name: str, topic_name: str, logger_name: str, message: str
) -> None:
    """Log a message."""
    # FIXME: This should move to the utilities module.
    pub.sendMessage(
        topic_name, logger_name=logger_name, message=f"{method_name}: {message}"
    )


class RAMSTKBasePanel(RAMSTKFrame):
    """The RAMSTKBasePanel class.

    The attributes of a RAMSTKBasePanel are:

    :cvar _record_field: the database table field that contains the record ID.
    :cvar _select_msg: the PyPubSub message the panel listens for to load values into
        its attribute widgets.  Defaults to "selected_revision".
    :cvar _tag: the name of the tag in the table or view model tree.  This should be
        the same value as the _tag attribute for the table or view model the panel is
        used to display.
    :cvar _title: the title to display on the panel frame.

    :ivar _lst_widget_configuration: a list containing dicts with each dict
    containing a widget object and, optionally, a dict with the widget attributes and a
    dict with the widget properties.
    :ivar _parent_id: the ID of the parent entity for the selected work stream entity.
        This is needed for hierarchical modules such as the function module.  For flat
        modules, this will always be zero.
    :ivar _record_id: the work stream module ID whose attributes this panel is
        displaying.
    """

    # Define private class attributes.
    _record_field: str = ""
    _select_msg: str = "selected_nothing"
    _tag: str = ""
    _title: str = ""

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKBasePanel widget."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = []
        self._parent_id: int = -1
        self._record_id: int = -1

    # ----- ----- Standard panel methods. ----- ----- #
    def do_set_widget_attributes(self) -> None:
        """Set the attributes of the RAMSTKBasePanel widgets."""
        for _widget in self._lst_widget_configuration:
            _widget["widget"].do_set_attributes(_widget["attributes"])

    def do_set_widget_callbacks(self) -> None:
        """Set the callbacks for the RAMSTKBasePanel widgets."""
        for _widget in self._lst_widget_configuration:
            _widget["widget"].do_set_callbacks()

        # For RAMSTKTreePanels, set RAMSTKTreeView callbacks.
        if hasattr(self, "tvwTreeView"):
            self.tvwTreeView.selection.connect("changed", self.on_row_change)

    def do_set_widget_properties(self) -> None:
        """Set the properties of the RAMSTKBasePanel widgets."""
        for _widget in self._lst_widget_configuration:
            _widget["widget"].do_set_properties(_widget["properties"])

    @staticmethod
    def do_set_widget_sensitivity(
        widgets: List[RAMSTKBaseWidget], sensitive=True
    ) -> None:
        """Set the sensitivity of the RAMSTKBasePanel widgets.

        :param widgets: a list of RAMSTKWidget objects to set sensitivity.
        :param sensitive: the sensitivity state to set the widgets to.
        """
        for _widget in widgets:
            _widget.set_sensitive(sensitive)

    @staticmethod
    def do_set_title(title: str) -> None:
        """Set the title of the RAMSTKBasePanel parent view.

        :param title: the title to set.
        """
        pub.sendMessage(
            "request_set_title",
            title=title,
        )
