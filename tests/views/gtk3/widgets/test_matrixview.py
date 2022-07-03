# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_matrixview.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 matrixview module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKLabel, RAMSTKMatrixView


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestRAMSTKMatrixView:
    """Test class for the RAMSTKMatrixView."""

    @pytest.mark.unit
    def test_create_matrixview(self):
        """Should create a RAMSTKMatrixView."""
        dut = RAMSTKMatrixView()

        assert isinstance(dut, RAMSTKMatrixView)
        assert dut.column_id_dic == {}
        assert dut.icons_dic == {"complete": "", "none": "", "partial": ""}
        assert dut.row_id_dic == {}
        assert dut.n_columns == 0
        assert dut.n_rows == 0

    @pytest.mark.unit
    def test_do_add_column(self):
        """Should add a column to the RAMSTKMatrixView."""
        dut = RAMSTKMatrixView()

        assert dut.n_columns == 0

        dut.do_add_column("Test Column Header", "Test Column Tooltip")
        _label_obj = dut.get_child_at(1, 0)

        assert dut.n_columns == 1
        assert isinstance(_label_obj, RAMSTKLabel)
        assert _label_obj.get_label() == "<b><span>Test Column Header</span></b>"
        assert _label_obj.get_property("tooltip-markup") == "Test Column Tooltip"

    @pytest.mark.unit
    def test_do_add_row(self):
        """Should add a row to the RAMSTKMatrixView."""
        dut = RAMSTKMatrixView()

        assert dut.n_columns == 0

        dut.do_add_row("Test Row Header", "Test Row Tooltip")
        _label_obj = dut.get_child_at(0, 1)

        assert dut.n_rows == 1
        assert isinstance(_label_obj, RAMSTKLabel)
        assert _label_obj.get_label() == "<b><span>Test Row Header</span></b>"
        assert _label_obj.get_property("tooltip-markup") == "Test Row Tooltip"

    @pytest.mark.unit
    def test_do_remove_column(self):
        """Should remove a column from the RAMSTKMatrixView."""
        dut = RAMSTKMatrixView()

        assert dut.n_columns == 0

        dut.do_add_column("", "")
        dut.do_add_column("", "")

        _label_obj = [dut.get_child_at(1, 0), dut.get_child_at(2, 0)]

        assert dut.n_columns == 2
        assert isinstance(_label_obj[0], RAMSTKLabel)
        assert isinstance(_label_obj[1], RAMSTKLabel)

        dut.do_remove_column(1)

        assert dut.n_columns == 1
        assert isinstance(dut.get_child_at(1, 0), RAMSTKLabel)
        assert not isinstance(dut.get_child_at(2, 0), RAMSTKLabel)

    @pytest.mark.unit
    def test_do_remove_row(self):
        """Should remove a row from the RAMSTKMatrixView."""
        dut = RAMSTKMatrixView()

        assert dut.n_columns == 0

        dut.do_add_row("", "")
        dut.do_add_row("", "")

        _label_lst = [
            dut.get_child_at(0, 1),
            dut.get_child_at(0, 2),
        ]

        assert dut.n_rows == 2
        assert isinstance(_label_lst[0], RAMSTKLabel)
        assert isinstance(_label_lst[1], RAMSTKLabel)

        dut.do_remove_row(1)

        assert dut.n_rows == 1
        assert isinstance(dut.get_child_at(0, 1), RAMSTKLabel)
        assert not isinstance(dut.get_child_at(0, 2), RAMSTKLabel)

    @pytest.mark.unit
    def test_do_set_column_headings(self):
        """Should add a row and populate with column heading RAMSTKLabels."""
        dut = RAMSTKMatrixView()

        assert dut.column_id_dic == {}
        assert dut.n_columns == 0
        assert dut.n_rows == 0

        dut.do_set_column_headings(
            [
                ("Column 1", "Tooltip 1", 12),
                ("Column 2", "Tooltip 2", 28),
                ("Column 3", "Tooltip 3", 3),
            ],
        )

        _label_lst = [
            dut.get_child_at(1, 0),
            dut.get_child_at(2, 0),
            dut.get_child_at(3, 0),
        ]

        assert dut.column_id_dic["Column 1"] == 12
        assert dut.column_id_dic["Column 2"] == 28
        assert dut.column_id_dic["Column 3"] == 3
        assert dut.n_columns == 3
        assert dut.n_rows == 1
        assert isinstance(_label_lst[0], RAMSTKLabel)
        assert _label_lst[0].get_label() == "<b><span>Column 1</span></b>"
        assert _label_lst[0].get_property("tooltip-markup") == "Tooltip 1"
        assert isinstance(_label_lst[1], RAMSTKLabel)
        assert _label_lst[1].get_label() == "<b><span>Column 2</span></b>"
        assert _label_lst[1].get_property("tooltip-markup") == "Tooltip 2"
        assert isinstance(_label_lst[2], RAMSTKLabel)
        assert _label_lst[2].get_label() == "<b><span>Column 3</span></b>"
        assert _label_lst[2].get_property("tooltip-markup") == "Tooltip 3"

    @pytest.mark.unit
    def test_do_set_row_headings(self):
        """Should add a column and populate with row heading RAMSTKLabels."""
        dut = RAMSTKMatrixView()

        assert dut.n_columns == 0
        assert dut.n_rows == 0
        assert dut.row_id_dic == {}

        dut.do_set_row_headings(
            [
                ("Row 1", "Tooltip 1", 4),
                ("Row 2", "Tooltip 2", 8),
                ("Row 3", "Tooltip 3", 12),
            ],
        )

        _label_lst = [
            dut.get_child_at(0, 1),
            dut.get_child_at(0, 2),
            dut.get_child_at(0, 3),
        ]

        assert dut.n_columns == 1
        assert dut.n_rows == 3
        assert dut.row_id_dic["Row 1"] == 4
        assert dut.row_id_dic["Row 2"] == 8
        assert dut.row_id_dic["Row 3"] == 12
        assert isinstance(_label_lst[0], RAMSTKLabel)
        assert _label_lst[0].get_label() == "<b><span>Row 1</span></b>"
        assert _label_lst[0].get_property("tooltip-markup") == "Tooltip 1"
        assert isinstance(_label_lst[1], RAMSTKLabel)
        assert _label_lst[1].get_label() == "<b><span>Row 2</span></b>"
        assert _label_lst[1].get_property("tooltip-markup") == "Tooltip 2"
        assert isinstance(_label_lst[2], RAMSTKLabel)
        assert _label_lst[2].get_label() == "<b><span>Row 3</span></b>"
        assert _label_lst[2].get_property("tooltip-markup") == "Tooltip 3"

    @pytest.mark.unit
    def test_do_build_matrix(self, test_toml_user_configuration):
        """Should build a 3 row by 3 column matrix."""
        dut = RAMSTKMatrixView()
        for _icon_str in ["none", "partial", "complete"]:
            dut.icons_dic[
                _icon_str
            ] = f"{test_toml_user_configuration.RAMSTK_ICON_DIR}/32x32/{_icon_str}.png"

        assert dut.n_columns == 0
        assert dut.n_rows == 0

        dut.do_set_column_headings(
            [
                ("Column 1", "Column Tooltip 1", 12),
                ("Column 2", "Column Tooltip 2", 28),
                ("Column 3", "Column Tooltip 3", 3),
            ],
        )
        dut.do_set_row_headings(
            [
                ("Row 1", "Row Tooltip 1", 4),
                ("Row 2", "Row Tooltip 2", 8),
                ("Row 3", "Row Tooltip 3", 12),
            ],
        )

        _label_lst = [
            dut.get_child_at(1, 0),
            dut.get_child_at(2, 0),
            dut.get_child_at(3, 0),
            dut.get_child_at(0, 1),
            dut.get_child_at(0, 2),
            dut.get_child_at(0, 3),
        ]

        assert isinstance(_label_lst[0], RAMSTKLabel)
        assert _label_lst[0].get_label() == "<b><span>Column 1</span></b>"
        assert _label_lst[0].get_property("tooltip-markup") == "Column Tooltip 1"
        assert isinstance(_label_lst[1], RAMSTKLabel)
        assert _label_lst[1].get_label() == "<b><span>Column 2</span></b>"
        assert _label_lst[1].get_property("tooltip-markup") == "Column Tooltip 2"
        assert isinstance(_label_lst[2], RAMSTKLabel)
        assert _label_lst[2].get_label() == "<b><span>Column 3</span></b>"
        assert _label_lst[2].get_property("tooltip-markup") == "Column Tooltip 3"
        assert isinstance(_label_lst[3], RAMSTKLabel)
        assert _label_lst[3].get_label() == "<b><span>Row 1</span></b>"
        assert _label_lst[3].get_property("tooltip-markup") == "Row Tooltip 1"
        assert isinstance(_label_lst[4], RAMSTKLabel)
        assert _label_lst[4].get_label() == "<b><span>Row 2</span></b>"
        assert _label_lst[4].get_property("tooltip-markup") == "Row Tooltip 2"
        assert isinstance(_label_lst[5], RAMSTKLabel)
        assert _label_lst[5].get_label() == "<b><span>Row 3</span></b>"
        assert _label_lst[5].get_property("tooltip-markup") == "Row Tooltip 3"

        _combo_lst = [
            dut.get_child_at(1, 1),
            dut.get_child_at(2, 1),
            dut.get_child_at(1, 2),
            dut.get_child_at(2, 2),
        ]

        assert isinstance(_combo_lst[0], RAMSTKComboBox)
        assert isinstance(_combo_lst[1], RAMSTKComboBox)
        assert isinstance(_combo_lst[2], RAMSTKComboBox)
        assert isinstance(_combo_lst[3], RAMSTKComboBox)
        assert _combo_lst[0].get_property("tooltip-markup") == (
            "Shows the strength of the relationship between the intersecting column "
            "and row with a blank meaning no relationship, a P meaning partial, and a "
            "C meaning complete."
        )
        assert isinstance(_combo_lst[1].get_model(), Gtk.ListStore)

        _row_obj = _combo_lst[2].get_model().get_iter_first()

        assert _combo_lst[2].get_model().get_value(_row_obj, 0) == ""
        assert isinstance(
            _combo_lst[2].get_model().get_value(_row_obj, 1), GdkPixbuf.Pixbuf
        )
