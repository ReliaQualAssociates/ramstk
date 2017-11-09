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

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from .ListView import RTKListView


class ListView(RTKListView):
    """
    The Stakeholder List View displays all the stakeholder inputs
    associated with the selected Revision.  The attributes of the Stakeholder
    List View are:

    :ivar _dtc_data_controller: the
    :class:`rtk.stakeholder.Stakeholder.Stakeholder`
    data controller associated with this List View.
    :ivar _revision_id: the Revision ID whose stakeholder inputs are being
                        displayed in the List View.
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """

        RTKListView.__init__(self, controller, module='stakeholder')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._stakeholder_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_tooltip_text(
            _(u"Displays the list of stakeholder inputs for the selected "
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
            _(u"Displays stakeholder inputs for the "
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
        :type treeview: :class:`gtk.TreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._stakeholder_id = _model.get_value(_row, 1)

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

        _return = False

        if not self.treeview.do_edit_cell(__cell, path, new_text,
                                          position, model):

            _stakeholder = self._dtc_data_controller.request_select(
                self._stakeholder_id)

            # Build a list of attributes based on the type of data package.
            _attributes = [None] * 15
            for i in xrange(15):
                _attributes.insert(i, model[path][i])
                #_attributes.append(model[path][i])
                print i, self._lst_col_order[i], _attributes
            _stakeholder.set_attributes(_attributes[2:])

            if position == 4:
                try:
                    _key = max(self._mdcRTK.RTK_CONFIGURATION.RTK_AFFINITY_GROUPS.keys()) + 1
                except ValueError:
                    _key = 1
                self._mdcRTK.RTK_CONFIGURATION.RTK_AFFINITY_GROUPS[_key] = _stakeholder.group
            print _stakeholder.get_attributes()
            pub.sendMessage('EditedStakeholder',
                            index=self._lst_col_order[position],
                            new_text=new_text)
        else:
            _return = True

        return _return

    def _do_request_delete(self, __button):
        """
        Method to delete the selected Stakeholder.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _stakeholder_id = _model.get_value(_row, 0)

        if not self._dtc_data_controller.request_delete(_stakeholder_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to delete failure "
                        u"stakeholder {0:d} to Revision {1:d}.").\
                format(_stakeholder_id, self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _do_request_insert(self, __button):
        """
        Method to add a Stakeholder.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self._dtc_data_controller.request_insert(self._revision_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to add a stakeholder " \
                        u"input to Revision {0:d}.").\
                format(self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _do_request_update(self, __button):
        """
        Method to save the currently selected Stakeholder.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update(self._stakeholder_id)

    def _do_request_update_all(self, __button):
        """
        Method to save all the Stakeholders.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self._dtc_data_controller.request_update_all():
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred attempting to save the " \
                        u"stakeholder inputs for Revision {0:d}.").\
                format(self._revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _make_buttonbox(self):
        """
        Method to create the buttonbox for the Stakeholder List View.

        :return: _buttonbox; the gtk.ButtonBox() for the Stakeholder
                             List View.
        :rtype: :class:`gtk.ButtonBox`
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

    def _make_treeview(self):
        """
        Method for setting up the gtk.TreeView() for Stakeholders.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Load the Affinity Group gtk.CellRendererCombo()
        _cell = self.treeview.get_column(3).get_cell_renderers()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _owner is (Description, Group Type).
        for _index, _key in enumerate(
                self._mdcRTK.RTK_CONFIGURATION.RTK_AFFINITY_GROUPS):
            _group = self._mdcRTK.RTK_CONFIGURATION.RTK_AFFINITY_GROUPS[_key]
            _cellmodel.append([_group[0]])

        # Load the Stakeholder gtk.CellRendererCombo()
        _cell = self.treeview.get_column(10).get_cell_renderers()[0]
        _cell.set_property('has-entry', True)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        # Each _owner is (Description, Group Type).
        for _index, _key in enumerate(
                self._mdcRTK.RTK_CONFIGURATION.RTK_STAKEHOLDERS):
            _group = self._mdcRTK.RTK_CONFIGURATION.RTK_STAKEHOLDERS[_key]
            _cellmodel.append([_group[0]])

        # Set the CellRendererSpin() columns to [1, 5] step 1.
        for i in [2, 7, 8]:
            _column = self.treeview.get_column(self._lst_col_order[i])
            _cell = _column.get_cell_renderers()[0]
            _adjustment = _cell.get_property('adjustment')
            _adjustment.set_all(1, 1, 5, 1)

        for i in xrange(2, 14):
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._do_edit_cell, i,
                             self.treeview.get_model())

        self.treeview.set_rubber_banding(True)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Stakeholder package
        ListView gtk.TreeView().

        :param treeview: the Stakeholder ListView gtk.TreeView().
        :type treeview: :class:`gtk.TreeView`.
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
            _image.set_from_file(self._dic_icons['add'])
            _menu_item.set_label(_(u"Add New Stakeholder Input"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Stakeholder Input"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Stakeholder Input"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Stakeholder Inputs"))
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

        self._dtc_data_controller = \
            self._mdcRTK.dic_controllers['stakeholder']
        _stakeholders = \
            self._dtc_data_controller.request_select_all(self._revision_id)

        _model = self.treeview.get_model()
        _model.clear()

        self.treeview.do_load_tree(_stakeholders)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        return _return
