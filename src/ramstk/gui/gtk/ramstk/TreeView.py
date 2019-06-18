# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.TreeView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTreeView Module."""

# Standard Library Imports
import datetime

# Third Party Imports
import defusedxml.lxml as lxml
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.Utilities import integer_to_boolean

# RAMSTK Local Imports
from .Label import RAMSTKLabel
from .Widget import Gdk, GdkPixbuf, GObject, Gtk, Pango


class RAMSTKTreeView(Gtk.TreeView):
    """The RAMSTKTreeView class."""

    # pylint: disable=R0913, R0914, W0613
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
        GObject.GObject.__init__(self)

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
                fmt_path,
                fmt_file,
                pixbuf=_pixbuf,
                indexed=_indexed,
            )
            self.make_model(bg_col, fg_col)

    def do_parse_format(self, fmt_path, fmt_file, pixbuf=False, indexed=False):
        """
        Parse the format file for the RAMSTKTreeView().

        :param str fmt_path: the base XML path in the format file to read.
        :param str fmt_file: the absolute path to the format file to read.
        :keyword bool pixbuf: indicates whether or not to prepend a PixBuf
                              column to the Gtk.TreeModel().
        :keyword bool indexed: indicates whether or not to append a column to
                               the Gtk.TreeModel() to hold indexing
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
            self.editable[i] = integer_to_boolean(int(self.editable[i].text))
            self.headings[i] = self.headings[i].text.replace("  ", "\n")
            self.order.append(int(_position[i].text))
            self.visible[i] = integer_to_boolean(int(self.visible[i].text))
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
            self.visible.append(True)
            self.widgets.append('pixbuf')

        # We may want to add a column to hold indexing information for program
        # control.  This is used, for example, by aggregate data views to hold
        # the Node ID from the PyPubSub Tree().
        if indexed:
            self.datatypes.append('gchararray')
            self.editable.append(0)
            self.headings.append('')
            self.order.append(len(self.order))
            self.visible.append(False)
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

        # Add a column at the end to hold a string representation of the
        # attributes dict.
        self.datatypes.append('gchararray')
        self.editable.append(0)
        self.headings.append('Attributes')
        self.korder.append('dict')
        self.order.append(len(self.order))
        self.visible.append(False)
        self.widgets.append('text')

    def do_set_visible_columns(self, **kwargs):
        """
        Set the treeview columns visible, hidden, and/or editable.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        try:
            _visible = kwargs['visible']
        except KeyError:
            _visible = []
        try:
            _editable = kwargs['editable']
        except KeyError:
            _editable = []
        _return = False

        for _col in _visible:
            try:
                self.get_column(_col).set_visible(1)
                _column = self.get_column(_col)
                _cells = _column.get_cells()
            except AttributeError:
                _cells = []

            for __, _cell in enumerate(_cells):
                try:
                    _cell.set_property('background', 'light gray')
                    _cell.set_property('editable', 0)
                except TypeError:
                    _cell.set_property('cell-background', 'light gray')

        for _col in _editable:
            try:
                _column = self.get_column(_col)
                _cells = _column.get_cells()
            except AttributeError:
                _cells = []

            for __, _cell in enumerate(_cells):
                try:
                    _cell.set_property('background', 'white')
                    _cell.set_property('editable', 1)
                except TypeError:
                    _cell.set_property('cell-background', 'white')

        return _return

    def do_load_tree(self, tree, row=None):
        """
        Load the Module View's Gtk.TreeModel() with the Module's tree.

        :param tree: the Module's treelib Tree().
        :type tree: :class:`treelib.Tree`
        :param row: the parent row in the Gtk.TreeView() to add the new item.
        :type row: :class:`Gtk.TreeIter`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _row = None
        _model = self.get_model()

        _node = tree.nodes[list(SortedDict(tree.nodes).keys())[0]]
        _entity = _node.data

        _attributes = []
        if _entity is not None: # pylint: disable=too-many-nested-blocks
            # For simple data models that return a RAMSTK database
            # table instance for the data object, the first try
            # statement will create the list of attribute values.
            try:
                _temp = _entity.get_attributes()
                for _key in self.korder:
                    if _key == 'dict':
                        _attributes.append(str(_temp))
                    else:
                        try:
                            if isinstance(_temp[_key], datetime.date):
                                _temp[_key] = _temp[_key].strftime("%Y-%m-%d")
                            _temp[_key] = _temp[_key].decode('utf-8')
                        except(AttributeError, KeyError):
                            pass
                        _attributes.append(_temp[_key])
            except AttributeError:
                # For aggregate data models (Hardware, Software) that
                # return a dictionary of attributes from ALL associated
                # RAMSTK database tables, this try statement will create
                # the list of attribute values.
                try:
                    for _key in self.korder:
                        if _key == 'dict':
                            _attributes.append(str(_entity))
                        else:
                            try:
                                _entity[_key] = _entity[_key].decode('utf-8')
                            except AttributeError:
                                pass
                            _attributes.append(_entity[_key])
                except TypeError:
                    _return = True

            try:
                _row = _model.append(row, _attributes)
            except TypeError:
                _row = None
                _return = True
            except ValueError:
                _row = None
                _return = True

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self.do_load_tree(_child_tree, _row)

        return _return

    def _do_make_column(self, cells, visible, heading):
        """
        Make a Gtk.TreeViewColumn().

        :param list cells: list of Gtk.CellRenderer()s that are to be packed in
                           the column.
        :param int visible: indicates whether the column will be visible.
        :param str heading: the column heading text.
        :return: _column
        :rtype: :class:`Gtk.TreeViewColumn`
        """
        _column = Gtk.TreeViewColumn("")

        for _cell in cells:
            if isinstance(_cell, Gtk.CellRendererPixbuf):
                _column.pack_start(_cell, False)
            else:
                _column.pack_start(_cell, True)
                _column.connect('notify::width', self._resize_wrap, _cell)

        _label = RAMSTKLabel(
            heading,
            width=-1,
            height=-1,
            justify=Gtk.Justification.CENTER,
        )
        _column.set_widget(_label)
        _column.set_resizable(True)
        _column.set_alignment(0.5)
        _column.set_visible(visible)

        return _column

    @staticmethod
    def _do_make_combo_cell():
        """
        Make a Gtk.CellRendererCombo().

        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        _cell = Gtk.CellRendererCombo()
        _cellmodel = Gtk.ListStore(GObject.TYPE_STRING)
        _cellmodel.append([""])
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)

        return _cell

    @staticmethod
    def _do_make_spin_cell():
        """
        Make a Gtk.CellRendererCombo().

        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        :param int position: the position in the Gtk.TreeModel() that this
                             cell falls.
        :param model: the Gtk.TreeModel() the cell belongs to.
        :type model: :class:`Gtk.TreeModel`
        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        _cell = Gtk.CellRendererSpin()
        _adjustment = Gtk.Adjustment(upper=5.0, step_incr=0.05)
        _cell.set_property('adjustment', _adjustment)
        _cell.set_property('digits', 2)

        return _cell

    @staticmethod
    def _do_make_text_cell(blob=False):
        """
        Make a Gtk.CellRendererCombo().

        :param bool blob: indicates whether the cell will be displaying a BLOB
                          field.
        :type model: :class:`Gtk.TreeModel`
        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        if not blob:
            _cell = Gtk.CellRendererText()
        else:
            _cell = CellRendererML()

        return _cell

    @staticmethod
    def _do_make_toggle_cell(editable):
        """
        Make a Gtk.CellRendererCombo().

        :param int editable: indicates whether the cell is editable.
        :return: _cell
        :rtype: :class:`Gtk.CellRendererCombo`
        """
        _cell = Gtk.CellRendererToggle()
        _cell.set_property('activatable', editable)

        return _cell

    @staticmethod
    def _do_set_properties(cell, bg_color, fg_color, editable):
        """
        Set common properties of Gtk.CellRenderers().

        :param cell: the cell whose properties are to be set.
        :type cell: :class:`Gtk.CellRenderer`
        :param str bg_color: the cell background color.
        :param str fg_color: the cell foreground color.
        :param int editable: indicates whether the cell is editable.
        :return: None
        :rtype: None
        """
        if editable == 0:
            cell.set_property('cell-background', 'light gray')
        else:
            cell.set_property('cell-background', bg_color)

        if not isinstance(cell, Gtk.CellRendererToggle):
            cell.set_property('editable', editable)
            cell.set_property('foreground', fg_color)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', Pango.WrapMode.WORD)
        else:
            cell.set_property('activatable', editable)

        cell.set_property('yalign', 0.1)

    @staticmethod
    def do_edit_cell(cell, path, new_text, position, model):
        """
        Handle Gtk.CellRenderer() edits.

        :param Gtk.CellRenderer cell: the Gtk.CellRenderer() that was edited.
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer() that
                         was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param Gtk.TreeModel model: the Gtk.TreeModel() the Gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
        _convert = GObject.type_name(model.get_column_type(position))

        if isinstance(cell, Gtk.CellRendererToggle):
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

    def get_cell_model(self, column, clear=True):
        """
        Retrieve the Gtk.TreeModel() from a Gtk.CellRendererCombo().

        :param int column: the column number to retrieve the cell's model.
        :param bool clear: whether or not to clear the Gtk.TreeModel().
        Default is True.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property("model")

        if clear:
            _model.clear()

        return _model

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
                _types.append(GdkPixbuf.Pixbuf)
            elif self.datatypes[i] == 'pyobject':
                _types.append(GObject.TYPE_PYOBJECT)
            else:
                _types.append(GObject.type_from_name(self.datatypes[i]))

        _model = Gtk.TreeStore(*_types)
        self.set_model(_model)

        for _idx, _widget in enumerate(self.widgets):
            if _widget == 'combo':
                _cell = self._do_make_combo_cell()
            elif _widget == 'spin':
                _cell = self._do_make_spin_cell()
            elif _widget == 'toggle':
                _cell = self._do_make_toggle_cell(self.editable[_idx])
            elif _widget == 'blob':
                _cell = self._do_make_text_cell(True)
            else:
                _cell = self._do_make_text_cell()
            self._do_set_properties(
                _cell,
                bg_color,
                fg_color,
                self.editable[_idx],
            )

            if self.pixbuf_col is not None and _idx == 0:
                _pbcell = Gtk.CellRendererPixbuf()
                _pbcell.set_property('xalign', 0.5)
                _column = self._do_make_column(
                    [_pbcell, _cell],
                    self.visible[_idx],
                    self.headings[_idx],
                )
                _column.set_attributes(_pbcell, pixbuf=self.pixbuf_col)
            else:
                _column = self._do_make_column(
                    [
                        _cell,
                    ],
                    self.visible[_idx],
                    self.headings[_idx],
                )
            _column.set_cell_data_func(
                _cell,
                self._format_cell,
                (self.order[_idx], self.datatypes[_idx]),
            )

            if _widget == 'toggle':
                _column.set_attributes(_cell, active=self.order[_idx])
            elif _widget != 'pixbuf':
                _column.set_attributes(_cell, text=self.order[_idx])

            if _idx > 0:
                _column.set_reorderable(True)

            self.append_column(_column)

    @staticmethod
    def _format_cell(__column, cell, model, row, data):
        """
        Set the formatting of the Gtk.Treeview() Gtk.CellRenderers().

        :param __column: the Gtk.TreeViewColumn() containing the
                         Gtk.CellRenderer() to format.
        :type __column: :class:`Gtk.TreeViewColumn`
        :param cell: the Gtk.CellRenderer() to format.
        :type cell: :class:`Gtk.CellRenderer`
        :param model: the Gtk.TreeModel() containing the Gtk.TreeViewColumn().
        :type model: :class:`Gtk.TreeModel`
        :param row: the Gtk.TreeIter() pointing to the row containing the
                    Gtk.CellRenderer() to format.
        :type row: :class:`Gtk.TreeIter`
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
        except TypeError:  # It's a Gtk.CellRendererToggle
            pass
        except ValueError:
            pass

        return

    @staticmethod
    def _resize_wrap(column, __param, cell):
        """
        Dynamically set wrap-width property for a Gtk.CellRenderer().

        This is called whenever the column width in the Gtk.TreeView() is
        resized.

        :param column: the Gtk.TreeViewColumn() being resized.
        :type column: :class:`Gtk.TreeViewColumn`
        :param GParamInt __param: the triggering parameter.
        :param cell: the Gtk.CellRenderer() that needs to be resized.
        :type cell: :class:`Gtk.CellRenderer`
        :return: None
        :rtype: None
        """
        _width = column.get_width()

        if _width <= 0:
            pass
        else:
            _width += 10

            try:
                cell.set_property('wrap-width', _width)
            except TypeError:  # This is a Gtk.CellRendererToggle
                cell.set_property('width', _width)


class CellRendererML(Gtk.CellRendererText):
    """Create a multi-line cell renderer."""

    def __init__(self):
        """Initialize a CellRendererML instance."""
        GObject.GObject.__init__(self)

        self.textedit_window = None
        self.selection = None
        self.treestore = None
        self.treeiter = None

        self.textedit = Gtk.TextView()
        self.textbuffer = self.textedit.get_buffer()

    def do_get_size(self, widget, cell_area):
        """
        Get the size of the CellRendererML.

        :param widget:
        :param cell_area:
        """
        size_tuple = Gtk.CellRendererText.do_get_size(self, widget, cell_area)

        return size_tuple

    def do_start_editing(
            self,
            __event,
            treeview,
            path,
            __background_area,
            cell_area,
            __flags,
    ):
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

        self.textedit_window = Gtk.Dialog(parent=treeview.get_toplevel())
        self.textedit_window.action_area.hide()
        self.textedit_window.set_decorated(False)
        self.textedit_window.set_property('skip-taskbar-hint', True)
        self.textedit_window.set_transient_for(None)

        self.textedit.set_editable(True)
        self.textedit.set_property('visible', True)
        self.textbuffer.set_property('text', self.get_property('text'))

        self.textedit_window.connect('key-press-event', self._keyhandler)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        scrolled_window.set_property('visible', True)
        # self.textedit_window.vbox.pack_start(scrolled_window, True, True, 0)

        scrolled_window.add(self.textedit)
        self.textedit_window.vbox.add(scrolled_window)
        self.textedit_window.realize()

        # Position the popup below the edited cell (and try hard to keep the
        # popup within the toplevel window)
        (tree_x, tree_y) = treeview.get_bin_window().get_origin()
        (tree_w, tree_h) = treeview.window.get_geometry()[2:4]
        (t_w, t_h) = self.textedit_window.window.get_geometry()[2:4]
        x_pos = tree_x + min(
            cell_area.x,
            tree_w - t_w + treeview.get_visible_rect().x,
        )
        y_pos = tree_y + min(
            cell_area.y,
            tree_h - t_h + treeview.get_visible_rect().y,
        )
        self.textedit_window.move(x_pos, y_pos)
        self.textedit_window.resize(cell_area.width, cell_area.height)

        # Run the dialog, get response by tracking keypresses
        response = self.textedit_window.run()

        if response == Gtk.ResponseType.OK:
            self.textedit_window.destroy()

            (iter_first, iter_last) = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(iter_first, iter_last)

            # self.treestore[path][2] = text

            treeview.set_cursor(path, None, False)

            self.emit('edited', path, text)

        elif response == Gtk.ResponseType.CANCEL:
            self.textedit_window.destroy()
        else:
            print(("response %i received" % response))
            self.textedit_window.destroy()

    def _keyhandler(self, __widget, event):
        """
        Handle key-press-events on the Gtk.TextView().

        :param __widget: the Gtk.TextView() that called this method.
        :param event: the Gdk.Event() that called this method.
        """
        _keyname = Gdk.keyval_name(event.keyval)

        if event.get_state() & (Gdk.ModifierType.SHIFT_MASK | Gdk.ModifierType.CONTROL_MASK) and \
                _keyname == 'Return':
            self.textedit_window.response(Gtk.ResponseType.OK)


# Register the new widget types.
GObject.type_register(RAMSTKTreeView)
GObject.type_register(CellRendererML)
