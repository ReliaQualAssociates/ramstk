# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.moduleviews.Validation.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Module View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.Utilities import date_to_ordinal
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from .ModuleView import RAMSTKModuleView


class ModuleView(RAMSTKModuleView):
    """
    Display Validation attribute data in the RAMSTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Validation Module
    View are:

    :ivar int _validation_id: the ID of the currently selected Validation.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Validation Module View.

        :param controller: the RAMSTK Master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKModuleView.__init__(self, controller, module='validation')

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/validation.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.make_treeview()
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
        _label = ramstk.RAMSTKLabel(
            _(u"Validation"),
            width=-1,
            height=-1,
            tooltip=_(u"Displays the program validation tasks."))

        self.hbx_tab_label.pack_end(_label, True, True, 0)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_tree, 'retrieved_validations')
        pub.subscribe(self._on_edit, 'wvwEditedValidation')

    def _do_change_row(self, treeview):
        """
        Handle events for the Validation package Module View RAMSTKTreeView().

        This method is called whenever a Validation Module View RAMSTKTreeView()
        row is activated/changed.

        :param treeview: the Validation class Gtk.TreeView().
        :type treeview: :class:`Gtk.TreeView`
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
        Handle edits of the Validation package Module View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: :class:`Gtk.TreeModel`
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

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._dtc_data_controller.request_do_calculate_all()

        return _return

    def _do_request_delete(self, __button):
        """
        Request to delete the selected record from the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _prompt = _(u"You are about to delete Validation {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self._validation_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            _dialog.do_destroy()
            if self._dtc_data_controller.request_do_delete(
                    self._validation_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Validation {0:d}.").format(self._validation_id)
                _error_dialog = ramstk.RAMSTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error')
                if _error_dialog.do_run() == Gtk.ResponseType.OK:
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

    def _do_request_export(self, __button):
        """
        Launch the Export assistant.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        return self.do_request_export('Validation')

    def _do_request_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Send request to insert a new record to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._dtc_data_controller.request_do_select(self._validation_id)

        if not self._dtc_data_controller.request_do_insert(
                revision_id=self._revision_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"An error occurred while attempting to add a "
                        u"Validation.")
            _error_dialog = ramstk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            self._mdcRAMSTK.debug_log.error(_prompt)

            if _error_dialog.do_run() == Gtk.ResponseType.OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_insert_sibling(self, __button, **kwargs):
        """
        Send request to insert a new sibling Validation task.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._do_request_insert(**kwargs)

    def _do_request_update(self, __button):
        """
        Send request to update the selected record to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._validation_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Send request to save all the records to the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

        return _return

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create the Gtk.ButtonBox() for the Validation Module View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Validation class
                 Module View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Validation task."),
            _(u"Remove the currently selected Validation task1."),
            _(u"Exports Verification tasks to an external file (CSV, Excel, "
              u"and text files are supported).")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_delete,
            self._do_request_export
        ]
        _icons = ['add', 'remove', 'export']

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Validation Module View RAMSTKTreeView().

        :param treeview: the Validation class Gtk.TreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :type event: :class:`Gdk.Event`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = ['add', 'remove', 'save', 'save-all']
            _labels = [
                _(u"Add Validation Task"),
                _(u"Remove the Selected Validation Task"),
                _(u"Save Selected Validation Task"),
                _(u"Save All Validation Tasks")
            ]
            _callbacks = [
                self._do_request_insert_sibling, self._do_request_delete,
                self._do_request_update, self._do_request_update_all
            ]
            RAMSTKModuleView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks)

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
            RAMSTKTreeView().
            """
            _node_id = model.get_value(row, self._lst_col_order[1])
            self._dtc_data_controller.request_get_attributes(_node_id)

        _model = self.treeview.get_model()
        _model.foreach(_load_row, self)

        return None

    def _on_edit(self, position, new_text):
        """
        Update the Module View RAMSTKTreeView() with Validation attribute changes.

        This method is called by other views when the Validation data model
        attributes are edited via their Gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            Gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_select_revision(self, module_id):
        """
        Load the Validation Module View RAMSTKTreeView().

        This method loads the RAMSTKTreeView() with Validation attribute data
        when an RAMSTK Program database is opened.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKBaseView.__init__
        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
            'validation']
        _validations = self._dtc_data_controller.request_do_select_all(
            revision_id=self._revision_id)

        _return = RAMSTKModuleView.on_select_revision(self, tree=_validations)
        if _return:
            _prompt = _(u"An error occured while loading Validation Tasks "
                        u"into the Module View.")
            _dialog = ramstk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _dialog.do_run() == self._response_ok:
                _dialog.do_destroy()

        return _return
