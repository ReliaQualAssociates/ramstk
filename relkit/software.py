#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to the software of the Program. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2009 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       software.py is part of the RTK Project
#
# All rights reserved.

import sys
import pango

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

# Import other RelKit modules.
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext

# Plotting package.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure


def _worksheet_1_tree_edit(cell, path, new_text, position, model):
    """
    Called whenever a gtk.TreeView CellRenderer is edited for the development
    environment worksheet (Worksheet 1).

    Keyword Arguments:
    cell     -- the gtk.CellRenderer that was edited.
    path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                edited.
    new_text -- the new text in the edited gtk.CellRenderer.
    position -- the column position of the edited gtk.CellRenderer.
    model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
    """

    model[path][position] = not cell.get_active()

    return False


def _worksheet_3_tree_edit(cell, path, new_text, position, model):
    """
    Called whenever a gtk.TreeView CellRenderer is edited for the anomaly
    management worksheet (Worksheet 2).

    Keyword Arguments:
    cell     -- the gtk.CellRenderer that was edited.
    path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                edited.
    new_text -- the new text in the edited gtk.CellRenderer.
    position -- the column position of the edited gtk.CellRenderer.
    model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
    """

    _type_ = gobject.type_name(model.get_column_type(position))

    if(position > 2):
        model[path][position] = not cell.get_active()
    elif(_type_ == 'gchararray'):
        model[path][position] = str(new_text)
    elif(_type_ == 'gint'):
        model[path][position] = int(new_text)
    elif(_type_ == 'gfloat'):
        model[path][position] = float(new_text)

    return False


def _test_selection_tree_edit(cell, path, new_text, position, model):
    """
    Called whenever a gtk.TreeView CellRenderer is edited for the
    test selection worksheet.

    Keyword Arguments:
    cell     -- the gtk.CellRenderer that was edited.
    path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                edited.
    new_text -- the new text in the edited gtk.CellRenderer.
    position -- the column position of the edited gtk.CellRenderer.
    model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
    """

    _type_ = gobject.type_name(model.get_column_type(position))

    if(position != 0 and position != 7):
        model[path][position] = not cell.get_active()
    elif(_type_ == 'gchararray'):
        model[path][position] = str(new_text)
    elif(_type_ == 'gint'):
        model[path][position] = int(new_text)
    elif(_type_ == 'gfloat'):
        model[path][position] = float(new_text)

    return False


def _set_answer(model, row, numerator, denominator, cutoff, criterion):
    """ Function to set 'Y' or 'N' check depending on the ratio of answers to
        previous quantitative questions.

        Keyword Arguments:
        model       -- the gtk.TreeModel containing the questions to be
                       answered.
        row         -- the  gtk.TreeModelRow that is being editted.
        numerator   -- the value of the question taken as the numerator in the
                       ratio.
        denominator -- the value of the question taken as the denominator in
                       the ratio.
        cutoff      -- the cutoff value that the ratio will be compared to when
                       determining whether the 'Y' checkbutton should be set.
        criterion   -- the comparison criterion for the ratio and the cutoff
                       value.
    """

    Yes = 0
    ratio = numerator / denominator
    model.set_value(row, 2, ratio)

    if(criterion == '==' and ratio == cutoff):
        Yes = 1
    if(criterion == '!=' and ratio != cutoff):
        Yes = 1
    elif(criterion == '>' and ratio > cutoff):
        Yes = 1
    elif(criterion == '>=' and ratio >= cutoff):
        Yes = 1
    elif(criterion == '<' and ratio < cutoff):
        Yes = 1
    elif(criterion == '<=' and ratio <= cutoff):
        Yes = 1

    No = Yes * -1 + 1
    model.set_value(row, 3, Yes)
    model.set_value(row, 4, No)
    model.set_value(row, 5, 0)          # Clear the NA field.
    model.set_value(row, 6, 0)          # Clear the UNK field.

    return False


def _test_techniques(button, _parent_):
    """
    Function used to display a gtk.Dialog with the software categories versus
    testing techniques matrix (Table TS201-2 in RL-TR-82-52)

    Keyword Arguments:
    button   -- the gtk.Button that called this function.
    _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Software Categories and Testing Techniques"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Matrix of software categories and test techniques.  Select test techniques with a confidence level less than or equal to the desired test confidence level."))

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn(_("Software Category"))
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=0)
    label = gtk.Label(column.get_title())
    _heading = _("Software Category")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=1)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Code Reviews")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=2)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Error/Anomaly Detection")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=3)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Structure Analysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=4)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Program Quality Analysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=5)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Path Analysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=6)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Domain Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=7)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Partition Analysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=8)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Data-Flow Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=9)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Path Analysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=10)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Performance Measurement")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=11)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Assertion Checking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Debug Aids")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=13)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Random Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=14)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Functional Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=15)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Mutation Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=16)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Real-Time Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=17)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Symbolic Testing")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.pack_start(cell, True)
    column.set_attributes(cell, text=18)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Formal Analysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 450
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = ((_("Batch (General)"), "L", "M", "H", "H", "H", "M", "H", "VH", "H", "M", "H", "H", "VH", "L", "VH", "", "VH", "VH"),
             (_("Event Control"), "L", "L", "M", "M", "M", "M", "VH", "VH", "H", "M", "H", "M", "H", "L", "VH", "H", "VH", "VH"),
             (_("Process Control"), "L", "L", "L", "M", "M", "L", "VH", "H", "M", "M", "H", "M", "H", "L", "VH", "M", "VH", "VH"),
             (_("Procedure Control"), "L", "L", "L", "L", "M", "L", "VH", "H", "M", "M", "M", "L", "H", "L", "H", "M", "H", "VH"),
             (_("Navigation"), "L", "L", "L", "H", "H", "H", "VH", "H", "H", "H", "H", "H", "VH", "L", "VH", "M", "VH", "VH"),
             (_("Flight Dynamics"), "L", "L", "L", "M", "H", "M", "H", "H", "H", "H", "H", "H", "H", "L", "VH", "L", "VH", "VH"),
             (_("Orbital Dynamics"), "L", "L", "L", "M", "H", "M", "M", "H", "H", "H", "M", "L", "H", "L", "H", "M", "H", "VH"),
             (_("Message Processing"), "L", "L", "M", "H", "H", "M", "H", "VH", "H", "H", "H", "M", "H", "L", "VH", "H", "VH", "VH"),
             (_("Diagnostic Software"), "L", "L", "L", "M", "L", "L", "H", "H", "M", "M", "H", "L", "H", "L", "H", "M", "VH", "VH"),
             (_("Sensor & Signal Processing"), "L", "L", "L", "L", "L", "L", "H", "H", "M", "M", "H", "L", "H", "L", "H", "M", "VH", "VH"),
             (_("Simulation"), "M", "M", "VH", "H", "L", "L", "H", "VH", "H", "M", "H", "L", "H", "L", "H", "M", "VH", "VH"),
             (_("Database Maangement"), "L", "L", "M", "M", "H", "L", "M", "H", "M", "M", "H", "M", "H", "L", "VH", "M", "VH", "VH"),
             (_("Data Acquisition"), "L", "L", "L", "H", "H", "L", "VH", "VH", "H", "M", "H", "M", "H", "L", "VH", "M", "VH", "VH"),
             (_("Data Presentation"), "L", "L", "L", "M", "M", "L", "H", "VH", "H", "M", "H", "L", "H", "L", "VH", "M", "H", "VH"),
             (_("Decision & Planning Aids"), "L", "L", "L", "M", "M", "M", "M", "H", "M", "H", "H", "M", "H", "L", "VH", "M", "H", "VH"),
             (_("Pattern & Image Processing"), "L", "L", "L", "M", "M", "L", "M", "H", "M", "H", "H", "L", "H", "L", "VH", "M", "H", "VH"),
             (_("Computer System Software"), "L", "L", "L", "M", "M", "M", "M", "H", "M", "H", "H", "L", "H", "L", "H", "M", "H", "VH"),
             (_("Software Development Tools"), "L", "L", "L", "M", "M", "M", "M", "M", "M", "H", "H", "L", "H", "L", "VH", "", "VH", ""))

    for i in range(len(_data)):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


def _csci_single_matrix(button, _parent_):
    """
    Function used to display a gtk.Dialog with the CSCI single test technique
    rankings based on effort, effectiveness, coverage, and efficiency
    (Table TS203-3 in RL-TR-82-52)

    Keyword Arguments:
    button   -- the gtk.Button that called this function.
    _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Single Test Technique Rankings (CSCI Level)"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Single test technique rankings by effort, effectiveness, coverage, and efficiency (CSCI Level)."))

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=0, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Test Technique")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=1, cell_background=7)
    label = gtk.Label(column.get_title())
    column.set_sort_column_id(1)
    _heading = _("Stopping\nRule\n(Hours)")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=2, cell_background=7)
    label = gtk.Label(column.get_title())
    column.set_sort_column_id(2)
    _heading = _("Average\nEffort\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=3, cell_background=7)
    column.set_sort_column_id(3)
    label = gtk.Label(column.get_title())
    _heading = _("% of Errors\nFound\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=4, cell_background=7)
    label = gtk.Label(column.get_title())
    column.set_sort_column_id(4)
    _heading = _("Detection\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=5, cell_background=7)
    label = gtk.Label(column.get_title())
    column.set_sort_column_id(5)
    _heading = _("% Average\nCoverage\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=6, cell_background=7)
    label = gtk.Label(column.get_title())
    column.set_sort_column_id(6)
    _heading = _("Coverage\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 250
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = (("Error/Anomaly Detection", 12, 1, 4, 1, 0, 0, '#E5E5E5'),
             ("Structure Analysis", 18, 1, 6, 5, 0 , 0, '#FFFFFF'),
             ("Code Review", 16, 3, 2, 2, 0 , 0, '#E5E5E5'),
             ("Functional Testing", 32, 4, 3, 4, 2, 1, '#FFFFFF'),
             ("Branch Testing", 58, 5, 1, 3, 1 , 2, '#E5E5E5'),
             ("Random Testing", 44, 5, 5, 6, 3, 3, '#FFFFFF'))

    n_records = len(_data)
    for i in range(n_records):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


def _csci_paired_matrix(button, _parent_):
    """
    Function used to display a gtk.Dialog with the CSCI paired test technique
    rankings based on effort, effectiveness, coverage, and efficiency
    (Table TS203-4 in RL-TR-82-52)

    Keyword Arguments:
    button   -- the gtk.Button that called this function.
    _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Paired Test Technique Rankings (CSCI Level)"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Paired test technique rankings by effort, effectiveness, coverage, and efficiency (CSCI Level)."))
    treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=0, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Category")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=1, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Error\Anomaly\nDetection")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=2, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Code\nReview")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=3, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Functional\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=4, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Branch\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=5, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Random\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=6, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Structure\nAnalysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=7, cell_background=12)
    column.set_sort_column_id(7)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Average\nEffort\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=8, cell_background=12)
    column.set_sort_column_id(8)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("% of Errors\nFound\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=9, cell_background=12)
    column.set_sort_column_id(9)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Detection\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=10, cell_background=12)
    column.set_sort_column_id(10)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("% Average\nCoverage\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=11, cell_background=12)
    column.set_sort_column_id(11)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Coverage\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 250
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = ((1, "X", "X", " ", " ", " " , " ", 2, 7, 1, 0, 0, '#E5E5E5'),
             (1, " ", "X", " ", " ", " " , "X", 2, 7, 1, 0, 0, '#FFFFFF'),
             (1, "X", " ", " ", " ", " " , "X", 1, 1, 3, 0, 0, '#E5E5E5'),
             (2, " ", "X", "X", " ", " " , " ", 4, 6, 4, 7, 1, '#FFFFFF'),
             (2, " ", " ", " ", "X", " " , "X", 10, 14, 5, 3, 3, '#E5E5E5'),
             (2, "X", " ", " ", "X", " " , " ", 10, 14, 5, 3, 3, '#FFFFFF'),
             (2, " ", "X", " ", " ", "X" , " ", 5, 3, 7, 10, 2, '#E5E5E5'),
             (2, "X", " ", "X", " ", " " , " ", 6, 10, 8, 7, 5, '#FFFFFF'),
             (2, " ", " ", "X", " ", " " , "X", 6, 9, 9, 7, 5, '#E5E5E5'),
             (3, " ", "X", " ", "X", " " , "X", 12, 12, 10, 3, 9, '#FFFFFF'),
             (3, " ", " ", "X", "X", " " , "X", 13, 12, 11, 1, 10, '#E5E5E5'),
             (3, "X", " ", " ", " ", "X" , " ", 8, 3, 12, 10, 7, '#FFFFFF'),
             (3, " ", " ", " ", " ", "X" , "X", 8, 3, 12, 10, 7, '#E5E5E5'),
             (3, " ", " ", " ", "X", "X" , " ", 15, 11, 14, 1, 11, '#FFFFFF'),
             (4, " ", " ", "X", " ", "X" , " ", 13, 2, 15, 6, 12, '#E5E5E5'))

    n_records = len(_data)
    for i in range(n_records):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


def _unit_single_matrix(button, _parent_):

    """ Function used to display a gtk.Dialog with the unit single test
        technique rankings based on effort, effectiveness, coverage, and
        efficiency (Table TS203-1 in RL-TR-82-52)

        Keyword Arguments:
        button   -- the gtk.Button that called this function.
        _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Single Test Technique Rankings (Unit Level)"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Single test technique rankings by effort, effectiveness, coverage, and efficiency (Unit Level)."))

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=0, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Test Technique")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=1, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Stopping\nRule\n(Hours)")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=2, cell_background=7)
    column.set_sort_column_id(2)
    label = gtk.Label(column.get_title())
    _heading = _("Average\nEffort\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=3, cell_background=7)
    column.set_sort_column_id(3)
    label = gtk.Label(column.get_title())
    _heading = _("% of Errors\nFound\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=4, cell_background=7)
    column.set_sort_column_id(4)
    label = gtk.Label(column.get_title())
    _heading = _("Detection\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=5, cell_background=7)
    column.set_sort_column_id(5)
    label = gtk.Label(column.get_title())
    _heading = _("% Average\nCoverage\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=6, cell_background=7)
    column.set_sort_column_id(6)
    label = gtk.Label(column.get_title())
    _heading = _("Coverage\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 250
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = (("Error/Anomaly Detection", 6, 2, 2, 1, 0, 0, '#E5E5E5'),
             ("Structure Analysis", 4, 1, 6, 2, 0, 0, '#FFFFFF'),
             ("Code Review", 8, 4, 1, 3, 0, 0, '#E5E5E5'),
             ("Functional Testing", 16, 3, 4, 4, 2 , 1, '#FFFFFF'),
             ("Branch Testing", 29, 6, 3, 5, 1, 3, '#E5E5E5'),
             ("Random Testing", 22, 5, 5, 6, 2, 2, '#FFFFFF'))

    n_records = len(_data)
    for i in range(n_records):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


def _unit_paired_matrix(button, _parent_):
    """
    Function used to display a gtk.Dialog with the unit paired test technique
    rankings based on effort, effectiveness, coverage, and efficiency
    (Table TS203-2 in RL-TR-82-52)

    Keyword Arguments:
    button   -- the gtk.Button that called this function.
    _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Paired Test Technique Rankings (Unit Level)"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_INT, gobject.TYPE_INT,
                          gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Paired test technique rankings by effort, effectiveness, coverage, and efficiency (Unit Level)."))
    treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=0, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Category")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=1, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Error\Anomaly\nDetection")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=2, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Code\nReview")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=3, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Functional\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=4, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Branch\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=5, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Random\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=6, cell_background=12)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Structure\nAnalysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=7, cell_background=12)
    column.set_sort_column_id(7)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Average\nEffort\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=8, cell_background=12)
    column.set_sort_column_id(8)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("% of Errors\nFound\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=9, cell_background=12)
    column.set_sort_column_id(9)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Detection\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=10, cell_background=12)
    column.set_sort_column_id(10)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("% Average\nCoverage\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=11, cell_background=12)
    column.set_sort_column_id(11)
    label = gtk.Label(column.get_title())
    label.set_property('angle', 90)
    _heading = _("Coverage\nEfficiency\nRanking")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 250
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = ((1, "X", " ", " ", " ", " " , "X", 1, 9, 1, 0, 0, '#E5E5E5'),
             (1, "X", "X", " ", " ", " " , " ", 3, 1, 2, 0, 0, '#FFFFFF'),
             (1, " ", "X", " ", " ", " " , "X", 2, 7, 3, 0, 0, '#E5E5E5'),
             (2, "X", " ", "X", " ", " " , " ", 10, 2, 4, 7, 1, '#FFFFFF'),
             (2, " ", "X", " ", " ", "X" , " ", 9, 4, 5, 7, 3, '#E5E5E5'),
             (2, "X", " ", " ", " ", "X" , " ", 5, 5, 6, 7, 3, '#FFFFFF'),
             (2, "X", " ", " ", "X", " " , " ", 12, 3, 7, 3, 2, '#E5E5E5'),
             (2, " ", "X", "X", " ", " " , " ", 6, 6, 8, 7, 5, '#FFFFFF'),
             (3, " ", " ", "X", " ", "X" , " ", 7, 10, 9, 6, 9, '#E5E5E5'),
             (3, " ", " ", "X", " ", " " , "X", 8, 12, 10, 7, 10, '#FFFFFF'),
             (3, " ", " ", " ", "X", "X" , " ", 13, 11, 11, 1, 7, '#E5E5E5'),
             (3, " ", " ", " ", "X", " " , "X", 11, 14, 12, 3, 7, '#FFFFFF'),
             (3, " ", " ", " ", " ", "X" , "X", 4, 15, 13, 7, 11, '#E5E5E5'),
             (4, " ", "X", " ", "X", " " , " ", 15, 8, 14, 3, 12, '#FFFFFF'),
             (4, " ", " ", "X", "X", " " , " ", 14, 13, 15, 1, 12, '#E5E5E5'))

    n_records = len(_data)
    for i in range(n_records):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


def _test_effectiveness(button, _parent_):

    """ Function used to display a gtk.Dialog with the test technique
        effectiveness versus error category matrix
        (Table TS203-6 in RL-TR-82-52)

        Keyword Arguments:
        button   -- the gtk.Button that called this function.
        _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Test Techniques Effectiuveness by Error Category"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Matrix of testing effectiveness by error category."))
    treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=0, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Error\nCategory")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=1, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Code\nReview")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=2, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Error/Anomaly\nDetection")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=3, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Structure\nAnalysis")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=4, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Random\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=5, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Functional\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=6, cell_background=7)
    label = gtk.Label(column.get_title())
    _heading = _("Branch\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 250
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = (("Computational Errors", "L", "L", " ", "L", "L", "L", '#E5E5E5'),
             ("Logic Errors", "H", "M", "L", " ", "L", "M", '#FFFFFF'),
             ("Data Input Errors", " ", " ", " ", "L", " ", " ", '#E5E5E5'),
             ("Data Verification Errors", "L", " ", " ", " ", "L", " ", '#FFFFFF'),
             ("Data Handling Errors", "H", " ", " ", "M", "H", "H", '#E5E5E5'),
             ("Data Output Errors", " ", " ", " ", "L", " ", "L", '#FFFFFF'),
             ("Interface Errors", "M", " ", " ", "M", "H", "H", '#E5E5E5'),
             ("Data Definition Errors", "L", "H", " ", " ", " ", " ", '#FFFFFF'),
             ("Database Errors", " ", " ", " ", " ", " ", " ", '#E5E5E5'),
             ("Other Errors", " ", " ", " ", " ", " ", " ", '#FFFFFF'))

    n_records = len(_data)
    for i in range(n_records):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


def _test_stopping_rules(button, _parent_):

    """ Function used to display a gtk.Dialog with the test technique
        effectiveness versus error category matrix
        (Table TS203-6 in RL-TR-82-52)

        Keyword Arguments:
        button   -- the gtk.Button that called this function.
        _parent_ -- the parent widget for this dialog.
    """

    dialog = gtk.Dialog(title=_("Test Stopping Rules"),
                        parent=_parent_,
                        flags=(gtk.DIALOG_DESTROY_WITH_PARENT),
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

    dialog.set_has_separator(True)

    model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_STRING)
    treeview = gtk.TreeView(model)
    treeview.set_tooltip_text(_("Stopping rules for various test techniques."))
    treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=0, cell_background=4)
    label = gtk.Label(column.get_title())
    _heading = _("Test\nTechnique")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    cell.set_property('wrap-width', 150)
    cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=1, cell_background=4)
    label = gtk.Label(column.get_title())
    _heading = _("Stopping\nRule")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=2, cell_background=4)
    label = gtk.Label(column.get_title())
    _heading = _("Unit Level\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    cell = gtk.CellRendererText()
    cell.set_property('editable', 0)
    column = gtk.TreeViewColumn()
    column.set_visible(1)
    column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
    column.set_resizable(True)
    column.pack_start(cell, False)
    column.set_attributes(cell, text=3, cell_background=4)
    label = gtk.Label(column.get_title())
    _heading = _("CSCI Level\nTesting")
    label.set_markup("<span weight='bold'>" + _heading + "</span>")
    label.show_all()
    column.set_widget(label)
    treeview.append_column(column)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.add(treeview)
    scrollwindow.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.props.height_request = 250
    frame.props.width_request = 750
    frame.add(scrollwindow)

    frame.show_all()

    _data = (("Code Review", "All required aspects of the method have been evaluated using SDDL where possible, manually where not.  Not to exceed X hours.", "X = 8", "X = 16", '#E5E5E5'),
             ("Error/Anomaly Detection", "All required aspects of the method have been evaluated using automated tools where possible, manually where not.  Not to exceed X hours.", "X = 6", "X = 12", '#FFFFFF'),
             ("Structure Analysis", "All required aspects of the method have been evaluated using automated tools where possible, manually where not.  Not to exceed X hours.", "X = 4", "X = 8", '#E5E5E5'),
             ("Random Testing", "Minimum number, Y, sampled from input space.  Not to exceed X hours.", "X = 22\nY = 25", "X = 44\nY = 50", '#FFFFFF'),
             ("Functional Testing", "All test procedures executed.  Not to exceed X hours.", "X = 16", "X = 32", '#FFFFFF'),
             ("Branch Testing", "100% of branches tested (with a minimum of two traversals per branch).  Not to exceed X hours.", "X = 29", "X = 58", '#E5E5E5'))

    n_records = len(_data)
    for i in range(n_records):
        model.append(None, _data[i])

    dialog.vbox.pack_start(frame)

    response = dialog.run()
    if(response == gtk.RESPONSE_ACCEPT):
        dialog.destroy()


class Software:

    # TODO: Write code to update notebook widgets when editing the
    # System treeview.

    """ The Software class is simply the treeview that holds and displays
        the system tree in the RelKit Treebook.
    """

    _gd_tab_labels = [[_("Module Description:"), _("Application Level:"),
                      _("Application Type:"), _("Development Environment:"),
                      _("Development Phase:")], [_("Test Confidence Level:"),
                      _("Test Selection Path:"), _("Software Category:"),
                      _("Test Techniques:")]]

    _ws1_tab_labels = [_("There are separate design and coding organizations."),
                       _("There is an independent software test organization."),
                       _("There is an independent software quality assurance organization."),
                       _("There is an independent software configuration management organization."),
                       _("There is an independent software verification and validation organization."),
                       _("A structured progamming team will develop the software."),
                       _("The educational level of the programming team members is above average."),
                       _("The experience level of teh programming team members is above average."),
                       _("Standards are defined and will be enforced."),
                       _("Software will be developed using a higher order language."),
                       _("The development process will include formal reviews (PDR, CDR, etc.)."),
                       _("The development process will include frequent walkthroughs."),
                       _("Development will take a top-down and structured approach."),
                       _("Unit development folders will be used."),
                       _("A software development library will be used."),
                       _("A formal change and error reporting process will be used."),
                       _("Progress and status will routinely be reported."),
                       _("System requirements specifications will be documented."),
                       _("Software requirements specifications will be documented."),
                       _("Interface design specifications will be documented."),
                       _("Software design specification will be documented."),
                       _("Test plans, procedures, and reports will be documented."),
                       _("The software development plan will be documented."),
                       _("The software quality assurance plan will be documented."),
                       _("The software configuration management plan will be documented."),
                       _("A requirements traceability matrix will be used."),
                       _("The software version description will be documented."),
                       _("All software discrepancies will be documented."),
                       _("The software language requirements will be specified."),
                       _("Formal program design language will be used."),
                       _("Program design graphical techniques (flowcharts, HIPO, etc.) will be used."),
                       _("Simulation/emulation tools will be used."),
                       _("Configuration management tools will be used."),
                       _("A code auditing tool will be used."),
                       _("A data flow analyzer will be used."),
                       _("A programmer's workbench will be used."),
                       _("Measurement tools will be used."),
                       _("Software code reviews will be used."),
                       _("Software branch testing will be used."),
                       _("Random testing will be used."),
                       _("Functional testing will be used."),
                       _("Error and anomaly detection testing will be used."),
                       _("Structure analysis will be used.")]

    _ws2_tab_labels = [[_("How many instances are there of different processes (or functions, subfunctions) which are required to be executed at the same time?"),
                        _("How many instances of concurrent processing are required to be centrally controlled?"),
                        _("How many error conditions are required to be recognized?"),
                        _("How many recognized error conditions require recover or repair?"),
                        _("Is there a standard for handling recognized errors such that all error conditions are passed to the calling function or software element?"),
                        _("How many instances exist of the same process (or function, subfunction) being required to execute more than once for comparison purposes (e.g., polling of parallel or redundant processing results)?"),
                        _("How many instances of parallel/redundant processing are required to be centrally controlled?"),
                        _("Are error tolerances specified for all applicable external input data (i.e., range of numerical values, legal combinations of alphanumerical values)?"),
                        _("Are there requirements for detection of and/or recovery from all computational failures?"),
                        _("Are there requirements to range test all critical loop and multiple transfer index parameters before used?"),
                        _("Are there requirements to range test all critical subscript values before use?"),
                        _("Are there requirements to range test all critical output data before final outputting?"),
                        _("Are there requirements for recovery from all detected hardware faults?"),
                        _("Are there requirements for recovery from all I/O divide errors?"),
                        _("Are there requirements for recovery from all communication transmission errors?"),
                        _("Are there requirements for recovery from all failures to communicate with other modes or other systems?"),
                        _("Are there requirements to periodically check adjscent nodes or interoperating system for operational status?"),
                        _("Are there requirements to provide a strategy for alternating routing of messages?"),
                        _("Are there requirements to ensure communication paths to all remaining nodes/communication links in the event of a failure of one node/link?"),
                        _("Are there requirements for maintaining the integrity of all data values following the occurence of anomalous conditions?"),
                        _("Are there requirements to enable all disconnected nodes to rejoin the network after recovery, such that the processing functions of the system are not interrupted?"),
                        _("Are there requirements to replicate all cricital data in the CSCI at two or more distinct nodes?")],
                       [_("Are there provisions for recovery from all computational failures?"),
                        _("Are there provisions for recovery from all detected hardware faults?"),
                        _("Are there provisions for recovery from all I/O device errors?"),
                        _("Are there provisions for recovery from all communication transmission errors?"),
                        _("Is error checking information (e.g., checksum, parity bit) computed and transmitted with all messages?"),
                        _("Is error checking information computed and compared with all message receptions?"),
                        _("Are transmission retries limited for all transmissions?"),
                        _("Are there provisions for recovery from all failures to communicate with other nodes or other systems?"),
                        _("Are there provisions to periodically check all adjacent nodes or interoperating systems for operational status?"),
                        _("Are there provisions for alternate routing of messages?"),
                        _("Do communication paths exist to all remaining nodes/links in the event of a failure of one node/link?"),
                        _("Is the integrity of all data values maintained following the occurence of anomalous conditions?"),
                        _("Can all disconnected nodes rejoin the network after recovery, such that the processing functions of the system are not interrupted?"),
                        _("Are all critical data in the system (or CSCI) replicated at two or more distinct nodes, in accordance with specified requirements?")],
                       [_("When an error condition is detected, is resolution of the error determined by the calling unit?"),
                        _("Is a check performed before processing begins to determine that all data is available?")],
                       [_("How many units in the CSCI?"),
                        _("For how many units, when an error condition is detected, is resolution of the error not determined by the calling unit?"),
                        _("Are values of all applicable external inputs with range specifications checked with respect to specified range prior to use?"),
                        _("Are all applicable external inputs checked with respect to specified conflicting requests prior to use?"),
                        _("Are all applicable external inputs checked with respect to illegal combinations prior to use?"),
                        _("Are all applicable external inputs checked for reasonableness before processing begins?"),
                        _("Are all detected errors, with respect to applicable external inputs, reported before processing begins?"),
                        _("How many units in the CSCI?"),
                        _("How many units do not perform a check to determine thaa all data is available before processing begins?"),
                        _("Are critical loop and multiple transfer index parameters checked for out-of-range values before use?"),
                        _("Are all critical subscripts checked for out-of-range values before use?"),
                        _("Are all critical output data checked for reasonable values prior to final outputting?")]]

    _ws3_tab_labels = [[_("There is a table tracing all of the CSCI's allocated requirements to the parent system or the subsystem specification.")],
                       [_("There is a table tracing all the top-level CSC allocated requirements to the parent CSCI specification.")],
                       [_("The description of each software unit identifies all the requirements that the unit helps satisfy."),
                        _("The decomposition of top-level CSCs into lower-level CSCs and software units is graphically depicted.")]]

    _ws4_tab_labels = [[_("Are there quantitative accuracy requirements for all applicable inputs associated with each applicable function?"),
                        _("Are there quantitative accuracy requirements for all applicable outputs associated with each applicable function?"),
                        _("Are there quantitative accuracy requirements for all applicable constants associated with each applicable function?"),
                        _("Do the existing math library routines which are planned for use provide enough precision to support accuracy objectives?"),
                        _("Are all processes and functions partitioned to be logically complete and self contained so as to minimize interface complexity?"),
                        _("Are there requirements for each operational CPU/System to have a separate power source?"),
                        _("Are there requirements for the executive software to perform testing of its own operation and of the communication links, memory devices, and peripheral devices?"),
                        _("Are all inputs, processing, and outputs clearly and precisely defined?"),
                        _("How many data references are identified?"),
                        _("How many identified data references are documented with regard to source, meaning, and format?"),
                        _("How many data items are defined?"),
                        _("How many data items are referenced?"),
                        _("Have all defined functions been referenced?"),
                        _("Have all system functions allocated to this CSCI been allocated to software functions within this CSCI?"),
                        _("Have all referenced functions been defined?"),
                        _("Is the flow of processing (algorithms) and all decision points (conditions and alternate paths) in the flow described for all functions?"),
                        _("Have specific standards been established for design representations (e.g., HIPO charts, program design language, flow charts, data flow diagrams)?"),
                        _("Have specific standards been established for calling sequence protocol between software units?"),
                        _("Have specific standards been established for external I/O protocol and format for all software units?"),
                        _("Have specific standards been established for error handling for all software units?"),
                        _("Do all references to the same CSCI function use a single, unique name?"),
                        _("Have specific standards been established for all data representation in the design?"),
                        _("Have specific standards been established for the naming of all data?"),
                        _("Have specific standards been established for the definition and use of global variables?"),
                        _("Are there procedures for establishing consistency and concurrency of multiple copies of the same software or data base version?"),
                        _("Are there procedures for verifying consistency and concurrency of multiple copies of the same software or data base version?"),
                        _("Do all references to the same data use a single, unique name?")],
                       [_("Do the numerical techniques used in implementing applicable functions provide enough precision to support accuracy objectives?"),
                        _("Are all processes and functions partitioned to be logically complete and self-contained so as to minimize interface complexity?"),
                        _("How much estimated processing time is typically spent executing the entire CSCI?"),
                        _("How much estimated processing time is typically spent in execution of hardware and device interface protocol?"),
                        _("Does the executive software perform testing of its own operation and of the communication links, memory devices, and peripheral devices?"),
                        _("Are all inputs, processing, and outputs clearly and precisely defined?"),
                        _("How many data references are defined?"),
                        _("How many identified data references are documented with regard to source, meaning, and format?"),
                        _("How many data items are defined (i.e., documented with regard to source, meaning, and format)?"),
                        _("How many data items are referenced?"),
                        _("How many data references are identified?"),
                        _("How many identified data references are computed or obtained from an external source?"),
                        _("Have all functions for this CSCI been allocated to top-level CSCs of this CSCI?"),
                        _("Are all conditions and alternative processing options defined for each decision point?"),
                        _("How many software discrepancy reports have been recorded, to date?"),
                        _("How many recorded software problem reports have been closed?"),
                        _("Are the design representations in the formats of the established standard?"),
                        _("Do all references to the same top-level CSC use a single, unique name?"),
                        _("Does all data representation comply with the established standard?"),
                        _("Does the naming of all data comply with the established standard?"),
                        _("Is the definition and use of all global variables in accordange with the established standard?"),
                        _("Are there procedures for establishing consistency and concurrency of multiple copies of the same software or data base version?"),
                        _("Are there procedures for verifying the consistency and concurrency of multiples copies of the same software or data base version?"),
                        _("Do all references to the same data use a single, unique name?")],
                       [_("Are all inputs, processing, and outputs clearly and precisely defined?"),
                        _("Are all data references defined?"),
                        _("How many identified data references are documented with regard to source, meaning, and format?"),
                        _("Are all conditions and alternative processing options defined for each decision point?"),
                        _("Are all parameters in the argument list used?"),
                        _("Are all design representations in teh formats of the established standard?"),
                        _("Does the calling sequence protocol (between units) comply with the established standard?"),
                        _("Does the I/O protocol and format comply with the established standard?"),
                        _("Does the handling of errors comply with the established standard?"),
                        _("Do all references to this unit use the same, unique name?"),
                        _("Does all data representation comply with the established standard?"),
                        _("Does the naming of all data comply with the established standard?"),
                        _("Is the definition and use of all global variables in accordance with the established standard?"),
                        _("Do all references to the same data use a single, unique name?")],
                       [_("How many estimated executable lines of source code?"),
                        _("How many estimated executable lines of source code necessary to handle hardware and device interface protocol?"),
                        _("How many units in the CSCI?"),
                        _("How many units perform processing of hardware and/or device interface protocol?"),
                        _("How much estimated processing time is typically spent executing the entire CSCI?"),
                        _("How much estimated processing time is typically spent in execution of hardware and devie interface protocol units?"),
                        _("How many units clearly and precisely define all inputs, processing, and outputs?"),
                        _("How many data references are identified?"),
                        _("How many identified data references are documented with regard to source, meaning, and format?"),
                        _("How many data items are defined?"),
                        _("How many data items are referenced?"),
                        _("How many data references are identified?"),
                        _("How many identified data references are computed or obtained from an external source?"),
                        _("How many units define all conditions and alternative processing options for each decision point?"),
                        _("For how many units are all parameters in the argument list used?"),
                        _("How many software problem reports have been recorded to date?"),
                        _("How many software problem reports have been resolved to date?"),
                        _("For how many units are all design representations in the formats of the established standard?"),
                        _("For how many units does the calling sequence protocol comply with the established standard?"),
                        _("For how many units does the I/O protocol and format comply with the established standard?"),
                        _("For how many units does the handling of errors comply with the established standard?"),
                        _("For how many units do all references to the unit use the same, unique name?"),
                        _("For how many units does data representation comply with the established standard?"),
                        _("For how many units does the naming of all data comply with the established standard?"),
                        _("For how many units is the definition and use of all global variables in accordance with the established standard?"),
                        _("For how many units do all references to the same data use a single, unique name?")]]

    _ws8_tab_label = [_("How many executable lines of code (SLOC) are present in this unit?"),
                      _("How many assembly language lines of code (ALOC) are present in this unit?"),
                      _("How many higher order language lines of code (HLOC) are present in this unit?"),
                      _("How many conditional branch statements in this unit (IF, WHILE, REPEAT, DO LOOP, FOR LOOP, CASE)?"),
                      _("How many unconditional branch statements in this unit (GO TO, CALL, RETURN)?")]

    _ws9_tab_label = [_("How many executable lines of code (SLOC) are present in this CSCI?"),
                      _("How many assembly lines of code (ALOC) are present in this CSCI?"),
                      _("How many higher order language lines of code (HLOC) are present in this CSCI?"),
                      _(u"For how many units in this CSCI is sx > 20?"),
                      _(u"For how many units in this CSCI is 7 \u2264 sx \u2264 20?"),
                      _(u"For how many units in this CSCI is sx less than 7?"),
                      _(u"How many total units (NM) are present in this CSCI?"),
                      _(u"For how many units in the system is SLOC \u2264 200?"),
                      _(u"For how many units in the system is 200 \u2264 SLOC \u2264 3000?"),
                      _(u"For how many units in the sustem is SLOC \u003E 3000?")]

    _ws11_tab_labels = [[_("Are the estimated lines of source code (MLOC) for this unit 100 lines or less?"),
                         _("How many parameters are there in teh calling sequence?"),
                         _("How many calling sequence parameters are control variables (e.g., select an operating mode or submode, direct the sequential flow, directly influence the function of the software)?"),
                         _("Is all data passed into the unit through calling sequence parameters (i.e., no data is input through global area or input statements)?"),
                         _("Is output data passed back to the calling unit through calling sequence parameters (i.e., not data is output through global areas)?"),
                         _("Is control always returned to the calling unit when execution is completed?"),
                         _("Is temporary storage (i.e., workspace reserved for intermediate or partial results) used only by this unit during execution (i.e., is not shared with other units)?"),
                         _("Does this unit have a single processing objective (i.e., all processing within this unit is related to the same objective)?"),
                         _("Is the unit independent of the source of the input and the destination of the output?"),
                         _("Is the unit independent of the knowledge of prior processing?"),
                         _("Does the unit description/prologue include input, output, processing, and limitations?"),
                         _("How many entrances into the unit?"),
                         _("How many exits from the unit?"),
                         _("Does the description of this unit identify all interfacing units and all interfacing hardware?"),
                         _("Is the flow control from top to bottom (i.e., flow of control does not jump erratically)?"),
                         _("How many negative boolean and compound boolean expressions are used?"),
                         _("How many loops (e.g., WHILE, DO/FOR, REPEAT)?"),
                         _("How many loops with unnatural exits (e.g., jump out of loop, return statement)?"),
                         _("How many iteration loops (e.g., DO/FOR loops)?"),
                         _("In how many iteration loops are indices modified to alter the fundamental processing of the loop?"),
                         _("Is the unit free from all self-modification of code (i.e., does not alter instructions, overlays of code, etc.)?"),
                         _("How many statement labels, excluding labels for format statements?"),
                         _("What is the maximum nesting level?"),
                         _("How many branches, conditional and unconditional?"),
                         _("How many data declaration statements?"),
                         _("How many data manipulation statements?"),
                         _("How many total data item, local and global, are used?"),
                         _("How many data items are used locally (e.g., variables declared locally and value parameters)?"),
                         _("Does each data item have a single use (e.g., each array serves only one purpose)?"),
                         _("Is this unit coded according to the required programming standard?"),
                         _("How many data items are used as input?"),
                         _("How many data items are used for output?"),
                         _("How many parameters in the unit's calling sequence return output values?'"),
                         _("Does the unit perform a single, nondivisible function?")],
                        [_("Are all units coded and tested according to structural techniques?"),
                         _("How many units in CSCI?"),
                         _("How many units with estimated executable lines of source code less than 100 lines?"),
                         _("How many parameters are there in the calling sequence?"),
                         _("How many calling sequence parameters are control variables (e.g., select an operating mode or submode, direct the sequential flow, directly influence the function of the software)?"),
                         _("For how many units is all input data passed into the unit through calling sequence parameters (i.e., no data is input through global areas or input statements)?"),
                         _("For how many units is output data passed back to the calling unit through calling sequence parameters (i.e., no data is output through global areas)?"),
                         _("For how many units is control always returned to the calling unit when execution is completed?"),
                         _("For how many units is temporary storage (i.e., workspace reserved for immediate or partial results) used only by the unit during execution (i.e., is not shared with other units)?"),
                         _("How many units have a single processing objective (i.e., all processing within the unit is related to the same objective)?"),
                         _("How many units are independent of the source of the input and the destination of the output?"),
                         _("How many units are independent of knowledge of prior processing?"),
                         _("For how many units does the description/prologue include input, output, processing, and limitations?"),
                         _("How many units have only one entrance and one exit?"),
                         _("How many units are in common blocks?"),
                         _("How many common blocks?"),
                         _("Do all descriptions of all units identify all interfacing units and all interfacing hardware?"),
                         _("How many units are implemented in a structured language or using a preprocessor?"),
                         _("For how many units is the flow of control from top to bottom (i.e., flow of control does not jump erratically)?"),
                         _("How many executable lines of code in this CSCI?"),
                         _("How many negative boolean and compound boolean expressions are used?"),
                         _("How many loops (e.g., WHILE, DO/FOR, REPEAT)?"),
                         _("How many loops with unnatural exits (e.g., jumps out of loopw, return statement)?"),
                         _("How many iteration loops (i.e., DO/FOR loops)?"),
                         _("In how many iteration loops are indices modified to alter fundamental processing of the loop?"),
                         _("How many units are free from all self-modification of code (i.e., does not alter instructions, overlays of code, etc.)?"),
                         _("How many statement labels, excluding labels for format statements?"),
                         _("What is the maximum nesting level?"),
                         _("How many branches, conditional and unconditional?"),
                         _("How many declaration statements?"),
                         _("How many data manipulation statements?"),
                         _("How many total data items, local and global, are used?"),
                         _("How many data items are used locally (e.g., variables declared locally and value parameters)?"),
                         _("For how many units does each data item have a single use?"),
                         _("How many units are coded according to the required programming standard?"),
                         _("Is repeated and redundant coede avoided (e.g., through utilizing macros, functions, and procudres)?"),
                         _("How many data item are as input?"),
                         _("How many data items are used as inputs?"),
                         _("How many parameters in the units' calling sequence return outout values?'"),
                         _("How many units perform a single, non-diivisible function?")]]

    _ar_tab_labels = [_("Application Type Factor (A)."),
                      _("Number of Development Characteristics (De)."),
                      _("Fraction of Development Characteristics Not Used (Dc)"),
                      _("Development Environment Factor (D = f(Dc))"),
                      _("Fraction of Anomaly Management Tools Not Used (AM)."),
                      _("Software Anomaly Management Factor (SA = f(AM))"),
                      _("Fraction of Requirements Analysis Tools Not Used (DR)."),
                      _("Software Requirements Traceability Factor (ST = f(DR))"),
                      _("Software Quality Factor (SQ)."),
                      _("Requirements and Design Representation Metric (S1 = SA*ST*SQ)"),
                      _("Number of Higher Order Language lines of Code (HLOC)"),
                      _("Number of Assembly Language Lines of Code (ALOC)"),
                      _("Total Number of Executable Lines of Code (SLOC)"),
                      _("Software Language Type Factor (SL = f(HLOC,ALOC))."),
                      _("Total Number of Modules in CSCI (NM)"),
                      _(u"Number of modules SLOC \u2264 200 (um)"),
                      _(u"Number of modules 200 \u2264 SLOC \u2264 3000 SLOC (wm)"),
                      _("Number of modules > 3000 SLOC (xm)"),
                      _("Software Modularity Factor (SM = f(um,wm,xm))."),
                      _("Number of CSCI Units with sx > 20 (ax)"),
                      _(u"Number of CSCI units with 7 \u2264 sx \u2264 20 (bx)"),
                      _(u"Number of CSCI units with sx \u2264 7 (cx)"),
                      _("Software Complexity Factor (SX = f(ax,bx,cx))."),
                      _("Fraction of Standards Complied (DF)."),
                      _("Software Standards Review Factor (SR = f(DF))"),
                      _("Software Implementation Metric (S2 = SL*SM*SX*SR)"),
                      _("Reliability Prediction Figure of Merit (RPFOM = A*D*S1*S2)"),
                      _("Test Effort Factor (TE)"),
                      _("Test Methodology Factor (TM)"),
                      _("Test Coverage Factor (TC)"),
                      _("Test Efficiency Factor (T = TE*TM*TC)"),
                      _("Average Failure Rate During Testing (FT1)"),
                      _("Average Failure Rate at End of Testing (FT2)"),
                      _("Estimated Failure Rate of CSCI During Testing (F1 = FT1*T)"),
                      _("Estimated Failure Rate of CSCI at End of Testing (F2 = FT2*T)"),
                      _("Operating Environment Variability (EV)"),
                      _("Operating Environment Workload (EW)"),
                      _("Operating Environment Factor (E = EV*EW)"),
                      _("Estimated Operational Failure Rate (F = 0.14*FT2*T*E)")]

    _ts_tab_labels = [_("Test Confidence Level:"), _("Test Path:"),
                      _("Test Effort:"), _("Test Approach:"),
                      _("Labor Hours for Testing:"),
                      _("Labor Hours for Development:"),
                      _("Budget for Testing:"),
                      _("Budget for Development:"),
                      _("Working Days for Testing:"),
                      _("Working Days for Development:"),
                      _("Number of Branches:"),
                      _("Number of Branches Tested:"),
                      _("Number of Inputs:"),
                      _("Number of Inputs Tested:"),
                      _("Number of Units:"),
                      _("Number of Units Tested:"),
                      _("Number of Interfaces:"),
                      _("Number of Interfaces Tested:"),
                      _("Number of Requirements:"),
                      _("Number of Requirements Tested:")]

    _tt_tab_labels = [[_("Incident ID:"), _("Incident Date:"),
                       _("Reported By:"), _("Category:"),
                       _("Problem Type:"), _("Description:"),
                       _("Details:"), _("Criticality:"),
                       _("Method of Detection:"), _("Remarks:"),
                       _("Product Life Cycle:"), _("Incident Status:")],
                      [_("Test Procedure:"), _("Test Case:"),
                       _("Execution Time:"), _("Effect of Problem:"),
                       _("Recommended Solution:")],
                      [_("This failure occurred on equipment or a component part that is production intent."),
                       _("This failure is independent of any other failure."),
                       _("This failure is due to design deficiencies or poor workmanship of the equipment or component part."),
                       _("This failure is due to a defective component part."),
                       _("This failure is due to a component part that wore out prior to it's stipulated life."),
                       _("This failure is the first occurrence of an intermittent failure on this equipment."),
                       _("This failure is a malfunction (including false alarm) of the built-in test features."),
                       _("This failure is due to misadjustment of operator controls AND the information necessary to properly adjust these controls is not available from indicators which are integral to the equipment under test."),
                       _("This failure is dependent on another, relevent, failure."),
                       _("This failure is directly attributable to improper test setup."),
                       _("This failure is the failure of test insrumentation or monitoring equipment (other than built-in test equipment)."),
                       _("This failure is the result of test operator error."),
                       _("This failure is attributable to an error in the test procedure."),
                       _("This failure is the second or subsequent intermittent failure on this equipment."),
                       _("This failure occurred during burn-in, troubleshooting, repair verification, or setup."),
                       _("This failure is clearly attributable to an overstress condition in excess of the design requirements."),
                       _("This failure is within the responsibility of this organization.")],
                      [_("Prescribed Action:"), _("Action Taken:"),
                       _("Owner:"), _("Due Date:"), _("Status:"),
                       _("Approved"), _("Approved By:"), _("Approval Date:"),
                       _("Closed"), _("Closed By:"), _("Closure Date:")],
                      [_("Reviewed"), _("Reviewed By:"), _("Reviewed Date:"),
                       _("Approved"), _("Approved By:"), _("Approved Date:"),
                       _("Closed"), _("Closed By:"), _("Closure Date:")]]

    _re_tab_labels = [_("Average FR During Test:"),
                      _("Failure Rate at EOT:"), _("Average REN:"),
                      _("EOT REN:"), _("Number of Exception Conditions:"),
                      _("Input Variability:"), _("Total Execution Time:"),
                      _("OS Overhead Time:"), _("Workload:"),
                      _("Operating Environment Factor:"),
                      _("Estimated Failure Rate:")]

    def __init__(self, application):

        """ Initializes the Software Object.

            Keyword Arguments:
            application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self._selected_row = None
        self.rpfom = 0.0
        self.software_id = 0

        self._col_order = []

# Create the Notebook for the SOFTWARE object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        # Create generic toolbar action buttons.  These will call different
        # methods or functions depending on the ASSEMBLY Object notebook tab
        # that is selected.
        self.btnAddItem = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        self.btnRemoveItem = gtk.ToolButton(stock_id = gtk.STOCK_REMOVE)
        self.btnAnalyze = gtk.ToolButton(stock_id = gtk.STOCK_NO)
        self.btnSaveResults = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)

# Create the General Data tab widgets for the SOFTWARE object.
        self.txtDescription = _widg.make_text_view(width=400)
        self.cmbLevel = _widg.make_combo(simple=True)
        self.cmbApplication = _widg.make_combo(simple=True)
        self.cmbDevelopment = _widg.make_combo(simple=True)
        self.cmbPhase = _widg.make_combo(simple=True)
        self.chkDevAssessType = _widg.make_check_button(_("Perform detailed development environment assessment"))
        if self._general_data_widgets_create():
            self._app.debug_log.error("software.py: Failed to create General Data tab widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("software.py: Failed to create General Data tab.")

# Create the Worksheet 1 tab widgets for the SOFTWARE object.
        self.tvwWorksheet1 = gtk.TreeView()
        if self._worksheet_1_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 1 tab widgets.")
        if self._worksheet_1_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 1 tab.")

# Create the Worksheet 2 tab for the SOFTWARE object.
        self.tvwWorksheet2 = gtk.TreeView()
        if self._worksheet_2_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 2 tab widgets.")
        if self._worksheet_2_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 2 tab.")

# Create the Worksheet 3 tab for the SOFTWARE object.
        self.lblWS3_1 = _widg.make_label(self._ws3_tab_labels[0][0], width=800)
        self.lblWS3_2 = _widg.make_label(self._ws3_tab_labels[1][0], width=800)
        self.lblWS3_3 = _widg.make_label(self._ws3_tab_labels[2][0], width=800)
        self.lblWS3_4 = _widg.make_label(self._ws3_tab_labels[2][1], width=800)
        self.chkTC11 = _widg.make_check_button()
        self.chkTC12 = _widg.make_check_button()
        self.tvwWorksheet3 = gtk.TreeView()
        if self._worksheet_3_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 3 tab widgets.")
        if self._worksheet_3_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 3 tab.")

# Create the Worksheet 4 tab for the SOFTWARE object.
        self.tvwWorksheet4 = gtk.TreeView()
        if self._worksheet_4_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 4 tab widgets.")
        if self._worksheet_4_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 4 tab.")

# Create the Worksheet 8 tab for the SOFTWARE object.
        self.txt81 = _widg.make_entry(_width_=75)
        self.txt82 = _widg.make_entry(_width_=75)
        self.txt83 = _widg.make_entry(_width_=75, editable=False)
        self.txt84 = _widg.make_entry(_width_=75)
        self.txt85 = _widg.make_entry(_width_=75)
        if self._worksheet_8_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 8 tab widgets.")
        if self._worksheet_8_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 8 tab.")

# Create the Worksheet 9 tab for the SOFTWARE object.
        self.txt91a = _widg.make_entry(_width_=75, editable=False)
        self.txt91b = _widg.make_entry(_width_=75, editable=False)
        self.txt91c = _widg.make_entry(_width_=75, editable=False)
        self.txt92a = _widg.make_entry(_width_=75, editable=False)
        self.txt92b = _widg.make_entry(_width_=75, editable=False)
        self.txt92c = _widg.make_entry(_width_=75, editable=False)
        self.txt92d = _widg.make_entry(_width_=75, editable=False)
        self.txt93a = _widg.make_entry(_width_=75, editable=False)
        self.txt93b = _widg.make_entry(_width_=75, editable=False)
        self.txt93c = _widg.make_entry(_width_=75, editable=False)
        if self._worksheet_9_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 9 tab widgets.")
        if self._worksheet_9_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 9 tab.")

# Create the Worksheet 11 tab for the SOFTWARE object.
        self.tvwWorksheet11 = gtk.TreeView()
        if self._worksheet_11_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 11 tab widgets.")
        if self._worksheet_11_tab_create():
            self._app.debug_log.error("software.py: Failed to create Worksheet 11 tab.")

# Create the Test Technique Selection tab widgets for the SOFTWARE object.
        self.cmbTCL = _widg.make_combo(simple=True)
        self.cmbTestPath = _widg.make_combo(simple=True)
        self.cmbTestEffort = _widg.make_combo(simple=True)
        self.cmbTestApproach = _widg.make_combo(simple=True)
        self.txtLaborTest = _widg.make_entry(_width_=100)
        self.txtLaborDev = _widg.make_entry(_width_=100)
        self.txtBudgetTest = _widg.make_entry(_width_=100)
        self.txtBudgetDev = _widg.make_entry(_width_=100)
        self.txtScheduleTest = _widg.make_entry(_width_=100)
        self.txtScheduleDev = _widg.make_entry(_width_=100)
        self.txtBranches = _widg.make_entry(_width_=100)
        self.txtBranchesTest = _widg.make_entry(_width_=100)
        self.txtInputs = _widg.make_entry(_width_=100)
        self.txtInputsTest = _widg.make_entry(_width_=100)
        self.txtUnits = _widg.make_entry(_width_=100)
        self.txtUnitsTest = _widg.make_entry(_width_=100)
        self.txtInterfaces = _widg.make_entry(_width_=100)
        self.txtInterfacesTest = _widg.make_entry(_width_=100)
        self.tvwTestSelectionMatrix = gtk.TreeView()
        self.btnSoftwareMatrix = _widg.make_button(_width_=40, _image_="help")
        self.btnCSCISingleMatrix = _widg.make_button(_width_=40, _image_="help")
        self.btnCSCIPairedMatrix = _widg.make_button(_width_=40, _image_="help")
        self.btnUnitSingleMatrix = _widg.make_button(_width_=40, _image_="help")
        self.btnUnitPairedMatrix = _widg.make_button(_width_=40, _image_="help")
        self.btnErrorCatMatrix = _widg.make_button(_width_=40, _image_="help")
        self.btnStoppingRules = _widg.make_button(_width_=40, _image_="help")
        if self._test_selection_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Test Technique Selection tab widgets.")
        if self._test_selection_tab_create():
            self._app.debug_log.error("software.py: Failed to create Test Technique Selection tab.")

# Create the RG Plot tab widgets for the SOFTWARE object.
        self.tvwGrowthIncidents = gtk.TreeView()
        self.fig = Figure(figsize=(6, 4))
        self.pltFailureRate = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        if self._reliability_growth_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Reliability Growth tab widgets.")
        if self._reliability_growth_tab_create():
            self._app.debug_log.error("software.py: Failed to create Reliability Growth tab.")

# Create the Reliability Estimation tab widgets for the SOFTWARE object.
        self.txtFT1 = _widg.make_entry()
        self.txtFT2 = _widg.make_entry()
        self.txtRENAVG = _widg.make_entry()
        self.txtRENEOT = _widg.make_entry()
        self.txtEC = _widg.make_entry()
        self.txtEV = _widg.make_entry()
        self.txtET = _widg.make_entry()
        self.txtOS = _widg.make_entry()
        self.txtEW = _widg.make_entry()
        self.txtE = _widg.make_entry()
        self.txtF = _widg.make_entry()
        if self._reliability_estimation_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Reliability Estimation tab widgets.")
        if self._reliability_estimation_tab_create():
            self._app.debug_log.error("software.py: Failed to create Reliability Estimation tab.")

# Create the Assessment Results tab widgets for the SOFTWARE object.
        self.tvwResults = gtk.TreeView()
        if self._assessment_results_widgets_create():
            self._app.debug_log.error("software.py: Failed to create Assessment Results tab widgets.")
        if self._assessment_results_tab_create():
            self._app.debug_log.error("software.py: Failed to create Assessment Results tab.")

        self.vbxSoftware = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxSoftware.pack_start(toolbar, expand=False)
        self.vbxSoftware.pack_start(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def _toolbar_create(self):
        """ Method to create the toolbar for the Assembly Object work book. """

        toolbar = gtk.Toolbar()

        # Add sibling assembly button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Adds a new software module at the same indenture level as the selected software module."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.module_add, 0)
        toolbar.insert(button, 0)

        # Add child assembly button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Adds a new software module one indenture level subordinate to the selected software module."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.module_add, 1)
        toolbar.insert(button, 1)

        # Delete assembly button
        button = gtk.ToolButton(stock_id = gtk.STOCK_DELETE)
        button.set_tooltip_text(_("Removes the currently selected software module from the RelKit Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.module_delete)
        toolbar.insert(button, 2)

        toolbar.insert(gtk.SeparatorToolItem(), 3)

        # Perform analysis button.  Depending on the notebook page selected
        # will determine which analysis is executed.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(image)
        self.btnAnalyze.set_tooltip_text(_("Calculates software reliability metrics."))
        self.btnAnalyze.connect('clicked', _calc.calculate_project,
                                self._app, 4)
        toolbar.insert(self.btnAnalyze, 4)

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveResults.set_icon_widget(image)
        self.btnSaveResults.set_name('Save')
        self.btnSaveResults.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSaveResults, 5)

        toolbar.show()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create General Data widgets. """

        # Quadrant 1 (left) widgets.  These widgets are used to display general
        # information about the selected software module.
        self.txtDescription.set_tooltip_text(_("Enter a description of the selected software module."))
        self.txtDescription.get_child().get_child().connect('focus-out-event',
                                                            self._callback_entry,
                                                            'text', 3)

        self.cmbLevel.set_tooltip_text(_("Select the application level of the selected software module."))
        self.cmbLevel.connect('changed',
                              self._callback_combo, 2)

        query = "SELECT fld_level_desc \
                 FROM tbl_software_level"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbLevel, results, True)

        self.cmbApplication.set_tooltip_text(_("Select the application type of the selected software module."))
        self.cmbApplication.connect('changed',
                                    self._callback_combo, 4)

        query = "SELECT fld_application_desc \
                 FROM tbl_software_application"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbApplication, results, True)

        self.cmbDevelopment.set_tooltip_text(_("Select the type of development environment for the selected software module."))
        self.cmbDevelopment.connect('changed',
                                    self._callback_combo, 5)

        query = "SELECT fld_development_desc \
                 FROM tbl_development_environment"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbDevelopment, results, True)

        self.cmbPhase.set_tooltip_text(_("Select the development phase for the selected software module."))
        self.cmbPhase.connect('changed',
                              self._callback_combo, 36)

        query = "SELECT fld_phase_desc \
                 FROM tbl_development_phase"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbPhase, results, True)

        self.chkDevAssessType.connect('toggled',
                                      self._callback_check, 35)

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and add it to the
        gtk.Notebook at the proper location.
        """

        # Populate quadrant 1 (upper left).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        # Place the widgets.
        y_pos = 5
        label = _widg.make_label(self._gd_tab_labels[0][0], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtDescription, 205, y_pos)
        y_pos += 110

        label = _widg.make_label(self._gd_tab_labels[0][1], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbLevel, 205, y_pos)
        #fixed.put(self.btnHelpLevel, 410, y_pos)
        y_pos += 35

        label = _widg.make_label(self._gd_tab_labels[0][2], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbApplication, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._gd_tab_labels[0][3], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbDevelopment, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._gd_tab_labels[0][4], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbPhase, 205, y_pos)
        y_pos += 35

        fixed.put(self.chkDevAssessType, 5, y_pos)

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("General\nData") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays general information about the selected software module."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the SOFTWARE Object.
        """

        if(self._selected_row is not None):
            self.cmbLevel.set_active(int(self.model.get_value(self._selected_row, 2)))
            textbuffer = self.txtDescription.get_child().get_child().get_buffer()
            textbuffer.set_text(self.model.get_value(self._selected_row, 3))
            self.cmbApplication.set_active(int(self.model.get_value(self._selected_row, 4)))
            self.cmbDevelopment.set_active(int(self.model.get_value(self._selected_row, 5)))
            self.cmbPhase.set_active(int(self.model.get_value(self._selected_row, 36)))

            self.cmbTCL.set_active(int(self.model.get_value(self._selected_row, 37)))
            self.cmbTestPath.set_active(int(self.model.get_value(self._selected_row, 38)))

        return False

    def _worksheet_1_widgets_create(self):
        """
        Method for creating Worksheet 1 (Development Environment Assessment)
        widgets for the Software Object.
        """

        # Create a TreeView to display the list of questions regarding the
        # development environment.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT)
        self.tvwWorksheet1.set_model(model)
        self.tvwWorksheet1.set_tooltip_text(_("Displays the development environment assessment worksheet."))

        _labels = [_("Software Development Consideration"), _("Plan to Use")]

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('wrap-width', 850)
        cell.set_property('wrap-mode', pango.WRAP_WORD)
        cell.set_property('background', 'grey')
        cell.set_property('foreground', 'black')
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" + _labels[0] + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwWorksheet1.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _worksheet_1_tree_edit, None, 1, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=1)
        column.set_max_width(25)
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" + _labels[1] + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwWorksheet1.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)

        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        column.set_visible(False)

        self.tvwWorksheet1.append_column(column)

        self.tvwWorksheet1.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _worksheet_1_tab_create(self):
        """
        Method to create the Worksheet 1 gtk.Notebook tab and add it to
        gtk.Notebook in the proper location.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwWorksheet1)

        frame = _widg.make_frame(_label_=_("Development Environment Assessment"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Development\nEnvironment") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows assessment of the development environment."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_1_tab_load(self):
        """
        Loads the gtk.TreeView with development environment assessment
        information for the Software Object.
        """

        self.chkDevAssessType.set_active(self.model.get_value(self._selected_row, 35))

        # Clear the anomaly management worksheet.
        model = self.tvwWorksheet1.get_model()
        model.clear()

        if(self.model.get_value(self._selected_row, 35)):

            values = (self.model.get_value(self._selected_row, 1),)
            if(_conf.BACKEND == 'mysql'):
                query = "SELECT * FROM tbl_software_development \
                         WHERE fld_software_id=%d"
            if(_conf.BACKEND == 'sqlite3'):
                query = "SELECT * FROM tbl_software_development \
                         WHERE fld_software_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

            if(results == '' or not results):
                return True

            for i in range(len(results)):
                _data = ((self._ws1_tab_labels[results[i][1]],
                          results[i][2], results[i][1]))

                model.append(_data)

        return False

    def _worksheet_1_save(self):
        """
        Method to save the software development environemnt assessment results
        (Worksheet 1).
        """

        model = self.tvwWorksheet1.get_model()
        row = model.get_iter_root()

        while row is not None:
            values = (model.get_value(row, 1), self.software_id,
                      model.get_value(row, 2))

            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_software_development \
                         SET fld_y=%d \
                         WHERE fld_software_id=%d \
                         AND fld_question_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_software_development \
                         SET fld_y=? \
                         WHERE fld_software_id=? \
                         AND fld_question_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("software.py: Failed to save Worksheet 1 results to software development table.")

            row = model.iter_next(row)

        return False

    def _worksheet_2_widgets_create(self):
        """
        Method for creating Worksheet 2 (Anomaly Management Assessment)
        widgets for the Software Object.
        """

        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT)
        self.tvwWorksheet2.set_model(model)
        self.tvwWorksheet2.set_tooltip_text(_("Displays the anomaly management assessment worksheet."))

        _labels = ["", _("Count"), _("Ratio"), _("Yes"), _("No"), _("NA"),
                   _("Unk"), ""]

        for i in range(7):
            if(i > 2):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 1)
                cell.connect('toggled', self._worksheet_2_tree_edit, None, i,
                             model)
            else:
                cell = gtk.CellRendererText()
                if(i == 0):
                    cell.set_property('editable', 0)
                    cell.set_property('wrap-width', 850)
                    cell.set_property('wrap-mode', pango.WRAP_WORD)
                    cell.set_property('background', 'grey')
                    cell.set_property('foreground', 'black')
                else:
                    cell.set_property('editable', 1)
                    cell.set_property('background', 'white')
                    cell.set_property('foreground', 'black')
                cell.connect('edited', self._worksheet_2_tree_edit, i, model)

            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            if(i > 2):
                column.set_attributes(cell, active=i)
            else:
                column.set_attributes(cell, text=i)

            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _labels[i] +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            column.set_widget(label)

            self.tvwWorksheet2.append_column(column)

            # Hide the ratio and question number columns.
            if(i == 2 or i == 8):
                column.set_visible(0)

        self.tvwWorksheet2.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _worksheet_2_tab_create(self):
        """
        Method to create the Worksheet 2 gtk.Notebook tab and add it in the
        correct location.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwWorksheet2)

        frame = _widg.make_frame(_label_=_("Anomaly Management Assessment"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Anomaly\nManagement") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows assessment of anomaly management."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_2_tab_load(self):
        """
        Loads the gtk.TreeView with anomaly management assessment information
        for the Software Object.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        if(_phase_id == 2 and _level_id == 2):      # Load Worksheet 2A
            _sheet = 0
        elif(_phase_id == 3 and _level_id == 2):    # Load Worksheet 2B
            _sheet = 1
        elif(_phase_id == 4 and _level_id == 3):    # Load Worksheet 2C
            _sheet = 2
        elif(_phase_id == 4 and _level_id == 2):    # Load Worksheet 2D
            _sheet = 3

        # Clear the anomaly management worksheet.
        model = self.tvwWorksheet2.get_model()
        model.clear()

        values = (self.model.get_value(self._selected_row, 1), _phase_id)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_anomaly_management \
                     WHERE fld_software_id=%d \
                     AND fld_phase_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_anomaly_management \
                     WHERE fld_software_id=? \
                     AND fld_phase_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        for i in range(len(results)):
            _data = ((self._ws2_tab_labels[_sheet][results[i][2]],
                      results[i][3], results[i][4], results[i][5],
                      results[i][6], results[i][7], results[i][8],
                      results[i][2]))

            model.append(_data)

        return False

    def _worksheet_2_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView CellRenderer is edited for the anomaly
        management worksheet (Worksheet 2).

        Keyword Arguments:
        cell     -- the gtk.CellRenderer that was edited.
        path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                    edited.
        new_text -- the new text in the edited gtk.CellRenderer.
        position -- the column position of the edited gtk.CellRenderer.
        model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        _type_ = gobject.type_name(model.get_column_type(position))

        if(position > 2):
            model[path][position] = not cell.get_active()
            _positions = [[4, 5, 6], [3, 5, 6], [3, 4, 6], [3, 4, 5]]
            for i in range(3):
                model[path][_positions[position - 3][i]] = 0
        elif(_type_ == 'gchararray'):
            model[path][position] = str(new_text)
        elif(_type_ == 'gint'):
            model[path][position] = int(new_text)
        elif(_type_ == 'gfloat'):
            model[path][position] = float(new_text)

        # Calculate ratios and set Y/N values for those questions related to
        # ratios for CSCI level software.
        if(_level_id != 2):
            return False

        row = model.get_iter(path)
        if(path != '0'):
            row_prev = model.get_iter(str(int(path[0]) - 1))
        row_next = model.iter_next(row)
        q_num = model.get_value(row, 7)

        if(_phase_id == 2):                 # SSR
            if(q_num == 0 or q_num == 2 or q_num == 5):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                row = row_next
                _set_answer(model, row, numerator, denominator, 1.0, '==')
            elif(q_num == 1 or q_num == 3 or q_num == 6):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 1.0, '==')
        elif(_phase_id == 4):               # CDR
            if(q_num == 0 or q_num == 7):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                row = row_next
                _set_answer(model, row, numerator, denominator, 1.0, '==')
            elif(q_num == 1 or q_num == 8):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 1.0, '==')

        return False

    def _worksheet_2_save(self):
        """
        Method to save the anomaly management assessment results (Worksheet 2A,
        2B, 2C, or 2D).
        """

        _phase_id = self.model.get_value(self._selected_row, 36)
        model = self.tvwWorksheet2.get_model()
        row = model.get_iter_root()

        while row is not None:
            values = (model.get_value(row, 1), model.get_value(row, 2),
                      model.get_value(row, 3), model.get_value(row, 4),
                      model.get_value(row, 5), model.get_value(row, 6),
                      self.software_id, _phase_id,
                      model.get_value(row, 7))

            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_anomaly_management \
                         SET fld_value=%d, fld_ratio=%f, \
                             fld_y=%d, fld_n=%d, fld_na=%d, \
                             fld_unk=%d \
                         WHERE fld_software_id=%d \
                         AND fld_phase_id=%d \
                         AND fld_question_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_anomaly_management \
                         SET fld_value=?, fld_ratio=?, \
                             fld_y=?, fld_n=?, fld_na=?, \
                             fld_unk=? \
                         WHERE fld_software_id=? \
                         AND fld_phase_id=? \
                         AND fld_question_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("software.py: Failed to save Worksheet 2 results to anomaly management table.")

            row = model.iter_next(row)

        return False

    def _worksheet_3_widgets_create(self):
        """
        Method for creating Worksheet 3 (Traceability Assessment) widgets for
        the Software Object.
        """

        # Create the traceability matrix.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)

        self.tvwWorksheet3.set_model(model)
        self.tvwWorksheet3.set_tooltip_text(_("Displays the requirements traceability matrix."))

        _labels = [_("System Requirement"), _("Software Component")]

        for i in range(2):
            cell = gtk.CellRendererText()
            cell.set_property('editable', 1)
            cell.set_property('background', 'white')
            cell.set_property('foreground', 'black')
            cell.connect('edited', _worksheet_3_tree_edit, i, model)

            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            column.set_attributes(cell, text=i)

            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _labels[i] +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            column.set_widget(label)

            self.tvwWorksheet3.append_column(column)

        self.tvwWorksheet3.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _worksheet_3_tab_create(self):
        """
        Method to create the Worksheet 3 gtk.Notebook tab and add it to the
        gtk.Notebook at the correct position.
        """

        hpaned = gtk.HPaned()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwWorksheet3)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hpaned.pack1(frame)

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Requirements Traceability Assessment"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hpaned.pack2(frame)

        y_pos = 5
        fixed.put(self.chkTC11, 5, y_pos)
        fixed.put(self.lblWS3_1, 25, y_pos)
        fixed.put(self.lblWS3_2, 25, y_pos)
        fixed.put(self.lblWS3_3, 25, y_pos)
        y_pos += 30

        fixed.put(self.chkTC12, 5, y_pos)
        fixed.put(self.lblWS3_4, 25, y_pos)

        fixed.show_all()

        self.chkTC11.hide()
        self.chkTC12.hide()
        self.lblWS3_1.hide()
        self.lblWS3_2.hide()
        self.lblWS3_3.hide()
        self.lblWS3_4.hide()

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Requirements\nTraceability") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows assessment of requirements traceability."))
        self.notebook.insert_page(hpaned,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_3_tab_load(self):
        """
        Loads the gtk.TreeView with requirements traceability assessment
        information for the Software Object.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        # Clear the traceability matrix.
        model = self.tvwWorksheet3.get_model()
        model.clear()

        values = (self.model.get_value(self._selected_row, 1), _phase_id)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_software_traceability \
                     WHERE fld_software_id=%d \
                     AND fld_phase_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_software_traceability \
                     WHERE fld_software_id=? \
                     AND fld_phase_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        self.chkTC11.set_active(results[0][2])
        self.chkTC12.set_active(results[0][3])

        # Load the tracability matrix
        #for i in range(len(results)):
        #    _data = ((self._ws3_tab_labels[0][results[i][2]], results[i][3],
        #              results[i][4], results[i][5], results[i][6],
        #              results[i][7], results[i][8], results[i][2]))

        #    model.append(_data)

        if(_phase_id == 2):
            self.chkTC11.show()
            self.chkTC12.hide()
            self.lblWS3_1.show()
            self.lblWS3_2.hide()
            self.lblWS3_3.hide()
            self.lblWS3_4.hide()
        elif(_phase_id == 3):
            self.chkTC11.show()
            self.chkTC12.hide()
            self.lblWS3_1.hide()
            self.lblWS3_2.show()
            self.lblWS3_3.hide()
            self.lblWS3_4.hide()
        elif(_phase_id == 4):
            self.chkTC11.show()
            self.chkTC12.show()
            self.lblWS3_1.hide()
            self.lblWS3_2.hide()
            self.lblWS3_3.show()
            self.lblWS3_4.show()
        else:
            self.chkTC11.hide()
            self.chkTC12.hide()
            self.lblWS3_1.hide()
            self.lblWS3_2.hide()
            self.lblWS3_3.hide()
            self.lblWS3_4.hide()

        return False

    def _worksheet_3_save(self):
        """
        Method to save the anomaly management assessment results (Worksheet 3A,
        3B, or 3C).
        """

        _phase_id = self.model.get_value(self._selected_row, 36)

        values = (self.chkTC11.get_active(), self.chkTC12.get_active(),
                  self.software_id, _phase_id)

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_software_traceability \
                     SET fld_tc11=%d, fld_tc12=%d \
                     WHERE fld_software_id=%d \
                     AND fld_phase_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_software_traceability \
                     SET fld_tc11=?, fld_tc12=? \
                     WHERE fld_software_id=? \
                     AND fld_phase_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to save Worksheet 3 results to the software traceability table.")

        return False

    def _worksheet_4_widgets_create(self):
        """
        Method for creating Worksheet 4 (Quality Review) widgets for the
        Software Object.
        """

        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT)
        self.tvwWorksheet4.set_model(model)
        self.tvwWorksheet4.set_tooltip_text(_("Displays the quality review worksheet."))

        _labels = ["", _("Count"), _("Ratio"), _("Yes"), _("No"), _("NA"),
                   _("Unk"), ""]

        for i in range(7):
            if(i > 2):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 1)
                cell.connect('toggled', self._worksheet_4_tree_edit, None, i,
                             model)
            else:
                cell = gtk.CellRendererText()
                if(i == 0):
                    cell.set_property('editable', 0)
                    cell.set_property('wrap-width', 850)
                    cell.set_property('wrap-mode', pango.WRAP_WORD)
                    cell.set_property('background', 'grey')
                    cell.set_property('foreground', 'black')
                else:
                    cell.set_property('editable', 1)
                    cell.set_property('background', 'white')
                    cell.set_property('foreground', 'black')
                cell.connect('edited', self._worksheet_4_tree_edit, i, model)

            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            if(i > 2):
                column.set_attributes(cell, active=i)
            else:
                column.set_attributes(cell, text=i)

            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _labels[i] +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            column.set_widget(label)

            self.tvwWorksheet4.append_column(column)

            # Hide the ratio and question number columns.
            if(i == 2 or i == 8):
                column.set_visible(0)

        self.tvwWorksheet4.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _worksheet_4_tab_create(self):
        """
        Method to create the Worksheet 4 gtk.Notebook tab and add it to the
        gtk.Notebook at the correct position.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwWorksheet4)

        frame = _widg.make_frame(_label_=_("Software Quality Review"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Quality\nReview") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows quality review of software."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_4_tab_load(self):
        """
        Loads the gtk.TreeView with software quality review assessment
        information for the Software Object.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        if(_phase_id == 2 and _level_id == 2):      # Load Worksheet 4A
            _sheet = 0
        elif(_phase_id == 3 and _level_id == 2):    # Load Worksheet 4B
            _sheet = 1
        elif(_phase_id == 4 and _level_id == 3):    # Load Worksheet 4C
            _sheet = 2
        elif(_phase_id == 4 and _level_id == 2):    # Load Worksheet 4D
            _sheet = 3

        # Clear the anomaly management worksheet.
        model = self.tvwWorksheet4.get_model()
        model.clear()

        values = (self.model.get_value(self._selected_row, 1), _phase_id)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_software_quality \
                     WHERE fld_software_id=%d \
                     AND fld_phase_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_software_quality \
                     WHERE fld_software_id=? \
                     AND fld_phase_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        for i in range(len(results)):
            _data = ((self._ws4_tab_labels[_sheet][results[i][2]],
                      results[i][3], results[i][4], results[i][5],
                      results[i][6], results[i][7], results[i][8],
                      results[i][2]))

            model.append(_data)

        return False

    def _worksheet_4_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView CellRenderer is edited for the quality
        review worksheet (Worksheet 4).

        Keyword Arguments:
        cell     -- the gtk.CellRenderer that was edited.
        path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                    edited.
        new_text -- the new text in the edited gtk.CellRenderer.
        position -- the column position of the edited gtk.CellRenderer.
        model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        _type_ = gobject.type_name(model.get_column_type(position))

        if(position > 2):
            model[path][position] = not cell.get_active()
            _positions = [[4, 5, 6], [3, 5, 6], [3, 4, 6], [3, 4, 5]]
            for i in range(3):
                model[path][_positions[position - 3][i]] = 0
        elif(_type_ == 'gchararray'):
            model[path][position] = str(new_text)
        elif(_type_ == 'gint'):
            model[path][position] = int(new_text)
        elif(_type_ == 'gfloat'):
            model[path][position] = float(new_text)

        # Calculate ratios and set Y/N values for those questions related to
        # ratios for CSCI level software.
        if(_level_id != 2):
            return False

        row = model.get_iter(path)
        if(path != '0'):
            row_prev = model.get_iter(str(int(path[0]) - 1))
        row_next = model.iter_next(row)
        q_num = model.get_value(row, 7)

        if(_phase_id == 2):                 # SSR
            if(q_num == 8 or q_num == 10):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 1.0, '==')
            elif(q_num == 9 or q_num == 11):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 1.0, '==')
        elif(_phase_id == 3):               # PDR
            if(q_num == 2):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator,
                            (numerator + denominator), 0.3, '<')
            elif(q_num == 3):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator,
                            (numerator + denominator), 0.3, '<')
            elif(q_num == 6 or q_num == 8 or q_num == 10):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 0.5, '>')
            elif(q_num == 7 or q_num == 9 or q_num == 11):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 0.5, '>')
            elif(q_num == 14):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 0.75, '>')
            elif(q_num == 15):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 0.75, '>')
        elif(_phase_id == 4):               # CDR
            if(q_num == 0 or q_num == 4):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 0.3, '<=')
            elif(q_num == 1 or q_num == 3 or q_num == 5):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 0.3, '<=')
            elif(q_num == 2):
                denominator = float(new_text)
                self.model.set_value(self._selected_row, 24, denominator) # Set NM value
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 0.5, '>')
            elif(q_num == 6 or q_num == 13 or q_num == 14 or q_num == 17 or
                 q_num == 18 or q_num == 19 or q_num == 20 or q_num == 22 or
                 q_num == 24):
                denominator = self.model.get_value(self._selected_row, 24)
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 0.5, '>')
            elif(q_num == 21 or q_num == 25):
                denominator = self.model.get_value(self._selected_row, 24)
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 1.0, '>=')
            elif(q_num == 7 or q_num == 9 or q_num == 11):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 0.5, '>')
            elif(q_num == 8 or q_num == 10 or q_num == 12):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 0.5, '>')
            elif(q_num == 15):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 0.75, '>')
            elif(q_num == 16):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 0.75, '>')

        return False

    def _worksheet_4_save(self):
        """
        Method to save the quality review assessment results (Worksheet 4A, 4B,
        4C, or 4D).
        """

        _phase_id = self.model.get_value(self._selected_row, 36)
        model = self.tvwWorksheet4.get_model()
        row = model.get_iter_root()

        while row is not None:
            values = (model.get_value(row, 1), model.get_value(row, 2),
                      model.get_value(row, 3), model.get_value(row, 4),
                      model.get_value(row, 5), model.get_value(row, 6),
                      self.software_id, _phase_id,
                      model.get_value(row, 7))

            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_software_quality \
                         SET fld_value=%d, fld_ratio=%f, \
                             fld_y=%d, fld_n=%d, fld_na=%d, \
                             fld_unk=%d \
                         WHERE fld_software_id=%d \
                         AND fld_phase_id=%d \
                         AND fld_question_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_software_quality \
                         SET fld_value=?, fld_ratio=?, \
                             fld_y=?, fld_n=?, fld_na=?, \
                             fld_unk=? \
                         WHERE fld_software_id=? \
                         AND fld_phase_id=? \
                         AND fld_question_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("software.py: Failed to save Worksheet 4 results to software quality table.")

            row = model.iter_next(row)

        return False

    def _worksheet_8_widgets_create(self):
        """
        Method for creating Worksheet 8 (Language Type Assessment) widgets for
        the Software Object.
        """

        # Create the traceability questions
        self.txt81.connect('focus-out-event',
                           self._callback_entry, 'int', 19)
        self.txt82.connect('focus-out-event',
                           self._callback_entry, 'int', 18)

        #self.txt84.connect('focus-out-event',
        #                   self._callback_entry, 'int', )

        return False

    def _worksheet_8_tab_create(self):
        """
        Method to create the Worksheet 8 gtk.Notebook tab and add it to the
        gtk.Notebook at the correct position.
        """

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Language Type Assessment"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5
        for i in range(len(self._ws8_tab_label)):
            label = _widg.make_label(self._ws8_tab_label[i], width=990)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txt81, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt82, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt83, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt84, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt85, 1000, y_pos)

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Language\nType") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows assessment of language types."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_8_tab_load(self):
        """
        Loads the language type assessment widgets with information for the
        Software Object.
        """

        self.txt83.set_text(str(self.model.get_value(self._selected_row, 17)))
        self.txt82.set_text(str(self.model.get_value(self._selected_row, 18)))
        self.txt81.set_text(str(self.model.get_value(self._selected_row, 19)))

        return False

    def _worksheet_8_save(self):
        """
        Method to save the language type assessment results (Worksheet 8D).
        """

        _level_id = self.model.get_value(self._selected_row, 2)

        try:
            sx = int(self.txt84.get_text()) + int(self.txt85.get_text())
        except ValueError:
            sx = 0.0

        values = (int(self.txt81.get_text()), int(self.txt82.get_text()),
                  int(self.txt83.get_text()), sx, self.software_id, _level_id)

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_software \
                     SET fld_loc=%d, fld_aloc=%d, fld_hloc=%d, \
                         fld_sx=%d \
                     WHERE fld_software_id=%d \
                     AND fld_level_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_software \
                     SET fld_loc=?, fld_aloc=?, fld_hloc=?, \
                         fld_sx=? \
                     WHERE fld_software_id=? \
                     AND fld_level_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to save Worksheet 8 results to software table.")

        return False

    def _worksheet_9_widgets_create(self):
        """
        Method for creating Worksheet 9 (Language Type, Complexity, and
        Modularity Assessment) widgets for the Software Object.
        """

        self.txt91a.set_tooltip_text(_(""))

        return False

    def _worksheet_9_tab_create(self):
        """
        Method to create the Worksheet 9 gtk.Notebook tab and populate it with
        the appropriate widgets.
        """

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Language Type/Complexity/Modularity Assessment"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5
        for i in range(len(self._ws9_tab_label)):
            label = _widg.make_label(self._ws9_tab_label[i], width=990)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txt91a, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt91b, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt91c, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt92a, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt92b, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt92c, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt92d, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt93a, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt93b, 1000, y_pos)
        y_pos += 30
        fixed.put(self.txt93c, 1000, y_pos)

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Modularity\nComplexity") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows assessment of complexity and modularity."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_9_tab_load(self):
        """
        Loads the software characteristics assessment widgets with information
        for the Software Object.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        self.txt91a.set_text(str(self.model.get_value(self._selected_row, 19)))
        self.txt91b.set_text(str(self.model.get_value(self._selected_row, 18)))
        self.txt91c.set_text(str(self.model.get_value(self._selected_row, 17)))
        self.txt92a.set_text(str(self.model.get_value(self._selected_row, 21)))
        self.txt92b.set_text(str(self.model.get_value(self._selected_row, 22)))
        self.txt92c.set_text(str(self.model.get_value(self._selected_row, 23)))
        self.txt92d.set_text(str(self.model.get_value(self._selected_row, 24)))
        self.txt93a.set_text(str(self.model.get_value(self._selected_row, 26)))
        self.txt93b.set_text(str(self.model.get_value(self._selected_row, 27)))
        self.txt93c.set_text(str(self.model.get_value(self._selected_row, 28)))

        return False

    def _worksheet_11_widgets_create(self):
        """
        Method for creating Worksheet 11 (Standards Review) widgets for the
        Software Object.
        """

        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT)
        self.tvwWorksheet11.set_model(model)
        self.tvwWorksheet11.set_tooltip_text(_("Displays the standards review worksheet."))

        _labels = ["", _("Count"), _("Ratio"), _("Yes"), _("No"), _("NA"),
                   _("Unk"), ""]

        for i in range(7):
            if(i > 2):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', 1)
                cell.connect('toggled', self._worksheet_11_tree_edit, None, i,
                             model)
            else:
                cell = gtk.CellRendererText()
                if(i == 0):
                    cell.set_property('editable', 0)
                    cell.set_property('wrap-width', 850)
                    cell.set_property('wrap-mode', pango.WRAP_WORD)
                    cell.set_property('background', 'grey')
                    cell.set_property('foreground', 'black')
                else:
                    cell.set_property('editable', 1)
                    cell.set_property('background', 'white')
                    cell.set_property('foreground', 'black')
                cell.connect('edited', self._worksheet_11_tree_edit, i, model)

            column = gtk.TreeViewColumn()
            column.pack_start(cell, True)
            if(i > 2):
                column.set_attributes(cell, active=i)
            else:
                column.set_attributes(cell, text=i)

            label = gtk.Label()
            label.set_markup("<span weight='bold'>" + _labels[i] + "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.show_all()
            column.set_widget(label)

            self.tvwWorksheet11.append_column(column)

            # Hide the ratio and question number columns.
            if(i == 2 or i == 8):
                column.set_visible(0)

        self.tvwWorksheet11.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _worksheet_11_tab_create(self):
        """
        Method to create the Worksheet 11 gtk.Notebook tab and add it to the
        gtk.Notebook at the correct location.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwWorksheet11)

        frame = _widg.make_frame(_label_=_("Software Standards Review"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Standards\nReview") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Allows standards review of software."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _worksheet_11_tab_load(self):
        """
        Loads the gtk.TreeView with software quality review assessment
        information for the Software Object.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        # Clear the anomaly management worksheet.
        model = self.tvwWorksheet11.get_model()
        model.clear()

        values = (self.model.get_value(self._selected_row, 1), _phase_id)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_software_standards \
                     WHERE fld_software_id=%d \
                     AND fld_phase_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_software_standards \
                     WHERE fld_software_id=? \
                     AND fld_phase_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        for i in range(len(results)):
            _data = ((self._ws11_tab_labels[1][results[i][2]],
                      results[i][3], results[i][4], results[i][5],
                      results[i][6], results[i][7], results[i][8],
                      results[i][2]))

            model.append(_data)

        return False

    def _worksheet_11_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView CellRenderer is edited for the standards
        review worksheet (Worksheet 11).

        Keyword Arguments:
        cell     -- the gtk.CellRenderer that was edited.
        path     -- the gtk.Treeview path of the gtk.CellRenderer that was
                    edited.
        new_text -- the new text in the edited gtk.CellRenderer.
        position -- the column position of the edited gtk.CellRenderer.
        model    -- the gtk.TreeModel the gtk.CellRenderer belongs to.
        """

        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        _type_ = gobject.type_name(model.get_column_type(position))

        if(position > 2):
            model[path][position] = not cell.get_active()
            _positions = [[4, 5, 6], [3, 5, 6], [3, 4, 6], [3, 4, 5]]
            for i in range(3):
                model[path][_positions[position - 3][i]] = 0
        elif(_type_ == 'gchararray'):
            model[path][position] = str(new_text)
        elif(_type_ == 'gint'):
            model[path][position] = int(new_text)
        elif(_type_ == 'gfloat'):
            model[path][position] = float(new_text)

        # Calculate ratios and set Y/N values for those questions related to
        # ratios for CSCI level software.
        if(_phase_id != 5):
            return False

        row = model.get_iter(path)
        if(path != '0'):
            row_prev = model.get_iter(str(int(path[0]) - 1))
        row_next = model.iter_next(row)
        q_num = model.get_value(row, 7)

        if(_level_id != 2):                 # CSCI
            if(q_num == 1 or q_num == 3 or q_num == 14 or q_num == 19 or q_num == 21 or q_num == 23):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 1.0, '==')
            elif(q_num == 2 or q_num == 4 or q_num == 15 or q_num == 20 or q_num == 22 or q_num == 24):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 1.0, '==')
        elif(_level_id != 3):               # CSCI
            if(q_num == 1 or q_num == 11 or q_num == 16 or q_num == 18 or q_num == 23 or q_num == 25):
                denominator = float(new_text)
                numerator = float(model.get_value(row_next, 1))
                _set_answer(model, row_next, numerator, denominator, 1.0, '==')
            elif(q_num == 2 or q_num == 12 or q_num == 17 or q_num == 19 or q_num == 24 or q_num == 26):
                denominator = float(model.get_value(row_prev, 1))
                numerator = float(new_text)
                _set_answer(model, row, numerator, denominator, 1.0, '==')

        return False

    def _worksheet_11_save(self):
        """
        Method to save the standards review assessment results (Worksheet 11D).
        """

        _phase_id = self.model.get_value(self._selected_row, 36)
        model = self.tvwWorksheet11.get_model()
        row = model.get_iter_root()

        while row is not None:
            values = (model.get_value(row, 1), model.get_value(row, 2),
                      model.get_value(row, 3), model.get_value(row, 4),
                      model.get_value(row, 5), model.get_value(row, 6),
                      self.software_id, _phase_id,
                      model.get_value(row, 7))

            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_software_standards \
                         SET fld_value=%d, fld_ratio=%f, \
                             fld_y=%d, fld_n=%d, fld_na=%d, \
                             fld_unk=%d \
                         WHERE fld_software_id=%d \
                         AND fld_phase_id=%d \
                         AND fld_question_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_software_standards \
                         SET fld_value=?, fld_ratio=?, \
                             fld_y=?, fld_n=?, fld_na=?, \
                             fld_unk=? \
                         WHERE fld_software_id=? \
                         AND fld_phase_id=? \
                         AND fld_question_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("software.py: Failed to save Worksheet 11 results to software standards table.")

            row = model.iter_next(row)

        return False

    def _test_selection_widgets_create(self):
        """ Method to create the test planning tab widgets for the SOFTWARE
            Object.
        """

        # Software test technique selection widgets.  These widgets are used
        # to display test technique information about the selected software
        # module.
        self.cmbTCL.connect('changed',
                            self._callback_combo, 37)
        self.cmbTCL.set_tooltip_text(_("Select the desired software test confidence level."))
        _list = [["Low"], ["Medium"], ["High"], ["Very High"]]
        _widg.load_combo(self.cmbTCL, _list, True)

        self.cmbTestPath.connect('changed',
                                 self._callback_combo, 38)
        self.cmbTestPath.set_tooltip_text(_("Select the path for determining software testing techniques."))
        _list = [[_("Choose techniques based on software category")],
                 [_("Choose techniques based on types of software errors")]]
        _widg.load_combo(self.cmbTestPath, _list, True)

        self.cmbTestEffort.connect('changed',
                                   self._callback_combo, 40)
        self.cmbTestEffort.set_tooltip_text(_("Select the software test effort alternative."))
        _list = [[_("Alternative 1, Labor Hours")],
                 [_("Alternative 2, Budget")],
                 [_("Alternative 3, Schedule")]]
        _widg.load_combo(self.cmbTestEffort, _list, True)

        self.cmbTestApproach.connect('changed',
                                     self._callback_combo, 41)
        self.cmbTestApproach.set_tooltip_text(_("Select the software test approach."))
        _list = [[_("Test Until Method is Exhausted")],
                 [_("Stopping Rules")]]
        _widg.load_combo(self.cmbTestApproach, _list, True)

        self.txtLaborTest.set_tooltip_text(_("Total number of labor hours for software testing."))
        self.txtLaborTest.connect('focus-out-event',
                                  self._callback_entry, 'float', 42)

        self.txtLaborDev.set_tooltip_text(_("Total number of labor hours entire software development effort."))
        self.txtLaborDev.connect('focus-out-event',
                                 self._callback_entry, 'float', 43)

        self.txtBudgetTest.set_tooltip_text(_("Total budget for software testing."))
        self.txtBudgetTest.connect('focus-out-event',
                                   self._callback_entry, 'float', 44)

        self.txtBudgetDev.set_tooltip_text(_("Total budget for entire software development effort."))
        self.txtBudgetDev.connect('focus-out-event',
                                  self._callback_entry, 'float', 45)

        self.txtScheduleTest.set_tooltip_text(_("Working days scheduled for software testing."))
        self.txtScheduleTest.connect('focus-out-event',
                                     self._callback_entry, 'float', 46)

        self.txtScheduleDev.set_tooltip_text(_("Working days scheduled for entire development effort."))
        self.txtScheduleDev.connect('focus-out-event',
                                    self._callback_entry, 'float', 47)

        self.txtBranches.set_tooltip_text(_("The total number of execution branches in the selected unit."))
        self.txtBranches.connect('focus-out-event',
                                 self._callback_entry, 'int', 48)

        self.txtBranchesTest.set_tooltip_text(_("The total number of execution branches actually tested in the selected unit."))
        self.txtBranchesTest.connect('focus-out-event',
                                     self._callback_entry, 'int', 49)

        self.txtInputs.set_tooltip_text(_("The total number of inputs to the selected unit."))
        self.txtInputs.connect('focus-out-event',
                               self._callback_entry, 'int', 50)

        self.txtInputsTest.set_tooltip_text(_("The total number of inputs to the selected unit actually tested."))
        self.txtInputsTest.connect('focus-out-event',
                                   self._callback_entry, 'int', 51)

        self.txtUnits.set_tooltip_text(_("The total number of units in the selected CSCI."))

        self.txtUnitsTest.set_tooltip_text(_("The total number of units in the selected CSCI actually tested."))
        self.txtUnitsTest.connect('focus-out-event',
                                  self._callback_entry, 'int', 52)

        self.txtInterfaces.set_tooltip_text(_("The total number of interfaces to the selected CSCI."))
        self.txtInterfaces.connect('focus-out-event',
                                   self._callback_entry, 'int', 53)

        self.txtInterfacesTest.set_tooltip_text(_("The total number of interfaces in the selected CSCI actually tested."))
        self.txtInterfacesTest.connect('focus-out-event',
                                       self._callback_entry, 'int', 54)

        self.btnSoftwareMatrix.set_tooltip_text(_("Display the software category vs. testing technique matrix."))
        self.btnSoftwareMatrix.connect('clicked', _test_techniques,
                                       self._app.winWorkBook)

        self.btnCSCISingleMatrix.set_tooltip_text(_("Display the CSCI level single test technique matrix."))
        self.btnCSCISingleMatrix.connect('clicked', _csci_single_matrix,
                                         self._app.winWorkBook)

        self.btnCSCIPairedMatrix.set_tooltip_text(_("Display the CSCI level paired test technique matrix."))
        self.btnCSCIPairedMatrix.connect('clicked', _csci_paired_matrix,
                                         self._app.winWorkBook)

        self.btnUnitSingleMatrix.set_tooltip_text(_("Display the unit level single test technique matrix."))
        self.btnUnitSingleMatrix.connect('clicked', _unit_single_matrix,
                                         self._app.winWorkBook)

        self.btnUnitPairedMatrix.set_tooltip_text(_("Display the unit level paired test technique matrix."))
        self.btnUnitPairedMatrix.connect('clicked', _unit_paired_matrix,
                                         self._app.winWorkBook)

        self.btnErrorCatMatrix.set_tooltip_text(_("Display the error category vs. test technique matrix."))
        self.btnErrorCatMatrix.connect('clicked', _test_effectiveness,
                                       self._app.winWorkBook)

        self.btnStoppingRules.set_tooltip_text(_("Display the estopping rules for test techniques."))
        self.btnStoppingRules.connect('clicked', _test_stopping_rules,
                                      self._app.winWorkBook)

        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- #
        model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvwTestSelectionMatrix.set_model(model)
        self.tvwTestSelectionMatrix.set_tooltip_text(_("Software test technique selection matrix."))

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        label = gtk.Label(column.get_title())
        _heading = _("Software Test Technique")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _test_selection_tree_edit, None, 1, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=1)
        column.set_max_width(50)
        label = gtk.Label(column.get_title())
        label.set_property('angle', 90)
        _heading = _("Single Test\nEffectiveness")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _test_selection_tree_edit, None, 2, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=2)
        column.set_max_width(50)
        label = gtk.Label(column.get_title())
        label.set_property('angle', 90)
        _heading = _("Paired Test\nEffectiveness")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _test_selection_tree_edit, None, 3, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=3)
        column.set_max_width(50)
        label = gtk.Label(column.get_title())
        label.set_property('angle', 90)
        _heading = _("Single Test\nCoverage")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _test_selection_tree_edit, None, 4, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=4)
        column.set_max_width(50)
        label = gtk.Label(column.get_title())
        label.set_property('angle', 90)
        _heading = _("Paired Test\nCoverage")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _test_selection_tree_edit, None, 5, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=5)
        column.set_max_width(50)
        label = gtk.Label(column.get_title())
        label.set_property('angle', 90)
        _heading = _("Error\nCategory")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', _test_selection_tree_edit, None, 6, model)
        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, active=6)
        column.set_max_width(50)
        label = gtk.Label(column.get_title())
        label.set_property('angle', 90)
        _heading = _("Actually\nUsed")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 1)
        cell.set_property('wrap-width', 300)
        cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        cell.connect('edited', _test_selection_tree_edit, 7, model)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=7)
        label = gtk.Label(column.get_title())
        _heading = _("Notes/Comments")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.show_all()
        column.set_widget(label)
        self.tvwTestSelectionMatrix.append_column(column)

        return False

    def _test_selection_tab_create(self):
        """
        Method to create the Test Technique selection gtk.Notebook tab and add
        it to the gtk.Notebook at the proper location.
        """

        hbox = gtk.HBox()

        vbox = gtk.VBox()

        # Add the test planning widgets ot the upper left quadrant.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Test Planning"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        y_pos = 5
        label = _widg.make_label(self._ts_tab_labels[0], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbTCL, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[1], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbTestPath, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[2], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbTestEffort, 205, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[3], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbTestApproach, 205, y_pos)
        y_pos += 35

        fixed.put(self.btnSoftwareMatrix, 5, y_pos)
        fixed.put(self.btnCSCISingleMatrix, 5, y_pos)
        fixed.put(self.btnUnitSingleMatrix, 5, y_pos)
        fixed.put(self.btnCSCIPairedMatrix, 50, y_pos)
        fixed.put(self.btnUnitPairedMatrix, 50, y_pos)
        fixed.put(self.btnErrorCatMatrix, 95, y_pos)
        fixed.put(self.btnStoppingRules, 140, y_pos)

        vbox.pack_start(frame)

        # Add the test effort widgets to the lower left quadrant.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Test Effort"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        y_pos = 5
        label = _widg.make_label(self._ts_tab_labels[4], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtLaborTest, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[5], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtLaborDev, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[6], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtBudgetTest, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[7], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtBudgetDev, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[8], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScheduleTest, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[9], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtScheduleDev, 210, y_pos)

        vbox.pack_start(frame)

        hbox.pack_start(vbox)

        vbox = gtk.VBox()

        # Add the test coverage widgets to the upper right quadrant.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Test Coverage"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        y_pos = 5
        label = _widg.make_label(self._ts_tab_labels[10], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtBranches, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[11], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtBranchesTest, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[12], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtInputs, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[13], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtInputsTest, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[14], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtUnits, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[15], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtUnitsTest, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[16], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtInterfaces, 210, y_pos)
        y_pos += 35

        label = _widg.make_label(self._ts_tab_labels[17], 200, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtInterfacesTest, 210, y_pos)

        fixed.show_all()

        vbox.pack_start(frame)

        # Add the test selection matrix gtk.Treeview to the lower right
        # quadrant.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwTestSelectionMatrix)

        frame = _widg.make_frame(_label_=_("Test Technique Selection"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        vbox.pack_start(frame)

        hbox.pack_start(vbox)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Test\nPlanning") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Assists in planning of software test program."))
        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _test_selection_tab_load(self):
        """
        Loads the test technique selection information for the selected
        software module.
        """

        self.cmbTCL.set_active(self.model.get_value(self._selected_row, 37))
        self.cmbTestPath.set_active(self.model.get_value(self._selected_row, 38))
        self.cmbTestEffort.set_active(self.model.get_value(self._selected_row, 40))
        self.cmbTestApproach.set_active(self.model.get_value(self._selected_row, 41))
        self.txtLaborTest.set_text(str(self.model.get_value(self._selected_row, 42)))
        self.txtLaborDev.set_text(str(self.model.get_value(self._selected_row, 43)))
        self.txtBudgetTest.set_text(str(self.model.get_value(self._selected_row, 44)))
        self.txtBudgetDev.set_text(str(self.model.get_value(self._selected_row, 45)))
        self.txtScheduleTest.set_text(str(self.model.get_value(self._selected_row, 46)))
        self.txtScheduleDev.set_text(str(self.model.get_value(self._selected_row, 47)))
        self.txtBranches.set_text(str(self.model.get_value(self._selected_row, 48)))
        self.txtBranchesTest.set_text(str(self.model.get_value(self._selected_row, 49)))
        self.txtInputs.set_text(str(self.model.get_value(self._selected_row, 50)))
        self.txtInputsTest.set_text(str(self.model.get_value(self._selected_row, 51)))
        self.txtUnits.set_text(str(self.model.get_value(self._selected_row, 24)))
        self.txtUnitsTest.set_text(str(self.model.get_value(self._selected_row, 52)))
        self.txtInterfaces.set_text(str(self.model.get_value(self._selected_row, 53)))
        self.txtInterfacesTest.set_text(str(self.model.get_value(self._selected_row, 54)))

        # Set the correct test coverage gtk.Entry widgets editable depending
        # on the application level of the selected software.
        _level_id = self.model.get_value(self._selected_row, 2)
        if(_level_id == 2):                 # CSCI
            self.txtBranches.props.editable = False
            self.txtBranches.set_sensitive(False)
            self.txtBranchesTest.props.editable = False
            self.txtBranchesTest.set_sensitive(False)
            self.txtInputs.props.editable = False
            self.txtInputs.set_sensitive(False)
            self.txtInputsTest.props.editable = False
            self.txtInputsTest.set_sensitive(False)
            self.txtUnits.props.editable = True
            self.txtUnits.set_sensitive(True)
            self.txtUnitsTest.props.editable = True
            self.txtUnitsTest.set_sensitive(True)
            self.txtInterfaces.props.editable = True
            self.txtInterfaces.set_sensitive(True)
            self.txtInterfacesTest.props.editable = True
            self.txtInterfacesTest.set_sensitive(True)
        elif(_level_id == 3):               # Unit
            self.txtBranches.props.editable = True
            self.txtBranches.set_sensitive(True)
            self.txtBranchesTest.props.editable = True
            self.txtBranchesTest.set_sensitive(True)
            self.txtInputs.props.editable = True
            self.txtInputs.set_sensitive(True)
            self.txtInputsTest.props.editable = True
            self.txtInputsTest.set_sensitive(True)
            self.txtUnits.props.editable = False
            self.txtUnits.set_sensitive(False)
            self.txtUnitsTest.props.editable = False
            self.txtUnitsTest.set_sensitive(False)
            self.txtInterfaces.props.editable = False
            self.txtInterfaces.set_sensitive(False)
            self.txtInterfacesTest.props.editable = False
            self.txtInterfacesTest.set_sensitive(False)
        else:
            self.txtBranches.props.editable = False
            self.txtBranches.set_sensitive(False)
            self.txtBranchesTest.props.editable = False
            self.txtBranchesTest.set_sensitive(False)
            self.txtInputs.props.editable = False
            self.txtInputs.set_sensitive(False)
            self.txtInputsTest.props.editable = False
            self.txtInputsTest.set_sensitive(False)
            self.txtUnits.props.editable = False
            self.txtUnits.set_sensitive(False)
            self.txtUnitsTest.props.editable = False
            self.txtUnitsTest.set_sensitive(False)
            self.txtInterfaces.props.editable = False
            self.txtInterfaces.set_sensitive(False)
            self.txtInterfacesTest.props.editable = False
            self.txtInterfacesTest.set_sensitive(False)

        # Load the test selection matrix.
        model = self.tvwTestSelectionMatrix.get_model()
        model.clear()

        _tests = ["Code Reviews", "Error/Anomaly Analysis",
                  "Structure Analysis", "Random Testing",
                  "Functional Testing", "Branch Testing"]

        values = (self.software_id,)
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_software_tests \
                     WHERE fld_software_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_software_tests \
                     WHERE fld_software_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(not results or results == ''):
            return True

        num_tests = len(results)

        for i in range(num_tests):
            _data = (_tests[i], results[i][3], results[i][4],
                     results[i][5], results[i][6], results[i][7],
                     results[i][9], _util.none_to_string(results[i][8]))
            model.append(None, _data)

        return False

    def _reliability_growth_widgets_create(self):
        """
        Method to create widgets for displaying reliability growth information
        and results.
        """

        # Create the failure data table.
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwGrowthIncidents.set_model(model)
        self.tvwGrowthIncidents.set_tooltip_text(_("Displays the data used to generate the software reliability growth plot."))

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        label = gtk.Label(column.get_title())
        _heading = _("Date")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwGrowthIncidents.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        label = gtk.Label(column.get_title())
        _heading = _("Start\nTime")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwGrowthIncidents.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        label = gtk.Label(column.get_title())
        _heading = _("End\nTime")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwGrowthIncidents.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        label = gtk.Label(column.get_title())
        _heading = _("Number of\nChargeable\nFailures")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwGrowthIncidents.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
        label = gtk.Label(column.get_title())
        _heading = _("Failure Rate\nDuring Test")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwGrowthIncidents.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn()
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=5)
        label = gtk.Label(column.get_title())
        _heading = _("Failure Rate at\nEnd of Test")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        column.set_widget(label)
        self.tvwGrowthIncidents.append_column(column)

        self.tvwGrowthIncidents.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _reliability_growth_tab_create(self):
        """
        Method to create the reliability growth gtk.Notebook tab and add it to
        the gtk.Notebook at the correct location.
        """

        hpaned = gtk.HPaned()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwGrowthIncidents)

        frame = _widg.make_frame(_label_=_("Reliability Growth Incidents"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        hpaned.pack1(frame)

        frame = _widg.make_frame(_label_=_("Software Failure Rate Plot"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(self.pltFailureRate)
        frame.show_all()

        hpaned.pack2(frame)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Reliability\nGrowth") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays software reliability growth plot."))
        self.notebook.insert_page(hpaned,
                                  tab_label=label,
                                  position=-1)

        return False

    def _reliability_growth_tab_load(self):
        """
        Method for populating the reliability growth tab with growth data for
        the selected SOFTWARE object.
        """

        from datetime import datetime, date

        _dates = []
        _start = []
        _end = []
        _count = []

        _data = []
        _data2 = []

        values = (self.software_id, )
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT fld_request_date, fld_execution_time, COUNT() \
                     FROM tbl_incident \
                     WHERE fld_software_id=%d \
                     AND fld_life_cycle=2 \
                     GROUP BY fld_request_date"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT fld_request_date, fld_execution_time, COUNT() \
                     FROM tbl_incident \
                     WHERE fld_software_id=? \
                     AND fld_life_cycle=2 \
                     GROUP BY fld_request_date"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        n_results = len(results)
        _start.append(0.0)
        for i in range(n_results):
            request_date = str(date.fromordinal(int(results[i][0])))
            request_date = datetime.strptime(request_date, '%Y-%m-%d')
            _dates.append(request_date)
            _start.append(results[i][1])
            _end.append(results[i][1])
            _count.append(results[i][2])

        model = self.tvwGrowthIncidents.get_model()
        model.clear()
        for i in range(len(_count)):
            try:
                _data.append(_count[i] / (_end[i] - _start[i]))
            except ZeroDivisionError:
                _data.append(0.0)
            if(i > 1):
                _data2.append(sum(_data[i-2:i]) / 3.0)
            else:
                _data2.append(0.0)

            model.append([_dates[i], _start[i], _end[i], _count[i], _data[i],
                          _data2[i]])

        _name = self.model.get_value(self._selected_row, 3)
        self.ax.set_title(_("Failure Rate Growth of %s") % _name)
        self.ax.set_xlabel(_("Date"))
        self.ax.set_ylabel(_("Failure Rate (failures/hour)"))

        line, = self.ax.plot_date(matplotlib.dates.date2num(_dates),
                                  _data, 'go-')
        line2, = self.ax.plot_date(matplotlib.dates.date2num(_dates),
                                   _data2, 'bo-')

        for i in range(len(_data)):
            line.set_ydata(_data)
            line2.set_ydata(_data2)

        self.pltFailureRate.draw()
        self.fig.legend((line, line2),
                        ("FR During Test", "FR at End of Test"),
                        'upper right')

        return False

    def _reliability_estimation_widgets_create(self):
        """
        Method for creating reliability estimation widgets for the SOFTWARE
        Object.
        """

        self.txtFT1.set_tooltip_text(_("Displays the average failure rate during test for the selected software module."))
        self.txtFT2.set_tooltip_text(_("Displays the failure rate at the end of test for the selected software module."))
        self.txtRENAVG.set_tooltip_text(_("Displays the average Reliability Estimation Number (REN) for the selected software module."))
        self.txtRENEOT.set_tooltip_text(_("Displays the end of test Reliability Estimation Number (REN) for the selected software module."))
        self.txtEC.set_tooltip_text(_("Displays the number of exception conditions for the selected software module."))
        self.txtEC.connect('focus-out-event',
                           self._callback_entry, 'float', 63)
        self.txtEV.set_tooltip_text(_("Displays the variability of input for the selected software module."))
        self.txtET.set_tooltip_text(_("Displays the total execution time for the selected software module."))
        self.txtET.connect('focus-out-event',
                           self._callback_entry, 'float', 65)
        self.txtOS.set_tooltip_text(_("Displays the operating system overhead time for the selected software module."))
        self.txtOS.connect('focus-out-event',
                           self._callback_entry, 'float', 66)
        self.txtEW.set_tooltip_text(_("Displays the workload for the selected software module."))
        self.txtE.set_tooltip_text(_("Displays the operating environment factor for the selected software module."))
        self.txtF.set_tooltip_text(_("Displays the estimated failure rate for the selected software module."))

        return False

    def _reliability_estimation_tab_create(self):
        """
        Method to create the reliability estimation gtk.Notebook tab and add it
        to the gtk.Notebook at the correct location.
        """

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Reliability Estimation Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        y_pos = 5
        label = _widg.make_label(self._re_tab_labels[0])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFT1, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[1])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFT2, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[2])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRENAVG, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[3])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRENEOT, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[4])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEC, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[5])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEV, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[6])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtET, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[7])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtOS, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[8])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtEW, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[9])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtE, 200, y_pos)
        y_pos += 30

        label = _widg.make_label(self._re_tab_labels[10])
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtF, 200, y_pos)

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Reliability\nEstimation") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays software reliability estimation results."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _reliability_estimation_tab_load(self):
        """
        Loads the gtk.Entry widgets with software reliability aestimation
        results information for the SOFTWARE Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if(self._selected_row is not None):
            self.txtFT1.set_text(str(fmt.format(self.model.get_value(self._selected_row, 59))))
            self.txtFT2.set_text(str(fmt.format(self.model.get_value(self._selected_row, 60))))
            self.txtRENAVG.set_text(str(fmt.format(self.model.get_value(self._selected_row, 61))))
            self.txtRENEOT.set_text(str(fmt.format(self.model.get_value(self._selected_row, 62))))
            self.txtEC.set_text(str(fmt.format(self.model.get_value(self._selected_row, 63))))
            self.txtEV.set_text(str(fmt.format(self.model.get_value(self._selected_row, 64))))
            self.txtET.set_text(str(fmt.format(self.model.get_value(self._selected_row, 65))))
            self.txtOS.set_text(str(fmt.format(self.model.get_value(self._selected_row, 66))))
            self.txtEW.set_text(str(fmt.format(self.model.get_value(self._selected_row, 67))))
            self.txtE.set_text(str(fmt.format(self.model.get_value(self._selected_row, 68))))
            self.txtF.set_text(str(fmt.format(self.model.get_value(self._selected_row, 69))))

        return False

    def _assessment_results_widgets_create(self):
        """
        Method for creating assessment result widgets for the SOFTWARE Object.
        """

        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                              gobject.TYPE_STRING)
        self.tvwResults.set_model(model)
        self.tvwResults.set_tooltip_text(_("Displays the software reliability assessment results worksheet."))

        _labels = [_("Software Reliability Factor"), _("Result")]

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('wrap-width', 850)
        cell.set_property('wrap-mode', pango.WRAP_WORD)
        cell.set_property('background', 'grey')
        cell.set_property('foreground', 'black')

        column = gtk.TreeViewColumn()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        label = gtk.Label(column.get_title())
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _labels[0])
        label.show_all()
        column.set_widget(label)

        self.tvwResults.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'white')
        cell.set_property('foreground', 'black')

        column = gtk.TreeViewColumn()
        column.pack_start(cell, False)
        column.set_attributes(cell, text=1)
        column.set_max_width(25)
        label = gtk.Label(column.get_title())
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_markup("<span weight='bold'>%s</span>" % _labels[1])
        label.show_all()
        column.set_widget(label)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'white')
        cell.set_property('foreground', 'black')

        column.pack_start(cell, False)
        column.set_attributes(cell, text=2)

        self.tvwResults.append_column(column)

        self.tvwResults.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_NONE)

        return False

    def _assessment_results_tab_create(self):
        """
        Method to create the assessment results gtk.Notebook tab and add it to
        the gtk.Notebook at the correct location.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwResults)

        frame = _widg.make_frame(_label_=_("Software Reliability Assessment Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)
        frame.show_all()

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Assessment\nResults") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays results of software reliability assessments."))
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_results_tab_load(self):
        """
        Loads the gtk.Entry widgets with software reliability assessment
        results information for the SOFTWARE Object.
        """

        _units = [_("Faults/LOC"), "", "", "", "", "", "", "", "", "",
                  _("Lines"), _("Lines"), _("Lines"), "", "", "", "",
                  "", "", "", "", "", "", "", "", "", _("Faults/LOC"), "",
                  "", "", "", "", _("Failures/hour"), _("Failures/hour"),
                  _("Failures/hour"), "", "", "", _("Failures/hour")]

        model = self.tvwResults.get_model()
        model.clear()

        values = (self.model.get_value(self._selected_row, 1),)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT fld_a, fld_dd, fld_dc, fld_d, fld_am, fld_sa, \
                            fld_dr, fld_st, fld_sq, fld_s1, fld_hloc, \
                            fld_aloc, fld_loc, fld_sl, fld_nm, fld_um, \
                            fld_wm, fld_xm, fld_sm, fld_ax, fld_bx, fld_cx, \
                            fld_sx, fld_df, fld_sr, fld_s2, fld_rpfom, \
                            fld_te, fld_tm, fld_tc, fld_t, fld_ft1, fld_ft2, \
                            fld_ren_avg, fld_ren_eot, fld_ev, fld_ew, fld_e, \
                            fld_f \
                     FROM tbl_software \
                     WHERE fld_software_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT fld_a, fld_dd, fld_dc, fld_d, fld_am, fld_sa, \
                            fld_dr, fld_st, fld_sq, fld_s1, fld_hloc, \
                            fld_aloc, fld_loc, fld_sl, fld_nm, fld_um, \
                            fld_wm, fld_xm, fld_sm, fld_ax, fld_bx, fld_cx, \
                            fld_sx, fld_df, fld_sr, fld_s2, fld_rpfom, \
                            fld_te, fld_tm, fld_tc, fld_t, fld_ft1, fld_ft2, \
                            fld_ren_avg, fld_ren_eot, fld_ev, fld_ew, fld_e, \
                            fld_f \
                     FROM tbl_software \
                     WHERE fld_software_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        for i in range(len(results[0])):
            _data = (self._ar_tab_labels[i], float(results[0][i]), _units[i])
            model.append(_data)

        return False

    def calculate(self, widget):
        """
        Method to calculate metrics for the selected Software Object.

        Keyword Arguments:
        widget -- the widget that called this method.
        """

        row = self.model.get_iter_root()
        RPFOM = _calc.calculate_software(self.model, row, self._app)
        self.model.set_value(row, 33, RPFOM)

        return False

    def module_add(self, widget, type_):
        """
        Adds a new Software module to the Program's database.

        Keyword Arguments:
        widget -- the widget that called this function.
        type_  -- the type of Software module to add; 0 = sibling,
                  1 = child.
        """

        if(type_ == 0):
            _iter = self.model.iter_parent(self._selected_row)
            _parent = self.model.get_string_from_iter(_iter)
            n_new_module = _util.add_items(_("Sibling Module"))
        if(type_ == 1):
            _parent = self.model.get_string_from_iter(self._selected_row)
            n_new_module = _util.add_items(_("Child Module"))

        for i in range(n_new_module):

            # Create the default description of the assembly.
            _descrip = str(_conf.RELIAFREE_PREFIX[16]) + ' ' + \
                       str(_conf.RELIAFREE_PREFIX[17])

            # Increment the assembly index.
            _conf.RELIAFREE_PREFIX[17] = _conf.RELIAFREE_PREFIX[17] + 1

            # Find the revision ID.
            if(_conf.RELIAFREE_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id,
                          _parent, _descrip)
            else:
                values = (0, _parent, _descrip)

            # First we add the module to the software table.
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_software \
                         (fld_revision_id, fld_parent_module, \
                          fld_description) \
                         VALUES (%d, '%s', '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_software \
                         (fld_revision_id, fld_parent_module, \
                          fld_description) \
                         VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("software.py: Failed to add new module to software table.")
                return True

            # Retrienve the ID of the newly created module.
            if(_conf.BACKEND == 'mysql'):
                query = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT seq \
                         FROM sqlite_sequence \
                         WHERE name='tbl_software'"

            _id = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

            if(_id == ''):
                self._app.debug_log.error("software.py: Failed to retrieve new module ID.")
                return True

            # Add new software module to the test table.
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_software_tests \
                                     (fld_software_id, fld_technique_id) \
                         VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_software_tests \
                                     (fld_software_id, fld_technique_id) \
                         VALUES (?, ?)"
            for i in len(6):
                values = (_id, i)
                self._app.DB.execute_query(query,
                                           values,
                                           self._app.ProgCnx)

        self.load_tree()

        return False

    def module_delete(self, widget):
        """
        Deletes the currently selected software modules from the Program's
        database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        values = (self.model.get_string_from_iter(self._selected_row),)

        # First delete all of the children from the software table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_software \
                     WHERE fld_parent_module=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_software \
                     WHERE fld_parent_module=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to delete module from software table.")
            return True

        # Second delete the parent from the software table.
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_software \
                     WHERE fld_revision_id=%d \
                     AND fld_software_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_software \
                     WHERE fld_revision_id=? \
                     AND fld_software_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to delete module from software table.")
            return True

        self.load_tree()

        return False

    def create_tree(self):
        """
        Creates the Software gtk.Treeview and connects it to callback functions
        to handle editting.  Background and foreground colors can be set using
        the user-defined values in the RelKit configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RELIAFREE_COLORS[6]
        fg_color = _conf.RELIAFREE_COLORS[7]
        (self.treeview, self._col_order) = _widg.make_treeview('Software', 15,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)

        self.treeview.set_tooltip_text(_("Displays an indentured list (tree) of software."))
        self.treeview.set_enable_tree_lines(True)
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None, 0)
        self.treeview.connect('row_activated', self._treeview_row_changed, 0)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Software treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_software WHERE fld_revision_id=%d"
        if(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_software WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_assemblies = len(results)

        self.model.clear()
        self._selected_row = None

        # Load the model with the returned results.
        for i in range(n_assemblies):

            if(results[i][34] == '-'):      # It's the top level element.
                piter = None
            elif(results[i][34] != '-'):    # It's a child element.
                piter = self.model.get_iter_from_string(results[i][34])

            self.model.append(piter, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Software Object
        treeview.

        Keyword Arguments:
        treeview -- the Software Object treeview.
        event    -- a gtk.gdk.Event that called this function (the
                    important attribute is which mouse button was clicked).
                    1 = left
                    2 = scrollwheel
                    3 = right
                    4 = forward
                    5 = backward
                    8 =
                    9 =
        """

        if(event.button == 1):
            self._treeview_row_changed(treeview, None, 0, 0)
        elif(event.button == 3):
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, path, column, _index_):
        """
        Callback function to handle events for the SOFTWARE Object
        gtk.Treeview.  It is called whenever the Software Object treeview is
        clicked or a row is activated.  It will save the previously selected
        row in the Software Object treeview.  Then it loads the SOFTWARE Object.

        Keyword Arguments:
        treeview -- the Software Object treeview.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        _index_  -- determined which treeview had the change (0 = main
                    treeview, 1 = incident list treeview, 2 = incident
                    action list treeview)
        """

        # Save the previously selected row in the Software tree.
        if(_index_ == 0):                   # The main software treeview.
            if self._selected_row is not None:
                path_ = self.model.get_path(self._selected_row)
                self._save_line_item(self.model, path_, self._selected_row)

            selection = self.treeview.get_selection()
            (self.model, self._selected_row) = selection.get_selected()
            self.software_id = self.model.get_value(self._selected_row, 1)

            # Build the queries to select the reliability tests and program
            # incidents associated with the selected HARDWARE.
            values = (self.software_id, )
            if(_conf.BACKEND == 'mysql'):
                qryIncidents = "SELECT * FROM tbl_incident \
                                WHERE fld_software_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                qryIncidents = "SELECT * FROM tbl_incident \
                                WHERE fld_software_id=?"

            if self._selected_row is not None:
                self.load_notebook()
                self._app.winParts.load_incident_tree(qryIncidents, values)
                return False
            else:
                return True

    def load_notebook(self):
        """ Method to load the SOFTWARE Object gtk.Notebook. """

        # Get the application level ID and development phase ID.
        _level_id = self.model.get_value(self._selected_row, 2)
        _phase_id = self.model.get_value(self._selected_row, 36)

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxSoftware)
        self._app.winWorkBook.show_all()

        # Always display the General Data page.
        self._general_data_tab_load()

        if(_level_id == 1):                 # System
            self._assessment_results_tab_load()
            self.chkTC11.hide()
            self.chkTC12.hide()
            self.lblWS3_1.hide()
            self.lblWS3_2.hide()
            self.lblWS3_3.hide()
            self.lblWS3_4.hide()

        elif(_level_id == 2):               # CSCI
            self._worksheet_1_tab_load()
            self._worksheet_2_tab_load()
            self._worksheet_3_tab_load()
            self._worksheet_4_tab_load()
            self._worksheet_9_tab_load()
            self._worksheet_11_tab_load()
            self._test_selection_tab_load()
            self._reliability_growth_tab_load()
            self._reliability_estimation_tab_load()
            self._assessment_results_tab_load()

        elif(_level_id == 3):               # Unit
            if(_phase_id == 4):
                self._worksheet_2_tab_load()
                self._worksheet_4_tab_load()

            elif(_phase_id == 5):
                self._worksheet_8_tab_load()
                self._worksheet_11_tab_load()
                self._test_selection_tab_load()
                self._reliability_growth_tab_load()
                self._reliability_estimation_tab_load()

        self.notebook.set_current_page(0)

        _title_ = _("RelKit Work Bench: Analyzing %s") % \
                  self.model.get_value(self._selected_row, 3)
        self._app.winWorkBook.set_title(_title_)

        return False

    def _callback_check(self, check, _index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check   -- the checkbutton that called the function.
        _index_ -- the position in the Software Object _attribute list
                   associated with the data from the calling checkbutton.
        """

        if(_index_ < 100):                  # Main Software Tree.
            self.model.set_value(self._selected_row,
                                 _index_,
                                 check.get_active())

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the Software Object gtk.TreeView
                   associated with the data from the calling combobox.
        """

        i = combo.get_active()

        if(_index_ < 100):
            if(_index_ == 2):                   # Software level
                _phase_id = self.model.get_value(self._selected_row, 36)
                self._add_assessment_questions(_phase_id, i)
            #elif(_index_ == 4):                # Application type
            #    self.model.set_value(self._selected_row, 6, self._fault_density[i])
            #elif(_index_ == 5):                # Development environment
            #    self.model.set_value(self._selected_row, 7, self._do[i])
            elif(_index_ == 36):                # Development phase
                _level_id = self.model.get_value(self._selected_row, 2)
                self._add_assessment_questions(i, _level_id)

            elif(_index_ == 38):
                _level_id = self.model.get_value(self._selected_row, 2)
                if(_level_id == 2):
                    self.btnUnitSingleMatrix.hide()
                    self.btnUnitPairedMatrix.hide()
                    if(i == 1):
                        self.btnSoftwareMatrix.show()
                        self.btnErrorCatMatrix.hide()
                        self.btnCSCISingleMatrix.hide()
                        self.btnCSCIPairedMatrix.hide()
                    elif(i == 2):
                        self.btnSoftwareMatrix.hide()
                        self.btnErrorCatMatrix.show()
                        self.btnCSCISingleMatrix.show()
                        self.btnCSCIPairedMatrix.show()
                    else:
                        self.btnSoftwareMatrix.hide()
                        self.btnErrorCatMatrix.hide()
                        self.btnCSCISingleMatrix.hide()
                        self.btnCSCIPairedMatrix.hide()
                elif(_level_id == 3):
                    self.btnCSCISingleMatrix.hide()
                    self.btnCSCIPairedMatrix.hide()
                    if(i == 1):
                        self.btnSoftwareMatrix.show()
                        self.btnErrorCatMatrix.hide()
                        self.btnUnitSingleMatrix.hide()
                        self.btnUnitPairedMatrix.hide()
                    elif(i == 2):
                        self.btnSoftwareMatrix.hide()
                        self.btnErrorCatMatrix.show()
                        self.btnUnitSingleMatrix.show()
                        self.btnUnitPairedMatrix.show()
                    else:
                        self.btnSoftwareMatrix.hide()
                        self.btnErrorCatMatrix.hide()
                        self.btnUnitSingleMatrix.hide()
                        self.btnUnitPairedMatrix.hide()

            elif(_index_ == 40):            # Test effort.
                if(i == 1):
                    self.txtLaborTest.props.editable = True
                    self.txtLaborTest.set_sensitive(True)
                    self.txtLaborDev.props.editable = True
                    self.txtLaborDev.set_sensitive(True)
                    self.txtBudgetTest.props.editable = False
                    self.txtBudgetTest.set_sensitive(False)
                    self.txtBudgetDev.props.editable = False
                    self.txtBudgetDev.set_sensitive(False)
                    self.txtScheduleTest.props.editable = False
                    self.txtScheduleTest.set_sensitive(False)
                    self.txtScheduleDev.props.editable = False
                    self.txtScheduleDev.set_sensitive(False)
                elif(i == 2):
                    self.txtLaborTest.props.editable = False
                    self.txtLaborTest.set_sensitive(False)
                    self.txtLaborDev.props.editable = False
                    self.txtLaborDev.set_sensitive(False)
                    self.txtBudgetTest.props.editable = True
                    self.txtBudgetTest.set_sensitive(True)
                    self.txtBudgetDev.props.editable = True
                    self.txtBudgetDev.set_sensitive(True)
                    self.txtScheduleTest.props.editable = False
                    self.txtScheduleTest.set_sensitive(False)
                    self.txtScheduleDev.props.editable = False
                    self.txtScheduleDev.set_sensitive(False)
                elif(i == 3):
                    self.txtLaborTest.props.editable = False
                    self.txtLaborTest.set_sensitive(False)
                    self.txtLaborDev.props.editable = False
                    self.txtLaborDev.set_sensitive(False)
                    self.txtBudgetTest.props.editable = False
                    self.txtBudgetTest.set_sensitive(False)
                    self.txtBudgetDev.props.editable = False
                    self.txtBudgetDev.set_sensitive(False)
                    self.txtScheduleTest.props.editable = True
                    self.txtScheduleTest.set_sensitive(True)
                    self.txtScheduleDev.props.editable = True
                    self.txtScheduleDev.set_sensitive(True)

            elif(_index_ == 41):            # Test approach.
                if(i == 2):
                    self.btnStoppingRules.show()
                else:
                    self.btnStoppingRules.hide()

            self.model.set_value(self._selected_row, _index_, i)

            self._worksheet_2_tab_load()
            self._worksheet_3_tab_load()
            self._worksheet_4_tab_load()
            self._worksheet_11_tab_load()

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry    -- the entry that called the function.
        event    -- the gtk.gdk.Event that called the function.
        convert  -- the data type to convert the entry contents to.
        _index_  -- the position in the Software Object gtk.TreeView
                    associated with the data from the calling entry.
        """

        from datetime import datetime

        if(convert == 'text'):
            if(_index_ == 3):
                textbuffer = self.txtDescription.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            try:
                _text_ = int(entry.get_text())
            except ValueError:
                _text_ = 0

        elif(convert == 'float'):
            _text_ = float(entry.get_text().replace('$', ''))

        elif(convert == 'date'):
            _text_ = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        if(_index_ < 100):                  # Software information.
            # Calculate the number of higher order language lines of code.
            if(_index_ == 18):
                ALOC = self.model.get_value(self._selected_row, 18)
                SLOC = self.model.get_value(self._selected_row, 19)
                HLOC = SLOC - _text_
                try:
                    SL = (float(HLOC)/float(_text_)) + 1.4 * (float(ALOC)/float(_text_))
                except ZeroDivisionError:
                    SL = 0.0
                self.txt83.set_text(str(HLOC))
                self.model.set_value(self._selected_row, 17, HLOC)
                self.model.set_value(self._selected_row, 20, SL)
            elif(_index_ == 19):
                ALOC = self.model.get_value(self._selected_row, 18)
                SLOC = self.model.get_value(self._selected_row, 19)
                HLOC = _text_ - ALOC
                try:
                    SL = (float(HLOC)/float(_text_)) + 1.4 * (float(ALOC)/float(_text_))
                except ZeroDivisionError:
                    SL = 0.0
                self.txt83.set_text(str(HLOC))
                self.model.set_value(self._selected_row, 17, HLOC)
                self.model.set_value(self._selected_row, 20, SL)

            # Update the Software Tree.
            self.model.set_value(self._selected_row, _index_, _text_)

    def _add_assessment_questions(self, _phase_id, _level_id):
        """
        Method to add assessment questions based on changes to the development
        phase ID and/or software indenture level ID.

        Keyword Arguments:
        _phase_id -- the numerical ID of the development phase.
        _level_id -- the numerical ID of the software indenture level.
        """

        # Insert each of the questions for the different development
        # phases.  The three fields make up the primary key, therefore
        # it's not possible to keep inserting the same questions.
        if(_phase_id == 1 and _level_id == 1):      # SRR and System
            n_anomaly_questions = 0
            n_trace_questions = 0
            n_quality_questions = 0
            n_standards_questions = 0
        elif(_phase_id == 2 and _level_id == 2):    # SSR and CSCI
            n_anomaly_questions = 22
            n_trace_questions = 1
            n_quality_questions = 27
            n_standards_questions = 0
        elif(_phase_id == 3 and _level_id == 2):    # PDR and CSCI
            n_anomaly_questions = 14
            n_trace_questions = 1
            n_quality_questions = 24
            n_standards_questions = 0
        elif(_phase_id == 4 and _level_id == 2):    # CDR and CSCI
            n_anomaly_questions = 12
            n_trace_questions = 2
            n_quality_questions = 26
            n_standards_questions = 0
        elif(_phase_id == 4 and _level_id == 3):    # CDR and Unit
            n_anomaly_questions = 2
            n_trace_questions = 0
            n_quality_questions = 14
            n_standards_questions = 0
        elif(_phase_id == 5 and _level_id == 2):    # TRR and CSCI
            n_anomaly_questions = 0
            n_trace_questions = 0
            n_quality_questions = 0
            n_standards_questions = 40
        elif(_phase_id == 5 and _level_id == 3):    # TRR and Unit
            n_anomaly_questions = 0
            n_trace_questions = 0
            n_quality_questions = 0
            n_standards_questions = 34
        else:
            return False

        if(_level_id == 2):                 # This is a CSCI.

            for j in range(43):
                # Add the CSCI to the detailed software development
                # assessment table.
                values = (self.software_id, j)
                if(_conf.BACKEND == 'mysql'):
                    query = "INSERT INTO 'tbl_software_development' \
                             (fld_software_id, fld_question_id) \
                             VALUES(%d, %d)"
                elif(_conf.BACKEND == 'sqlite3'):
                    query = "INSERT INTO 'tbl_software_development' \
                             (fld_software_id, fld_question_id) \
                             VALUES(?, ?)"

                results = self._app.DB.execute_query(query,
                                                     values,
                                                     self._app.ProgCnx,
                                                     commit=True)

                if not results:
                    #_util.application_error(_("Failed to add new module to software development table for module %d and question %d." % values))
                    self._app.debug_log.error("software.py: Failed to add new module to software development table.")
                    return True

        # Insert rows to the anomaly management table.
        for j in range(n_anomaly_questions):
            values = (self.software_id, _phase_id, j)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_anomaly_management \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_anomaly_management \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

        # Insert rows to the software traceability table.
        for j in range(n_trace_questions):
            values = (self.software_id, _phase_id, j)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_software_traceability \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_software_traceability \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

        # Insert rows to the software quality table.
        for j in range(n_quality_questions):
            values = (self.software_id, _phase_id, j)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_software_quality \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_software_quality \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

        # Insert rows in the software standards table.
        for j in range(n_standards_questions):
            values = (self.software_id, _phase_id, j)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_software_standards \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_software_standards \
                         (fld_software_id, fld_phase_id, fld_question_id) \
                         VALUES(?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

        # Insert rows in the software traceability table.
        for j in range(2):
            values = (self.software_id, _phase_id, 0, 0)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_software_traceability \
                         (fld_software_id, fld_phase_id, fld_tc11, fld_tc12) \
                         VALUES(%d, %d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_software_traceability \
                         (fld_software_id, fld_phase_id, fld_tc11, fld_tc12) \
                         VALUES(?, ?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

        return False

    def software_save(self):
        """
        Saves the SOFTWARE Object treeview information to the RelKit Program's
        MySQL or SQLit3 database.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the SOFTWARE Object treeview model to the MySQL or
        SQLite3 database.

        Keyword Arguments:
        model -- the Software Object treemodel.
        path_ -- the path of the active row in the Software Object
                 treemodel.
        row   -- the selected row in the Software Object treeview.
        """

        values = (model.get_value(row, self._col_order[2]),
                  model.get_value(row, self._col_order[3]),
                  model.get_value(row, self._col_order[4]),
                  model.get_value(row, self._col_order[5]),
                  model.get_value(row, self._col_order[6]),
                  model.get_value(row, self._col_order[7]),
                  model.get_value(row, self._col_order[8]),
                  model.get_value(row, self._col_order[9]),
                  model.get_value(row, self._col_order[10]),
                  model.get_value(row, self._col_order[11]),
                  model.get_value(row, self._col_order[12]),
                  model.get_value(row, self._col_order[13]),
                  model.get_value(row, self._col_order[14]),
                  model.get_value(row, self._col_order[15]),
                  model.get_value(row, self._col_order[16]),
                  model.get_value(row, self._col_order[17]),
                  model.get_value(row, self._col_order[18]),
                  model.get_value(row, self._col_order[19]),
                  model.get_value(row, self._col_order[20]),
                  model.get_value(row, self._col_order[21]),
                  model.get_value(row, self._col_order[22]),
                  model.get_value(row, self._col_order[23]),
                  model.get_value(row, self._col_order[24]),
                  model.get_value(row, self._col_order[25]),
                  model.get_value(row, self._col_order[26]),
                  model.get_value(row, self._col_order[27]),
                  model.get_value(row, self._col_order[28]),
                  model.get_value(row, self._col_order[29]),
                  model.get_value(row, self._col_order[30]),
                  model.get_value(row, self._col_order[31]),
                  model.get_value(row, self._col_order[32]),
                  model.get_value(row, self._col_order[33]),
                  model.get_value(row, self._col_order[34]),
                  model.get_value(row, self._col_order[35]),
                  model.get_value(row, self._col_order[36]),
                  model.get_value(row, self._col_order[37]),
                  model.get_value(row, self._col_order[38]),
                  model.get_value(row, self._col_order[39]),
                  model.get_value(row, self._col_order[40]),
                  model.get_value(row, self._col_order[41]),
                  model.get_value(row, self._col_order[42]),
                  model.get_value(row, self._col_order[43]),
                  model.get_value(row, self._col_order[44]),
                  model.get_value(row, self._col_order[45]),
                  model.get_value(row, self._col_order[46]),
                  model.get_value(row, self._col_order[47]),
                  model.get_value(row, self._col_order[48]),
                  model.get_value(row, self._col_order[49]),
                  model.get_value(row, self._col_order[50]),
                  model.get_value(row, self._col_order[51]),
                  model.get_value(row, self._col_order[52]),
                  model.get_value(row, self._col_order[53]),
                  model.get_value(row, self._col_order[54]),
                  model.get_value(row, self._col_order[55]),
                  model.get_value(row, self._col_order[56]),
                  model.get_value(row, self._col_order[57]),
                  model.get_value(row, self._col_order[58]),
                  model.get_value(row, self._col_order[59]),
                  model.get_value(row, self._col_order[60]),
                  model.get_value(row, self._col_order[61]),
                  model.get_value(row, self._col_order[62]),
                  model.get_value(row, self._col_order[63]),
                  model.get_value(row, self._col_order[64]),
                  model.get_value(row, self._col_order[65]),
                  model.get_value(row, self._col_order[66]),
                  model.get_value(row, self._col_order[67]),
                  model.get_value(row, self._col_order[68]),
                  model.get_value(row, self._col_order[69]),
                  model.get_value(row, self._col_order[0]),
                  model.get_value(row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_software \
                     SET fld_level_id=%d, fld_description='%s', \
                         fld_application_id=%d, fld_development_id=%d, \
                         fld_a=%f, fld_do=%f, fld_dd=%d, fld_dc=%f, \
                         fld_d=%f, fld_am=%f, fld_sa=%f, fld_st=%f, \
                         fld_dr=%f, fld_sq=%f, fld_s1=%f, fld_hloc=%d, \
                         fld_aloc=%d, fld_loc=%d, fld_sl=%f, fld_ax=%d, \
                         fld_bx=%d, fld_cx=%d, fld_nm=%d, fld_sx=%f, \
                         fld_um=%d, fld_wm=%d, fld_xm=%d, fld_sm=%f, \
                         fld_df=%f, fld_sr=%f, fld_s2=%f, fld_rpfom=%f, \
                         fld_parent_module='%s', fld_dev_assess_type=%d, \
                         fld_phase_id=%d, fld_tcl=%d, fld_test_path=%d, \
                         fld_category=%d, fld_test_effort=%d, \
                         fld_test_approach=%d, fld_labor_hours_test=%f, \
                         fld_labor_hours_dev=%f, fld_budget_test=%f, \
                         fld_budget_dev=%f, fld_schedule_test=%f, \
                         fld_schedule_dev=%f, fld_branches=%d, \
                         fld_branches_test=%d, fld_inputs=%d, \
                         fld_inputs_test=%d, fld_nm_test=%d, \
                         fld_interfaces=%d, fld_interfaces_test=%d, \
                         fld_te=%f, fld_tc=%f, fld_tm=%f, fld_t=%f, \
                         fld_ft1=%f, fld_ft2=%f, fld_ren_avg=%f, \
                         fld_ren_eot=%f, fld_ec=%f, fld_ev=%f, fld_et=%f, \
                         fld_os=%f, fld_ew=%f, fld_e=%f, fld_f=%f \
                 WHERE fld_revision_id=%d AND fld_software_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_software \
                     SET fld_level_id=?, fld_description=?, \
                         fld_application_id=?, fld_development_id=?, \
                         fld_a=?, fld_do=?, fld_dd=?, fld_dc=?, \
                         fld_d=?, fld_am=?, fld_sa=?, fld_st=?, \
                         fld_dr=?, fld_sq=?, fld_s1=?, fld_hloc=?, \
                         fld_aloc=?, fld_loc=?, fld_sl=?, fld_ax=?, \
                         fld_bx=?, fld_cx=?, fld_nm=?, fld_sx=?, \
                         fld_um=?, fld_wm=?, fld_xm=?, fld_sm=?, \
                         fld_df=?, fld_sr=?, fld_s2=?, fld_rpfom=?, \
                         fld_parent_module=?, fld_dev_assess_type=?, \
                         fld_phase_id=?, fld_tcl=?, fld_test_path=?, \
                         fld_category=?, fld_test_effort=?, \
                         fld_test_approach=?, fld_labor_hours_test=?, \
                         fld_labor_hours_dev=?, fld_budget_test=?, \
                         fld_budget_dev=?, fld_schedule_test=?, \
                         fld_schedule_dev=?, fld_branches=?, \
                         fld_branches_test=?, fld_inputs=?, \
                         fld_inputs_test=?, fld_nm_test=?, \
                         fld_interfaces=?, fld_interfaces_test=?, \
                         fld_te=?, fld_tc=?, fld_tm=?, fld_t=?, \
                         fld_ft1=?, fld_ft2=?, fld_ren_avg=?, \
                         fld_ren_eot=?, fld_ec=?, fld_ev=?, fld_et=?, \
                         fld_os=?, fld_ew=?, fld_e=?, fld_f=? \
                    WHERE fld_revision_id=? AND fld_software_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("software.py: Failed to save software to software table.")
            return True

        return False

    def _save_test_techniques(self, button):
        """
        Method to save the test techniques for the currently selected
        software module.

        Keyword ArgumentsL
        button -- the gtk.Button widget that called this method.
        """

        self.model.set_value(self._selected_row, 37, self.cmbTCL.get_active())
        self.model.set_value(self._selected_row, 38,
                             self.cmbTestPath.get_active())

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_software_tests \
                     SET fld_effectiveness_single=%d, \
                         fld_effectiveness_paired=%d, \
                         fld_coverage_single=%d, fld_coverage_paired=%d, \
                         fld_error_cat=%d, fld_used=%d, fld_remarks='%s' \
                         WHERE fld_software_id=%d \
                         AND fld_technique_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_software_tests \
                     SET fld_effectiveness_single=?, \
                         fld_effectiveness_paired=?, \
                         fld_coverage_single=?, fld_coverage_paired=?, \
                         fld_error_cat=?, fld_used=?, fld_remarks=? \
                         WHERE fld_software_id=? \
                         AND fld_technique_id=?"

        model = self.tvwTestSelectionMatrix.get_model()
        row = model.get_iter_root()
        for i in range(5):
            values = (model.get_value(row, 1), model.get_value(row, 2),
                      model.get_value(row, 3), model.get_value(row, 4),
                      model.get_value(row, 5), model.get_value(row, 6),
                      model.get_value(row, 7), self.software_id, i)

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("software.py: Failed to save test techniques to software test table.")
                return True

            row = model.iter_next(row)

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = General Data
                    1 = Worksheet 1
                    2 = Worksheet 2
                    3 = Worksheet 3
                    4 = Worksheet 4
                    5 = Worksheet 8
                    6 = Worksheet 9
                    7 = Worksheet 11
                    8 = Test Planning
        """

        if(page_num == 1):                  # Worksheet 1
            self.btnSaveResults.set_tooltip_text(_("Saves development environment information for the selected software module."))
        elif(page_num == 2):                # Worksheet 2
            self.btnSaveResults.set_tooltip_text(_("Saves anomaly management information for the selected software module."))
        elif(page_num == 3):                # Worksheet 3
            self.btnSaveResults.set_tooltip_text(_("Saves requirements traceability information for the selected software module."))
        elif(page_num == 4):                # Worksheet 4
            self.btnSaveResults.set_tooltip_text(_("Saves quality review information for the selected software module."))
        elif(page_num == 5):                # Worksheet 8
            self.btnSaveResults.set_tooltip_text(_("Saves language type information for the selected software module."))
        elif(page_num == 6):                # Worksheet 9
            self.btnSaveResults.set_tooltip_text(_("Saves modularity and complexity information for the selected software module."))
        elif(page_num == 7):                # Worksheet 11
            self.btnSaveResults.set_tooltip_text(_("Saves standards review information for the selected software module."))
        elif(page_num == 8):                # RG tracking tab
            self.btnSaveResults.set_tooltip_text(_("Saves test planning information for the selected software module."))
        else:                               # Everything else
            self.btnSaveResults.set_tooltip_text(_("Saves the selected software module."))

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to reacte to the SOFTWARE Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 1):                    # Worksheet 1
            if(_button_ == 'Save'):
                self._worksheet_1_save()
        elif(_page_ == 2):                  # Worksheet 2
            if(_button_ == 'Save'):
                self._worksheet_2_save()
        elif(_page_ == 3):                  # Worksheet 3
            if(_button_ == 'Save'):
                self._worksheet_3_save()
        elif(_page_ == 4):                  # Worksheet 4
            if(_button_ == 'Save'):
                self._worksheet_4_save()
        elif(_page_ == 5):                  # Worksheet 8.
            if(_button_ == 'Save'):
                self._worksheet_8_save()
        elif(_page_ == 7):                  # Worksheet 11.
            if(_button_ == 'Save'):
                self._worksheet_11_save()
        else:                               # Everything else.
            if(_button_ == 'Save'):
                self.software_save()

        return False
