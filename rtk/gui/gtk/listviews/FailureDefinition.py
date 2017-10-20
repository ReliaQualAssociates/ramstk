# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.FailureDefinition.py is part of the RTK Project
#
# All rights reserved.
"""
###############################################################################
Failure Definition Package List Book View
###############################################################################
"""

from pubsub import pub                          # pylint: disable=E0401

# Modules required for the GUI.
import pango                                    # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk                         # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from .ListView import RTKListView


class ListView(RTKListView):
    """
    The Failure Definition List View displays all the failure definitions
    associated with the selected Revision.  The attributes of the Failure
    Definition List View are:

    :ivar _dtc_failure_definition: the
    :py:class:`rtk.failure_definition.FailureDefinition.FailureDefinition`
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
        self._dtc_failure_definition = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_rubber_banding(True)
        self.treeview.set_tooltip_text(
            _(u"Displays the list of failure definitions for the selected "
              u"revision."))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        # _icon = gtk.gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
        #                                              22, 22)
        # _image = gtk.Image()
        # _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Failure\nDefinitions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays failure definitions for the "
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

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Failure Definition List View
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

        # Update the Failure Definition data model.
        _definition_id = model[path][0]
        _definition = \
            self._dtc_failure_definition.request_select(_definition_id)
        _definition.definition = str(new_text)

        return False

    def _do_request_delete(self, __button):
        """
        Method to delete the selected Failure Definition.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _definition_id = _model.get_value(_row, 0)

        if not self._dtc_failure_definition.request_delete(_definition_id):
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
        Method to add a Failure Definition.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self._dtc_failure_definition.request_insert(self._revision_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to add a failure "
                        u"definition to Revision {0:d}.").\
                format(self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _do_request_update_all(self, __button):
        """
        Method to save all the Failure Definitions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self._dtc_failure_definition.request_update_all():
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
        Method to create the buttonbox for the Failure Definition List View.

        :return: _buttonbox; the gtk.ButtonBox() for the Failure Definition
                             List View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [_(u"Add a new Failure Definition."),
                     _(u"Remove the currently selected Failure Definition."),
                     _(u"Save the Failure Definitions to the open RTK Program "
                       u"database."),
                     _(u"Create the Failure Definition report.")]
        _callbacks = [self._do_request_insert, self._do_request_delete,
                      self._do_request_update_all]
        _icons = ['add', 'remove', 'save', 'reports']

        _buttonbox = RTKListView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_treeview(self):
        """
        Method for setting up the gtk.TreeView() for Failure Definitions.

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
        Method for handling mouse clicks on the Failure Definition package
        ListView gtk.TreeView().

        :param treeview: the Failure Definition ListView gtk.TreeView().
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

        treeview.handler_block(self._lst_handler_id[0])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            print "FIXME: Rick clicking should launch a pop-up menu with " \
                  "options to add, remove (selected), and save all in " \
                  "rtk.gui.gtk.listviews.FailureDefinition._on_button_press."

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_select_revision(self, module_id):
        """
        Method to load the Failure Definition List View gtk.TreeModel() with
        Failure Definition information whenever a new Revision is selected.

        :param int revision_id: the Revision ID to select the Failure
                                Definitions for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._revision_id = module_id

        self._dtc_failure_definition = \
            self._mdcRTK.dic_controllers['definition']
        _definitions = \
            self._dtc_failure_definition.request_select_all(self._revision_id)

        _model = self.treeview.get_model()
        _model.clear()

        for _key in _definitions.nodes.keys():
            try:
                _model.append([_definitions[_key].data.definition_id,
                               _definitions[_key].data.definition])
            except AttributeError:
                print "FIXME: Handle AttributeError in " \
                      "gtk.gui.listviews.FailureDefinition._on_select_revision"

        return _return
