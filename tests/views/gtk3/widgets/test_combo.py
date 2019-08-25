# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_combo.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 combo module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject
from ramstk.views.gtk3.widgets import RAMSTKComboBox


class TestRAMSTKComboBox():
    """Test class for the RAMSTKComboBox."""
    @pytest.mark.gui
    def test_create_entry(self):
        """__init__() should create a RAMSTKEntry."""
        DUT = RAMSTKComboBox()

        assert isinstance(DUT, RAMSTKComboBox)
        assert DUT._index == 0
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1
        assert DUT.get_model().get_n_columns() == 1
        assert DUT.get_model().get_column_type(0) == GObject.TYPE_STRING

    @pytest.mark.gui
    def test_create_combobox_not_simple(self):
        """__init__() should create a RAMSTKComboBox with three columns when passed simple=False."""
        DUT = RAMSTKComboBox(index=2, simple=False)

        assert isinstance(DUT, RAMSTKComboBox)
        assert DUT._index == 2
        assert DUT.get_property('height-request') == -1
        assert DUT.get_property('width-request') == -1
        assert DUT.get_model().get_n_columns() == 3
        assert DUT.get_model().get_column_type(0) == GObject.TYPE_STRING
        assert DUT.get_model().get_column_type(1) == GObject.TYPE_STRING
        assert DUT.get_model().get_column_type(2) == GObject.TYPE_STRING

    @pytest.mark.gui
    def test_set_properties(self):
        """do_set_properties() should set the properties of a RAMSTKComboBox."""
        DUT = RAMSTKComboBox()
        DUT.do_set_properties(height=70, width=150, tooltip="Test tooltip")

        assert DUT.get_property('height-request') == 70
        assert DUT.get_property('tooltip-markup') == "Test tooltip"
        assert DUT.get_property('width-request') == 150

    @pytest.mark.gui
    def test_set_properties_default_values(self):
        """do_set_properties() should set the default properties of a RAMSTKComboBox when no keywords are passed to the method."""
        DUT = RAMSTKComboBox()
        DUT.do_set_properties()

        assert DUT.get_property('height-request') == 30
        assert DUT.get_property('tooltip-markup') == (
            "Missing tooltip, please file a quality type issue to have one "
            "added.")
        assert DUT.get_property('width-request') == 200

    @pytest.mark.gui
    def test_set_properties_zero_height(self):
        """do_set_properties() should set the height to the default value if it is passed as zero."""
        DUT = RAMSTKComboBox()
        DUT.do_set_properties(height=0)

        assert DUT.get_property('height-request') == 30

    @pytest.mark.gui
    def test_set_properties_zero_width(self):
        """do_set_properties() should set the width to the default value if it is passed as zero."""
        DUT = RAMSTKComboBox()
        DUT.do_set_properties(width=0)

        assert DUT.get_property('width-request') == 200

    @pytest.mark.gui
    def test_do_load_combo_simple(self):
        """do_load_combo() should load a list of string values into a simple RAMSTKComboBox."""
        _test_list = [['This'], ['is'], ['a'], ['test'], ['of'], ['the'], ['RAMSTKComboBox']]
        DUT = RAMSTKComboBox()

        assert DUT.do_load_combo(_test_list) is None

    @pytest.mark.gui
    def test_do_load_combo_not_simple(self):
        """do_load_combo() should load a list of string values into a non-simple RAMSTKComboBox."""
        _test_list = [['This', 'is', 'a'], ['test', 'of', 'the'], ['RAMSTKComboBox', 'not', 'simple']]
        DUT = RAMSTKComboBox(index=1, simple=False)

        assert DUT.do_load_combo(_test_list, simple=False) is None

    @pytest.mark.gui
    def test_do_load_combo_simple_not_string_list(self):
        """do_load_combo() should raise a TypeError when passed a list of other than strings to load or a single non-string value."""
        _test_list = [0, 1, 2, 3, 4]
        DUT = RAMSTKComboBox()

        with pytest.raises(TypeError):
            DUT.do_load_combo(_test_list)
        with pytest.raises(TypeError):
            DUT.do_load_combo(10)

    @pytest.mark.gui
    def test_do_get_options_simple(self):
        """do_get_options() should return a dict of all the options available in a simple RAMSTKComboBox."""
        _test_list = [['This'], ['is'], ['a'], ['test'], ['of'], ['the'], ['RAMSTKComboBox']]
        DUT = RAMSTKComboBox()
        DUT.do_load_combo(_test_list)

        _options = DUT.do_get_options()
        assert isinstance(_options, dict)
        assert _options == {0: '', 1: 'This', 2: 'is', 3: 'a', 4: 'test', 5: 'of', 6: 'the', 7: 'RAMSTKComboBox'}

    @pytest.mark.gui
    def test_do_get_options_not_simple(self):
        """do_load_combo() should load a list of string values into a non-simple RAMSTKComboBox."""
        _test_list = [['This', 'is', 'a'], ['test', 'of', 'the'], ['RAMSTKComboBox', 'not', 'simple']]
        DUT = RAMSTKComboBox(index=1, simple=False)
        DUT.do_load_combo(_test_list, simple=False)

        _options = DUT.do_get_options()
        assert isinstance(_options, dict)
        assert _options == {0: '', 1: 'is', 2: 'of', 3: 'not'}
