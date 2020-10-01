# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_button.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 button module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import (
    RAMSTKButton, RAMSTKCheckButton, RAMSTKOptionButton
)


class TestRAMSTKButton():
    """Test class for the RAMSTKButton."""
    @pytest.mark.gui
    def test_create_button(self):
        """__init__() should create a RAMSTKButton."""
        DUT = RAMSTKButton(label="Test Button")

        assert isinstance(DUT, RAMSTKButton)
        assert DUT.get_label() == "Test Button"
        assert DUT.get_image() is None
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1

    @pytest.mark.gui
    def test_set_properties(self):
        """do_set_properties() should set the properties of a RAMSTKButton."""
        DUT = RAMSTKButton(label="Test Button")
        DUT.do_set_properties(height=20, width=150, tooltip="Test tooltip")

        assert DUT.get_property('height-request') == 20
        assert DUT.get_property('tooltip-markup') == "Test tooltip"
        assert DUT.get_property('width-request') == 150

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKButton when no keywords are passed to the method."""
        DUT = RAMSTKButton(label="Test Button")
        DUT.do_set_properties()

        assert DUT.get_property('height-request') == 30
        assert DUT.get_property('image') is None
        assert DUT.get_property('tooltip-markup') == (
            "Missing tooltip, please file a quality type issue to have one "
            "added.")
        assert DUT.get_property('width-request') == 200

    @pytest.mark.gui
    def test_set_properties_zero_height(self):
        """do_set_properties() should set the height to the default value if it is passed as zero.."""
        DUT = RAMSTKButton(label="Test Button")
        DUT.do_set_properties(height=0)

        assert DUT.get_property('height-request') == 30

    @pytest.mark.gui
    def test_set_properties_zero_width(self):
        """do_set_properties() should set the width to the default value if it is passed as zero.."""
        DUT = RAMSTKButton(label="Test Button")
        DUT.do_set_properties(width=0)

        assert DUT.get_property('width-request') == 200


class TestRAMSTKCheckButton():
    """Test class for the RAMSTKCheckButton."""
    @pytest.mark.gui
    def test_create_button(self):
        """__init__() should create a RAMSTKCheckButton."""
        DUT = RAMSTKCheckButton(label="Test Check Button")

        assert isinstance(DUT, RAMSTKCheckButton)
        assert isinstance(DUT.get_child(), Gtk.Label)
        assert DUT.get_label() == "Test Check Button"
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1

    @pytest.mark.gui
    def test_set_properties(self):
        """do_set_properties() should set the properties of a RAMSTKCheckButton."""
        DUT = RAMSTKCheckButton(label="Test Check Button")
        DUT.do_set_properties(height=20, width=150, tooltip="Test tooltip")

        assert DUT.get_child().get_property('height-request') == 20
        assert DUT.get_property('tooltip-markup') == "Test tooltip"
        assert DUT.get_child().get_property('width-request') == 150
        assert DUT.get_use_underline()

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKCheckButton when no keywords are passed to the method."""
        DUT = RAMSTKCheckButton(label="Test Check Button")
        DUT.do_set_properties()

        assert DUT.get_child().get_property('height-request') == 40
        assert DUT.get_property('tooltip-markup') == (
            "Missing tooltip, please file a quality type issue to have one "
            "added.")
        assert DUT.get_child().get_property('width-request') == 200

    @pytest.mark.gui
    def test_set_properties_zero_height(self):
        """do_set_properties() should set the height to the default value if it is passed as zero.."""
        DUT = RAMSTKCheckButton(label="Test Check Button")
        DUT.do_set_properties(height=0)

        assert DUT.get_child().get_property('height-request') == 40

    @pytest.mark.gui
    def test_set_properties_zero_width(self):
        """do_set_properties() should set the width to the default value if it is passed as zero.."""
        DUT = RAMSTKCheckButton(label="Test Check Button")
        DUT.do_set_properties(width=0)

        assert DUT.get_child().get_property('width-request') == 200


class TestRAMSTKOptionButton():
    """Test class for the RAMSTKOptionButton."""
    @pytest.mark.gui
    def test_create_button(self):
        """__init__() should create a RAMSTKOptionButton."""
        DUT = RAMSTKOptionButton(label="Test Option Button")

        assert isinstance(DUT, RAMSTKOptionButton)
        assert DUT.get_label() == "Test Option Button"
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1
