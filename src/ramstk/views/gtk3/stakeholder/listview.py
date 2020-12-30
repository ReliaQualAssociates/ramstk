# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.stakeholder.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Stakeholder Input list view."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView, RAMSTKPanel


class StakeholderPanel(RAMSTKPanel):
    """Panel to display list of stakeholder inputs."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'stakeholder'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the stakeholder input panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys = {
            0: ['revision_id', 'integer'],
            1: ['stakeholder_id', 'integer'],
            2: ['customer_rank', 'integer'],
            3: ['description', 'string'],
            4: ['group', 'string'],
            5: ['improvement', 'float'],
            7: ['planned_rank', 'integer'],
            6: ['overall_weight', 'float'],
            8: ['priority', 'integer'],
            9: ['requirement_id', 'string'],
            10: ['stakeholder', 'string'],
            11: ['user_float_1', 'float'],
            12: ['user_float_2', 'float'],
            13: ['user_float_3', 'float'],
            14: ['user_float_4', 'float'],
            15: ['user_float_5', 'float'],
        }
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'stakeholder_id': [None, 'edited', 1],
            'customer_rank': [None, 'edited', 2],
            'description': [None, 'edited', 3],
            'group': [None, 'edited', 4],
            'improvement': [None, 'edited', 5],
            'overall_weight': [None, 'edited', 6],
            'planned_rank': [None, 'edited', 7],
            'priority': [None, 'edited', 8],
            'requirement_id': [None, 'edited', 9],
            'stakeholder': [None, 'edited', 10],
            'user_float_1': [None, 'edited', 11],
            'user_float_2': [None, 'edited', 12],
            'user_float_3': [None, 'edited', 13],
            'user_float_4': [None, 'edited', 14],
            'user_float_5': [None, 'edited', 15],
        }
        self._dic_row_loader = {
            'stakeholder': self.__do_load_stakeholder,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Stakeholder Input List")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_stakeholders')
        pub.subscribe(super().do_load_panel, 'succeed_insert_stakeholder')
        pub.subscribe(super().do_refresh_tree, 'succeed_calculate_stakeholder')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_stakeholder')
        pub.subscribe(super().on_delete, 'succeed_delete_stakeholder')

        pub.subscribe(self._do_load_requirements,
                      'succeed_retrieve_requirements')
        pub.subscribe(self._on_module_switch, 'lvwSwitchedPage')

    def do_load_affinity_groups(
            self, affinities: Dict[int, Tuple[str, str]]) -> None:
        """Load the affinity group list.

        :param affinities: the dict containing the affinity groups and the
            group type (affinity in all cases).
        :return: None
        """
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position['col4']).get_cells()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for __, _key in enumerate(affinities):
            _group = affinities[_key]
            _cellmodel.append([_group[0]])

    def do_load_stakeholders(self, stakeholders: Dict[int, str]) -> None:
        """Load the stakeholder list.

        :param stakeholders: the dict containing the names of the stakeholders.
        :return: None
        """
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position['col10']).get_cells()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for __, _key in enumerate(stakeholders):
            _group = stakeholders[_key]
            _cellmodel.append([_group])

    def do_set_callbacks(self) -> None:
        """Set callbacks for the stakeholder input list view.

        :return: None
        """
        self.tvwTreeView.dic_handler_id[
            'changed'] = self.tvwTreeView.selection.connect(
                'changed', self._on_row_change)

        for _key in [
                'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9',
                'col10', 'col11', 'col12', 'col13', 'col14', 'col15'
        ]:
            _cell = self.tvwTreeView.get_column(
                self.tvwTreeView.position[_key]).get_cells()[0]
            _cell.connect('edited',
                          super().on_cell_edit,
                          self.tvwTreeView.position[_key],
                          'lvw_editing_stakeholder')

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the list of stakeholders."))

        # Set the spin button cells to have a range of [1, 5] with a step of 1.
        for _key in self.tvwTreeView.widgets:
            if self.tvwTreeView.widgets[_key] == 'spin':
                _column = self.tvwTreeView.get_column(
                    self.tvwTreeView.position[_key])
                _cell = _column.get_cells()[0]
                _adjustment = _cell.get_property('adjustment')
                _adjustment.set_lower(1)
                _adjustment.set_step_increment(1)
                _adjustment.set_upper(5)

    def _do_load_requirements(self, tree: treelib.Tree) -> None:
        """Load the requirement ID list when Requirements are retrieved.

        :param tree: the treelib Tree() containing the Stakeholder data
            records.
        :return: None
        """
        _cell = self.tvwTreeView.get_column(
            self._lst_col_order[9]).get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        for _node in tree.nodes:
            if _node != 0:
                _model.append([
                    str(tree.nodes[_node].data['requirement'].requirement_id)
                ])

    def _on_insert(self, tree: treelib.Tree) -> None:
        """Wrap the do_load_panel() method when an element is inserted.

        The do_set_cursor_active() method responds to the same message,
        but one less argument in it's call.  This results in a PyPubSub
        error and is the reason this wrapper method is needed.

        :param tree: the module's treelib Tree().
        :return: None
        """
        super().do_load_panel(tree)

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'stakeholder' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[1])
            _name = _model.get_value(_row, self._lst_col_order[3])
            _title = _("Analyzing Stakeholder {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the List View RAMSTKTreeView().

        This method is called whenever a Stakeholder List View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Stakeholder class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['stakeholder_id']
            self._parent_id = _attributes['requirement_id']

            pub.sendMessage('selected_stakeholder', attributes=_attributes)

    def __do_load_stakeholder(self, node: treelib.Node,
                              row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a stakeholder input into the RAMSTKTreeView().

        :param node: the treelib Node() with the stakeholder data to load.
        :param row: the parent row of the stakeholder input to load.
        :return: _new_row; the row that was just populated with stakeholder
            input data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None
        _data: List[Any] = []

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable
        _attributes = _entity.get_attributes()

        _model = self.tvwTreeView.get_model()
        for _col, _attr in self.tvwTreeView.korder.items():
            _pos = self.tvwTreeView.position[_col]
            _data.insert(_pos, _attributes[_attr])

        try:
            _new_row = _model.append(row, _data)
        except (AttributeError, TypeError, ValueError) as _error:
            _new_row = None
            _message = _(
                "An error occurred when loading stakeholder input {0:s}.  "
                "This might indicate it was missing it's data package, some "
                "of the data in the package was missing, or some of the data "
                "was the wrong type.  Row data was: {1}.  Error was: {2}."
                "").format(str(node.identifier), _data, _error)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row


# noinspection PyUnresolvedReferences
class Stakeholders(RAMSTKListView):
    """Display Stakeholder Inputs associated with the selected Revision.

    The Stakeholder List View displays all the stakeholder inputs associated
    with the selected Requirement.  The attributes of the Stakeholder List
    View are:

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

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'stakeholders'
    _tablabel = "<span weight='bold'>" + _("Stakeholder\nInputs") + "</span>"
    _tabtooltip = _("Displays stakeholder inputs for the selected revision.")
    _view_type = 'list'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, self._do_request_delete)
        self._lst_callbacks.insert(2, self._do_request_calculate)
        self._lst_icons.insert(1, 'remove')
        self._lst_icons.insert(2, 'calculate')
        self._lst_mnu_labels.insert(1, _("Delete Selected Input"))
        self._lst_mnu_labels.insert(2, _("Calculate Inputs"))
        self._lst_tooltips.insert(0, _("Add a new stakeholder input."))
        self._lst_tooltips.insert(
            1, _("Remove the currently selected stakeholder input."))
        self._lst_tooltips.insert(
            2, _("Calculate the stakeholder improvement factors."))
        self._lst_tooltips.insert(
            3, _("Update the currently selected stakeholder input."))
        self._lst_tooltips.insert(4, _("Update all stakeholder inputs."))

        # Initialize private scalar attributes.
        self._pnlPanel = StakeholderPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_stakeholder')

    def _do_add_to_affinity_group(self, new_text: str) -> None:
        """Add an entry to the RAMSTK_AFFINITY_GROUP dictionary.

        :param new_text: the name of the new group to add to the
            RAMSTK_AFFINITY_GROUP dictionary.
        :return: None
        """
        try:
            _new_key = max(self.RAMSTK_USER_CONFIGURATION.
                           RAMSTK_AFFINITY_GROUPS.keys()) + 1
        except ValueError:
            _new_key = 1
        self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[_new_key] = str(
            new_text)

    # pylint: disable=unused-argument
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the selected Stakeholder input.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_stakeholder',
                        node_id=self._record_id)
        super().do_set_cursor_active()

    # pylint: disable=unused-argument
    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate all Stakeholder inputs.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_all_stakeholders')
        super().do_set_cursor_active()

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Stakeholder.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_("You are about to delete Stakeholder input {0:d} and "
                      "all data associated with it.  Is this really what you "
                      "want to do?").format(self._record_id))
        _dialog.do_set_message_type(message_type='question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_stakeholder',
                            node_id=self._record_id)

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the stakeholder input's record ID.

        :param attributes: the attributes dict for the selected stakeholder
            input.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['stakeholder_id']

    def __make_ui(self) -> None:
        """Build the user interface for the stakeholder input list view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_load_affinity_groups(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS)
        self._pnlPanel.do_load_stakeholders(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_STAKEHOLDERS)
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
