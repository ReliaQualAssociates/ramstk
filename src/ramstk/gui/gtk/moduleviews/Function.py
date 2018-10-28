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
from ramstk.gui.gtk.ramstk.Widget import _, gtk
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
        self._dic_icons['tab'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/function.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None
        self._parent_id = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.make_treeview(editable=[5, 15, 17, 18])
        self.treeview.set_tooltip_text(_(u"Displays the list of functions."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_change))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = ramstk.RAMSTKLabel(
            _(u"Functions"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program functions."))

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrollwindow, expand=False, fill=False)

        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_tree, 'retrieved_functions')
        pub.subscribe(self._do_load_tree, 'deleted_function')
        pub.subscribe(self._do_load_tree, 'inserted_function')
        pub.subscribe(self._do_refresh_tree, 'editing_function')

    def _do_load_tree(self, tree):
        """
        Load the Function Module View RAMSTKTreeView().

        This method is called in response to the 'retrieved_functions'.

        :param tree: the treelib Tree containing the Functions to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        if self.treeview.do_load_tree(tree):
            _prompt = _(u"An error occured while loading the Functions "
                        u"for Revision ID {0:d} into the Module "
                        u"View.").format(self._revision_id)
            _dialog = ramstk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return None

    def _do_refresh_tree(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Refresh the data in the Function Module View RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        _column = [
            _index for _index, _key in enumerate(self.treeview.korder)
            if _key == key
        ][0]

        _model, _row = self.treeview.get_selection().get_selected()
        _model.set_value(_row, _column, value)

        return None

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Function and it's children.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _(u"You are about to delete Function {0:d} and all "
                    u"data associated with it.  Is this really what "
                    u"you want to do?").format(self._function_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            pub.sendMessage(
                'request_delete_function', node_id=self._function_id)

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

    def _do_request_insert_child(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Request to insert a new chid Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        return self._do_request_insert(sibling=False)

    def _do_request_insert_sibling(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Request to insert a new sibling Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        return self._do_request_insert(sibling=True)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_function', node_id=self._function_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Function class Module View.

        :return: _buttonbox; the gtk.ButtonBox() for the Function class Module
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Adds a new Function at the same hierarchy level as "
              u"the selected Function (i.e., a sibling Function)."),
            _(u"Adds a new Function one level subordinate to the "
              u"selected Function (i.e., a child function)."),
            _(u"Remove the currently selected Function."),
            _(u"Save the currently selected Function to the open "
              u"RAMSTK Program database."),
            _(u"Saves all Functions to the open RAMSTK Program "
              u"database."),
            _(u"Exports Functions to an external file (CSV, Excel, and "
              u"text files are supported).")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete, self._do_request_update,
            self._do_request_update_all, self._do_request_export
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'remove', 'save', 'save-all',
            'export'
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

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Function Module View RAMSTKTreeView().

        :param treeview: the Function Module View RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was
                      clicked).

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

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :class:`gtk.CellRenderer`
        :param str path: the gtk.TreeView() path of the
                         gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the edited
                             gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs
                      to.
        :type model: :class:`gtk.TreeStore`
        :return: None
        :rtype: None
        """
        if not self.treeview.do_edit_cell(__cell, path, new_text, position,
                                          model):
            if self._lst_col_order[position] == 5:
                _key = 'function_code'
            elif self._lst_col_order[position] == 15:
                _key = 'name'
            elif self._lst_col_order[position] == 17:
                _key = 'remarks'
            elif self._lst_col_order[position] == 18:
                _key = 'safety_critical'

            pub.sendMessage(
                'editing_function',
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

        _model, _row = treeview.get_selection().get_selected()

        _attributes['revision_id'] = _model.get_value(_row, 0)
        _attributes['function_id'] = _model.get_value(_row, 1)
        _attributes['availability_logistics'] = _model.get_value(_row, 2)
        _attributes['availability_mission'] = _model.get_value(_row, 3)
        _attributes['cost'] = _model.get_value(_row, 4)
        _attributes['function_code'] = _model.get_value(_row, 5)
        _attributes['hazard_rate_logistics'] = _model.get_value(_row, 6)
        _attributes['hazard_rate_mission'] = _model.get_value(_row, 7)
        _attributes['level'] = _model.get_value(_row, 8)
        _attributes['mmt'] = _model.get_value(_row, 9)
        _attributes['mcmt'] = _model.get_value(_row, 10)
        _attributes['mpmt'] = _model.get_value(_row, 11)
        _attributes['mtbf_logistics'] = _model.get_value(_row, 12)
        _attributes['mtbf_mission'] = _model.get_value(_row, 13)
        _attributes['mttr'] = _model.get_value(_row, 14)
        _attributes['name'] = _model.get_value(_row, 15)
        _attributes['parent_id'] = _model.get_value(_row, 16)
        _attributes['remarks'] = _model.get_value(_row, 17)
        _attributes['safety_critical'] = _model.get_value(_row, 18)
        _attributes['total_mode_count'] = _model.get_value(_row, 19)
        _attributes['total_part_count'] = _model.get_value(_row, 20)
        _attributes['type_id'] = _model.get_value(_row, 21)

        self._function_id = _attributes['function_id']

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_function', attributes=_attributes)

        return None
