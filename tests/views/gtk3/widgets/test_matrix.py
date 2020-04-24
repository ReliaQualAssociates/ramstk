# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_matrix.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 matrix module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import RAMSTKMatrixView


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKMatrixView():
    """Test class for the RAMSTKBaseMatrix."""
    @pytest.mark.gui
    def test_create_matrixview(self):
        """__init__() should create a RAMSTKMatrixView."""
        DUT = RAMSTKMatrixView('fnctn_hrdwr')

        assert isinstance(DUT, RAMSTKMatrixView)
        assert isinstance(DUT, Gtk.TreeView)
        assert DUT._matrix_type == 'fnctn_hrdwr'
        assert DUT._n_columns == 0
        assert DUT._n_rows == 0
        assert DUT._revision_id is None
        assert DUT.dic_icons == {}
        assert DUT.matrix is None
        assert DUT.n_fixed_columns == 0
