# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panels.matrix_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Matrix Panel Class."""


# Standard Library Imports
import inspect
from typing import Dict, List, Tuple, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _

# RAMSTK Local Imports
from ..combo import RAMSTKComboBox
from ..matrix import RAMSTKMatrixView
from ..scrolledwindow import RAMSTKScrolledWindow
from . import RAMSTKBasePanel, do_log_message


class RAMSTKMatrixPanel(RAMSTKBasePanel):
    """The RAMSTKMatrixPanel class."""

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKMatrixPanel."""
        super().__init__()

        # Initialize widgets.
        self.grdMatrixView: RAMSTKMatrixView = RAMSTKMatrixView()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_clear_views": self.do_clear_matrix_panel,
            }
        )

    def do_clear_matrix_panel(self) -> None:
        """Clear the contents of the matrix."""
        for _row_idx in range(self.grdMatrixView.n_rows):
            self.grdMatrixView.remove_row(_row_idx)

    def do_load_matrix_panel(
        self,
        attribute_dic: Dict[str, Union[List[int], Tuple[int]]],
    ) -> None:
        """Load data into the widgets on matrix type panel.

        The attribute_dic should use row labels as the key and the value should be a
        list or tuple of integers (0, 1, or 2).

        :param attribute_dic: the attribute dict for the selected item.
        """
        # The first row is for column heading labels.  We skip this row.
        for _row_idx in range(self.grdMatrixView.n_rows - 1):
            _row_label_str = self.grdMatrixView.get_child_at(0, _row_idx + 1).get_text()
            _row_data_obj = attribute_dic[_row_label_str]

            # The first column is for row heading labels.  We skip this row.
            for _column_idx in range(len(_row_data_obj) - 1):
                _combo_obj = self.grdMatrixView.get_child_at(
                    _column_idx + 1,
                    _row_idx + 1,
                )
                _combo_obj.do_load_combo(
                    _row_data_obj,
                )

        pub.sendMessage("request_set_cursor_active")

    def do_make_matrix_panel(self) -> None:
        """Create a panel with an embedded RAMSTKMatrixView()."""
        _scrollwindow_obj: RAMSTKScrolledWindow = RAMSTKScrolledWindow(
            self.grdMatrixView
        )

        self.add(_scrollwindow_obj)

    def do_set_callbacks(self) -> None:
        """Set the callback methods for RAMSTKMatrixView() widgets."""
        for _row_idx in range(self.grdMatrixView.n_rows):
            for _column_idx in range(self.grdMatrixView.n_columns):
                _combo_obj: Gtk.Widget = self.grdMatrixView.do_get_widget(
                    _column_idx,
                    _row_idx,
                )

                if _combo_obj is not None:  # Ensure we don't call .connect() on None
                    _combo_obj.connect("changed", self.on_changed_combo, _combo_obj)

    def on_combo_changed(
        self,
        combo_obj: RAMSTKComboBox,
    ) -> int:
        """Retrieve changes made in RAMSTKComboBox() widgets.

        :param combo_obj: the RAMSTKComboBox() that called the method.
        :return: _combo_idx
        :rtype: int
        """
        try:
            return combo_obj.get_active()
        except (KeyError, ValueError):
            _frame = inspect.currentframe()
            _method_name = _frame.f_code.co_name if _frame else "unknown_method"
            do_log_message(
                _method_name,
                "do_log_debug_msg",
                "DEBUG",
                _(
                    f"An error occurred while editing {self._tag} data for record ID "
                    f"{self._record_id} in the view."
                ),
            )
            return 0
