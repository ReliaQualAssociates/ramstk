#!/usr/bin/env python
"""
#####################################################
Software Package Test Selection Matrix Work Book View
#####################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.__gui.gtk.TestSelection.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import Configuration
except ImportError:
    import rtk.Configuration as Configuration

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class CSCITestSelection(gtk.ScrolledWindow):
    """
    The List Book view for analyzing and displaying the Test Selection Matrix
    for a CSCI.  The attributes of a Test Selection Matrix List Book view are:

    :cvar list _lst_test_rankings: the list of CSCI test rankings from
                                   RL-TR-92-52.
    :ivar gtk.TreeView _treeview: the gtk.TreeView() to display the matrix.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` to
                           display in the matrix.
    """

    _lst_test_rankings = [[1, 0, 0, 0, 0, 0, '12', '1', '4', '1', '-', '-', 0,
                           0, ''],
                          [0, 1, 0, 0, 0, 0, '18', '2', '6', '5', '-', '-', 0,
                           0, ''],
                          [0, 0, 1, 0, 0, 0, '16', '3', '2', '2', '-', '-', 0,
                           0, ''],
                          [0, 0, 0, 1, 0, 0, '32', '4', '3', '4', '2', '1', 0,
                           0, ''],
                          [0, 0, 0, 0, 1, 0, '58', '5', '1', '3', '1', '2', 0,
                           0, ''],
                          [0, 0, 0, 0, 0, 1, '44', '5', '5', '6', '3', '3', 0,
                           0, ''],
                          [1, 0, 1, 0, 0, 0, '-', '2', '7', '1', '-', '-', 0,
                           0, ''],
                          [0, 1, 1, 0, 0, 0, '-', '2', '7', '1', '-', '-', 0,
                           0, ''],
                          [1, 1, 0, 0, 0, 0, '-', '1', '1', '3', '-', '-', 0,
                           0, ''],
                          [0, 0, 1, 1, 0, 0, '-', '4', '6', '4', '7', '1', 0,
                           0, ''],
                          [0, 1, 0, 0, 1, 0, '-', '10', '14', '5', '3', '3', 0,
                           0, ''],
                          [1, 0, 0, 0, 1, 0, '-', '10', '14', '5', '3', '3', 0,
                           0, ''],
                          [0, 0, 1, 0, 0, 1, '-', '5', '3', '7', '10', '2', 0,
                           0, ''],
                          [1, 0, 0, 1, 0, 0, '-', '6', '10', '8', '7', '5', 0,
                           0, ''],
                          [0, 1, 0, 1, 0, 0, '-', '6', '9', '9', '7', '5', 0,
                           0, ''],
                          [0, 1, 1, 0, 1, 0, '-', '12', '12', '10', '3', '9',
                           0, 0, ''],
                          [0, 0, 0, 1, 1, 0, '-', '13', '12', '11', '1', '10',
                           0, 0, ''],
                          [1, 0, 0, 0, 0, 1, '-', '8', '3', '12', '10', '7', 0,
                           0, ''],
                          [0, 1, 0, 0, 0, 1, '-', '8', '3', '12', '10', '7', 0,
                           0, ''],
                          [0, 0, 0, 0, 1, 1, '-', '15', '11', '14', '1', '11',
                           0, 0, ''],
                          [0, 0, 0, 1, 0, 1, '-', '13', '2', '15', '6', '12',
                           0, 0, '']]

    def __init__(self):
        """
        Method to initialize a CSCI Test Selection Matrix.
        """

        gtk.ScrolledWindow.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._treeview = gtk.TreeView()
        self._software_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.

    def create_test_planning_matrix(self):
        """
        Method to create the CSCI Test Selection Matrix.
        """

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(self._treeview)

        self._treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # Create and load the Test Matrix for CSCI-level testing.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING)
        self._treeview.set_model(_model)
        self._treeview.set_tooltip_text(_(u"Software module (CSCI) level test "
                                          u"technique selection matrix."))

        _headings = [_(u"Error/Anomaly\nDetection"),
                     _(u"Structure\nAnalysis &amp;\nDocumentation"),
                     _(u"Code\nReviews"), _(u"Functional\nTesting"),
                     _(u"Branch\nTesting"), _(u"Random\nTesting"),
                     _(u"Stopping\nRule (Hours)"), _(u"Average\nEffort"),
                     _(u"Average %\nErrors Found"),
                     _(u"Detection\nEfficiency"),
                     _(u"% Average\nCoverage"), _(u"Coverage\nEfficiency")]

        for i in range(len(_headings[:6])):
            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 0)
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i] + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=i)
            _column.set_clickable(True)
            _column.set_reorderable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(i)
            _column.set_widget(_label)
            self._treeview.append_column(_column)

        for i in range(len(_headings[6:])):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i + 6] + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i + 6)
            _column.set_clickable(True)
            _column.set_reorderable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(i + 6)
            _column.set_widget(_label)
            self._treeview.append_column(_column)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.set_property('xalign', 0.5)
        _cell.set_property('yalign', 0.5)
        _label = gtk.Label()
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_property('angle', 90)
        _label.set_markup("<span weight='bold'>" +
                          _(u"Recommended") +
                          "</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_visible(True)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=12)
        _column.set_clickable(True)
        _column.set_max_width(75)
        _column.set_sort_column_id(12)
        _column.set_widget(_label)
        self._treeview.append_column(_column)

        _cell.connect('toggled', self._on_cell_toggled, 12, _model)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.set_property('xalign', 0.5)
        _cell.set_property('yalign', 0.5)
        _label = gtk.Label()
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_property('angle', 90)
        _label.set_markup("<span weight='bold'>" +
                          _(u"Selected") +
                          "</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_visible(True)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=13)
        _column.set_clickable(True)
        _column.set_max_width(75)
        _column.set_sort_column_id(13)
        _column.set_widget(_label)

        self._treeview.append_column(_column)
        _cell.connect('toggled', self._on_cell_toggled, 13, _model)

        for i in range(len(self._lst_test_rankings)):
            _model.append(self._lst_test_rankings[i])

        self.show_all()

        return False

    def load_test_selections(self, software):
        """
        Method to load the test matrix Recommended and Selected columns for the
        selected CSCI.

        :param software: the :py:class:`rtk.software.Software.Model` to load
                         into the test matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = software

        _model = self._treeview.get_model()
        _row = _model.get_iter_root()

        try:
            _n_selections = len(software.lst_test_selection)
        except TypeError:
            _n_selections = 0

        for i in range(_n_selections):
            _model.set_value(_row, 12, software.lst_test_selection[i][0])
            _model.set_value(_row, 13, software.lst_test_selection[i][1])
            _row = _model.iter_next(_row)

        return False

    def _on_cell_toggled(self, cell, path, position, model):
        """
        Method called whenever a gtk.TreeView() CellRenderer is edited for the
        test selection worksheet.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.Treeview() path of the gtk.CellRenderer() that
                         was edited.
        :param int position: the column position in the Software class
                             gtk.TreeView() of the edited gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        model[path][position] = not cell.get_active()

        if cell.get_active() is not True:
            _selection = 1
        else:
            _selection = 0
        self._software_model.lst_test_selection[int(path)][position - 12] = _selection

        return False


class UnitTestSelection(gtk.ScrolledWindow):
    """
    The List Book view for analyzing and displaying the Test Selection Matrix
    for a Software Unit.  The attributes of a Test Selection Matrix List Book
    view are:

    :cvar list _lst_test_rankings: the list of Unit test rankings from
                                   RL-TR-92-52.
    :ivar gtk.TreeView _treeview: the gtk.TreeView() to display the matrix.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` to
                           display in the matrix.
    """

    _lst_test_rankings = [[1, 0, 0, 0, 0, 0, '6', '2', '2', '1', '-', '-', 'L',
                           'M', '', '', '', '', 'H', '', '', '', 0, 0, ''],
                          [0, 1, 0, 0, 0, 0, '4', '1', '6', '2', '-', '-', '',
                           'L', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 1, 0, 0, 0, '8', '4', '1', '3', '-', '-', 'L',
                           'H', '', 'L', 'H', '', 'L', 'M', '', 'L', 0, 0, ''],
                          [0, 0, 0, 1, 0, 0, '16', '3', '4', '4', '2', '1',
                           'L', 'L', '', 'L', 'H', '', '', 'H', '', 'L', 0, 0,
                           ''],
                          [0, 0, 0, 0, 1, 0, '29', '6', '3', '5', '1', '3',
                           'L', 'M', '', '', 'H', 'L', '', 'H', '', 'L', 0, 0,
                           ''],
                          [0, 0, 0, 0, 0, 1, '22', '5', '5', '6', '2', '2',
                           'L', '', 'L', '', 'M', 'L', '', 'M', '', 'L', 0, 0,
                           ''],
                          [1, 1, 0, 0, 0, 0, '-', '1', '9', '1', '-', '-', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [1, 0, 1, 0, 0, 0, '-', '3', '1', '2', '-', '-', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 1, 1, 0, 0, 0, '-', '2', '7', '3', '-', '-', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [1, 0, 0, 1, 0, 0, '-', '10', '2', '4', '7', '1', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 1, 0, 0, 1, '-', '9', '4', '5', '7', '1', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [1, 0, 0, 0, 0, 1, '-', '5', '5', '6', '7', '1', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [1, 0, 0, 0, 1, 0, '-', '12', '3', '7', '3', '1', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 1, 1, 0, 0, '-', '6', '6', '8', '7', '1', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 0, 1, 0, 1, '-', '7', '10', '8', '6', '1', '',
                           '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 1, 0, 1, 0, 0, '-', '8', '12', '10', '7', '1',
                           '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 0, 0, 1, 1, '-', '13', '11', '11', '1', '1',
                           '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 1, 0, 0, 1, 0, '-', '11', '14', '12', '3', '1',
                           '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 1, 0, 0, 0, 1, '-', '4', '15', '13', '7', '1',
                           '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 1, 0, 1, 0, '-', '15', '8', '14', '37', '11',
                           '', '', '', '', '', '', '', '', '', '', 0, 0, ''],
                          [0, 0, 0, 1, 1, 0, '-', '14', '13', '15', '1', '11',
                           '', '', '', '', '', '', '', '', '', '', 0, 0, '']]

    def __init__(self):
        """
        Method to initialize a Unit Test Selection Matrix.
        """

        gtk.ScrolledWindow.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._treeview = gtk.TreeView()
        self._software_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.

    def create_test_planning_matrix(self):
        """
        Method to create the Unit Test Selection Matrix.
        """

        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.add(self._treeview)

        self._treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # Create and load the Test Matrix for unit-level testing.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING)
        self._treeview.set_model(_model)
        self._treeview.set_tooltip_text(_(u"Software unit-level test "
                                          u"technique selection matrix."))

        _headings = [_(u"Error/Anomaly\nDetection"),
                     _(u"Structure\nAnalysis &amp;\nDocumentation"),
                     _(u"Code\nReviews"), _(u"Functional\nTesting"),
                     _(u"Branch\nTesting"), _(u"Random\nTesting"),
                     _(u"Stopping\nRule (Hours)"), _(u"Average\nEffort"),
                     _(u"Average %\nErrors Found"),
                     _(u"Detection\nEfficiency"),
                     _(u"% Average\nCoverage"),
                     _(u"Coverage\nEfficiency"),
                     _(u"Computational\nErrors"),
                     _(u"Logic\nErrors"), _(u"Data\nInput\nErrors"),
                     _(u"Data\nVerification\nErrors"),
                     _(u"Data\nHandling\nErrors"),
                     _(u"Data\nOutput\nErrors"),
                     _(u"Data\nDefinition\nErrors"),
                     _(u"Interface\nErrors"),
                     _(u"Database\nErrors"), _(u"Other\nErrors")]

        for i in range(len(_headings[:6])):
            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 0)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i] + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=i)
            _column.set_clickable(True)
            _column.set_reorderable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(i)
            _column.set_widget(_label)
            self._treeview.append_column(_column)

        for i in range(len(_headings[6:])):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _headings[i + 6] + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i + 6)
            _column.set_clickable(True)
            _column.set_reorderable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(i + 6)
            _column.set_widget(_label)

            self._treeview.append_column(_column)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _label = gtk.Label()
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_property('angle', 90)
        _label.set_markup("<span weight='bold'>" +
                          _(u"Recommended") + "</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_visible(True)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=22)
        _column.set_clickable(True)
        _column.set_max_width(75)
        _column.set_sort_column_id(22)
        _column.set_widget(_label)

        self._treeview.append_column(_column)
        _cell.connect('toggled', self._on_cell_toggled, 22, _model)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _label = gtk.Label()
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_property('angle', 90)
        _label.set_markup("<span weight='bold'>" +
                          _(u"Selected") + "</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_visible(True)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=23)
        _column.set_clickable(True)
        _column.set_max_width(75)
        _column.set_sort_column_id(23)
        _column.set_widget(_label)
        self._treeview.append_column(_column)

        _cell.connect('toggled', self._on_cell_toggled, 23, _model)
        for i in range(len(self._lst_test_rankings)):
            _model.append(self._lst_test_rankings[i])

        self.show_all()

        return False

    def load_test_selections(self, software):
        """
        Method to load the test matrix Recommended and Selected columns for the
        selected software Unit.

        :param software: the :py:class:`rtk.software.Software.Model` to load
                         into the test matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = software

        _model = self._treeview.get_model()
        _row = _model.get_iter_root()

        try:
            _n_selections = len(software.lst_test_selection)
        except TypeError:
            _n_selections = 0

        for i in range(_n_selections):
            _model.set_value(_row, 22, software.lst_test_selection[i][0])
            _model.set_value(_row, 23, software.lst_test_selection[i][1])
            _row = _model.iter_next(_row)

        return False

    def _on_cell_toggled(self, cell, path, position, model):
        """
        Called whenever a gtk.TreeView() CellRenderer is edited for the
        test selection worksheet.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.Treeview() path of the gtk.CellRenderer() that
                         was edited.
        :param int position: the column position in the Software class
                             gtk.TreeView() of the edited gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        model[path][position] = not cell.get_active()

        if cell.get_active() is not True:
            _selection = 1
        else:
            _selection = 0
        self._software_model.lst_test_selection[int(path)][position - 22] = _selection

        return False
