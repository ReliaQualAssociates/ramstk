# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.similar_item.workview.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK SimilarItem Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.assistants import EditFunction
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKWorkView


class SimilarItem(RAMSTKWorkView):
    """
    Display Similar Item attribute data in the Work Book.

    The WorkView displays all the attributes for the Similar Item Analysis. The
    attributes of a SimilarItem Work View are:

    :cvar dict _dic_quality: the quality levels and associated index to use in
        a Topic 633 analysis.
    :cvar dict _dic_environment: the environments and associated index to use
        in a Topic 633 analysis.
    :cvar str _module: the name of the module.

    :ivar dict _dic_hardware: dict to hold information from the Hardware
        module.
    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    :ivar int _hardware_id: the Hardware ID of the selected Similar Item.
    :ivar int _method_id: the ID of the similar item method to use.
    :ivar cmbSimilarItemMethod: the method (Topic 633 or user-defined) to use
        for the similar item analysis.
    """
    # Define private dict class attributes.
    _dic_keys = {2: 'method_id'}
    _dic_column_keys = {
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
        54: 'user_int_5'
    }
    _dic_quality = {
        0: '',
        1: 'Space',
        2: 'Full Military',
        3: 'Ruggedized',
        4: 'Commercial'
    }
    _dic_environment = {
        0: '',
        1: 'Ground, Benign',
        2: 'Ground,Mobile',
        3: 'Naval, Sheltered',
        4: 'Airborne, Inhabited, Cargo',
        5: 'Airborne, Rotary Wing',
        6: 'Space, Flight'
    }

    # Define private list class attributes.
    _lst_labels: List[str] = [_("Select Method")]
    _lst_title: List[str] = [
        _("Similar Item Method"),
        _("Similar Item Analysis")
    ]

    # Define private scalar class attributes.
    _module: str = 'similar_item'
    _tablabel: str = _("SimilarItem")
    _tabtooltip: str = _(
        "Displays the Similar Item analysis for the selected hardware item.")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Hardware Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_hardware: Dict[str, Any] = {}

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_edit_function, self._do_request_rollup,
            self._do_request_calculate
        ]
        self._lst_icons = ['edit', 'rollup', 'calculate']
        self._lst_mnu_labels = [
            _("Edit Function"),
            _("Roll-Up Descriptions"),
            _("Calculate Similar Item")
        ]
        self._lst_tooltips = [
            _("Edit the Similar Item analysis functions."),
            _("Roll up descriptions to next higher level assembly."),
            _("Calculate the Similar Item analysis.")
        ]

        # Initialize private scalar attributes.
        self._similar_item_tree: treelib.Tree = treelib.Tree()
        self._method_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbSimilarItemMethod: RAMSTKComboBox = RAMSTKComboBox()

        # TMPLT: This is the list of widgets for the workview.  The order of
        # TMPLT: the items in the list is the order they will appear on the
        # TMPLT: workview's container (generally a Gtk.Fixed()) using the
        # TMPLT: parent class' make_ui() method .  The list can be sliced if
        # TMPLT: the information is to be displayed across multiple views.  It
        # TMPLT: can also be used to make customized views.  Use this list
        # TMPLT: in conjunction with the class variable _lst_labels.
        self._lst_widgets = [self.cmbSimilarItemMethod]

        self.__set_properties()
        super().make_ui_with_treeview()
        self.__set_callbacks()
        self.__load_combobox()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_row, 'succeed_get_similar_item_attributes')

        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'do_load_similar_item')
        pub.subscribe(self._do_set_tree, 'succeed_get_hardware_tree')

    def __do_get_environment(self, environment_id: int) -> str:
        """
        Retrieve the environment name given the ID.

        :param int environment_id: the ID number of the environment to return.
        :return: _environment; the noun name of the environment.
        :rtype; str
        """
        _environment = ''
        try:
            _environment = self._dic_environment[environment_id]
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return _environment

    def __do_get_quality(self, quality_id: int) -> str:
        """
        Retrieve the quality name given the ID.

        :param int quality_id: the ID number of the quality level to return.
        :return: _quality; the noun name of the quality level.
        :rtype; str
        """
        _quality = ''
        try:
            _quality = self._dic_quality[quality_id]
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return _quality

    def __load_combobox(self) -> None:
        """
        Load Similar Item analysis RAMSTKComboBox()s.

        :return: None
        :rtype: None
        """
        # Load the quality from and quality to Gtk.CellRendererCombo().
        for _idx in [4, 5]:
            _model = self._get_cell_model(_idx)
            for _quality in self._dic_quality.values():
                _model.append([_quality])

        # Load the environment from and environment to Gtk.CellRendererCombo().
        for _idx in [6, 7]:
            _model = self._get_cell_model(_idx)
            for _environment in self._dic_environment.values():
                _model.append([_environment])

        # Load the method combobox.
        self.cmbSimilarItemMethod.do_load_combo(
            [[_("Topic 633"), 0], [_("User-Defined"), 1]], signal='changed')

    def __set_callbacks(self) -> None:
        """
        Set the callback functions and methods for the Similar Item widgets.

        :return: None
        :rtype: None
        """
        super().do_set_cell_callbacks('wvw_editing_hardware',
                                      self._lst_col_order[3:])

        self.cmbSimilarItemMethod.dic_handler_id[
            'changed'] = self.cmbSimilarItemMethod.connect(
                'changed', self._on_combo_changed, 2)

    def __set_properties(self) -> None:
        """
        Set the properties of the Similar Item widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the Similar Item Analysis for the currently "
              "selected Hardware item."))

        self.cmbSimilarItemMethod.do_set_properties(
            tooltip=_("Select the similar item analysis method."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        super().do_clear_tree()

        self.cmbSimilarItemMethod.do_update(0, signal='changed')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Similar Item Work View page.

        :param dict attributes: a dict of attributes key:value pairs for the
            displayed Hardware item's Similar Item analysis.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._record_id = attributes['hardware_id']
        self._method_id = attributes['similar_item_method_id']

        self.cmbSimilarItemMethod.do_update(self._method_id, signal='changed')

        if self._record_id > 0:
            self._do_load_tree()

    def _do_load_row(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Similar Item RAMSTKTreeView() and other widgets.

        :param dict attributes: the attributes dict for the row to be loaded.
        :return: None
        :rtype: None
        """
        attributes['quality_from'] = self.__do_get_quality(
            attributes['quality_from_id'])
        attributes['quality_to'] = self.__do_get_quality(
            attributes['quality_to_id'])
        attributes['environment_from'] = self.__do_get_environment(
            attributes['environment_from_id'])
        attributes['environment_to'] = self.__do_get_environment(
            attributes['environment_to_id'])

        _node_id = attributes['hardware_id']
        attributes['revision_id'] = self._similar_item_tree.get_node(
            _node_id).data['hardware'].get_attributes()['revision_id']
        attributes['name'] = self._similar_item_tree.get_node(
            _node_id).data['hardware'].get_attributes()['name']
        attributes['hazard_rate_active'] = self._similar_item_tree.get_node(
            _node_id).data['reliability'].get_attributes(
            )['hazard_rate_active']

        super().do_load_row(attributes)

    def _do_load_tree(self) -> None:
        """
        Load the Similar Item RAMSTKTreeView() with allocation data.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        self._tree_loaded = False
        for _node in self._similar_item_tree.children(self._record_id):
            _node_id = _node.data['hardware'].get_attributes()['hardware_id']
            pub.sendMessage('request_get_hardware_attributes',
                            node_id=_node_id,
                            table='similar_item')
        self._tree_loaded = True

    def _do_refresh_tree(self, model: Gtk.TreeModel, row: Gtk.TreeIter,
                         functions: List[str]) -> None:
        """
        Refresh the Similar Item Work View RAMSTKTreeView functions.

        :param model:
        :param row:
        :param functions:
        :return: None
        :rtype: None
        """
        model.set_value(row, self._lst_col_order[30], functions[0])
        model.set_value(row, self._lst_col_order[31], functions[1])
        model.set_value(row, self._lst_col_order[32], functions[2])
        model.set_value(row, self._lst_col_order[33], functions[3])
        model.set_value(row, self._lst_col_order[34], functions[4])

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Request to iteratively calculate the Similar Item metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _row = _model.get_iter_first()

        # Iterate through the assemblies and calculate the Similar Item hazard
        # intensities.
        self.do_set_cursor_busy()
        _node_ids = []
        while _row is not None:
            _node_ids.append(_model.get_value(_row, 1))
            _row = _model.iter_next(_row)

        for _node_id in _node_ids:
            pub.sendMessage('request_calculate_similar_item', node_id=_node_id)

        self.do_set_cursor_active(node_id=self._record_id)

    def _do_request_edit_function(self, __button: Gtk.ToolButton) -> None:
        """
        Request to edit the Similar Item analysis user-defined functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        (_model, _row) = self.treeview.get_selection().get_selected()

        _dialog = EditFunction(
            self.treeview,
            dlgparent=self.get_parent().get_parent().get_parent().get_parent())

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

    def _do_request_rollup(self, __button: Gtk.ToolButton) -> None:
        """
        Request to roll-up the Similar Item change descriptions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_roll_up_similar_item',
                        node_id=self._parent_id)
        self.do_set_cursor_active(node_id=self._record_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the selected Similar Item record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)
        self.do_set_cursor_active(node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the entities in the Similar Item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')
        self.do_set_cursor_active(node_id=self._record_id)

    def _do_set_tree(self, dmtree: treelib.Tree) -> None:
        """
        Sets the _allocation_tree equal to the datamanger Hardware tree.

        :param dmtree: the Hardware datamanger treelib.Tree() of data.
        :type dmtree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._similar_item_tree = dmtree

    def _get_cell_model(self, column: int) -> Gtk.TreeModel:
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

    def _get_hardware_attributes(self, tree: treelib.Tree) -> None:
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
                    _attributes['name'], _attributes['hazard_rate_logistics']
                ]
            except TypeError:
                pass

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Respond to RAMSTKComboBox() 'changed' signals.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`ramstk.views.gtk3.widgets.RAMSTKComboBox`
        :param int index: the index in the handler ID list oc the callback
            signal associated with the Gtk.ComboBox() that called this method.
        :return: None
        :rtype: None
        """
        _package = super().on_combo_changed(combo, index,
                                            'wvw_editing_hardware')
        _new_text = list(_package.values())[0]

        self._method_id = _new_text

        _visible: List[int] = []
        _editable: List[int] = []
        if _new_text == 1:  # Topic 633.
            _visible = [
                0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
            _editable = [
                0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
        elif _new_text == 2:  # User-defined
            _visible = self.treeview.visible
            _editable = self.treeview.editable

        try:
            self.treeview.do_set_visible_columns(visible=_visible)
            self.treeview.do_set_columns_editable(editable=_editable)
        except KeyError:
            pass
