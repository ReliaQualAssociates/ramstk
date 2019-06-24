# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.SimilarItem.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RASMTK SimilarItem Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.assistants.SimilarItem import EditFunction
from ramstk.gui.gtk.ramstk import (
    RAMSTKComboBox, RAMSTKFrame, RAMSTKLabel, RAMSTKTreeView,
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
from .WorkView import RAMSTKWorkView


class SimilarItem(RAMSTKWorkView):
    """
    Display Similar Item attribute data in the Work Book.

    The WorkView displays all the attributes for the Similar Item Analysis. The
    attributes of a SimilarItem Work View are:

    :cvar dict _dic_quality: the quality levels and associated index to use in
    a Topic 633 analysis.
    :cvar dict _dic_environment: the environments and associated index to use
    in a Topic 633 analysis.

    :ivar dict _dic_hardware: dict to hold information from the Hardware
    module.
    :ivar int _hardware_id: the Hardware ID of the selected Similar Item.
    :ivar int _method_id: the ID of the similar item method to use.
    :ivar cmbSimilarItemMethod: the method (Tpoic 633 or user-defined) to use
    for the similar item analysis.

    The _lst_handler_id for the Similar Item Work View:
    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | treeview - `cursor_changed`               |
    +-------+-------------------------------------------+
    |   1   | treeview - `button_press_event`           |
    +-------+-------------------------------------------+
    |   2   | cmbSimilarItemMethod - `changed`          |
    +-------+-------------------------------------------+
    |   3   | treeview (cell) - `edited` or `toggled`   |
    +-------+-------------------------------------------+
    """
    # Define private dictionary attributes.
    _dic_quality = {
        0: '',
        1: 'Space',
        2: 'Full Military',
        3: 'Ruggedized',
        4: 'Commercial',
    }
    _dic_environment = {
        0: '',
        1: 'Ground, Benign',
        2: 'Ground,Mobile',
        3: 'Naval, Sheltered',
        4: 'Airborne, Inhabited, Cargo',
        5: 'Airborne, Rotary Wing',
        6: 'Space, Flight',
    }

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Similar Item.

        :param configuration: the RAMSTK Configuration instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKWorkView.__init__(self, configuration, module='SimilarItem')

        # Initialize private dictionary attributes.
        self._dic_icons['edit'] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR +
            '/32x32/edit.png'
        )
        self._dic_hardware = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._method_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        _fmt_file = (
            self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/' +
            self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE['similaritem']
        )
        _fmt_path = "/root/tree[@name='SimilarItem']/column"

        self.treeview = RAMSTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            '#FFFFFF',
            '#000000',
            pixbuf=False,
        )
        self._lst_col_order = self.treeview.order

        self.cmbSimilarItemMethod = RAMSTKComboBox()

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(
            self._do_load_children,
            'retrieved_similar_item_children',
        )
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self._get_hardware_attributes, 'retrieved_hardware')

    def __load_combobox(self):
        """
        Load Similar Item analysis RAMSTKComboboxes.

        :return: None
        :rtype: None
        """
        # Load the quality from and quality to Gtk.CellRendererCombo().
        for _idx in [4, 5]:
            _model = self._get_cell_model(_idx)
            for _quality in self._dic_quality.values():
                _model.append([
                    _quality,
                ])

        # Load the environment from and environment to Gtk.CellRendererCombo().
        for _idx in [6, 7]:
            _model = self._get_cell_model(_idx)
            for _environment in self._dic_environment.values():
                _model.append([
                    _environment,
                ])

        # Load the method and goal comboboxes.
        self.cmbSimilarItemMethod.do_load_combo([
            [_("Topic 633"), 0],
            [_("User-Defined"), 1],
        ])

    def __make_ui(self):
        """
        Make the Similar Item RAMSTKTreeview().

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrolledwindow.add_with_viewport(
            RAMSTKWorkView._make_buttonbox(
                self,
                icons=[
                    'edit',
                    'rollup',
                    'calculate',
                ],
                tooltips=[
                    _("Edit the Similar Item analysis functions."),
                    _("Roll up descriptions to next higher level assembly."),
                    _("Calculate the Similar Item analysis."),
                ],
                callbacks=[
                    self._do_request_edit_function,
                    self._do_request_rollup,
                    self._do_request_calculate,
                ],
            ), )
        self.pack_start(_scrolledwindow, False, False, 0)

        _hbox = Gtk.HBox()
        _fixed = Gtk.Fixed()

        _fixed.put(RAMSTKLabel(_("Select Method")), 5, 5)
        _fixed.put(self.cmbSimilarItemMethod, 5, 30)

        _frame = RAMSTKFrame(label=_("Similar Item Method"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_fixed)

        _hbox.pack_start(_frame, False, True, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame(label=_("Similar Item Analysis"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

        _hbox.pack_end(_frame, True, True, 0)

        self.pack_end(_hbox, True, True, 0)

        _label = RAMSTKLabel(
            _("SimilarItem"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays the Similar Item analysis for the selected "
                "hardware item.", ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback functions and methods for the Similar Item widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._do_change_row), )
        self._lst_handler_id.append(
            self.treeview.connect(
                'button_press_event',
                self._on_button_press,
            ), )
        self._lst_handler_id.append(
            self.cmbSimilarItemMethod.connect(
                'changed',
                self._on_combo_changed,
                2,
            ), )

        for _idx in self._lst_col_order[3:]:
            _cell = self.treeview.get_column(
                self._lst_col_order[_idx], ).get_cells()
            try:
                _cell[0].connect(
                    'edited',
                    self._on_cell_edit,
                    _idx,
                    self.treeview.get_model(),
                )
            except TypeError:
                _cell[0].connect(
                    'toggled',
                    self._on_cell_edit,
                    'new text',
                    _idx,
                    self.treeview.get_model(),
                )

    def __set_properties(self):
        """
        Set the properties of the Similar Item widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _(
                "Displays the Similar Item Analysis for the currently "
                "selected Hardware item.", ), )

        self.cmbSimilarItemMethod.do_set_properties(
            tooltip=_("Select the similar item analysis method."), )

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _columns = self.treeview.get_columns()
        for _column in _columns:
            self.treeview.remove_column(_column)

        _model.clear()

        self.cmbSimilarItemMethod.handler_block(self._lst_handler_id[2])
        self.cmbSimilarItemMethod.set_active(0)
        self.cmbSimilarItemMethod.handler_unblock(self._lst_handler_id[2])

    def _do_change_row(self, treeview):
        """
        Handle events for the Similar Item Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the SimilarItem RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeViewRAMSTKTreeView`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()
        try:
            self._hardware_id = _model.get_value(_row, 1)
        except TypeError:
            self._hardware_id = None

        treeview.handler_unblock(self._lst_handler_id[0])

    def _do_load_page(self, attributes):
        """
        Load the Similar Item Work View page.

        :param dict attributes: a dict of attributes key:value pairs for the
        displayed Hardware item's Similar Item analysis.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._parent_id = attributes['hardware_id']

        RAMSTKWorkView.on_select(
            self,
            title=_(
                "Performing Similar Item Analysis for Hardware ID "
                "{0:d}", ).format(self._parent_id),
        )

    def _do_load_children(self, children):
        """
        Load the Similar Item RAMSTKTreeView() and other widgets.

        :param list children: a list of child treelib Node()s associated with
        the Hardware item selected in the RAMSTK Module View.
        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.handler_block(self._lst_handler_id[2])
        self.cmbSimilarItemMethod.set_active(self._method_id)
        self.cmbSimilarItemMethod.handler_unblock(self._lst_handler_id[2])

        _model = self.treeview.get_model()
        _model.clear()

        _data = []
        for _child in children:
            try:
                _attributes = _child.data.get_attributes()
                _node_id = _child.identifier
                try:
                    _quality_from = self._dic_quality[
                        _attributes['quality_from_id']
                    ]
                except ValueError:
                    _quality_from = ''
                try:
                    _quality_to = self._dic_quality[
                        _attributes['quality_to_id']
                    ]
                except ValueError:
                    _quality_to = ''
                try:
                    _environment_from = self._dic_environment[
                        _attributes['environment_from_id']
                    ]
                except ValueError:
                    _environment_from = ''
                try:
                    _environment_to = self._dic_environment[
                        _attributes['environment_to_id']
                    ]
                except ValueError:
                    _environment_to = ''

                _data = [
                    self._revision_id,
                    _attributes['hardware_id'],
                    self._dic_hardware[_attributes['hardware_id']][0],
                    self._dic_hardware[_attributes['hardware_id']][1],
                    _quality_from,
                    _quality_to,
                    _environment_from,
                    _environment_to,
                    _attributes['temperature_from'],
                    _attributes['temperature_to'],
                    _attributes['change_description_1'].decode('utf-8'),
                    _attributes['change_factor_1'],
                    _attributes['change_description_2'].decode('utf-8'),
                    _attributes['change_factor_2'],
                    _attributes['change_description_3'].decode('utf-8'),
                    _attributes['change_factor_3'],
                    _attributes['change_description_4'].decode('utf-8'),
                    _attributes['change_factor_4'],
                    _attributes['change_description_5'].decode('utf-8'),
                    _attributes['change_factor_5'],
                    _attributes['change_description_6'].decode('utf-8'),
                    _attributes['change_factor_6'],
                    _attributes['change_description_7'].decode('utf-8'),
                    _attributes['change_factor_7'],
                    _attributes['change_description_8'].decode('utf-8'),
                    _attributes['change_factor_8'],
                    _attributes['change_description_9'].decode('utf-8'),
                    _attributes['change_factor_9'],
                    _attributes['change_description_10'].decode('utf-8'),
                    _attributes['change_factor_10'],
                    _attributes['function_1'],
                    _attributes['function_2'],
                    _attributes['function_3'],
                    _attributes['function_4'],
                    _attributes['function_5'],
                    _attributes['result_1'],
                    _attributes['result_2'],
                    _attributes['result_3'],
                    _attributes['result_4'],
                    _attributes['result_5'],
                    _attributes['user_blob_1'].decode('utf-8'),
                    _attributes['user_blob_2'].decode('utf-8'),
                    _attributes['user_blob_3'].decode('utf-8'),
                    _attributes['user_blob_4'].decode('utf-8'),
                    _attributes['user_blob_5'].decode('utf-8'),
                    _attributes['user_float_1'],
                    _attributes['user_float_2'],
                    _attributes['user_float_3'],
                    _attributes['user_float_4'],
                    _attributes['user_float_5'],
                    _attributes['user_int_1'],
                    _attributes['user_int_2'],
                    _attributes['user_int_3'],
                    _attributes['user_int_4'],
                    _attributes['user_int_5'],
                    _attributes['parent_id'],
                    str(_attributes),
                ]
# TODO: Handle user/debug messages in workview.SimilarItem._do_load_children
                try:
                    _model.append(None, _data)
                except TypeError:
                    _error_code = 1
                    _user_msg = _(
                        "One or more Similar Item line items "
                        "had the wrong data type in it's data "
                        "package and is not displayed in the "
                        "Similar Item analysis.", )
                    _debug_msg = (
                        "RAMSTK ERROR: Data for Similar Item ID "
                        "{0:s} for Hardware ID {1:s} is the "
                        "wrong type for one or more "
                        "columns.".format(
                            str(_node_id),
                            str(self._parent_id),
                        )
                    )
                    # TODO: Create and log a useful user and/or debug message in src/ramstk/gui/gtk/workviews/SimilarItem.py.
                    print(_data)
                except ValueError as _error:
                    _error_code = 1
                    _user_msg = _(
                        "One or more Similar Item line items "
                        "was missing some of it's data and is "
                        "not displayed in the Similar Item "
                        "analysis.", )
                    _debug_msg = (
                        "RAMSTK ERROR: Data for Similar Item ID "
                        "{0:s} for Hardware ID {1:s} is the "
                        "wrong type for one or more "
                        "columns.  Error was: {2:s}".format(
                            str(_node_id),
                            str(self._parent_id),
                            str(_error),
                        )
                    )
                    # TODO: Create and log a useful user and/or debug message in src/ramstk/gui/gtk/workviews/SimilarItem.py.
            except AttributeError:
                if _node_id != 0:
                    _error_code = 1
                    _user_msg = _(
                        "One or more Similar Item line items "
                        "was missing it's data package and is "
                        "not displayed in the Similar Item "
                        "analysis.", )
                    _debug_msg = (
                        "RAMSTK ERROR: There is no data package "
                        "for Similar Item ID {0:s} for Hardware "
                        "ID {1:s}.".format(
                            str(_node_id),
                            str(self._parent_id),
                        )
                    )
                    # TODO: Create and log a useful user and/or debug message in src/ramstk/gui/gtk/workviews/SimilarItem.py.

    def _do_refresh_tree(self, model, row, functions):
        """
        Refresh the Similar Item Work View RAMSTKTreeView functions.

        :param model:
        :param row:
        :param functions:
        :return: None
        :rtype: None
        """
        model.set_value(
            row,
            self._lst_col_order[30],
            functions[0],
        )
        model.set_value(
            row,
            self._lst_col_order[31],
            functions[1],
        )
        model.set_value(
            row,
            self._lst_col_order[32],
            functions[2],
        )
        model.set_value(
            row,
            self._lst_col_order[33],
            functions[3],
        )
        model.set_value(
            row,
            self._lst_col_order[34],
            functions[4],
        )

    def _do_request_calculate(self, __button):
        """
        Request to iteratively calculate the Similar Item metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _row = _model.get_iter_first()

        # Iterate through the hazards and calculate the Similar Item hazard
        # intensities.
        self.do_set_cursor(Gdk.CursorType.WATCH)
        while _row is not None:
            pub.sendMessage(
                'request_calculate_similar_item',
                node_id=_model.get_value(_row, 1),
                hazard_rate=_model.get_value(_row, 3),
            )
            _row = _model.iter_next(_row)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_edit_function(self, __button):
        """
        Request to edit the Similar Item analysis user-defined functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        (_model, _row) = self.treeview.get_selection().get_selected()

        _dialog = EditFunction(self.treeview, dlgparent=self.get_parent(),)

        if _dialog.do_run() == Gtk.ResponseType.OK:
            _functions = _dialog.do_set_functions(self.treeview)
            if _dialog.chkApplyAll.get_active():
                _row = _model.get_iter_first()
                while _row is not None:
                    self._do_refresh_tree(_model, _row, _functions)
                    _row = _model.iter_next(_row)
            else:
                self._do_refresh_tree(_model, _row, _functions)

        _dialog.do_destroy()

    def _do_request_rollup(self, __button):
        """
        Request to roll-up the Similar Item change descriptions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_roll_up_similar_item',
            node_id=self._parent_id,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Request to save the selected Similar Item record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_similar_item',
            node_id=self._hardware_id,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the Similar Item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_similar_items')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_set_visible(self, **kwargs):
        """
        Set the Similar Item treeview columns visible and hidden.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self.treeview.do_set_visible_columns(**kwargs)

    def _get_cell_model(self, column):
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property('model')
        _model.clear()

        return _model

    def _get_hardware_attributes(self, tree):
        """
        Retrieve the information needed from the Hardware module.

        :param tree: the treelib Tree() containing the Hardware items.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes():
            try:
                _attributes = _node.data

                self._dic_hardware[_attributes['hardware_id']] = [
                    _attributes['name'],
                    _attributes['hazard_rate_logistics'],
                ]
            except TypeError:
                pass

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Similar Item Work View RAMSTKTreeView().

        :param treeview: the Similar Item TreeView RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=[
                    'edit',
                    'calculate',
                ],
                labels=[
                    _("Edit Function"),
                    _("Calculate"),
                ],
                callbacks=[
                    self._do_request_edit_function,
                    self._do_request_calculate,
                ],
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Similar Item Work View RAMSTKTreeview().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param Gtk.TreeModel model: the Gtk.TreeModel() the Gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
        _dic_keys = {
            4: 'quality_from_id',
            5: 'quality_to_id',
            6: 'environment_from_id',
            7: 'environment_to_id',
            8: 'temperature_from',
            9: 'temperature_to',
            10: 'change_description_1',
            11: 'change_factor_1',
            12: 'change_description_2',
            13: 'change_factor_2',
            14: 'change_description_3',
            15: 'change_factor_3',
            16: 'change_description_4',
            17: 'change_factor_4',
            18: 'change_description_5',
            19: 'change_factor_5',
            20: 'change_description_6',
            21: 'change_factor_6',
            22: 'change_description_7',
            23: 'change_factor_7',
            24: 'change_description_8',
            25: 'change_factor_8',
            26: 'change_description_9',
            27: 'change_factor_9',
            28: 'change_description_10',
            29: 'change_factor_10',
            40: 'user_blob_1',
            41: 'user_blob_2',
            42: 'user_blob_3',
            43: 'user_blob_4',
            44: 'user_blob_5',
            45: 'user_float_1',
            46: 'user_float_2',
            47: 'user_float_3',
            48: 'user_float_4',
            49: 'user_float_5',
            50: 'user_int_1',
            51: 'user_int_2',
            52: 'user_int_3',
            53: 'user_int_4',
            54: 'user_int_5',
        }
        try:
            _key = _dic_keys[self._lst_col_order[position]]
        except KeyError:
            _key = ''

        if not self.treeview.do_edit_cell(
                __cell,
                path,
                new_text,
                position,
                model,
        ):

            pub.sendMessage(
                'wvw_editing_similar_item',
                module_id=self._hardware_id,
                key=_key,
                value=new_text,
            )

    def _on_combo_changed(self, combo, index):
        """
        Respond to Gtk.ComboBox() 'changed' signals.

        :param Gtk.ComboBox combo: the Gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the Gtk.ComboBox() that
                          called this method.
        :return: None
        :rtype: None
        """
        _visible = []
        _editable = []

        combo.handler_block(self._lst_handler_id[index])

        _new_text = int(combo.get_active())

        if _new_text == 1:  # Topic 633.
            _visible = [
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                35,
            ]
            _editable = [
                4,
                5,
                6,
                7,
                8,
                9,
            ]

        elif _new_text == 2:  # User-defined
            for (_index, _value) in enumerate(self.treeview.visible):
                if _value == 1:
                    _visible.append(_index)
            for (_index, _value) in enumerate(self.treeview.editable):
                if _value == 1:
                    _editable.append(_index)

        self._do_set_visible(visible=_visible, editable=_editable)
        self._method_id = _new_text

        combo.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(
            'wvw_editing_similar_item',
            module_id=self._parent_id,
            key='method_id',
            value=_new_text,
        )
