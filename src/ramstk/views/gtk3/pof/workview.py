# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK PoF Work View."""

# Standard Library Imports
import json
from typing import Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, GdkPixbuf, Gtk, _
from ramstk.views.gtk3.assistants import AddStressTestMethod
from ramstk.views.gtk3.widgets import (RAMSTKLabel, RAMSTKTreeView,
                                       RAMSTKWorkView)


class PoF(RAMSTKWorkView):
    """
    Display PoF attribute data in the Work Book.

    The WorkView displays all the attributes for the Physics of Failure
    Analysis (PoF). The attributes of a PoF Work View are:

    :cvar dict _dic_column_masks: dict with the list of masking values for
        the PoF worksheet.  Key is the PoF indenture level, value is a
        list of True/False values for each column in the worksheet.
    :cvar dict _dic_headings: the dict with the variable headings for the
        first two columns.  Key is the name of the PoF indenture level,
        value is a list of heading text.
    :cvar dict _dic_keys:
    :cvar dict _dic_column_keys:
    :cvar list _lst_labels: the list of labels for the widgets on the work
        view.  The PoF work stream module has no labels, but an empty list
        is required to prevent an AttributeError when creating the UI.
    :cvar bool _pixbuf: indicates whether or icons are displayed in the
        RAMSTKTreeView.  If true, a GDKPixbuf column will be appended when
        creating the RAMSTKTreeView.  Default is True.

    :ivar list _lst_callbacks: the list of callback functions/methods to
        assign to toolbar Gtk.Toolbutton().
    :ivar list _lst_icons: the list of icons to display on the toolbar
        Gtk.Toolbutton().
    :ivar list _lst_tooltips: the list of tooltips to apply to each toolbar
        Gtk.Toolbutton().
    """

    # Define private class dict attributes.
    _dic_column_masks: Dict[str, List[bool]] = {
        'mode': [
            True, True, True, True, True, False, False, False, False, False,
            False, False, False
        ],
        'mechanism': [
            True, True, True, False, False, False, False, False, False, False,
            False, False, False
        ],
        'opload': [
            True, True, True, False, False, True, False, False, False, True,
            True, False, False
        ],
        'opstress': [
            True, True, True, False, False, False, True, True, False, False,
            True, False, False
        ],
        'testmethod': [
            True, True, True, False, False, False, False, False, True, False,
            True, False, False
        ]
    }
    _dic_headings: Dict[str, List[str]] = {
        'mode': [_("Mode ID"), _("Failure\nMode")],
        'mechanism': [_("Mechanism ID"),
                      _("Failure\nMechanism")],
        'opload': [_("Load ID"), _("Operating\nLoad")],
        'opstress': [_("Stress ID"), _("Operating\nStress")],
        'testmethod': [_("Test ID"), _("Recommended\nTest")]
    }
    _dic_keys: Dict[int, str] = {
        1: 'description',
        5: 'damage_model',
        6: 'measurable_parameter',
        7: 'load_history',
        8: 'boundary_conditions',
        9: 'priority_id',
        10: 'remarks'
    }
    _dic_column_keys: Dict[int, str] = _dic_keys

    # Define private list class attributes.
    _lst_labels: List[str] = []

    # Define private class scalar attributes.
    _pixbuf: bool = True

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'pof') -> None:
        """
        Initialize the Work View for the PoF.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :keyword str module: the name of the RAMSTK workstream module this
            workview is associated with.
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete
        ]
        self._lst_icons: List[str] = [
            'insert_sibling', 'insert_child', 'remove'
        ]
        self._lst_tooltips: List[str] = [
            _("Add a new PoF entity at the same level as the "
              "currently selected entity."),
            _("Add a new PoF entity one level below the currently "
              "selected entity."),
            _("Remove the selected entity from the PoF.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_tree, 'succeed_retrieve_pof')
        pub.subscribe(self._on_delete_insert_pof, 'succeed_delete_pof')
        pub.subscribe(self._on_delete_insert_pof, 'succeed_insert_opload')
        pub.subscribe(self._on_delete_insert_pof, 'succeed_insert_opstress')
        pub.subscribe(self._on_delete_insert_pof, 'succeed_insert_test_method')

        pub.subscribe(self.do_set_cursor_active, 'succeed_delete_pof_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_pof')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_pof')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_delete_pof')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_opload')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_opstress')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_test_method')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_update_pof')

    def __do_load_damage_models(self) -> None:
        """
        Load the RAMSTKTreeView() damage model CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[5])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS[_item][0]
            ])

    def __do_load_load_history(self) -> None:
        """
        Load the RAMSTKTreeView() operating load history CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[7])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY:
            _model.append(
                [self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY[_item]])

    def __do_load_measureable_parameters(self) -> None:
        """
        Load the RAMSTKTreeView() measureable parameters CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[6])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASURABLE_PARAMETERS:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.
                RAMSTK_MEASURABLE_PARAMETERS[_item][1]
            ])

    def __load_combobox(self) -> None:
        """
        Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.__do_load_damage_models()
        self.__do_load_measureable_parameters()
        self.__do_load_load_history()

    def __make_ui(self) -> None:
        """
        Make the PoF RAMSTKTreeview().

        :return: a Gtk.Frame() containing the instance of Gtk.Treeview().
        :rtype: :class:`Gtk.Frame`
        """
        # This page has the following layout:
        #
        # +-----+---------------------------------------+
        # |  B  |                                       |
        # |  U  |                                       |
        # |  T  |                                       |
        # |  T  |              SPREAD SHEET             |
        # |  O  |                                       |
        # |  N  |                                       |
        # |  S  |                                       |
        # +-----+---------------------------------------+
        #                                    buttons -----+--> self
        #                                                 |
        #             Gtk.ScrolledWindow -->RAMSTKFrame --+
        # Make the buttons.
        super().make_toolbuttons(icons=self._lst_icons,
                                 tooltips=self._lst_tooltips,
                                 callbacks=self._lst_callbacks)
        super().make_ui_with_treeview(
            title=["", _("Physics of Failure (PoF) Analysis")])
        super().make_tab_label(tablabel=_("PoF"),
                               tooltip=_(
                                   "Displays the Physics of Failure (PoF) "
                                   "Analysis for "
                                   "the selected hardware item."))

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback functions and methods for the PoF widgets.

        :return: None
        :rtype: None
        """
        self.treeview.dic_handler_id['button-press'] = self.treeview.connect(
            'button_press_event', self._on_button_press)

        for i in self._lst_col_order:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cells()

            if isinstance(_cell[0], Gtk.CellRendererPixbuf):
                pass
            else:
                _cell[0].connect('edited',
                                 super().on_cell_edit, 'wvw_editing_pof', i)

    def __set_properties(self) -> None:
        """
        Set the properties of the PoF widgets.

        :return: None
        :rtype: None
        """
        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the Physics of Failure (PoF) Analysis for the "
              "currently selected hardware item."))

        # Sets the FMEA carry-over information uneditable and displayed in
        # bold text.
        for i in [0, 1, 2, 3, 4]:
            _column = self.treeview.get_column(self._lst_col_order[i])
            if i == 0:
                _cell = _column.get_cells()[1]
            else:
                _cell = _column.get_cells()[0]
            _cell.set_property('editable', False)
            _cell.set_property('font', 'normal bold')

        # Set the priority Gtk.CellRendererSpin()'s adjustment limits and
        # step increments.
        _cell = self.treeview.get_column(self._lst_col_order[9]).get_cells()[0]
        _adjustment = _cell.get_property('adjustment')
        _adjustment.configure(5, 1, 5, -1, 0, 0)

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the PoF page.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

    def _do_load_mechanism(self, node: treelib.Node,
                           row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['mechanism'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "", "", "", "",
            0, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure mechanism {0:s} was missing it's data "
                           "package.").format(str(_entity.mechanism_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for failure mechanism ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.mechanism_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "failure mechanism ID {0:s}.".format(
                              str(_entity.mechanism_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_mode(self, node: treelib.Node,
                      row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mode to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self._dic_icons['mode'],
                                                       22, 22)

        _attributes = [
            node.identifier, _entity.description, _entity.effect_end,
            _entity.severity_class, _entity.mode_ratio, "", "", "", "", 0, "",
            _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure mode {0:s} was missing it's data "
                           "package.").format(str(_entity.mode_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = ("Data for failure mode ID {0:s} is the wrong "
                          "type for one or more columns.".format(
                              str(_entity.mode_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for Mode ID "
                          "{0:s}.".format(str(_entity.mode_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_opload(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['opload'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0,
            _entity.damage_model, "", "", "", _entity.priority_id, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Operating load {0:s} was missing it's data "
                           "package.").format(str(_entity.load_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for operating load ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.load_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "operating load ID {0:s}.".format(
                              str(_entity.load_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_opstress(self, node: treelib.Node,
                          row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['opstress'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "",
            _entity.measurable_parameter, _entity.load_history, "", 0,
            _entity.remarks, _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Operating stress ID {0:s} was missing it's "
                           "data package.").format(str(_entity.stress_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for operating stress ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.stress_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "operating stress ID {0:s}.".format(
                              str(_entity.stress_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_test_method(self, node: treelib.Node,
                             row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['testmethod'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "", "", "",
            _entity.boundary_conditions, 0, _entity.remarks, _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Test method ID {0:s} was missing it's "
                           "data package.").format(str(_entity.test_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for test method ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.test_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "test method ID {0:s}.".format(str(_entity.test_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_row(self, node: treelib.Node,
                     row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Determines which type of row to load and loads the data.

        :param node: the FMEA treelib Node() whose data is to be loaded.
        :type node: :class:`treelib.Node`
        :param row: the parent row for the row to be loaded.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just added to the FMEA treeview.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # The root node will have no data package, so this indicates the need
        # to clear the tree in preparation for the load.
        if node.tag == 'pof':
            self._do_clear_page()
        else:
            _method = {
                'mode': self._do_load_mode,
                'mechanism': self._do_load_mechanism,
                'opload': self._do_load_opload,
                'opstress': self._do_load_opstress,
                'method': self._do_load_test_method
            }[node.tag]
            # noinspection PyArgumentList
            _new_row = _method(node, row)

        return _new_row

    def _do_load_tree(self,
                      tree: treelib.Tree,
                      row: Gtk.TreeIter = None) -> None:
        """
        Iterate through tree and load the PoF RAMSTKTreeView().

        :param tree: the treelib.Tree() containing the data packages for the
            PoF analysis.
        :type tree: :class:`treelib.Tree`
        :param row: the last row to be loaded with PoF data.
        :type row: :class:`Gtk.TreeIter`
        :return: None
        :rtype: None
        """
        _node = tree.nodes[list(tree.nodes.keys())[0]]

        _new_row = self._do_load_row(_node, row)

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, row=_new_row)

        super().do_expand_tree()

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected entity from the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 0)

        super().do_set_cursor_busy()
        pub.sendMessage('request_delete_pof', node_id=_node_id)

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """
        Request to insert a new child entity to the PoF.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the PoF.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _parent_id = _model.get_value(_row, 0)
            _attributes = _model.get_value(_row, 12).replace("'", '"')
            _attributes = json.loads("{0}".format(_attributes))
            _level = self._get_indenture_level()
        except TypeError:
            _parent_id = '0'
            _attributes = {}
            _level = 'opload'

        _level = {
            'mechanism': 'opload',
            'opload': 'opstress_testmethod'
        }[_level]

        if _level == 'opstress_testmethod':
            _level = self._on_request_insert_opstress_method()

        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_pof_{0:s}'.format(_level),
                        parent_id=str(_parent_id))

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """
        Request to insert a new sibling entity to the PoF.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the PoF.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _attributes = _model.get_value(_row, 12).replace("'", '"')
            _attributes = json.loads("{0}".format(_attributes))
            _parent_id = _model.get_value(_model.iter_parent(_row), 0)
            _level = self._get_indenture_level()
        except TypeError:
            _attributes = {}
            _parent_id = '0'
            _level = 'opload'

        if _level in ['opstress', 'testmethod']:
            _level = self._on_request_insert_opstress_method()

        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_pof_{0:s}'.format(_level),
                        parent_id=str(_parent_id))

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected entity in the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_pof', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the entities in the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_pof')

    def _get_cell_model(self, column: Gtk.TreeViewColumn) -> Gtk.TreeModel:
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model

    def _get_indenture_level(self) -> str:
        """
        Return the level in the PoF FMEA based on the Node ID.

        :return: _level
        :rtype: str
        """
        _level = ''

        if self._record_id.count('.') == 0:
            _level = 'mode'
        elif self._record_id.count('.') == 1:
            _level = 'mechanism'
        elif self._record_id.count('.') == 2:
            _level = 'opload'
        elif self._record_id.count('.') == 4 and self._record_id[-1] == 's':
            _level = 'opstress'
        elif self._record_id.count('.') == 4 and self._record_id[-1] == 't':
            _level = 'testmethod'

        return _level

    # noinspection PyUnusedLocal
    def _on_button_press(self, __treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the PoF Work View RAMSTKTreeView().

        :param __treeview: the PoF TreeView RAMSTKTreeView().
        :type __treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
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
        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            RAMSTKWorkView.on_button_press(self,
                                           event,
                                           icons=self._lst_icons,
                                           tooltips=self._lst_tooltips,
                                           callbacks=self._lst_callbacks)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_insert_pof(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Update PoF worksheet whenever an element is inserted or deleted.

        :param int node_id: the ID of the inserted/deleted PoF element.
        :param tree: the treelib Tree() containing the PoF module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._do_load_tree(tree)

    def _on_request_insert_opstress_method(self) -> str:
        """
        Raise dialog to select whether to add a stress or test method.

        :return: _level; the level to add, opstress or testmethod.
        :rtype: str
        """
        _level = ""

        _dialog = AddStressTestMethod(
            parent=self.get_parent().get_parent().get_parent().get_parent())

        if _dialog.do_run() == Gtk.ResponseType.OK:
            if _dialog.rdoOpStress.get_active():
                _level = 'opstress'
            elif _dialog.rdoTestMethod.get_active():
                _level = 'testmethod'

        _dialog.do_destroy()

        return _level

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the PoF Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the TreeSelection() of the currently
            selected row in the PoF RAMSTKTreeView().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _model, _row = selection.get_selected()

        try:
            self._record_id = _model.get_value(_row, 0)
        except TypeError:
            self._record_id = '0'

        _level = self._get_indenture_level()
        _headings = super().do_get_headings(_level)

        self.treeview.headings['col0'] = _headings[0]
        self.treeview.headings['col1'] = _headings[1]

        _cell = self.treeview.get_column(self._lst_col_order[1]).get_cells()[0]
        if _level in ['opload', 'opstress', 'testmethod']:
            _cell.set_property('editable', True)
        else:
            _cell.set_property('editable', False)

        _columns = self.treeview.get_columns()
        i = 0
        for _key in self.treeview.headings:
            _label = RAMSTKLabel(self.treeview.headings[_key])
            _label.do_set_properties(height=-1,
                                     justify=Gtk.Justification.CENTER,
                                     wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            _columns[i].set_visible(self.treeview.visible[_key])

            i += 1
