# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.Validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Module View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (
    RAMSTKLabel, RAMSTKMessageDialog, do_make_buttonbox,
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Validation attribute data in the RAMSTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Validation
    Module View are:

    :ivar int _validation_id: the ID of the currently selected Validation.
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Validation Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKModuleView.__init__(self, configuration, module='validation')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/validation.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_refresh_tree, 'calculated_validation')
        pub.subscribe(self.do_load_tree, 'deleted_validation')
        pub.subscribe(self.do_load_tree, 'inserted_validation')
        pub.subscribe(self.do_load_tree, 'retrieved_validations')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_validation')

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrolledwindow.add_with_viewport(
            do_make_buttonbox(
                self,
                icons=['add', 'remove', 'calculate_all', 'export'],
                tooltips=[
                    _("Add a new Validation task."),
                    _("Remove the currently selected Validation task."),
                    _("Calculate the entire validation program."),
                    _(
                        "Exports Verification tasks to an external file (CSV, "
                        "Excel, and text files are supported).",
                    ),
                ],
                callbacks=[
                    self.do_request_insert_sibling, self._do_request_delete,
                    self._do_request_calculate_all, self._do_request_export,
                ],
            ),
        )
        self.pack_start(_scrolledwindow, False, False, 0)

        self.make_treeview(editable=[2, 4])
        self.treeview.set_tooltip_text(
            _("Displays the list of validation tasks."),
        )

        RAMSTKModuleView.make_ui(self)

        i = 0
        for _column in self.treeview.get_columns():
            _cell = _column.get_cells()[0]
            try:
                if _cell.get_property('editable'):
                    _cell.connect(
                        'edited', self._on_cell_edit, i,
                        self.treeview.get_model(),
                    )
            except TypeError:
                pass
            i += 1

        _label = RAMSTKLabel(
            _("Validation"),
            width=-1,
            height=-1,
            tooltip=_("Displays the list of validation tasks."),
        )

        self.hbx_tab_label.pack_end(_label, True, True, 0)

        self.show_all()

    def _do_refresh_tree(self, attributes):
        """
        Load the new attribute values for the entire tree after calculating.

        :return: None
        :rtype: None
        """
        for _key in [
                'cost_ll', 'cost_mean', 'cost_ul', 'cost_variance', 'time_ll',
                'time_mean', 'time_ul', 'time_variance',
        ]:
            self.do_refresh_tree(self._validation_id, _key, attributes[_key])

        pub.sendMessage('request_update_status')

    def _do_request_calculate_all(self, __button):
        """
        Send request to calculate all validation tasks.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'request_calculate_validation', node_id=self._validation_id,
        )

    def _do_request_delete(self, __button):
        """
        Request to delete the selected record from the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(
            "You are about to delete Validation {0:d} and all "
            "data associated with it.  Is this really what "
            "you want to do?",
        ).format(self._validation_id)
        _dialog = RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question',
        )
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage(
                'request_delete_validation', node_id=self._validation_id,
            )

        _dialog.do_destroy()

    def _do_request_export(self, __button):
        """
        Launch the Export assistant.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        return self.do_request_export('Validation')

    def _do_request_insert(self, **kwargs):
        """
        Send request to insert a new record to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        if _sibling:
            try:
                _parent_id = self._parent_id
            except AttributeError:
                _parent_id = 0
        else:
            _parent_id = self._validation_id

        pub.sendMessage(
            'request_insert_validation', revision_id=self._revision_id,
        )

    def _do_request_update(self, __button):
        """
        Send request to update selected record to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_validation', node_id=self._validation_id,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Send request to save all the records to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_validations')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Validation Module View RAMSTKTreeView().

        :param treeview: the Validation class Gtk.TreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
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
            _icons = ['add', 'calculate_all']
            _labels = [
                _("Add Validation Task"),
                _("Remove the Selected Validation Task"),
                _("Calculate the entire validation program."),
                _("Save Selected Validation Task"),
                _("Save All Validation Tasks"),
            ]
            _callbacks = [
                self.do_request_insert_sibling, self._do_request_calculate_all,
            ]

            RAMSTKModuleView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Validation package Module View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _dic_keys = {
            2: 'description',
            3: 'task_type',
            4: 'task_specification',
            5: 'measurement_unit',
            6: 'acceptable_minimum',
            7: 'acceptable_mean',
            8: 'acceptable_maximum',
            9: 'acceptable_variance',
            10: 'date_start',
            11: 'date_end',
            12: 'status',
            13: 'time_minimum',
            14: 'time_average',
            15: 'time_maximum',
            18: 'cost_minimum',
            19: 'cost_average',
            20: 'cost_maximum',
            23: 'confidence',
        }

        if not self.treeview.do_edit_cell(
                __cell, path, new_text, position, model,
        ):
            try:
                _key = _dic_keys[self._lst_col_order[position]]
            except KeyError:
                _key = None

            pub.sendMessage(
                'mvw_editing_validation',
                module_id=self._validation_id,
                key=_key,
                value=new_text,
            )

    def _on_row_change(self, treeview):
        """
        Handle events for the Validation package Module View RAMSTKTreeView().

        This method is called whenever a Validation Module View RAMSTKTreeView()
        row is activated/changed.

        :param treeview: the Validation class Gtk.TreeView().
        :type treeview: :class:`Gtk.TreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _attributes['revision_id'] = _model.get_value(
                _row, self._lst_col_order[0],
            )
            _attributes['validation_id'] = _model.get_value(
                _row, self._lst_col_order[1],
            )
            _attributes['description'] = _model.get_value(
                _row, self._lst_col_order[2],
            )
            _attributes['task_type'] = _model.get_value(
                _row, self._lst_col_order[3],
            )
            _attributes['task_specification'] = _model.get_value(
                _row, self._lst_col_order[4],
            )
            _attributes['measurement_unit'] = _model.get_value(
                _row, self._lst_col_order[5],
            )
            _attributes['acceptable_minimum'] = _model.get_value(
                _row, self._lst_col_order[6],
            )
            _attributes['acceptable_mean'] = _model.get_value(
                _row, self._lst_col_order[7],
            )
            _attributes['acceptable_maximum'] = _model.get_value(
                _row, self._lst_col_order[8],
            )
            _attributes['acceptable_variance'] = _model.get_value(
                _row, self._lst_col_order[9],
            )
            _attributes['date_start'] = _model.get_value(
                _row, self._lst_col_order[10],
            )
            _attributes['date_end'] = _model.get_value(
                _row,
                self._lst_col_order[11],
            )
            _attributes['status'] = _model.get_value(
                _row,
                self._lst_col_order[12],
            )
            _attributes['time_minimum'] = _model.get_value(
                _row, self._lst_col_order[13],
            )
            _attributes['time_average'] = _model.get_value(
                _row, self._lst_col_order[14],
            )
            _attributes['time_maximum'] = _model.get_value(
                _row, self._lst_col_order[15],
            )
            _attributes['cost_minimum'] = _model.get_value(
                _row, self._lst_col_order[18],
            )
            _attributes['cost_average'] = _model.get_value(
                _row, self._lst_col_order[19],
            )
            _attributes['cost_maximum'] = _model.get_value(
                _row, self._lst_col_order[20],
            )
            _attributes['confidence'] = _model.get_value(
                _row, self._lst_col_order[23],
            )
            _attributes['time_ll'] = _model.get_value(
                _row,
                self._lst_col_order[24],
            )
            _attributes['time_mean'] = _model.get_value(
                _row, self._lst_col_order[25],
            )
            _attributes['time_ul'] = _model.get_value(
                _row,
                self._lst_col_order[26],
            )
            _attributes['time_variance'] = _model.get_value(
                _row, self._lst_col_order[27],
            )
            _attributes['cost_ll'] = _model.get_value(
                _row,
                self._lst_col_order[28],
            )
            _attributes['cost_mean'] = _model.get_value(
                _row, self._lst_col_order[29],
            )
            _attributes['cost_ul'] = _model.get_value(
                _row,
                self._lst_col_order[30],
            )
            _attributes['cost_variance'] = _model.get_value(
                _row, self._lst_col_order[31],
            )

            # pylint: disable=attribute-defined-outside-init
            self._revision_id = _attributes['revision_id']
            self._validation_id = _attributes['validation_id']

            pub.sendMessage('selected_validation', attributes=_attributes)

        treeview.handler_unblock(self._lst_handler_id[0])
