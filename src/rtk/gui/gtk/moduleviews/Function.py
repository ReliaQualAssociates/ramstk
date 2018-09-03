# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Function.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Function Module View."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Function attribute data in the RAMSTK Module Book.

    The Function Module Book view displays all the Functions associated with
    the RAMSTK Program in a flat list.  The attributes of the Function Module View
    are:

    :ivar int _function_id: the ID of the currently selected Function.
    :ivar int _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Module View for the Function package.

        :param controller: the RAMSTK Master data controller instance.
        :type controller: :class:`rtk.RAMSTK.RAMSTK`
        """
        RAMSTKModuleView.__init__(self, controller, module='function')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/function.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_tooltip_text(_(u"Displays the list of functions."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = rtk.RAMSTKLabel(
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

        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_edit, 'wvwEditedFunction')

    def _do_change_row(self, treeview):
        """
        Handle events for the Function package Module Book RAMSTKTreeView().

        This method is called whenever a Module Book RAMSTKTreeView() row is
        activated.

        :param treeview: the Function Module View RAMSTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RAMSTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._function_id = _model.get_value(_row, 1)

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selectedFunction', module_id=self._function_id)

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Function package Module View RAMSTKTreeview().

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

            _attributes = self._dtc_data_controller.request_get_attributes(
                self._function_id)

            if self._lst_col_order[position] == 5:
                _attributes['function_code'] = str(new_text)
            elif self._lst_col_order[position] == 15:
                _attributes['name'] = str(new_text)
            elif self._lst_col_order[position] == 17:
                _attributes['remarks'] = str(new_text)
            elif self._lst_col_order[position] == 18:
                _attributes['safety_critical'] = int(new_text)

            self._dtc_data_controller.request_set_attributes(
                self._function_id, _attributes)

            pub.sendMessage(
                'mvwEditedFunction',
                index=self._lst_col_order[position],
                new_text=new_text)
        else:
            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Send request to delete the selected Function and it's children.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _prompt = _(u"You are about to delete Function {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._function_id)
        _dialog = rtk.RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_data_controller.request_do_delete(self._function_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Function {0:d}.").format(self._function_id)
                _error_dialog = rtk.RAMSTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error')
                if _error_dialog.do_run() == gtk.RESPONSE_OK:
                    _error_dialog.do_destroy()

                _return = True
            else:
                _model, _row = self.treeview.get_selection().get_selected()
                _prow = _model.iter_parent(_row)
                _model.remove(_row)

                if _prow is not None:
                    _path = _model.get_path(_prow)
                    _column = self.treeview.get_column(0)
                    self.treeview.set_cursor(_path, None, False)
                    self.treeview.row_activated(_path, _column)

        else:
            _dialog.do_destroy()

        return _return

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
        Send request to insert a new Function into the RAMSTK Program database.

        :param bool sibling: indicates whether to insert a sibling (default)
                             Function or a child Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _sibling = kwargs['sibling']
        _return = False

        _function = self._dtc_data_controller.request_do_select(
            self._function_id)

        if _sibling:
            _parent_id = _function.parent_id
        else:
            _parent_id = _function.function_id

        if not self._dtc_data_controller.request_do_insert(
                self._revision_id, _parent_id):
            # TODO: Add code to the FMEA Class to respond to the 'insertedFunction' pubsub message and insert a set of functional failure modes.
            # TODO: Add code to the Matrix Class to respond to the 'insertedFunction' pubsub message and insert a record into each of the Function-X matrices.
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"function to Revision "
                        u"{0:d}.").format(self._revision_id)
            _error_dialog = rtk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            self._mdcRAMSTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_insert_child(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new chid Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(sibling=False)

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
        Send request to save the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._function_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Send request to save all the Functions.

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
            _(u"Exports Functions to an external file (CSV, Excel, and text "
              u"files are supported).")
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
        Set up the Function Module View RAMSTKTreeView().

        This method sets all cells as non-editable to make the Function Module
        View read-only.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _color = gtk.gdk.color_parse('#EEEEEE')
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            try:
                _cell.set_property('editable', False)
            except TypeError:
                _cell.set_property('activatable', False)
            _cell.set_property('cell-background-gdk', _color)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Function package Module View RAMSTKTreeView().

        :param treeview: the Function Module View RAMSTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RAMSTKTreeView`
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
            _image.set_from_file(self._dic_icons['insert_sibling'])
            _menu_item.set_label(_(u"Add Sibling Function"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_child'])
            _menu_item.set_label(_(u"Add Child Function"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Function"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Function"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Functions"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_edit(self, position, new_text):
        """
        Update the Module View RAMSTKTreeView().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model, _row = self.treeview.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_select_revision(self, module_id):
        """
        Load the Function Module View RAMSTKTreeView().

        This method is called whenever an RAMSTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers['function']
        _functions = self._dtc_data_controller.request_do_select_all(
            revision_id=self._revision_id)

        _return = RAMSTKModuleView.on_select_revision(self, tree=_functions)
        if _return:
            _prompt = _(u"An error occured while loading the Functions for "
                        u"Revision ID {0:d} into the Module "
                        u"View.").format(self._revision_id)
            _dialog = rtk.RAMSTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
