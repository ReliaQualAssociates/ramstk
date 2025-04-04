# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.plot.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
# isort:skip_file
"""The RAMSTKPlot module."""

# Standard Library Imports
from typing import List, Optional, Tuple, TypedDict, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _
from .widget import RAMSTKBaseWidget

# type: ignore
try:
    # noinspection PyPackageRequirements
    # Third Party Imports
    import matplotlib

    # noinspection PyPackageRequirements
    from matplotlib.backends.backend_gtk3cairo import (
        FigureCanvasGTK3Cairo as FigureCanvas,
    )

    # noinspection PyPackageRequirements
    from matplotlib.figure import Figure

    # noinspection PyPackageRequirements
    from matplotlib.lines import Line2D
except RuntimeError:
    # This is necessary to have the tests pass on headless servers.
    pass


class PlotProperties(TypedDict, total=False):
    """Type for plot properties dict."""

    font_size: Union[int, str]
    """font_size options are:
        - xx-small
        - x-small
        - small
        - medium
        - large
        - x-large
        - xx-large
        - an actual integer value"""
    font_weight: str
    frame_on: bool
    horizontal_alignment: str
    line_width: float
    location: str
    """location options are:
        - best
        - upper right
        - upper left
        - lower left
        - lower right
        - right
        - center left
        - center right
        - lower center
        - upper center
        - center"""
    n_columns: int
    rotation: str
    shadow: bool
    title: str
    vertical_alignment: str
    x_pos: int
    y_pos: int


class RAMSTKPlot(RAMSTKBaseWidget):
    """The RAMSTKPlot class."""

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPlot widget."""
        RAMSTKBaseWidget.__init__(  # type: ignore[call-arg] # pylint: disable=too-many-function-args # noqa
            self
        )

        # Initialize private instance attributes.
        self._lst_max: List[float] = []
        self._lst_min: List[float] = [0.0]

        # Initialize public instance attributes.
        self.figure: matplotlib.figure.Figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)

    # ----- ----- RAMSTKPlot specific methods. ----- ----- #
    def do_load_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        plot_type: str = "scatter",
    ) -> None:
        """Load the RAMSTKPlot.

        Pass the keyword plot_type to select.  Markers can be set using the marker
        keyword.  The default marker is 'g-' or a solid green line.  See matplotlib
        documentation for other options.

        :param x_values: list of the x-values to plot.
        :param y_values: list of the y-values to plot or list of bin edges if plotting a
            histogram.
        :param plot_type: the type of plot to produce. Options are 'date', 'histogram',
            'scatter' (default), and 'step'.
        """
        if plot_type == "step":
            self._do_make_step_plot(x_values, y_values)
        elif plot_type == "scatter":
            self._do_make_scatter_plot(x_values, y_values)
        elif plot_type == "histogram":
            self._do_make_histogram(x_values, y_values)
        elif plot_type == "date":
            self._do_make_date_plot(x_values, y_values)

        _min, _max = self._get_minimax_ordinates()

        self.axis.set_ybound(_min, 1.05 * _max)

        self.canvas.show()

    def do_add_line(
        self,
        x_values: List[float],
        y_values: Optional[List[float]] = None,
        color: str = "k",
        marker: str = "^",
    ) -> None:
        """Load the RAMSTKPlot.

        :param x_values: list of the x-values to plot.
        :param y_values: list of the y-values to plot or list of bin edges if plotting a
            histogram.
        :param color: the color of the line to add to the plot. Black is the default.
            See matplotlib documentation for options.
        :param marker: the marker to use on the plot. Default is '^' or an upward
            pointing triangle. See matplotlib documentation for other options.
        """
        _line = Line2D(
            x_values,
            y_values,
            lw=0.0,
            color=color,
            marker=marker,
            markersize=10,
        )
        self.axis.add_line(_line)

    def do_close_plot(
        self, __window: Gtk.Window, __event: Gdk.Event, parent: Gtk.Widget
    ) -> None:
        """Return the plot to the Work Book page it is part of.

        :param __window: the Gtk.Window() that is being destroyed.
        :type __window: :class:`Gtk.Window`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param parent: the original parent Gtk.Widget() for the plot.
        :type parent: :class:`Gtk.Widget`
        """
        self.canvas.reparent(parent)

    # noinspection PyUnresolvedReferences
    def do_expand_plot(self, event: matplotlib.backend_bases.MouseEvent) -> None:
        """Display a plot in its own window.

        :param event: the matplotlib.backend_bases.MouseEvent() that called
            this method.
        :type event: :class:`matplotlib.backend_bases.MouseEvent`
        """
        self.canvas = event.canvas
        _parent = self.canvas.get_parent()

        if event.button == 3:  # Right click.
            _window = Gtk.Window()
            _window.set_skip_pager_hint(True)
            _window.set_skip_taskbar_hint(True)
            _window.set_default_size(800, 400)
            _window.set_border_width(5)
            _window.set_position(Gtk.WindowPosition.NONE)
            _window.set_title(_("RAMSTK Plot"))

            _window.connect("delete_event", self.do_close_plot, _parent)

            self.canvas.reparent(_window)

            _window.show_all()

    # noinspection PyUnresolvedReferences
    def do_make_labels(
        self,
        label: str,
        properties: PlotProperties,
        set_x: bool = True,
        x_pos: int = 0,
        y_pos: int = 0,
    ) -> matplotlib.text.Text:
        """Make the abscissa or ordinate label.

        :param label: the text to display as the abscissa or ordinate
            label.
        :param properties: the PlotProperties for the plot label.
        :param set_x: whether to set the x-axis label (default) or the y-axis label.
        :param x_pos:
        :param y_pos:
        :return: matplotlib text instance representing the label.
        :rtype: :class:`matplotlib.text.Text`
        """
        if set_x:
            return self.axis.set_xlabel(
                label,
                {
                    "fontsize": properties.get("font_size", 14),
                    "fontweight": properties.get("font_weight", "bold"),
                    "horizontalalignment": properties.get(
                        "horizontal_alignment", "center"
                    ),
                    "verticalalignment": properties.get("vertical_alignment", "center"),
                    "x": x_pos,
                    "y": y_pos,
                },
            )
        return self.axis.set_ylabel(
            label,
            {
                "fontsize": properties.get("font_size", 14),
                "fontweight": properties.get("font_weight", "bold"),
                "verticalalignment": properties.get("horizontal_alignment", "center"),
                "horizontalalignment": properties.get("vertical_alignment", "center"),
                "rotation": properties.get("rotation", "vertical"),
            },
        )

    # pylint: disable=too-many-arguments
    def do_make_legend(
        self, text: List[str], title: str, properties: PlotProperties
    ) -> None:
        """Make a legend on the RAMSTKPlot.

        :param text: the text to display in the legend.
        :param title: the title for the legend block.
        :param properties: the PlotProperties for the plot legend.
        """
        _legend = self.axis.legend(
            text,
            frameon=properties.get("frame_on", False),
            loc=properties.get("location", "upper right"),
            ncol=properties.get("n_columns", 1),
            shadow=properties.get("shadow", True),
            title=title,
        )

        for _text in _legend.get_texts():
            _text.set_fontsize(properties.get("font_size", "small"))
        for _line in _legend.get_lines():
            _line.set_linewidth(properties.get("line_width", 0.5))

    # noinspection PyUnresolvedReferences
    def do_make_title(
        self, title: str, properties: PlotProperties
    ) -> matplotlib.text.Text:
        """Make the plot title.

        :param title: the text to display as the title.
        :param properties: the PlotProperties for the plot title.
        :return: matplotlib text instance representing the title.
        :rtype: :class:`matplotlib.text.Text`
        """
        return self.axis.set_title(
            title,
            {
                "fontsize": properties.get("font_size", 16),
                "fontweight": properties.get("font_weight", "bold"),
                "horizontalalignment": properties.get("horizontal_alignment", "center"),
                "verticalalignment": properties.get("vertical_alignment", "baseline"),
            },
        )

    def _do_make_date_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "g-",
    ) -> None:
        """Make a date plot.

        :param x_values: the list of x-values (dates) for the plot.
        :param y_values: the list of y-values for the plot.
        :param marker: type and color of marker to use for the plot. Default is 'go' or
            a solid green line.
        """
        if y_values is not None:
            self.axis.plot_date(x_values, y_values, marker, xdate=True, linewidth=2)
            self._lst_min.append(min(y_values))
            self._lst_max.append(max(y_values))

    def _do_make_histogram(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "g",
    ) -> None:
        """Make a histogram.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of bin edges for the plot.
        :param marker: type and color of marker to use for the plot. Default is 'g' or
            solid green.
        """
        if y_values is not None:
            self.axis.grid(False, which="both")
            # pylint: disable=unused-variable
            _values, _edges, __ = self.axis.hist(x_values, bins=y_values, color=marker)
            self._lst_min.append(min(_values))
            self._lst_max.append(max(_values) + 1)

    def _do_make_scatter_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "go",
    ) -> None:
        """Make a scatter plot.

        :param x_values: the list of x-values for the plot.
        :param y_values: the list of y-values for the plot.
        :param marker: type and color of marker to use for the plot. Default is 'go' or
            open green circles.
        """
        if y_values is not None:
            (_line,) = self.axis.plot(x_values, y_values, marker, linewidth=2)
            _line.set_ydata(y_values)
            self._lst_min.append(min(y_values))
            self._lst_max.append(max(y_values))

    def _do_make_step_plot(
        self,
        x_values: List[float],
        y_values: List[float],
        marker: str = "g-",
    ) -> None:
        """Make a step plot.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of y-values for the plot.
        :param marker: type and color of marker to use for the plot. Default is 'g-' or
            a solid green line.
        """
        if y_values is not None:
            (_line,) = self.axis.step(x_values, y_values, marker, where="mid")
            _line.set_ydata(y_values)
            self._lst_min.append(min(y_values))
            self._lst_max.append(max(y_values))

    def _get_minimax_ordinates(self) -> Tuple[float, float]:
        """Get minimum and maximum y-values to set the axis bounds.

        If the maximum value is infinity, use the next largest value and so forth.

        :return: _min, _max; tuple containing the minimum and maximum ordinate values.
        """
        _min: float = min(self._lst_min)
        _max: float = max(1.0, self._lst_max[0])
        for i in range(1, len(self._lst_max)):
            if _max < self._lst_max[i] != float("inf"):
                _max = self._lst_max[i]

        return _min, _max
