# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.TreeView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
TreeView Module
-------------------------------------------------------------------------------

This module contains RTK treeview and associated classes.  These classes are
derived from the applicable pyGTK treeviews, but are provided with RTK specific
property values and methods.  This ensures a consistent look and feel to
widgets in the RTK application.
"""

import defusedxml.lxml as lxml  # pylint: disable=E0401
from sortedcontainers import SortedDict  # pylint: disable=E0401

# Import other RTK Widget classes.
from .Widget import gobject, gtk, pango  # pylint: disable=E0401
from .Label import RTKLabel  # pylint: disable=E0401


class RTKTreeView(gtk.TreeView):
    """
    This is the RTKTreeView class.
    """

    # pylint: disable=R0913, R0914
    def __init__(self,
                 fmt_path,
                 fmt_idx,
                 fmt_file,
                 bg_col='white',
                 fg_col='black',
                 pixbuf=False,
                 indexed=False):
        """
        Initialize an RTK TreeView widget.

        :param str fmt_path: the base XML path in the format file to read.
        :param int fmt_idx: the index of the format file to use when creating
                            the gtk.TreeView().
        :keyword str bg_col: the background color to use for each row.
                             Defaults to white.
        :keyword str fg_col: the foreground (text) color to use for each row.
                             Defaults to black.
        :keyword bool pixbuf: indicates whether or not to append a PixBuf
                              column to the gtk.TreeModel().
        """
        gtk.TreeView.__init__(self)

        # Initialize private dictionary instance attributes:

        # Initialize private list instance attributes:

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.
        self.order = []
        self.korder = []

        # Initialize public scalar instance attributes.

        # Retrieve the column heading text from the format file.
        _headings = lxml.parse(fmt_file).xpath(fmt_path + "/usertitle")

        # Retrieve the column datatype from the format file.
        _datatypes = lxml.parse(fmt_file).xpath(fmt_path + "/datatype")

        # Retrieve the column position from the format file.
        _position = lxml.parse(fmt_file).xpath(fmt_path + "/position")

        # Retrieve the cell renderer type from the format file.
        _widgets = lxml.parse(fmt_file).xpath(fmt_path + "/widget")

        # Retrieve whether or not the column is editable from the format file.
        _editable = lxml.parse(fmt_file).xpath(fmt_path + "/editable")

        # Retrieve whether or not the column is visible from the format file.
        _visible = lxml.parse(fmt_file).xpath(fmt_path + "/visible")

        _keys = lxml.parse(fmt_file).xpath(fmt_path + "/key")

        # Create a list of GObject datatypes to pass to the model.
        _types = []
        for i in range(len(_datatypes)):  # pylint: disable=C0200
            _datatypes[i] = _datatypes[i].text
            _headings[i] = _headings[i].text.replace("  ", "\n")
            _widgets[i] = _widgets[i].text
            _editable[i] = int(_editable[i].text)
            _position[i] = int(_position[i].text)
            _visible[i] = int(_visible[i].text)
            _types.append(gobject.type_from_name(_datatypes[i]))
            try:
                _keys[i] = _keys[i].text
            except IndexError:
                pass

        # Sort each of the lists according to the desired sequence provided in
        # the _position list.  This is necessary to all for user-specific
        # ordering of columns in the RTKTreeView.
        _datatypes = [x for _, x in sorted(zip(_position, _datatypes))]
        _headings = [x for _, x in sorted(zip(_position, _headings))]
        _widgets = [x for _, x in sorted(zip(_position, _widgets))]
        _editable = [x for _, x in sorted(zip(_position, _editable))]
        _visible = [x for _, x in sorted(zip(_position, _visible))]
        _types = [x for _, x in sorted(zip(_position, _types))]
        self.korder = [x for _, x in sorted(zip(_position, _keys))]

        # Append entries to each list if this RTKTreeView is to display an
        # icon at the beginning of the row (Usage Profile, Hardware, etc.)
        if pixbuf:
            _datatypes.append('pixbuf')
            _headings.append('')
            _types.append(gtk.gdk.Pixbuf)
            _widgets.append('pixbuf')
            _editable.append(0)
            _position.append(len(_position))
            _visible.append(1)
        # FIXME: What is this for?  It'll become obvious later...maybe.
        elif fmt_idx in [15, 16]:
            print fmt_file
            _types.append(gobject.TYPE_INT)
            _types.append(gobject.TYPE_STRING)
            _types.append(gobject.TYPE_BOOLEAN)
            _types.append(gtk.gdk.Pixbuf)

        # We may want to add a column to hold indexing information for program
        # control.
        # FIXME: Are we using this?  If not, we need to eliminate.
        if indexed:
            _datatypes.append('text')
            _headings.append('')
            _types.append(gobject.TYPE_STRING)
            _widgets.append('text')
            _editable.append(0)
            _position.append(len(_position))
            _visible.append(0)

        # Create the model.
        _model = gtk.TreeStore(*_types)

        if pixbuf:
            _n_cols = int(len(_types)) - 2
        else:
            _n_cols = int(len(_types)) - 1

        for i in range(_n_cols):
            self.order.append(_position[i])

            if _widgets[i] == 'combo':
                _cell = self._do_make_combo_cell()
                self._do_set_properties(_cell, bg_col, fg_col, _editable[i])
            elif _widgets[i] == 'spin':
                _cell = self._do_make_spin_cell()
                self._do_set_properties(_cell, bg_col, fg_col, _editable[i])
            elif _widgets[i] == 'toggle':
                _cell = self._do_make_toggle_cell(_editable[i])
                self._do_set_properties(_cell, bg_col, fg_col, _editable[i])
            elif _widgets[i] == 'blob':
                _cell = self._do_make_text_cell(True)
                self._do_set_properties(_cell, bg_col, fg_col, _editable[i])
            else:
                _cell = self._do_make_text_cell()
                self._do_set_properties(_cell, bg_col, fg_col, _editable[i])

            if pixbuf and i == 0:
                _pbcell = gtk.CellRendererPixbuf()
                _pbcell.set_property('xalign', 0.5)
                _column = self._do_make_column([_pbcell, _cell], _visible[i],
                                               _headings[i])
                _column.set_attributes(_pbcell, pixbuf=_n_cols)
            else:
                _column = self._do_make_column([
                    _cell,
                ], _visible[i], _headings[i])
            _column.set_cell_data_func(_cell, self._format_cell,
                                       (_position[i], _datatypes[i]))

            if _widgets[i] == 'toggle':
                _column.set_attributes(_cell, active=_position[i])
            else:
                _column.set_attributes(_cell, text=_position[i])

            if i > 0:
                _column.set_reorderable(True)

            self.append_column(_column)

        # Finally, we want to add a column to hold indexing information for
        # program control.
        _cell = gtk.CellRendererText()
        _column = self._do_make_column([
            _cell,
        ], False, "")
        _column.pack_start(_cell, False)
        _column.set_attributes(_cell, text=_n_cols + 1)
        self.append_column(_column)

        # FIXME: What is this for?  It'll become obvious later...maybe.
        if fmt_idx == 9:
            print fmt_file
            column = gtk.TreeViewColumn("")
            column.set_visible(0)
            cell = gtk.CellRendererText()
            column.pack_start(cell, True)
            column.set_attributes(cell, text=_n_cols)
            self.append_column(column)

        self.set_model(_model)

    def do_load_tree(self, tree, row=None):
        """
        Load the Module View's gtk.TreeModel() with the Module's tree.

        :param tree: the Module's treelib Tree().
        :type tree: :class:`treelib.Tree`
        :param row: the parent row in the gtk.TreeView() to add the new item.
        :type row: :class:`gtk.TreeIter`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _row = None
        _model = self.get_model()

        _node = tree.nodes[SortedDict(tree.nodes).keys()[0]]
        _entity = _node.data

        _attributes = []
        try:
            _temp = _entity.get_attributes()
            for _key in self.korder:
                _attributes.append(_temp[_key])
            try:
                _row = _model.append(row, _attributes)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.rtk.TreeView.RTKTreeView.do_load_tree"
        except AttributeError:
            _row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self.do_load_tree(_child_tree, _row)

        return _return

    def _do_make_column(self, cells, visible, heading):
        """
        Method to make a gtk.TreeViewColumn()

        :param list cells: list of gtk.CellRenderer()s that are to be packed in
                           the column.
        :param int visible: indicates whether the column will be visible.
        :param str heading: the column heading text.
        :return: _column
        :rtype: :class:`gtk.TreeViewColumn`
        """

        _column = gtk.TreeViewColumn("")

        for _cell in cells:
            if isinstance(_cell, gtk.CellRendererPixbuf):
                _column.pack_start(_cell, False)
            else:
                _column.pack_start(_cell, True)
                _column.connect('notify::width', self._resize_wrap, _cell)

        _label = RTKLabel(
            heading, width=-1, height=-1, justify=gtk.JUSTIFY_CENTER)
        _column.set_widget(_label)
        _column.set_resizable(True)
        _column.set_alignment(0.5)
        _column.set_visible(visible)

        return _column

    @staticmethod
    def _do_make_combo_cell():
        """
        Method to make a gtk.CellRendererCombo().

        :return: _cell
        :rtype: :class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        return _cell

    @staticmethod
    def _do_make_spin_cell():
        """
        Method to make a gtk.CellRendererCombo().

        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        :param int position: the position in the gtk.TreeModel() that this
                             cell falls.
        :param model: the gtk.TreeModel() the cell belongs to.
        :type model: :class:`gtk.TreeModel`
        :return: _cell
        :rtype: :class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererSpin()
        _adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
        _cell.set_property('adjustment', _adjustment)
        _cell.set_property('digits', 2)

        return _cell

    @staticmethod
    def _do_make_text_cell(blob=False):
        """
        Method to make a gtk.CellRendererCombo().

        :param bool blob: indicates whether the cell will be displaying a BLOB
                          field.
        :type model: :class:`gtk.TreeModel`
        :return: _cell
        :rtype: :class:`gtk.CellRendererCombo`
        """

        if not blob:
            _cell = gtk.CellRendererText()
        else:
            _cell = CellRendererML()

        return _cell

    @staticmethod
    def _do_make_toggle_cell(editable):
        """
        Make a gtk.CellRendererCombo().

        :param int editable: indicates whether the cell is editable.
        :return: _cell
        :rtype: :class:`gtk.CellRendererCombo`
        """

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', editable)

        return _cell

    @staticmethod
    def _do_set_properties(cell, bg_color, fg_color, editable):
        """
        Set common properties of gtk.CellRenderers().

        :param cell: the cell whose properties are to be set.
        :type cell: :class:`gtk.CellRenderer`
        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        """

        if editable == 0:
            cell.set_property('cell-background', 'light gray')
        else:
            cell.set_property('cell-background', bg_color)

        if not isinstance(cell, gtk.CellRendererToggle):
            cell.set_property('editable', editable)
            cell.set_property('foreground', fg_color)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        else:
            cell.set_property('activatable', editable)

        cell.set_property('yalign', 0.1)

    @staticmethod
    def do_edit_cell(cell, path, new_text, position, model):
        """
        Method called when a gtk.TreeView() gtk.CellRenderer() is edited.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _convert = gobject.type_name(model.get_column_type(position))

        if isinstance(cell, gtk.CellRendererToggle):
            model[path][position] = not cell.get_active()
        elif _convert == 'gchararray':
            model[path][position] = str(new_text)
        elif _convert == 'gint':
            try:
                model[path][position] = int(new_text)
            except ValueError:
                model[path][position] = int(float(new_text))
        elif _convert == 'gfloat':
            model[path][position] = float(new_text)

        return _return

    @staticmethod
    def _format_cell(__column, cell, model, row, data):
        """
        Method to set the formatting of the gtk.Treeview() gtk.CellRenderers().

        :param __column: the gtk.TreeViewColumn() containing the
                         gtk.CellRenderer() to format.
        :type __column: :class:`gtk.TreeViewColumn`
        :param cell: the gtk.CellRenderer() to format.
        :type cell: :class:`gtk.CellRenderer`
        :param model: the gtk.TreeModel() containing the gtk.TreeViewColumn().
        :type model: :class:`gtk.TreeModel`
        :param row: the gtk.TreeIter() pointing to the row containing the
                    gtk.CellRenderer() to format.
        :type row: :class:`gtk.TreeIter`
        :param tuple data: a tuple containing the position and the data type.
        """

        if data[1] == 'gfloat':
            # fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'
            fmt = '{0:0.6g}'
        elif data[1] == 'gint':
            fmt = '{0:0d}'
        else:
            return

        val = model.get_value(row, data[0])
        try:
            cell.set_property('text', fmt.format(val))
        except TypeError:  # It's a gtk.CellRendererToggle
            pass
        except ValueError:
            pass

        return

    @staticmethod
    def _resize_wrap(column, __param, cell):
        """
        Method to dynamically set the wrap-width property for a
        gtk.CellRenderer() in the gtk.TreeView() when the column width is
        resized.

        :param column: the gtk.TreeViewColumn() being resized.
        :type column: :class:`gtk.TreeViewColumn`
        :param GParamInt __param: the triggering parameter.
        :param cell: the gtk.CellRenderer() that needs to be resized.
        :type cell: :class:`gtk.CellRenderer`
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
        except TypeError:  # This is a gtk.CellRendererToggle
            cell.set_property('width', _width)

        return False


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
        x_pos = tree_x + min(cell_area.x,
                             tree_w - t_w + treeview.get_visible_rect().x)
        y_pos = tree_y + min(cell_area.y,
                             tree_h - t_h + treeview.get_visible_rect().y)
        self.textedit_window.move(x_pos, y_pos)
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
gobject.type_register(RTKTreeView)
gobject.type_register(CellRendererML)
