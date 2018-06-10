# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Hardware.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Module View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .ModuleView import RTKModuleView


class ModuleView(RTKModuleView):
    """
    Display Hardware attribute data in the RTK Module Book.

    The Hardware Module Book view displays all the Hardwares associated with
    the RTK Program in a flat list.  The attributes of the Hardware Module View
    are:

    :ivar int _hardware_id: the ID of the currently selected Hardware.
    :ivar int _revision_id: the ID of the currently selected Revision.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Module View for the Hardware package.

        :param controller: the RTK Master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKModuleView.__init__(self, controller, module='hardware')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/hardware.png'
        self._dic_icons['insert_part'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/insert_part.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.treeview.set_tooltip_text(
            _(u"Displays the hierarchical list of "
              u"hardware items."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = rtk.RTKLabel(
            _(u"Hardware"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the hierarchical list of hardware items."))

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrollwindow, expand=False, fill=False)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_edit, 'wvwEditedHardware')
        pub.subscribe(self._on_calculate, 'calculatedHardware')

    def _do_change_row(self, treeview):
        """
        Handle events for the Hardware package Module Book RTKTreeView().

        This method is called whenever a Module Book RTKTreeView() row is
        activated.

        :param treeview: the Hardware Module View RTKTreeView().
        :type treeview: :class:`rtk.gui.gtk.rtk.TreeView.RTKTreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._hardware_id = _model.get_value(_row, 1)

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selectedHardware', module_id=self._hardware_id)

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Hardware package Module View RTKTreeview().

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
                self._hardware_id)

            if self._lst_col_order[position] == 5:
                _attributes['hardware_code'] = str(new_text)
            elif self._lst_col_order[position] == 15:
                _attributes['name'] = str(new_text)
            elif self._lst_col_order[position] == 17:
                _attributes['remarks'] = str(new_text)
            elif self._lst_col_order[position] == 18:
                _attributes['safety_critical'] = int(new_text)

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

            pub.sendMessage(
                'mvwEditedHardware',
                index=self._lst_col_order[position],
                new_text=new_text)
        else:
            _return = True

        return _return

    def _do_request_calculate_all(self, __button):
        """
        Send request to calculate all hardware items.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._dtc_data_controller.request_do_calculate_all()

        return _return

    def _do_request_delete(self, __button):
        """
        Send request to delete the selected Hardware and it's children.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _prompt = _(u"You are about to delete Hardware {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._hardware_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_data_controller.request_do_delete(self._hardware_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Hardware {0:d}.").format(self._hardware_id)
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

    def _do_request_insert(self, **kwargs):
        """
        Send request to insert a new Hardware into the RTK Program database.

        :param bool sibling: indicates whether to insert a sibling (default)
                             Hardware item or a child Hardware item.
        :param int part: indicates whether the item to insert is an
                         assembly (default) or a component/part.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _sibling = kwargs['sibling']
        _part = kwargs['part']
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        _model, _row = self.treeview.get_selection().get_selected()
        _path = _model.get_path(_row)

        if _sibling:
            _parent_id = _attributes['parent_id']
        else:
            _parent_id = _attributes['hardware_id']

        if not self._dtc_data_controller.request_do_insert(
                revision_id=self._revision_id, parent_id=_parent_id,
                part=_part):
            # TODO: Add code to the FMEA Class to respond to the 'insertedHardware' pubsub message and insert a set of hardwareal failure modes.
            # TODO: Add code to the Matrix Class to respond to the 'insertedHardware' pubsub message and insert a record into each of the Hardware-X matrices.
            self._on_select_revision(self._revision_id)
            if _part == 0:
                self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['assembly'][1] += 1
            elif _part == 1:
                self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['part'][1] += 1

            self.treeview.set_cursor(_path)

        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"hardware to Revision "
                        u"{0:d}.").format(self._revision_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            self._mdcRTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_insert_child(self, __button, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new child Hardware assembly.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(**kwargs)

    def _do_request_insert_sibling(self, __button, **kwargs):
        """
        Send request to insert a new sibling Hardware assembly.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(**kwargs)

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Hardware.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update(self._hardware_id)

    def _do_request_update_all(self, __button):
        """
        Send request to save all the Hardwares.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update_all()

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Hardware class Module View.

        :return: _buttonbox; the gtk.ButtonBox() for the Hardware class Module
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Adds a new Hardware assembly at the same hierarchy level as "
              u"the selected Hardware (i.e., a sibling Hardware)."),
            _(u"Adds a new Hardware assembly one level subordinate to the "
              u"selected Hardware (i.e., a child hardware)."),
            _(u"Adds a new Hardware component/piece-part at the same "
              u"hierarchy level as the selected Hardware component/piece-part "
              u"(i.e., a sibling component/piece-part)."),
            _(u"Adds a new Hardware component/piece-part one level "
              u"subordinate to selected Hardware component/piece-part "
              u"(i.e., a child component/piece-part)."),
            _(u"Remove the currently selected Hardware item and any "
              u"children."),
            _(u"Calculate the entire system."),
            _(u"Save the currently selected Hardware item to the open "
              u"RTK Program database."),
            _(u"Saves all Hardware items to the open RTK Program "
              u"database.")
        ]
        _callbacks = [
            self._do_request_insert_sibling(None, sibling=True, part=0),
            self._do_request_insert_child(None, sibling=False, part=1),
            self._do_request_insert_sibling(None, sibling=True, part=0),
            self._do_request_insert_child(None, sibling=False, part=1),
            self._do_request_delete, self._do_request_calculate_all,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'insert_part', 'insert_part',
            'remove', 'calculate_all', 'save', 'save-all'
        ]

        _buttonbox = RTKModuleView._make_buttonbox(
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
        Set up the Hardware Module View RTKTreeView().

        This method is used to "personalize" the basic RTKTreeView for the
        Hardware Module View.  Primarily which columns are editable.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        i = 0
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            if _cell.get_property('editable'):
                _cell.connect('edited', self._do_edit_cell,
                              i, self._lst_col_order[i],
                              self.treeview.get_model())
            i += 1

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Hardware package Module View RTKTreeView().

        :param treeview: the Hardware Module View RTKTreeView().
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
            _menu_item.set_label(_(u"Add Sibling Assembly"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate',
                               self._do_request_insert_sibling_assembly)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_child'])
            _menu_item.set_label(_(u"Add Child Assembly"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate',
                               self._do_request_insert_child_assembly)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_part'])
            _menu_item.set_label(_(u"Add Sibling Piece Part"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate',
                               self._do_request_insert_sibling_part)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_part'])
            _menu_item.set_label(_(u"Add Child Piece Part"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert_child_part)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['calculate_all'])
            _menu_item.set_label(_(u"Calculate the System"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_calculate_all)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Hardware"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Hardware"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Hardwares"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_calculate(self):
        """
        Load the new attribute values for the entire tree after calculating.

        :return: None
        :rtype: None
        """

        def _load_row(model, __path, row, self):
            """
            Load the row associated with node_id.

            This is a helper function to allow iterative updating of the
            RTKTreeView().
            """
            _node_id = model.get_value(row, self._lst_col_order[1])
            _attributes = self._dtc_data_controller.request_get_attributes(
                _node_id)

            model.set(row, self._lst_col_order[35],
                      _attributes['hazard_rate_active'])
            model.set(row, self._lst_col_order[37],
                      _attributes['hazard_rate_logistics'])
            model.set(row, self._lst_col_order[42],
                      _attributes['hr_active_variance'])
            model.set(row, self._lst_col_order[44],
                      _attributes['hr_logistics_variance'])
            model.set(row, self._lst_col_order[48],
                      _attributes['mtbf_logistics'])
            model.set(row, self._lst_col_order[49],
                      _attributes['mtbf_mission'])
            model.set(row, self._lst_col_order[51],
                      _attributes['mtbf_log_variance'])
            model.set(row, self._lst_col_order[52],
                      _attributes['mtbf_miss_variance'])
            model.set(row, self._lst_col_order[56],
                      _attributes['reliability_logistics'])
            model.set(row, self._lst_col_order[57],
                      _attributes['reliability_mission'])

        _model = self.treeview.get_model()
        _model.foreach(_load_row, self)

        return None

    def _on_edit(self, position, new_text):
        """
        Update the Module View RTKTreeView().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if position is not None:
            _model, _row = self.treeview.get_selection().get_selected()
            try:
                _model.set(_row, self._lst_col_order[position], new_text)
            except TypeError:
                _return = True

        return _return

    def _on_select_revision(self, **kwargs):
        """
        Load the Hardware Module View RTKTreeView().

        This method is called whenever an RTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._revision_id = kwargs['module_id']

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['hardware']
        _hardware = self._dtc_data_controller.request_do_select_all(
            self._revision_id)

        _return = RTKModuleView.on_select_revision(self, tree=_hardware)
        if _return:
            _prompt = _(u"An error occured while loading the Hardware for "
                        u"Revision ID {0:d} into the Module "
                        u"View.").format(self._revision_id)
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
