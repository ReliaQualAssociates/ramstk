# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Function Module View Module
-------------------------------------------------------------------------------
"""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611
from .ModuleView import RTKModuleView  # pylint: disable=E0401


class ModuleView(RTKModuleView):
    """
    The Function Module Book view displays all the Functions associated with
    the RTK Program in a flat list.  The attributes of the Function Module View
    are:

    :ivar _function_id: the ID of the currently selected Function.
    :ivar _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller):
        """
        Method to initialize the Module View for the Function package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKModuleView.__init__(self, controller, module='function')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
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
        _label = rtk.RTKLabel(
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
        Method to handle events for the Function package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
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
        Method to handle edits of the Function package Module View
        gtk.Treeview().

        :param __cell: the gtk.CellRenderer() that was edited.
        :type __cell: :py:class:`gtk.CellRenderer`
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: :py:class:`gtk.TreeModel`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not RTKModuleView._do_edit_cell(__cell, path, new_text, position,
                                           model):

            _function = self._dtc_data_controller.request_select(
                self._function_id)
            _attributes = list(_function.get_attributes())[2:]
            _attributes[self._lst_col_order[position] - 2] = str(new_text)
            _function.set_attributes(_attributes)

            pub.sendMessage(
                'mvwEditedFunction',
                index=self._lst_col_order[position],
                new_text=new_text)
        else:
            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Method to delete the selected Function and it's children.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _prompt = _(u"You are about to delete Function {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._function_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_data_controller.request_delete(self._function_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Function {0:d}.").format(self._function_id)
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
                    ssself.treeview.row_activated(_path, _column)

        else:
            _dialog.do_destroy()

        return _return

    def _do_request_insert(self, sibling=True):
        """
        Method to send request to insert a new Function into the RTK Program
        database.

        :param bool sibling: indicates whether to insert a sibling (default)
                             Function or a child Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _function = self._dtc_data_controller.request_select(self._function_id)

        if sibling:
            _parent_id = _function.parent_id
        else:
            _parent_id = _function.function_id

        # By default we add the new function as a top-level function.
        if _parent_id is None:
            _parent_id = 0

        if not self._dtc_data_controller.request_insert(
                self._revision_id, _parent_id, sibling):
            # TODO: Add code to the FMEA Class to respond to the 'insertedFunction' pubsub message and insert a set of functional failure modes.
            # TODO: Add code to the Matrix Class to respond to the 'insertedFunction' pubsub message and insert a record into each of the Function-X matrices.

            _last_id = self._dtc_data_controller.request_last_id()
            _function = self._dtc_data_controller.request_select(_last_id)
            _data = _function.get_attributes()

            _model, _row = self.treeview.get_selection().get_selected()
            _prow = _model.iter_parent(_row)
            if _function.parent_id == 0:
                _model.append(None, _data)
            elif _function.parent_id != 0 and sibling:
                _model.append(_prow, _data)
            else:  # Inserting a child.
                _model.append(_row, _data)
                _path = _model.get_path(_row)
                self.treeview.expand_row(_path, True)

            self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['function'][1] += 1
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"function to Revision "
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
        Method to send request to insert a new Function into the RTK Program
        database as child of the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._do_request_insert(False)

    def _do_request_insert_sibling(self, __button):
        """
        Method to send request to insert a new Function into the RTK Program
        database as a sibling of the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._do_request_insert(True)

    def _do_request_update(self, __button):
        """
        Method to save the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update(self._function_id)

    def _do_request_update_all(self, __button):
        """
        Method to save all the Functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update_all()

    def _make_buttonbox(self):
        """
        Method to create the gtk.ButtonBox() for the Function class Module
        View.

        :return: _buttonbox; the gtk.ButtonBox() for the Function class Module
                 View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [
            _(u"Adds a new Function at the same hierarchy level as "
              u"the selected Function (i.e., a sibling Function)."),
            _(u"Adds a new Function one level subordinate to the "
              u"selected Function (i.e., a child function)."),
            _(u"Remove the currently selected Function."),
            _(u"Save the currently selected Function to the open "
              u"RTK Program database."),
            _(u"Saves all Functions to the open RTK Program "
              u"database.")
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
        Method for setting up the gtk.TreeView() for Functions.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        for i in [5, 15, 17]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._do_edit_cell, i,
                             self.treeview.get_model())

        return _return

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Function package Module View
        gtk.TreeView().

        :param treeview: the Function class gtk.TreeView().
        :type treeview: :py:class:`gtkTreeView`
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :type event: :py:class:`gtk.gdk.Event`
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
        Method to update the Module View RTKTreeView with changes to the
        Function data model attributes.

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model, _row = self.treeview.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_select_revision(self, module_id):  # pylint: disable=W0221
        """
        Method to load the Function Module Book view gtk.TreeModel() with
        Function information when an RTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['function']
        _functions = self._dtc_data_controller.request_select_all(
            self._revision_id)

        _return = RTKModuleView._on_select_revision(self, _functions)
        if _return:
            _prompt = _(u"An error occured while loading the Functions for "
                        u"Revision ID {0:d} into the Module "
                        u"View.").format(self._revision_id)
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
