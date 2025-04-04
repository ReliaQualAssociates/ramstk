# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.widget.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseWidget module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Optional, TypedDict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, GObject, Gtk, Pango, _


class WidgetAttributes(TypedDict, total=False):
    """Type for the widget attributes."""

    datatype: Union[bool, date, float, int, str, None]
    default: Union[bool, date, float, int, str, None]
    field: str
    format: str
    index: int
    label_text: Optional[str]
    listen_topic: str
    record_id: int
    send_topic: str
    subscribe: str
    x_pos: int
    y_pos: int


class WidgetProperties(TypedDict, total=False):
    """Type for widget properties dict."""

    action: Optional[Gtk.FileChooserAction]
    activatable: bool
    adjustment: Optional[Gtk.Adjustment]
    alignment: Optional[Pango.Alignment]
    always_show_image: bool
    angle: float
    background_rgba: Optional[Gdk.RGBA]
    bg_color: str
    bold: bool
    buffer: Optional[Gtk.TextBuffer]
    can_focus: bool
    cell_background_rgba: Optional[Gdk.RGBA]
    cell_foreground_rgba: Optional[Gdk.RGBA]
    climb_rate: float
    destroy_with_parent: bool
    digits: int
    editable: bool
    ellipsize: Optional[Pango.EllipsizeMode]
    enable_grid_lines: Optional[Gtk.TreeViewGridLines]
    enable_tree_lines: bool
    fg_color: str
    foreground_rgba: Optional[Gdk.RGBA]
    group: Optional[Gtk.RadioButton]
    has_entry: bool
    height_request: int
    icon: str
    input_purpose: Optional[Gtk.InputPurpose]
    invisible_char: str
    justify: Optional[Gtk.Justification]
    label: str
    level_indentation: int
    lines: int
    lower: float
    modal: bool
    model: Optional[Gtk.ListStore]
    name: str
    numeric: bool
    opacity: int
    page_increment: float
    page_size: float
    parent: Optional[Gtk.Widget]
    rubber_banding: bool
    sensitive: bool
    shadow_type: Optional[Gtk.ShadowType]
    snap_to_ticks: bool
    step_increment: float
    text_column: int
    tooltip: str
    tooltip_column: int
    upper: float
    use_markup: bool
    use_underline: bool
    visible: bool
    weight: int
    weight_set: bool
    width_request: int
    wrap: bool
    wrap_mode: Optional[Gtk.WrapMode.WORD]
    wrap_width: int
    xalign: float
    yalign: float


class RAMSTKBaseWidget(Gtk.Widget):
    """The RAMSTKBaseWidget class."""

    # Define private class attributes.
    _default_height: int = -1
    _default_width: int = -1
    _edit_signal: str = "changed"

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKBaseWidget widget."""
        GObject.GObject.__init__(self)

        # Initialize public attributes.
        self.dic_handler_id: Dict[str, int] = {}
        self.dic_properties = WidgetProperties(
            can_focus=True,
            editable=True,
            height_request=-1,
            sensitive=True,
            tooltip=_(
                "Missing tooltip, please file a quality type issue to have one added."
            ),
            visible=True,
            width_request=-1,
        )
        self.datatype: Union[bool, date, float, int, str, None] = None
        self.default: Union[bool, date, float, int, str, None] = None
        self.field: str = ""
        self.format: str = "{}"
        self.handler_id: int = -1
        self.height: int = -1
        self.index: int = -1
        self.label_text: str = ""
        self.listen_topic: str = ""
        self.record_id: int = -1
        self.send_topic: str = ""
        self.width: int = -1
        self.x_pos: int = 0
        self.y_pos: int = 0

    # ----- ----- Standard widget methods. ----- ----- #
    def do_get_attribute(
        self, attribute: str
    ) -> Union[bool, date, float, int, str, None]:
        """Get the value of the requested RAMSTKBaseWidget attribute.

        :param attribute: the name of the attribute to retrieve.
        :return: the value of the requested attribute.
        """
        return {
            "datatype": self.datatype,
            "default": self.default,
            "field": self.field,
            "format": self.format,
            "index": self.index,
            "label_text": self.label_text,
            "record_id": self.record_id,
            "listen_topic": self.listen_topic,
            "send_topic": self.send_topic,
            "x_pos": self.x_pos,
            "y_pos": self.y_pos,
        }[attribute]

    def do_set_attributes(self, attributes: WidgetAttributes) -> None:
        """Set the RAMSTKBaseWidget attributes.

        :param attributes: the WidgetAttributes dict with the attribute values to set
            for the RAMSTKBaseWidget.
        """
        self.datatype = attributes.get("datatype", None)
        self.default = str(attributes.get("default", "None"))
        self.field = str(attributes.get("field", ""))
        self.format = str(attributes.get("format", "{}"))
        self.index = int(attributes.get("index", -1))
        self.label_text = str(attributes.get("label_text", ""))
        self.record_id = int(attributes.get("record_id", -1))
        self.listen_topic = str(attributes.get("listen_topic", ""))
        self.send_topic = str(attributes.get("send_topic", ""))
        self.x_pos = int(attributes.get("x_pos", 0))
        self.y_pos = int(attributes.get("y_pos", 0))

    def do_set_callbacks(self) -> None:
        """Set the callback method for the RAMSTKBaseWidget."""
        if hasattr(self, "on_changed"):
            # RAMSTKTextViews need to connect their Gtk.TextBuffer to the callback.
            if (
                "buffer" in self.dic_properties
                and self.dic_properties["buffer"] is not None
            ):
                self.dic_properties["buffer"].connect(  # type: ignore[attr-defined]
                    self._edit_signal,
                    self.on_changed,
                )
            else:
                self.handler_id = self.connect(
                    self._edit_signal,
                    self.on_changed,
                )

    def do_set_properties(self, properties: WidgetProperties) -> None:
        """Set the properties of the RAMSTKBaseWidget.

        :param properties: the WidgetProperties dict with the property values to set for
            the RAMSTKBaseWidget.
        """
        self.dic_properties["can_focus"] = properties.get("can_focus", True)
        self.dic_properties["height_request"] = properties.get(
            "height_request", self._default_height
        )
        self.dic_properties["sensitive"] = properties.get("sensitive", True)
        self.dic_properties["tooltip"] = properties.get(
            "tooltip",
            "Missing tooltip, please file a quality type issue to have one added.",
        )
        self.dic_properties["visible"] = properties.get("visible", True)
        self.dic_properties["width_request"] = properties.get(
            "width_request", self._default_width
        )

        if self.dic_properties["height_request"] == 0:
            self.dic_properties["height_request"] = self._default_height
        if self.dic_properties["width_request"] == 0:
            self.dic_properties["width_request"] = self._default_width

        if hasattr(self, "can-focus"):
            self.set_property(  # type: ignore[attr-defined]
                "can-focus",
                self.dic_properties["can_focus"],
            )
        if hasattr(self, "height-request"):
            self.set_property(  # type: ignore[attr-defined]
                "height-request",
                self.dic_properties["height_request"],
            )
        if hasattr(self, "tooltip-markup"):
            self.set_property(  # type: ignore[attr-defined]
                "tooltip-markup",
                self.dic_properties["tooltip"],
            )
        if hasattr(self, "width-request"):
            self.set_property(  # type: ignore[attr-defined]
                "width-request",
                self.dic_properties["width_request"],
            )
        self.set_visible(
            self.dic_properties["visible"],
        )

    def do_subscribe_to_messages(self) -> None:
        """Subscribe the RAMSTKBaseWidget to PyPubSub messages."""
        pub.subscribe(self.do_update, self.listen_topic)


class WidgetConfig(TypedDict):
    """Type for widget configuration."""

    widget: RAMSTKBaseWidget
    attributes: WidgetAttributes
    properties: WidgetProperties


def set_widget_sensitivity(
    widgets: List[RAMSTKBaseWidget | Gtk.Widget], sensitive: bool = True
) -> None:
    """Set the sensitivity for a list of widgets.

    :param widgets: list of widget objects.
    :param sensitive: whether to make the widgets sensitive or not.
    """
    for _widget in widgets:
        _widget.set_sensitive(sensitive)  # type: ignore[union-attr]
