# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name
# -*- coding: utf-8 -*-
#
#       tests.views.gtk3.widgets.test_plot.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the GTK3 plot module algorithms and models."""

# Third Party Imports
import matplotlib
import pytest
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo
from matplotlib.figure import Figure

# RAMSTK Package Imports
from ramstk.views.gtk3.widgets import RAMSTKPlot


class TestRAMSTKPlot():
    """Test class for the RAMSTKPlot."""
    @pytest.mark.gui
    def test_create_plot(self):
        """__init__() should create a RAMSTKPlot."""
        DUT = RAMSTKPlot()

        assert isinstance(DUT, RAMSTKPlot)
        assert isinstance(DUT.figure, Figure)
        assert isinstance(DUT.canvas, FigureCanvasGTK3Cairo)
        assert DUT._lst_max == []
        assert DUT._lst_min == [0.0]

    @pytest.mark.gui
    def test_do_make_date_plot(self):
        """do_load_plot() should create a date plot when passed a plot_type of date."""
        DUT = RAMSTKPlot()

        _x_values = [
            matplotlib.dates.datestr2num('20190701'),
            matplotlib.dates.datestr2num('20190715'),
            matplotlib.dates.datestr2num('20190801'),
            matplotlib.dates.datestr2num('20190815')
        ]
        _y_values = [100.0, 90.0, 75.0, 50.0]

        assert DUT.do_load_plot(_x_values, _y_values, plot_type='date') is None
        assert DUT._lst_min == [0.0, 50.0]
        assert DUT._lst_max == [100.0]

    @pytest.mark.gui
    def test_do_make_histogram(self):
        """do_load_plot() should create a histogram when passed a plot_type of histogram."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9, 1.3, 3.2, 3.4, 2.6]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        assert DUT.do_load_plot(
            _x_values, _y_values, plot_type='histogram', marker='r') is None
        assert DUT._lst_min == [0.0, 2.0]
        assert DUT._lst_max == [4.0]

    @pytest.mark.gui
    def test_do_make_scatter_plot(self):
        """do_load_plot() should create a histogram when passed a plot_type of scatter."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        assert DUT.do_load_plot(
            _x_values, _y_values, plot_type='scatter', marker='bo') is None
        assert DUT._lst_min == [0.0, 1.0]
        assert DUT._lst_max == [4.0]

    @pytest.mark.gui
    def test_do_make_step_plot(self):
        """do_load_plot() should create a histogram when passed a plot_type of step."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        assert DUT.do_load_plot(
            _x_values, _y_values, plot_type='scatter', marker='r-') is None
        assert DUT._lst_min == [0.0, 1.0]
        assert DUT._lst_max == [4.0]

    @pytest.mark.gui
    def test_do_add_line_to_scatter_plot(self):
        """do_add_line() should add a line to a scatter plot."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')

        _x_values = [2.3, 3.2, 4.8, 5.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        assert DUT.do_add_line(_x_values, _y_values) is None

    @pytest.mark.gui
    def test_do_make_x_labels(self):
        """do_make_labels() should add a label to the x-axis of a plot."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')

        _label = DUT.do_make_labels("Test Plot x-Label",
                                    x_pos=1.5,
                                    y_pos=2.5,
                                    fontsize=16,
                                    fontweight='bold')

        assert isinstance(_label, matplotlib.text.Text)
        assert _label.get_fontsize() == 16
        assert _label.get_fontweight() == 'bold'

    @pytest.mark.gui
    def test_do_make_y_labels(self):
        """do_make_labels() should add a label to the y-axis of a plot."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')

        _label = DUT.do_make_labels("Test Plot y-Label",
                                    x_pos=1.5,
                                    y_pos=2.5,
                                    set_x=False,
                                    fontsize=16,
                                    fontweight='bold')

        assert isinstance(_label, matplotlib.text.Text)
        assert _label.get_fontsize() == 16
        assert _label.get_fontweight() == 'bold'

    @pytest.mark.gui
    def test_do_make_legend(self):
        """do_make_legend() should add a legend to a plot with default values."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')

        assert DUT.do_make_legend(("This", "is", "legend", "text")) is None

    @pytest.mark.gui
    def test_do_make_legend_with_kwargs(self):
        """do_make_legend() should add a legend to a plot with passed values."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')

        assert DUT.do_make_legend(("This", "is", "legend", "text"),
                                  fontsize='medium',
                                  frameon=True,
                                  location='lower left',
                                  ncol=2,
                                  shadow=False,
                                  title="Test Title",
                                  lwd=0.25) is None

    @pytest.mark.gui
    def test_do_make_title(self):
        """do_make_title() should add a title to a plot with default values."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')
        _title = DUT.do_make_title("This is a Test Title")

        assert isinstance(_title, matplotlib.text.Text)
        assert _title.get_fontsize() == 16
        assert _title.get_fontweight() == 'bold'

    @pytest.mark.gui
    def test_do_make_title_with_kwargs(self):
        """do_make_title() should add a title to a plot with passed values."""
        DUT = RAMSTKPlot()

        _x_values = [1.4, 1.2, 2.8, 4.9]
        _y_values = [1.0, 2.0, 3.0, 4.0]

        DUT.do_load_plot(_x_values,
                         _y_values,
                         plot_type='scatter',
                         marker='bo')

        _title = DUT.do_make_title("This is a Test Title",
                                   fontsize=8,
                                   fontweight="medium")
        assert isinstance(_title, matplotlib.text.Text)
        assert _title.get_fontsize() == 8
        assert _title.get_fontweight() == 'medium'
