# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
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
            _("Select Allocation Method"),
            _("Select Goal Metric"),
            _("R(t) Goal"),
            _("h(t) Goal"),
            _("MTBF Goal"),
        ]

        # Initialize private scalar instance attributes.
        self._measure_id: int = 0
        self._method_id: int = 0
        self._title: str = _("Allocation Goals and Method")

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbAllocationGoal: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbAllocationMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHazardRateGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtMTBFGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtReliabilityGoal: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater: Dict[str, Union[object, str]] = {
            'allocation_method_id':
            [self.cmbAllocationMethod.do_update, 'changed'],
            'goal_measure_id': [self.cmbAllocationGoal.do_update, 'changed'],
            'reliability_goal': [self.txtReliabilityGoal.do_update, 'changed'],
            'hazard_rate_goal': [self.txtHazardRateGoal.do_update, 'changed'],
            'mtbf_goal': [self.txtMTBFGoal.do_update, 'changed'],
        }
        self._lst_widgets = [
            self.cmbAllocationMethod,
            self.cmbAllocationGoal,
            self.txtReliabilityGoal,
            self.txtHazardRateGoal,
            self.txtMTBFGoal,
        ]

        # Make a fixed type panel.
        super().do_make_panel_fixed()
        self.__do_load_combobox()
        self.__do_set_properties()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self._do_load_panel,
                      'succeed_calculate_allocation_goals')

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

        :param dict attributes: the attributes dict for the selected
            Hardware item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._measure_id = attributes['goal_measure_id']
        self._method_id = attributes['allocation_method_id']

        self.cmbAllocationMethod.do_update(attributes['allocation_method_id'],
                                           signal='changed')
        self.cmbAllocationGoal.do_update(attributes['goal_measure_id'],
                                         signal='changed')
        self.txtReliabilityGoal.do_update(str(
            self.fmt.format(attributes['reliability_goal'])),
                                          signal='changed')  # noqa
        self.txtHazardRateGoal.do_update(str(
            self.fmt.format(attributes['hazard_rate_goal'])),
                                         signal='changed')  # noqa
        self.txtMTBFGoal.do_update(str(self.fmt.format(
            attributes['mtbf_goal'])),
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
                'changed', self.on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbAllocationGoal.dic_handler_id[
            'changed'] = self.cmbAllocationGoal.connect(
                'changed', self.on_changed_combo, 1, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtReliabilityGoal.dic_handler_id[
            'changed'] = self.txtReliabilityGoal.connect(
                'changed', self.on_changed_text, 2, 'wvw_editing_hardware')
        self.txtHazardRateGoal.dic_handler_id[
            'changed'] = self.txtHazardRateGoal.connect(
                'changed', self.on_changed_text, 3, 'wvw_editing_hardware')
        self.txtMTBFGoal.dic_handler_id['changed'] = self.txtMTBFGoal.connect(
            'changed', self.on_changed_text, 4, 'wvw_editing_hardware')

    def __do_set_properties(self) -> None:
        """Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

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

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._allocation_tree: treelib.Tree = treelib.Tree()
        self._method_id: int = 0
        self._title: List[str] = _("Allocation Analysis")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Make a treeview type panel.
        super().do_make_panel_treeview()
        self.__do_set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_clear_tree, 'request_clear_workviews')

        pub.subscribe(self._do_load_panel, 'do_load_allocation')
        pub.subscribe(self._do_load_panel, 'succeed_allocate_reliability')
        pub.subscribe(self._do_load_row, 'succeed_get_allocation_attributes')
        pub.subscribe(self._do_set_tree, 'succeed_get_hardware_tree')

    def do_set_callbacks(self) -> None:
        """Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        super().do_set_cell_callbacks('wvw_editing_hardware', [
            self._lst_col_order[3],
            self._lst_col_order[5],
            self._lst_col_order[6],
            self._lst_col_order[7],
            self._lst_col_order[8],
            self._lst_col_order[9],
            self._lst_col_order[10],
            self._lst_col_order[11],
        ])

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Allocation worksheet panel.

        :param attributes: the attributes dict for the selected Hardware item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._method_id = attributes['allocation_method_id']

        if self._record_id > 0:
            self._do_load_tree()
            self._do_set_columns_editable()

    def _do_load_row(self, attributes: Dict[str, Any]) -> None:
        """Load the Allocation RAMSTKTreeView().

        :param dict attributes: the attributes dict for the row to be loaded.
        :return: None
        :rtype: None
        """
        _node_id = attributes['hardware_id']

        attributes['name'] = self._allocation_tree.get_node(
            _node_id).data['hardware'].get_attributes()['name']
        attributes['hazard_rate_logistics'] = self._allocation_tree.get_node(
            _node_id).data['reliability'].get_attributes()[
                'hazard_rate_logistics']  # noqa
        attributes['mtbf_logistics'] = self._allocation_tree.get_node(
            _node_id).data['reliability'].get_attributes()['mtbf_logistics']
        attributes['reliability_logistics'] = self._allocation_tree.get_node(
            _node_id).data['reliability'].get_attributes()[
                'reliability_logistics']  # noqa
        attributes['availability_logistics'] = self._allocation_tree.get_node(
            _node_id).data['reliability'].get_attributes()[
                'availability_logistics']  # noqa

        super().do_load_row(attributes)

    def _do_load_tree(self) -> None:
        """Load the Allocation RAMSTKTreeView() with allocation data.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

        self._tree_loaded = False
        for _node in self._allocation_tree.children(self._record_id):
            _node_id = _node.data['hardware'].get_attributes()['hardware_id']
            pub.sendMessage('request_get_hardware_attributes',
                            node_id=_node_id,
                            table='allocation')
        self._tree_loaded = True

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

        self.tvwTreeView.editable = _dic_editable[self._method_id]
        self.tvwTreeView.do_set_columns_editable(editable=None)

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

        self.tvwTreeView.visible = _dic_visible[self._method_id]
        self.tvwTreeView.do_set_visible_columns()

    def _do_set_tree(self, dmtree: treelib.Tree) -> None:
        """Set the _allocation_tree equal to the datamanger Hardware tree.

        :param dmtree: the Hardware datamanger treelib.Tree() of data.
        :return: None
        :rtype: None
        """
        self._allocation_tree = dmtree

    def __do_set_properties(self) -> None:
        """Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

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

    :cvar str _module: the name of the module.

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

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'allocation'
    _tablabel: str = _("Allocation")
    _tabtooltip: str = _("Displays the Allocation analysis for "
                         "the selected hardware item.")

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
        self._lst_callbacks = [
            self._do_request_calculate,
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons = [
            'calculate',
            'save',
            'save-all',
        ]
        self._lst_mnu_labels = [
            _("Calculate"),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Calculate the currently selected Allocation line item."),
            _("Save changes to the currently selected Allocation line item."),
            _("Save changes to all Allocation line items."),
        ]

        # Initialize private scalar attributes.
        self._method_id: int = 0

        self._pnlGoalMethods: RAMSTKPanel = GoalMethodPanel()
        self._pnlAllocation: RAMSTKPanel = AllocationPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_hardware')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_hardware')

        pub.subscribe(self._do_load_page,
                      'succeed_get_all_hardware_attributes')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """Load the Allocation page.

        :param attributes: the attributes dict for the selected Hardware item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._method_id = attributes['allocation_method_id']

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Calculate the Allocation reliability metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_allocate_reliability',
                        node_id=self._record_id)
        super().do_set_cursor_active()

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')

    def __make_ui(self) -> None:
        """Build the user interface for the Allocation tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        self._pnlGoalMethods.fmt = self.fmt
        _hpaned.pack1(self._pnlGoalMethods, True, True)

        _fmt_file = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
            + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[self._module])

        try:
            _bg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                self._module + 'bg']
            _fg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                self._module + 'fg']
        except KeyError as _error:
            _bg_color = '#FFFFFF'
            _fg_color = '#000000'

        self._pnlAllocation.do_make_treeview(bg_color=_bg_color,
                                             fg_color=_fg_color,
                                             fmt_file=_fmt_file)
        self._pnlAllocation.do_set_callbacks()

        _hpaned.pack2(self._pnlAllocation, True, True)

        self.show_all()
