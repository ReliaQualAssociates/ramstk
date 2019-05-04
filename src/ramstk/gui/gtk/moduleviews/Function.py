# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.Function.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Module View."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, Gtk
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Function attribute data in the RAMSTK Module Book.

    The Function Module Book view displays all the Functions associated with
    the RAMSTK Program in a flat list.  The attributes of the Function Module
    View are:

    :ivar int _function_id: the ID of the currently selected Function.
    :ivar int _parent_id: the ID of the parent Function for the currently
                          selected Function.
    :ivar int _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Module View for the Function package.

        :param controller: the RAMSTK Master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKModuleView.__init__(self, controller, module='function')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/function.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_tree, 'deleted_function')
        pub.subscribe(self.do_load_tree, 'inserted_function')
        pub.subscribe(self.do_load_tree, 'retrieved_functions')
        pub.subscribe(self.do_refresh_tree, 'wvw_editing_function')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Function class Module View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Function class Module
                 View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Adds a new Function at the same hierarchy level as "
              u"the selected Function (i.e., a sibling Function)."),
            _(u"Adds a new Function one level subordinate to the "
              u"selected Function (i.e., a child function)."),
            _(u"Remove the currently selected Function."),
            _(u"Exports Functions to an external file (CSV, Excel, and "
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

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(self.__make_buttonbox())
        self.pack_start(_scrolledwindow, False, False, 0)

        self.make_treeview(editable=[5, 15, 17, 18])
        self.treeview.set_tooltip_text(_(u"Displays the list of functions."))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = ramstk.RAMSTKLabel(
            _(u"Functions"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program functions."))

        self.hbx_tab_label.pack_end(_label, True, True, 0)

        return None

    def __set_callbacks(self):
        """
        Set the callback functions.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        return None

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Function and it's children.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(u"You are about to delete Function {0:d} and all "
                    u"data associated with it.  Is this really what "
                    u"you want to do?").format(self._function_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage(
                'request_delete_function', node_id=self._function_id)

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
        return self.do_request_export('Function')

    def _do_request_insert(self, **kwargs):
        """
        Request insert a new Function into the RAMSTK Program database.

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
            _parent_id = self._function_id

        pub.sendMessage(
            'request_insert_function',
            revision_id=self._revision_id,
            parent_id=_parent_id)

        return None

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_function', node_id=self._function_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

        return None

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Function Module View RAMSTKTreeView().

        :param treeview: the Function Module View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was
                      clicked).

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
        # _on_change_row is called from here, it gets called twice.
        # Once on the currently selected row and once on the newly
        # selected row.  Thus, we don't need (or want) to respond to
        # left button clicks.
        if event.button == 3:
            _icons = [
                'insert_sibling', 'insert_child', 'remove', 'save', 'save-all'
            ]
            _labels = [
                _(u"Add Sibling Function"),
                _(u"Add Child Function"),
                _(u"Remove the Selected Function"),
                _(u"Save Selected Function"),
                _(u"Save All Functions")
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
        Handle edits of Function package Module View RAMSTKTreeview().

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
        _dic_keys = {
            5: 'function_code',
            15: 'name',
            17: 'remarks',
            18: 'safety_critical'
        }

        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):
            try:
                _key = _dic_keys[self._lst_col_order[position]]
            except KeyError:
                _key = None

            pub.sendMessage(
                'mvw_editing_function',
                module_id=self._function_id,
                key=_key,
                value=new_text)

        return None

    def _on_row_change(self, treeview):
        """
        Handle events for the Function package Module Book RAMSTKTreeView().

        This method is called whenever a Module Book RAMSTKTreeView() row is
        activated.

        :param treeview: the Function Module View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

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
        _attributes['hazard_rate_logistics'] = _model.get_value(
            _row, self._lst_col_order[6])
        _attributes['hazard_rate_mission'] = _model.get_value(
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
        _attributes['name'] = _model.get_value(_row, self._lst_col_order[15])
        _attributes['parent_id'] = _model.get_value(_row,
                                                    self._lst_col_order[16])
        _attributes['remarks'] = _model.get_value(_row,
                                                  self._lst_col_order[17])
        _attributes['safety_critical'] = _model.get_value(
            _row, self._lst_col_order[18])
        _attributes['total_mode_count'] = _model.get_value(
            _row, self._lst_col_order[19])
        _attributes['total_part_count'] = _model.get_value(
            _row, self._lst_col_order[20])
        _attributes['type_id'] = _model.get_value(_row,
                                                  self._lst_col_order[21])

        # pylint: disable=attribute-defined-outside-init
        self._function_id = _attributes['function_id']
        self._parent_id = _attributes['parent_id']
        self._revision_id = _attributes['revision_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_function', attributes=_attributes)

        return None
