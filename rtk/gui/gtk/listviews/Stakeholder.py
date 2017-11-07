# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.Stakeholder.py is part of the RTK Project
#
# All rights reserved.
"""
Stakeholder List View Module
-------------------------------------------------------------------------------
"""

from pubsub import pub  # pylint: disable=E0401

# Modules required for the GUI.
import pango  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from .ListView import RTKListView


class ListView(RTKListView):
    """
    The Stakeholder List View displays all the failure definitions
    associated with the selected Revision.  The attributes of the Failure
    Definition List View are:

    :ivar _dtc_stakeholder: the
    :py:class:`rtk.stakeholder.Stakeholder.Stakeholder`
    data controller associated with this List View.
    :ivar _revision_id: the Revision ID whose failure definitions are being
                        displayed in the List View.
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKListView.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_stakeholder = None
        self._revision_id = None
        self._definition_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        _bg_color = '#FFFFFF'
        _fg_color = '#000000'
        _fmt_file = controller.RTK_CONFIGURATION.RTK_CONF_DIR + \
            '/' + controller.RTK_CONFIGURATION.RTK_FORMAT_FILE['stakeholder']
        _fmt_path = "/root/tree[@name='Stakeholder']/column"

        self.treeview = rtk.RTKTreeView(_fmt_path, 0, _fmt_file, _bg_color,
                                        _fg_color)

        self.treeview.set_rubber_banding(True)
        self.treeview.set_tooltip_text(
            _(u"Displays the list of failure definitions for the selected "
              u"revision."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        # _icon = gtk.gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
        #                                              22, 22)
        # _image = gtk.Image()
        # _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Stakeholder\nInputs") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays failure definitions for the "
              u"selected revision."))

        # self.hbx_tab_label.pack_start(_image)
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
        Method to handle events for the Stakeholder package List View
        gtk.TreeView().  It is called whenever a Stakeholder List View
        gtk.TreeView() row is activated.

        :param treeview: the Stakeholder List View gtk.TreeView().
        :type treeview: :py:class:`gtk.TreeView`
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
        Method to handle edits of the Stakeholder List View
        gtk.Treeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        RTKListView._do_edit_cell(__cell, path, new_text, position, model)

        # Update the Stakeholder data model.
        _definition_id = model[path][0]
        _definition = \
            self._dtc_stakeholder.request_select(_definition_id)
        _definition.definition = str(new_text)

        return False

    def _do_request_delete(self, __button):
        """
        Method to delete the selected Stakeholder.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _definition_id = _model.get_value(_row, 0)

        if not self._dtc_stakeholder.request_delete(_definition_id):
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
        Method to add a Stakeholder.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self._dtc_stakeholder.request_insert(self._revision_id):
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
        Method to save the currently selected Stakeholder.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_stakeholder.request_update(self._definition_id)

    def _do_request_update_all(self, __button):
        """
        Method to save all the Stakeholders.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self._dtc_stakeholder.request_update_all():
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
        Method to create the buttonbox for the Stakeholder List View.

        :return: _buttonbox; the gtk.ButtonBox() for the Stakeholder
                             List View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [
            _(u"Add a new Stakeholder."),
            _(u"Remove the currently selected Stakeholder."),
            _(u"Save the currently selected Stakeholder to "
              u"the open RTK Program database."),
            _(u"Save all of the Stakeholders to the open RTK "
              u"Program database."),
            _(u"Create the Stakeholder report.")
        ]
        _callbacks = [
            self._do_request_insert, self._do_request_delete,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = ['add', 'remove', 'save', 'save-all', 'reports']

        _buttonbox = RTKListView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Stakeholder package
        ListView gtk.TreeView().

        :param treeview: the Stakeholder ListView gtk.TreeView().
        :type treeview: :py:class:`gtk.TreeView`.
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
        Method to load the Stakeholder List View gtk.TreeModel() with
        Stakeholder information whenever a new Revision is selected.

        :param int revision_id: the Revision ID to select the Failure
                                Definitions for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._revision_id = module_id

        self._dtc_stakeholder = \
            self._mdcRTK.dic_controllers['definition']
        _definitions = \
            self._dtc_stakeholder.request_select_all(self._revision_id)

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
                      "gtk.gui.listviews.Stakeholder._on_select_revision"

        return _return
