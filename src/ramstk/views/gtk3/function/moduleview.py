# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.moduleview.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Function GTK3 module view."""

# Standard Library Imports
import datetime
from typing import Any, Dict, List

# Third Party Imports
import treelib
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
    Display Function attribute data in the RAMSTK Module Book.

    The Function Module View displays all the Functions associated with the
    connected RAMSTK Program in a flat list.  All attributes of a Function
    Module View are inherited.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Function Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKModuleView.__init__(self,
                                  configuration,
                                  logger,
                                  module='function')
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/function.png')

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id: int = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_delete, 'succeed_delete_function')
        pub.subscribe(self._on_insert, 'succeed_insert_function')
        pub.subscribe(self.do_load_tree, 'succeed_retrieve_functions')
        pub.subscribe(self._do_refresh_tree, 'wvw_editing_function')

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
                                  _("Add a new Function."),
                                  _("Remove the currently selected Function.")
                              ],
                              callbacks=[
                                  self.do_request_insert_sibling,
                                  self._do_request_delete
                              ]))
        self.pack_start(_scrolledwindow, False, False, 0)

        self.treeview.set_tooltip_text(_("Displays the list of functions."))

        RAMSTKModuleView.make_ui(self)

        _label = RAMSTKLabel(_("Functions"))
        _label.do_set_properties(width=-1,
                                 height=-1,
                                 tooltip=_("Displays the program functions."))
        self.hbx_tab_label.pack_end(_label, True, True, 0)

        self.show_all()

    # pylint: disable=unused-argument
    def _do_refresh_tree(self, node_id: List, package: Dict) -> None:
        """
        Update the module view RAMSTKTreeView() with attribute changes.

        This method is called by other views when the Function data model
        attributes are edited via their gtk.Widgets().

        :param list node_id: unused in this method.
        :param dict package: the key:value for the data being updated.
        :return: None
        :rtype: None
        """
        _dic_keys = {'name': 17, 'remarks': 20, 'function_code': 22}
        [[_key, _value]] = package.items()

        _position = self._lst_col_order[_dic_keys[_key]]

        _model, _row = self.treeview.get_selection().get_selected()
        _model.set(_row, _position, _value)

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to delete selected record from the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _("You are about to delete Function {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._function_id)
        _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                      'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_function',
                            node_id=self._function_id)

        _dialog.do_destroy()

    @staticmethod
    def _do_request_insert(**kwargs: Any) -> None:
        """
        Request insert a new Function into the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        if _sibling:
            pub.sendMessage('request_insert_function')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to update the selected record to the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_function', node_id=self._function_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Send request to save all the records to the RAMSTKFunction table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the Function Module View RAMSTKTreeView().

        :param treeview: the Function class Gtk.TreeView().
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
                _("Add Function"),
                _("Remove the Selected Function"),
                _("Save Selected Function"),
                _("Save All Functions")
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
        Handle edits of Function package Module View RAMSTKTreeview().

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
        _dic_keys = {17: 'name', 20: 'remarks', 22: 'function_code'}
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        self.treeview.do_edit_cell(self, __cell, path, new_text, position)

        pub.sendMessage('mvw_editing_function',
                        node_id=[self._function_id, -1, ''],
                        package={_key, new_text})

    def _on_insert(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Add row to module view for newly added function.

        :param int node_id: the ID of the newly added function.
        :return: None
        :rtype: None
        """
        _attributes = []
        _model = self.treeview.get_model()
        _data = tree.get_node(node_id).data['function'].get_attributes()

        for _key in self.treeview.korder:
            if _key == 'dict':
                _attributes.append(str(_data))
            else:
                try:
                    if isinstance(_data[_key], datetime.date):
                        _data[_key] = _data[_key].strftime("%Y-%m-%d")
                    _data[_key] = _data[_key].decode('utf-8')
                except (AttributeError, KeyError):
                    pass
                _attributes.append(_data[_key])

        _row = _model.append(None, _attributes)

        self.treeview.selection.select_iter(_row)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the Function package Module View RAMSTKTreeView().

        This method is called whenever a Function Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Function class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _attributes = {}

        selection.handler_block(self._lst_handler_id[0])

        _model, _row = selection.get_selected()

        _attributes['revision_id'] = _model.get_value(_row,
                                                      self._lst_col_order[0])
        _attributes['function_id'] = _model.get_value(_row,
                                                      self._lst_col_order[1])
        _attributes['availability_logistics'] = _model.get_value(
            _row, self._lst_col_order[2])
        _attributes['availability_mission'] = _model.get_value(
            _row, self._lst_col_order[3])
        _attributes['cost'] = _model.get_value(_row, self._lst_col_order[4])
        _attributes['function_code'] = _model.get_value(
            _row, self._lst_col_order[5])
        _attributes['failure_rate_logistics'] = _model.get_value(
            _row, self._lst_col_order[6])
        _attributes['failure_rate_mission'] = _model.get_value(
            _row, self._lst_col_order[7])
        _attributes['level'] = _model.get_value(_row, self._lst_col_order[8])
        _attributes['mmt'] = _model.get_value(_row, self._lst_col_order[9])
        _attributes['mcmt'] = _model.get_value(_row, self._lst_col_order[10])
        _attributes['mpmt'] = _model.get_value(_row, self._lst_col_order[11])
        _attributes['mtbf_logistics'] = _model.get_value(
            _row, self._lst_col_order[12])
        _attributes['mtbf_mission'] = _model.get_value(_row,
                                                       self._lst_col_order[13])
        _attributes['mttr'] = _model.get_value(_row, self._lst_col_order[14])
        _attributes['function_name'] = _model.get_value(
            _row, self._lst_col_order[15])
        _attributes['parent'] = _model.get_value(_row, self._lst_col_order[16])
        _attributes['remarks'] = _model.get_value(_row,
                                                  self._lst_col_order[17])
        _attributes['safety_critical'] = _model.get_value(
            _row, self._lst_col_order[18])
        _attributes['total_mode_count'] = _model.get_value(
            _row, self._lst_col_order[19])
        _attributes['total_part_count'] = _model.get_value(
            _row, self._lst_col_order[20])
        _attributes['type'] = _model.get_value(_row, self._lst_col_order[21])

        self._function_id = _attributes['function_id']

        pub.sendMessage('selected_function', attributes=_attributes)
        #pub.sendMessage('request_get_function_attributes',
        #                node_id=self._function_id,
        #                table='failure_definitions')
        #pub.sendMessage('request_get_function_attributes',
        #                node_id=self._function_id,
        #                table='usage_profile')

        selection.handler_unblock(self._lst_handler_id[0])
