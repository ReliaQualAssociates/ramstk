# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from ..plot import RAMSTKPlot as RAMSTKPlot
from . import RAMSTKBasePanel as RAMSTKBasePanel

class RAMSTKPlotPanel(RAMSTKBasePanel):
    pltPlot: RAMSTKPlot
    lst_axis_labels: list[str]
    lst_legend: list[str]
    legend_title: str
    plot_title: str
    def __init__(self) -> None: ...
    def do_clear_plot_panel(self) -> None: ...
    def do_load_plot_panel(self) -> None: ...
    def do_make_plot_panel(self) -> None: ...
