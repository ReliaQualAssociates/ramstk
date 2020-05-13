# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKBaseView Module."""

# Standard Library Imports
import datetime
import locale
from typing import Any, Dict, List, Tuple

# Third Party Imports
# noinspection PyPackageRequirements
import pandas as pd
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, _

# RAMSTK Local Imports
from .button import RAMSTKCheckButton, do_make_buttonbox
from .dialog import RAMSTKMessageDialog
from .entry import RAMSTKTextView
from .frame import RAMSTKFrame
from .label import RAMSTKLabel, do_make_label_group, do_make_label_group2
from .matrixview import RAMSTKMatrixView
from .scrolledwindow import RAMSTKScrolledWindow
from .treeview import RAMSTKTreeView


class RAMSTKBaseView(Gtk.HBox):
    """
    Meta class for all RAMSTK ListView, ModuleView, and WorkView classes.

    Attributes of the RAMSTKBaseView are:

    :cvar RAMSTK_USER_CONFIGURATION: the instance of the RAMSTK Configuration
        class.
    :type RAMSTK_USER_CONFIGURATION: :class:`ramstk.Configuration.Configuration`
    :cvar dict dic_tab_position: dictionary holding the Gtk.PositionType()s for
        each of left, right, top, and botton.

    :ivar dict _dic_icons: dictionary containing icon name and absolute path
        key:value pairs.
    :ivar list _lst_col_order: list containing the order of the columns in the
        List View RAMSTKTreeView().
    :ivar list _lst_handler_id: list containing the ID's of the callback
        signals for each Gtk.Widget() associated with an editable attribute.
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
    :ivar hbx_tab_label: the Gtk.HBox() containing the View's Gtk.Notebook()
        tab Gtk.Label().
    :type hbx_tab_label: :class:`Gtk.HBox`
    """
    RAMSTK_USER_CONFIGURATION = None

    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM
    }

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = '') -> None:
        """
        Initialize the RAMSTK Base View.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        GObject.GObject.__init__(self)

        self.RAMSTK_USER_CONFIGURATION = configuration
        self.RAMSTK_LOGGER = logger
        self.RAMSTK_LOGGER.do_create_logger(
            __name__, self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL)

        # Initialize private dictionary attributes.
        self._dic_icons = self.__set_icons()

        # Initialize private list attributes.
        self._lst_col_order: List[int] = []
        self._lst_handler_id: List[int] = []
        self._lst_layouts: List[str] = [
            'allocation', 'failure_definition', 'fmea', 'function', 'hardware',
            'hazard', 'incident', 'pof', 'requirement', 'revision',
            'similar_item', 'software', 'stakeholder', 'testing', 'validation'
        ]

        # Initialize private scalar attributes.
        self._mission_time: float = float(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MTIME)
        self._module: str = module
        self._notebook: Gtk.Notebook = Gtk.Notebook()
        self._revision_id: int = 0
        self._parent_id: int = 0
        self._record_id: int = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.treeview: RAMSTKTreeView = self._make_treeview(module)
        self.fmt: str = (
            '{0:0.' + str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES)
            + 'G}')
        self.hbx_tab_label: Gtk.HBox = Gtk.HBox()

        try:
            locale.setlocale(locale.LC_ALL,
                             self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOCALE)
        except locale.Error as _error:
            locale.setlocale(locale.LC_ALL, '')
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_select_revision, 'selected_revision')

    def __set_callbacks(self) -> None:
        """
        Set common callback methods.

        Sets callback for the RAMSTKView, Gtk.TreeView, and Gtk.TreeSelection.

        :return: None
        :rtype: None
        """
        try:
            self._lst_handler_id.append(
                self.treeview.selection.connect('changed',
                                                self._on_row_change))
        except AttributeError as _error:
            if self._module in self._lst_layouts:
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        try:
            self._lst_handler_id.append(
                self.treeview.connect('button_press_event',
                                      self._on_button_press))
        except AttributeError as _error:
            if self._module in self._lst_layouts:
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def __set_icons(self) -> Dict:
        """
        Set the dict of icons.

        :return: the dict of icons to use in RAMSTK.
        :rtype: dict
        """
        return {
            'add':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/add.png',
            'calculate':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/calculate.png',
            'calculate_all':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/calculate-all.png',
            'cancel':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/cancel.png',
            'complete':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/complete.png',
            'chart':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/charts.png',
            'error':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/error.png',
            'export':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/export.png',
            'important':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/important.png',
            'insert_child':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/insert_child.png',
            'insert_sibling':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/insert_sibling.png',
            'none':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/none.png',
            'partial':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/partial.png',
            'question':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/question.png',
            'refresh-view':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/view-refresh.png',
            'remove':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/remove.png',
            'rollup':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/rollup.png',
            'reports':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/reports.png',
            'save':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/save.png',
            'save-all':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/save-all.png',
            'warning':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/warning.png'
        }

    def _make_toolbar(self,
                      icons: List[str],
                      orientation: str = 'horizontal',
                      height: int = 60,
                      width: int = 60) -> Tuple[Gtk.Toolbar, int]:
        """
        Create the toolbar for RAMSTK Views.

        This method creates the base toolbar used by all RAMSTK Views.  Use a
        toolbar for an RAMSTK View if there are other than buttons to be added.

        :param list icons: list of icon names to place on the toolbuttons.
            The items in the list are keys in _dic_icons.
        :return: _toolbar, _position
        :rtype: (:class:`Gtk.Toolbar`, int)
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
                    int(_scale * width))
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

    def _make_treeview(self, module: str) -> RAMSTKTreeView:
        """
        Make the RAMSTKTreeView instance for this view.

        :param str module: the name of the module this view is associated with.
        :return: _treeview; the RAMSTKTreeView() created.
        :rtype: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        """
        try:
            _treeview = RAMSTKTreeView()
            self._lst_col_order = _treeview.order

            _fmt_file = (
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
                + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[module])
            _fmt_path = "/root/tree[@name='" + module.title() + "']/column"
            _treeview.do_parse_format(_fmt_path, _fmt_file)

            try:
                _bg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                    module + 'bg']
                _fg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                    module + 'fg']
            except KeyError as _error:
                _bg_color = '#FFFFFF'
                _fg_color = '#000000'
                if module in self._lst_layouts:
                    self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

            _treeview.make_model(_bg_color, _fg_color)

        except KeyError as _error:
            _treeview = Gtk.TreeView()
            _treeview.selection = _treeview.get_selection()
            if module in self._lst_layouts:
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        _treeview.set_grid_lines(3)
        _treeview.set_enable_tree_lines(True)
        _treeview.set_level_indentation(2)

        return _treeview

    def do_expand_tree(self) -> None:
        """
        Expands the RAMSTKTreeView.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _row = _model.get_iter_first()

        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

    def do_load_tree(self, tree: treelib.Tree) -> None:
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
        except AttributeError as _error:
            _tag = "UNK"
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        try:
            self.treeview.do_load_tree(tree, _tag)
            self.treeview.expand_all()
            _row = _model.get_iter_first()
            if _row is not None:
                self.treeview.selection.select_iter(_row)
                self.show_all()
        except TypeError as _error:
            _error_msg = _(
                "An error occured while loading {1:s} records for Revision ID "
                "{0:d} into the view.  One or more values from the database "
                "was the wrong type for the column it was trying to "
                "load.").format(self._revision_id, _tag)
            self.RAMSTK_LOGGER.do_log_error(__name__, _error_msg)
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
        except ValueError as _error:
            _error_msg = _(
                "An error occured while loading {1:s} records for Revision ID "
                "{0:d} into the view.  One or more values from the database "
                "was missing.").format(self._revision_id, _tag)
            self.RAMSTK_LOGGER.do_log_error(__name__, _error_msg)
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def do_raise_dialog(self, **kwargs: Any) -> None:
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
            _dialog = RAMSTKMessageDialog(kwargs['user_msg'],
                                          self._dic_icons[kwargs['severity']],
                                          kwargs['severity'],
                                          parent=self)
            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.destroy()
        except KeyError as _error:
            _debug_msg = ("Failed attempting to raise a RAMSTKMessageDialog "
                          "with either the severity or message missing.")
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
        try:
            _debug_msg = kwargs['debug_msg']
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except KeyError as _error:
            _debug_msg = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def do_refresh_tree(self, package: Dict, keys: Dict) -> None:
        """
        Update the module view RAMSTKTreeView() with attribute changes.

        This method receives two dicts.  This first is from the
        workflow's workview module and is sent when a workview widget is
        edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The second dict is from the workflow's moduleview.

            `keys` key: `keys` value

        corresponds to:

            database field name: TreeModel default column position

        Since both dicts contain the same key values, this method can refresh
        the proper column of the RAMSTKTreeView with the new data.

        :param dict package: the key:value for the data being updated.
        :param dict keys: the name:index relationship for the work stream
            module's data keys.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        _position = self._lst_col_order[keys[_key]]

        _model, _row = self.treeview.get_selection().get_selected()
        _model.set(_row, _position, _value)

    def do_request_insert(self, **kwargs: Any) -> None:
        """
        Request insert a new work stream element into the program database.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        if _sibling:
            pub.sendMessage('request_insert_{0:s}'.format(
                self._module.lower()))
        else:
            pub.sendMessage('request_insert_{0:s}'.format(
                self._module.lower()),
                            parent_id=self._parent_id)

    def do_request_insert_child(self, __button: Gtk.ToolButton,
                                **kwargs: Any) -> Any:
        """
        Request to insert a new child entity of the selected entity.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.selection.get_selected()
        self._parent_id = _model.get_value(_row, self._lst_col_order[1])

        return self.do_request_insert(sibling=False, **kwargs)

    def do_request_insert_sibling(self, __button: Gtk.ToolButton,
                                  **kwargs: Any) -> Any:
        """
        Send request to insert a new sibling entity.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        # If the sibling is nested below the top level, get the parent ID from
        # the previous row.  Otherwise, this is a top level item and the parent
        # ID is zero.
        try:
            _model, _row = self.treeview.selection.get_selected()
            _prow = _model.iter_parent(_row)
            self._parent_id = _model.get_value(_prow, self._lst_col_order[1])
        except TypeError as _error:
            self._parent_id = 0
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return self.do_request_insert(sibling=True, **kwargs)

    def do_set_cursor(self, cursor: Gdk.CursorType) -> None:
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
        self.get_parent_window().set_cursor(Gdk.Cursor.new(cursor))
        Gdk.flush()

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_set_cursor_active(self, node_id: Any) -> None:
        """
        Set the active cursor for the Module, List, and Work Book Gdk.Window().

        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def do_set_cursor_busy(self) -> None:
        """
        Set the busy cursor for the Module, List, and Work Book Gdk.Window().

        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)

    def on_button_press(self, event: Gdk.Event, **kwargs: Any) -> None:
        """
        Handle mouse clicks on the View's RTKTreeView().

        :param event: the Gdk.Event() that called this method (the important
        attribute is which mouse button was clicked).

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
        _menu.popup_at_pointer(event)

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

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_delete(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Update the RAMSTKTreeView after deleting a line item.

        :param int node_id: the treelib Tree() node ID that was deleted.
        :param tree: the treelib Tree() containing the workflow module data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.selection.get_selected()
        _model.remove(_row)

        _row = _model.get_iter_first()
        if _row is not None:
            self.treeview.selection.select_iter(_row)
            self.show_all()

    # noinspection PyUnboundLocalVariable
    def on_focus_out(self, entry: Any, index: int, module_id: int,
                     message: str) -> None:
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
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text: Any = int(entry.get_text())
        except ValueError as _error:
            try:
                _new_text = float(entry.get_text())
            except ValueError as _error:
                try:
                    _new_text = str(entry.get_text())
                except ValueError as _error:
                    _new_text = None
                    self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        entry.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(message,
                        node_id=module_id,
                        package={_key: _new_text})

    def on_insert(self, data: Any) -> None:
        """
        Add row to module view for newly added work stream element.

        :param data: the data package for the work stream element to add.
        :return: None
        :rtype: None
        """
        _attributes = []
        _model, _row = self.treeview.selection.get_selected()

        try:
            if self._record_id == self._parent_id:
                _prow = _row
            else:
                _prow = _model.iter_parent(_row)
        except TypeError:
            _prow = None

        for _key in self.treeview.korder:
            if _key == 'dict':
                _attributes.append(str(data))
            else:
                try:
                    if isinstance(data[_key], datetime.date):
                        data[_key] = data[_key].strftime("%Y-%m-%d")
                    data[_key] = data[_key].decode('utf-8')
                except (AttributeError, KeyError) as _error:
                    self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

                _attributes.append(data[_key])

        _row = _model.append(_prow, _attributes)

        self.treeview.selection.select_iter(_row)

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        """
        Common method for views to use for RAMSTKTreeView() row changes.

        :param selection: the current Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: _attributes; the dict containing the record's attributes.
        :rtype: dict
        """
        _attributes: Dict[str, Any] = {}

        selection.handler_block(self._lst_handler_id[0])

        _model, _row = selection.get_selected()
        if _row is not None:
            for _key in self._dic_key_index:
                _attributes[_key] = _model.get_value(
                    _row, self._lst_col_order[self._dic_key_index[_key]])

        return _attributes

    def on_select_revision(self, attributes: Dict[str, Any]) -> None:
        """
        Set the Revision ID when a new Revision is selected.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']


class RAMSTKListView(RAMSTKBaseView):
    """
    Class to display list and matrix type data in the RAMSTK List Book.

    This is the meta class for all RAMSTK List View classes.  Attributes of the
    RAMSTKListView are:

    :ivar str _matrix_type: the name of the matrix displayed by this view.
    :ivar str _module: the capitalized name of the RAMSTK module the List View
        is associated with.
    :ivar int _n_columns: the number of columns in a matrix.
    :ivar int _n_rows: the number of rows in a matrix.
    :ivar matrix: the Pandas DataFrame() containing the matrix data.
    :ivar matrix: :class:`Pandas.DataFrame`
    :ivar matrixview: the MatrixView() displaying the matrix data.
    :type matrixview: :class:`ramstk.views.gtk3.widgets.RAMSTKMatrixView`
    :ivar int n_fixed_columns: the number of matrix columns on the left that
        contain fixed data.
    :ivar tab_label: the Gtk.Label() displaying text for the List View tab.
    :type tab_label: :class:`Gtk.Label`
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = '') -> None:
        """
        Initialize the List View.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            module,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        self._module: str = ''
        for __, char in enumerate(module):
            if char.isalpha():
                self._module = module.capitalize()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.matrixview: RAMSTKMatrixView = RAMSTKMatrixView(module=module)
        self.tab_label: Gtk.Label = Gtk.Label()

        self.__set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_matrix, 'succeed_load_matrix')

    def __set_properties(self) -> None:
        """
        Set common properties of the ListView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_rubber_banding(True)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Send request to update the matrix."""
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type=self._module.lower())

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Send request to update the matrix."""
        self._do_request_update(__button)

    def do_load_matrix(self, matrix_type: str, matrix: pd.DataFrame) -> None:
        """
        Load the RAMSTKMatrixView() with matrix data.

        :param str matrix_type: the type of matrix to load.
        :param matrix: the data matrix to display.
        :return: None
        :rtype: None
        """
        if matrix_type.capitalize() == self._module:
            self.matrixview.do_load_matrix(matrix)

    def make_ui(self, vtype: str = 'list', **kwargs) -> None:
        """
        Build the list view user interface.

        :param str vtype: the type of view to create; 'list' (default) or
            'matrix'.
        :return: None
        :rtype: None
        """
        try:
            _tab_label = kwargs['tab_label']
        except KeyError:
            _tab_label = 'Tab'
        try:
            _tooltip = kwargs['tooltip']
        except KeyError:
            _tooltip = _("Missing tooltip, please file a quality type issue "
                         "to have one added.")

        self.tab_label.set_markup("<span weight='bold'>" + _tab_label
                                  + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(_tooltip)

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(do_make_buttonbox(self, **kwargs))
        self.pack_start(_scrolledwindow, False, False, 0)

        self.hbx_tab_label.pack_end(self.tab_label, True, True, 0)
        self.hbx_tab_label.show_all()

        _scrolledwindow = Gtk.ScrolledWindow()
        if vtype == 'matrix':
            self.matrixview.dic_icons = {
                'complete':
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                + '/32x32/complete.png',
                'none':
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                + '/32x32/none.png',
                'partial':
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
                + '/32x32/partial.png'
            }
            self.matrixview.set_tooltip_text(_tooltip)
            _scrolledwindow.add(self.matrixview)
        else:
            self.treeview.set_tooltip_text(_tooltip)
            _scrolledwindow.add(self.treeview)

        self.pack_end(_scrolledwindow, True, True, 0)

        self.show_all()

    def on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                     position: int) -> None:
        """
        Handle edits of the List View RAMSTKTreeView().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _type = GObject.type_name(_model.get_column_type(position))
        if _type == 'gchararray':
            _model[path][position] = str(new_text)
        elif _type == 'gint':
            _model[path][position] = int(new_text)
        elif _type == 'gfloat':
            _model[path][position] = float(new_text)


class RAMSTKModuleView(RAMSTKBaseView):
    """
    Display data in the RAMSTK Module Book.

    This is the meta class for all RAMSTK Module View classes.  Attributes of
    the RAMSTKModuleView are:

    :ivar _img_tab: the :class:`Gtk.Image` to display on the tab.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = '') -> None:
        """
        Initialize the RAMSTKModuleView meta-class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module)

        # Initialize private dictionary attributes.
        self._dic_icons['insert_part'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/insert_part.png')

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._img_tab = Gtk.Image()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()

    def __set_properties(self) -> None:
        """
        Set common properties of the ModuleView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_rubber_banding(True)

    def do_request_export(self, module: str) -> None:
        """
        Launch the Export assistant.

        :return: None
        :rtype: None
        """
        # _tree = self._dtc_data_controller.request_do_select_all(
        #     revision_id=self._revision_id)
        # ExportModule(self._mdcRAMSTK, module, _tree)

    def make_ui(self, icons: List[str], tooltips: List[str],
                callbacks: List[object]) -> None:
        """
        Build the user interface.

        :param icons: the list of icons to display on the toolbar, if any,
            in addition to the default Save and Save All.  Pass an empty list
            if there are no additional buttons.
        :param tooltips: the list of tooltip strings for the extra buttons.
            Pass an empty list if there are no additional buttons.
        :param callbacks: the list of callback functions for each extra button.
              Pass an empty list if there are no additional buttons.
        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            do_make_buttonbox(self,
                              icons=icons,
                              tooltips=tooltips,
                              callbacks=callbacks))
        self.pack_start(_scrolledwindow, False, False, 0)

        self.treeview.set_tooltip_text(
            _("Displays the list of {0:s}s.").format(self._module))

        self._img_tab.set_from_file(self._dic_icons['tab'])

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)
        self.pack_end(_scrolledwindow, True, True, 0)

        self.hbx_tab_label.pack_start(self._img_tab, True, True, 0)
        self.hbx_tab_label.show_all()

        _label = RAMSTKLabel(_("{0:s}").format(self._module.capitalize()))
        _label.do_set_properties(width=-1,
                                 height=-1,
                                 tooltip=_("Displays the program "
                                           "{0:s}s.").format(self._module))
        self.hbx_tab_label.pack_end(_label, True, True, 0)

        self.show_all()

        self.treeview.do_set_editable_columns(self._on_cell_edit)

    def on_button_press(self, event: Gdk.Event, **kwargs: Any) -> None:
        """
        Handle mouse clicks on the Module View RAMSTKTreeView().

        :param event: the Gdk.Event() that called this method (the
            important attribute is which mouse button was clicked).
                * 1 = left
                * 2 = scrollwheel
                * 3 = right
                * 4 = forward
                * 5 = backward
                * 8 =
                * 9 =
        :type event: :class:`Gdk.Event`
        :return: None
        :rtype: None
        """
        _icons = kwargs['icons']
        _labels = kwargs['labels']
        _callbacks = kwargs['callbacks']

        # Append the default save and save-all buttons found on all Module View
        # pop-up menus.
        try:
            _icons.extend(['remove', 'save', 'save-all'])
            _callbacks.extend([
                self._do_request_delete, self._do_request_update,
                self._do_request_update_all
            ])
        except AttributeError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        RAMSTKBaseView.on_button_press(self,
                                       event,
                                       icons=_icons,
                                       labels=_labels,
                                       callbacks=_callbacks)


class RAMSTKWorkView(RAMSTKBaseView):
    """
    Class to display data in the RAMSTK Work Book.

    This is the meta class for all RAMSTK Work View classes.  Attributes of the
    RAMSTKWorkView are:

    :ivar str _module: the all capitalized name of the RAMSKT module the View
    is for.
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = '') -> None:
        """
        Initialize the RAMSTKWorkView meta-class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_widgets: List[object] = []

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')

    def make_toolbuttons(self, **kwargs: Any) -> None:
        """
        Common method to create the WorkView tool buttons.

        :return: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(do_make_buttonbox(
            self, **kwargs))
        self.pack_start(_scrolledwindow, False, False, 0)

    def make_ui(self, **kwargs: Any) -> Tuple[int, List[int], Gtk.Fixed]:
        """
        Common method to create work view Gtk.Notebook() general data pages.

        :return: (_x_pos, _y_pos, _fixed); the x-position of the left edge of
            each widget, the list of y-positions of the top of each widget, and
            the Gtk.Fixed() that all the widgets are placed on.
        :rtype: (int, list, :class:`Gtk.Fixed`)
        """
        try:
            _index_end = kwargs['end']
        except KeyError:
            _index_end = len(self._lst_labels)
        try:
            _index_start = kwargs['start']
        except KeyError:
            _index_start = 0
        try:
            _y_inc = kwargs['y_inc']
        except KeyError:
            _y_inc = 25

        # TODO: See issue #304.
        if self._lst_widgets:
            _fixed = Gtk.Fixed()

            _y_pos = 5
            (_x_pos, _lst_labels) = do_make_label_group2(
                self._lst_labels[_index_start:_index_end], x_pos=5, y_pos=5)
            for _idx, _label in enumerate(_lst_labels):
                _minimum: Gtk.Requisition = self._lst_widgets[
                    _idx + _index_start].get_preferred_size()[0]
                if _minimum.height == 0:
                    _minimum.height = self._lst_widgets[_idx
                                                        + _index_start].height

                _fixed.put(_label, 5, _y_pos)
                # RAMSTKTextViews are placed inside a scrollwindow so that's
                # what needs to be placed on the container.
                if isinstance(self._lst_widgets[_idx + _index_start],
                              RAMSTKTextView):
                    _fixed.put(
                        self._lst_widgets[_idx + _index_start].scrollwindow,
                        _x_pos + 5, _y_pos)
                    _y_pos += _minimum.height + 30
                else:
                    _fixed.put(self._lst_widgets[_idx + _index_start],
                               _x_pos + 5, _y_pos)
                    _y_pos += _minimum.height + 5
        else:
            self.make_toolbuttons(**kwargs)

            _fixed = Gtk.Fixed()

            _scrollwindow = RAMSTKScrolledWindow(_fixed)
            _frame = RAMSTKFrame()
            _frame.do_set_properties(title=_("General Information"))
            _frame.add(_scrollwindow)

            self.pack_start(_frame, True, True, 0)

            _x_pos, _y_pos = do_make_label_group(self._lst_labels,
                                                 _fixed,
                                                 5,
                                                 5,
                                                 y_inc=_y_inc)
            _x_pos += 50

            _fixed.put(self.txtCode, _x_pos, _y_pos[0])
            _fixed.put(self.txtName, _x_pos, _y_pos[1])

        return _x_pos, _y_pos, _fixed

    def on_edit(self, node_id: List, package: Dict[str, Any]) -> None:
        """
        Update the Work View Gtk.Widgets() when attributes change.

        This method is called whenever an attribute is edited in a different
        view.

        :param int module_id: the ID of the Hardware being edited.  This
            parameter is required to allow the PyPubSub signals to call this
            method and the request_set_attributes() method in the
            RAMSTKDataController.
        :param int index: the index in the Hardware attributes list of the
            attribute that was edited.
        :param str value: the new text to update the Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        _module_id = node_id[0]
        [[_key, _value]] = package.items()

        (_function, _id) = self._dic_switch.get(_key)
        _function(_value, self._lst_handler_id[_id])

    def on_toggled(self, checkbutton: RAMSTKCheckButton, index: int,
                   **kwargs) -> None:
        """
        Common method to respond to work view checkbutton 'toggles'.

        :param checkbutton: the Gtk.CheckButton() that was toggled.
        :param index: the index of the Gtk.CheckButton() in the list handler
            list.
        :return: None
        """
        _message = kwargs['message']
        _keys = kwargs['keys']
        try:
            _key = _keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        checkbutton.handler_block(self._lst_handler_id[index])

        _new_text = int(checkbutton.get_active())

        pub.sendMessage(_message,
                        node_id=[self._record_id, -1, ''],
                        package={_key: _new_text})
