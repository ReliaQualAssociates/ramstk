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

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub                              # pylint: disable=E0401

# Modules required for the GUI.
import pango                                        # pylint: disable=E0401
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
from gui.gtk import rtk                             # pylint: disable=E0401

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List View displays all the matrices and lists associated with the
    Revision Class.  The attributes of a List View are:

    :ivar _lst_handler_id: the list of gtk.Widget() signal IDs.
    :ivar _mdcRTK: the current instance of the RTK master data controller.
    :ivar _configuration: the current instance of
                          :py:class:`Configuration.Configuration`
    :ivar _dtc_failure_definition: the
    :py:class:`rtk.failure_definition.FailureDefinition.FailureDefinition`
    data controller associated with this ListView.
    :ivar _revision_id: the Revision ID whose information is being displayed
                        in the ModuleBook.
    :ivar tvw_definition: the :py:class:`gtk.TreeView` to display the Failure
                          Definitions for the selected Revision.
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.VBox.__init__(self)

        # Initialize private dictionary attributes.
        self._dic_icons = {'tab':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/revision.png',
                           'mission':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/mission.png',
                           'phase':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/phase.png',
                           'environment':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/environment.png',
                           'add':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/add.png',
                           'remove':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/remove.png',
                           'save':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/save.png',
                           'error':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/error.png'}

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._dtc_failure_definition = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tvw_definition = gtk.TreeView()

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvw_definition.set_model(_model)

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
        self.tvw_definition.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 1)
        _cell.set_property('wrap-width', 450)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_cell_edited, 1, _model)
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
        self.tvw_definition.append_column(_column)

        self.tvw_definition.set_rubber_banding(True)
        self.tvw_definition.set_tooltip_text(
            _(u"Displays the list of failure definitions for the selected "
              u"revision."))
        self.tvw_definition.connect('button_press_event',
                                    self._on_button_press)

        _icon = gtk.gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
                                                     22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Failure\nDefinitions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays failure definitions for the "
                                  u"selected revision."))

        self.hbx_tab_label = gtk.HBox()
        # self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _toolbar = self._create_toolbar()

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.tvw_definition)

        self.pack_start(_toolbar, expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _create_toolbar(self):
        """
        Creates the toolbar for the Failure Definition ListView.

        :return: _toolbar: the gtk.Toolbar() for the Failure Definition
                          ListView.
        :rtype: :py:class:`gtk.Toolbar`
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add new definition button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Add a new failure definition."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['add'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_insert)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Deletes the selected failure "
                                   u"definition."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['remove'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_delete)
        _toolbar.insert(_button, _position)
        _position += 1

        # Save button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Save changes to the failure "
                                   u"definitions."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['save'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_update_all)
        _toolbar.insert(_button, _position)

        _toolbar.show_all()

        return _toolbar

    def _on_select_revision(self, revision_id):
        """
        Method to load the Failure Definition List View gtk.TreeModel() with
        Failure Definition information whenever a new Revision is selected.

        :param int revision_id: the Revision ID to select the Failure
                                Definitions for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._dtc_failure_definition = \
            self._mdcRTK.dic_controllers['definition']
        _definitions = \
            self._dtc_failure_definition.request_select_all(revision_id)

        _model = self.tvw_definition.get_model()
        _model.clear()
        for _key in _definitions.nodes.keys():
            if _key != 0:
                _model.append([_definitions[_key].data.definition_id,
                               _definitions[_key].data.definition])
            else:
                _return = True

        _row = _model.get_iter_root()
        self.tvw_definition.expand_all()
        self.tvw_definition.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvw_definition.get_column(0)
            self.tvw_definition.row_activated(_path, _column)

        self._revision_id = revision_id

        return _return

    @staticmethod
    def _on_button_press(__treeview, event):
        """
        Method for handling mouse clicks on the Failure Definition package
        ListView gtk.TreeView().

        :param __treeview: the Failure Definition ListView gtk.TreeView().
        :type __treeview: :py:class:`gtk.TreeView`.
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

        if event.button == 1:
            pass
        elif event.button == 3:
            # FIXME: See bug 190.
            pass

        return False

    def _on_cell_edited(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Revision package Module Book
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

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))
        _definition_id = model[path][0]

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Now update the Failure Definition data model.
        _definition = \
            self._dtc_failure_definition.request_select(_definition_id)
        _definition.definition = str(new_text)

        return False

    def _request_insert(self, __button):
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

    def _request_delete(self, __button):
        """
        Method to delete the selected Failure Definition.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.tvw_definition.get_selection().get_selected()
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

    def _request_update_all(self, __button):
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
