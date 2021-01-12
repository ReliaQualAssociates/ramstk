# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK PoF Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.assistants import AddStressTestMethod
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog, RAMSTKPanel, RAMSTKWorkView
)


def get_indenture_level(record_id: str) -> str:
    """Determine the PoF indenture level based on the record ID.

    :param record_id: the ID of the record to determine the indenture
        level.
    :return: _level; the level in the PoF that is currently selected.
    """
    _level = ''

    if record_id.count('.') == 0:
        _level = 'mode'
    elif record_id.count('.') == 1:
        _level = 'mechanism'
    elif record_id.count('.') == 2:
        _level = 'opload'
    elif record_id.count('.') == 4 and record_id[-1] == 's':
        _level = 'opstress'
    elif record_id.count('.') == 4 and record_id[-1] == 't':
        _level = 'testmethod'

    return _level


class PoFPanel(RAMSTKPanel):
    """Panel to display Physics if Failure analysis worksheet."""

    # Define private dictionary class attributes.
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
        ],
    }
    _dic_headings: Dict[str, List[str]] = {
        'mode': [_("Mode ID"), _("Failure\nMode")],
        'mechanism': [_("Mechanism ID"),
                      _("Failure\nMechanism")],
        'opload': [_("Load ID"), _("Operating\nLoad")],
        'opstress': [_("Stress ID"), _("Operating\nStress")],
        'testmethod': [_("Test ID"), _("Recommended\nTest")],
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'pof'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the PoF analysis worksheet."""
        super().__init__()

        # Initialize private dictionary instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            1: ['description', 'text'],
            5: ['damage_model', 'text'],
            6: ['measurable_parameter', 'text'],
            7: ['load_history', 'text'],
            8: ['boundary_conditions', 'text'],
            9: ['priority_id', 'integer'],
            10: ['remarks', 'text'],
        }
        self._dic_attribute_updater = {
            'description': [None, 'edited', 1],
            'damage_model': [None, 'edited', 5],
            'measurable_parameter': [None, 'edited', 6],
            'load_history': [None, 'edited', 7],
            'boundary_conditions': [None, 'edited', 8],
            'priority_id': [None, 'edited', 9],
            'remarks': [None, 'edited', 10],
        }
        self._dic_row_loader = {
            'mode': self.__do_load_mode,
            'mechanism': self.__do_load_mechanism,
            'opload': self.__do_load_opload,
            'opstress': self.__do_load_opstress,
            'method': self.__do_load_test_method,
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._title: str = _("Physics of Failure (PoF) Analysis")

        # Initialize public dictionary instance attributes.
        self.dic_damage_models: Dict[int, str] = {0: ""}
        self.dic_icons: Dict[str, str] = {}
        self.dic_load_history: Dict[int, str] = {0: ""}
        self.dic_measurable_parameters: Dict[int, str] = {0: ""}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_clear_tree, 'request_clear_workviews')
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_pof')
        pub.subscribe(super().do_load_panel, 'succeed_insert_pof')

        pub.subscribe(self._on_delete_insert_pof, 'succeed_delete_pof')

    def do_load_combobox(self) -> None:
        """Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.__do_load_damage_models()
        self.__do_load_measureable_parameters()
        self.__do_load_load_history()

    def do_set_callbacks(self) -> None:
        """Set the callback functions and methods for the PoF widgets.

        :return: None
        :rtype: None
        """
        self.__do_set_properties()

        super().do_set_callbacks()

        for i in self._lst_col_order:
            _cell = self.tvwTreeView.get_column(
                self._lst_col_order[i]).get_cells()

            if isinstance(_cell[0], Gtk.CellRendererPixbuf):
                pass
            else:
                _cell[0].connect('edited',
                                 super().on_cell_edit, i, 'wvw_editing_pof')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_insert_pof(self, tree: treelib.Tree) -> None:
        """Update PoF worksheet whenever an element is inserted or deleted.

        :param tree: the treelib Tree() containing the PoF module's data.
        :return: None
        """
        super().do_load_panel(tree)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the PoF Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the TreeSelection() of the currently
            selected row in the PoF RAMSTKTreeView().
        :return: None
        """
        _columns: List[str] = [
            'col0', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7',
            'col8', 'col9', 'col10', 'pixbuf'
        ]
        _editable = {
            'mode': [
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False'
            ],
            'mechanism': [
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False'
            ],
            'opload': [
                'False', 'True', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'True', 'False', 'False'
            ],
            'opstress': [
                'False', 'False', 'False', 'False', 'False', 'False', 'True',
                'True', 'False', 'False', 'True', 'False'
            ],
            'testmethod': [
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'True', 'False', 'True', 'False'
            ],
        }
        _visible = {
            'mode': [
                'True', 'True', 'True', 'True', 'True', 'False', 'False',
                'False', 'False', 'False', 'False', 'False'
            ],
            'mechanism': [
                'True', 'True', 'True', 'True', 'True', 'False', 'False',
                'False', 'False', 'False', 'False', 'False'
            ],
            'opload': [
                'True', 'True', 'True', 'True', 'True', 'False', 'False',
                'False', 'False', 'True', 'False', 'False'
            ],
            'opstress': [
                'True', 'True', 'True', 'True', 'True', 'False', 'True',
                'True', 'False', 'False', 'True', 'False'
            ],
            'testmethod': [
                'True', 'True', 'True', 'True', 'True', 'False', 'False',
                'False', 'True', 'False', 'True', 'False'
            ],
        }

        _model, _row = selection.get_selected()

        try:
            self._record_id = _model.get_value(_row, 0)
        except TypeError:
            self._record_id = '0'

        _level = get_indenture_level(self._record_id)
        (self.tvwTreeView.headings['col0'],
         self.tvwTreeView.headings['col1']) = {
             'mode': ('Mode ID', 'Failure Mode'),
             'mechanism': ('Mechanism ID', 'Failure Mechanism'),
             'opload': ('Load ID', 'Operating\nLoad'),
             'opstress': ('Stress ID', 'Operating\nStress'),
             'testmethod': ('Method ID', 'Test\nMethod'),
         }[_level]
        super().do_set_headings()

        self.tvwTreeView.editable = dict(zip(_columns, _editable[_level]))
        self.tvwTreeView.visible = dict(zip(_columns, _visible[_level]))
        self.tvwTreeView.do_set_columns_editable()
        self.tvwTreeView.do_set_visible_columns()

        _attributes = super().on_row_change(selection)
        _attributes['node_id'] = self._record_id
        if _attributes:
            pub.sendMessage(
                'selected_pof',
                attributes=_attributes,
            )

    def __do_load_damage_models(self) -> None:
        """Load the RAMSTKTreeView() damage model CellRendererCombo().

        :return: None
        """
        _model = self.__get_cell_model(self._lst_col_order[5])
        for _item in self.dic_damage_models:
            _model.append([self.dic_damage_models[_item]])

    def __do_load_load_history(self) -> None:
        """Load the operating load history CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.__get_cell_model(self._lst_col_order[7])
        for _item in self.dic_load_history:
            _model.append([self.dic_load_history[_item]])

    def __do_load_measureable_parameters(self) -> None:
        """Load the measureable parameters CellRendererCombo().

        :return: None
        """
        _model = self.__get_cell_model(self._lst_col_order[6])
        for _item in self.dic_measurable_parameters:
            _model.append([self.dic_measurable_parameters[_item]])

    def __do_load_mechanism(self, node: treelib.Node,
                            row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['mechanism'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "", "", "", "",
            0, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure mechanism {0:s} in "
                "the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_mode(self, node: treelib.Node,
                       row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons['mode'],
                                                       22, 22)

        _attributes = [
            node.identifier, _entity.description, _entity.effect_end,
            _entity.severity_class, _entity.mode_ratio, "", "", "", "", 0, "",
            _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure mode {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_opload(self, node: treelib.Node,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['opload'], 22, 22)

        _damage_model = self.dic_damage_models[_entity.damage_model]

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, _damage_model,
            "", "", "", _entity.priority_id, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading operating load {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_opstress(self, node: treelib.Node,
                           row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['opstress'], 22, 22)

        _load_history = self.dic_load_history[_entity.load_history]
        _measurable_parameter = self.dic_measurable_parameters[
            _entity.measurable_parameter]

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "",
            _measurable_parameter, _load_history, "", 0, _entity.remarks, _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading operating stress {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_test_method(self, node: treelib.Node,
                              row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['testmethod'], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", 0.0, "", "", "",
            _entity.boundary_conditions, 0, _entity.remarks, _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading test method {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_set_properties(self) -> None:
        """Set the properties of the PoF widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        self.tvwTreeView.set_tooltip_text(
            _("Displays the Physics of Failure (PoF) Analysis for the "
              "currently selected hardware item."))

        # Sets the FMEA carry-over information uneditable and displayed in
        # bold text.
        for i in [0, 1, 2, 3, 4]:
            _column = self.tvwTreeView.get_column(self._lst_col_order[i])
            if i == 0:
                _cell = _column.get_cells()[1]
            else:
                _cell = _column.get_cells()[0]
            _cell.set_property('editable', False)
            _cell.set_property('font', 'normal bold')

        # Set the priority Gtk.CellRendererSpin()'s adjustment limits and
        # step increments.
        _cell = self.tvwTreeView.get_column(
            self._lst_col_order[9]).get_cells()[0]
        _adjustment = _cell.get_property('adjustment')
        _adjustment.configure(5, 1, 5, -1, 0, 0)

    def __get_cell_model(self, column: Gtk.TreeViewColumn) -> Gtk.TreeModel:
        """Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param column: the column number to retrieve the cell from.
        :return: _model
        """
        _column = self.tvwTreeView.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model


class PoF(RAMSTKWorkView):
    """Display PoF attribute data in the Work Book.

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
    :cvar str _module: the name of the module.
    :cvar bool _pixbuf: indicates whether or icons are displayed in the
        RAMSTKTreeView.  If true, a GDKPixbuf column will be appended when
        creating the RAMSTKTreeView.  Default is True.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'pof'
    _pixbuf: bool = True
    _tablabel = _("PoF")
    _tabtooltip = _("Displays the Physics of Failure (PoF) Analysis for "
                    "the selected hardware item.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Work View for the PoF.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_insert_sibling)
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_delete)
        self._lst_icons.insert(0, 'insert_sibling')
        self._lst_icons.insert(1, 'insert_child')
        self._lst_icons.insert(2, 'remove')
        self._lst_mnu_labels.insert(0, _("Insert Sibling"))
        self._lst_mnu_labels.insert(1, _("Insert Child"))
        self._lst_mnu_labels.insert(2, _("Delete Selected"))
        self._lst_tooltips: List[str] = [
            _("Add a new PoF entity at the same level as the "
              "currently selected entity."),
            _("Add a new PoF entity one level below the currently "
              "selected entity."),
            _("Remove the selected entity from the PoF."),
            _("Save changes to the currently selected PoF line."),
            _("Save changes to all PoF lines."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel: RAMSTKPanel = PoFPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_pof')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected entity from the PoF.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent()
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected(
        )
        _node_id = _model.get_value(_row, 0)

        _prompt = _("You are about to delete {1} item {0} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(_node_id, self._module.title())
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                'request_delete_pof',
                node_id=_node_id,
            )

        _dialog.do_destroy()

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new child entity to the PoF.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the PoF.
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected(
        )
        try:
            _parent_id = _model.get_value(_row, 0)
            _level = {
                2: 'opload',
                3: 'opstress_testmethod',
            }[len(str(_parent_id).split('.'))]
        except TypeError:
            _parent_id = '0'
            _level = 'opload'

        if _level == 'opstress_testmethod':
            _level = self.__on_request_insert_opstress_method()

        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_pof_{0:s}'.format(_level),
                        parent_id=str(_parent_id))

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new sibling entity to the PoF.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the PoF.
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected(
        )
        try:
            _parent_id = _model.get_value(_model.iter_parent(_row), 0)
            _level = {
                2: 'opload',
                3: 'opstress_testmethod',
            }[len(str(_parent_id).split('.'))]
        except TypeError:
            _parent_id = '0'
            _level = 'opload'

        if _level == 'opstress_testmethod':
            _level = self.__on_request_insert_opstress_method()

        super().do_set_cursor_busy()
        pub.sendMessage('request_insert_pof_{0:s}'.format(_level),
                        parent_id=str(_parent_id))

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record and revision ID when a hardware item is selected.

        :param attributes: the hazard dict for the selected hardware ID.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['node_id']

    def __make_ui(self) -> None:
        """Build the user interface for the PoF tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        for _idx, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS):
            self._pnlPanel.dic_damage_models[_idx + 1] = \
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_DAMAGE_MODELS[_key]
        for _idx, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY):
            self._pnlPanel.dic_load_history[_idx + 1] = \
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOAD_HISTORY[_key]
        for _idx, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASURABLE_PARAMETERS):
            self._pnlPanel.dic_measurable_parameters[_idx + 1] = \
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASURABLE_PARAMETERS[
                    _key][1]
        self._pnlPanel.dic_icons = self._dic_icons

        super().do_embed_treeview_panel()
        self._pnlPanel.do_load_combobox()
        self._pnlPanel.do_set_callbacks()

        self.show_all()

    def __on_request_insert_opstress_method(self) -> str:
        """Raise dialog to select whether to add a stress or test method.

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
