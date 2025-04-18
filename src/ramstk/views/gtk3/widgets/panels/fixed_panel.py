# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panels.fixed_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Fixed Panel Class."""


# Standard Library Imports
from datetime import date
from typing import Dict, List, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets.buttons import RAMSTKCheckButton

# RAMSTK Local Imports
from ..entry import RAMSTKTextView
from ..label import RAMSTKLabel, do_make_label_group
from ..scrolledwindow import RAMSTKScrolledWindow
from ..widget import RAMSTKBaseWidget
from . import RAMSTKBasePanel

COLUMN_WIDTH = 300
MARGIN = 5
LABEL_SPACING = 30


class RAMSTKFixedPanel(RAMSTKBasePanel):
    """The RAMSTKFixedPanel class."""

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKFixedPanel widget."""
        super().__init__()

        # Initialize private instance attributes.
        self._dic_widget_field_map: Dict[str, RAMSTKBaseWidget] = {}
        self.fixed = Gtk.Fixed()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_clear_views": self.do_clear_fixed_panel,
                f"selected_{self._tag}": self.do_load_fixed_panel,
                f"succeed_get_{self._tag}_attributes": self.do_load_fixed_panel,
            }
        )

    def do_clear_fixed_panel(self) -> None:
        """Clear the contents of the widgets on a RAMSTKFixedPanel."""
        for _widget in self._lst_widget_configuration:
            _widget["widget"].do_update(_widget["widget"].default)

    def do_load_fixed_panel(
        self,
        attributes: Dict[str, Union[bool, date, float, int, str]],
    ) -> None:
        """Load data into the widgets on a RAMSTKFixedPanel.

        :param attributes: the attribute dict for the selected record.
        """
        self._record_id = int(attributes[self._record_field])  # type: ignore[arg-type]
        for _widget in self._lst_widget_configuration:
            _widget["widget"].record_id = self._record_id
            _widget["widget"].do_update(
                {_widget["widget"].field: attributes[_widget["widget"].field]}
            )

        pub.sendMessage("request_set_cursor_active")

    def do_make_fixed_panel(
        self, justify: Gtk.Justification = Gtk.Justification.RIGHT, n_columns: int = 1
    ) -> None:
        """Create a panel with the labels and widgets on a Gtk.Fixed.

        :param justify: the Gtk.Justification for the RAMSTKLabels that will be placed
            on the RAMSTKFixedPanel.
        :param n_columns: the number of columns to place widgets and associated labels
            on the RAMSTKFixedPanel
        """
        # Update the dictionary mapping each widget to its field index.
        for _widget in self._lst_widget_configuration:
            self._dic_widget_field_map[_widget["attributes"]["field"]] = _widget[
                "widget"
            ]

        for _column in range(n_columns):
            self._do_create_widgets_for_column(
                _column,
                justify,
            )

        self.add(RAMSTKScrolledWindow(self.fixed))

    def _do_create_widgets_for_column(
        self,
        column: int,
        __justify: Gtk.Justification,
    ):
        """Extract the widget configurations for the RAMSTKFixedPanel column.

        :param column: the column number where the widgets will be placed on the
            RAMSTKFixedPanel.
        :param __justify: the Gtk.Justification for the RAMSTKLabels associated with the
            column widgets.
        """
        # fmt: off
        _column_labels: List[str] = [
            str(_widget["attributes"]["label_text"])
            for _widget in self._lst_widget_configuration
        ][column:]
        _column_widgets: List[RAMSTKBaseWidget] = [
            _widget["widget"] for _widget in self._lst_widget_configuration
        ][column:]
        _lst_attributes = [
            _widget["attributes"] for _widget in self._lst_widget_configuration
        ][column:]
        _lst_properties = [
            _widget["properties"] for _widget in self._lst_widget_configuration
        ][column:]
        # fmt: on

        # for _attribute in _lst_attributes:
        #    _attribute["x_pos"] = column * COLUMN_WIDTH + MARGIN
        #    _attribute["y_pos"] = MARGIN

        # for _property in _lst_properties:
        #    _property["bold"] = True
        #    _property["justify"] = justify
        #    _property["wrap"] = True

        _x_pos, _labels = do_make_label_group(
            _column_labels,
        )
        return self._do_place_widgets(
            [column * COLUMN_WIDTH + MARGIN, _x_pos],
            _labels,
            _column_widgets,
        )

    def _do_place_widgets(
        self,
        x_pos: List[int],
        labels: List[RAMSTKLabel],
        widgets: List[RAMSTKBaseWidget],
    ) -> None:
        """Place the widgets and their associated labels on the RAMSTKFixedPanel.

        :param x_pos: the x-coordinate position to place the RAMSTLabel objects.
        :param labels: the list of RAMSTKLabel objects to place.
        :param widgets: the list of RAMSTKBaseWidget objects to place.
        """
        _y_pos: int = MARGIN

        for _label, _widget in zip(labels, widgets):
            self.fixed.put(_label, x_pos[0], _y_pos)

            _minimum_height = max(
                _widget.get_preferred_size()[0].height or _widget.height,  # type: ignore[attr-defined] # noqa
                0,
            )

            # Place widgets while handling special cases
            _widget_to_place = (
                _widget.scrollwindow if isinstance(_widget, RAMSTKTextView) else _widget
            )
            self.fixed.put(_widget_to_place, x_pos[1] + 10, _y_pos)

            _y_pos += _minimum_height + (
                LABEL_SPACING
                if isinstance(_widget, (RAMSTKTextView, RAMSTKCheckButton))
                else MARGIN
            )
