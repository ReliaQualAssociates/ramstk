# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Revision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Revision Module View Module
-------------------------------------------------------------------------------
"""

# Import modules for localization support.
import gettext

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk                         # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from .ModuleView import RTKModuleView           # pylint: disable=E0401

_ = gettext.gettext


class ModuleView(RTKModuleView):
    """
    The Module Book view displays all the Revisions associated with the RTK
    Project in a flat list.  The attributes of a Module View are:

    :ivar _dtc_data_controller: the :py:class:`rtk.revision.Revision.Revision`
                                data controller to use for accessing the
                                Revision data models.
    :ivar _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller):
        """
        Method to initialize the Module Book view for the Revision package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKModuleView.__init__(self, controller, module='revision')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
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
        _label = rtk.RTKLabel(_(u"Revisions"), width=-1, height=-1,
                              tooltip=_(u"Displays the program revisions."))

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrollwindow, expand=False, fill=False)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'openedProgram')
        pub.subscribe(self._on_select_revision, 'insertedRevision')
        pub.subscribe(self._on_select_revision, 'deletedRevision')
        pub.subscribe(self._on_edit, 'wvwEditedRevision')

    def _do_change_row(self, treeview):
        """
        Method to handle events for the Revision package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param treeview: the Revision class gtk.TreeView().
        :type treeview: :py:class:`gtk.TreeView`
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
        Method to handle edits of the Revision package Module View
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

        if not self.treeview.do_edit_cell(__cell, path, new_text,
                                          position, model):

            _revision = self._dtc_data_controller.request_select(
                self._revision_id)
            _attributes = list(_revision.get_attributes())[2:]
            _attributes[self._lst_col_order[position] - 2] = str(new_text)
            _revision.set_attributes(_attributes)

            pub.sendMessage('mvwEditedRevision',
                            index=self._lst_col_order[position],
                            new_text=new_text)
        else:
            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Method to delete the selected Revision.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _prompt = _(u"You are about to delete Revision {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._revision_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_function.request_delete(self._function_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Revision {0:d}.").format(self._revision_id)
                _error_dialog = rtk.RTKMessageDialog(_prompt,
                                                     self._dic_icons['error'],
                                                     'error')
                if _error_dialog.do_run() == gtk.RESPONSE_OK:
                    _error_dialog.do_destroy()

                _return = True
        else:
            _dialog.do_destroy()

        return _return

    def _do_request_insert(self, __button):
        """
        Method to send request to insert a new Revision into the RTK Program
        database.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _revision = self._dtc_data_controller.request_select(self._revision_id)

        if not self._dtc_data_controller.request_insert():
            # Get the currently selected row, the level of the currently
            # selected item, and it's parent row in the Function tree.
            _model, _row = self.treeview.get_selection().get_selected()
            _prow = _model.iter_parent(_row)

            _data = _revision.get_attributes()
            _model.append(None, _data)

            self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['revision'][1] += 1
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"Revision.")
            _error_dialog = rtk.RTKMessageDialog(_prompt,
                                                 self._dic_icons['error'],
                                                 'error')
            self._mdcRTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_update(self, __button):
        """
        Method to save the currently selected Revision.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update(self._revision_id)

    def _do_request_update_all(self, __button):
        """
        Method to save all the Revisions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update_all()

    def _make_buttonbox(self):
        """
        Method to create the gtk.ButtonBox() for the Revision class Module
        View.

        :return: _buttonbox; the gtk.ButtonBox() for the Revision class Module
                 View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [_(u"Add a new Revision."),
                     _(u"Remove the currently selected Revision."),
                     _(u"Save the currently selected Revision to the open "
                       u"RTK Program database."),
                     _(u"Saves all Revisions to the open RTK Program "
                       u"database.")]
        _callbacks = [self._do_request_insert, self._do_request_delete,
                      self._do_request_update, self._do_request_update_all]
        _icons = ['add', 'remove', 'save', 'save-all']

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

        for i in [17, 20, 22]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._do_edit_cell, i,
                             self.treeview.get_model())

        return _return

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Revision package Module View
        gtk.TreeView().

        :param treeview: the Revision class gtk.TreeView().
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
            _image.set_from_file(self._dic_icons['add'])
            _menu_item.set_label(_(u"Add New Revision"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
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
        Method to update the Module Book gtk.TreeView() with changes to the
        Revision data model attributes.  Called by other views when the
        Revision data model attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model, _row = self.treeview.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_select_revision(self):                  # pylint: disable=W0221
        """
        Method to load the Revision Module Book view gtk.TreeModel() with
        Revision information when an RTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['revision']
        _revisions = self._dtc_data_controller.request_select_all()

        _return = RTKModuleView._on_select_revision(self, _revisions)
        if _return:
            _prompt = _(u"An error occured while loading Revisions into the "
                        u"Module View.")
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
