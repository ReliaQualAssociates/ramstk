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
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, _

# RAMSTK Local Imports
from .button import do_make_buttonbox
from .dialog import RAMSTKMessageDialog
from .frame import RAMSTKFrame
from .label import RAMSTKLabel, do_make_label_group
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

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module: str) -> None:
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
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons = self.__set_icons()

        # Initialize private list attributes.
        self._lst_col_order: List[int] = []
        self._lst_handler_id: List[int] = []

        # Initialize private scalar attributes.
        self._mission_time = float(self.RAMSTK_USER_CONFIGURATION.RAMSTK_MTIME)
        self._module: str = module
        self._notebook = Gtk.Notebook()
        self._revision_id = 0
        self._parent_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.treeview = self._make_treeview(module)
        self.fmt = ('{0:0.'
                    + str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES)
                    + 'G}')
        self.hbx_tab_label = Gtk.HBox()

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
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        try:
            self._lst_handler_id.append(
                self.treeview.connect('button_press_event',
                                      self._on_button_press))
        except AttributeError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def __set_icons(self) -> Dict:
        """
        Set the dict of icons.

        :return: the dict of icons to use in RAMSTK.
        :rtype: dict
        """
        return {
            'calculate':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/calculate.png',
            'calculate_all':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/calculate-all.png',
            'add':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/add.png',
            'remove':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/remove.png',
            'reports':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/reports.png',
            'save':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/save.png',
            'save-all':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/save-all.png',
            'important':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/important.png',
            'error':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/error.png',
            'question':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/question.png',
            'insert_sibling':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/insert_sibling.png',
            'insert_child':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/insert_child.png',
            'cancel':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/cancel.png',
            'export':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/export.png',
            'warning':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/warning.png',
            'rollup':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/rollup.png'
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
                _bg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[module
                                                                         + 'bg']
                _fg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[module
                                                                         + 'fg']
            except KeyError as _error:
                _bg_color = '#000000'
                _fg_color = '#FFFFFF'
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

            _treeview.make_model(_bg_color, _fg_color)

        except KeyError as _error:
            _treeview = Gtk.TreeView()
            _treeview.selection = _treeview.get_selection()
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

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
            if kwargs['error_code'] != 0:
                _dialog = RAMSTKMessageDialog(
                    kwargs['user_msg'],
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
            self.RAMSTK_LOGGER.do_log_debug(__name__, kwargs['debug_msg'])
        except KeyError as _error:
            _debug_msg = ''
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def do_refresh_tree(self, package: Dict, keys: Dict) -> None:
        """
        Update the module view RAMSTKTreeView() with attribute changes.

        This method is called by other views when the work stream module's data
        model attributes are edited via their gtk.Widgets().

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
            pub.sendMessage('request_insert_{0:s}'.format(self._module))
        else:
            pub.sendMessage('request_insert_{0:s}'.format(self._module),
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
        _model, _row = self.treeview.selection.get_selected()
        _prow = _model.iter_parent(_row)
        # If the sibling is nested below the top level, get the parent ID from
        # the previous row.  Otherwise, this is a top level item and the parent
        # ID is zero.
        try:
            self._parent_id = _model.get_value(_prow, self._lst_col_order[1])
        except TypeError as _error:
            self._parent_id = 0
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return self.do_request_insert(sibling=True, **kwargs)

    def do_set_cursor(self, cursor: Gdk.CursorType) -> Any:
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

    def on_delete(self, tree: treelib.Tree) -> None:  # pylint: disable=unused-argument
        """
        Update the RAMSTKTreeView after deleting a line item.

        :param tree: the treelib Tree() containing the
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
                        module_id=module_id,
                        key=_key,
                        value=_new_text)

    def on_select(self, **kwargs: Any) -> None:
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
        except AttributeError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return self.do_raise_dialog(severity='warning', **kwargs)

    def on_select_revision(self, attributes: Dict[str, Any]) -> None:
        """
        Set the Revision ID when a new Revision is selected.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']


class RAMSTKListView(RAMSTKBaseView):
    """
    Class to display data in the RAMSTK List Book.

    This is the meta class for all RAMSTK List View classes.  Attributes of the
    RAMSTKListView are:

    :ivar str _module: the capitalized name of the RAMSTK module the List View
        is associated with.
    :ivar tab_label: the Gtk.Label() displaying text for the List View tab.
    :type tab_label: :class:`Gtk.Label`
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module: str) -> None:
        """
        Initialize the List View.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        RAMSTKBaseView.__init__(self, configuration, logger, module)

        self._module = None
        for __, char in enumerate(module):
            if char.isalpha():
                self._module = module.capitalize()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tab_label = Gtk.Label()

        self.__set_properties()

    def __set_properties(self) -> None:
        """
        Set common properties of the ListView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_rubber_banding(True)

    def make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.hbx_tab_label.pack_end(self.tab_label, True, True, 0)
        self.hbx_tab_label.show_all()

        _scrolledwindow = Gtk.ScrolledWindow()
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
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module: str) -> None:
        """
        Initialize the RAMSTKModuleView meta-class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        RAMSTKBaseView.__init__(self, configuration, logger, module)

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

    def make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.treeview.set_tooltip_text(
            _("Displays the list of "
              "{0:s}s.").format(self._module))

        self._img_tab.set_from_file(self._dic_icons['tab'])

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)
        self.pack_end(_scrolledwindow, True, True, 0)

        self.hbx_tab_label.pack_start(self._img_tab, True, True, 0)
        self.hbx_tab_label.show_all()

        _label = RAMSTKLabel(_("{0:s}s").format(self._module.capitalize()))
        _label.do_set_properties(width=-1,
                                 height=-1,
                                 tooltip=_("Displays the program "
                                           "{0:s}s.").format(self._module))
        self.hbx_tab_label.pack_end(_label, True, True, 0)

        self.show_all()

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

    def on_insert(self, data: Any, prow: Gtk.TreeIter = None) -> None:
        """
        Add row to module view for newly added work stream element.

        :param data: the data package for the work stream element to add.
        :param prow: the parent row in the treeview.
        :type prow: :class:`Gtk.TreeIter`
        :return: None
        :rtype: None
        """
        _attributes = []
        _model = self.treeview.get_model()

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

        _row = _model.append(prow, _attributes)

        self.treeview.selection.select_iter(_row)


class RAMSTKWorkView(RAMSTKBaseView):
    """
    Class to display data in the RAMSTK Work Book.

    This is the meta class for all RAMSTK Work View classes.  Attributes of the
    RAMSTKWorkView are:

    :ivar str _module: the all capitalized name of the RAMSKT module the View
    is for.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, module: str) -> None:
        """
        Initialize the RAMSTKWorkView meta-class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module)

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

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')

    def _make_buttonbox(self, **kwargs: Any) -> Gtk.ButtonBox:
        """
        Create the Gtk.ButtonBox() for the Work Views.

        :return: _buttonbox; the Gtk.ButtonBox() for the Work View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _icons = kwargs['icons']
        _tooltips = kwargs['tooltips']
        _callbacks = kwargs['callbacks']

        # do_make_buttonbox always adds the save and save-all options to the
        # end of the list of callbacks, icons, and tooltips that are passed to
        # this method.
        _buttonbox = do_make_buttonbox(self,
                                       icons=_icons,
                                       tooltips=_tooltips,
                                       callbacks=_callbacks,
                                       orientation='vertical',
                                       height=-1,
                                       width=-1)

        return _buttonbox

    def make_ui(self, **kwargs: Any) -> Tuple[int, List[int], Gtk.Fixed]:
        """
        Make the Function class Gtk.Notebook() general data page.

        :return: (_x_pos, _y_pos, _fixed); the x-position of the left edge of
            each widget, the list of y-positions of the top of each widget, and
            the Gtk.Fixed() that all the widgets are placed on.
        :rtype: (int, list, :class:`Gtk.Fixed`)
        """
        _icons = kwargs['icons']
        _tooltips = kwargs['tooltips']
        _callbacks = kwargs['callbacks']

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            self._make_buttonbox(icons=_icons,
                                 tooltips=_tooltips,
                                 callbacks=_callbacks))
        self.pack_start(_scrolledwindow, False, False, 0)

        _fixed = Gtk.Fixed()

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = do_make_label_group(self._lst_labels, _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])

        self.pack_start(_frame, True, True, 0)

        return _x_pos, _y_pos, _fixed
