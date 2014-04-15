#!/usr/bin/env python
""" widgets contains functions for creating, populating, destroying, and
    interacting with pyGTK widgets.  Import this module as _widg in other
    modules that create, populate, destroy, or interact with pyGTK widgets in
    the RTK application.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       widgets.py is part of The RTK Project
#
# All rights reserved.

import gettext
import sys

import pango

# Import other RTK modules.
import configuration as _conf

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

    def __init__(self):
        gtk.CellRendererText.__init__(self)

    def do_get_size(self, widget, cell_area):
        size_tuple = gtk.CellRendererText.do_get_size(self, widget, cell_area)

        return(size_tuple)

    def do_start_editing(self, event, treeview, path, background_area,
                         cell_area, flags):

        if not self.get_property('editable'):
            return

        self.selection = treeview.get_selection()
        self.treestore, self.treeiter = self.selection.get_selected()

        self.textedit_window = gtk.Dialog(parent=treeview.get_toplevel())

        self.textedit_window.action_area.hide()
        self.textedit_window.set_decorated(False)
        self.textedit_window.set_property('skip-taskbar-hint', True)
        self.textedit_window.set_transient_for(None)

        self.textedit = gtk.TextView()
        self.textedit.set_editable(True)
        self.textedit.set_property('visible', True)
        self.textbuffer = self.textedit.get_buffer()
        self.textbuffer.set_property('text', self.get_property('text'))

        self.textedit_window.connect('key-press-event', self._keyhandler)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_property('visible', True)
        #self.textedit_window.vbox.pack_start(scrolled_window)

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

    def _keyhandler(self, widget, event):

        keyname = gtk.gdk.keyval_name(event.keyval)

        if event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK) and \
                gtk.gdk.keyval_name(event.keyval) == 'Return':

            self.textedit_window.response(gtk.RESPONSE_OK)


class CellRendererButton(gtk.CellRendererText):

    __gproperties__ = {"callable": (gobject.TYPE_PYOBJECT,
                                    "callable property",
                                    "callable property",
                                    gobject.PARAM_READWRITE)}
    _button_width = 40
    _button_height = 30

    def __init__(self):
        self.__gobject_init__()
        gtk.CellRendererText.__init__(self)
        self.set_property("xalign", 0.5)
        self.set_property("mode", gtk.CELL_RENDERER_MODE_ACTIVATABLE)
        self.callable = None
        self.table = None

    def do_set_property(self, pspec, value):
        if pspec.name == "callable":
            if callable(value):
                self.callable = value
            else:
                raise TypeError("callable property must be callable!")
        else:
                raise AttributeError("Unknown property %s" % pspec.name)

    def do_get_property(self, pspec):
        if pspec.name == "callable":
            return self.callable
        else:
            raise AttributeError("Unknown property %s" % pspec.name)

    def do_get_size(self, wid, cell_area):
        xpad = self.get_property("xpad")
        ypad = self.get_property("ypad")

        if not cell_area:
            x, y = 0, 0
            w = 2 * xpad + self._button_width
            h = 2 * ypad + self._button_height
        else:
            w = 2 * xpad + cell_area.width
            h = 2 * ypad + cell_area.height

            xalign = self.get_property("xalign")
            yalign = self.get_property("yalign")

            x = max(0, xalign * (cell_area.width - w))
            y = max(0, yalign * (cell_area.height - h))

        return(x, y, w, h)

    def do_render(self, window, wid, bg_area, cell_area, expose_area, flags):

        if not window:
            return

        xpad = self.get_property("xpad")
        ypad = self.get_property("ypad")

        x, y, w, h = self.get_size(wid, cell_area)

# if flags & gtk.CELL_RENDERER_SELECTED :
# state = gtk.STATE_ACTIVE
# shadow = gtk.SHADOW_OUT
        if flags & gtk.CELL_RENDERER_PRELIT:
            state = gtk.STATE_PRELIGHT
            shadow = gtk.SHADOW_ETCHED_OUT
        else:
            state = gtk.STATE_NORMAL
            shadow = gtk.SHADOW_OUT

        wid.get_style().paint_box(window, state, shadow, cell_area,
                                  wid, "button", cell_area.x + x + xpad,
                                  cell_area.y + y + ypad,  w - 6, h - 6)
        flags = flags & ~gtk.STATE_SELECTED
        gtk.CellRendererText.do_render(self, window, wid, bg_area,
                                       (cell_area[0], cell_area[1] + ypad,
                                        cell_area[2], cell_area[3]),
                                       expose_area, flags)

    def do_activate(self, event, wid, path, bg_area, cell_area, flags):
        cb = self.get_property("callable")
        if cb is not None:
            cb(path)
        return True

gobject.type_register(CellRendererML)           # @UndefinedVariable
gobject.type_register(CellRendererButton)       # @UndefinedVariable


def make_button(height=40, width=200, label="", image='default'):
    """
    Utility function to create gtk.Button() widgets.

    :param integer height: the height of the gtk.Button().
    :param integer width: the width of the gtk.Button().
    :param string label: the text to display on the gtk.Button().  Default is
                         an empty string.
    :param image: the image to display on the gtk.Button().  Options for this
                  argument are:

                    - add
                    - assign
                    - calculate
                    - commit
    :rtype: gtk.Button()
    """

    if width == 0:
        width = int((int(_conf.PLACES) + 5) * 8)

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

    return(_button)


def make_check_button(label="", width=-1):
    """
    Utility function to create CheckButton widgets.

    :param string label: the text to display with the gtk.CheckButton().
                         Default is no text.
    :param integer width: the desired width of the gtk.CheckButton().  Default
                          is -1 or natural request.
    """

    _checkbutton = gtk.CheckButton(_label_, True)

    _checkbutton.get_child().set_use_markup(True)
    _checkbutton.get_child().set_line_wrap(True)
    _checkbutton.get_child().props.width_request = width

    return(_checkbutton)


def make_option_button(_group_=None, _label_=_(u"")):

    optbutton = gtk.RadioButton(group=_group_, label=_label_)

    return(optbutton)


def make_combo(_width_=200, _height_=30, simple=True):
    """
    Utility function to create gtk.ComboBox widgets.

    Keyword Arguments:
    _width_  -- width of the gtk.ComboBox widget.  Default is 200.
    _height_ -- height of the gtk.ComboBox widget.  Default is 30.
    _simple_ -- boolean indicating whether to create a simple text
                gtk.ComboBox.  Defaults to True.
    """

    if simple:
        #_combo_ = gtk.combo_box_new_text()
        _list_ = gtk.ListStore(gobject.TYPE_STRING)
        _combo_ = gtk.ComboBox(_list_)
        _cell_ = gtk.CellRendererText()
        _combo_.pack_start(_cell_, True)
        _combo_.set_attributes(_cell_, text=0)
    else:
        _list_ = gtk.TreeStore(gobject.TYPE_STRING,
                               gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        _combo_ = gtk.ComboBox(_list_)
        _cell_ = gtk.CellRendererText()
        _combo_.pack_start(_cell_, True)
        _combo_.set_attributes(_cell_, text=0)

    _combo_.props.width_request = _width_
    _combo_.props.height_request = _height_

    return(_combo_)


def load_combo(combo, _list_, simple=True, _index_=0):
    """
    Utility function to load gtk.ComboBox widgets.

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
    Utility function to create gtk.Dialog widgets.

    Keyword Arguments:
    _title_   -- the title text for the gtk.Dialog.
    _parent_  -- the parent window to associate the gtk.Dialog with.  Defaults
                 to None.
    _flags_   -- the flags that control the operation of the gtk.Dialog.
                 Defaults to gtk.DIALOG_MODAL and
                 gtk.DIALOG_DESTROY_WITH_PARENT.
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


def make_entry(width=200, _height_=25,
               editable=True, bold=False,
               _color_='#BBDDFF'):
    """
    Utility function to create gtk.Entry widgets.

    Keyword Arguments:
    width    -- width of the gtk.Entry widget.  Default is 200.
    eight    -- height of the gtk.Entry widget.  Default is 25.
    editable -- boolean indicating whether gtk.Entry should be editable.
                Defaults to True.
    bold     -- boolean indicating whether text should be bold.  Defaults
                to False.
    _color_  -- the hexidecimal color to set the background.  Defaults to
                #FFF (light grey).
    """

    entry = gtk.Entry()
    entry.props.width_request = width
    entry.props.height_request = _height_
    entry.props.editable = editable

    if bold:
        entry.modify_font(pango.FontDescription('bold'))

    if not editable:
        bg_color = gtk.gdk.Color(_color_)  # @UndefinedVariable
        entry.modify_base(gtk.STATE_NORMAL, bg_color)
        entry.modify_base(gtk.STATE_ACTIVE, bg_color)
        entry.modify_base(gtk.STATE_PRELIGHT, bg_color)
        entry.modify_base(gtk.STATE_SELECTED, bg_color)
        entry.modify_base(gtk.STATE_INSENSITIVE, bg_color)
        entry.modify_font(pango.FontDescription('bold'))

    entry.show()

    return(entry)


def make_label(text, width=190, height=25, bold=True, wrap=False,
               justify=gtk.JUSTIFY_LEFT):
    """
    Utility function to create gtk.Label widgets.

    Keyword Arguments:
    text    -- the text to display in the gtk.Label widget.
    width   -- width of the gtk.Label widget.  Default is 190.
    height  -- height of the gtk.Label widget.  Default is 25.
    bold    -- boolean indicating whether text should be bold.  Defaults
               to True.
    wrap    -- boolean indicating whether the label should be multi-line or
               not.
    justify -- the justification type when the label wraps and contains more
               than one line.
    """

    label = gtk.Label()
    label.set_markup("<span>" + text + "</span>")
    label.set_line_wrap(wrap)
    label.set_justify(justify)
    label.set_alignment(xalign=0.05, yalign=0.5)
    label.props.width_request = width
    label.props.height_request = height

    if not bold:
        label.modify_font(pango.FontDescription('normal'))
    else:
        label.modify_font(pango.FontDescription('bold'))

    label.show()

    return(label)


def make_labels(text, container, x_pos, y_pos, y_inc=25):
    """
    Utility function to make and place a group of labels.  The width of each
    label is set using a natural request.  This ensures the label doesn't cut
    off letters.  The maximum size of the labels is determined and used to set
    the left position of widget displaying the data described by the label.
    This ensures everything lines up.  It also returns a list of y-coordinates
    indicating the placement of each label that is used to place the
    corresponding widget.

    Keyword Arguments:
    text      -- a list containing the text for each label.
    container -- the container widget to place the labels on.
    x_pos     -- the x position in the container for the left edge of all
                 labels.
    y_pos     -- the y position in the container of the first label.
    y_inc     -- the amount to increment the y_pos between each label.
    """

    _int_max_x_ = 0
    _lst_y_pos_ = []
    for i in range(len(text)):
        label = make_label(text[i], width=-1, height=-1, wrap=True)
        _int_max_x_ = max(_int_max_x_, label.size_request()[0])
        container.put(label, x_pos, y_pos)
        _lst_y_pos_.append(y_pos)
        y_pos += max(label.size_request()[1], y_inc) + 5

    return(_int_max_x_, _lst_y_pos_)


def make_text_view(buffer_=None, width=200, height=100):
    """
    Utility function to create gtk.TextView widgets.

    Keyword Arguments:
    buffer_ -- the TextBuffer to associate with the gtk.TextView.  Default is
               None.
    width   -- width of the gtk.TextView widget.  Default is 200.
    height  -- height of the gtk.TextView widget.  Default is 100.
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
    Utility function to create gtk.Frame widgets.

    Keyword Arguments:
    _label_ -- the text to display in the gtk.Frame label.
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
    """
    Utility function to create gtk.TreeView widgets.

    Keyword Arguments:
    name    -- the name of the gtk.TreeView to read formatting information for.
    fmt_idx -- the index of the format file to use when creating the
               gtk.TreeView.
    _app    -- the RTK application.
    _list   -- the list of items to load into the gtk.CellRendererCombo.
    bg_col  -- the background color to use for each row.  Defaults to white.
    fg_col  -- the foreground (text) color to use for each row.  Defaults to
               black.
    @rtype : gtk.TreeView()
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
# If this is the FMECA tree, add an integer column and a column for a pixbuf.
    if(fmt_idx == 3):
        gobject_types.append(gtk.gdk.Pixbuf)
    elif(fmt_idx == 9 or fmt_idx == 18):
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

        if(widget[i].text == 'combo'):
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
        elif(widget[i].text == 'spin'):
            cell = gtk.CellRendererSpin()
            adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
            cell.set_property('adjustment', adjustment)
            cell.set_property('background', bg_col)
            cell.set_property('digits', 2)
            cell.set_property('editable', int(editable[i].text))
            cell.set_property('foreground', fg_col)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', edit_tree, int(position[i].text), model)
        elif(widget[i].text == 'toggle'):
            cell = gtk.CellRendererToggle()
            cell.set_property('activatable', int(editable[i].text))
            cell.connect('toggled', cell_toggled, int(position[i].text), model)
        elif(widget[i].text == 'blob'):
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

        if(int(editable[i].text) == 0 and widget[i].text != 'toggle'):
            cell.set_property('background', 'light gray')

        column = gtk.TreeViewColumn("")

# If this is the Hardware tree, add a column for a pixbuf.
# If this is the FMECA tree, add a column for an integer and a pixbuf
        if(i == 1 and fmt_idx == 3):
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols)
        elif(i == 0 and fmt_idx == 9):
            column.set_visible(1)
            cellpb = gtk.CellRendererPixbuf()
            column.pack_start(cellpb, True)
            column.set_attributes(cellpb, pixbuf=cols + 3)
        else:
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)
            if(widget[i].text == 'toggle'):
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

        if(i > 0):
            column.set_reorderable(True)

        treeview.append_column(column)

    if(fmt_idx == 9):
        column = gtk.TreeViewColumn("")
        column.set_visible(0)
        cell = gtk.CellRendererText()
        column.pack_start(cell, True)
        column.set_attributes(cell, text=cols)
        treeview.append_column(column)

    return(treeview, order)


def format_cell(column, cell, model, iter, data_):
    """
    Function to set the formatting of the gtk.Treeview gtk.CellRenderers.

    Keyword Arguments:
    column -- the gtk.TreeViewColumn containing the gtk.CellRenderer to format.
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
    try:
        cell.set_property('text', fmt.format(val))
    except TypeError:                       # It's a gtk.CellRendererToggle
        pass

    return


def edit_tree(cell, path, new_text, position, model):
    """
    Called whenever a TreeView CellRenderer is edited.

    Keyword Arguments:
    cell     -- the CellRenderer that was edited.
    path     -- the TreeView path of the CellRenderer that was edited.
    new_text -- the new text in the edited CellRenderer.
    position -- the column position of the edited CellRenderer.
    model    -- the TreeModel the CellRenderer belongs to.
    """

    _convert_ = gobject.type_name(model.get_column_type(position))

    if new_text is None:
        model[path][position] = not cell.get_active()
    elif _convert_ == 'gchararray':
        model[path][position] = str(new_text)
    elif _convert_ == 'gint':
        model[path][position] = int(new_text)
    elif _convert_ == 'gfloat':
        model[path][position] = float(new_text)

    return False


def cell_toggled(cell, path, position, model):
    """
    Called whenever a TreeView CellRenderer is edited.

    Keyword Arguments:
    cell     -- the CellRenderer that was edited.
    path     -- the TreeView path of the CellRenderer that was edited.
    position -- the column position of the edited CellRenderer.
    model    -- the TreeModel the CellRenderer belongs to.
    """

    model[path][position] = not cell.get_active()

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

    try:
        cell.set_property('wrap-width', width)
    except TypeError:                       # This is a gtk.CellRendererToggle
        cell.set_property('width', width)

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


def load_plot(axis, plot, x, y1=None, y2=None, y3=None, y4=None,
              _title_="", _xlab_="", _ylab_="", _type_=[1, 1, 1, 1],
              _marker_=['g-', 'r-', 'b-', 'k--']):
        """
        Function to load the matplotlib plots.

        Keyword Arguments:
        axis     -- the matplotlib axis object.
        plot     -- the matplotlib plot object.
        x        -- the x values to plot.
        y1       -- the first data set y values to plot.
        y2       -- the second data set y values to plot.
        y3       -- the third data set y values to plot.
        y4       -- the fourth data set y values to plot.
        _title_  -- the title for the plot.
        _xlab_   -- the x asis label for the plot.
        _ylab_   -- the y axis label for the plot.
        _type_   -- the type of line to plot.
                    1 = step
                    2 = plot
                    3 = histogram
                    4 = date plot
        _marker_ -- the marker to use on the plot.
                    g- = green solid line
                    r- = red solid line
                    b- = blue solid line
                    k- = black dashed line
        """

        #import numpy
        #from scipy.interpolate import spline

        n_points = len(x)

        axis.cla()

        axis.grid(True, which='both')

        _lst_min_ = []
        _lst_max_ = []
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
            elif(_type_[0] == 4):
                line, = axis.plot_date(x, y1, _marker_[0],
                                       xdate=True, linewidth=2)
            _lst_min_.append(min(y1))
            _lst_max_.append(max(y1))

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
            elif(_type_[1] == 4):
                line2, = axis.plot_date(x, y2, _marker_[1],
                                        xdate=True, linewidth=2)
            _lst_min_.append(min(y2))
            _lst_max_.append(max(y2))

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
            elif(_type_[2] == 4):
                line3, = axis.plot_date(x, y3, _marker_[2],
                                        xdate=True, linewidth=2)
            _lst_min_.append(min(y3))
            _lst_max_.append(max(y3))

        if(y4 is not None):
            if(_type_[3] == 1):
                line4, = axis.step(x, y4, _marker_[3], where='mid')
                for i in range(n_points):
                    line4.set_ydata(y4)
            elif(_type_[3] == 2):
                line4, = axis.plot(x, y4, _marker_[3], linewidth=2)
                for i in range(n_points):
                    line4.set_ydata(y4)
            elif(_type_[3] == 3):
                axis.grid(False, which='both')
                n, bins, patches = axis.hist(x, bins=y4, color=_marker_[3])
                line4, = axis.plot(bins, y4)
            elif(_type_[3] == 4):
                line4, = axis.plot_date(x, y4, _marker_[3],
                                        xdate=True, linewidth=2)
            _lst_min_.append(min(y4))
            _lst_max_.append(max(y4))

        axis.set_title(_title_)
        axis.set_xlabel(_xlab_)
        axis.set_ylabel(_ylab_)

        _min_ = min(_lst_min_)
        _max_ = max(_lst_max_)
        axis.set_ybound(_min_, _max_)

        plot.draw()

        return False


def create_legend(axis, text, _fontsize_='small', _frameon_=False,
                  _location_='upper right', _ncol_=1, _shadow_=True,
                  _title_="", _lwd_=0.5):
    """
    Function to create legends on matplotlib plots.

    Keyword Arguments:
    axis       -- the axis object to associate the legend with.
    text       -- the text to display in the legend.  This is a tuple of strings.
    _fontsize_ -- the size of the font, in poiunts, to use for the legend.
                  Options are:
                    xx-small
                    x-small
                    small
                    medium
                    large
                    x-large
                    xx-large
    _frameon_  -- whether or not there is a frame around the legend.
    _location_ -- the location of the legend on the plot.  Options are:
                    best or 0
                    upper right or 1
                    upper left or 2
                    lower left or 3
                    lower right or 4
                    right or 5
                    center left or 6
                    center right or 7
                    lower center or 8
                    upper center or 9
                    center or 10
    _ncol_     -- the number columns in the legend.
    _shadow_   -- whether or not to display a shadow behind the legend block.
    _title_    -- the titel of the legend.
    _lwd_      -- the linewidth of the box around the legend.
    """

    leg = axis.legend(text, frameon=_frameon_, loc=_location_, ncol=_ncol_,
                      shadow=_shadow_, title=_title_)

    for t in leg.get_texts():
        t.set_fontsize(_fontsize_)
    for l in leg.get_lines():
        l.set_linewidth(_lwd_)

    return False
