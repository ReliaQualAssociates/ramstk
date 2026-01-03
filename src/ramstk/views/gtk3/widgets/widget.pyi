# Standard Library Imports
from datetime import date
from types import EllipsisType
from typing import Dict, List, TypedDict, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import Pango as Pango
from ramstk.views.gtk3 import _ as _

class WidgetAttributes(TypedDict, total=False):
    column_types: Union[List[EllipsisType], List[GObject.GType]]
    datatype: bool | date | float | int | str | None
    default: bool | date | float | int | str | None
    field: str
    format: str
    index: int
    label_text: str | None
    listen_topic: str | None
    parent_id: int
    record_id: int
    send_topic: str | None
    subscribe: str
    x_pos: int
    y_pos: int

class WidgetProperties(TypedDict, total=False):
    action: Gtk.FileChooserAction | None
    activatable: bool
    adjustment: Gtk.Adjustment | None
    alignment: Pango.Alignment | None
    alpha: int
    always_show_image: bool
    angle: float
    background_rgba: Gdk.RGBA | None
    bg_color: str
    bold: bool
    buffer: Gtk.TextBuffer | None
    can_focus: bool
    cell_background_rgba: Gdk.RGBA | None
    cell_foreground_rgba: Gdk.RGBA | None
    climb_rate: float
    destroy_with_parent: bool
    digits: int
    editable: bool
    ellipsize: Pango.EllipsizeMode | None
    enable_grid_lines: Gtk.TreeViewGridLines | None
    enable_tree_lines: bool
    fg_color: str
    foreground_rgba: Gdk.RGBA | None
    group: Gtk.RadioButton | None
    has_entry: bool
    height_request: int
    icon: str
    input_purpose: Gtk.InputPurpose | None
    invisible_char: str
    justify: Gtk.Justification | None
    label: str
    level_indentation: int
    lines: int
    lower: float
    modal: bool
    model: Gtk.ListStore | None
    name: str
    numeric: bool
    opacity: int
    page_increment: float
    page_size: float
    parent: Gtk.Widget | None
    rgba: Gdk.RGBA | None
    rubber_banding: bool
    sensitive: bool
    shadow_type: Gtk.ShadowType | None
    snap_to_ticks: bool
    step_increment: float
    text_column: int
    title: str
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
    wrap_mode: Gtk.WrapMode.WORD | None
    wrap_width: int
    xalign: float
    yalign: float

class RAMSTKBaseWidget(Gtk.Widget):
    _default_height: int
    _default_width: int
    _edit_signal: str
    dic_handler_id: dict[str, int]
    dic_properties: WidgetProperties
    datatype: bool | date | float | int | str | None
    default: bool | date | float | int | str | None
    field: str
    format: str
    height: int
    index: int
    label_text: str
    listen_topic: str
    parent_id: int
    record_id: int
    send_topic: str
    width: int
    x_pos: int
    y_pos: int
    def __init__(self) -> None: ...
    def do_get_attribute(
        self, attribute: str
    ) -> bool | date | float | int | str | None: ...
    def do_set_attributes(self, attributes: WidgetAttributes) -> None: ...
    def do_set_callbacks(self) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_subscribe_to_messages(self) -> None: ...
    def do_update(
        self, package: Dict[str, Union[bool, date, float, int, str, None]]
    ) -> None: ...

class WidgetConfig(TypedDict):
    widget: RAMSTKBaseWidget
    attributes: WidgetAttributes
    properties: WidgetProperties

def make_widget_config(
    widget: RAMSTKBaseWidget,
    attributes: WidgetAttributes,
    properties: WidgetProperties,
) -> WidgetConfig: ...
def set_widget_sensitivity(
    widgets: list[RAMSTKBaseWidget | Gtk.Widget], sensitive: bool = True
) -> None: ...
