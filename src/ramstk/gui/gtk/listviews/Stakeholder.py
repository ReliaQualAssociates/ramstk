# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.listviews.Stakeholder.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder List View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
from .ListView import RAMSTKListView


class ListView(RAMSTKListView):
    """
    Display all the Stakeholder Inputs associated with the selected Stakeholder.

    The Stakeholder List View displays all the stakeholder inputs associated
    with the selected Stakeholder.  The attributes of the Stakeholder List View
    are:

    :ivar int _stakeholder_id: the Stakeholder ID of the input being displayed
                               in the List View.
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the List View for the Stakeholder package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKListView.__init__(self, configuration, module='stakeholder')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._stakeholder_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_requirements, 'retrieved_requirements')
        pub.subscribe(self.do_load_tree, 'deleted_stakeholder')
        pub.subscribe(self.do_load_tree, 'inserted_stakeholder')
        pub.subscribe(self.do_load_tree, 'retrieved_stakeholders')
        pub.subscribe(self._do_refresh_tree, 'calculated_stakeholder')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the buttonbox for the Stakeholder List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Stakeholder
                             List View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Add a new Stakeholder input."),
            _("Remove the currently selected Stakeholder input."),
            _("Calculate the currently selected Stakeholder input."),
            _("Calculate all Stakeholder intputs."),
        ]
        _callbacks = [
            self.do_request_insert_sibling, self._do_request_delete,
            self._do_request_calculate, self._do_request_calculate_all,
        ]
        _icons = [
            'add',
            'remove',
            'calculate',
            'calculate_all',
        ]

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1,
        )

        return _buttonbox

    def __make_treeview(self):
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
        for _index, _key in enumerate(
                self.RAMSTK_CONFIGURATION.RAMSTK_AFFINITY_GROUPS,
        ):
            _group = self.RAMSTK_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[_key]
            _cellmodel.append([_group[0]])

        # Load the Stakeholders Gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[10],
        ).get_cells()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _owner is (Description, Group Type).
        for _index, _key in enumerate(
                self.RAMSTK_CONFIGURATION.RAMSTK_STAKEHOLDERS,
        ):
            _group = self.RAMSTK_CONFIGURATION.RAMSTK_STAKEHOLDERS[_key]
            _cellmodel.append([_group[0]])

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
                self._lst_col_order[14], self._lst_col_order[15],
        ]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i],
            ).get_cells()
            _cell[0].connect(
                'edited', self._on_cell_edit, i,
                self.treeview.get_model(),
            )

        self.treeview.set_rubber_banding(True)

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup(
            "<span weight='bold'>" +
            _("Stakeholder\nInputs") + "</span>",
        )
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays stakeholder inputs for the selected revision."),
        )

        self.pack_start(self.__make_buttonbox(), False, False, 0)
        RAMSTKListView._make_ui(self)

    def __set_properties(self):
        """
        Set properties of the Failure Definition ListView and widgets.

        :return: None
        :rtype: None
        """
        RAMSTKListView._set_properties(self)
        self.treeview.set_tooltip_text(
            _(
                "Displays the list of stakeholder inputs for the selected "
                "revision.",
            ),
        )

    def _do_load_requirements(self, tree):
        """
        Load the requirement ID list when Requirements are retrieved.

        :return: None
        :rtype: None
        """
        _cell = self.treeview.get_column(self._lst_col_order[9]).get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        for _key in tree.nodes:
            try:
                _model.append([str(tree.nodes[_key].data.requirement_id)])
            except AttributeError:
                pass

    def _do_refresh_tree(self, node_id, results):
        """
        Refresh the calculated values whenever an input is calculated.

        :param int node_id: the ID of the Stakeholder input that is to be
                            refreshed.
        :param list results: a list of the results of the Stakeholder input
                             calculations.
        :return: None
        :rtype: None
        """
        self.do_refresh_tree(node_id, 'improvement', results[0])
        self.do_refresh_tree(node_id, 'overall_weight', results[1])

    def _do_request_calculate(self, __button):
        """
        Request to calculate the selected Stakeholder input.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'request_calculate_stakeholder', node_id=self._stakeholder_id,
        )

    @staticmethod
    def _do_request_calculate_all(__button):
        """
        Request to calculate all Stakeholder inputs.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_calculate_all_stakeholders')

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Stakeholder.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(
            "You are about to delete Stakeholder input {0:d} and "
            "all data associated with it.  Is this really what you "
            "want to do?",
        ).format(self._stakeholder_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question',
        )
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage(
                'request_delete_stakeholder', node_id=self._stakeholder_id,
            )

        _dialog.do_destroy()

    def _do_request_insert(self, **kwargs):
        """
        Request to add a Stakeholder.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        pub.sendMessage(
            'request_insert_stakeholder', revision_id=self._revision_id,
        )

    def _do_request_update(self, __button):
        """
        Save the currently selected Stakeholder Input.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_stakeholder', node_id=self._stakeholder_id,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Save all the Stakeholder Inputs.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: none
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_stakeholders')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Stakeholder List View RAMSTKTreeView().

        :param treeview: the Stakeholder ListView RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
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
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = ['add', 'remove', 'save', 'save-all']
            _labels = [
                _("Add New Stakeholder Input"),
                _("Remove Selected Stakeholder Input"),
                _("Save Selected Stakeholder Input"),
                _("Save All Stakeholder Inputs"),
            ]
            _callbacks = [
                self._do_request_insert, self._do_request_delete,
                self._do_request_update, self._do_request_update_all,
            ]

            self.on_button_press(
                event, icons=_icons, labels=_labels, callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Stakeholder List View RAMSTKTreeView().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param Gtk.TreeModel model: the Gtk.TreeModel() the Gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
        _dic_keys = {
            2: 'customer_rank',
            3: 'description',
            4: 'group',
            7: 'planned_rank',
            8: 'priority',
            9: 'requirement_id',
            10: 'stakeholder',
            11: 'user_float_1',
            12: 'user_float_2',
            13: 'user_float_3',
            14: 'user_float_4',
            15: 'user_float_5',
        }
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        if not RAMSTKListView._do_edit_cell(
                __cell, path, new_text, position, model,
        ):
            if _key == 'group':
                # FIXME: See issue #60.
                try:
                    _new_key = max(
                        self.RAMSTK_CONFIGURATION.
                        RAMSTK_AFFINITY_GROUPS.keys(),
                    ) + 1
                except ValueError:
                    _new_key = 1
                self.RAMSTK_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[
                    _new_key
                ] = str(new_text)

            pub.sendMessage(
                'lvw_editing_stakeholder',
                module_id=self._stakeholder_id,
                key=_key,
                value=new_text,
            )

    def _on_row_change(self, treeview):
        """
        Handle events for the Stakeholder List View RAMSTKTreeView().

        This method is called whenever a Stakeholder List View RAMSTKTreeView()
        row is activated.

        :param treeview: the Stakeholder List View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        if _row is not None:
            _attributes['revision_id'] = _model.get_value(
                _row, self._lst_col_order[0],
            )
            _attributes['stakeholder_id'] = _model.get_value(
                _row, self._lst_col_order[1],
            )
            _attributes['customer_rank'] = _model.get_value(
                _row, self._lst_col_order[2],
            )
            _attributes['description'] = _model.get_value(
                _row, self._lst_col_order[3],
            )
            _attributes['group'] = _model.get_value(
                _row,
                self._lst_col_order[4],
            )
            _attributes['improvement'] = _model.get_value(
                _row, self._lst_col_order[5],
            )
            _attributes['overall_weight'] = _model.get_value(
                _row, self._lst_col_order[6],
            )
            _attributes['planned_rank'] = _model.get_value(
                _row, self._lst_col_order[7],
            )
            _attributes['priority'] = _model.get_value(
                _row,
                self._lst_col_order[8],
            )
            _attributes['requirement_id'] = _model.get_value(
                _row, self._lst_col_order[9],
            )
            _attributes['stakeholder'] = _model.get_value(
                _row, self._lst_col_order[10],
            )
            _attributes['user_float_1'] = _model.get_value(
                _row, self._lst_col_order[11],
            )
            _attributes['user_float_2'] = _model.get_value(
                _row, self._lst_col_order[12],
            )
            _attributes['user_float_3'] = _model.get_value(
                _row, self._lst_col_order[13],
            )
            _attributes['user_float_4'] = _model.get_value(
                _row, self._lst_col_order[14],
            )
            _attributes['user_float_5'] = _model.get_value(
                _row, self._lst_col_order[15],
            )

            self._stakeholder_id = _attributes['stakeholder_id']

            pub.sendMessage('selected_stakeholder', attributes=_attributes)

        treeview.handler_unblock(self._lst_handler_id[0])
