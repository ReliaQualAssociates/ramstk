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
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView, RAMSTKTreeView


class Stakeholders(RAMSTKListView):
    """
    Display all the Stakeholder Inputs associated with the selected Revision.

    The Stakeholder List View displays all the stakeholder inputs associated
    with the selected Stakeholder.  The attributes of the Stakeholder List View
    are:
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

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'stakeholder') -> None:
        """
        Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger, module)
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
        self._lst_icons = ['add', 'remove', 'calculate']
        self._lst_tooltips = [
            _("Add a new Stakeholder input."),
            _("Remove the currently selected "
              "Stakeholder input."),
            _("Calculate the Stakeholder improvement factors.")
        ]
        self._lst_callbacks = [
            self.do_request_insert_sibling, self._do_request_delete,
            self._do_request_calculate
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_requirements,
                      'succeed_retrieve_requirements')
        pub.subscribe(self.on_delete, 'succeed_delete_stakeholder')
        pub.subscribe(self._on_insert, 'succeed_insert_stakeholder')
        pub.subscribe(self.do_load_tree, 'succeed_retrieve_stakeholders')
        pub.subscribe(self._do_refresh_tree, 'succeed_calculate_stakeholder')

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        super().make_ui(icons=self._lst_icons,
                        tooltips=self._lst_tooltips,
                        callbacks=self._lst_callbacks)

        self.tab_label.set_markup("<span weight='bold'>"
                                  + _("Stakeholder\nInputs") + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays stakeholder inputs for the selected revision."))

    def __make_treeview(self) -> None:
        """
        Set up the RAMSTKTreeView() for Stakeholders.

        :return: None
        :rtype: None
        """
        # Load the Affinity Group Gtk.CellRendererCombo()
        _cell = self.treeview.get_column(self._lst_col_order[4]).get_cells()[0]
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
            self._lst_col_order[10]).get_cells()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for _index, _key in enumerate(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_STAKEHOLDERS):
            _group = self.RAMSTK_USER_CONFIGURATION.RAMSTK_STAKEHOLDERS[_key]
            _cellmodel.append([_group])

        # Set the CellRendererSpin() columns to [1, 5] step 1.
        for i in [2, 7, 8]:
            _column = self.treeview.get_column(self._lst_col_order[i])
            _cell = _column.get_cells()[0]
            _adjustment = _cell.get_property('adjustment')
            _adjustment.set_lower(1)
            _adjustment.set_step_increment(1)
            _adjustment.set_upper(5)

        for i in [
                self._lst_col_order[2], self._lst_col_order[3],
                self._lst_col_order[4], self._lst_col_order[5],
                self._lst_col_order[6], self._lst_col_order[7],
                self._lst_col_order[8], self._lst_col_order[9],
                self._lst_col_order[10], self._lst_col_order[11],
                self._lst_col_order[12], self._lst_col_order[13],
                self._lst_col_order[14], self._lst_col_order[15]
        ]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cells()
            _cell[0].connect('edited',
                             super().on_cell_edit, 'lvw_editing_stakeholder',
                             i)

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

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_refresh_tree(self, node_id: int, package: Dict) -> None:
        """
        Refresh the Stakeholder tree whenever the Stakeholders are calculated.

        :param int node_id: the ID of the Stakeholder input that is to be
            refreshed.
        :param dict package: the key:value for the data being updated.
        :return: None
        :rtype: None
        """
        self.do_refresh_tree(package)
        pub.sendMessage('lvw_editing_stakeholder',
                        node_id=[self._record_id, -1],
                        package=package)

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
        _dialog = super().do_raise_dialog(user_msg=_(
            "You are about to delete Stakeholder input {0:d} and "
            "all data associated with it.  Is this really what you "
            "want to do?").format(self._record_id),
                                          severity='question',
                                          parent=_parent)

        if _dialog.do_run() == Gtk.ResponseType.YES:
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
        super().do_set_cursor_active()

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
        super().do_set_cursor_active()

    # pylint: disable=unused-argument
    def _on_button_press(self, __treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Stakeholder List View RAMSTKTreeView().

        :param __treeview: the Stakeholder ListView RAMSTKTreeView().
        :type __treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
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
        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            super().on_button_press(event,
                                    icons=self._lst_icons,
                                    tooltips=self._lst_tooltips,
                                    callbacks=self._lst_callbacks)

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
    Display all the Requirement-Hardware matrix for the selected Revision.

    The attributes of the Requirement-Hardware Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'rqrmnt_hrdwr') -> None:
        """
        Initialize the List View for the Requirement package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger, module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().make_ui(vtype='matrix',
                        tab_label=_("Requirement-Hardware\nMatrix"),
                        tooltip=_("Displays the Requirement-Hardware matrix "
                                  "for the selected revision."))

        # Subscribe to PyPubSub messages.
