# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.listviews.Stakeholder.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder List View."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from .ListView import RAMSTKListView


class ListView(RAMSTKListView):
    """
    Display all the Stakeholder Inputs associated with the selected Stakeholder.

    The Stakeholder List View displays all the stakeholder inputs associated
    with the selected Stakeholder.  The attributes of the Stakeholder List View
    are:

    :ivar int _revision_id: the Revision ID whose stakeholder inputs are being
                            displayed in the List View.
    :ivar int _stakeholder_id: the Stakeholder ID of the input being displayed
                               in the List View.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the List View for the Stakeholder package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKListView.__init__(self, controller, module='stakeholder')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._stakeholder_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_tooltip_text(
            _(u"Displays the list of stakeholder inputs for the selected "
              u"revision."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        _label = Gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Stakeholder\nInputs") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays stakeholder inputs for the "
              u"selected revision."))

        self.hbx_tab_label.pack_end(_label, True, True, 0)
        self.hbx_tab_label.show_all()

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_start(self._make_buttonbox(, True, True, 0), expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._do_load_requirements, 'retrieved_requirements')
        pub.subscribe(self.do_load_tree, 'deleted_stakeholder')
        pub.subscribe(self.do_load_tree, 'inserted_stakeholder')
        pub.subscribe(self.do_load_tree, 'retrieved_stakeholders')
        pub.subscribe(self._do_refresh_tree, 'calculated_stakeholder')

    def _do_load_requirements(self, tree):
        """
        Load the requirement ID list when Requirements are retrieved.

        :return: None
        :rtype: None
        """
        _cell = self.treeview.get_column(
            self._lst_col_order[9]).get_cell_renderers()[0]
        _model = _cell.get_property('model')
        _model.clear()

        for _key in tree.nodes:
            try:
                _model.append([tree.nodes[_key].data.requirement_id])
            except AttributeError:
                pass

        return None

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

        return None

    def _do_request_calculate(self, __button):
        """
        Request to calculate the selected Stakeholder input.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'request_calculate_stakeholder', node_id=self._stakeholder_id)

        return None

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

        return None

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Stakeholder.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(u"You are about to delete Stakeholder input {0:d} and "
                    u"all data associated with it.  Is this really what you "
                    u"want to do?").format(self._stakeholder_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage(
                'request_delete_stakeholder', node_id=self._stakeholder_id)

        _dialog.do_destroy()

        return None

    def _do_request_insert(self, **kwargs):
        """
        Request to add a Stakeholder.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        pub.sendMessage(
            'request_insert_stakeholder', revision_id=self._revision_id)

        return None

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
            'request_update_stakeholder', node_id=self._stakeholder_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

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

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the buttonbox for the Stakeholder List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Stakeholder
                             List View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Stakeholder input."),
            _(u"Remove the currently selected Stakeholder input."),
            _(u"Calculate the currently selected Stakeholder input."),
            _(u"Calculate all Stakeholder intputs."),
        ]
        _callbacks = [
            self.do_request_insert_sibling, self._do_request_delete,
            self._do_request_calculate, self._do_request_calculate_all
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
            width=-1)

        return _buttonbox

    def _make_treeview(self):
        """
        Set up the RAMSTKTreeView() for Stakeholders.

        :return: None
        :rtype: None
        """
        # Load the Affinity Group Gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[4]).get_cell_renderers()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _group is (Description, Group Type).
        for _index, _key in enumerate(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_AFFINITY_GROUPS):
            _group = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[
                _key]
            _cellmodel.append([_group[0]])

        # Load the Stakeholders Gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[10]).get_cell_renderers()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _owner is (Description, Group Type).
        for _index, _key in enumerate(
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_STAKEHOLDERS):
            _group = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_STAKEHOLDERS[
                _key]
            _cellmodel.append([_group[0]])

        # Set the CellRendererSpin() columns to [1, 5] step 1.
        for i in [2, 7, 8]:
            _column = self.treeview.get_column(self._lst_col_order[i])
            _cell = _column.get_cell_renderers()[0]
            _adjustment = _cell.get_property('adjustment')
            _adjustment.set_all(1, 1, 5, 1)

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
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._on_cell_edit, i,
                             self.treeview.get_model())

        self.treeview.set_rubber_banding(True)

        return None

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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _menu = Gtk.Menu()
            _menu.popup(None, None, None, event.button, event.time)

            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(self._dic_icons['add'])
            _menu_item.set_label(_(u"Add New Stakeholder Input"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Stakeholder Input"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Stakeholder Input"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = Gtk.ImageMenuItem()
            _image = Gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Stakeholder Inputs"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

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
        if not RAMSTKListView._do_edit_cell(__cell, path, new_text, position,
                                            model):

            if position == self._lst_col_order[2]:
                _key = 'customer_rank'
            elif position == self._lst_col_order[3]:
                _key = 'description'
            elif position == self._lst_col_order[4]:
                _key = 'group'
                # FIXME: See issue #60.
                try:
                    _new_key = max(self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                                   RAMSTK_AFFINITY_GROUPS.keys()) + 1
                except ValueError:
                    _new_key = 1
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_AFFINITY_GROUPS[
                    _new_key] = str(new_text)
            elif position == self._lst_col_order[7]:
                _key = 'planned_rank'
            elif position == self._lst_col_order[8]:
                _key = 'priority'
            elif position == self._lst_col_order[9]:
                _key = 'requirement_id'
            elif position == self._lst_col_order[10]:
                _key = 'stakeholder'
            elif position == self._lst_col_order[11]:
                _key = 'user_float_1'
            elif position == self._lst_col_order[12]:
                _key = 'user_float_2'
            elif position == self._lst_col_order[13]:
                _key = 'user_float_3'
            elif position == self._lst_col_order[14]:
                _key = 'user_float_4'
            elif position == self._lst_col_order[15]:
                _key = 'user_float_5'

            pub.sendMessage(
                'lvw_editing_stakeholder',
                module_id=self._stakeholder_id,
                key=_key,
                value=new_text)
        return None

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

        _attributes['revision_id'] = _model.get_value(_row,
                                                      self._lst_col_order[0])
        _attributes['stakeholder_id'] = _model.get_value(
            _row, self._lst_col_order[1])
        _attributes['customer_rank'] = _model.get_value(
            _row, self._lst_col_order[2])
        _attributes['description'] = _model.get_value(_row,
                                                      self._lst_col_order[3])
        _attributes['group'] = _model.get_value(_row, self._lst_col_order[4])
        _attributes['improvement'] = _model.get_value(_row,
                                                      self._lst_col_order[5])
        _attributes['overall_weight'] = _model.get_value(
            _row, self._lst_col_order[6])
        _attributes['planned_rank'] = _model.get_value(_row,
                                                       self._lst_col_order[7])
        _attributes['priority'] = _model.get_value(_row,
                                                   self._lst_col_order[8])
        _attributes['requirement_id'] = _model.get_value(
            _row, self._lst_col_order[9])
        _attributes['stakeholder'] = _model.get_value(_row,
                                                      self._lst_col_order[10])
        _attributes['user_float_1'] = _model.get_value(_row,
                                                       self._lst_col_order[11])
        _attributes['user_float_2'] = _model.get_value(_row,
                                                       self._lst_col_order[12])
        _attributes['user_float_3'] = _model.get_value(_row,
                                                       self._lst_col_order[13])
        _attributes['user_float_4'] = _model.get_value(_row,
                                                       self._lst_col_order[14])
        _attributes['user_float_5'] = _model.get_value(_row,
                                                       self._lst_col_order[15])

        self._revision_id = _attributes['revision_id']
        self._stakeholder_id = _attributes['stakeholder_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_stakeholder', attributes=_attributes)

        return None
