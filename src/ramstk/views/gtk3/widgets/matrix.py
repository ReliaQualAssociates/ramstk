# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.matrix.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMatrixView Module."""


# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, GObject, Gtk, _

# RAMSTK Local Imports
from .combo import RAMSTKComboBox
from .label import RAMSTKLabel


class RAMSTKMatrixView(Gtk.Grid):
    """The RAMSTKMatrixView class."""

    def __init__(self) -> None:
        """Initialize a RAMSTKMatrixView() instance.

        :return: None
        :rtype: None
        """
        # noinspection PyCallByClass,PyTypeChecker
        Gtk.Grid.__init__(self)
        GObject.GObject.__init__(self)

        # Initialize private dictionary instance attributes:

        # Initialize private list instance attributes:

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.column_id_dic: Dict[str, int] = {}
        self.icons_dic = {"complete": "", "none": "", "partial": ""}
        self.row_id_dic: Dict[str, int] = {}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.n_columns = 0
        self.n_rows = 0

    def do_add_column(self, heading_str: str, tooltip_str: str) -> None:
        """Add a column to the RAMSTKMatrixView().

        :param heading_str: the text to display as the heading for the new column.
        :param tooltip_str: the tooltip for the new column's header widget.
        :return: None
        :rtype: None
        """
        self.insert_column(self.n_columns + 1)

        self._do_add_widgets(
            (self.n_columns + 1, 0),
            self.n_rows,
            heading_str,
            tooltip_str,
            row_flag=False,
        )

        self.n_columns += 1

    def do_add_row(self, heading_str: str, tooltip_str: str) -> None:
        """Add a row to the RAMSTKMatrixView().

        :param heading_str: the text to display as the heading for the new row.
        :param tooltip_str: the tooltip for the new row's header widget.
        :return: None
        :rtype: None
        """
        self.insert_row(self.n_rows + 1)

        self._do_add_widgets(
            (0, self.n_rows + 1),
            self.n_columns,
            heading_str,
            tooltip_str,
        )

        self.n_rows += 1

    def do_remove_column(self, position_idx: int) -> None:
        """Remove the RAMSTKMatrixView() column at position_idx.

        :param position_idx: the column position to remove.
        :return: None
        :rtype: None
        """
        self.remove_column(position_idx)

        self.n_columns -= 1

    def do_remove_row(self, position_idx: int) -> None:
        """Remove the RAMSTKMatrixView() row at position_idx.

        :param position_idx: the row position to remove.
        :return: None
        :rtype: None
        """
        self.remove_row(position_idx)

        self.n_rows -= 1

    def do_set_column_headings(
        self,
        column_name_lst: List[Tuple[str, str, int]],
    ) -> None:
        """Load the RAMSTKMatrixView() column headings for each column.

        The tuples in the list passed to this method should contain a code, a
        description for the row element, and a database ID for the element displayed
        in the row.  For example, a requirement might be:

            ("RELI-0001", "The widget shall have an MTBF >= 1000 hours.", 5)

        The code (position 0) is the displayed value and the description (position 1)
        becomes the tooltip.

        :param column_name_lst: a list of tuples with the name and description of the
            items to use as the column heading and the tooltip.
        :return: None
        :rtype: None
        """
        self.n_columns = 0

        for _column_name_tpl in column_name_lst:
            self.do_add_column(_column_name_tpl[0], _column_name_tpl[1])
            self.column_id_dic[_column_name_tpl[0]] = _column_name_tpl[2]

        self.n_rows = 1

    def do_set_row_headings(
        self,
        row_name_lst: List[Tuple[str, str, int]],
    ) -> None:
        """Load the RAMSTKMatrixView() row headings for each row.

        A row of data in a matrix is a list or tuple with the first entry being the
        row heading.  The remaining entries will be a 0, 1, or 2 and there will be
        one entry for each column in the matrix.

        The tuples in the list passed to this method should contain a code, a
        description for the row element, and a database ID for the element displayed
        in the row.  For example, a verification task might be:

            ("RELI-0001", "Perform reliability prediction for PDR.", 14)

        The code (position 0) is the displayed value and the description (position 1)
        becomes the tooltip.

        :param row_name_lst: a list of tuples with the name and description of the
            items to use as the row heading and the tooltip.
        :return: None
        :rtype: None
        """
        self.n_rows = 0

        for _row_name_tpl in row_name_lst:
            self.do_add_row(_row_name_tpl[0], _row_name_tpl[1])
            self.row_id_dic[_row_name_tpl[0]] = _row_name_tpl[2]

        self.n_columns = 1

    def _do_add_widgets(
        self,
        position_tpl: Tuple[int, int],
        n_positions_int: int,
        heading_str: str,
        tooltip_str: str,
        row_flag: bool = True,
    ) -> None:
        """Add either a column or row to the RAMSTKMatrixView().

        :param position_tpl: the column number and row number to attach the left
            side and top side respectively of new widgets to.
        :param n_positions_int: the number of columns or rows in the RAMSTKMatrixView().
        :param heading_str: the text to display as the heading for the new column/row.
        :param tooltip_str: the tooltip for the new column's/row's header widget.
        :param row_flag: indicates whether to insert a column or a row (default).
        :return: None
        :rtype: None
        """
        _label_obj = RAMSTKLabel(heading_str)
        _label_obj.do_set_properties(
            angle=90,
            can_focus=False,
            tooltip=tooltip_str,
            wrap=False,
        )
        self.attach(_label_obj, position_tpl[0], position_tpl[1], 1, 1)

        for _add_idx in range(n_positions_int - 1):
            _combo_obj = self._do_make_combobox()
            if row_flag:
                self.attach(_combo_obj, _add_idx + 1, position_tpl[1], 1, 1)
            else:
                self.attach(_combo_obj, position_tpl[0], _add_idx + 1, 1, 1)
                _label_obj.set_angle(90.0)

    def _do_make_combobox(self) -> RAMSTKComboBox:
        """Create a RAMSTKComboBox() to display the relationship results for a cell.

        :return: _combo_obj; the RAMSTKComboBox() created by this method.
        :rtype: :class:`RAMSTKComboBox()`
        """
        _combo_obj = RAMSTKComboBox(1)
        _model_obj = Gtk.ListStore(*[GObject.TYPE_STRING, GdkPixbuf.Pixbuf])
        for _option_idx, _pixbuf_key_str in enumerate(self.icons_dic):
            _pixbuf_obj = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.icons_dic[_pixbuf_key_str], 22, 22
            )
            _model_obj.append(
                [["", "Partial", "Complete"][_option_idx], _pixbuf_obj],
            )
        _combo_obj.set_model(_model_obj)
        _combo_obj.do_set_properties(
            tooltip=_(
                "Shows the strength of the relationship between the intersecting "
                "column and row with a blank meaning no relationship, a P meaning "
                "partial, and a C meaning complete."
            ),
            width=35,
        )
        _cell_obj = Gtk.CellRendererPixbuf()
        _combo_obj.pack_start(_cell_obj, True)
        _combo_obj.add_attribute(_cell_obj, "pixbuf", 1)

        return _combo_obj


# Register the new widget types.
GObject.type_register(RAMSTKMatrixView)
