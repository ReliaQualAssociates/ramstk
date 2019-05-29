# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.Revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Module View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Revision attribute data in the RAMSTK Module Book.

    The Revision Module View displays all the Revisions associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Revision Module
    View are:

    :ivar int _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the Revision Module View.

        :param controller: the RAMSTK Master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKModuleView.__init__(self, controller, module='revision')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/revision.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_tooltip_text(_(u"Displays the list of revisions."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = ramstk.RAMSTKLabel(
            _(u"Revisions"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program revisions."))

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrollwindow, expand=False, fill=False)

        self.show_all()

        pub.subscribe(self._do_refresh_view, 'calculatedAllHardware')
        pub.subscribe(self._on_select_revision, 'openedProgram')
        pub.subscribe(self._on_select_revision, 'insertedRevision')
        pub.subscribe(self._on_select_revision, 'deletedRevision')
        pub.subscribe(self._on_edit, 'wvwEditedRevision')

    def _do_change_row(self, treeview):
        """
        Handle events for the Revision package Module View RAMSTKTreeView().

        This method is called whenever a Revision Module View RAMSTKTreeView() row
        is activated/changed.

        :param treeview: the Revision class gtk.TreeView().
        :type treeview: :class:`gtk.TreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._revision_id = _model.get_value(_row, 0)

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selectedRevision', module_id=self._revision_id)

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Revision package Module View RAMSTKTreeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :class:`gtk.CellRenderer`
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: :class:`gtk.TreeModel`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):

            _attributes = self._dtc_data_controller.request_get_attributes()

            if self._lst_col_order[position] == 17:
                _attributes['name'] = str(new_text)
            elif self._lst_col_order[position] == 20:
                _attributes['remarks'] = str(new_text)
            elif self._lst_col_order[position] == 22:
                _attributes['revision_code'] = str(new_text)

            self._dtc_data_controller.request_set_attributes(_attributes)

            pub.sendMessage(
                'mvwEditedRevision',
                index=self._lst_col_order[position],
                new_text=new_text)
        else:
            _return = True

        return _return

    def _do_refresh_view(self):
        """
        Refresh the view.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._revision_id)

        # Update Revision attributes with system-level attribute values.
        _dtc_hardware = self._mdcRAMSTK.dic_controllers['hardware']
        _sys_attributes = _dtc_hardware.request_get_attributes(1)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._revision_id)

        _attributes['availability_logistics'] = _sys_attributes[
            'availability_logistics']
        _attributes['availability_mission'] = _sys_attributes[
            'availability_mission']
        _attributes['cost'] = _sys_attributes['total_cost']
        _attributes['cost_per_failure'] = _sys_attributes['cost_failure']
        _attributes['cost_per_hour'] = _sys_attributes['cost_hour']
        _attributes['hazard_rate_active'] = _sys_attributes[
            'hazard_rate_active']
        _attributes['hazard_rate_dormant'] = _sys_attributes[
            'hazard_rate_dormant']
        _attributes['hazard_rate_logistics'] = _sys_attributes[
            'hazard_rate_logistics']
        _attributes['hazard_rate_mission'] = _sys_attributes[
            'hazard_rate_mission']
        _attributes['mtbf_logistics'] = _sys_attributes['mtbf_logistics']
        _attributes['mtbf_mission'] = _sys_attributes['mtbf_mission']
        _attributes['n_parts'] = _sys_attributes['total_part_count']
        _attributes['reliability_logistics'] = _sys_attributes[
            'reliability_logistics']
        _attributes['reliability_mission'] = _sys_attributes[
            'reliability_mission']
        self._dtc_data_controller.request_set_attributes(
            self._revision_id, _attributes)
        self._dtc_data_controller.request_do_update(self._revision_id)

        _model.set(_row, self._lst_col_order[1],
                   _attributes['availability_logistics'])
        _model.set(_row, self._lst_col_order[2],
                   _attributes['availability_mission'])
        _model.set(_row, self._lst_col_order[3], _attributes['cost'])
        _model.set(_row, self._lst_col_order[4],
                   _attributes['cost_per_failure'])
        _model.set(_row, self._lst_col_order[5], _attributes['cost_per_hour'])
        _model.set(_row, self._lst_col_order[6],
                   _attributes['hazard_rate_active'])
        _model.set(_row, self._lst_col_order[7],
                   _attributes['hazard_rate_dormant'])
        _model.set(_row, self._lst_col_order[8],
                   _attributes['hazard_rate_mission'])
        _model.set(_row, self._lst_col_order[9],
                   _attributes['hazard_rate_logistics'])
        _model.set(_row, self._lst_col_order[14], _attributes['mtbf_mission'])
        _model.set(_row, self._lst_col_order[15],
                   _attributes['mtbf_logistics'])
        _model.set(_row, self._lst_col_order[18],
                   _attributes['reliability_mission'])
        _model.set(_row, self._lst_col_order[19],
                   _attributes['reliability_logistics'])
        _model.set(_row, self._lst_col_order[21], _attributes['n_parts'])

        return _return

    def _do_request_delete(self, __button):
        """
        Send request to delete the selected record from the RAMSTKRevision table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _prompt = _(u"You are about to delete Revision {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._revision_id)
        _dialog = ramstk.RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                          'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_data_controller.request_do_delete(self._revision_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Revision {0:d}.").format(self._revision_id)
                _error_dialog = ramstk.RAMSTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error')
                if _error_dialog.do_run() == gtk.RESPONSE_OK:
                    _error_dialog.do_destroy()

                _return = True
        else:
            _dialog.do_destroy()

        return _return

    def _do_request_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new record to the RAMSTKRevision table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._dtc_data_controller.request_do_select(self._revision_id)

        if not self._dtc_data_controller.request_do_insert():
            self._on_select_revision()
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"Revision.")
            _error_dialog = ramstk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            self._mdcRAMSTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_insert_sibling(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new sibling Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=True)

    def _do_request_update(self, __button):
        """
        Send request to update the selected record to the RAMSTKRevision table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._revision_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Send request to save all the records to the RAMSTKRevision table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create the gtk.ButtonBox() for the Revision Module View.

        :return: _buttonbox; the gtk.ButtonBox() for the Revision class Module
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Revision."),
            _(u"Remove the currently selected Revision."),
            _(u"Save the currently selected Revision to the open "
              u"RAMSTK Program database."),
            _(u"Saves all Revisions to the open RAMSTK Program "
              u"database.")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_delete,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = ['add', 'remove', 'save', 'save-all']

        _buttonbox = RAMSTKModuleView._make_buttonbox(
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
        Set up the Revision Module View RAMSTKTreeView().

        This method sets all cells as non-editable to make the Revision Module
        View read-only.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _color = gtk.gdk.color_parse('#EEEEEE')
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            _cell.set_property('editable', False)
            _cell.set_property('cell-background-gdk', _color)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Revision Module View RAMSTKTreeView().

        :param treeview: the Revision class gtk.TreeView().
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
            _menu = gtk.Menu()
            _menu.popup(None, None, None, event.button, event.time)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['add'])
            _menu_item.set_label(_(u"Add New Revision"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert_sibling)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Revision"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Revision"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Revisions"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_edit(self, position, new_text):
        """
        Update the Module View RAMSTKTreeView() with Revision attribute changes.

        This method is called by other views when the Revision data model
        attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model, _row = self.treeview.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_select_revision(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Revision Module View RAMSTKTreeView().

        This method loads the RAMSTKTreeView() with Revision attribute data when
        an RAMSTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
                'revision']

        _revisions = self._dtc_data_controller.request_do_select_all()
        _return = RAMSTKModuleView.on_select_revision(self, tree=_revisions)
        if _return:
            _prompt = _(u"An error occured while loading Revisions into the "
                        u"Module View.")
            _dialog = ramstk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
