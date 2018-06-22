# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.moduleviews.Validation.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Validation Module View."""

# Import modules for localization support.
import gettext

from pubsub import pub

# Import other RTK modules.
from rtk.Utilities import date_to_ordinal
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .ModuleView import RTKModuleView

_ = gettext.gettext


class ModuleView(RTKModuleView):
    """
    Display Validation attribute data in the RTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RTK Program in a flat list.  The attributes of a Validation Module
    View are:

    :ivar int _validation_id: the ID of the currently selected Validation.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Validation Module View.

        :param controller: the RTK Master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKModuleView.__init__(self, controller, module='validation')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/validation.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_tooltip_text(
            _(u"Displays the list of validation "
              u"tasks."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        i = 0
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            try:
                if _cell.get_property('editable'):
                    _cell.connect('edited', self._do_edit_cell, i,
                                  self.treeview.get_model())
            except TypeError:
                pass
            i += 1

        self._img_tab.set_from_file(self._dic_icons['tab'])
        _label = rtk.RTKLabel(
            _(u"Validation"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program validation tasks."))

        self.hbx_tab_label.pack_start(self._img_tab)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self._make_buttonbox())
        self.pack_start(_scrollwindow, expand=False, fill=False)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')
        pub.subscribe(self._on_edit, 'wvwEditedValidation')

    def _do_change_row(self, treeview):
        """
        Handle events for the Validation package Module View RTKTreeView().

        This method is called whenever a Validation Module View RTKTreeView()
        row is activated/changed.

        :param treeview: the Validation class gtk.TreeView().
        :type treeview: :class:`gtk.TreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()

        self._validation_id = _model.get_value(_row, 1)

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selectedValidation', module_id=self._validation_id)

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Validation package Module View RTKTreeview().

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
                self._validation_id)

            if self._lst_col_order[position] == 2:
                _attributes['description'] = str(new_text)
            elif self._lst_col_order[position] == 3:
                _attributes['task_type'] = str(new_text)
            elif self._lst_col_order[position] == 4:
                _attributes['task_specification'] = str(new_text)
            elif self._lst_col_order[position] == 5:
                _attributes['measurement_unit'] = str(new_text)
            elif self._lst_col_order[position] == 6:
                _attributes['acceptable_minimum'] = float(new_text)
            elif self._lst_col_order[position] == 7:
                _attributes['acceptable_mean'] = float(new_text)
            elif self._lst_col_order[position] == 8:
                _attributes['acceptable_maximum'] = float(new_text)
            elif self._lst_col_order[position] == 9:
                _attributes['acceptable_variance'] = str(new_text)
            elif self._lst_col_order[position] == 10:
                _attributes['date_start'] = date_to_ordinal(new_text)
            elif self._lst_col_order[position] == 11:
                _attributes['date_end'] = date_to_ordinal(new_text)
            elif self._lst_col_order[position] == 12:
                _attributes['status'] = float(new_text)
            elif self._lst_col_order[position] == 13:
                _attributes['time_mimimum'] = str(new_text)
            elif self._lst_col_order[position] == 14:
                _attributes['time_average'] = str(new_text)
            elif self._lst_col_order[position] == 15:
                _attributes['time_maximum'] = str(new_text)
            elif self._lst_col_order[position] == 18:
                _attributes['cost_minimum'] = str(new_text)
            elif self._lst_col_order[position] == 19:
                _attributes['cost_average'] = str(new_text)
            elif self._lst_col_order[position] == 20:
                _attributes['cost_maximum'] = str(new_text)
            elif self._lst_col_order[position] == 23:
                _attributes['confidence'] = str(new_text)

            self._dtc_data_controller.request_set_attributes(
                self._validation_id, _attributes)

            pub.sendMessage(
                'mvwEditedValidation',
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
        Request to delete the selected record from the RTKValidation table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _prompt = _(u"You are about to delete Validation {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._validation_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_function.request_do_delete(self._function_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Validation {0:d}.").format(self._validation_id)
                _error_dialog = rtk.RTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error')
                if _error_dialog.do_run() == gtk.RESPONSE_OK:
                    _error_dialog.do_destroy()

                _return = True
        else:
            _dialog.do_destroy()

        return _return

    def _do_request_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new record to the RTKValidation table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _validation = self._dtc_data_controller.request_do_select(
            self._validation_id)

        if not self._dtc_data_controller.request_do_insert():
            self._on_select_validation()
            self._mdcRTK.RTK_CONFIGURATION.RTK_PREFIX['validation'][1] += 1
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"Validation.")
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            self._mdcRTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_insert_sibling(self, __button, **kwargs):
        """
        Send request to insert a new sibling Validation task.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(**kwargs)

    def _do_request_update(self, __button):
        """
        Send request to update the selected record to the RTKValidation table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update(self._validation_id)

    def _do_request_update_all(self, __button):
        """
        Send request to save all the records to the RTKValidation table.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update_all()

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create the gtk.ButtonBox() for the Validation Module View.

        :return: _buttonbox; the gtk.ButtonBox() for the Validation class
                 Module View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Validation task."),
            _(u"Remove the currently selected Validation task1."),
            _(u"Save the currently selected Validation task to the open "
              u"RTK Program database."),
            _(u"Saves all Validation tasks to the open RTK Program "
              u"database.")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_delete,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = ['add', 'remove', 'save', 'save-all']

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
        Set up the Validation RTKTreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Load the gtk.CellRendererCombo() holding the task types.
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])
        for i in range(
                len(self._mdcRTK.RTK_CONFIGURATION.RTK_VALIDATION_TYPE.values(
                ))):
            _model.append([
                self._mdcRTK.RTK_CONFIGURATION.RTK_VALIDATION_TYPE.values()[i][
                    1]
            ])

        # Load the gtk.CellRendererCombo() holding the measurement units.
        _cell = self.treeview.get_column(
            self._lst_col_order[5]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])

        for i in range(
                len(self._mdcRTK.RTK_CONFIGURATION.RTK_MEASUREMENT_UNITS.
                    values())):
            _model.append([
                self._mdcRTK.RTK_CONFIGURATION.RTK_MEASUREMENT_UNITS.values()[
                    i][1]
            ])

        # Reset the limits of adjustment on the percent complete
        # gtk.CellRendererSpin() to 0 - 100 with steps of 1.
        _cell = self.treeview.get_column(
            self._lst_col_order[12]).get_cell_renderers()[0]
        _cell.set_property('digits', 0)
        _adjustment = _cell.get_property('adjustment')
        _adjustment.configure(0, 0, 100, 1, 0, 0)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Validation Module View RTKTreeView().

        :param treeview: the Validation class gtk.TreeView().
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
            _image.set_from_file(self._dic_icons['add'])
            _menu_item.set_label(_(u"Add New Validation"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Validation"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Selected Validation"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save-all'])
            _menu_item.set_label(_(u"Save All Validations"))
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
            Load the row associated with the selected Validation task.

            This is a helper function to allow iterative updating of the
            RTKTreeView().
            """
            _node_id = model.get_value(row, self._lst_col_order[1])
            _attributes = self._dtc_data_controller.request_get_attributes(
                _node_id)

            #model.set(row, self._lst_col_order[35],
            #          _attributes['hazard_rate_active'])

        _model = self.treeview.get_model()
        _model.foreach(_load_row, self)

        return None

    def _on_edit(self, position, new_text):
        """
        Update the Module View RTKTreeView() with Validation attribute changes.

        This method is called by other views when the Validation data model
        attributes are edited via their gtk.Widgets().

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
        Load the Validation Module View RTKTreeView().

        This method loads the RTKTreeView() with Validation attribute data when
        an RTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['validation']
        _validations = self._dtc_data_controller.request_do_select_all(
            revision_id=self._revision_id)

        _return = RTKModuleView.on_select_revision(self, tree=_validations)
        if _return:
            _prompt = _(u"An error occured while loading Validation Tasks "
                        u"into the Module View.")
            _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['error'],
                                           'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
