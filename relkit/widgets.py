#!/usr/bin/env python
""" widgets contains functions for creating, populating, destroying, and
    interacting with pyGTK widgets.  Import this module as _widg in other
    modules that create, populate, destroy, or interact with pyGTK widgets in
    the RelKit application.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       widgets.py is part of The RelKit Project
#
# All rights reserved.

import sys

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

import pango

# Import other RelKit modules.
import configuration as _conf

import gettext
_ = gettext.gettext


def make_button(_height_=40, _width_=0, _label_="", _image_='default'):
    """
    Utility function to create Button widgets.

    Keyword Arguments:
    _width_ -- the width of the Button widget.
    _label_ -- the text to display with the Button widget.
               Default is None.
    _image_ -- the file image to display on the Button.
    """

    if(_width_ == 0):
        _width_ = int((int(_conf.PLACES) + 5) * 8)

    button = gtk.Button(label=_label_)

    if(_image_ is not None):
        if(_width_ >= 32):
            file_image = _conf.ICON_DIR + '32x32/' + _image_ + '.png'
        else:
            file_image = _conf.ICON_DIR + '16x16/' + _image_ + '.png'
        image = gtk.Image()
        image.set_from_file(file_image)
        button.set_image(image)

    button.props.width_request = _width_
    button.props.height_request = _height_

    return(button)


def make_check_button(_label_=None):

    """ Utility function to create CheckButton widgets.

        Keyword Arguments:
        _label_ -- the text to display with the CheckButton widget.
                   Default is None.

    """

    checkbutton = gtk.CheckButton(_label_, True)
    if(_label_ is not None):
        checkbutton.get_child().set_use_markup(True)

    return(checkbutton)


def make_combo(_width_=200, _height_=30, simple=True):

    """ Utility function to create ComboBox widgets.

        Keyword Arguments:
        width  -- width of the ComboBox widget.  Default is 200.
        height -- height of the ComboBOx widget.  Default is 30.
        simple -- boolean indicating whether to create a simple text ComboBox.
                  Defaults to True.
    """

    if simple:
        combo = gtk.combo_box_new_text()
    else:
        list_ = gtk.TreeStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        combo = gtk.ComboBox(list_)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.set_attributes(cell, text=0)

    combo.props.width_request = _width_
    combo.props.height_request = _height_

    return(combo)


def load_combo(combo, _list_, simple=True, _index_=0):

    """ Utility function to load gtk.ComboBox widgets.

        Keyword Arguments:
        combo   -- the gtk.ComboBox to load.
        _list_  -- the information to load into the gtk.ComboBox.
        simple  -- indicates whether the load is simple (single column) or
                   complex (multiple columns).
        _index_ -- the index in the list to display.  Only used when doing a
                   simple load.
    """

    model = combo.get_model()
    model.clear()

    if simple:
        combo.append_text("")
        for i in range(len(_list_)):
            combo.append_text(_list_[i][_index_])
    else:
        model.append(None, ["", "", ""])
        for i in range(len(_list_)):
            model.append(None, _list_[i])

    return False


def make_dialog(_title_, _parent_=None,
                _flags_=(gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT),
                _buttons_=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                           gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)):
    """
    Utility function to create Dialog widgets.

    Keyword Arguments:
    _title_   -- the title text for the Dialog.
    _parent_  -- the parent window to associate the Dialog with.  Defaults to
                 None.
    _flags_   -- the flags that control the operation of the Dialog.  Defaults
                 to gtk.DIALOG_MODAL and gtk.DIALOG_DESTROY_WITH_PARENT.
    _buttons_ -- the buttons to display and their response values.  Defaults to
                 gtk.STOCK_OK <==> gtk.RESPONSE_ACCEPT and
                 gtk.STOCK_CANCEL <==> gtk.RESPONSE_REJECT.
    """

    dialog = gtk.Dialog(title=_title_,
                        parent=_parent_,
                        flags=_flags_,
                        buttons=_buttons_)

    dialog.set_has_separator(True)

    return(dialog)


def make_entry(_width_=200, _height_=25,
               editable=True, bold=False,
               _color_='#BBDDFF'):
    """
    Utility function to create Entry widgets.

    Keyword Arguments:
    width    -- width of the Entry widget.  Default is 200.
    eight    -- height of the Entry widget.  Default is 25.
    editable -- boolean indicating whether Entry should be editable.
                Defaults to True.
    bold     -- boolean indicating whether text should be bold.  Defaults
                to False.
    _color_  -- the hexidecimal color to set the foreground.  Defaults to
                #FFF (light grey).
    """

    entry = gtk.Entry()
    entry.props.width_request = _width_
    entry.props.height_request = _height_
    entry.props.editable = editable

    if bold:
        entry.modify_font(pango.FontDescription('bold'))

    if not editable:
        bg_color = gtk.gdk.Color(_color_)
        entry.modify_base(gtk.STATE_NORMAL, bg_color)
        entry.modify_base(gtk.STATE_ACTIVE, bg_color)
        entry.modify_base(gtk.STATE_PRELIGHT, bg_color)
        entry.modify_base(gtk.STATE_SELECTED, bg_color)
        entry.modify_base(gtk.STATE_INSENSITIVE, bg_color)
        entry.modify_font(pango.FontDescription('bold'))

    entry.show()

    return(entry)


def make_label(text, width=190, height=25, bold=True):

    """ Utility function to create Label widgets.

        Keyword Arguments:
        text   -- the text to display in the Label widget.
        width  -- width of the Label widget.  Default is 190.
        height -- height of the Label widget.  Default is 25.
        bold   -- boolean indicating whether text should be bold.  Defaults
                  to True.
    """

    label = gtk.Label()
    label.set_markup("<span>" + text + "</span>")
    label.set_line_wrap(True)
    label.set_alignment(xalign=0.5, yalign=0.5)
    label.set_justify(gtk.JUSTIFY_CENTER)
    label.props.width_request = width
    label.props.height_request = height

    if not bold:
        label.modify_font(pango.FontDescription('normal'))
    else:
        label.modify_font(pango.FontDescription('bold'))

    label.show()

    return(label)


def make_text_view(buffer_=None, width=200, height=100):

    """ Utility function to create TextView widgets.

        Keyword Arguments:
        buffer_ -- the TextBuffer to associate with the TextView.  Default is
                   None.
        width   -- width of the TextView widget.  Default is 200.
        height  -- height of the TextView widget.  Default is 100.

    """

    view = gtk.TextView(buffer=buffer_)
    view.set_wrap_mode(gtk.WRAP_WORD)

    scrollwindow = gtk.ScrolledWindow()
    scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrollwindow.props.width_request = width
    scrollwindow.props.height_request = height
    scrollwindow.add_with_viewport(view)

    return(scrollwindow)


def make_frame(_label_=""):

    """
    Utility function to create gtk.Frame() widgets.

    Keyword Arguments:
    _label_ -- the text to display in the frame's label.
    '"""

    label = gtk.Label()
    label.set_markup("<span weight='bold'>" +
                     _label_ +
                     "</span>")
    label.set_justify(gtk.JUSTIFY_LEFT)
    label.set_alignment(xalign=0.5, yalign=0.5)
    label.show_all()

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_IN)
    frame.set_label_widget(label)

    return(frame)


def make_fixed():

    fixed = gtk.Fixed()

    return(fixed)


def make_treeview(name, fmt_idx, _app, _list, bg_col='white', fg_col='black'):

    """ Utility function to create TreeView widgets.

        Keyword Arguments:
        name    -- the name of the TreeView to read formatting information
                   for.
        fmt_idx -- the index of the format file to use when creating the
                   TreeView.
        _app    -- the RelKit application.
        _list   -- the list of items to load into the gtk.CellRendererCombo.
        bg_col  -- the background color to use for each row.  Defaults to
                   white.
        fg_col  -- the foreground (text) color to use for each row.  Defaults
                   to black.
    """

    from lxml import etree

    # Retrieve the column heading text from the format file.
    path = "/root/tree[@name='%s']/column/usertitle" % name
    heading = etree.parse(_conf.RELIAFREE_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve the column datatype from the format file.
    path = "/root/tree[@name='%s']/column/datatype" % name
    datatype = etree.parse(_conf.RELIAFREE_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve the column position from the format file.
    path = "/root/tree[@name='%s']/column/position" % name
    position = etree.parse(_conf.RELIAFREE_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve whether or not the column is editable from the format file.
    path = "/root/tree[@name='%s']/column/editable" % name
    editable = etree.parse(_conf.RELIAFREE_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve whether or not the column is visible from the format file.
    path = "/root/tree[@name='%s']/column/visible" % name
    visible = etree.parse(_conf.RELIAFREE_FORMAT_FILE[fmt_idx]).xpath(path)

    # Create a list of GObject datatypes to pass to the model.
    types = []
    for i in range(len(position)):
        types.append(datatype[i].text)

    #if(name == 'Revision'):
    #    query = "SELECT * FROM tbl_revision_format"
    #    results = _app.DB.execute_query(query,
    #                                    None,
    #                                    _app.ProgCnx)
    #    _types = []
    #    for i in range(len(results)):
    #        _types.append(results[i][3])
    #    print _types
    #    print types

    gobject_types = []
    gobject_types = [gobject.type_from_name(types[ix])
         for ix in range(len(types))]

    # If this is the Hardware tree, add a column for a pixbuf.
    if(fmt_idx == 3):
        gobject_types.append(gtk.gdk.Pixbuf)

    # Create the model and treeview.
    model = gtk.TreeStore(*gobject_types)
    treeview = gtk.TreeView(model)
    treeview.set_name(name)
    cols = int(len(heading))
    _visible = False
    order = []
    for i in range(cols):
        order.append(int(position[i].text))

        cell = gtk.CellRendererText()
        cell.set_property('editable', int(editable[i].text))

        if(int(editable[i].text) == 0):
            cell.set_property('background', 'light gray')
        else:
            cell.set_property('background', bg_col)
            cell.set_property('foreground', fg_col)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.connect('edited', edit_tree, int(position[i].text), model)

        # If this is the Hardware tree, add a column for a pixbuf.
        if(i == 1 and fmt_idx == 3):
            column = gtk.TreeViewColumn("")
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols)
        else:
            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            column.set_attributes(cell, text=int(position[i].text))

        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        text = _(heading[i].text)
        label.set_markup("<span weight='bold'>" + text + "</span>")
        label.show_all()
        column.set_widget(label)

        column.set_cell_data_func(cell, format_cell,
                                  (int(position[i].text), datatype[i].text))
        column.set_resizable(True)
        column.connect('notify::width', resize_wrap, cell)

        if(i > 0):
            column.set_reorderable(True)

        treeview.append_column(column)

    return(treeview, order)


def format_cell(column, cell, model, iter, data_):

    """ Function to set the formatting of the gtk.Treeview gtk.CellRenderers.

        Keyword Arguments:
        column -- the gtk.TreeViewColumn containing the gtk.CellRenderer to
                  format.
        cell   -- the gtk.CellRenderer to format.
        model  -- the gtk.TreeModel containing the gtk.TreeViewColumn.
        iter   -- the gtk.TreeIter pointing to the row containing the
                  gtk.CellRenderer to format.
        data_  -- a tuple containing the position and the data type.
    """

    if(data_[1] == 'gfloat'):
        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'
    elif(data_[1] == 'gint'):
        fmt = '{0:0.0f}'
    else:
        return

    val = model.get_value(iter, data_[0])
    cell.set_property('text', fmt.format(val))

    return


def edit_tree(cell, path, new_text, position, model):

    """ Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
    """

    type = gobject.type_name(model.get_column_type(position))

    if(type == 'gchararray'):
        model[path][position] = str(new_text)
    elif(type == 'gint'):
        model[path][position] = int(new_text)
    elif(type == 'gfloat'):
        model[path][position] = float(new_text)

    return False


def resize_wrap(column, param, cell):
    """
    This function dynamically sets the wrap-width property for the
    gtk.CellRenderers in the gtk.TreeView when the column width is resized.

    Keyword Arguments:
    column -- the column being resized.
    param  -- the triggering parameter (this is a GParamInt object).
    cell   -- the cell that needs to be resized.
    """

    # TODO: Adjust the height of the row when the width is adjusted.
    width = column.get_width()
    tree=column.get_tree_view().get_name()

    if width <= 0:
        return
    else:
        width += 10

    cell.set_property('wrap-width', width)

    return False


def make_column_heading(_heading_=""):
    """
    This function creates labels to use for gtk.TreeView column headings.

    Keyword Arguments:
    _heading_ -- the text to use for the heading.
    """

    _heading_ = "<span weight='bold'>%s</span>" % unicode(_heading_)

    label = gtk.Label()
    label.set_markup(_heading_)
    label.set_alignment(xalign=0.5, yalign=0.5)
    label.set_justify(gtk.JUSTIFY_CENTER)
    label.set_line_wrap(True)
    label.show_all()

    return(label)



def load_plot(axis, plot, x, y1=None, y2=None, y3=None,
              _title_="", _xlab_="", _ylab_="", _type_=[1, 1, 1],
              _marker_=['g-', 'r-', 'b-']):
    """
    Function to load the matplotlib plots.

    Keyword Arguments:
    axis     -- the matplotlib axis object.
    plot     -- the matplotlib plot object.
    x        -- the x values to plot.
    y1       -- the first data set y values to plot.
    y2       -- the second data set y values to plot.
    y3       -- the third data set y values to plot.
    _title_  -- the title for the plot.
    _xlab_   -- the x asis label for the plot.
    _ylab_   -- the y axis label for the plot.
    _type_   -- the type of line to plot (1=step, 2=plot, 3=histogram).
    _marker_ -- the marker to use on the plot.
    """

    n_points = len(x)

    axis.cla()

    axis.grid(True, which='both')

    if(y1 is not None):
        if(_type_[0] == 1):
            line, = axis.step(x, y1, _marker_[0], where='mid')
            for i in range(n_points):
                line.set_ydata(y1)
        elif(_type_[0] == 2):
            line, = axis.plot(x, y1, _marker_[0], linewidth=2)
            for i in range(n_points):
                line.set_ydata(y1)
        elif(_type_[0] == 3):
            axis.grid(False, which='both')
            n, bins, patches = axis.hist(x, bins=y1, color=_marker_[0])
    if(y2 is not None):
        if(_type_[1] == 1):
            line2, = axis.step(x, y2, _marker_[1], where='mid')
            for i in range(n_points):
                line2.set_ydata(y2)
        elif(_type_[1] == 2):
            line2, = axis.plot(x, y2, _marker_[1], linewidth=2)
            for i in range(n_points):
                line2.set_ydata(y2)
        elif(_type_[1] == 3):
            axis.grid(False, which='both')
            n, bins, patches = axis.hist(x, bins=y2, color=_marker_[1])
            line2, = axis.plot(bins, y2)

    if(y3 is not None):
        if(_type_[2] == 1):
            line3, = axis.step(x, y3, _marker_[2], where='mid')
            for i in range(n_points):
                line3.set_ydata(y3)
        elif(_type_[2] == 2):
            line3, = axis.plot(x, y3, _marker_[2], linewidth=2)
            for i in range(n_points):
                line3.set_ydata(y3)
        elif(_type_[2] == 3):
            axis.grid(False, which='both')
            n, bins, patches = axis.hist(x, bins=y3, color=_marker_[2])
            line3, = axis.plot(bins, y3)
        elif(_type_[0] == 4):
            line3, = axis.scatter(x, y1, _marker_[2])

    axis.set_title(_title_)
    axis.set_xlabel(_xlab_)
    axis.set_ylabel(_ylab_)

    plot.draw()

    return False
