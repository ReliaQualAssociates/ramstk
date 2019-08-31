# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Revision GTK3 module view."""

# Standard Library Imports
from typing import Any

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKLabel, RAMSTKMessageDialog, RAMSTKModuleView,
    RAMSTKTreeView, do_make_buttonbox
)


class ModuleView(RAMSTKModuleView):
    """
    Display Revision attribute data in the RAMSTK Module Book.

    The Revision Module View displays all the Revisions associated with the
    connected RAMSTK Program in a flat list.  All attributes of a Revision
    Module View are inherited.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, **kwargs: Any) -> None:
        """
        Initialize the Revision Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKModuleView.__init__(self,
                                  configuration,
                                  logger,
                                  module='revision')
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/revision.png')

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_tree, 'succeed_delete_revision')
        pub.subscribe(self.do_load_tree, 'succeed_insert_revision')
        pub.subscribe(self.do_load_tree, 'succeed_retrieve_revisions')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_revision')

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            do_make_buttonbox(self,
                              icons=['add', 'remove'],
                              tooltips=[
                                  _("Add a new Revision."),
                                  _("Remove the currently selected Revision.")
                              ],
                              callbacks=[
                                  self.do_request_insert_sibling,
                                  self._do_request_delete
                              ]))
        self.pack_start(_scrolledwindow, False, False, 0)

        self.treeview.set_tooltip_text(_("Displays the list of revisions."))

        RAMSTKModuleView.make_ui(self)

        _label = RAMSTKLabel(_("Revisions"))
        _label.do_set_properties(width=-1,
                                 height=-1,
                                 tooltip=_("Displays the program revisions."))
        self.hbx_tab_label.pack_end(_label, True, True, 0)

        self.show_all()

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to delete selected record from the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _("You are about to delete Revision {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._revision_id)
        _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                      'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_revision',
                            node_id=self._revision_id)

        _dialog.do_destroy()

    @staticmethod
    def _do_request_insert(**kwargs: Any) -> None:
        """
        Request insert a new Revision into the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        if _sibling:
            pub.sendMessage('request_insert_revision')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to update the selected record to the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_revision', node_id=self._revision_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKRevision table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_revisions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Revision Module View RAMSTKTreeView().

        :param treeview: the Revision class Gtk.TreeView().
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
            _icons = ['add']
            _labels = [
                _("Add Revision"),
                _("Remove the Selected Revision"),
                _("Save Selected Revision"),
                _("Save All Revisions")
            ]
            _callbacks = [self.do_request_insert_sibling]

            RAMSTKModuleView.on_button_press(self,
                                             event,
                                             icons=_icons,
                                             labels=_labels,
                                             callbacks=_callbacks)

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of Revision package Module View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the
            Gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the edited
            Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        _dic_keys = {17: 'name', 20: 'remarks', 22: 'revision_code'}
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(self, __cell, path, new_text, position)

        pub.sendMessage('mvw_editing_revision',
                        module_id=self._revision_id,
                        key=_key,
                        value=new_text)

    def _on_row_change(self, treeview: RAMSTKTreeView) -> None:
        """
        Handle events for the Revision package Module View RAMSTKTreeView().

        This method is called whenever a Revision Module View RAMSTKTreeView()
        row is activated/changed.

        :param treeview: the Revision class Gtk.TreeView().
        :type treeview: :class:`Gtk.TreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        _attributes['revision_id'] = _model.get_value(_row,
                                                      self._lst_col_order[0])
        _attributes['availability_logistics'] = _model.get_value(
            _row, self._lst_col_order[1])
        _attributes['availability_mission'] = _model.get_value(
            _row, self._lst_col_order[2])
        _attributes['cost'] = _model.get_value(_row, self._lst_col_order[3])
        _attributes['cost_per_failure'] = _model.get_value(
            _row, self._lst_col_order[4])
        _attributes['cost_per_hour'] = _model.get_value(
            _row, self._lst_col_order[5])
        _attributes['hazard_rate_active'] = _model.get_value(
            _row, self._lst_col_order[6])
        _attributes['hazard_rate_dormant'] = _model.get_value(
            _row, self._lst_col_order[7])
        _attributes['hazard_rate_logistics'] = _model.get_value(
            _row, self._lst_col_order[8])
        _attributes['hazard_rate_mission'] = _model.get_value(
            _row, self._lst_col_order[9])
        _attributes['hazard_rate_software'] = _model.get_value(
            _row, self._lst_col_order[10])
        _attributes['mmt'] = _model.get_value(_row, self._lst_col_order[11])
        _attributes['mcmt'] = _model.get_value(_row, self._lst_col_order[12])
        _attributes['mpmt'] = _model.get_value(_row, self._lst_col_order[13])
        _attributes['mtbf_logistics'] = _model.get_value(
            _row, self._lst_col_order[14])
        _attributes['mtbf_mission'] = _model.get_value(_row,
                                                       self._lst_col_order[15])
        _attributes['mttr'] = _model.get_value(_row, self._lst_col_order[16])
        _attributes['name'] = _model.get_value(_row, self._lst_col_order[17])
        _attributes['reliability_logistics'] = _model.get_value(
            _row, self._lst_col_order[18])
        _attributes['reliability_mission'] = _model.get_value(
            _row, self._lst_col_order[19])
        _attributes['remarks'] = _model.get_value(_row,
                                                  self._lst_col_order[20])
        _attributes['n_parts'] = _model.get_value(_row,
                                                  self._lst_col_order[21])
        _attributes['revision_code'] = _model.get_value(
            _row, self._lst_col_order[22])
        _attributes['program_time'] = _model.get_value(_row,
                                                       self._lst_col_order[23])
        _attributes['program_time_sd'] = _model.get_value(
            _row, self._lst_col_order[24])
        _attributes['program_cost'] = _model.get_value(_row,
                                                       self._lst_col_order[25])
        _attributes['program_cost_sd'] = _model.get_value(
            _row, self._lst_col_order[26])

        self._revision_id = _attributes['revision_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_revision', attributes=_attributes)
        pub.sendMessage('request_get_revision_attributes',
                        node_id=self._revision_id,
                        table='failure_definitions')
        pub.sendMessage('request_get_revision_attributes',
                        node_id=self._revision_id,
                        table='usage_profile')
