# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_baseview.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 baseview module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import RAMSTKBaseView, RAMSTKMessageDialog


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestRAMSTKBaseView:
    """Test class for the RAMSTKBaseView."""

    @pytest.mark.skip
    def test_create_baseview(self, test_toml_user_configuration):
        """__init__() should create a RAMSTKBaseView."""
        _logger = RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG)
        DUT = RAMSTKBaseView(test_toml_user_configuration, _logger)
        DUT._module = "revision"

        assert isinstance(DUT, RAMSTKBaseView)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION, RAMSTKUserConfiguration)
        assert DUT.dic_tab_position["left"] == Gtk.PositionType.LEFT
        assert DUT.dic_tab_position["right"] == Gtk.PositionType.RIGHT
        assert DUT.dic_tab_position["top"] == Gtk.PositionType.TOP
        assert DUT.dic_tab_position["bottom"] == Gtk.PositionType.BOTTOM
        assert isinstance(DUT._lst_col_order, list)
        # assert DUT._mission_time == 100.0
        assert isinstance(DUT._notebook, Gtk.Notebook)
        assert DUT._revision_id == 0
        assert DUT._parent_id == 0
        assert isinstance(DUT.treeview, Gtk.TreeView)
        # assert DUT.fmt == '{0:0.4G}'
        assert isinstance(DUT.hbx_tab_label, Gtk.HBox)
        pub.isSubscribed(DUT.on_select_revision, "selected_revision")

    @pytest.mark.skip
    def test_do_raise_dialog_missing_severity(self, test_toml_user_configuration):
        """do_raise_dialog() should log a message to the debug log when the severity is missing from the kwargs."""
        _logger = RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG)
        test_toml_user_configuration.RAMSTK_LOGLEVEL = "DEBUG"
        DUT = RAMSTKBaseView(test_toml_user_configuration, _logger)
        DUT._module = "revision"

        assert isinstance(
            DUT.do_raise_dialog(
                error_code=1,
                user_msg="This is a test user message.",
                debug_msg="This is a test debug message.",
            ),
            RAMSTKMessageDialog,
        )

    @pytest.mark.skip
    def test_do_raise_dialog_missing_message(self, test_toml_user_configuration):
        """do_raise_dialog() should log a message to the debug log when the message is missing from the kwargs."""
        _logger = RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG)
        test_toml_user_configuration.RAMSTK_LOGLEVEL = "DEBUG"
        DUT = RAMSTKBaseView(test_toml_user_configuration, _logger)
        DUT._module = "revision"

        assert isinstance(
            DUT.do_raise_dialog(
                error_code=1,
                severity="error",
                debug_msg="This is a test debug message.",
            ),
            RAMSTKMessageDialog,
        )
