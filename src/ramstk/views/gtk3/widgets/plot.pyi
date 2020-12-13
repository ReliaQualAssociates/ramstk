# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
import matplotlib

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

class RAMSTKPlot:
    _lst_max: Any = ...
    _lst_min: Any = ...
    figure: Any = ...
    canvas: Any = ...
    axis: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_plot(self, x_values: List[float], y_values: List[float],
                     **kwargs: Dict[str, str]) -> None:
        ...

    def do_add_line(self,
                    x_values: List[float],
                    y_values: List[float] = ...,
                    color: str = ...,
                    marker: str = ...) -> None:
        ...

    def do_close_plot(self, __window: Gtk.Window, __event: Gdk.Event,
                      parent: Gtk.Widget) -> None:
        ...

    def do_expand_plot(self,
                       event: matplotlib.backend_bases.MouseEvent) -> None:
        ...

    def do_make_labels(self, label: str,
                       **kwargs: Any) -> matplotlib.text.Text:
        ...

    def do_make_legend(self, text: Union[Any], **kwargs: Any) -> None:
        ...

    def do_make_title(self,
                      title: str,
                      fontsize: int = ...,
                      fontweight: str = ...) -> matplotlib.text.Text:
        ...

    def _do_make_date_plot(self, x_values: List[float], y_values: List[float],
                           **kwargs: Dict[str, str]) -> None:
        ...

    def _do_make_histogram(self, x_values: List[float], y_values: List[float],
                           **kwargs: Dict[str, str]) -> None:
        ...

    def _do_make_scatter_plot(self, x_values: List[float],
                              y_values: List[float],
                              **kwargs: Dict[str, str]) -> None:
        ...

    def _do_make_step_plot(self, x_values: List[float], y_values: List[float],
                           **kwargs: Dict[str, str]) -> None:
        ...

    def _get_minimax_ordinates(self) -> Tuple[float, float]:
        ...
