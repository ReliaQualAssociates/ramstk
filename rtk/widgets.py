#!/usr/bin/env python
"""
This module contains functions for creating, populating, destroying, and
interacting with pyGTK widgets.  Import this module as _widg in other modules
that create, populate, destroy, or interact with pyGTK widgets in the RTK
application.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       widgets.py is part of The RTK Project
#
# All rights reserved.

import gettext
import sys

import pango

# Import other RTK modules.
import Configuration as _conf

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gtk.glade  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

_ = gettext.gettext


class CellRendererML(gtk.CellRendererText):
    """
    Class to create a multi-line cell renderer.  It is based on the base class
    gtk.CellRendererText().
    """

    def __init__(self):

        gtk.CellRendererText.__init__(self)

        self.textedit_window = None
        self.selection = None
        self.treestore = None
        self.treeiter = None

        self.textedit = gtk.TextView()
        self.textbuffer = self.textedit.get_buffer()

    def do_get_size(self, widget, cell_area):
        """
        Method to get the size of the CellRendererML.
        """

        size_tuple = gtk.CellRendererText.do_get_size(self, widget, cell_area)

        return size_tuple

    def do_start_editing(self, __event, treeview, path, __background_area,
                         cell_area, __flags):
        """


        :param __event:
        :param treeview:
        :param path:
        :param __background_area:
        :param cell_area:
        :param __flags:
        """

        if not self.get_property('editable'):
            return

        self.selection = treeview.get_selection()
        self.treestore, self.treeiter = self.selection.get_selected()

        self.textedit_window = gtk.Dialog(parent=treeview.get_toplevel())
        self.textedit_window.action_area.hide()
        self.textedit_window.set_decorated(False)
        self.textedit_window.set_property('skip-taskbar-hint', True)
        self.textedit_window.set_transient_for(None)

        self.textedit.set_editable(True)
        self.textedit.set_property('visible', True)
        self.textbuffer.set_property('text', self.get_property('text'))

        self.textedit_window.connect('key-press-event', self._keyhandler)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_property('visible', True)
        # self.textedit_window.vbox.pack_start(scrolled_window)

        scrolled_window.add(self.textedit)
        self.textedit_window.vbox.add(scrolled_window)
        self.textedit_window.realize()

        # Position the popup below the edited cell (and try hard to keep the
        # popup within the toplevel window)

        (tree_x, tree_y) = treeview.get_bin_window().get_origin()
        (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
        (t_w, t_h) = self.textedit_window.window.get_geometry()[2:4]
        x = tree_x + min(cell_area.x,
                         tree_w - t_w + treeview.get_visible_rect().x)
        y = tree_y + min(cell_area.y,
                         tree_h - t_h + treeview.get_visible_rect().y)
        self.textedit_window.move(x, y)
        self.textedit_window.resize(cell_area.width, cell_area.height)

        # Run the dialog, get response by tracking keypresses
        response = self.textedit_window.run()

        if response == gtk.RESPONSE_OK:
            self.textedit_window.destroy()

            (iter_first, iter_last) = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(iter_first, iter_last)

            # self.treestore[path][2] = text

            treeview.set_cursor(path, None, False)

            self.emit('edited', path, text)

        elif response == gtk.RESPONSE_CANCEL:
            self.textedit_window.destroy()
        else:
            print "response %i received" % response
            self.textedit_window.destroy()

    def _keyhandler(self, __widget, event):
        """


        :param __widget:
        :param event:
        """

        _keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK) and \
                _keyname == 'Return':
            self.textedit_window.response(gtk.RESPONSE_OK)

# Register the new widget types.
gobject.type_register(CellRendererML)


def make_button(height=40, width=200, label="", image='default'):
    """
    Utility function to create gtk.Button() widgets.

    :keyword int height: the height of the gtk.Button().  Default is 40.
    :keyword int  width: the width of the gtk.Button().  Default is 200.
    :keyword str label: the text to display on the gtk.Button().  Default is an
                        empty string.
    :keyword str image: the image to display on the gtk.Button().  Options for
                        this argument are:
                        - add
                        - assign
                        - calculate
                        - commit
                        - default (default)
    :return: _button
    :rtype: gtk.Button
    """

    if width == 0:
        _width = int((int(_conf.PLACES) + 5) * 8)

    _button = gtk.Button(label=label)

    if image is not None:
        if width >= 32:
            _file_image = _conf.ICON_DIR + '32x32/' + image + '.png'
        else:
            _file_image = _conf.ICON_DIR + '16x16/' + image + '.png'
        _image = gtk.Image()
        _image.set_from_file(_file_image)
        _button.set_image(_image)

    _button.props.width_request = width
    _button.props.height_request = height

    return _button


def make_check_button(label="", width=-1):
    """
    Utility function to create gtk.CheckButton() widgets.

    :keyword str label: the text to display with the gtk.CheckButton().
                        Default is an empty string.
    :keyword int width: the desired width of the gtk.CheckButton().  Default
                        is -1 or a natural request.
    :return: _checkbutton
    :rtype: gtk.CheckButton
    """

    _checkbutton = gtk.CheckButton(label, True)

    _checkbutton.get_child().set_use_markup(True)
    _checkbutton.get_child().set_line_wrap(True)
    _checkbutton.get_child().props.width_request = width

    return _checkbutton


def make_option_button(btngroup=None, btnlabel=_(u"")):
    """
    Utility function to create gtk.RadioButton() widgets.

    :keyword str btngroup: the group the gtk.RadioButton() belongs to, if any.
                           Default is None.
    :keyword str btnlabel: the text to place in the label on the
                           gtk.RadioButton().  Default is an empty string.
    :return: _optbutton
    :rtype: gtk.RadioButton
    """

    _optbutton = gtk.RadioButton(group=btngroup, label=btnlabel)

    return _optbutton


def make_combo(width=200, height=30, simple=True):
    """
    Utility function to create gtk.ComboBox widgets.

    :keyword int width: width of the gtk.ComboBox() widget.  Default is 200.
    :keyword int height: height of the gtk.ComboBox widget.  Default is 30.
    :keyword bool simple: boolean indicating whether to create a simple text
                          gtk.ComboBox().  Defaults is True.
    :return: _combo
    :rtype: gtk.ComboBox
    """

    if simple:
        _list = gtk.ListStore(gobject.TYPE_STRING)
        _combo = gtk.ComboBox(_list)
        _cell = gtk.CellRendererText()
        _combo.pack_start(_cell, True)
        _combo.set_attributes(_cell, text=0)
    else:
        _list = gtk.TreeStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING)
        _combo = gtk.ComboBox(_list)
        _cell = gtk.CellRendererText()
        _combo.pack_start(_cell, True)
        _combo.set_attributes(_cell, text=0)

    _combo.props.width_request = width
    _combo.props.height_request = height

    return _combo


def load_combo(combo, entries, simple=True, index=0):
    """
    Utility function to load gtk.ComboBox widgets.

    :param gtk.ComboBox combo: the gtk.ComboBox() to load.
    :param list entries: the information to load into the gtk.ComboBox().
    :keyword boolean simple: indicates whether the load is simple (single
                             column) or complex (multiple columns).  For
                             complex gtk.ComboBox(), the displayed value will
                             be in column 0.
    :keyword int index: the index in the list to display.  Only used when doing
                        a simple load.  Default is 0.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _model = combo.get_model()
    _model.clear()

    if simple:
        combo.append_text("")
        for i in range(len(entries)):
            combo.append_text(entries[i][index])
    else:
        _model.append(None, ["", "", ""])
        for i in range(len(entries)):
            _model.append(None, entries[i])

    return False


def make_dialog(dlgtitle, dlgparent=None,
                dlgflags=(gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT),
                dlgbuttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)):
    """
    Utility function to create gtk.Dialog() widgets.

    :param str dlgtitle: the title text for the gtk.Dialog().
    :keyword gtk.Window dlgparent: the parent window to associate the
                                   gtk.Dialog() with.
    :keyword tuple dlgflags: the flags that control the operation of the
                             gtk.Dialog().  Defaults to gtk.DIALOG_MODAL and
                             gtk.DIALOG_DESTROY_WITH_PARENT.
    :keyword tuple dlgbuttons: the buttons to display and their response
                               values.  Defaults to:
                               gtk.STOCK_OK <==> gtk.RESPONSE_ACCEPT
                               gtk.STOCK_CANCEL <==> gtk.RESPONSE_REJECT
    :return: _dialog
    :rtype: gtk.Dialog
    """

    _dialog = gtk.Dialog(title=dlgtitle,
                         parent=dlgparent,
                         flags=dlgflags,
                         buttons=dlgbuttons)

    _dialog.set_has_separator(True)

    return _dialog


def make_entry(width=200, height=25, editable=True, bold=False,
               color='#BBDDFF'):
    """
    Utility function to create gtk.Entry() widgets.

    :keyword int width: width of the gtk.Entry() widget.  Default is 200.
    :keyword int height: height of the gtk.Entry() widget.  Default is 25.
    :keyword boolean editable: boolean indicating whether gtk.Entry() should be
                               editable.  Defaults to True.
    :keyword boolean bold: boolean indicating whether text should be bold.
                           Defaults to False.
    :keyword str color: the hexidecimal color to set the background when the
                        gtk.Entry() is not editable.  Defaults to #BBDDFF
                        (light blue).
    :return: _entry
    :rtype: gtk.Entry
    """

    _entry = gtk.Entry()
    _entry.props.width_request = width
    _entry.props.height_request = height
    _entry.props.editable = editable

    if bold:
        _entry.modify_font(pango.FontDescription('bold'))

    if not editable:
        _bg_color = gtk.gdk.Color(color)
        _entry.modify_base(gtk.STATE_NORMAL, _bg_color)
        _entry.modify_base(gtk.STATE_ACTIVE, _bg_color)
        _entry.modify_base(gtk.STATE_PRELIGHT, _bg_color)
        _entry.modify_base(gtk.STATE_SELECTED, _bg_color)
        _entry.modify_base(gtk.STATE_INSENSITIVE, _bg_color)
        _entry.modify_font(pango.FontDescription('bold'))

    _entry.show()

    return _entry


def make_label(text, width=190, height=25, bold=True, wrap=False,
               justify=gtk.JUSTIFY_LEFT):
    """
    Utility function to create gtk.Label() widgets.

    :param str text: the text to display in the gtk.Label() widget.
    :param int width: width of the gtk.Label() widget.  Default is 190.
    :param int height: height of the gtk.Label() widget.  Default is 25.
    :param bool bold: boolean indicating whether text should be bold.  Default
                      is True.
    :param bool wrap: boolean indicating whether the label text should wrap or
                      not.
    :param justify: the justification type when the label wraps and contains
                    more than one line.  Default is gtk.JUSTIFY_LEFT.
    :type justify: GTK Justification Constant
    :return: _label
    :rtype: gtk.Label
    """

    _label = gtk.Label()
    _label.set_markup("<span>" + text + "</span>")
    _label.set_line_wrap(wrap)
    _label.set_justify(justify)
    if justify == gtk.JUSTIFY_CENTER:
        _label.set_alignment(xalign=0.5, yalign=0.5)
    elif justify == gtk.JUSTIFY_LEFT:
        _label.set_alignment(xalign=0.05, yalign=0.5)
    else:
        _label.set_alignment(xalign=0.95, yalign=0.5)
    _label.props.width_request = width
    _label.props.height_request = height

    if not bold:
        _label.modify_font(pango.FontDescription('normal'))
    else:
        _label.modify_font(pango.FontDescription('bold'))

    _label.show()

    return _label


def make_labels(text, container, x_pos, y_pos, y_inc=25, wrap=True):
    """
    Utility function to make and place a group of labels.  The width of each
    label is set using a natural request.  This ensures the label doesn't cut
    off letters.  The maximum size of the labels is determined and used to set
    the left position of widget displaying the data described by the label.
    This ensures everything lines up.  It also returns a list of y-coordinates
    indicating the placement of each label that is used to place the
    corresponding widget.

    :param list text: a list containing the text for each label.
    :param gtk.Widget container: the container widget to place the labels in.
    :param int x_pos: the x position in the container for the left edge of all
                      labels.
    :param int y_pos: the y position in the container of the first label.
    :keyword int y_inc: the amount to increment the y_pos between each label.
    :keyword boolean wrap: boolean indicating whether the label text should
                           wrap or not.
    :return: (_int_max_x, _lst_y_pos)
             the width of the label with the longest text and a list of the y
             position for each label in the container.  Use this list to place
             gtk.Entry(), gtk.ComboBox(), etc. so they line up with their
             associated label.
    :rtype: tuple of (integer, list of integers)
    """

    _int_max_x_ = 0
    _lst_y_pos_ = []
    for i in range(len(text)):
        _label = make_label(text[i], width=-1, height=-1, wrap=wrap)
        _int_max_x_ = max(_int_max_x_, _label.size_request()[0])
        container.put(_label, x_pos, y_pos)
        _lst_y_pos_.append(y_pos)
        y_pos += max(_label.size_request()[1], y_inc) + 5

    return(_int_max_x_, _lst_y_pos_)


def make_text_view(txvbuffer=None, width=200, height=100):
    """
    Utility function to create gtk.TextView() widgets encapsulated
    within a gtkScrolledWindow() widget.

    :keyword gtk.TextBuffer txvbuffer: the gtk.TextBuffer() to associate with
                            the gtk.TextView().  Default is None.
    :keyword int width: width of the gtk.TextView() widget.  Default is 200.
    :keyword int height: height of the gtk.TextView() widget.  Default is 100.
    :return: _scrollwindow
    :rtype: gtk.ScrolledWindow
    """

    _view = gtk.TextView(buffer=txvbuffer)
    _view.set_wrap_mode(gtk.WRAP_WORD)

    _scrollwindow = gtk.ScrolledWindow()
    _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    _scrollwindow.props.width_request = width
    _scrollwindow.props.height_request = height
    _scrollwindow.add_with_viewport(_view)

    return _scrollwindow


def make_frame(label=_(u"")):
    """
    Utility function to create gtk.Frame() widgets.

    :keyword str label: the text to display in the gtk.Frame() label.  Default
                        is an empty string.
    :return: _frame
    :rtype: gtk.Frame
    """

    _label = gtk.Label()
    _label.set_markup("<span weight='bold'>" + label + "</span>")
    _label.set_justify(gtk.JUSTIFY_LEFT)
    _label.set_alignment(xalign=0.5, yalign=0.5)
    _label.show_all()

    _frame = gtk.Frame()
    _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
    _frame.set_label_widget(_label)

    return _frame


def make_fixed():
    """
    Utility function to create gtk.Fixed() containers.

    :return: _fixed
    :rtype: gtk.Fixed
    """

    _fixed = gtk.Fixed()

    return _fixed


def make_treeview(name, fmt_idx, app, cmblist=[''], bg_col='white',
                  fg_col='black'):
    """
    Utility function to create gtk.TreeView() widgets.

    :param str name: the name of the gtk.TreeView() to read formatting
                     information for.
    :param int fmt_idx: the index of the format file to use when creating the
                        gtk.TreeView().
    :param RTK app: the RTK application.
    :keyword list cmblist: the list of items to load into the
                           gtk.CellRendererCombo().
    :keyword str bg_col: the background color to use for each row.  Defaults to
                         white.
    :keyword str fg_col: the foreground (text) color to use for each row.
                         Defaults to black.
    :return: the gtk.TreeView() created by this method and the order of the
             gtk.TreeView() columns.
    :rtype: gtk.TreeView, list
    """

    from lxml import etree

    # Retrieve the column heading text from the format file.
    path = "/root/tree[@name='%s']/column/usertitle" % name
    heading = etree.parse(_conf.RTK_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve the column datatype from the format file.
    path = "/root/tree[@name='%s']/column/datatype" % name
    datatype = etree.parse(_conf.RTK_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve the column position from the format file.
    path = "/root/tree[@name='%s']/column/position" % name
    position = etree.parse(_conf.RTK_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve the cell renderer type from the format file.
    path = "/root/tree[@name='%s']/column/widget" % name
    widget = etree.parse(_conf.RTK_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve whether or not the column is editable from the format file.
    path = "/root/tree[@name='%s']/column/editable" % name
    editable = etree.parse(_conf.RTK_FORMAT_FILE[fmt_idx]).xpath(path)

    # Retrieve whether or not the column is visible from the format file.
    path = "/root/tree[@name='%s']/column/visible" % name
    visible = etree.parse(_conf.RTK_FORMAT_FILE[fmt_idx]).xpath(path)

    # Create a list of GObject datatypes to pass to the model.
    types = []
    for i in range(len(position)):
        types.append(datatype[i].text)

    gobject_types = [gobject.type_from_name(types[ix])
                     for ix in range(len(types))]

# If this is the Hardware, Software, or Testing tree, add a column for a pixbuf.
# If this is the FMECA tree, add an integer column and a column for a pixbuf.
    if fmt_idx in [3, 11, 15]:
        gobject_types.append(gtk.gdk.Pixbuf)
    elif fmt_idx in [9, 18]:
        gobject_types.append(gobject.TYPE_INT)
        gobject_types.append(gobject.TYPE_STRING)
        gobject_types.append(gobject.TYPE_BOOLEAN)
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

        if widget[i].text == 'combo':
            cell = gtk.CellRendererCombo()
            cellmodel = gtk.ListStore(gobject.TYPE_STRING)
            cellmodel.append([""])
            cell.set_property('background', bg_col)
            cell.set_property('editable', int(editable[i].text))
            cell.set_property('foreground', fg_col)
            cell.set_property('has-entry', False)
            cell.set_property('model', cellmodel)
            cell.set_property('text-column', 0)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', edit_tree, int(position[i].text), model)
        elif widget[i].text == 'spin':
            cell = gtk.CellRendererSpin()
            adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
            cell.set_property('adjustment', adjustment)
            cell.set_property('background', bg_col)
            cell.set_property('digits', 2)
            cell.set_property('editable', int(editable[i].text))
            cell.set_property('foreground', fg_col)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', edit_tree, int(position[i].text), model)
        elif widget[i].text == 'toggle':
            cell = gtk.CellRendererToggle()
            cell.set_property('activatable', int(editable[i].text))
            cell.connect('toggled', cell_toggled, int(position[i].text), model)
        elif widget[i].text == 'blob':
            cell = CellRendererML()
            cell.set_property('background', bg_col)
            cell.set_property('editable', int(editable[i].text))
            cell.set_property('foreground', fg_col)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', edit_tree, int(position[i].text), model)
        else:
            cell = gtk.CellRendererText()
            cell.set_property('background', bg_col)
            cell.set_property('editable', int(editable[i].text))
            cell.set_property('foreground', fg_col)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', edit_tree, int(position[i].text), model)

        if int(editable[i].text) == 0 and widget[i].text != 'toggle':
            cell.set_property('background', 'light gray')

        column = gtk.TreeViewColumn("")

# If this is the Hardware, Software, FMECA, or Testing tree, add a column for a pixbuf.
# If this is the FMECA tree, add a column for an integer and a pixbuf
        if i == 1 and fmt_idx == 3:
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols)
        elif i == 0 and fmt_idx == 9:
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols + 3)
        elif i == 1 and fmt_idx == 11:
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols)
        elif i == 1 and fmt_idx == 15:
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols)
        else:
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            if widget[i].text == 'toggle':
                column.set_attributes(cell, active=int(position[i].text))
            else:
                column.set_attributes(cell, text=int(position[i].text))

        label = gtk.Label(column.get_title())
        label.set_line_wrap(True)
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        _text = heading[i].text.replace("  ", "\n")
        label.set_markup("<span weight='bold'>" + _text + "</span>")
        label.set_use_markup(True)
        label.show_all()
        column.set_widget(label)
        column.set_cell_data_func(cell, format_cell,
                                  (int(position[i].text), datatype[i].text))
        column.set_resizable(True)
        column.set_alignment(0.5)
        column.connect('notify::width', resize_wrap, cell)

        if i > 0:
            column.set_reorderable(True)

        treeview.append_column(column)

    if fmt_idx == 9:
        column = gtk.TreeViewColumn("")
        column.set_visible(0)
        cell = gtk.CellRendererText()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=cols)
        treeview.append_column(column)

    return(treeview, order)


def format_cell(__column, cell, model, row, data):
    """
    Function to set the formatting of the gtk.Treeview() gtk.CellRenderers().

    :param gtk.TreeViewColumn __column: the gtk.TreeViewColumn() containing the
                                        gtk.CellRenderer() to format.
    :param gtk.CellRenderer cell: the gtk.CellRenderer() to format.
    :param gtk.TreeModel model: the gtk.TreeModel() containing the
                                gtk.TreeViewColumn().
    :param gtk.TreeIter row: the gtk.TreeIter() pointing to the row containing
                             the gtk.CellRenderer() to format.
    :param tuple data: a tuple containing the position and the data type.
    """

    if data[1] == 'gfloat':
        fmt = '{0:0.' + str(_conf.PLACES) + 'f}'
    elif data[1] == 'gint':
        fmt = '{0:0.0f}'
    else:
        return

    val = model.get_value(row, data[0])
    try:
        cell.set_property('text', fmt.format(val))
    except TypeError:                       # It's a gtk.CellRendererToggle
        pass

    return


def edit_tree(cell, path, new_text, position, model):
    """
    Called whenever a gtk.TreeView() gtk.CellRenderer() is edited.

    :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
    :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                     edited.
    :param str new_text: the new text in the edited gtk.CellRenderer().
    :param int position: the column position of the edited gtk.CellRenderer().
    :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                belongs to.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _convert = gobject.type_name(model.get_column_type(position))

    if new_text is None:
        model[path][position] = not cell.get_active()
    elif _convert == 'gchararray':
        model[path][position] = str(new_text)
    elif _convert == 'gint':
        model[path][position] = int(new_text)
    elif _convert == 'gfloat':
        model[path][position] = float(new_text)

    return False


def cell_toggled(cell, path, position, model):
    """
    Called whenever a gtk.TreeView() gtk.CellRendererToggle() is edited.

    :param gtk.CellRendererToggle cell: the gtk.CellRendererToggle() that was
                                        edited.
    :param str path: the gtk.TreeView() path of the gtk.CellRendererToggle()
                     that was edited.
    :param int position: the column position of the edited
                         gtk.CellRendererToggle().
    :param gtk.TreeModel model: the gtk.TreeModel() the
                                gtk.CellRendererToggle() belongs to.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    model[path][position] = not cell.get_active()

    return False


def resize_wrap(column, __param, cell):
    """
    This function dynamically sets the wrap-width property for a
    gtk.CellRenderer() in the gtk.TreeView() when the column width is resized.

    :param gtk.TreeViewColumn column: the gtk.TreeViewColumn() being resized.
    :param GParamInt __param: the triggering parameter.
    :param gtk.CellRenderer cell: the gtk.CellRenderer() that needs to be
                                  resized.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _width = column.get_width()

    if _width <= 0:
        return
    else:
        _width += 10

    try:
        cell.set_property('wrap-width', _width)
    except TypeError:                       # This is a gtk.CellRendererToggle
        cell.set_property('width', _width)

    return False


def make_column_heading(heading=""):
    """
    This function creates labels to use for gtk.TreeView() column headings.

    :keyword str heading: the text to use for the heading.
    :return: _label
    :rtype: gtk.Label
    """

    _heading = "<span weight='bold'>%s</span>" % unicode(heading)

    _label = gtk.Label()
    _label.set_markup(_heading)
    _label.set_alignment(xalign=0.5, yalign=0.5)
    _label.set_justify(gtk.JUSTIFY_CENTER)
    _label.set_line_wrap(True)
    _label.show_all()

    return _label


def load_plot(axis, plot, x, y1=None, y2=None, y3=None, y4=None,
              _title="", _xlab="", _ylab="", _type=[1, 1, 1, 1],
              _marker=['g-', 'r-', 'b-', 'k--']):
    """
    Function to load the matplotlib plots.

    :param matplotlib.Axis axis: the matplotlib axis object.
    :param matplotlib.FigureCanvas plot: the matplotlib plot object.
    :param list x: list of the x values to plot.
    :keyword float y1: list of the first data set y values to plot.
    :keyword float y2: list of the second data set y values to plot.
    :keyword float y3: list of the third data set y values to plot.
    :keyword float y4: list of the fourth data set y values to plot.
    :keyword str title: the title for the plot.
    :keyword str xlab: the x axis label for the plot.
    :keyword str ylab: the y axis label for the plot.
    :keyword int type: list of the type of line to plot. Options are:
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

    n_points = len(x)

    axis.cla()

    axis.grid(True, which='both')

    _x_min = min(x)
    _x_max = max(x)
    _y_min = 0.0
    _y_max = 1.0
    _lst_min = [0.0]
    _lst_max = []
    if y1 is not None:
        if _type[0] == 1:
            line, = axis.step(x, y1, _marker[0], where='mid')
            line.set_ydata(y1)
            _lst_min.append(min(y1))
            _lst_max.append(max(y1))
        elif _type[0] == 2:
            line, = axis.plot(x, y1, _marker[0], linewidth=2)
            line.set_ydata(y1)
            _lst_min.append(min(y1))
            _lst_max.append(max(y1))
        elif _type[0] == 3:
            axis.grid(False, which='both')
            n, bins, __patches = axis.hist(x, bins=y1, color=_marker[0])
            _x_min = min(bins)
            _x_max = max(bins)
            _lst_min.append(min(n))
            _lst_max.append(max(n) + 1)
        elif _type[0] == 4:
            line, = axis.plot_date(x, y1, _marker[0],
                                   xdate=True, linewidth=2)
            _lst_min.append(min(y1))
            _lst_max.append(max(y1))
        _y_min = min(y1)
        _y_max = max(y1)

    if y2 is not None:
        if _type[1] == 1:
            line2, = axis.step(x, y2, _marker[1], where='mid')
            line2.set_ydata(y2)
            _lst_min.append(min(y2))
            _lst_max.append(max(y2))
        elif _type[1] == 2:
            line2, = axis.plot(x, y2, _marker[1], linewidth=2)
            line2.set_ydata(y2)
            _lst_min.append(min(y2))
            _lst_max.append(max(y2))
        elif _type[1] == 3:
            axis.grid(False, which='both')
            n, bins, __patches = axis.hist(x, bins=len(y2),
                                           color=_marker[1])
            _x_min = min(bins)
            _x_max = max(bins)
            _lst_min.append(min(n))
            _lst_max.append(max(n) + 1)
        elif _type[1] == 4:
            line2, = axis.plot_date(x, y2, _marker[1],
                                    xdate=True, linewidth=2)
            _lst_min.append(min(y2))
            _lst_max.append(max(y2))
        _y_min = min(y2)
        _y_max = max(y2)

    if y3 is not None:
        if _type[2] == 1:
            line3, = axis.step(x, y3, _marker[2], where='mid')
            line3.set_ydata(y3)
            _lst_min.append(min(y3))
            _lst_max.append(max(y3))
        elif _type[2] == 2:
            line3, = axis.plot(x, y3, _marker[2], linewidth=2)
            line3.set_ydata(y3)
            _lst_min.append(min(y3))
            _lst_max.append(max(y3))
        elif _type[2] == 3:
            axis.grid(False, which='both')
            n, bins, __patches = axis.hist(x, bins=len(y3),
                                           color=_marker[2])
            _x_min = min(bins)
            _x_max = max(bins)
            _lst_min.append(min(n))
            _lst_max.append(max(n) + 1)
        elif _type[2] == 4:
            line3, = axis.plot_date(x, y3, _marker[2],
                                    xdate=True, linewidth=2)
            _lst_min.append(min(y3))
            _lst_max.append(max(y3))
        _y_min = min(y3)
        _y_max = max(y3)

    if y4 is not None:
        if _type[3] == 1:
            line4, = axis.step(x, y4, _marker[3], where='mid')
            line4.set_ydata(y4)
            _lst_min.append(min(y4))
            _lst_max.append(max(y4))
        elif _type[3] == 2:
            line4, = axis.plot(x, y4, _marker[3], linewidth=2)
            line4.set_ydata(y4)
            _lst_min.append(min(y4))
            _lst_max.append(max(y4))
        elif _type[3] == 3:
            axis.grid(False, which='both')
            n, bins, __patches = axis.hist(x, bins=len(y4),
                                           color=_marker[3])
            _x_min = min(bins)
            _x_max = max(bins)
            _lst_min.append(min(n))
            _lst_max.append(max(n) + 1)
        elif _type[3] == 4:
            line4, = axis.plot_date(x, y4, _marker[3],
                                    xdate=True, linewidth=2)
            _lst_min.append(min(y4))
            _lst_max.append(max(y4))
        _y_min = min(y4)
        _y_max = max(y4)

    axis.set_title(_title, {'fontsize': 16, 'fontweight': 'bold',
                            'verticalalignment': 'baseline',
                            'horizontalalignment': 'center'})

    # Set the x-axis label.
    _x_pos = (_x_max - _x_min) / 2.0
    _y_pos = _y_min - 0.65
    axis.set_xlabel(_xlab, {'fontsize': 14, 'fontweight': 'bold',
                            'verticalalignment': 'center',
                            'horizontalalignment': 'center',
                            'x': _x_pos, 'y': _y_pos})

    # Set the y-axis label.
    axis.set_ylabel(_ylab, {'fontsize': 14, 'fontweight': 'bold',
                            'verticalalignment': 'center',
                            'horizontalalignment': 'center',
                            'rotation':'vertical'})

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
    Utility function to display a plot in it's own window.

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
    Utility function to close the plot.

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
