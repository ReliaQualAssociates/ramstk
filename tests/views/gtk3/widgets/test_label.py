# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_label.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 label module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, Pango
from ramstk.views.gtk3.widgets import RAMSTKLabel, do_make_label_group


@pytest.mark.gui
def test_do_make_label_group():
    """do_make_label_group() should return the x- and y-positions of a group of labels."""
    _test_labels = ["This", "is", "a", "list", "of", "labels"]
    _x_pos, _y_pos = do_make_label_group(_test_labels, Gtk.Fixed(), 5, 5)

    assert _x_pos == 48
    assert _y_pos == [5, 35, 65, 95, 125, 155]


class TestRAMSTKLabel():
    """Test class for the RAMSTKLabel."""
    @pytest.mark.gui
    def test_create_label(self):
        """__init__() should create a RAMSTKLabel."""
        DUT = RAMSTKLabel("Test Label Text")

        assert isinstance(DUT, RAMSTKLabel)
        assert DUT.get_property('attributes') is None
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('justify') == Gtk.Justification.LEFT
        assert DUT.get_property('label') == "<span>Test Label Text</span>"
        assert DUT.get_property('tooltip-markup') is None
        assert DUT.get_property('width-request') == -1
        assert not DUT.get_property('wrap')
        assert DUT.get_property('wrap-mode') == Pango.WrapMode.WORD

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKLabel when no keywords are passed to the method."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties()

        assert DUT.get_property('height-request') == 25
        assert DUT.get_property('justify') == Gtk.Justification.LEFT
        assert DUT.get_property('label') == (
            "<b><span>Test Label Text</span></b>")
        assert DUT.get_property('tooltip-markup') == (
            "Missing tooltip, please file a quality type issue to have one "
            "added.")
        assert DUT.get_property('width-request') == 190
        assert DUT.get_property('xalign') == pytest.approx(0.05)
        assert DUT.get_property('yalign') == 0.5

    @pytest.mark.gui
    def test_set_properties_centered(self):
        """do_set_properties() should center the RAMSTKLabel."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties(height=70,
                              width=150,
                              tooltip="Test tooltip",
                              justify=Gtk.Justification.CENTER,
                              wrap=True,
                              bold=True)

        assert DUT.get_property('attributes') is None
        assert DUT.get_property('height-request') == 70
        assert DUT.get_property('justify') == Gtk.Justification.CENTER
        assert DUT.get_property('label') == (
            "<b><span>Test Label Text</span></b>")
        assert DUT.get_property('tooltip-markup') == "Test tooltip"
        assert DUT.get_property('width-request') == 150
        assert DUT.get_property('wrap')
        assert DUT.get_property('wrap-mode') == Pango.WrapMode.WORD
        assert DUT.get_property('xalign') == 0.5
        assert DUT.get_property('yalign') == 0.5

    @pytest.mark.gui
    def test_set_properties_left(self):
        """do_set_properties() should left justify the RAMSTKLabel."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties(height=70,
                              width=150,
                              tooltip="Test tooltip",
                              justify=Gtk.Justification.LEFT,
                              wrap=True,
                              bold=False)

        assert DUT.get_property('attributes') is None
        assert DUT.get_property('height-request') == 70
        assert DUT.get_property('justify') == Gtk.Justification.LEFT
        assert DUT.get_property('label') == "<span>Test Label Text</span>"
        assert DUT.get_property('tooltip-markup') == "Test tooltip"
        assert DUT.get_property('width-request') == 150
        assert DUT.get_property('wrap')
        assert DUT.get_property('wrap-mode') == Pango.WrapMode.WORD
        assert DUT.get_property('xalign') == pytest.approx(0.05)
        assert DUT.get_property('yalign') == 0.5

    @pytest.mark.gui
    def test_set_properties_right(self):
        """do_set_properties() should right justify the RAMSTKLabel."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties(height=70,
                              width=150,
                              tooltip="Test tooltip",
                              justify=Gtk.Justification.RIGHT,
                              wrap=True,
                              bold=False)

        assert DUT.get_property('attributes') is None
        assert DUT.get_property('height-request') == 70
        assert DUT.get_property('justify') == Gtk.Justification.RIGHT
        assert DUT.get_property('label') == "<span>Test Label Text</span>"
        assert DUT.get_property('tooltip-markup') == "Test tooltip"
        assert DUT.get_property('width-request') == 150
        assert DUT.get_property('wrap')
        assert DUT.get_property('wrap-mode') == Pango.WrapMode.WORD
        assert DUT.get_property('xalign') == pytest.approx(0.99)
        assert DUT.get_property('yalign') == 0.5

    @pytest.mark.gui
    def test_set_properties_zero_height(self):
        """do_set_properties() should set the height to the default value if passed a height of zero."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties(height=0)

        assert DUT.get_property('height-request') == 25

    @pytest.mark.gui
    def test_set_properties_zero_width(self):
        """do_set_properties() should set the width to the default value if passed a height of zero."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties(width=0)

        assert DUT.get_property('width-request') == 190

    @pytest.mark.gui
    def test_get_attribute_height(self):
        """do_get_attribute() should return the natural height of the RAMSTKLabel."""
        DUT = RAMSTKLabel("Test Label Text")
        DUT.do_set_properties(height=300)

        assert DUT.get_attribute('height') == 300

    @pytest.mark.gui
    def test_get_attribute_width(self):
        """do_get_attribute() should return the natural width of the RAMSTKLabel."""
        DUT = RAMSTKLabel("")
        DUT.do_set_properties(width=30)

        assert DUT.get_attribute('width') == 30
