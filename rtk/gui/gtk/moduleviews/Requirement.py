# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Requirement.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Requirement Module View."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611
from .ModuleView import RTKModuleView  # pylint: disable=E0401


class ModuleView(RTKModuleView):
    """
    Display Requirement attribute data in the RTK Module Book.

    The Requirement Module Book view displays all the Requirements associated
    with the RTK Program in a hierarchical list.  The attributes of the
    Requriements Module View are:

    :ivar _requirement_id: the ID of the currently selected Requirement.
    :ivar _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller):
        """
        Initialize the Requirement Module View.

        :param controller: the RTK Master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKModuleView.__init__(self, controller, module='requirement')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/requirement.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._requirement_id = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_tooltip_text(
            _(u"Displays the hierarchical list of "
              u"requirements."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = rtk.RTKLabel(
            _(u"Requirements"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program requirements."))

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrollwindow, expand=False, fill=False)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_edit, 'wvwEditedRequirement')

    def _do_change_cell(self, cell, __path, new_iter, position):
        """
        Handle edits of the Requirement Module View gtk.CellRendererCombo()s.

        :param __cell: the gtk.CellRendererCombo() that was edited.
        :type __cell: :class:`gtk.CellRendererCombo`
        :param str __path: the gtk.TreeView() path of the
                           gtk.CellRendererCombo() that was edited.
        :param str new_iter: the new gtk.TreeITer() selected in the changed
                             gtk.CellRendererCombo().
        :param int position: the column position of the edited
                             gtk.CellRendererConbo().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = cell.get_property('model')
        _new_value = _model.get_value(new_iter, 0)

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._requirement_id)

        if self._lst_col_order[position] == 5:
            _attributes['owner'] = str(_new_value)
        elif self._lst_col_order[position] == 8:
            _attributes['priority'] = str(_new_value)
        elif self._lst_col_order[position] == 11:
            _attributes['requirement_type'] = str(_new_value)

        self._dtc_data_controller.request_set_attributes(
            self._requirement_id, _attributes)

        pub.sendMessage(
            'mvwEditedRequirement',
            index=self._lst_col_order[position],
            new_text=_new_value)

        return _return

    def _do_change_row(self, treeview):
        """
        Handle events for the Requirement Module View RTKTreeView().

        This method is called whenever a Module View RTKTreeView() row is
        activated or changed.

        :param treeview: the Requirement class RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._requirement_id = _model.get_value(_row, 1)

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selectedRequirement', module_id=self._requirement_id)

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Requirement package Module View RTKTreeView().

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
                self._requirement_id)

            if self._lst_col_order[position] == 2:
                _attributes['derived'] = str(new_text)
            elif self._lst_col_order[position] == 3:
                _attributes['description'] = str(new_text)
            elif self._lst_col_order[position] == 4:
                _attributes['figure_number'] = str(new_text)
            elif self._lst_col_order[position] == 6:
                _attributes['page_number'] = str(new_text)
            elif self._lst_col_order[position] == 10:
                _attributes['specification'] = str(new_text)
            elif self._lst_col_order[position] == 12:
                _attributes['validated'] = str(new_text)
            elif self._lst_col_order[position] == 13:
                _attributes['validated_date'] = str(new_text)

            _error_code, \
                _msg = self._dtc_data_controller.request_set_attributes(
                    self._requirement_id, _attributes)

            if _error_code == 0:
                pub.sendMessage(
                    'mvwEditedRequirement',
                    index=self._lst_col_order[position],
                    new_text=new_text)
            else:
                _return = True
        else:
            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Requirement and it's children.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _prompt = _(u"You are about to delete Requirement {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._requirement_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_data_controller.request_delete(self._requirement_id):
                _prompt = _(
                    u"An error occurred when attempting to delete "
                    u"Requirement {0:d}.").format(self._requirement_id)
                _error_dialog = rtk.RTKMessageDialog(
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

    def _do_request_insert(self, sibling=True):
        """
        Request to insert a new Requirement into the RTK Program database.

        :param bool sibling: indicates whether to insert a sibling (default)
                             Requirement or a child Requirement.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _requirement = self._dtc_data_controller.request_select(
            self._requirement_id)

        if sibling:
            _parent_id = _requirement.parent_id
        else:
            _parent_id = _requirement.requirement_id

        # By default we add the new requirement as a top-level requirement.
        if _parent_id is None:
            _parent_id = 0

        if not self._dtc_data_controller.request_insert(
                self._revision_id, _parent_id, sibling):
            # TODO: Add code to the Matrix Class to respond to the 'insertedRequirement' pubsub message and insert a record into each of the Requirement-X matrices.

            _last_id = self._dtc_data_controller.request_last_id()
            _requirement = self._dtc_data_controller.request_select(_last_id)
            _data = _requirement.get_attributes()

            _model, _row = self.treeview.get_selection().get_selected()
            _prow = _model.iter_parent(_row)
            if _parent_id == 0:
                _model.append(None, _data)
            elif _parent_id != 0 and sibling:
                _model.append(_prow, _data)
            else:  # Inserting a child.
                _model.append(_row, _data)
                _path = _model.get_path(_row)
                self.treeview.expand_row(_path, True)

            self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['requirement'][1] += 1
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"requirement to Revision "
                        u"{0:d}.").format(self._revision_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            self._mdcRTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_insert_child(self, __button):
        """
        Request to insert a child Requirement of the selected Requirement.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(False)

    def _do_request_insert_sibling(self, __button):
        """
        Request to insert a sibling Requirement of the selected Requirement.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(True)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Requirement.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update(self._requirement_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all the Requirements.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update_all()

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Requirement Module View.

        :return: _buttonbox; the gtk.ButtonBox() for the Requirement class
                 Module View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Adds a new Requirement at the same hierarchy level as the "
              u"selected Requirement (i.e., a sibling Requirement)."),
            _(u"Adds a new Requirement one level subordinate to the selected "
              u"Requirement (i.e., a derived requirement)."),
            _(u"Remove the currently selected Requirement."),
            _(u"Save the currently selected Requirement to the open RTK "
              u"Program database."),
            _(u"Saves all Requirements to the open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete, self._do_request_update,
            self._do_request_update_all
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'remove', 'save', 'save-all'
        ]

        _buttonbox = RTKModuleView._make_buttonbox(self, _icons, _tooltips,
                                                   _callbacks, 'vertical')

        return _buttonbox

    def _make_treeview(self):
        """
        Set up the gtk.TreeView() for Requirements.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Load the Owner gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[5]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _owner is (Description, Group Type).
        for _index, _key in enumerate(
                self._mdcRTK.RTK_CONFIGURATION.RTK_WORKGROUPS):
            _owner = self._mdcRTK.RTK_CONFIGURATION.RTK_WORKGROUPS[_key]
            _cellmodel.append([_owner[0]])

        # Load the Priority gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[8]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Priority can be 1 - 5.
        for i in range(1, 6):
            _cellmodel.append([str(i)])

        # Load the Requirements Type gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[11]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _type is (Code, Description, Type).
        for _index, _key in enumerate(
                self._mdcRTK.RTK_CONFIGURATION.RTK_REQUIREMENT_TYPE):
            _type = self._mdcRTK.RTK_CONFIGURATION.RTK_REQUIREMENT_TYPE[_key]
            _cellmodel.append([_type[1]])

        for i in [3, 4, 6, 10]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._do_edit_cell, i,
                             self.treeview.get_model())

        for i in [5, 8, 11]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('changed', self._do_change_cell, i)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Requirement Module View RTKTreeView().

        :param treeview: the Requirement class RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`
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
            _menu_item.set_label(_(u"Add Sibling Requirement"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_child'])
            _menu_item.set_label(_(u"Add Child Requirement"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Requirement"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Requirement"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Requirements"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_edit(self, position, new_text):
        """
        Update the Requirement Module View RTKTreeView.

        This method updates the Module View RTKTreeView with changes to the
        Requirement data model attributes.  It is called when Requirement
        attributes are changed in other views.

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model, _row = self.treeview.get_selection().get_selected()

        _model.set_value(_row, self._lst_col_order[position], new_text)

        return False

    def _on_select_revision(self, module_id):  # pylint: disable=W0221
        """
        Load the Requirement Module View gtk.TreeModel().

        This method is called whenever an RTK Program database is opened or a
        Revision is selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['requirement']
        _requirements = self._dtc_data_controller.request_select_all(
            self._revision_id)

        _return = RTKModuleView._on_select_revision(self, _requirements)
        if _return:
            _prompt = _(u"An error occured while loading the Requirements for "
                        u"Revision ID {0:d} into the Module "
                        u"View.").format(self._revision_id)
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
