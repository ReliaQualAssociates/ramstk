# Standard Library Imports
from typing import List, Tuple, TypedDict

# Third Party Imports
import matplotlib
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from .widget import RAMSTKBaseWidget as RAMSTKBaseWidget

class PlotProperties(TypedDict, total=False):
    font_size: int | str
    font_weight: str
    frame_on: bool
    horizontal_alignment: str
    line_width: float
    location: str
    n_columns: int
    rotation: str
    shadow: bool
    title: str
    vertical_alignment: str
    x_pos: int
    y_pos: int

class RAMSTKPlot(RAMSTKBaseWidget):
    _lst_max: List[float]
    _lst_min: List[float]
    figure: matplotlib.figure.Figure
    canvas: Incomplete
    axis: Incomplete
    def __init__(self) -> None: ...
    def do_load_plot(
        self,
        x_values: list[float],
        y_values: list[float],
        marker: str,
        plot_type: str = "scatter",
    ) -> None: ...
    def do_add_line(
        self,
        x_values: list[float],
        y_values: list[float] | None = None,
        color: str = "k",
        marker: str = "^",
    ) -> None: ...
    def do_close_plot(
        self, __window: Gtk.Window, /, __event: Gdk.Event, parent: Gtk.Widget
    ) -> None: ...
    def do_expand_plot(self, event: matplotlib.backend_bases.MouseEvent) -> None: ...
    def do_make_labels(
        self,
        label: str,
        properties: PlotProperties,
        set_x: bool = True,
        x_pos: float = 0.0,
        y_pos: float = 0.0,
    ) -> matplotlib.text.Text: ...
    def do_make_legend(
        self, text: list[str], title: str, properties: PlotProperties
    ) -> None: ...
    def do_make_title(
        self, title: str, properties: PlotProperties
    ) -> matplotlib.text.Text: ...
    def _do_make_date_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "g-",
    ) -> None: ...
    def _do_make_histogram(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "g",
    ) -> None: ...
    def _do_make_scatter_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "go",
    ) -> None: ...
    def _do_make_step_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "g-",
    ) -> None: ...
    def _get_minimax_ordinates(self) -> Tuple[float, float]: ...
