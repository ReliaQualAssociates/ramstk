# pylint: disable=non-parent-init-called, too-many-public-methods
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
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
# noinspection PyPackageRequirements
import pandas as pd
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GObject, Gtk, _

# RAMSTK Local Imports
from .button import RAMSTKCheckButton, do_make_buttonbox
from .combo import RAMSTKComboBox
from .dialog import RAMSTKMessageDialog
from .entry import RAMSTKTextView
from .frame import RAMSTKFrame
from .label import RAMSTKLabel, do_make_label_group
from .matrixview import RAMSTKMatrixView
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
    # Define private class scalar attributes.
    _pixbuf: bool = False

    # Define public class dict attributes.
    dic_tab_position = {
        'left': Gtk.PositionType.LEFT,
        'right': Gtk.PositionType.RIGHT,
        'top': Gtk.PositionType.TOP,
        'bottom': Gtk.PositionType.BOTTOM
    }

    # Define public class scalar attributes.
    RAMSTK_USER_CONFIGURATION = None

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
        self._parent_id: int = 0
        self._record_id: int = -1
        self._revision_id: int = 0
        self._tree_loaded: bool = False

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
            self.treeview.dic_handler_id[
                'changed'] = self.treeview.selection.connect(
                    'changed', self._on_row_change)
        except AttributeError as _error:
            if self._module in self._lst_layouts:
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        try:
            self.treeview.dic_handler_id[
                'button-press'] = self.treeview.connect(
                    'button_press_event', self._on_button_press)
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
            'action':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/action.png',
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
            'cause':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/cause.png',
            'complete':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/complete.png',
            'control':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/control.png',
            'chart':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/charts.png',
            'edit':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/edit.png',
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
            'mechanism':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/mechanism.png',
            'mode':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/mode.png',
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

    def _make_treeview(self, module: str) -> RAMSTKTreeView:
        """
        Make the RAMSTKTreeView instance for this view.

        :param str module: the name of the module this view is associated with.
        :return: _treeview; the RAMSTKTreeView() created.
        :rtype: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        """
        try:
            _treeview = RAMSTKTreeView()

            _fmt_file = (
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
                + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[module])
            _fmt_path = "/root/tree[@name='" + module.title() + "']/column"
            _treeview.do_parse_format(_fmt_path, _fmt_file, self._pixbuf)

            self._lst_col_order = _treeview.order
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
            _treeview.dic_handler_id = {'': 0}
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

    def do_get_headings(self, level: str) -> List:
        """
        Get the list of headings for the Usage Profile treeview.

        :param level: the level (mission, phase, environment) to retrieve
            headers for.
        :return: list of headings
        :rtype: list
        """
        try:
            _headings = self._dic_headings[level]
        except KeyError:
            _headings = []

        return _headings

    def do_load_row(self, attributes: Dict[str, Any]) -> None:
        """
        Load the data into a row.

        This is used to load data into a RAMSTKTreeView() that is being used in
        a "worksheet" manner.  See the Allocation and Similar Item work views
        for examples.

        :param dict attributes: the Hardware attributes dict for the row to
            be loaded in the WorkView worksheet.
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()

        _data = []
        for _key in self.treeview.korder:
            if _key == 'dict':
                _data.append(str(attributes))
            else:
                _data.append(attributes[_key])

        # Only load items that are immediate children of the selected item and
        # prevent loading the selected item itself in the worksheet.
        if not _data[1] == self._record_id and not self._tree_loaded:
            # noinspection PyDeepBugsSwappedArgs
            _model.append(None, _data)

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
            _user_msg = kwargs['user_msg']
        except KeyError:
            _user_msg = "User message not supplied by calling function."
            _severity = 'error'
        try:
            _severity = kwargs['severity']
        except KeyError:
            _severity = 'error'
        try:
            _parent = kwargs['parent']
        except KeyError:
            _parent = None

        try:
            _dialog = RAMSTKMessageDialog(_user_msg,
                                          self._dic_icons[_severity],
                                          _severity,
                                          parent=_parent)
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

        return _dialog

    def do_refresh_tree(self, package: Dict[str, Any]) -> None:
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
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        try:
            _position = self._lst_col_order[self._dic_key_index[_key]]

            _model, _row = self.treeview.get_selection().get_selected()
            _model.set(_row, _position, _value)
        except KeyError as _error:
            # Not all attributes available on the workview are stored in the
            # moduleview tree.  We log the error in case the offending
            # attribute is supposed to be there and then continue.
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

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

    def do_set_cell_callbacks(self, message: str, columns: List[int]) -> None:
        """
        Set the callback methods for RAMSTKTreeView() cells.

        :param str message: the PyPubSub message to broadcast on a
            successful edit.
        :param list columns: the list of column numbers whose cells should
            have a callback function assigned.
        :return: None
        :rtype: None
        """
        for _idx in columns:
            _cell = self.treeview.get_column(
                self._lst_col_order[_idx]).get_cells()
            try:
                _cell[0].connect('edited', self.on_cell_edit, message, _idx)
            except TypeError:
                _cell[0].connect('toggled', self.on_cell_edit, 'new text',
                                 message, _idx)

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
    def do_set_cursor_active(self, node_id: Any = '') -> None:
        """
        Set the active cursor for the Module, List, and Work Book Gdk.Window().

        :keyword node_id: the node ID passed in the PyPubSub message.  Only
            needed when this method is a PyPubSub subscriber.
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
        self.treeview.handler_block(self.treeview.dic_handler_id['button-press'])

        #// TODO: Add _lst_icons, _lst_callbacks, and _lst_tooltips to GUIs.
        #//
        #// These lists are used in multiple private methods in each GUI
        #// class as well as several public methods in the GUI meta-classes.
        #// Having these lists as class attributes will allow simplifying or
        #// eliminating class methods and likely remove **kwargs from argument
        #// lists for others.  It will also simplify creation of new GUI
        #// classes.
        _icons = kwargs['icons']
        _labels = kwargs['labels']
        _callbacks = kwargs['callbacks']

        _menu = Gtk.Menu()
        _menu.popup_at_pointer(event)

        # pylint: disable=unused-variable
        for _idx, __ in enumerate(_icons):
            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(self._dic_icons[_icons[_idx]])
            _menu_item.set_label(_labels[_idx])
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', _callbacks[_idx],
                               self.RAMSTK_USER_CONFIGURATION)
            _menu_item.show()
            _menu.append(_menu_item)

        self.treeview.handler_unblock(self.treeview.dic_handler_id['button-press'])

    def on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str,
                     message: str, position: int) -> None:
        """
        Handle edits of the Allocation Work View RAMSTKTreeview().

        :param Gtk.CellRenderer cell: the Gtk.CellRenderer() that was edited.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param str message: the PyPubSub message to publish on success.
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        self.treeview.do_edit_cell(cell, path, new_text, position)

        try:
            _key = self._dic_column_keys[self._lst_col_order[position]]
        except (IndexError, KeyError):
            _key = ''

        pub.sendMessage(message,
                        node_id=[self._record_id, -1],
                        package={_key: new_text})

    def on_combo_changed(self, combo: RAMSTKComboBox, index: int,
                         message: str) -> Dict[Union[str, Any], Any]:
        """
        Retrieve RAMSTKCombo() changes and return to the child class.

        This method is called by the child class instance _on_combo_changed()
        methods.  The child class should unblock the RAMSTKComboBox()'s
        handler.  This is to allow the child class to perform other
        manipulations of the RAMSTKComboBox that may be needed besides
        simply reading it's contents (which is the most likely user-case).

        :param combo: the RAMSTKComboBox() that called the child method.
        :type combo: :class:`ramstk.views.widgets.RAMSTKComboBox`
        :param int index: the position in the child class Gtk.TreeModel()
            associated with the data from the calling RAMSTKComboBox().
        :param str message: the PyPubSub message to broadcast.
        :return: {_key: _new_text}; the child module attribute name and the
        index of the newly selected RAMSTKComboBox() item.
        :rtype: dict
        """
        combo.handler_block(combo.dic_handler_id['changed'])

        try:
            _key: str = self._dic_keys[index]
        except KeyError as _error:
            # TODO: Raise warning dialogs per convention 308.1.
            #
            #  Do this for all workviews.
            #
            #  Warning dialogs for exceptions potentially resulting from user
            #  error per convention 308.1 need to be implemented in all views.
            #  See issue #308.
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        try:
            _new_text: int = int(combo.get_active())
        except ValueError as _error:
            _new_text = 0
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        try:
            # Only if something is selected should we send the message.
            # Otherwise attributes get updated to a value of -1 which isn't
            # correct.  And it sucks trying to figure out why, so leave the
            # conditional unless you have a more elegant (and there prolly
            # is) solution.
            if _new_text > -1:
                pub.sendMessage(message,
                                node_id=[self._record_id, -1],
                                package={_key: _new_text})
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        combo.handler_unblock(combo.dic_handler_id['changed'])

        return {_key: _new_text}

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
    def on_focus_out(self, entry: object, index: int,
                     message: str) -> Dict[Union[str, Any], Any]:
        """
        Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        The child class calling this method should unblock the signal in
        case there is anything else the child class needs to do with the
        RAMSTKEntry() or RAMSTKTextView() that called this method.

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
            method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
        :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
            associated with the data from the calling Gtk.Widget().
        :param str message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the child module attribute name and the
            index of the newly changed RAMSTKEntry() or RAMSTKTextView().
        :rtype: dict
        """
        entry.handler_block(entry.dic_handler_id['changed'])

        try:
            _key = self._dic_keys[index][0]
            _type = self._dic_keys[index][1]
        except KeyError as _error:
            _key = ''
            _type = 'string'
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        if _type == 'float':
            _new_text: Any = float(entry.get_text())
        elif _type == 'integer':
            _new_text = int(entry.get_text())
        elif _type == 'string':
            _new_text = str(entry.get_text())

        pub.sendMessage(message,
                        node_id=[self._record_id, -1],
                        package={_key: _new_text})

        entry.handler_unblock(entry.dic_handler_id['changed'])

        return {_key: _new_text}

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
        selection.handler_block(self.treeview.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = {}

        _model, _row = selection.get_selected()
        if _row is not None:
            #// TODO: Update base view on_row_change() to use _dic_column_keys.
            #//
            #// The _dic_key_index and _dic_column_keys are both
            #// dictionaries with the object's attribute name (str) as the key
            #// and the associated work flow column number (int) as the
            #// value.  Only one is needed; the _dic_column_keys is more
            #// widely used and is more descriptive of what the dict holds.
            for _key in self._dic_key_index:
                _attributes[_key] = _model.get_value(
                    _row, self._lst_col_order[self._dic_key_index[_key]])

        try:
            self._record_id = _attributes['hardware_id']
        except KeyError:
            self._record_id = -1

        selection.handler_unblock(self.treeview.dic_handler_id['changed'])

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
        # pylint: disable=unused-variable
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

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_matrix, 'succeed_load_matrix')

    def do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Send request to update the matrix."""
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type=self._module.lower())

    def do_request_update_all(self, __button: Gtk.ToolButton) -> None:
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
        self.tab_label.set_xalign(0.5)
        self.tab_label.set_yalign(0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(_tooltip)

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add(do_make_buttonbox(self, **kwargs))
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

        self.treeview.do_set_editable_columns(self.on_cell_edit)

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

    def do_clear_tree(self) -> None:
        """
        Clear the contents of a RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _columns = self.treeview.get_columns()
        for _column in _columns:
            self.treeview.remove_column(_column)

        _model.clear()

    def make_toolbuttons(self, **kwargs: Any) -> None:
        """
        Common method to create the WorkView tool buttons.

        :return: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(do_make_buttonbox(self, **kwargs))
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

        _fixed = Gtk.Fixed()

        _y_pos = 5
        (_x_pos, _lst_labels) = do_make_label_group(
            self._lst_labels[_index_start:_index_end], x_pos=5, y_pos=5)
        for _idx, _label in enumerate(_lst_labels):
            _minimum: Gtk.Requisition = self._lst_widgets[
                _idx + _index_start].get_preferred_size()[0]
            if _minimum.height == 0:
                _minimum.height = self._lst_widgets[_idx + _index_start].height

            _fixed.put(_label, 5, _y_pos)
            # RAMSTKTextViews are placed inside a scrollwindow so that's
            # what needs to be placed on the container.
            if isinstance(self._lst_widgets[_idx + _index_start],
                          RAMSTKTextView):
                _fixed.put(self._lst_widgets[_idx + _index_start].scrollwindow,
                           _x_pos + 5, _y_pos)
                _y_pos += _minimum.height + 30
            else:
                _fixed.put(self._lst_widgets[_idx + _index_start], _x_pos + 5,
                           _y_pos)
                _y_pos += _minimum.height + 5

        return _fixed

    def make_ui_with_treeview(self, title: List[str]) -> None:
        """
        Build the work view UI containing a RAMSTKTreeView().

        :param list title: the list of titles for the two RAMSTKFrame()s
            used in this view.
        :return: None
        :rtype: None
        """
        # TMPLT: Use this method to create a work view layout like this:
        # TMPLT:
        # TMPLT: +-----+-----+---------------------------------+
        # TMPLT: |  B  |  W  |                                 |
        # TMPLT: |  U  |  I  |                                 |
        # TMPLT: |  T  |  D  |                                 |
        # TMPLT: |  T  |  G  |          SPREAD SHEET           |
        # TMPLT: |  O  |  E  |                                 |
        # TMPLT: |  N  |  T  |                                 |
        # TMPLT: |  S  |  S  |                                 |
        # TMPLT: +-----+-----+---------------------------------+
        # TMPLT:                                      buttons -----+--> self
        # TMPLT:                                                   |
        # TMPLT:     Gtk.Fixed --->RAMSTKFrame ---+-->Gtk.HBox ----+
        # TMPLT:                                  |
        # TMPLT:  Scrollwindow --->RAMSTKFrame ---+
        # TMPLT:  w/ self.treeview
        # TMPLT:
        # TMPLT: The overall view is created by a call to make_toolbuttons()
        # TMPLT: from the child class' __make_ui() method followed by a call
        # TMPLT: to this method.
        _hbox = Gtk.HBox()

        _fixed = Gtk.Fixed()
        _y_pos = 5
        for _idx, _label in enumerate(self._lst_labels):
            _fixed.put(RAMSTKLabel(_label), 5, _y_pos)
            _fixed.put(self._lst_widgets[_idx], 5, _y_pos + 25)

            _y_pos += 65

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=title[0])
        _frame.add(_fixed)

        _hbox.pack_start(_frame, False, True, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                 Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=title[1])
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True, 0)
        self.pack_end(_hbox, True, True, 0)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """
        Update the Work View Gtk.Widgets() when attributes change.

        This method is called whenever an attribute is edited in the module
        view.

        :param list node_id: the list of IDs of the item being edited.  This
            parameter is required to allow the PyPubSub signals to call this
            method and the request_set_attributes() method in the
            RAMSTKDataController.
        :param dict package: the index in the module attributes list of the
            attribute that was edited and the new text to update the
            Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        (_function, _signal) = self._dic_switch.get(_key)
        _function(_value, _signal)

    def on_toggled(self, checkbutton: RAMSTKCheckButton, index: int,
                   message: str) -> None:
        """
        Common method to respond to work view checkbutton 'toggles'.

        :param checkbutton: the Gtk.CheckButton() that was toggled.
        :type checkbutton: :class:`Gtk.CheckButton`
        :param int index: the index of the Gtk.CheckButton() in the list
        handler list.
        :param str message: the PyPubSub message to broadcast.
        :return: None
        """
        try:
            _key = self._dic_keys[index]
        except KeyError as _error:
            _key = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        _new_text = int(checkbutton.get_active())

        checkbutton.do_update(_new_text, signal='toggled')

        pub.sendMessage(message,
                        node_id=[self._record_id, -1, ''],
                        package={_key: _new_text})
