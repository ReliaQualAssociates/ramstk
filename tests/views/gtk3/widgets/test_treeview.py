# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_treeview.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 treeview module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3.widgets import RAMSTKTreeView


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKTreeView():
    """Test class for the RAMSTKTreeView."""
    @pytest.mark.gui
    def test_create_treeview(self):
        """__init__() should create a RAMSTKTreeView."""
        DUT = RAMSTKTreeView()

        assert isinstance(DUT, RAMSTKTreeView)
        assert DUT.datatypes == []
        assert DUT.editable == []
        assert DUT.headings == []
        assert DUT.korder == []
        assert DUT.order == []
        assert DUT.visible == []
        assert DUT.widgets == []
        assert DUT.pixbuf_col == -1
        assert DUT.index_col == 0
