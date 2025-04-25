# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_widget.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 button module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk
from ramstk.views.gtk3.widgets import (
    RAMSTKBaseWidget,
    WidgetAttributes,
    make_widget_config,
)


class TestWidgetConfig:
    """Test class for the WidgetConfig and make_widget_config function."""

    @pytest.mark.gui
    def test_create_widget_config(self):
        """make_widget_config should create a WidgetConfig."""
        dut = make_widget_config(RAMSTKBaseWidget, {}, {})

        assert dut["attributes"] == {}
        assert dut["properties"] == {}

    @pytest.mark.gui
    def test_create_widget_config_with_attributes(self):
        """make_widget_config should create a WidgetConfig with attributes."""
        dut = make_widget_config(
            RAMSTKBaseWidget,
            {
                "datatype": "gchararray",
                "default": "",
                "field": "test_field",
                "format": "",
                "index": 0,
                "label_text": None,
                "listen_topic": None,
                "record_id": 1,
                "send_topic": None,
                "subscribe": "",
                "x_pos": 0,
                "y_pos": 0,
            },
            {
                "action": Gtk.FileChooserAction.OPEN,
                "activatable": True,
                "adjustment": None,
                "alignment": None,
                "alpha": 255,
                "always_show_image": False,
                "angle": 0.0,
                "background_rgba": None,
                "bg_color": "#FFFFFF",
                "bold": False,
                "buffer": None,
                "can_focus": True,
                "cell_background_rgba": None,
                "cell_foreground_rgba": None,
                "climb_rate": 1.0,
                "destroy_with_parent": True,
                "digits": 2,
                "editable": True,
                "ellipsize": None,
                "enable_grid_lines": Gtk.TreeViewGridLines.BOTH,
            },
        )

        assert dut["attributes"]["datatype"] == "gchararray"
        assert dut["attributes"]["default"] == ""
        assert dut["attributes"]["field"] == "test_field"
        assert dut["attributes"]["format"] == ""
        assert dut["attributes"]["index"] == 0
        assert dut["attributes"]["label_text"] is None
        assert dut["attributes"]["listen_topic"] is None
        assert dut["attributes"]["record_id"] == 1
        assert dut["attributes"]["send_topic"] is None
        assert dut["attributes"]["subscribe"] == ""
        assert dut["attributes"]["x_pos"] == 0
        assert dut["attributes"]["y_pos"] == 0
        assert dut["properties"]["action"] == Gtk.FileChooserAction.OPEN
        assert dut["properties"]["activatable"]
        assert dut["properties"]["adjustment"] is None
        assert dut["properties"]["alignment"] is None
        assert dut["properties"]["alpha"] == 255
        assert dut["properties"]["always_show_image"] is False
        assert dut["properties"]["angle"] == 0.0
        assert dut["properties"]["background_rgba"] is None
        assert dut["properties"]["bg_color"] == "#FFFFFF"
        assert dut["properties"]["bold"] is False
        assert dut["properties"]["buffer"] is None
        assert dut["properties"]["can_focus"]
        assert dut["properties"]["cell_background_rgba"] is None
        assert dut["properties"]["cell_foreground_rgba"] is None
        assert dut["properties"]["climb_rate"] == 1.0
        assert dut["properties"]["destroy_with_parent"]
        assert dut["properties"]["digits"] == 2
        assert dut["properties"]["editable"]
        assert dut["properties"]["ellipsize"] is None
        assert dut["properties"]["enable_grid_lines"] == Gtk.TreeViewGridLines.BOTH


class TestRAMSTKBaseWidget:
    """Test class for the RAMSTKBaseWidget."""

    @pytest.mark.gui
    def test_create_widget(self):
        """__init__() should create a RAMSTKBaseWidget."""
        dut = RAMSTKBaseWidget()

        assert isinstance(dut, RAMSTKBaseWidget)
        assert dut._default_height == -1
        assert dut._default_width == -1
        assert dut._edit_signal == "changed"
        assert dut.dic_handler_id == {}
        assert dut.dic_properties == {
            "can_focus": True,
            "editable": True,
            "height_request": -1,
            "sensitive": True,
            "tooltip": "Missing tooltip, please file a quality type issue to have one "
            "added.",
            "visible": True,
            "width_request": -1,
        }
        assert dut.datatype is None
        assert dut.default is None
        assert dut.field == ""
        assert dut.format == "{}"
        assert dut.height == -1
        assert dut.index == -1
        assert dut.label_text == ""
        assert dut.listen_topic == ""
        assert dut.record_id == -1
        assert dut.send_topic == ""
        assert dut.width == -1
        assert dut.x_pos == 0
        assert dut.y_pos == 0

    @pytest.mark.gui
    def test_widget_do_set_attributes(self):
        """do_set_attributes should set the attributes of a RAMSTKBaseWidget."""
        dut = RAMSTKBaseWidget()
        dut.do_set_attributes(
            WidgetAttributes(
                datatype="gchararray",
                default="",
                field="test_field",
                format="",
                index=0,
                label_text="Test Label",
                listen_topic="",
                record_id=1,
                send_topic="",
                x_pos=0,
                y_pos=0,
            )
        )

        assert isinstance(dut, RAMSTKBaseWidget)
        assert dut.datatype == "gchararray"
        assert dut.default == ""
        assert dut.field == "test_field"
        assert dut.format == ""
        assert dut.index == 0
        assert dut.label_text == "Test Label"
        assert dut.listen_topic == ""
        assert dut.record_id == 1
        assert dut.send_topic == ""
        assert dut.x_pos == 0
        assert dut.y_pos == 0

    @pytest.mark.gui
    def test_widget_do_get_attribute(self):
        """do_get_attribute should return the value of the requested attribute."""
        dut = RAMSTKBaseWidget()
        dut.do_set_attributes(
            WidgetAttributes(
                datatype="gchararray",
                default="",
                field="test_field",
                format="",
                index=0,
                label_text="Test Label",
                listen_topic="",
                record_id=1,
                send_topic="",
                x_pos=0,
                y_pos=0,
            )
        )

        assert isinstance(dut, RAMSTKBaseWidget)
        assert dut.do_get_attribute("datatype") == "gchararray"
        assert dut.do_get_attribute("default") == ""
        assert dut.do_get_attribute("field") == "test_field"
        assert dut.do_get_attribute("format") == ""
        assert dut.do_get_attribute("index") == 0
        assert dut.do_get_attribute("label_text") == "Test Label"
        assert dut.do_get_attribute("listen_topic") == ""
        assert dut.do_get_attribute("record_id") == 1
        assert dut.do_get_attribute("send_topic") == ""
        assert dut.do_get_attribute("x_pos") == 0
        assert dut.do_get_attribute("y_pos") == 0

    @pytest.mark.gui
    def test_widget_do_get_properties(self):
        """do_get_properties should return the properties of a RAMSTKBaseWidget."""
        dut = RAMSTKBaseWidget()
        dut.do_set_attributes(
            WidgetAttributes(
                datatype="gchararray",
                default="",
                field="test_field",
                format="",
                index=0,
                label_text="Test Label",
                listen_topic="",
                record_id=1,
                send_topic="",
                x_pos=0,
                y_pos=0,
            )
        )

        assert isinstance(dut, RAMSTKBaseWidget)
        assert dut.dic_properties["can_focus"]
        assert dut.dic_properties["editable"]
        assert dut.dic_properties["height_request"] == -1
        assert dut.dic_properties["sensitive"]
        assert dut.dic_properties["tooltip"] == (
            "Missing tooltip, please file a quality type issue to have one added."
        )
        assert dut.dic_properties["visible"]
        assert dut.dic_properties["width_request"] == -1
