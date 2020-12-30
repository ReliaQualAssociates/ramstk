# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.plot.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
# isort:skip_file
"""RAMSTK GTK3 Plot Module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _

# type: ignore
try:
    # noinspection PyPackageRequirements
    # Third Party Imports
    import matplotlib
    # noinspection PyPackageRequirements
    from matplotlib.backends.backend_gtk3cairo import (FigureCanvasGTK3Cairo as
                                                       FigureCanvas)
    # noinspection PyPackageRequirements
    from matplotlib.figure import Figure
    # noinspection PyPackageRequirements
    from matplotlib.lines import Line2D
except RuntimeError:
    # This is necessary to have the tests pass on headless servers.
    pass


class RAMSTKPlot:
    """The RAMSTKPlot class.

    This module contains RAMSTK plot class.  This class is derived from
    the applicable pyGTK widgets and matplotlib plots, but are provided
    with RAMSTK specific property values and methods.  This ensures a
    consistent look and feel to widgets in the RAMSTK application.
    """
    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPlot."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_max: List[float] = []
        self._lst_min: List[float] = [0.0]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.figure: matplotlib.figure.Figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)

    def do_load_plot(self, x_values: List[float], y_values: List[float],
                     **kwargs: Dict[str, str]) -> None:
        """Load the RAMSTKPlot.

        Plots can be one of the following types:

            * 'date'
            * 'histogram'
            * 'scatter' (default)
            * 'step'

        Pass the keyword plot_type to select.  Markers can be set using the
        marker keyword.  The default marker is 'g-' or a solid green line.  See
        matplotlib documentation for other options.

        :param x_values: list of the x-values to plot.
        :param y_values: list of the y-values to plot or list of bin edges if
            plotting a histogram.
        :return: None
        :rtype: None
        """
        _plot_type = kwargs.get('plot_type', 'scatter')

        if _plot_type == 'step':
            self._do_make_step_plot(x_values, y_values, **kwargs)
        elif _plot_type == 'scatter':
            self._do_make_scatter_plot(x_values, y_values, **kwargs)
        elif _plot_type == 'histogram':
            self._do_make_histogram(x_values, y_values, **kwargs)
        elif _plot_type == 'date':
            self._do_make_date_plot(x_values, y_values, **kwargs)

        _min, _max = self._get_minimax_ordinates()

        self.axis.set_ybound(_min, 1.05 * _max)

        self.canvas.show()

    def do_add_line(self,
                    x_values: List[float],
                    y_values: List[float] = None,
                    color: str = 'k',
                    marker: str = '^') -> None:
        """Load the RAMSTKPlot.

        :param x_values: list of the x-values to plot.
        :param y_values: list of the y-values to plot or list of bin edges if
            plotting a histogram.
        :param color: the color of the line to add to the plot.  Black is the
            default.  See matplotlib documentation for options.
        :param marker: the marker to use on the plot. Default is '^' or an
            upward pointing triangle.  See matplotlib documentation for other
            options.
        :return: None
        :rtype: None
        """
        _line = Line2D(x_values,
                       y_values,
                       lw=0.0,
                       color=color,
                       marker=marker,
                       markersize=10)
        self.axis.add_line(_line)

    def do_close_plot(self, __window: Gtk.Window, __event: Gdk.Event,
                      parent: Gtk.Widget) -> None:
        """Return the plot to the Work Book page it is part of.

        :param __window: the Gtk.Window() that is being destroyed.
        :type __window: :class:`Gtk.Window`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param parent: the original parent Gtk.Widget() for the plot.
        :type parent: :class:`Gtk.Widget`
        :return: None
        :rtype: None
        """
        self.canvas.reparent(parent)

    # noinspection PyUnresolvedReferences
    def do_expand_plot(self,
                       event: matplotlib.backend_bases.MouseEvent) -> None:
        """Display a plot in it's own window.

        :param event: the matplotlib.backend_bases.MouseEvent() that called
            this method.
        :type event: :class:`matplotlib.backend_bases.MouseEvent`
        :return: None
        :rtype: None
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
            _window.set_title(_(u"RAMSTK Plot"))

            _window.connect('delete_event', self.do_close_plot, _parent)

            self.canvas.reparent(_window)

            _window.show_all()

    # noinspection PyUnresolvedReferences
    def do_make_labels(self, label: str,
                       **kwargs: Any) -> matplotlib.text.Text:
        """Make the abscissa or ordinate label.

        Accepts keyword arguments:
            * *fontsize* -- the size of the font to use for the axis label.
            * *fontweight* -- the weight of the font to use for the axis label.
            * *set_x* -- whether to set the abscissa (default) or ordinate
                label.
            * *x_pos* -- the position along the abscissa to place the label.
            * *y_pos* -- the position along the ordinate to place the label.

        :param label: the text to display as the abscissa or ordinate
            label.
        :return: matplotlib text instance representing the label.
        :rtype: :class:`matplotlib.text.Text`
        """
        _fontsize = kwargs.get('fontsize', 14)
        _fontweight = kwargs.get('fontweight', 'bold')
        _set_x = kwargs.get('set_x', True)
        _x_pos = kwargs.get('x_pos', 0)
        _y_pos = kwargs.get('y_pos', 0)

        _label = None

        if _set_x:
            _label = self.axis.set_xlabel(
                label, {
                    'fontsize': _fontsize,
                    'fontweight': _fontweight,
                    'verticalalignment': 'center',
                    'horizontalalignment': 'center',
                    'x': _x_pos,
                    'y': _y_pos
                })
        else:
            _label = self.axis.set_ylabel(
                label, {
                    'fontsize': _fontsize,
                    'fontweight': _fontweight,
                    'verticalalignment': 'center',
                    'horizontalalignment': 'center',
                    'rotation': 'vertical'
                })

        return _label

    # pylint: disable=too-many-arguments
    def do_make_legend(self, text: Union[Any], **kwargs: Any) -> None:
        """Make a legend on the RAMSTKPlot.

        Accepts keyword arguments:
            * *fontsize* (str) -- the size of the font to use for the legend.
                Options are:
                    - xx-small
                    - x-small
                    - small (default)
                    - medium
                    - large
                    - x-large
                    - xx-large
            * *frameon* (bool) -- whether or not there is a frame around the
                legend.
            * *location* (str) -- the location of the legend on the plot.
                Options are:
                    - best
                    - upper right (default)
                    - upper left
                    - lower left
                    - lower right
                    - right
                    - center left
                    - center right
                    - lower center
                    - upper center
                    - center
            * *ncol* (int) -- the number columns in the legend.  Default is 1.
            * *shadow* (bool) -- whether or not to display a shadow behind the
                legend block.  Default is True.
            * *title* (str) -- the title of the legend.  Default is an empty
                string.
            * *lwd* (float) -- the linewidth of the box around the legend.

        :param tuple text: the text to display in the legend.
        :return: None
        :rtype: None
        """
        _fontsize = kwargs.get('fontsize', 'small')
        _frameon = kwargs.get('frameon', False)
        _location = kwargs.get('location', 'upper right')
        _lwd = kwargs.get('lwd', 0.5)
        _ncol = kwargs.get('ncol', 1)
        _shadow = kwargs.get('shadow', True)
        _title = kwargs.get('title', "")

        _legend = self.axis.legend(text,
                                   frameon=_frameon,
                                   loc=_location,
                                   ncol=_ncol,
                                   shadow=_shadow,
                                   title=_title)

        for _text in _legend.get_texts():
            _text.set_fontsize(_fontsize)
        for _line in _legend.get_lines():
            _line.set_linewidth(_lwd)

    # noinspection PyUnresolvedReferences
    def do_make_title(self,
                      title: str,
                      fontsize: int = 16,
                      fontweight: str = 'bold') -> matplotlib.text.Text:
        """Make the plot title.

        :param title: the text to display as the title.
        :param fontsize: the size of the font to use for the title.
        :param fontweight: the weight of the font to use for the title.
        :return: matplotlib text instance representing the title.
        :rtype: :class:`matplotlib.text.Text`
        """
        return self.axis.set_title(
            title, {
                'fontsize': fontsize,
                'fontweight': fontweight,
                'verticalalignment': 'baseline',
                'horizontalalignment': 'center'
            })

    def _do_make_date_plot(self, x_values: List[float], y_values: List[float],
                           **kwargs: Dict[str, str]) -> None:
        """Make a date plot.

        Use the keyword marker to set the type and color of marker to use
        for the plot.  Default is 'g-' or a solid green line.

        :param x_values: the list of x-values (dates) for the plot.
        :param y_values: the list of y-values for the plot.
        :return: None
        :rtype: None
        """
        _marker = kwargs.get('marker', 'g-')

        if y_values is not None:
            self.axis.plot_date(x_values,
                                y_values,
                                _marker,
                                xdate=True,
                                linewidth=2)
            self._lst_min.append(min(y_values))
            self._lst_max.append(max(y_values))

    def _do_make_histogram(self, x_values: List[float], y_values: List[float],
                           **kwargs: Dict[str, str]) -> None:
        """Make a histogram.

        Use the keyword marker to set the color of the bars used for the plot.
        Default is 'g' or green.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of bin edges for the plot.
        :keyword str marker: the color of bars to use for the histogram.
            Default is green.
        :return: None
        :rtype: None
        """
        _marker = kwargs.get('marker', 'g')

        if y_values is not None:
            self.axis.grid(False, which='both')
            # pylint: disable=unused-variable
            _values, _edges, __ = self.axis.hist(x_values,
                                                 bins=y_values,
                                                 color=_marker)
            self._lst_min.append(min(_values))
            self._lst_max.append(max(_values) + 1)

    def _do_make_scatter_plot(self, x_values: List[float],
                              y_values: List[float],
                              **kwargs: Dict[str, str]) -> None:
        """Make a scatter plot.

        Use the keyword marker to set the type and color of marker to use
        for the plot.  Default is 'go' or open green circles.

        :param x_values: the list of x-values for the plot.
        :param y_values: the list of y-values for the plot.
        :return: None
        :rtype: None
        """
        _marker = kwargs.get('marker', 'go')

        if y_values is not None:
            _line, = self.axis.plot(x_values, y_values, _marker, linewidth=2)
            _line.set_ydata(y_values)
            self._lst_min.append(min(y_values))
            self._lst_max.append(max(y_values))

    def _do_make_step_plot(self, x_values: List[float], y_values: List[float],
                           **kwargs: Dict[str, str]) -> None:
        """Make a step plot.

        Use the keyword marker to set the type and color of marker to use
        for the plot.  Default is 'g-' or a solid green line.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of y-values for the plot.
        :return: None
        :rtype: None
        """
        _marker = kwargs.get('marker', 'g-')

        if y_values is not None:
            _line, = self.axis.step(x_values, y_values, _marker, where='mid')
            _line.set_ydata(y_values)
            self._lst_min.append(min(y_values))
            self._lst_max.append(max(y_values))

    def _get_minimax_ordinates(self) -> Tuple[float, float]:
        """Get minimum and maximum y-values to set the axis bounds.

        If the maximum value is infinity, use the next largest value and so
        forth.

        :return: _min, _max; tuple containing the minimum and maximum ordinate
            values.
        """
        _min: float = min(self._lst_min)
        _max: float = max(1.0, self._lst_max[0])
        for i in range(1, len(self._lst_max)):
            if _max < self._lst_max[i] != float('inf'):
                _max = self._lst_max[i]

        return _min, _max
