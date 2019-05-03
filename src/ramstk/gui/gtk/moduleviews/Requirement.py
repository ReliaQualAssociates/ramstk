# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.Requirement.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Module View."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Requirement attribute data in the RAMSTK Module Book.

    The Requirement Module Book view displays all the Requirements associated
    with the RAMSTK Program in a hierarchical list.  The attributes of the
    Requriements Module View are:

    :ivar _requirement_id: the ID of the currently selected Requirement.
    :ivar _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Requirement Module View.

        :param controller: the RAMSTK Master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKModuleView.__init__(self, controller, module='requirement')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/requirement.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id = None
        self._requirement_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.make_treeview()
        self.treeview.set_tooltip_text(
            _(u"Displays the hierarchical list of "
              u"requirements."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = ramstk.RAMSTKLabel(
            _(u"Requirements"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program requirements."))

        self.hbx_tab_label.pack_end(_label, True, True, 0)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_tree, 'retrieved_requirements')
        pub.subscribe(self.do_load_tree, 'deleted_requirement')
        pub.subscribe(self.do_load_tree, 'inserted_requirement')
        pub.subscribe(self._do_load_code, 'created_requirement_code')
        pub.subscribe(self._do_refresh_tree, 'wvw_editing_requirement')

    def _do_load_code(self, code):
        """
        Refresh the Requirement Code Gtk.Entry().

        :param str code: the new Requirement code.
        :return: None
        :rtype: None
        """
        (_model, _row) = self.treeview.get_selection().get_selected()
        _path = _model.get_path(_row)

        _model[_path][self._lst_col_order[9]] = code

        return None

    def _do_refresh_tree(self, module_id, key, value):
        """
        Refresh the data in the Requirement RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        if key == 'requirement_type':
            value = value[1]

        return self.do_refresh_tree(module_id, key, value)

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Requirement and it's children.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(u"You are about to delete Requirement {0:d} and all "
                    u"data associated with it.  Is this really what "
                    u"you want to do?").format(self._requirement_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage(
                'request_delete_requirement', node_id=self._requirement_id)

        _dialog.do_destroy()

        return None

    def _do_request_export(self, __button):
        """
        Launch the Export assistant.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        return self.do_request_export('Requirement')

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new Requirement into the RAMSTK Program database.

        :param bool sibling: indicates whether to insert a sibling (default)
                             Requirement or a child Requirement.
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
            _parent_id = self._requirement_id

        pub.sendMessage(
            'request_insert_requirement',
            revision_id=self._revision_id,
            parent_id=_parent_id)

        return None

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Requirement.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_requirement', node_id=self._requirement_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Requirements.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_requirements')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Requirement Module View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Requirement class
                 Module View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Adds a new Requirement at the same hierarchy level as the "
              u"selected Requirement (i.e., a sibling Requirement)."),
            _(u"Adds a new Requirement one level subordinate to the selected "
              u"Requirement (i.e., a derived requirement)."),
            _(u"Remove the currently selected Requirement."),
            _(u"Exports Requirementss to an external file (CSV, Excel, and "
              u"text files are supported).")
        ]
        _callbacks = [
            self.do_request_insert_sibling, self.do_request_insert_child,
            self._do_request_delete, self._do_request_export
        ]
        _icons = ['insert_sibling', 'insert_child', 'remove', 'export']

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Requirement Module View RAMSTKTreeView().

        :param treeview: the Requirement class RAMSTKTreeView().
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
                'insert_sibling', 'insert_child', 'remove', 'save', 'save-all'
            ]
            _labels = [
                _(u"Add Sibling Requirement"),
                _(u"Add Child Requirement"),
                _(u"Remove the Selected Requirement"),
                _(u"Save Selected Requirement"),
                _(u"Save All Requirements")
            ]
            _callbacks = [
                self._do_request_insert_sibling, self._do_request_insert_child,
                self._do_request_delete, self._do_request_update,
                self._do_request_update_all
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
        Handle edits of Requirement package Module View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the
                         Gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the edited
                             Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs
                      to.
        :type model: :class:`Gtk.TreeStore`
        :return: None
        :rtype: None
        """
        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):
            if self._lst_col_order[position] == 2:
                _key = 'derived'
            elif self._lst_col_order[position] == 3:
                _key = 'description'
            elif self._lst_col_order[position] == 4:
                _key = 'figure_number'
            elif self._lst_col_order[position] == 6:
                _key = 'page_number'
            elif self._lst_col_order[position] == 10:
                _key = 'specification'
            elif self._lst_col_order[position] == 12:
                _key = 'validated'
            elif self._lst_col_order[position] == 13:
                _key = 'validated_date'

            pub.sendMessage(
                'editing_requirement',
                module_id=self._requirement_id,
                key=_key,
                value=new_text)

        return None

    def _on_row_change(self, treeview):
        """
        Handle events for the Requrement package Module Book RAMSTKTreeView().

        This method is called whenever a Module Book RAMSTKTreeView() row is
        activated.

        :param treeview: the Requirement Module View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        _attributes['revision_id'] = _model.get_value(_row,
                                                      self._lst_col_order[0])
        _attributes['requirement_id'] = _model.get_value(
            _row, self._lst_col_order[1])
        _attributes['derived'] = _model.get_value(_row, self._lst_col_order[2])
        _attributes['description'] = _model.get_value(_row,
                                                      self._lst_col_order[3])
        _attributes['figure_number'] = _model.get_value(
            _row, self._lst_col_order[4])
        _attributes['owner'] = _model.get_value(_row, self._lst_col_order[5])
        _attributes['page_number'] = _model.get_value(_row,
                                                      self._lst_col_order[6])
        _attributes['parent_id'] = _model.get_value(_row,
                                                    self._lst_col_order[7])
        _attributes['priority'] = _model.get_value(_row,
                                                   self._lst_col_order[8])
        _attributes['requirement_code'] = _model.get_value(
            _row, self._lst_col_order[9])
        _attributes['specification'] = _model.get_value(
            _row, self._lst_col_order[10])
        _attributes['requirement_type'] = _model.get_value(
            _row, self._lst_col_order[11])
        _attributes['validated'] = _model.get_value(_row,
                                                    self._lst_col_order[12])
        _attributes['validated_date'] = _model.get_value(
            _row, self._lst_col_order[13])
        _attributes['q_clarity_0'] = _model.get_value(_row,
                                                      self._lst_col_order[14])
        _attributes['q_clarity_1'] = _model.get_value(_row,
                                                      self._lst_col_order[15])
        _attributes['q_clarity_2'] = _model.get_value(_row,
                                                      self._lst_col_order[16])
        _attributes['q_clarity_3'] = _model.get_value(_row,
                                                      self._lst_col_order[17])
        _attributes['q_clarity_4'] = _model.get_value(_row,
                                                      self._lst_col_order[18])
        _attributes['q_clarity_5'] = _model.get_value(_row,
                                                      self._lst_col_order[19])
        _attributes['q_clarity_6'] = _model.get_value(_row,
                                                      self._lst_col_order[20])
        _attributes['q_clarity_7'] = _model.get_value(_row,
                                                      self._lst_col_order[21])
        _attributes['q_clarity_8'] = _model.get_value(_row,
                                                      self._lst_col_order[22])
        _attributes['q_complete_0'] = _model.get_value(_row,
                                                       self._lst_col_order[23])
        _attributes['q_complete_1'] = _model.get_value(_row,
                                                       self._lst_col_order[24])
        _attributes['q_complete_2'] = _model.get_value(_row,
                                                       self._lst_col_order[25])
        _attributes['q_complete_3'] = _model.get_value(_row,
                                                       self._lst_col_order[26])
        _attributes['q_complete_4'] = _model.get_value(_row,
                                                       self._lst_col_order[27])
        _attributes['q_complete_5'] = _model.get_value(_row,
                                                       self._lst_col_order[28])
        _attributes['q_complete_6'] = _model.get_value(_row,
                                                       self._lst_col_order[29])
        _attributes['q_complete_7'] = _model.get_value(_row,
                                                       self._lst_col_order[30])
        _attributes['q_complete_8'] = _model.get_value(_row,
                                                       self._lst_col_order[31])
        _attributes['q_complete_9'] = _model.get_value(_row,
                                                       self._lst_col_order[32])
        _attributes['q_consistent_0'] = _model.get_value(
            _row, self._lst_col_order[33])
        _attributes['q_consistent_1'] = _model.get_value(
            _row, self._lst_col_order[34])
        _attributes['q_consistent_2'] = _model.get_value(
            _row, self._lst_col_order[35])
        _attributes['q_consistent_3'] = _model.get_value(
            _row, self._lst_col_order[36])
        _attributes['q_consistent_4'] = _model.get_value(
            _row, self._lst_col_order[37])
        _attributes['q_consistent_5'] = _model.get_value(
            _row, self._lst_col_order[38])
        _attributes['q_consistent_6'] = _model.get_value(
            _row, self._lst_col_order[39])
        _attributes['q_consistent_7'] = _model.get_value(
            _row, self._lst_col_order[40])
        _attributes['q_consistent_8'] = _model.get_value(
            _row, self._lst_col_order[41])
        _attributes['q_verifiable_0'] = _model.get_value(
            _row, self._lst_col_order[42])
        _attributes['q_verifiable_1'] = _model.get_value(
            _row, self._lst_col_order[43])
        _attributes['q_verifiable_2'] = _model.get_value(
            _row, self._lst_col_order[44])
        _attributes['q_verifiable_3'] = _model.get_value(
            _row, self._lst_col_order[45])
        _attributes['q_verifiable_4'] = _model.get_value(
            _row, self._lst_col_order[46])
        _attributes['q_verifiable_5'] = _model.get_value(
            _row, self._lst_col_order[47])

        self._parent_id = _attributes['parent_id']
        self._requirement_id = _attributes['requirement_id']
        self._revision_id = _attributes['revision_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_requirement', attributes=_attributes)

        return None
