# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.TreeView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTreeView Module."""

import datetime

from sortedcontainers import SortedDict
import defusedxml.lxml as lxml

# Import other RAMSTK Widget classes.
from .Widget import gobject, gtk, pango
from .Label import RAMSTKLabel


class RAMSTKTreeView(gtk.TreeView):
    """The RAMSTKTreeView class."""

    # pylint: disable=R0913, R0914
    # Retain the arguments for backwards compatibility.  Once all current
    # RAMSTKTreeView() instances are updated to use the new API, the arguments
    # can be removed.
    def __init__(self, fmt_path, fmt_idx, fmt_file, bg_col, fg_col, **kwargs):
        r"""
        Initialize a RAMSTKTreeView() instance.

        :param str fmt_path: the absolute path to the format file.
        :param int fmt_idx: the index of the format file (deprecated).
        :param str fmt_file: the name of the format file.
        :param str bg_col: the hex string for the cell background color.
        :param str fg_col: the hex string for the cell foreground color.
        :param \**kwargs: See below

        :Keyword Arguments:
            * *pixbuf* (bool) -- indicates whether there is a pixbuf at the
                                 beginning of each row.
            * *indexed* (bool) -- indicates whether the data to load into the
                                  tree will be indexed.
        """
        gtk.TreeView.__init__(self)

        # Initialize private dictionary instance attributes:

        # Initialize private list instance attributes:

        # Initialize private scalar instance attributes.
        try:
            _pixbuf = kwargs['pixbuf']
        except KeyError:
            _pixbuf = False
        try:
            _indexed = kwargs['indexed']
        except KeyError:
            _indexed = False

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.
        self.datatypes = []
        self.editable = []
        self.headings = []
        self.korder = []
        self.order = []
        self.position = []
        self.widgets = []
        self.visible = []

        # Initialize public scalar instance attributes.
        self.pixbuf_col = None
        self.index_col = None

        # This is required for backwards compatibility.  Once current
        # RAMSTKTreeView() instances are updated to use the new API, this if
        # block can be removed.
        if fmt_file is not None:
            self.do_parse_format(
                fmt_path, fmt_file, pixbuf=_pixbuf, indexed=_indexed)
            self.make_model(bg_col, fg_col)

    def do_parse_format(self, fmt_path, fmt_file, pixbuf=False, indexed=False):
        """
        Parse the format file for the RAMSTKTreeView().

        :param str fmt_path: the base XML path in the format file to read.
        :param str fmt_file: the absolute path to the format file to read.
        :keyword bool pixbuf: indicates whether or not to prepend a PixBuf
                              column to the gtk.TreeModel().
        :keyword bool indexed: indicates whether or not to append a column to
                               the gtk.TreeModel() to hold indexing
                               information.
        :return: None
        :rtype: None
        """
        # Retrieve the column heading text from the format file.
        self.headings = lxml.parse(fmt_file).xpath(fmt_path + "/usertitle")

        # Retrieve the column datatype from the format file.
        self.datatypes = lxml.parse(fmt_file).xpath(fmt_path + "/datatype")

        # Retrieve the column position from the format file.
        _position = lxml.parse(fmt_file).xpath(fmt_path + "/position")

        # Retrieve the cell renderer type from the format file.
        self.widgets = lxml.parse(fmt_file).xpath(fmt_path + "/widget")

        # Retrieve whether or not the column is editable from the format file.
        self.editable = lxml.parse(fmt_file).xpath(fmt_path + "/editable")

        # Retrieve whether or not the column is visible from the format file.
        self.visible = lxml.parse(fmt_file).xpath(fmt_path + "/visible")

        # Initialize public scalar instance attributes.
        _keys = lxml.parse(fmt_file).xpath(fmt_path + "/key")

        # Create a list of GObject datatypes to pass to the model.
        for i in range(len(self.datatypes)):  # pylint: disable=C0200
            self.datatypes[i] = self.datatypes[i].text
            self.editable[i] = int(self.editable[i].text)
            self.headings[i] = self.headings[i].text.replace("  ", "\n")
            self.order.append(int(_position[i].text))
            self.visible[i] = int(self.visible[i].text)
            self.widgets[i] = self.widgets[i].text
            _position[i] = int(_position[i].text)
            # Not all format files will have keys.
            try:
                _keys[i] = _keys[i].text
            except IndexError:
                pass

        # Append entries to each list if this RAMSTKTreeView is to display an
        # icon at the beginning of the row (Usage Profile, Hardware, etc.)
        if pixbuf:
            self.datatypes.append('pixbuf')
            self.editable.append(0)
            self.headings.append('')
            self.order.append(len(self.order))
            self.pixbuf_col = int(len(self.datatypes)) - 1
            self.visible.append(1)
            self.widgets.append('pixbuf')

        # We may want to add a column to hold indexing information for program
        # control.  This is used, for example, by aggregate data views to hold
        # the Node ID from the PyPubSub Tree().
        if indexed:
            self.datatypes.append('gchararray')
            self.editable.append(0)
            self.headings.append('')
            self.order.append(len(self.order))
            self.visible.append(0)
            self.widgets.append('text')
            self.index_col = int(len(self.datatypes)) - 1

        # Sort each of the lists according to the desired sequence provided in
        # the _position list.  This is necessary to allow for user-specific
        # ordering of columns in the RAMSTKTreeView.
        self.datatypes = [
            x for _, x in sorted(zip(self.order, self.datatypes))
        ]
        self.editable = [x for _, x in sorted(zip(self.order, self.editable))]
        self.headings = [x for _, x in sorted(zip(self.order, self.headings))]
        self.korder = [x for _, x in sorted(zip(_position, _keys))]
        self.visible = [x for _, x in sorted(zip(self.order, self.visible))]
        self.widgets = [x for _, x in sorted(zip(self.order, self.widgets))]

        return None

    def make_model(self, bg_color='#000000', fg_color='#FFFFFF'):
        """
        Make the RAMSTKTreeView() data model.

        :keyword str bg_col: the background color to use for each row.
                             Defaults to white.
        :keyword str fg_col: the foreground (text) color to use for each row.
                             Defaults to black.
        :return: None
        :rtype: None
        """
        _types = []

        # Create a list of GObject datatypes to pass to the model.
        for i in range(len(self.datatypes)):  # pylint: disable=C0200
            if self.datatypes[i] == 'pixbuf':
                _types.append(gtk.gdk.Pixbuf)
            else:
                _types.append(gobject.type_from_name(self.datatypes[i]))

        _model = gtk.TreeStore(*_types)
        self.set_model(_model)

        for _idx, _widget in enumerate(self.widgets):
            if _widget == 'combo':
                _cell = self._do_make_combo_cell()
                self._do_set_properties(_cell, bg_color, fg_color,
                                        self.editable[_idx])
            elif _widget == 'spin':
                _cell = self._do_make_spin_cell()
                self._do_set_properties(_cell, bg_color, fg_color,
                                        self.editable[_idx])
            elif _widget == 'toggle':
                _cell = self._do_make_toggle_cell(self.editable[_idx])
                self._do_set_properties(_cell, bg_color, fg_color,
                                        self.editable[_idx])
            elif _widget == 'blob':
                _cell = self._do_make_text_cell(True)
                self._do_set_properties(_cell, bg_color, fg_color,
                                        self.editable[_idx])
            else:
                _cell = self._do_make_text_cell()
                self._do_set_properties(_cell, bg_color, fg_color,
                                        self.editable[_idx])

            if self.pixbuf_col is not None and _idx == 0:
                _pbcell = gtk.CellRendererPixbuf()
                _pbcell.set_property('xalign', 0.5)
                _column = self._do_make_column(
                    [_pbcell, _cell], self.visible[_idx], self.headings[_idx])
                _column.set_attributes(_pbcell, pixbuf=self.pixbuf_col)
            else:
                _column = self._do_make_column([
                    _cell,
                ], self.visible[_idx], self.headings[_idx])
            _column.set_cell_data_func(
                _cell, self._format_cell,
                (self.order[_idx], self.datatypes[_idx]))

            if _widget == 'toggle':
                _column.set_attributes(_cell, active=self.order[_idx])
            elif _widget != 'pixbuf':
                _column.set_attributes(_cell, text=self.order[_idx])

            if _idx > 0:
                _column.set_reorderable(True)

            self.append_column(_column)

        return None

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
        if _entity is not None:
            # For simple data models that return an RAMSTK database
            # table instance for the data object, the first try
            # statement will create the list of attribute values.
            try:
                _temp = _entity.get_attributes()
                for _key in self.korder:
                    if isinstance(_temp[_key], datetime.date):
                        _temp[_key] = _temp[_key].strftime("%Y-%m-%d")
                    _attributes.append(_temp[_key])
            except AttributeError:
                # For aggregate data models (Hardware, Software) that
                # return a dictionary of attributes from ALL associated
                # RAMSTK database tables, this try statement will create
                # the list of attribute values.
                try:
                    for _key in self.korder:
                        _attributes.append(_entity[_key])
                except TypeError:
                    _return = True

            try:
                _row = _model.append(row, _attributes)
            except (TypeError, ValueError):
                _row = None
                _return = True

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self.do_load_tree(_child_tree, _row)

        return _return

    def _do_make_column(self, cells, visible, heading):
        """
        Make a gtk.TreeViewColumn().

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

        _label = RAMSTKLabel(
            heading, width=-1, height=-1, justify=gtk.JUSTIFY_CENTER)
        _column.set_widget(_label)
        _column.set_resizable(True)
        _column.set_alignment(0.5)
        _column.set_visible(visible)

        return _column

    @staticmethod
    def _do_make_combo_cell():
        """
        Make a gtk.CellRendererCombo().

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
        Make a gtk.CellRendererCombo().

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
        Make a gtk.CellRendererCombo().

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
            cell.set_property('wrap-mode', pango.WRAP_WORD)
        else:
            cell.set_property('activatable', editable)

        cell.set_property('yalign', 0.1)

    @staticmethod
    def do_edit_cell(cell, path, new_text, position, model):
        """
        Handle gtk.CellRenderer() edits.

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
        Set the formatting of the gtk.Treeview() gtk.CellRenderers().

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
        Dynamically set wrap-width property for a gtk.CellRenderer().

        This is called whenever the column widht in the gtk.TreeView() is
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
            return True
        else:
            _width += 10

        try:
            cell.set_property('wrap-width', _width)
        except TypeError:  # This is a gtk.CellRendererToggle
            cell.set_property('width', _width)

        return False


class CellRendererML(gtk.CellRendererText):
    """Create a multi-line cell renderer."""

    def __init__(self):
        """Initialize a CellRendererML instance."""
        gtk.CellRendererText.__init__(self)

        self.textedit_window = None
        self.selection = None
        self.treestore = None
        self.treeiter = None

        self.textedit = gtk.TextView()
        self.textbuffer = self.textedit.get_buffer()

    def do_get_size(self, widget, cell_area):
        """
        Get the size of the CellRendererML.

        :param widget:
        :param cell_area:
        """
        size_tuple = gtk.CellRendererText.do_get_size(self, widget, cell_area)

        return size_tuple

    def do_start_editing(self, __event, treeview, path, __background_area,
                         cell_area, __flags):
        """
        Handle edits of the CellRendererML.

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
            print("response %i received" % response)
            self.textedit_window.destroy()

    def _keyhandler(self, __widget, event):
        """
        Handle key-press-events on the gtk.TextView().

        :param __widget: the gtk.TextView() that called this method.
        :param event: the gtk.gdk.Event() that called this method.
        """
        _keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & (gtk.gdk.SHIFT_MASK | gtk.gdk.CONTROL_MASK) and \
                _keyname == 'Return':
            self.textedit_window.response(gtk.RESPONSE_OK)


# Register the new widget types.
gobject.type_register(RAMSTKTreeView)
gobject.type_register(CellRendererML)
