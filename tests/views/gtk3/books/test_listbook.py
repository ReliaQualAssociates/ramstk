# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.books.test_listbook.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 basebook list algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.books import RAMSTKListBook
from ramstk.views.gtk3.widgets import RAMSTKBook


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKListBook():
    """Test class for the RAMSTKBook."""
    @pytest.mark.gui
    def test_create_listbook(self, test_toml_user_configuration):
        """__init__() should create a RAMSTKListBook."""
        DUT = RAMSTKListBook(
            test_toml_user_configuration,
            RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG))

        # Did it inherit from the RAMSTKBook?
        assert isinstance(DUT, RAMSTKBook)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT.dic_books, dict)
        assert DUT.dic_tab_position['left'] == Gtk.PositionType.LEFT
        assert DUT.dic_tab_position['right'] == Gtk.PositionType.RIGHT
        assert DUT.dic_tab_position['top'] == Gtk.PositionType.TOP
        assert DUT.dic_tab_position['bottom'] == Gtk.PositionType.BOTTOM
        assert isinstance(DUT.menubar, Gtk.MenuBar)
        assert isinstance(DUT.notebook, Gtk.Notebook)
        assert isinstance(DUT.progressbar, Gtk.ProgressBar)
        assert isinstance(DUT.statusbar, Gtk.Statusbar)
        assert isinstance(DUT.toolbar, Gtk.Toolbar)
        assert DUT.get_property('border-width') == 5
        assert DUT.get_resizable()
        assert pub.isSubscribed(DUT._on_request_open, 'request_open_program ')

        # RAMSTKListBook specific.
        assert isinstance(DUT, RAMSTKListBook)
        assert DUT.dic_books['listbook'] == DUT
        assert isinstance(DUT._dic_list_views, dict)
        assert len(DUT._lst_handler_id) == 0
        assert pub.isSubscribed(DUT._on_module_change, 'mvwSwitchedPage')
        assert pub.isSubscribed(DUT._on_close, 'succeed_closed_program')
