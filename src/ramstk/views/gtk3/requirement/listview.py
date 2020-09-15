# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Requirement List View Module."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class Stakeholders(RAMSTKListView):
    """
    Display all the Stakeholder Inputs associated with the selected Revision.

    The Stakeholder List View displays all the stakeholder inputs associated
    with the selected Requriement.  The attributes of the Stakeholder List View
    are:

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
    _dic_keys = {
        2: 'customer_rank',
        3: 'description',
        4: 'group',
        5: 'improvement',
        6: 'overall_weight',
        7: 'planned_rank',
        8: 'priority',
        9: 'requirement_id',
        10: 'stakeholder',
        11: 'user_float_1',
        12: 'user_float_2',
        13: 'user_float_3',
        14: 'user_float_4',
        15: 'user_float_5'
    }
    _dic_column_keys = _dic_keys

    # Define private scalar class attributes.
    _module: str = 'stakeholder'
    _tablabel = "<span weight='bold'>" + _("Stakeholder\nInputs") + "</span>"
    _tabtooltip = _("Displays stakeholder inputs for the selected revision.")
    _view_type: str = 'list'

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_key_index = {
            'revision_id': 0,
            'stakeholder_id': 1,
            'customer_rank': 2,
            'description': 3,
            'group': 4,
            'improvement': 5,
            'overall_weight': 6,
            'planned_rank': 7,
            'priority': 8,
            'requirement_id': 9,
            'stakeholder': 10,
            'user_float_1': 11,
            'user_float_2': 12,
            'user_float_3': 13,
            'user_float_4': 14,
            'user_float_5': 15
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self.do_request_insert_sibling, self._do_request_delete,
            self._do_request_calculate, self._do_request_update,
            self._do_request_update_all
        ]
        self._lst_icons = ['add', 'remove', 'calculate', 'save', 'save-all']
        self._lst_mnu_labels = [
            _("Add Input"),
            _("Delete Selected Input"),
            _("Calculate Inputs"),
            _("Update Input"),
            _("Update All Inputs")
        ]
        self._lst_tooltips = [
            _("Add a new stakeholder input."),
            _("Remove the currently selected stakeholder input."),
            _("Calculate the stakeholder improvement factors."),
            _("Save changes to the selected stakeholder input."),
            _("Save change to all stakeholder inputs.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        super().make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_requirements,
                      'succeed_retrieve_requirements')
        pub.subscribe(self._on_insert, 'succeed_insert_stakeholder')

        pub.subscribe(self.do_load_tree, 'succeed_retrieve_stakeholders')
        pub.subscribe(self.do_refresh_tree, 'succeed_calculate_stakeholder')
        pub.subscribe(self.do_set_cursor_active,
                      'succeed_delete_stakeholder_2')
        pub.subscribe(self.do_set_cursor_active,
                      'succeed_insert_stakeholder_2')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_stakeholder')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_stakeholder')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_stakeholder')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_stakeholder')
        pub.subscribe(self.on_delete, 'succeed_delete_stakeholder')

    def __make_treeview(self) -> None:
        """
        Set up the RAMSTKTreeView() for Stakeholders.

        :return: None
        :rtype: None
        """
        # Load the Affinity Group Gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self.treeview.position['col4']).get_cells()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _group is (Description, Group Type).
        # pylint: disable=unused-variable
        for __, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS):
            _group = self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[
                _key]
            _cellmodel.append([_group[0]])

        # Load the Stakeholders Gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self.treeview.position['col10']).get_cells()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for _index, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_STAKEHOLDERS):
            _group = self.RAMSTK_USER_CONFIGURATION.RAMSTK_STAKEHOLDERS[_key]
            _cellmodel.append([_group])

        # Set the CellRendererSpin() columns to [1, 5] step 1.
        for _key in ['col2', 'col7', 'col8']:
            _column = self.treeview.get_column(self.treeview.position[_key])
            _cell = _column.get_cells()[0]
            _adjustment = _cell.get_property('adjustment')
            _adjustment.set_lower(1)
            _adjustment.set_step_increment(1)
            _adjustment.set_upper(5)

        _idx = 2
        for _key in [
                'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9',
                'col10', 'col11', 'col12', 'col13', 'col14', 'col15'
        ]:
            _cell = self.treeview.get_column(
                self.treeview.position[_key]).get_cells()[0]
            _cell.connect('edited',
                          super().on_cell_edit, 'lvw_editing_stakeholder',
                          _idx)
            _idx += 1

        self.treeview.set_rubber_banding(True)

    def __set_properties(self) -> None:
        """
        Set properties of the Requirement ListView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_rubber_banding(True)
        self.treeview.set_tooltip_text(
            _("Displays the list of stakeholder inputs for the selected "
              "revision."))

    def _do_insert_to_affinity_group(self, new_text: str) -> None:
        """
        Add an entry to the RAMSTK_AFFINITY_GROUP dictionary.

        :param str new_text: the name of the new group to add to the
            RAMSTK_AFFINITY_GROUP dictionary.
        :return: None
        :rtype: None
        """
        try:
            _new_key = max(self.RAMSTK_USER_CONFIGURATION.
                           RAMSTK_AFFINITY_GROUPS.keys()) + 1
        except ValueError:
            _new_key = 1
        self.RAMSTK_USER_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[_new_key] = str(
            new_text)

    def _do_load_requirements(self, tree: treelib.Tree) -> None:
        """
        Load the requirement ID list when Requirements are retrieved.

        :param tree: the treelib Tree() containing the Stakeholder data
            records.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _cell = self.treeview.get_column(self._lst_col_order[9]).get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        for _node in tree.nodes:
            if _node != 0:
                _model.append([
                    str(tree.nodes[_node].data['requirement'].requirement_id)
                ])

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Request to calculate the selected Stakeholder input.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_stakeholder',
                        node_id=self._record_id)
        super().do_set_cursor_active()

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to calculate all Stakeholder inputs.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_all_stakeholders')
        super().do_set_cursor_active()

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected Stakeholder.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
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

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Save the currently selected Stakeholder Input.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_stakeholder', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Save all the Stakeholder Inputs.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: none
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_stakeholders')

    def _on_insert(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added requirement.

        :param int node_id: the ID of the newly added requirement.
        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _data = tree.get_node(node_id).data['stakeholder'].get_attributes()

        super().on_insert(_data)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Stakeholder List View RAMSTKTreeView().

        This method is called whenever a Stakeholder List View RAMSTKTreeView()
        row is activated.

        :param selection: the Stakeholder class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _attributes: Dict[str, Any] = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['stakeholder_id']


class RequirementHardware(RAMSTKListView):
    """
    Display all the Requirement::Hardware matrix for the selected Revision.

    The attributes of the Requirement::Hardware Matrix View are:

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

    # Define private scalar class attributes.
    _module: str = 'rqrmnt_hrdwr'
    _tablabel = "<span weight='bold'>" + _(
        "Requirement::Hardware\nMatrix") + "</span>"
    _tabtooltip = _("Displays the Requirement::Hardware matrix "
                    "for the selected revision.")
    _view_type: str = 'matrix'

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [self.do_request_update]
        self._lst_icons = ['save']
        self._lst_mnu_labels = [_("Save Matrix")]
        self._lst_tooltips = [
            _("Save changes to the Requirement::Hardware matrix.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui()

        # Subscribe to PyPubSub messages.

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Requirement::Hardware matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='rqrmnt_hrdwr')

    def _do_request_update_all(self, __button: Gtk.Button) -> None:
        """
        Sends message to request updating the Requirement::Hardware matrix.

        :param __button: the Gtk.Button() that call this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('do_request_update_matrix',
                        revision_id=self._revision_id,
                        matrix_type='rqrmnt_hrdwr')
