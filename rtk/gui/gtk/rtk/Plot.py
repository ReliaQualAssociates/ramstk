# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Plot.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTK Plot Module."""

# pylint: disable=E0401
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure  # pylint: disable=E0401
from matplotlib.lines import Line2D  # pylint: disable=E0401

# Import other RTK Widget classes.
from .Widget import _, gtk  # pylint: disable=E0401


class RTKPlot(object):
    """
    The RTKPlot class.

    This module contains RTK plot class.  This class is derived from the
    applicable pyGTK widgets and matplotlib plots, but are provided with RTK
    specific property values and methods.  This ensures a consistent look and
    feel to widgets in the RTK application.
    """

    def __init__(self):
        """Initialize an instance of the RTKPlot."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_max = []
        self._lst_min = [0.0]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.figure = Figure()
        self.plot = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)

    def _do_make_date_plot(self, x_values, y_values, marker='g-'):
        """
        Make a date plot.

        :param list x_values: the list of x-values (dates) for the plot.
        :param list y_values: the list of y-values for the plot.
        :keyword str marker: the type and color of marker to use for the plot.
                             Default is a solid green line.
        """
        _line, = self.axis.plot_date(
            x_values, y_values, marker, xdate=True, linewidth=2)
        self._lst_min.append(min(y_values))
        self._lst_max.append(max(y_values))

        return _line

    def _do_make_histogram(self, x_values, y_values, marker='g'):
        """
        Make a histogram.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of bin edges for the plot.
        :keyword str marker: the color of bars to use for the histogram.
                             Default is green.
        """
        self.axis.grid(False, which='both')
        _values, _edges, __ = self.axis.hist(
            x_values, bins=y_values, color=marker)
        self._lst_min.append(min(_values))
        self._lst_max.append(max(_values) + 1)

        return _values, _edges

    def _do_make_scatter_plot(self, x_values, y_values, marker='go'):
        """
        Make a scatter plot.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of y-values for the plot.
        :keyword str marker: the type and color of marker to use for the plot.
                             Default is open green circles.
        """
        _line, = self.axis.plot(x_values, y_values, marker, linewidth=2)
        _line.set_ydata(y_values)
        self._lst_min.append(min(y_values))
        self._lst_max.append(max(y_values))

        return _line

    def _do_make_step_plot(self, x_values, y_values, marker='g-'):
        """
        Make a step plot.

        :param list x_values: the list of x-values for the plot.
        :param list y_values: the list of y-values for the plot.
        :keyword str marker: the type and color of marker to use for the plot.
                             Default is a solid green line.
        """
        _line, = self.axis.step(x_values, y_values, marker, where='mid')
        _line.set_ydata(y_values)
        self._lst_min.append(min(y_values))
        self._lst_max.append(max(y_values))

        return _line

    def do_load_plot(self,
                     x_values,
                     y_values=None,
                     plot_type='scatter',
                     marker='g-'):
        """
        Load the RTKPlot.

        :param list x_values: list of the x-values to plot.
        :keyword list y_values: list of the y-values to plot or list of bin
                                edges if plotting a histogram.
        :keyword str plot_type: list of the type of line to plot. Options are:
                                    * 'date'
                                    * 'histogram'
                                    * 'scatter' (default)
                                    * 'step'
        :keyword str marker: the marker to use on the plot. Defaults is 'g-' or
                             a solid green line.  See matplotlib documentation
                             for other options.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if y_values is not None:
            _x_min = min(x_values)
            _x_max = max(x_values)

            if plot_type == 'step':
                _line = self._do_make_step_plot(x_values, y_values, marker)
            elif plot_type == 'scatter':
                _line = self._do_make_scatter_plot(x_values, y_values, marker)
            elif plot_type == 'histogram':
                _values, _edges = self._do_make_histogram(
                    x_values, y_values, marker)
                _x_min = min(_edges)
                _x_max = max(_edges)
            elif plot_type == 'date':
                _line = self._do_make_date_plot(x_values, y_values, marker)

        # Get the minimum and maximum y-values to set the axis bounds.  If the
        # maximum value is infinity, use the next largest value and so forth.
        _min = min(self._lst_min)
        _max = self._lst_max[0]
        for i in range(1, len(self._lst_max)):
            if _max < self._lst_max[i] and self._lst_max[i] != float('inf'):
                _max = self._lst_max[i]

        self.axis.set_ybound(_min, 1.05 * _max)

        self.plot.draw()

        return False

    def do_add_line(self, x_values, y_values=None, color='k', marker='^'):
        """
        Load the RTKPlot.

        :param list x_values: list of the x-values to plot.
        :keyword list y_values: list of the y-values to plot or list of bin
                                edges if plotting a histogram.
        :keyword str color: the color of the line to add to the plot.  Black
                            is the default.  See matplotlib documentation for
                            options.
        :keyword str marker: the marker to use on the plot. Defaults is '^' or
                             an upward pointing triangle.  See matplotlib
                             documentation for other options.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _line = Line2D(
            x_values,
            y_values,
            lw=0.0,
            color=color,
            marker=marker,
            markersize=10)
        self.axis.add_line(_line)
        self.figure.canvas.draw()

        return False

    def do_close_plot(self, __window, __event, parent):
        """
        Return the plot to the Work Book page it is part of.

        :param __window: the gtk.Window() that is being destroyed.
        :type __window: :class:`gtk.Window`
        :param __event: the gtk.gdk.Event() that called this method.
        :type __event: :class:`gtk.gdk.Event`
        :param parent: the original parent gtk.Widget() for the plot.
        :type parent: :class:`gtk.Widget`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.plot.reparent(parent)

        return False

    def do_expand_plot(self, event):
        """
        Display a plot in it's own window.

        :param event: the matplotlib.MouseEvent() that called this method.
        :type event: :class:`matplotlib.MouseEvent`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.plot = event.canvas
        _parent = self.plot.get_parent()

        if event.button == 3:  # Right click.
            _window = gtk.Window()
            _window.set_skip_pager_hint(True)
            _window.set_skip_taskbar_hint(True)
            _window.set_default_size(800, 400)
            _window.set_border_width(5)
            _window.set_position(gtk.WIN_POS_NONE)
            _window.set_title(_(u"RTK Plot"))

            _window.connect('delete_event', self.close_plot, _parent)

            self.plot.reparent(_window)

            _window.show_all()

        return False

    def do_make_labels(self,
                       label,
                       x_pos,
                       y_pos,
                       set_x=True,
                       fontsize=14,
                       fontweight='bold'):
        """
        Make the abscissa or ordinate label.

        :param str label: the text to display as the abscissa or ordinate
                          label.
        :param float x_pos: the position along the abscissa to place the label.
        :param float y_pos: the position along the ordinate to place the label.
        :keyword bool set_x: whether to set the abscissa (default) or ordinate
                             label.
        :keyword int fontsize: the size of the font to use for the axis label.
        :keyword str fontweight: the weight of the font to use for the axis
                                 label.
        :return: matplotlib text instance representing the label.
        :rtype: :class:`matplotlib.text.Text`
        """
        _label = None

        if set_x:
            _label = self.axis.set_xlabel(label, {
                'fontsize': fontsize,
                'fontweight': fontweight,
                'verticalalignment': 'center',
                'horizontalalignment': 'center',
                'x': x_pos,
                'y': y_pos
            })
        else:
            _label = self.axis.set_ylabel(label, {
                'fontsize': fontsize,
                'fontweight': fontweight,
                'verticalalignment': 'center',
                'horizontalalignment': 'center',
                'rotation': 'vertical'
            })

        return _label

    # pylint: disable=too-many-arguments
    def do_make_legend(self,
                       text,
                       fontsize='small',
                       frameon=False,
                       location='upper right',
                       ncol=1,
                       shadow=True,
                       title="",
                       lwd=0.5):
        """
        Make a legend on the RTKPlot.

        :param tuple text: the text to display in the legend.
        :keyword str fontsize: the size of the font to use for the legend.
                               Options are:
                                - xx-small
                                - x-small
                                - small (default)
                                - medium
                                - large
                                - x-large
                                - xx-large
        :keyword bool frameon: whether or not there is a frame around the
                               legend.
        :keyword str location: the location of the legend on the plot.  Options
                               are:
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
        :keyword int ncol: the number columns in the legend.  Default is 1.
        :keyword bool shadow: whether or not to display a shadow behind the
                              legend block.  Default is True.
        :keyword str title: the title of the legend.  Default is an empty
                            string.
        :keyword float lwd: the linewidth of the box around the legend.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _legend = self.axis.legend(
            text,
            frameon=frameon,
            loc=location,
            ncol=ncol,
            shadow=shadow,
            title=title)

        for _text in _legend.get_texts():
            _text.set_fontsize(fontsize)
        for _line in _legend.get_lines():
            _line.set_linewidth(lwd)

        return False

    def do_make_title(self, title, fontsize=16, fontweight='bold'):
        """
        Make the plot title.

        :param str title: the text to display as the title.
        :keyword int fontsize: the size of the font to use for the title.
        :keyword str fontweight: the weight of the font to use for the title.
        :return: matplotlib text instance representing the title.
        :rtype: :class:`matplotlib.text.Text`
        """
        return self.axis.set_title(title, {
            'fontsize': fontsize,
            'fontweight': fontweight,
            'verticalalignment': 'baseline',
            'horizontalalignment': 'center'
        })
