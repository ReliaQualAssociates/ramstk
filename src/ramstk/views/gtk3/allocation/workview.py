# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import none_to_default
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox, RAMSTKEntry, RAMSTKPanel, RAMSTKWorkView
)


class GoalMethodPanel(RAMSTKPanel):
    """Panel to display reliability Allocation goals and method."""
    def __init__(self):
        """Initialize an instance of the Allocation goals and method panel."""
        super().__init__()

        # Initialize private dictionary instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['allocation_method_id', 'integer'],
            1: ['goal_measure_id', 'integer'],
            2: ['reliability_goal', 'float'],
            3: ['hazard_rate_goal', 'float'],
            4: ['mtbf_goal', 'float'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Select Allocation Method "),
            _("Select Goal Metric "),
            _("R(t) Goal "),
            _("h(t) Goal "),
            _("MTBF Goal "),
        ]

        # Initialize private scalar instance attributes.
        self._measure_id: int = 0
        self._method_id: int = 0
        self._title: str = _("Allocation Goals and Method")
        self._tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbAllocationGoal: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbAllocationMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHazardRateGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtMTBFGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtReliabilityGoal: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'allocation_method_id':
            [self.cmbAllocationMethod.do_update, 'changed', 0],
            'goal_measure_id':
            [self.cmbAllocationGoal.do_update, 'changed', 1],
            'reliability_goal':
            [self.txtReliabilityGoal.do_update, 'changed', 2],
            'hazard_rate_goal':
            [self.txtHazardRateGoal.do_update, 'changed', 3],
            'mtbf_goal': [self.txtMTBFGoal.do_update, 'changed', 4],
        }
        self._lst_widgets = [
            self.cmbAllocationMethod,
            self.cmbAllocationGoal,
            self.txtReliabilityGoal,
            self.txtHazardRateGoal,
            self.txtMTBFGoal,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_load_combobox()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_hardware')
        pub.subscribe(self._do_set_tree, 'succeed_retrieve_allocation')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.cmbAllocationMethod.do_update(0, signal='changed')
        self.cmbAllocationGoal.do_update(0, signal='changed')
        self.txtHazardRateGoal.do_update("", signal='changed')
        self.txtMTBFGoal.do_update("", signal='changed')
        self.txtReliabilityGoal.do_update("", signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Allocation goals and methods panel.

        :param attributes: the attributes dict for the selected
            Hardware item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        _allocation = self._tree.get_node(self._record_id).data['allocation']
        self._measure_id = _allocation.goal_measure_id
        self._method_id = _allocation.allocation_method_id

        _allocation.reliability_goal = none_to_default(
            _allocation.reliability_goal, 0.0)
        _allocation.hazard_rate_goal = none_to_default(
            _allocation.hazard_rate_goal, 0.0)
        _allocation.mtbf_goal = none_to_default(_allocation.mtbf_goal, 0.0)

        self.cmbAllocationMethod.do_update(_allocation.allocation_method_id,
                                           signal='changed')
        self.cmbAllocationGoal.do_update(_allocation.goal_measure_id,
                                         signal='changed')
        self.txtReliabilityGoal.do_update(str(
            self.fmt.format(_allocation.reliability_goal)),
                                          signal='changed')  # noqa
        self.txtHazardRateGoal.do_update(str(
            self.fmt.format(_allocation.hazard_rate_goal)),
                                         signal='changed')  # noqa
        self.txtMTBFGoal.do_update(str(self.fmt.format(_allocation.mtbf_goal)),
                                   signal='changed')  # noqa

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected R(t) goal.

        :return: None
        :rtype: None
        """
        self.txtReliabilityGoal.props.editable = False
        self.txtReliabilityGoal.set_sensitive(False)
        self.txtMTBFGoal.props.editable = False
        self.txtMTBFGoal.set_sensitive(False)
        self.txtHazardRateGoal.props.editable = False
        self.txtHazardRateGoal.set_sensitive(False)

        if self._measure_id == 1:  # Expressed as reliability.
            self.txtReliabilityGoal.props.editable = True
            self.txtReliabilityGoal.set_sensitive(True)
        elif self._measure_id == 2:  # Expressed as a hazard rate.
            self.txtHazardRateGoal.props.editable = True
            self.txtHazardRateGoal.set_sensitive(True)
        elif self._measure_id == 3:  # Expressed as an MTBF.
            self.txtMTBFGoal.props.editable = True
            self.txtMTBFGoal.set_sensitive(True)

    def _do_set_tree(self, tree: treelib.Tree) -> None:
        """Set the _allocation_tree equal to the datamanger Hardware tree.

        :param tree: the allocation datamanger treelib.Tree() of data.
        :return: None
        :rtype: None
        """
        self._tree = tree

    def __do_load_combobox(self) -> None:
        """Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.cmbAllocationGoal.do_load_combo([[_("Reliability"), 0],
                                              [_("Hazard Rate"), 1],
                                              [_("MTBF"), 2]])
        self.cmbAllocationMethod.do_load_combo(
            [[_("Equal Apportionment"), 0], [_("AGREE Apportionment"), 1],
             [_("ARINC Apportionment"), 2],
             [_("Feasibility of Objectives"), 3]])

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbAllocationMethod.dic_handler_id[
            'changed'] = self.cmbAllocationMethod.connect(
                'changed',
                super().on_changed_combo, 0, 'wvw_editing_allocation')
        self.cmbAllocationGoal.dic_handler_id[
            'changed'] = self.cmbAllocationGoal.connect(
                'changed',
                super().on_changed_combo, 1, 'wvw_editing_allocation')

        self.cmbAllocationMethod.connect('changed', self.__on_method_changed)
        self.cmbAllocationGoal.connect('changed', self.__do_set_sensitive)

        # ----- ENTRIES
        self.txtReliabilityGoal.dic_handler_id[
            'changed'] = self.txtReliabilityGoal.connect(
                'changed',
                super().on_changed_entry, 2, 'wvw_editing_allocation')
        self.txtHazardRateGoal.dic_handler_id[
            'changed'] = self.txtHazardRateGoal.connect(
                'changed',
                super().on_changed_entry, 3, 'wvw_editing_allocation')
        self.txtMTBFGoal.dic_handler_id['changed'] = self.txtMTBFGoal.connect(
            'changed',
            super().on_changed_entry, 4, 'wvw_editing_allocation')

    def __do_set_properties(self) -> None:
        """Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # ----- COMBOBOXES
        self.cmbAllocationGoal.do_set_properties(tooltip=_(
            "Selects the goal measure for the selected hardware assembly."))
        self.cmbAllocationMethod.do_set_properties(tooltip=_(
            "Selects the method for allocating the reliability goal for "
            "the selected hardware assembly."))

        # ----- ENTRIES
        self.txtHazardRateGoal.do_set_properties(
            tooltip=("Displays the hazard rate goal for the selected hardware "
                     "item."),
            width=125)
        self.txtMTBFGoal.do_set_properties(tooltip=_(
            "Displays the MTBF goal for the selected hardware item."),
                                           width=125)  # noqa
        self.txtReliabilityGoal.do_set_properties(tooltip=_(
            "Displays the reliability goal for the selected hardware item."),
                                                  width=125)  # noqa

    def __do_set_sensitive(self, combo: RAMSTKComboBox) -> None:
        """Wrap the _do_set_sensitive() method when goal combo changes.

        :param combo: the allocation goal measure RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        self._measure_id = combo.get_active()
        self._do_set_sensitive()

    def __on_method_changed(self, combo: RAMSTKComboBox) -> None:
        """Wrap the _do_set_sensitive() method when goal combo changes.

        :param combo: the allocation calculation method RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        self._method_id = combo.get_active()
        pub.sendMessage('succeed_change_allocation_method',
                        method_id=self._method_id)


class AllocationPanel(RAMSTKPanel):
    """Panel to display reliability Allocation worksheet."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    def __init__(self):
        """Initialize an instance of the Allocation worksheet panel."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'hardware_id': [None, 'edited', 1],
            'included': [None, 'toggled', 3],
            'n_sub_systems': [None, 'edited', 4],
            'n_sub_elements': [None, 'edited', 5],
            'mission_time': [None, 'edited', 6],
            'duty_cycle': [None, 'edited', 7],
            'int_factor': [None, 'edited', 8],
            'soa_factor': [None, 'edited', 9],
            'op_time_factor': [None, 'edited', 10],
            'env_factor': [None, 'edited', 11],
        }
        self._dic_hardware_attrs: Dict[str, Any] = {}
        self._dic_row_loader = {
            'allocation': self.__do_load_allocation,
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._selected_hardware_id: int = 0
        self._hardware_tree: treelib.Tree = treelib.Tree()
        self._method_id: int = 0
        self._title: str = _("Allocation Analysis")
        self._tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Make a treeview type panel.
        super().do_make_panel_treeview()
        self.__do_set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_clear_tree, 'request_clear_workviews')
        pub.subscribe(super().do_load_panel, 'succeed_calculate_allocation')

        pub.subscribe(self._do_set_tree, 'succeed_retrieve_allocation')
        pub.subscribe(self._do_set_tree, 'succeed_retrieve_hardware')
        pub.subscribe(self._on_select_hardware, 'selected_hardware')

        pub.subscribe(self._on_method_changed,
                      'succeed_change_allocation_method')

    def do_set_callbacks(self) -> None:
        """Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        super().do_set_callbacks()
        super().do_set_cell_callbacks('wvw_editing_allocation', [
            self._lst_col_order[3],
            self._lst_col_order[5],
            self._lst_col_order[6],
            self._lst_col_order[7],
            self._lst_col_order[8],
            self._lst_col_order[9],
            self._lst_col_order[10],
            self._lst_col_order[11],
        ])

    def _do_set_columns_editable(self) -> None:
        """Set editable columns based on the Allocation method selected.

        :return: None
        :rtype: None
        """
        # Key is the allocation method ID:
        #   1: Equal apportionment
        #   2: AGREE apportionment
        #   3: ARINC apportionment
        #   4: Feasibility of Objectives
        # Value is the list of columns that should be made editable for the
        # selected method.
        _dic_editable: Dict[int, Dict[str, str]] = {
            1: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'False',
                'col3': 'True',
                'col4': 'False',
                'col5': 'False',
                'col6': 'True',
                'col7': 'False',
                'col8': 'False',
                'col9': 'False',
                'col10': 'False',
                'col11': 'False',
                'col12': 'False',
                'col13': 'False',
                'col14': 'False',
                'col15': 'False',
                'col16': 'False',
                'col17': 'False',
                'col18': 'False',
                'col19': 'False',
                'col20': 'False',
                'col21': 'False'
            },
            2: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'False',
                'col3': 'True',
                'col4': 'False',
                'col5': 'True',
                'col6': 'True',
                'col7': 'True',
                'col8': 'False',
                'col9': 'False',
                'col10': 'False',
                'col11': 'False',
                'col12': 'False',
                'col13': 'False',
                'col14': 'False',
                'col15': 'False',
                'col16': 'False',
                'col17': 'False',
                'col18': 'False',
                'col19': 'False',
                'col20': 'False',
                'col21': 'False'
            },
            3: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'False',
                'col3': 'True',
                'col4': 'False',
                'col5': 'False',
                'col6': 'False',
                'col7': 'False',
                'col8': 'False',
                'col9': 'False',
                'col10': 'False',
                'col11': 'False',
                'col12': 'False',
                'col13': 'False',
                'col14': 'False',
                'col15': 'False',
                'col16': 'False',
                'col17': 'False',
                'col18': 'False',
                'col19': 'False',
                'col20': 'False',
                'col21': 'False'
            },
            4: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'False',
                'col3': 'True',
                'col4': 'False',
                'col5': 'False',
                'col6': 'False',
                'col7': 'False',
                'col8': 'True',
                'col9': 'True',
                'col10': 'True',
                'col11': 'True',
                'col12': 'False',
                'col13': 'False',
                'col14': 'False',
                'col15': 'False',
                'col16': 'False',
                'col17': 'False',
                'col18': 'False',
                'col19': 'False',
                'col20': 'False',
                'col21': 'False'
            },
        }

        _dic_visible: Dict[int, Dict[str, str]] = {
            1: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'True',
                'col3': 'True',
                'col4': 'True',
                'col5': 'False',
                'col6': 'True',
                'col7': 'False',
                'col8': 'False',
                'col9': 'False',
                'col10': 'False',
                'col11': 'False',
                'col12': 'False',
                'col13': 'False',
                'col14': 'True',
                'col15': 'True',
                'col16': 'True',
                'col17': 'True',
                'col18': 'True',
                'col19': 'True',
                'col20': 'True',
                'col21': 'True'
            },
            2: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'True',
                'col3': 'True',
                'col4': 'True',
                'col5': 'True',
                'col6': 'True',
                'col7': 'True',
                'col8': 'False',
                'col9': 'False',
                'col10': 'False',
                'col11': 'False',
                'col12': 'True',
                'col13': 'False',
                'col14': 'True',
                'col15': 'True',
                'col16': 'True',
                'col17': 'True',
                'col18': 'True',
                'col19': 'True',
                'col20': 'True',
                'col21': 'True'
            },
            3: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'True',
                'col3': 'True',
                'col4': 'False',
                'col5': 'False',
                'col6': 'False',
                'col7': 'False',
                'col8': 'False',
                'col9': 'False',
                'col10': 'False',
                'col11': 'False',
                'col12': 'True',
                'col13': 'False',
                'col14': 'True',
                'col15': 'True',
                'col16': 'True',
                'col17': 'True',
                'col18': 'True',
                'col19': 'True',
                'col20': 'True',
                'col21': 'True'
            },
            4: {
                'col0': 'False',
                'col1': 'False',
                'col2': 'True',
                'col3': 'True',
                'col4': 'False',
                'col5': 'False',
                'col6': 'False',
                'col7': 'False',
                'col8': 'True',
                'col9': 'true',
                'col10': 'True',
                'col11': 'True',
                'col12': 'True',
                'col13': 'False',
                'col14': 'True',
                'col15': 'True',
                'col16': 'True',
                'col17': 'True',
                'col18': 'True',
                'col19': 'True',
                'col20': 'True',
                'col21': 'True'
            },
        }

        if self._method_id != 0:
            self.tvwTreeView.editable = _dic_editable[self._method_id]
            self.tvwTreeView.do_set_columns_editable()
            self.tvwTreeView.visible = _dic_visible[self._method_id]
            self.tvwTreeView.do_set_visible_columns()

    def _do_set_tree(self, tree: treelib.Tree) -> None:
        """Set the _allocation_tree equal to the datamanger Hardware tree.

        :param tree: the Hardware datamanger treelib.Tree() of data.
        :return: None
        :rtype: None
        """
        if tree.get_node(0).tag == 'allocations':
            self._tree = tree
        elif tree.get_node(0).tag == 'hardwares':
            self._hardware_tree = tree
            self._do_load_hardware_attrs()

    def _do_load_hardware_attrs(self) -> None:
        """Load the hardware data dict.

        :return: None
        :rtype: None
        """
        for _node in self._hardware_tree.all_nodes()[1:]:
            _hardware = _node.data['hardware']
            _reliability = _node.data['reliability']
            self._dic_hardware_attrs[_hardware.hardware_id] = [
                _hardware.name, _reliability.hazard_rate_logistics,
                _reliability.mtbf_logistics,
                _reliability.reliability_logistics,
                _reliability.availability_logistics, _hardware.part
            ]

    def _on_method_changed(self, method_id: int) -> None:
        """Set method ID attributes when user changes the selection.

        :param method_id: the newly selected allocation method.
        :return: None
        :rtype: None
        """
        self._method_id = method_id
        self._do_set_columns_editable()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Hardware package Module View RAMSTKTreeView().

        This method is called whenever a Hardware Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)
        if _attributes:
            self._record_id = _attributes['hardware_id']

    def _on_select_hardware(self, attributes: Dict[str, Any]) -> None:
        """Load the allocation list for the selected hardware item.

        :param attributes: the attributes dict for the selected hardware item.
        :return: None
        :rtype: None
        """
        self._selected_hardware_id = attributes['hardware_id']
        self._method_id = self._tree.get_node(
            attributes['hardware_id']).data['allocation'].allocation_method_id
        self._method_id = none_to_default(self._method_id, 0)
        super().do_load_panel(self._tree)
        self._do_set_columns_editable()

    def __do_load_allocation(self,
                             node: Any = '',
                             row: Gtk.TreeIter = None) -> Gtk.TreeIter:
        """Load the allocation RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # pylint: disable=unused-variable
        _entity = node.data['allocation']

        if (not self._dic_hardware_attrs[_entity.hardware_id][5]
                and _entity.parent_id == self._selected_hardware_id):
            _hardware = self._hardware_tree.get_node(_entity.hardware_id).data
            _model = self.tvwTreeView.get_model()

            _name = _hardware['hardware'].name
            _hr_logistics = _hardware['reliability'].hazard_rate_logistics
            _mtbf_logistics = _hardware['reliability'].mtbf_logistics
            _rel_logistics = _hardware['reliability'].reliability_logistics
            _avail_logistics = _hardware['reliability'].availability_logistics

            _attributes = [
                _entity.revision_id, _entity.hardware_id, _name,
                _entity.included, _entity.n_sub_systems,
                _entity.n_sub_elements, _entity.mission_time,
                _entity.duty_cycle, _entity.int_factor, _entity.soa_factor,
                _entity.op_time_factor, _entity.env_factor,
                _entity.weight_factor, _entity.percent_weight_factor,
                _hr_logistics, _entity.hazard_rate_alloc, _mtbf_logistics,
                _entity.mtbf_alloc, _rel_logistics, _entity.reliability_alloc,
                _avail_logistics, _entity.availability_alloc
            ]

            try:
                _new_row = _model.append(row, _attributes)
            except (AttributeError, TypeError, ValueError):
                _new_row = None
                _message = _(
                    "An error occurred when loading allocation record {0} "
                    "into the allocation list.  This might indicate it was "
                    "missing it's data package, some of the data in the "
                    "package was missing, or some of the data was the wrong "
                    "type.  Row data was: {1}").format(str(node.identifier),
                                                       _attributes)
                pub.sendMessage(
                    'do_log_warning_msg',
                    logger_name='WARNING',
                    message=_message,
                )

        return _new_row

    def __do_set_properties(self) -> None:
        """Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
        self.tvwTreeView.set_tooltip_text(
            _("Displays the Allocation Analysis for the currently selected "
              "Hardware item."))


class Allocation(RAMSTKWorkView):
    """Display Allocation attribute data in the RAMSTK Work Book.

    The Allocation Work View displays all the allocation data attributes for
    the selected hardware item. The attributes of an Allocation General Data
    Work View are:

    :cvar _module: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'allocation'
    _tablabel: str = _("Allocation")
    _tabtooltip: str = _("Displays the Allocation analysis for the selected "
                         "hardware item.")

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Allocation Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_calculate)
        self._lst_icons.insert(0, 'calculate')
        self._lst_mnu_labels.insert(0, _("Calculate"))
        self._lst_tooltips = [
            _("Calculate the currently selected Allocation line item."),
            _("Save changes to the currently selected Allocation line item."),
            _("Save changes to all Allocation line items."),
        ]

        # Initialize private scalar attributes.
        self._pnlGoalMethods: RAMSTKPanel = GoalMethodPanel()
        self._pnlPanel: RAMSTKPanel = AllocationPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_hardware')

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the allocation's record ID.

        :param attributes: the attributes dict for the selected allocation
            record.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._parent_id = attributes['parent_id']

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Calculate the Allocation reliability metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_allocation',
                        node_id=self._record_id)

    def __make_ui(self) -> None:
        """Build the user interface for the allocation tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        self._pnlGoalMethods.fmt = self.fmt

        super().do_embed_treeview_panel()
        self._pnlPanel.do_set_callbacks()

        self.remove(self.get_children()[-1])
        _hpaned.pack1(self._pnlGoalMethods, True, True)
        _hpaned.pack2(self._pnlPanel, True, True)

        self.show_all()
