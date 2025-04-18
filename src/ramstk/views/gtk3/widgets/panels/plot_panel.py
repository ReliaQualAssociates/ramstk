# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panels.plot_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Plot Panel Class."""


# Standard Library Imports
from typing import List

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
from pandas.plotting import register_matplotlib_converters

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _

# RAMSTK Local Imports
from ..plot import RAMSTKPlot
from . import RAMSTKBasePanel

register_matplotlib_converters()


class RAMSTKPlotPanel(RAMSTKBasePanel):
    """The RAMSTKPlotPanel class.

    The attributes of a RAMSTKPlotPanel are:

    :ivar pltPlot: a RAMSTPlot() for the panels that embed a plot.
    :ivar lst_axis_labels: a list containing the labels for the plot's axes.  Index 0 is
        the abscissa (x-axis) and index 1 is the ordinate (y-axis).
    :ivar lst_legend: a list containing the text to display in the plot's legend.
    :ivar plot_title: the title of the plot.
    """

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPlotPanel."""
        super().__init__()

        # Initialize widgets.
        self.pltPlot: RAMSTKPlot = RAMSTKPlot()

        # Initialize public instance attributes.
        self.lst_axis_labels: List[str] = [_("abscissa"), _("ordinate")]
        self.lst_legend: List[str] = []
        self.legend_title: str = ""
        self.plot_title: str = ""

        super().do_set_properties({"bold": True, "label": self._title})

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_clear_views": self.do_clear_plot_panel,
            }
        )

    def do_clear_plot_panel(self) -> None:
        """Clear the contents of the RAMSTKPlot on a plot type panel."""
        self.pltPlot.axis.cla()
        self.pltPlot.figure.clf()
        self.pltPlot.plot.draw()

    def do_load_plot_panel(self) -> None:
        """Load data into the RAMSTKPlot on a plot type panel."""
        self.pltPlot.do_make_title(
            self.plot_title,
            {
                "font_size": 16,
                "font_weight": "bold",
                "horizontal_alignment": "center",
                "vertical_alignment": "baseline",
            },
        )
        self.pltPlot.do_make_labels(
            self.lst_axis_labels[1],
            {
                "font_size": 14,
                "font_weight": "bold",
                "horizontal_alignment": "center",
                "vertical_alignment": "center",
            },
            set_x=False,
            x_pos=-0.5,
            y_pos=0.0,
        )

        self.pltPlot.do_make_legend(
            self.lst_legend,
            self.legend_title,
            {
                "frame_on": False,
                "location": "upper right",
                "n_columns": 1,
                "shadow": True,
            },
        )
        self.pltPlot.figure.canvas.draw()

    def do_make_plot_panel(self) -> None:
        """Create a panel with a RAMSTKPlot."""
        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.pltPlot.canvas)

        self.add(_scrollwindow)
