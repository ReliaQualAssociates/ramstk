# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.FailureDefinition.py is part of the RTK Project
#
# All rights reserved.
"""Failure Definition List View Module."""

from pubsub import pub  # pylint: disable=E0401

# Modules required for the GUI.
import pango

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gobject, gtk
from .ListView import RTKListView


class ListView(RTKListView):
    """
    Display all the Failure Definitions associated with the selected Revision.

    The attributes of the Failure Definition List View are:

    :ivar int _revision_id: the Revision ID whose failure definitions are being
                            displayed in the List View.
    :ivar int _definition_id: the Failure Definition ID of the definition being
                              displayed in the List View.
    """

    def __init__(self, controller):
        """
        Initialize the List View for the Failure Definition package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKListView.__init__(self, controller, module='failure_definition')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._definition_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_rubber_banding(True)
        self.treeview.set_tooltip_text(
            _(u"Displays the list of failure definitions for the selected "
              u"revision."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Failure\nDefinitions") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays failure definitions for the "
              u"selected revision."))

        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _do_change_row(self, treeview):
        """
        Handle row changes for the Failure Definition package List View.

        This method is called whenever a Failure Definition List View
        RTKTreeView() row is activated or changed.

        :param treeview: the Failure Definition List View RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._definition_id = _model.get_value(_row, 0)

        treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Failure Definition List View RTKTreeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
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
        RTKListView._do_edit_cell(__cell, path, new_text, position, model)

        # Update the Failure Definition data model.
        _definition_id = model[path][0]
        _definition = \
            self._dtc_data_controller.request_select(_definition_id)
        _definition.definition = str(new_text)

        return False

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Failure Definition record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _definition_id = _model.get_value(_row, 0)

        if not self._dtc_data_controller.request_delete(_definition_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to delete failure "
                        u"definition {0:d} to Revision {1:d}.").\
                format(_definition_id, self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _do_request_insert(self, __button):
        """
        Request to add a Failure Definition record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self._dtc_data_controller.request_insert(self._revision_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to add a failure "
                        u"definition to Revision {0:d}.").\
                format(self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _do_request_update(self, __button):
        """
        Request to update the currently selected Failure Definition record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update(self._definition_id)

    def _do_request_update_all(self, __button):
        """
        Request to update all Failure Definitions records.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self._dtc_data_controller.request_update_all():
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to save the failure "
                        u"definitions for Revision {0:d}.").\
                format(self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _make_buttonbox(self):
        """
        Make the buttonbox for the Failure Definition List View.

        :return: _buttonbox; the gtk.ButtonBox() for the Failure Definition
                             List View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Failure Definition."),
            _(u"Remove the currently selected Failure Definition."),
            _(u"Save the currently selected Failure Definition to "
              u"the open RTK Program database."),
            _(u"Save all of the Failure Definitions to the open RTK "
              u"Program database."),
            _(u"Create the Failure Definition report.")
        ]
        _callbacks = [
            self._do_request_insert, self._do_request_delete,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = ['add', 'remove', 'save', 'save-all', 'reports']

        _buttonbox = RTKListView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_treeview(self):
        """
        Set up the RTKTreeView() for Failure Definitions.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.treeview.set_model(_model)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Definition\nNumber</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        self.treeview.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 1)
        _cell.set_property('wrap-width', 450)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._do_edit_cell, 1, _model)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Failure Definition</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        self.treeview.append_column(_column)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Failure Definition List View RTKTreeView().

        :param treeview: the Failure Definition ListView gtk.TreeView().
        :type treeview: :class:`rtk.gui.rtk.TreeView.RTKTreeView`.
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
            _menu_item.set_label(_(u"Add New Definition"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Definition"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Definition"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Definitions"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_select_revision(self, module_id):
        """
        Load the Failure Definition List View gtk.TreeModel().

        This method is called whenever a new Revision is selected in the RTK
        Module View.

        :param int module_id: the Revision ID to select the Failure
                              Definitions for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = \
            self._mdcRTK.dic_controllers['definition']
        _definitions = \
            self._dtc_data_controller.request_select_all(self._revision_id)

        _model = self.treeview.get_model()
        _model.clear()

        for _key in _definitions.nodes.keys():
            try:
                _model.append([
                    _definitions[_key].data.definition_id,
                    _definitions[_key].data.definition
                ])
            except AttributeError:
                print "FIXME: Handle AttributeError in " \
                      "gtk.gui.listviews.FailureDefinition._on_select_revision"

        return _return
