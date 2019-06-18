# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.View.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseView Module."""

# Standard Library Imports
import ast
import locale

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKMessageDialog, RAMSTKTreeView
from ramstk.gui.gtk.ramstk.Widget import Gdk, GdkPixbuf, Gtk, _


class RAMSTKBaseView():
    """
    Meta class for all RAMSTK ListView, ModuleView, and WorkView classes.

    Attributes of the RAMSTKBaseView are:

    :cvar RAMSTK_CONFIGURATION: the instance of the RAMSTK Configuration class.
    :type RAMSTK_CONFIGURATION: :class:`ramstk.Configuration.Configuration`
    :cvar dict dic_tab_position: dictionary holding the Gtk.PositionType()s for
                                 each of left, right, top, and botton.

    :ivar dict _dic_icons: dictionary containing icon name and absolute path
                           key:value pairs.
    :ivar list _lst_col_order: list containing the order of the columns in the
                               List View RAMSTKTreeView().
    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each Gtk.Widget() associated with
                                an editable attribute.
    :ivar float _mission_time: the mission time for the open RAMSTK Program.
    :ivar _notebook: the Gtk.Notebook() to hold all the pages of information to
                     be displayed.
    :type _notebook: :class:`Gtk.Notebook`
    :ivar int _revision_id: the ID of the Revision associated with the
                            information being displayed in the View.
    :ivar int _parent_id: the ID of the parent object associated with the
                          information being displayed in the View.
    :ivar treeview: the Gtk.TreeView() to display the information for the View.
    :type treeview: :class:`Gtk.TreeView`
    :ivar str fmt: the formatting code for numerical displays.
    :ivar hbox_tab_label: the Gtk.HBox() containing the View's Gtk.Notebook()
                          tab Gtk.Label().
    :type hbox_tab_label: :class:`Gtk.HBox`
    """

    RAMSTK_CONFIGURATION = None

    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM,
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize the RAMSTK Base View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        _module = kwargs['module']
        self.RAMSTK_CONFIGURATION = configuration

        # Initialize private dictionary attributes.
        self._dic_icons = {
            'calculate':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/calculate.png',
            'calculate_all':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/calculate-all.png',
            'add':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/add.png',
            'remove':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/remove.png',
            'reports':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/reports.png',
            'save':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/save.png',
            'save-all':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/save-all.png',
            'important':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/important.png',
            'error':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/error.png',
            'question':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/question.png',
            'insert_sibling':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/insert_sibling.png',
            'insert_child':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/insert_child.png',
            'cancel':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/cancel.png',
            'export':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/export.png',
            'warning':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/warning.png',
            'rollup':
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/rollup.png',
        }

        # Initialize private list attributes.
        self._lst_col_order = []
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mission_time = float(self.RAMSTK_CONFIGURATION.RAMSTK_MTIME)
        self._notebook = Gtk.Notebook()
        self._revision_id = None
        self._parent_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        if _module is None:
            self.treeview = None
        else:
            try:
                _bg_color = self.RAMSTK_CONFIGURATION.RAMSTK_COLORS[
                    _module +
                    'bg'
                ]
                _fg_color = self.RAMSTK_CONFIGURATION.RAMSTK_COLORS[
                    _module +
                    'fg'
                ]
                _fmt_file = (
                    self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/' +
                    self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE[_module]
                )
                _fmt_path = "/root/tree[@name='" + _module.title(
                ) + "']/column"

                self.treeview = RAMSTKTreeView(
                    _fmt_path, 0, _fmt_file,
                    _bg_color, _fg_color,
                )
                self._lst_col_order = self.treeview.order
            except KeyError:
                self.treeview = Gtk.TreeView()

        self.fmt = '{0:0.' + \
                   str(self.RAMSTK_CONFIGURATION.RAMSTK_DEC_PLACES) + \
                   'G}'
        self.hbx_tab_label = Gtk.HBox()

        try:
            locale.setlocale(
                locale.LC_ALL,
                self.RAMSTK_CONFIGURATION.RAMSTK_LOCALE,
            )
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_select_revision, 'selected_revision')

    def do_load_tree(self, tree):
        """
        Load the RAMSTK View RAMSTKTreeView().

        This method is called in response to the 'retrieved_<module>'.

        :param tree: the treelib Tree containing the module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        try:
            _tag = tree.get_node(0).tag
        except AttributeError:
            _tag = "UNK"

        if self.treeview.do_load_tree(tree):
            _prompt = _(
                "An error occured while loading the {1:s} "
                "records for Revision ID {0:d} into the "
                "view.",
            ).format(self._revision_id, _tag)
            _dialog = RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'],
                'error', self,
            )
            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.do_destroy()

        _row = _model.get_iter_first()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

    def do_raise_dialog(self, **kwargs):
        """
        Raise a dialog in response to information, warnings, and errors.

        This method will display an message dialog of the appropriate severity
        information, warning, or error containing a message to the user.  It
        will also write a message to the RAMSTK debug_log to (hopefully) assist
        in troubleshooting.

        :return: None
        :rtype: None
        """
        try:
            _error_code = kwargs['error_code']
        except KeyError:
            _error_code = 0
        try:
            _severity = kwargs['severity']
        except KeyError:
            _severity = ''
        try:
            _user_msg = kwargs['user_msg']
        except KeyError:
            _user_msg = ''
        try:
            _debug_msg = kwargs['debug_msg']
        except KeyError:
            _debug_msg = ''

        if _error_code != 0:
            self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(_debug_msg)
            _dialog = RAMSTKMessageDialog(
                _user_msg, self._dic_icons[_severity], _severity,
            )
            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.destroy()

    def do_refresh_tree(self, module_id, key, value):
        """
        Refresh the data in the RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()

        try:
            _column = [
                _index for _index, _key in enumerate(self.treeview.korder)
                if _key == key
            ][0]

            try:
                _model.set_value(_row, _column, value)
            except AttributeError:
                _prompt = _(
                    "An error occurred while refreshing column {0:d} "
                    "for record {1:d}.",
                ).format(_column, module_id)
                _dialog = RAMSTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error',
                )
                if _dialog.do_run() == self._response_ok:
                    _dialog.do_destroy()
        except IndexError:
            pass

        # Update the attributes dict in the last column.
        _attributes = ast.literal_eval(
            _model.get_value(
                _row,
                _model.get_n_columns() - 1,
            ),
        )
        _attributes[key] = value
        _model.set_value(_row, _model.get_n_columns() - 1, str(_attributes))

    def do_request_insert_child(self, __button, **kwargs):
        """
        Request to insert a new child entity of the selected entity.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=False, **kwargs)

    def do_request_insert_sibling(self, __button, **kwargs):
        """
        Send request to insert a new sibling entity.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=True, **kwargs)

    def do_set_cursor(self, cursor):
        """
        Set the cursor for the Module, List, and Work Book Gdk.Window().

        :param cursor: the Gdk.Cursor.new() to set.  Only handles one of the
                       following:
                       - Gdk.CursorType.X_CURSOR
                       - Gdk.CursorType.ARROW
                       - Gdk.CursorType.CENTER_PTR
                       - Gdk.CIRCLE
                       - Gdk.CROSS
                       - Gdk.CROSS_REVERSE
                       - Gdk.CursorType.CROSSHAIR
                       - Gdk.DIAMOND_CROSS
                       - Gdk.DOUBLE_ARROW
                       - Gdk.DRAFT_LARGE
                       - Gdk.DRAFT_SMALL
                       - Gdk.EXCHANGE
                       - Gdk.FLEUR
                       - Gdk.GUMBY
                       - Gdk.HAND1
                       - Gdk.HAND2
                       - Gdk.CursorType.LEFT_PTR - non-busy cursor
                       - Gdk.PENCIL
                       - Gdk.PLUS
                       - Gdk.QUESTION_ARROW
                       - Gdk.CursorType.RIGHT_PTR
                       - Gdk.SB_DOWN_ARROW
                       - Gdk.SB_H_DOUBLE_ARROW
                       - Gdk.SB_LEFT_ARROW
                       - Gdk.SB_RIGHT_ARROW
                       - Gdk.SB_UP_ARROW
                       - Gdk.SB_V_DOUBLE_ARROW
                       - Gdk.TCROSS
                       - Gdk.TOP_LEFT_ARROW
                       - Gdk.CursorType.WATCH - when application is busy
                       - Gdk.XTERM - selection bar
        :type cursor: :class:`Gdk.Cursor`
        :return: None
        :rtype: None
        """
        self.get_parent_window().set_cursor(
            Gdk.Cursor.new(cursor),
        )
        #self._mdcRAMSTK.dic_books['modulebook'].get_window().set_cursor(
        #    Gdk.Cursor.new(cursor),
        #)
        #self._mdcRAMSTK.dic_books['workbook'].get_window().set_cursor(
        #    Gdk.Cursor.new(cursor),
        #)

        Gdk.flush()

    def _make_toolbar(
            self,
            icons,
            orientation='horizontal',
            height=60,
            width=60,
    ):
        """
        Create the toolbar for RAMSTK Views.

        This method creates the base toolbar used by all RAMSTK Views.  Use a
        toolbar for an RAMSTK View if there are other than buttons to be added.

        :param list icons: list of icon names to place on the toolbuttons.
                           The items in the list are keys in _dic_icons.
        :return: _toolbar, _position
        :rtype: (:py:class:`Gtk.Toolbar`, int)
        """
        _toolbar = Gtk.Toolbar()

        if orientation == 'horizontal':
            _toolbar.set_orientation(Gtk.Orientation.HORIZONTAL)
            _scale = 0.58
        else:
            _toolbar.set_orientation(Gtk.Orientation.VERTICAL)
            _scale = 0.4

        _position = 0
        for _icon in icons:
            if _icon is None:
                _toolbar.insert(Gtk.SeparatorToolItem(), _position)
            else:
                _image = Gtk.Image()
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons[_icon], int(_scale * height),
                    int(_scale * width),
                )
                _image.set_from_pixbuf(_icon)

                _button = Gtk.ToolButton()
                _button.set_property("height_request", height)
                _button.set_property("width_request", width)
                _button.set_icon_widget(_image)
                _button.show()
                _toolbar.insert(_button, _position)

            _position += 1

        _toolbar.show()

        # Return the toolbar and the next position to place an Gtk.ToolBar()
        # item.  The _position variable can be used by derived classes to
        # add additional items to the Gtk.ToolBar().
        return _toolbar, _position

    def make_treeview(self, **kwargs):
        """
        Set up the Module View RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        try:
            _editable = kwargs['editable']
        except KeyError:
            _editable = []
        _index = 0

        for _column in self.treeview.get_columns():
            _cell = _column.get_cells()[0]
            if _index in _editable:
                _color = Gdk.RGBA(255.0, 255.0, 255.0, 1.0)
                try:
                    _cell.set_property('editable', True)
                    _cell.connect(
                        'edited', self._on_cell_edit, _index,
                        self.treeview.get_model(),
                    )
                except TypeError:
                    _cell.set_property('activatable', True)
                    _cell.connect(
                        'toggled', self._on_cell_edit, _index,
                        self.treeview.get_model(),
                    )
            else:
                _color = Gdk.RGBA(238.0, 238.0, 238.0, 1.0)
                try:
                    _cell.set_property('editable', False)
                except TypeError:
                    _cell.set_property('activatable', False)
            _cell.set_property('cell-background-rgba', _color)
            _index += 1

    def on_button_press(self, event, **kwargs):
        """
        Handle mouse clicks on the View's RTKTreeView().

        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: None
        :rtype: None
        """
        _icons = kwargs['icons']
        _labels = kwargs['labels']
        _callbacks = kwargs['callbacks']

        _menu = Gtk.Menu()
        _menu.popup(None, None, None, event.button, event.time)

        for _idx, __ in enumerate(_icons):
            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(self._dic_icons[_icons[_idx]])
            _menu_item.set_label(_labels[_idx])
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', _callbacks[_idx])
            _menu_item.show()
            _menu.append(_menu_item)

    def on_focus_out(self, entry, index, module_id, message):
        """
        Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
        method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
        :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
        associated with the data from the calling Gtk.Widget().
        :param int module_id: the ID of the RAMSTK<MODULE> whose entry is being
        changed.
        :param str message: the PyPubSub message to publish.
        :return: None
        :rtype: None
        """
        try:
            _key = self._dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(entry.get_text())
        except ValueError:
            try:
                _new_text = float(entry.get_text())
            except ValueError:
                try:
                    _new_text = str(entry.get_text())
                except ValueError:
                    _new_text = None

        entry.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(
            message,
            module_id=module_id,
            key=_key,
            value=_new_text,
        )

    def on_select(self, **kwargs):
        """
        Respond to load the Work View Gtk.Notebook() widgets.

        This method handles the results of the an individual module's
        _on_select() method.  It sets the title of the RAMSTK Work Book and
        raises an error dialog if needed.

        :return: None
        :rtype: None
        """
        _title = kwargs['title']

        try:
            _workbook = self.get_parent().get_parent()
            _workbook.set_title(_title)
        except AttributeError:
            pass

        return self.do_raise_dialog(severity='warning', **kwargs)

    def on_select_revision(self, attributes):
        """
        Set the Revision ID when a new Revision is selected.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
