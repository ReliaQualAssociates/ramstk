# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.Hardware.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Module View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Hardware attribute data in the RAMSTK Module Book.

    The Hardware Module Book view displays all the Hardwares associated with
    the RAMSTK Program in a flat list.  The attributes of the Hardware Module
    View are:

    :ivar int _hardware_id: the ID of the currently selected Hardware.
    :ivar int _parent_id: the ID if the parent Hardware item of the selected
                          Hardware.
    :ivar int _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Module View for the Hardware package.

        :param controller: the RAMSTK Master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKModuleView.__init__(self, controller, module='hardware')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/hardware.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._parent_id = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.make_treeview()
        self.treeview.set_tooltip_text(
            _(u"Displays the hierarchical list of "
              u"hardware items."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = ramstk.RAMSTKLabel(
            _(u"Hardware"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the hierarchical list of hardware items."))

        self.hbx_tab_label.pack_end(_label)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_tree, 'deleted_hardware')
        pub.subscribe(self.do_load_tree, 'inserted_hardware')
        pub.subscribe(self.do_load_tree, 'retrieved_hardware')
        pub.subscribe(self._do_refresh_tree, 'calculated_hardware')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_hardware')

    def _do_refresh_tree(self, attributes):
        """
        Load the new attribute values for the entire tree after calculating.

        :return: None
        :rtype: None
        """
        for _key in [
                'hazard_rate_percent', 'lambdaBP', 'Cac',
                'hazard_rate_logistics', 'lambdaBD', 'hazard_rate_software',
                'total_power_dissipation', 'Cl', 'temperature_junction', 'piP',
                'Cgs', 'reliability_miss_variance', 'piCYC', 'piU',
                'cost_failure', 'B1', 'B2', 'piNR', 'hazard_rate_dormant',
                'comp_ref_des', 'Csf', 'Csc', 'voltage_ratio', 'Cst', 'Csw',
                'Csv', 'total_cost', 'piCV', 'piCR', 'temperature_case',
                'hr_mission_variance', 'piCD', 'piCF', 'reliability_mission',
                'hazard_rate_active', 'mtbf_log_variance', 'Ccw', 'Ccv', 'Cpd',
                'Ccp', 'Cpf', 'piR', 'overstress', 'reason', 'Ccs', 'Ccf',
                'Cpv', 'Cbl', 'availability_mission', 'piQ', 'Cf',
                'temperature_hot_spot', 'Clc', 'hr_logistics_variance',
                'cost_hour', 'lambda_b', 'lambdaCYC', 'Cd',
                'reliability_logistics', 'C2', 'C1', 'Crd', 'Cmu',
                'current_ratio', 'avail_mis_variance', 'Ck', 'Ci', 'Ch', 'Cn',
                'Cm', 'Cc', 'Cb', 'Cg', 'Ce', 'mtbf_logistics', 'power_ratio',
                'Cy', 'Cbv', 'Cbt', 'reliability_log_variance', 'Cs', 'piTAPS',
                'Cq', 'Cp', 'Cw', 'Cv', 'Ct', 'Cnw', 'hr_specified_variance',
                'Cnp', 'total_part_count', 'Csz', 'Calt', 'lambdaEOS',
                'hazard_rate_mission', 'avail_log_variance', 'piK', 'piL',
                'piM', 'piN', 'Cr', 'Cga', 'piA', 'piC', 'piE', 'piF', 'A1',
                'A2', 'Cgp', 'piS', 'piT', 'Cgt', 'piV', 'Cgv', 'piPT',
                'mtbf_miss_variance', 'hr_active_variance', 'mtbf_mission',
                'piMFG', 'Cgl', 'piI', 'Cdc', 'Cdl', 'hr_dormant_variance',
                'Cdt', 'Cdw', 'Cdp', 'Cds', 'availability_logistics', 'Cdy',
                'temperature_rise'
        ]:
            self.do_refresh_tree(self._hardware_id, _key, attributes[_key])

        return None

    def _do_request_calculate_all(self, __button):
        """
        Request to calculate all Hardware inputs.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'request_calculate_all_hardware',
            node_id=self._hardware_id,
            hr_multiplier=self._mdcRAMSTK.RAMSTK_CONFIGURATION.
            RAMSTK_HR_MULTIPLIER)

        return None

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Hardware and it's children.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(u"You are about to delete Hardware {0:d} and all "
                    u"data associated with it.  Is this really what "
                    u"you want to do?").format(self._hardware_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            pub.sendMessage(
                'request_delete_hardware', node_id=self._hardware_id)

        _dialog.do_destroy()

        return None

    def _do_request_export(self, __button):
        """
        Launch the Export assistant.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        return self.do_request_export('Hardware')

    def _do_request_insert(self, **kwargs):
        """
        Send request to insert a new Hardware into the RAMSTK Program database.

        :param bool sibling: indicates whether to insert a sibling (default)
                             Hardware item or a child Hardware item.
        :param int part: indicates whether the item to insert is an
                         assembly (default) or a component/part.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']
        _part = kwargs['part']
        _return = False

        if _sibling:
            _parent_id = self._parent_id,
        else:
            _parent_id = self._hardware_id,

        pub.sendMessage(
            'request_insert_hardware',
            revision_id=self._revision_id,
            parent_id=_parent_id,
            part=_part)

        return None

    def _do_request_insert_child(self, button, **kwargs):
        """
        Send request to insert a new child Hardware assembly.

        :param button: the gtk.ToolButton() that called this method.
        :type button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if button.get_property('name') == 'assembly':
            _part = 0
        else:
            _part = 1

        return self._do_request_insert(sibling=False, part=_part, **kwargs)

    def _do_request_insert_sibling(self, button, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new sibling Hardware assembly.

        :param button: the gtk.ToolButton() that called this method.
        :type button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if button.get_property('name') == 'assembly':
            _part = 0
        else:
            _part = 1

        return self._do_request_insert(sibling=True, part=_part)

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_hardware', node_id=self._hardware_id)
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Send request to save all the Hardwares.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Hardware class Module View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Module
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Adds a new Hardware assembly at the same hierarchy level as "
              u"the selected Hardware (i.e., a sibling Hardware)."),
            _(u"Adds a new Hardware assembly one level subordinate to the "
              u"selected Hardware (i.e., a child hardware)."),
            _(u"Adds a new Hardware component/piece-part at the same "
              u"hierarchy level as the selected Hardware component/piece-part "
              u"(i.e., a sibling component/piece-part)."),
            _(u"Adds a new Hardware component/piece-part one level "
              u"subordinate to selected Hardware component/piece-part "
              u"(i.e., a child component/piece-part)."),
            _(u"Remove the currently selected Hardware item and any "
              u"children."),
            _(u"Calculate the entire system."),
            _(u"Exports Hardware to an external file (CSV, Excel, and text "
              u"files are supported).")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete, self._do_request_calculate_all,
            self._do_request_export
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'insert_part', 'insert_part',
            'remove', 'calculate_all', 'export'
        ]

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        _buttons = _buttonbox.get_children()
        _buttons[0].set_property('name', 'assembly')
        _buttons[1].set_property('name', 'assembly')
        _buttons[2].set_property('name', 'part')
        _buttons[3].set_property('name', 'part')

        return _buttonbox

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Hardware package Module View RAMSTKTreeView().

        :param treeview: the Hardware Module View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :type event: :class:`gtk.gdk.Event`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = [
                'insert_sibling', 'insert_child', 'insert_part', 'insert_part',
                'calculate_all', 'remove', 'save', 'save-all'
            ]
            _labels = [
                _(u"Add Sibling Assembly"),
                _(u"Add Child Assembly"),
                _(u"Add Sibling Piece Part"),
                _(u"Add Child Piece Part"),
                _(u"Calculate the System"),
                _(u"Remove the Selected Hardware"),
                _(u"Save Selected Hardware"),
                _(u"Save All Hardware")
            ]
            _callbacks = [
                self._do_request_insert_sibling, self._do_request_insert_child,
                self._do_request_insert_sibling, self._do_request_insert_child,
                self._do_request_calculate_all, self._do_request_delete,
                self._do_request_update, self._do_request_update_all
            ]
            RAMSTKModuleView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Hardware package Module View RAMSTKTreeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :class:`gtk.CellRenderer`
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: :class:`gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _dic_keys = {
            2: 'alt_part_num',
            3: 'cage_code',
            4: 'comp_ref_des',
            5: 'cost',
            8: 'description',
            9: 'duty_cycle',
            10: 'figure_number',
            11: 'lcn',
            12: 'level',
            14: 'mission_time',
            15: 'name',
            16: 'nsn',
            17: 'page_number',
            19: 'part',
            20: 'part_number',
            21: 'quantity',
            22: 'ref_des',
            23: 'remarks',
            24: 'repairable',
            25: 'specification_number',
            26: 'tagged_part',
            27: 'total_part_count',
            28: 'total_power_dissipation',
            29: 'year_of_manufacture',
            30: 'add_adj_factor',
            40: 'hazard_rate_software',
            41: 'hazard_rate_specified',
            46: 'hr_specified_variance',
            47: 'location_parameter',
            50: 'mtbf_specified',
            53: 'mtbf_spec_variance',
            54: 'mult_adj_factor',
            55: 'reliability_goal',
            60: 'scale_parameter',
            61: 'shape_parameter'
        }

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):
            try:
                _key = _dic_keys[self._lst_col_order[position]]
            except KeyError:
                _key = None

            pub.sendMessage(
                'mvw_editing_hardware',
                module_id=self._hardware_id,
                key=_key,
                value=new_text)

        return None

    def _on_row_change(self, treeview):
        """
        Handle events for the Hardware package Module Book RAMSTKTreeView().

        This method is called whenever a Module Book RAMSTKTreeView() row is
        activated.

        :param treeview: the Hardware Module View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _attributes = eval(_model.get_value(_row, _model.get_n_columns() - 1))

        self._hardware_id = _attributes['hardware_id']
        self._parent_id = _attributes['parent_id']
        self._revision_id = _attributes['revision_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_hardware', attributes=_attributes)

        return None
