# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Plot.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Plot Module
-------------------------------------------------------------------------------

This module contains RTK plot classes.  These classes are derived from the
applicable pyGTK widgets and matplotlib plots, but are provided with RTK
specific property values and methods.  This ensures a consistent look and feel
to widgets in the RTK application.
"""

# Import other RTK Widget classes.
from .Widget import _, gtk                             # pylint: disable=E0401


def load_plot(axis, plot, x_vals, y1=None, y2=None, y3=None, y4=None,
              title="", xlab="", ylab="", ltype=[1, 1, 1, 1],
              marker=['g-', 'r-', 'b-', 'k--']):
    """
    Function to load the matplotlib plots.

    :param matplotlib.Axis axis: the matplotlib axis object.
    :param matplotlib.FigureCanvas plot: the matplotlib plot object.
    :param list x_vals: list of the x values to plot.
    :keyword float y1: list of the first data set y values to plot.
    :keyword float y2: list of the second data set y values to plot.
    :keyword float y3: list of the third data set y values to plot.
    :keyword float y4: list of the fourth data set y values to plot.
    :keyword str title: the title for the plot.
    :keyword str xlab: the x axis label for the plot.
    :keyword str ylab: the y axis label for the plot.
    :keyword int ltype: list of the type of line to plot. Options are:
                        1 = step
                        2 = plot
                        3 = histogram
                        4 = date plot
    :keyword str marker: list of the markers to use on the plot. Defaults are:
                         g- = green solid line
                         r- = red solid line
                         b- = blue solid line
                         k- = black dashed line
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
    # WARNING: Refactor load_plot; current McCabe Complexity metric=23.
    axis.cla()

    axis.grid(True, which='both')

    _x_min = min(x_vals)
    _x_max = max(x_vals)
    _y_min = 0.0
    _lst_min = [0.0]
    _lst_max = []
    if y1 is not None:
        if ltype[0] == 1:
            line, = axis.step(x_vals, y1, marker[0], where='mid')
            line.set_ydata(y1)
            _lst_min.append(min(y1))
            _lst_max.append(max(y1))
        elif ltype[0] == 2:
            line, = axis.plot(x_vals, y1, marker[0], linewidth=2)
            line.set_ydata(y1)
            _lst_min.append(min(y1))
            _lst_max.append(max(y1))
        elif ltype[0] == 3:
            axis.grid(False, which='both')
            _values, _edges, __patches = axis.hist(x_vals, bins=y1,
                                                   color=marker[0])
            _x_min = min(_edges)
            _x_max = max(_edges)
            _lst_min.append(min(_values))
            _lst_max.append(max(_values) + 1)
        elif ltype[0] == 4:
            line, = axis.plot_date(x_vals, y1, marker[0],
                                   xdate=True, linewidth=2)
            _lst_min.append(min(y1))
            _lst_max.append(max(y1))
        _y_min = min(y1)

    if y2 is not None:
        if ltype[1] == 1:
            line2, = axis.step(x_vals, y2, marker[1], where='mid')
            line2.set_ydata(y2)
            _lst_min.append(min(y2))
            _lst_max.append(max(y2))
        elif ltype[1] == 2:
            line2, = axis.plot(x_vals, y2, marker[1], linewidth=2)
            line2.set_ydata(y2)
            _lst_min.append(min(y2))
            _lst_max.append(max(y2))
        elif ltype[1] == 3:
            axis.grid(False, which='both')
            _values, _edges, __patches = axis.hist(x_vals, bins=len(y2),
                                                   color=marker[1])
            _x_min = min(_edges)
            _x_max = max(_edges)
            _lst_min.append(min(_values))
            _lst_max.append(max(_values) + 1)
        elif ltype[1] == 4:
            line2, = axis.plot_date(x_vals, y2, marker[1],
                                    xdate=True, linewidth=2)
            _lst_min.append(min(y2))
            _lst_max.append(max(y2))
        _y_min = min(y2)

    if y3 is not None:
        if ltype[2] == 1:
            line3, = axis.step(x_vals, y3, marker[2], where='mid')
            line3.set_ydata(y3)
            _lst_min.append(min(y3))
            _lst_max.append(max(y3))
        elif ltype[2] == 2:
            line3, = axis.plot(x_vals, y3, marker[2], linewidth=2)
            line3.set_ydata(y3)
            _lst_min.append(min(y3))
            _lst_max.append(max(y3))
        elif ltype[2] == 3:
            axis.grid(False, which='both')
            _values, _edges, __patches = axis.hist(x_vals, bins=len(y3),
                                                   color=marker[2])
            _x_min = min(_edges)
            _x_max = max(_edges)
            _lst_min.append(min(_values))
            _lst_max.append(max(_values) + 1)
        elif ltype[2] == 4:
            line3, = axis.plot_date(x_vals, y3, marker[2],
                                    xdate=True, linewidth=2)
            _lst_min.append(min(y3))
            _lst_max.append(max(y3))
        _y_min = min(y3)

    if y4 is not None:
        if ltype[3] == 1:
            line4, = axis.step(x_vals, y4, marker[3], where='mid')
            line4.set_ydata(y4)
            _lst_min.append(min(y4))
            _lst_max.append(max(y4))
        elif ltype[3] == 2:
            line4, = axis.plot(x_vals, y4, marker[3], linewidth=2)
            line4.set_ydata(y4)
            _lst_min.append(min(y4))
            _lst_max.append(max(y4))
        elif ltype[3] == 3:
            axis.grid(False, which='both')
            _values, _edges, __patches = axis.hist(x_vals, bins=len(y4),
                                                   color=marker[3])
            _x_min = min(_edges)
            _x_max = max(_edges)
            _lst_min.append(min(_values))
            _lst_max.append(max(_values) + 1)
        elif ltype[3] == 4:
            line4, = axis.plot_date(x_vals, y4, marker[3],
                                    xdate=True, linewidth=2)
            _lst_min.append(min(y4))
            _lst_max.append(max(y4))
        _y_min = min(y4)

    axis.set_title(title, {'fontsize': 16, 'fontweight': 'bold',
                           'verticalalignment': 'baseline',
                           'horizontalalignment': 'center'})

    # Set the x-axis label.
    _x_pos = (_x_max - _x_min) / 2.0
    _y_pos = _y_min - 0.65
    axis.set_xlabel(xlab, {'fontsize': 14, 'fontweight': 'bold',
                           'verticalalignment': 'center',
                           'horizontalalignment': 'center',
                           'x': _x_pos, 'y': _y_pos})

    # Set the y-axis label.
    axis.set_ylabel(ylab, {'fontsize': 14, 'fontweight': 'bold',
                           'verticalalignment': 'center',
                           'horizontalalignment': 'center',
                           'rotation': 'vertical'})

    # Get the minimum and maximum y-values to set the axis bounds.  If the
    # maximum value is infinity, use the next largest value and so forth.
    _min = min(_lst_min)
    _max = _lst_max[0]
    for i in range(1, len(_lst_max)):
        if _max < _lst_max[i] and _lst_max[i] != float('inf'):
            _max = _lst_max[i]

    axis.set_ybound(_min, _max)

    plot.draw()

    return False


def create_legend(axis, text, fontsize='small', legframeon=False,
                  location='upper right', legncol=1, legshadow=True,
                  legtitle="", lwd=0.5):
    """
    Function to create legends on matplotlib plots.

    :param matplotlib.Axis axis: the axis object to associate the legend with.
    :param tuple text: the text to display in the legend.
    :keyword str fontsize: the size of the font to use for the legend.  Options
                           are:
                           - xx-small
                           - x-small
                           - small (default)
                           - medium
                           - large
                           - x-large
                           - xx-large
    :keyword boolean legframeon: whether or not there is a frame around the
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
    :keyword int legncol: the number columns in the legend.  Default is 1.
    :keyword boolean legshadow: whether or not to display a shadow behind the
                                legend block.  Default is True.
    :keyword str legtitle: the title of the legend.  Default is an emptry
                           string.
    :keyword float lwd: the linewidth of the box around the legend.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _legend = axis.legend(text, frameon=legframeon, loc=location, ncol=legncol,
                          shadow=legshadow, title=legtitle)

    for _text in _legend.get_texts():
        _text.set_fontsize(fontsize)
    for _line in _legend.get_lines():
        _line.set_linewidth(lwd)

    return False


def expand_plot(event):
    """
    Function to display a plot in it's own window.

    :param matplotlib.MouseEvent event: the matplotlib MouseEvent() that called
                                        this method.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _plot = event.canvas
    _parent = _plot.get_parent()

    if event.button == 3:                   # Right click.
        _window = gtk.Window()
        _window.set_skip_pager_hint(True)
        _window.set_skip_taskbar_hint(True)
        _window.set_default_size(800, 400)
        _window.set_border_width(5)
        _window.set_position(gtk.WIN_POS_NONE)
        _window.set_title(_(u"RTK Plot"))

        _window.connect('delete_event', close_plot, _plot, _parent)

        _plot.reparent(_window)

        _window.show_all()

    return False


def close_plot(__window, __event, plot, parent):
    """
    Function to close the plot.

    :param gtk.Window __window: the gtk.Window() that is being destroyed.
    :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this method.
    :param matplotlib.FigureCanvas plot: the matplotlib.FigureCanvas() that was
                                         expanded.
    :param gtk.Widget parent: the original parent gtk.Widget() for the plot.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    plot.reparent(parent)

    return False
