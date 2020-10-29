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
from typing import Any, Dict, List, Tuple

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
from .button import do_make_buttonbox
from .dialog import RAMSTKMessageDialog
from .label import RAMSTKLabel
from .matrixview import RAMSTKMatrixView
from .panel import RAMSTKPanel
from .treeview import RAMSTKTreeView


# noinspection PyUnresolvedReferences
class RAMSTKBaseView(Gtk.HBox):
    """Meta class for all RAMSTK ListView, ModuleView, and WorkView classes.

    Attributes of the RAMSTKBaseView are:

    :cvar RAMSTK_USER_CONFIGURATION: the instance of the RAMSTK Configuration
        class.
    :cvar dic_tab_position: dictionary holding the Gtk.PositionType()s for
        each of left, right, top, and bottom.

    The following attributes are used to build toolbars and pop-up menus:

    :ivar _dic_icons: dictionary containing icon name and absolute path
        key:value pairs.

    :ivar _lst_callbacks: the list of callback functions to associate with
        toolbutton items and pop-up menu entries on a view.
    :ivar _lst_icons: the list of icon names (keys) in the _dic_icons
        dictionary to use for each toolbutton item and pop-up menu entry.
    :ivar _lst_mnu_labels: the list of labels to use on pop-up menu entries
        for a view.  These are generally only used for views with a
        RAMSTKTreeView().
    :ivar _lst_tooltips: the list of tooltips to associate with each
        toolbutton item.

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
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = None

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the RAMSTK Base View.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        GObject.GObject.__init__(self)

        self.RAMSTK_USER_CONFIGURATION = configuration
        self.RAMSTK_LOGGER = logger
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons: Dict[str, str] = self.__set_icons()

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = []
        self._lst_icons: List[str] = []
        self._lst_mnu_labels: List[str] = []
        self._lst_tooltips: List[str] = []

        self._lst_col_order: List[int] = []
        self._lst_handler_id: List[int] = []
        self._lst_layouts: List[str] = [
            'allocation', 'failure_definition', 'fmea', 'function', 'hardware',
            'hazard', 'incident', 'pof', 'requirement', 'revision',
            'similar_item', 'software', 'stakeholder', 'testing', 'validation'
        ]

        # Initialize private scalar attributes.
        self._img_tab: Gtk.Image = Gtk.Image()
        self._mission_time: float = float(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MTIME)
        self._notebook: Gtk.Notebook = Gtk.Notebook()
        self._parent_id: int = 0
        self._pnlPanel: RAMSTKPanel = RAMSTKPanel()
        self._record_id: int = -1
        self._revision_id: int = 0
        self._tree_loaded: bool = False

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.treeview: RAMSTKTreeView = self._make_treeview()
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
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_matrix')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_update_matrix')

    def __set_callbacks(self) -> None:
        """Set common callback methods.

        Sets callback for the RAMSTKView, Gtk.TreeView, and Gtk.TreeSelection.

        :return: None
        :rtype: None
        """
        try:
            self.treeview.dic_handler_id[
                'button-press'] = self.treeview.connect(
                    'button_press_event', self.on_button_press)
        except AttributeError as _error:
            if self._module in self._lst_layouts:
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def __set_icons(self) -> Dict[str, str]:
        """Set the dict of icons.

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
            'environment':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/environment.png',
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
            'mission':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/mission.png',
            'mode':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/mode.png',
            'none':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/none.png',
            'opload':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/load.png',
            'opstress':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/stress.png',
            'partial':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/partial.png',
            'phase':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/phase.png',
            'plot':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/charts.png',
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
            'save-layout':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/save-layout.png',
            'testmethod':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/method.png',
            'warning':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/warning.png'
        }

    def _make_treeview(self) -> RAMSTKTreeView:
        """Make the RAMSTKTreeView instance for this view.

        :return: _treeview; the RAMSTKTreeView() created.
        :rtype: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        """
        try:
            _treeview = RAMSTKTreeView()

            _fmt_file = (self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR
                         + '/layouts/'
                         + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[
                             self._module])

            _treeview.do_parse_format(_fmt_file)
            self._lst_col_order = list(_treeview.position.values())
            try:
                _bg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                    self._module + 'bg']
                _fg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                    self._module + 'fg']
            except KeyError as _error:
                _bg_color = '#FFFFFF'
                _fg_color = '#000000'
                if self._module in self._lst_layouts:
                    self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

            _treeview.do_make_model()
            _treeview.do_make_columns(colors={
                'bg_color': _bg_color,
                'fg_color': _fg_color
            })
            _treeview.do_set_editable_columns(_treeview.do_edit_cell)
        except KeyError as _error:
            _treeview = Gtk.TreeView()
            _treeview.selection = _treeview.get_selection()
            _treeview.dic_handler_id = {'': 0}
            if self._module in self._lst_layouts:
                self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        _treeview.set_grid_lines(3)
        _treeview.set_enable_tree_lines(True)
        _treeview.set_level_indentation(2)

        return _treeview

    def do_embed_matrixview_panel(self) -> None:
        """Embed a matrixview RAMSTKPanel() into the layout.

        :return: None
        """
        self.matrixview.dic_icons = {
            'complete':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/complete.png',
            'none':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/none.png',
            'partial':
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/partial.png'
        }
        self.matrixview.set_tooltip_text(self._tabtooltip)

        self._pnlPanel.do_make_panel_matrixview(self.matrixview)

        self.pack_end(self._pnlPanel, True, True, 0)

        self.show_all()

    def do_embed_treeview_panel(self) -> None:
        """Embed a treeview RAMSTKPanel() into the layout.

        :return: None
        """
        _fmt_file = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
            + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[self._module])

        try:
            _bg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                self._module + 'bg']
            _fg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                self._module + 'fg']
        except KeyError:
            _bg_color = '#FFFFFF'
            _fg_color = '#000000'

        self._pnlPanel.do_make_treeview(bg_color=_bg_color,
                                        fg_color=_fg_color,
                                        fmt_file=_fmt_file)

        self.pack_end(self._pnlPanel, True, True, 0)

        self.show_all()

    def do_expand_tree(self) -> None:
        """Expand the RAMSTKTreeView.

        :return: None
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
        """Get the list of headings for the Usage Profile treeview.

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
        """Load the data into a row.

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
            _data.append(attributes[self.treeview.korder[_key]])

        # Only load items that are immediate children of the selected item and
        # prevent loading the selected item itself in the worksheet.
        if not _data[1] == self._record_id and not self._tree_loaded:
            # noinspection PyDeepBugsSwappedArgs
            _model.append(None, _data)

    def do_load_tree(self, tree: treelib.Tree) -> None:
        """Load the RAMSTK View RAMSTKTreeView().

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
                "An error occurred while loading {1:s} records for Revision "
                "ID {0:d} into the view.  One or more values from the "
                "database was the wrong type for the column it was trying to "
                "load.").format(self._revision_id, _tag)
            self.RAMSTK_LOGGER.do_log_error(__name__, _error_msg)
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
        except ValueError as _error:
            _error_msg = _(
                "An error occurred while loading {1:s} records for Revision "
                "ID {0:d} into the view.  One or more values from the "
                "database was missing.").format(self._revision_id, _tag)
            self.RAMSTK_LOGGER.do_log_error(__name__, _error_msg)
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def do_make_layout(self) -> None:
        """Create a view with the following layout.

        +-----+---------------------------------------+
        |  B  |                WIDGETS                |
        |  U  |                                       |
        |  T  |                                       |
        |  T  |                                       |
        |  O  |                                       |
        |  N  |                                       |
        |  S  |                                       |
        +-----+---------------------------------------+
        self.make_toolbuttons -------> self

        :return: None
        :rtype: None
        """
        self.make_tab_label(tablabel=self._tablabel, tooltip=self._tabtooltip)
        self.make_toolbuttons(
            icons=self._lst_icons,  # type: ignore
            tooltips=self._lst_tooltips,  # type: ignore
            callbacks=self._lst_callbacks)  # type: ignore

    def do_make_layout_lr(self) -> Gtk.HPaned:
        """Create a view with the following layout.

        +-----+-------------------+-------------------+
        |  B  |      L. SIDE      |      R. SIDE      |
        |  U  |                   |                   |
        |  T  |                   |                   |
        |  T  |                   |                   |
        |  O  |                   |                   |
        |  N  |                   |                   |
        |  S  |                   |                   |
        +-----+-------------------+-------------------+
        self.make_toolbuttons -----+--> self
                                   |
                      _hpaned -----+

        :return: _hpaned; the Gtk.HPaned() that creates the left and right
            sides for further population.
        :rtype: :class:`Gtk.Hpaned`
        """
        self.do_make_layout()

        _hpaned: Gtk.HPaned = Gtk.HPaned()

        self.pack_start(_hpaned, True, True, 0)

        return _hpaned

    def do_make_layout_lrr(self) -> Tuple[Gtk.HPaned, Gtk.VPaned]:
        """Create a view with the following layout.

        +-----+-------------------+-------------------+
        |  B  |      L. SIDE      |      R. TOP       |
        |  U  |                   |                   |
        |  T  |                   |                   |
        |  T  |                   +-------------------+
        |  O  |                   |     R. BOTTOM     |
        |  N  |                   |                   |
        |  S  |                   |                   |
        +-----+-------------------+-------------------+
           self.make_toolbuttons  -----+--> self
                                       |
        _vpaned_right -----> _hpaned --+

        :return: (_hpaned, _vpaned_right); the Gtk.HPaned() and Gtk.Vpaned()
            that create the left and right sections for further population.
        :rtype: tuple
        """
        self.do_make_layout()

        _hpaned: Gtk.HPaned = Gtk.HPaned()
        _vpaned_right: Gtk.VPaned = Gtk.VPaned()

        _hpaned.pack2(_vpaned_right, True, True)

        self.pack_start(_hpaned, True, True, 0)

        return _hpaned, _vpaned_right

    def do_make_layout_llr(self) -> Tuple[Gtk.HPaned, Gtk.VPaned]:
        """Create a view with the following layout.

        +-----+-------------------+-------------------+
        |  B  |       L. TOP      |     R. SIDE       |
        |  U  |                   |                   |
        |  T  |                   |                   |
        |  T  +-------------------+                   |
        |  O  |     L. BOTTOM     |                   |
        |  N  |                   |                   |
        |  S  |                   |                   |
        +-----+-------------------+-------------------+
           self.make_toolbuttons  -----+--> self
                                       |
         _vpaned_left -----> _hpaned --+

        :return: (_hpaned, _vpaned_left); the Gtk.HPaned() and Gtk.Vpaned()
            that create the left and right sections for further population.
        :rtype: tuple
        """
        self.do_make_layout()

        _hpaned: Gtk.HPaned = Gtk.HPaned()
        _vpaned_left: Gtk.VPaned = Gtk.VPaned()

        _hpaned.pack1(_vpaned_left, True, True)

        self.pack_start(_hpaned, True, True, 0)

        return _hpaned, _vpaned_left

    def do_make_layout_llrr(self) -> Tuple[Gtk.VPaned, Gtk.VPaned]:
        """Create a view with the following layout.

        +-----+-------------------+-------------------+
        |  B  |       L. TOP      |      R. TOP       |
        |  U  |                   |                   |
        |  T  |                   |                   |
        |  T  +-------------------+-------------------+
        |  O  |     L. BOTTOM     |     R. BOTTOM     |
        |  N  |                   |                   |
        |  S  |                   |                   |
        +-----+-------------------+-------------------+
           self.make_toolbuttons  -----+--> self
                                       |
         _vpaned_left --+--> _hpaned --+
                        |
        _vpaned_right --+

        :return: (_vpaned_left, _vpaned_right); the two Gtk.Vpaned()
            that create the left and right sections for further population.
        :rtype: tuple
        """
        self.do_make_layout()

        _hpaned: Gtk.HPaned = Gtk.HPaned()
        _vpaned_left: Gtk.VPaned = Gtk.VPaned()
        _vpaned_right: Gtk.VPaned = Gtk.VPaned()

        _hpaned.pack1(_vpaned_left, True, True)
        _hpaned.pack2(_vpaned_right, True, True)

        self.pack_start(_hpaned, True, True, 0)

        return _vpaned_left, _vpaned_right

    def do_raise_dialog(self, **kwargs: Any) -> RAMSTKMessageDialog:
        """Raise a dialog in response to information, warnings, and errors.

        This method will display an message dialog of the appropriate severity
        information, warning, or error containing a message to the user.  It
        will also write a message to the RAMSTK debug_log to (hopefully) assist
        in troubleshooting.

        :return: _dialog
        """
        _debug_msg = kwargs.get('debug_msg', '')
        _parent = kwargs.get('parent', None)

        _dialog = RAMSTKMessageDialog(parent=_parent)

        self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)

        return _dialog

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_refresh_tree(self, node_id: List, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

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

        :param list node_id: unused in this method.
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
        """Request insert a new work stream element into the program database.

        :return: None
        """
        _sibling = kwargs['sibling']

        if _sibling:
            pub.sendMessage('request_insert_{0:s}'.format(
                self._module.lower()))
        else:
            pub.sendMessage('request_insert_{0:s}'.format(
                self._module.lower()),
                            parent_id=self._parent_id)  # noqa

    def do_request_insert_child(self, __button: Gtk.ToolButton,
                                **kwargs: Any) -> Any:
        """Request to insert a new child entity of the selected entity.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        self._parent_id = _model.get_value(_row,
                                           self._pnlPanel._lst_col_order[1])  # pylint: disable=protected-access

        return self.do_request_insert(sibling=False, **kwargs)

    def do_request_insert_sibling(self, __button: Gtk.ToolButton,
                                  **kwargs: Any) -> Any:
        """Send request to insert a new sibling entity.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        # If the sibling is nested below the top level, get the parent ID from
        # the previous row.  Otherwise, this is a top level item and the parent
        # ID is zero.
        try:
            _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
            _prow = _model.iter_parent(_row)
            self._parent_id = _model.get_value(
                _prow, self._pnlPanel._lst_col_order[1])  # pylint: disable=protected-access
        except TypeError as _error:
            self._parent_id = 0
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return self.do_request_insert(sibling=True, **kwargs)

    def do_set_cursor(self, cursor: Gdk.CursorType) -> None:
        """Set the cursor for the Module, List, and Work Book Gdk.Window().

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
        try:
            self.get_parent_window().set_cursor(Gdk.Cursor.new(cursor))
            Gdk.flush()
        except AttributeError:
            # There is no parent window.
            pass

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_set_cursor_active(self, node_id: Any = '', tree: Any = '') -> None:
        """Set active cursor for the Module, List, and Work Book Gdk.Window().

        :param node_id: the node ID passed in the PyPubSub message.  Only
            needed when this method is a PyPubSub subscriber.
        :param tree: the treelib Tree() passed in the PyPubSub message.  Only
            needed when this method is a PyPubSub subscriber.
        :return: None
        """
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_set_cursor_active_on_fail(self, error_message: str = '') -> None:
        """Set active cursor for the Module, List, and Work Book Gdk.Window().

        :keyword str error_message: the error message broadcast with the
        'fail' message.  Only needed when this method is a PyPubSub subscriber.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def do_set_cursor_busy(self) -> None:
        """Set busy cursor for the Module, List, and Work Book Gdk.Window().

        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    def make_tab_label(self, **kwargs: Dict[str, Any]) -> None:
        """Make the view's tab label.

        :return: None
        """
        try:
            self._img_tab.set_from_file(self._dic_icons['tab'])
            self.hbx_tab_label.pack_start(self._img_tab, True, True, 0)
        except KeyError:
            # There is no icon to display on the tab.  Just move along.
            pass

        _label: RAMSTKLabel = RAMSTKLabel(self._tablabel)
        _label.do_set_properties(height=30,
                                 width=-1,
                                 justify=Gtk.Justification.CENTER,
                                 tooltip=self._tabtooltip)
        self.hbx_tab_label.pack_end(_label, True, True, 0)
        self.hbx_tab_label.show_all()

    def make_toolbuttons(self, **kwargs: List[Any]) -> None:
        """Create the RAMSTKBaseView() tool buttons.

        Keyword arguments are passed along to the do_make_buttonbox() function.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(do_make_buttonbox(self, **kwargs))
        self.pack_start(_scrolledwindow, False, False, 0)

    def on_button_press(self, __treeview: RAMSTKTreeView,
                        event: Gdk.EventButton) -> None:
        """Handle mouse clicks on the View's RTKTreeView().

        :param __treeview: the RAMSTKTreeView() that called this method.  If is
            unused in this method.
        :param event: the Gdk.Event() that called this method (the important
        attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards

        :return: None
        """
        self.treeview.handler_block(
            self.treeview.dic_handler_id['button-press'])

        if event.button == 3:
            _menu = Gtk.Menu()
            _menu.popup_at_pointer(event)

            # pylint: disable=unused-variable
            for _idx, __ in enumerate(self._lst_icons):
                _menu_item = Gtk.ImageMenuItem()
                _image = Gtk.Image()
                _image.set_from_file(self._dic_icons[self._lst_icons[_idx]])
                _menu_item.set_label(self._lst_mnu_labels[_idx])
                _menu_item.set_image(_image)
                _menu_item.set_property('use_underline', True)
                _menu_item.connect('activate', self._lst_callbacks[_idx],
                                   self.RAMSTK_USER_CONFIGURATION)
                _menu_item.show()
                _menu.append(_menu_item)

        self.treeview.handler_unblock(
            self.treeview.dic_handler_id['button-press'])

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_delete(self, node_id: int, tree: treelib.Tree) -> None:
        """Update the RAMSTKTreeView after deleting a line item.

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

    def on_insert(self, data: Any) -> None:
        """Add row to module view for newly added work stream element.

        :param data: the data package for the work stream element to add.
        :return: None
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
        """Respond to RAMSTKTreeView() row changes.

        :param selection: the current Gtk.TreeSelection().
        :return: _attributes; the dict containing the record's attributes.
        """
        selection.handler_block(self.treeview.dic_handler_id['changed'])

        _attributes: Dict[str, Any] = {}

        _model, _row = selection.get_selected()
        if _row is not None:
            # // TODO: Update base view on_row_change() to use _dic_column_keys.    # noqa
            # //
            # // The _dic_key_index and _dic_column_keys are both
            # // dictionaries with the object's attribute name (str) as the key
            # // and the associated work flow column number (int) as the
            # // value.  Only one is needed; the _dic_column_keys is more
            # // widely used and is more descriptive of what the dict holds.
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
        """Set the Revision ID when a new Revision is selected.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']


class RAMSTKListView(RAMSTKBaseView):
    """Class to display list and matrix type data in the RAMSTK List Book.

    This is the meta class for all RAMSTK List View classes.  Attributes of the
    RAMSTKListView are:

    :ivar str _matrix_type: the name of the matrix displayed by this view.
    :ivar str _module: the capitalized name of the RAMSTK module the List View
        is associated with.
    :ivar int _n_columns: the number of columns in a matrix.
    :ivar int _n_rows: the number of rows in a matrix.
    :ivar matrixview: the MatrixView() displaying the matrix data.
    :type matrixview: :class:`ramstk.views.gtk3.widgets.RAMSTKMatrixView`
    :ivar int n_fixed_columns: the number of matrix columns on the left that
        contain fixed data.
    :ivar tab_label: the Gtk.Label() displaying text for the List View tab.
    :type tab_label: :class:`Gtk.Label`
    """

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the List View.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        if self._view_type == 'matrix':
            self._lst_callbacks = [self.do_request_update]
            self._lst_icons = ['save']
            self._lst_mnu_labels = [_("Save Matrix")]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.matrixview: RAMSTKMatrixView = RAMSTKMatrixView(
            module=self._module)
        self.tab_label: Gtk.Label = Gtk.Label()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_matrix, 'succeed_load_matrix')

    def do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Send request to update the matrix."""
        if self._view_type == 'list':
            super().do_set_cursor_busy()
            pub.sendMessage('request_update_{0:s}'.format(self._module),
                            revision_id=self._revision_id,
                            node_id=self._record_id)
        elif self._view_type == 'matrix':
            super().do_set_cursor_busy()
            pub.sendMessage('do_request_update_matrix',
                            revision_id=self._revision_id,
                            matrix_type=self._module.lower())

    def do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Send request to update the matrix."""
        if self._view_type == 'list':
            super().do_set_cursor_busy()
            pub.sendMessage('request_update_all_{0:s}s'.format(self._module),
                            revision_id=self._revision_id)
        elif self._view_type == 'matrix':
            self._do_request_update(__button)

    def do_load_matrix(self, matrix_type: str, matrix: pd.DataFrame) -> None:
        """Load the RAMSTKMatrixView() with matrix data.

        :param str matrix_type: the type of matrix to load.
        :param matrix: the data matrix to display.
        :return: None
        :rtype: None
        """
        if matrix_type.capitalize() == self._module.capitalize():
            self.matrixview.do_load_matrix(matrix)

    def make_ui(self) -> None:
        """Build the list view user interface.

        :return: None
        """
        super().do_make_layout()

        if self._view_type == 'matrix':
            super().do_embed_matrixview_panel()
        else:
            super().do_embed_treeview_panel()


class RAMSTKModuleView(RAMSTKBaseView):
    """Display data in the RAMSTK Module Book.

    This is the meta class for all RAMSTK Module View classes.
    Attributes of the RAMSTKModuleView are:
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the RAMSTKModuleView meta-class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['insert_part'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/insert_part.png')
        self._dic_key_index: Dict[str, int] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def make_ui(self) -> None:
        """Build the user interface for a ModuleView.

        :return: None
        :rtype: None
        """
        super().do_make_layout()
        super().do_embed_treeview_panel()


class RAMSTKWorkView(RAMSTKBaseView):
    """Class to display data in the RAMSTK Work Book.

    This is the meta class for all RAMSTK Work View classes.  Attributes of the
    RAMSTKWorkView are:

    :ivar list _lst_widgets: the list of RAMSTK (preferred) and Gtk widgets
        used to display information on a workview.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the RAMSTKWorkView meta-class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_widgets: List[object] = []

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.

    def do_clear_tree(self) -> None:
        """Clear the contents of a RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _columns = self.treeview.get_columns()
        for _column in _columns:
            self.treeview.remove_column(_column)

        _model.clear()

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """Update the Work View Gtk.Widgets() when attributes change.

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
