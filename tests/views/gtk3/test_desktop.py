# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_basebook.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 basebook module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, RAMSTKDesktop
from ramstk.views.gtk3.books import (
    RAMSTKListBook, RAMSTKModuleBook, RAMSTKWorkBook
)


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestRAMSTKBook():
    """Test class for the RAMSTKBook."""
    @pytest.mark.gui
    def test_create_basebook(self, test_toml_user_configuration,
                             test_toml_site_configuration):
        """__init__() should create a RAMSTKBook."""
        test_toml_user_configuration.RAMSTK_AFFINITY_GROUPS = \
            test_toml_site_configuration.RAMSTK_AFFINITY_GROUPS
        test_toml_user_configuration.RAMSTK_REQUIREMENT_TYPE = \
            test_toml_site_configuration.RAMSTK_REQUIREMENT_TYPE
        test_toml_user_configuration.RAMSTK_STAKEHOLDERS = \
            test_toml_site_configuration.RAMSTK_STAKEHOLDERS
        test_toml_user_configuration.RAMSTK_WORKGROUPS = \
            test_toml_site_configuration.RAMSTK_WORKGROUPS
        test_toml_user_configuration.RAMSTK_VALIDATION_TYPE = \
            test_toml_site_configuration.RAMSTK_VALIDATION_TYPE
        test_toml_user_configuration.RAMSTK_MEASUREMENT_UNITS = \
            test_toml_site_configuration.RAMSTK_MEASUREMENT_UNITS

        DUT = RAMSTKDesktop(
            [test_toml_user_configuration, test_toml_site_configuration],
            RAMSTKLogManager(test_toml_user_configuration.RAMSTK_USER_LOG))

        assert isinstance(DUT, RAMSTKDesktop)
        assert isinstance(DUT.RAMSTK_USER_CONFIGURATION,
                          RAMSTKUserConfiguration)
        assert isinstance(DUT.menubar, Gtk.MenuBar)
        assert isinstance(DUT.nbkListBook, RAMSTKListBook)
        assert isinstance(DUT.nbkModuleBook, RAMSTKModuleBook)
        assert isinstance(DUT.nbkWorkBook, RAMSTKWorkBook)
        assert isinstance(DUT.progressbar, Gtk.ProgressBar)
        assert isinstance(DUT.statusbar, Gtk.Statusbar)
        assert isinstance(DUT.toolbar, Gtk.Toolbar)
        assert DUT.get_property('border-width') == 5
        assert DUT.get_resizable()
        assert pub.isSubscribed(DUT._on_request_open, 'request_open_program ')
