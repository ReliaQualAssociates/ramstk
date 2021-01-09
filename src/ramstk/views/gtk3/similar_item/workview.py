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
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox, RAMSTKPanel, RAMSTKWorkView
)


class MethodPanel(RAMSTKPanel):
    """Panel to display Similar Item analysis methods."""
    def __init__(self):
        """Initialize an instance of the Similar Item methods panel."""
        super().__init__()

        # Initialize private dictionary instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['similar_item_method_id', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Select Method"),
        ]

        # Initialize private scalar instance attributes.
        self._method_id: int = 0
        self._title: str = _("Similar Item Method")
        self._tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbSimilarItemMethod: RAMSTKComboBox = RAMSTKComboBox()

        self._dic_attribute_updater = {
            'similar_item_method_id':
            [self.cmbSimilarItemMethod.do_update, 'changed', 0],
        }
        self._lst_widgets = [
            self.cmbSimilarItemMethod,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_load_combobox()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_hardware')
        pub.subscribe(self._do_set_tree, 'succeed_retrieve_similar_item')

    def _do_clear_panel(self) -> None:
        """Clear the widgets on the panel.

        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.do_update(0, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Similar Item Work View page.

        :param attributes: a dict of attributes key:value pairs for the
            displayed Hardware item's Similar Item analysis.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        _similar_item = self._tree.get_node(
            self._record_id).data['similar_item']

        self.cmbSimilarItemMethod.do_update(
            _similar_item.similar_item_method_id, signal='changed')

    def _do_set_tree(self, tree: treelib.Tree) -> None:
        """Set the work view _tree equal to the datamanger tree.

        :param tree: the similar item datamanger treelib.Tree() of data.
        :return: None
        :rtype: None
        """
        self._tree = tree

    def __do_load_combobox(self) -> None:
        """Load Similar Item analysis RAMSTKComboBox()s.

        :return: None
        :rtype: None
        """
        # Load the method combobox.
        self.cmbSimilarItemMethod.do_load_combo(
            [[_("Topic 633"), 0], [_("User-Defined"), 1]], signal='changed')

    def __do_set_callbacks(self) -> None:
        """Set the callback functions and methods for the Similar Item widgets.

        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.dic_handler_id[
            'changed'] = self.cmbSimilarItemMethod.connect(
                'changed', self.on_changed_combo, 0,
                'wvw_editing_similar_item')

        self.cmbSimilarItemMethod.connect('changed', self.__on_method_changed)

    def __do_set_properties(self) -> None:
        """Set the properties of the Similar Item widgets.

        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.do_set_properties(
            tooltip=_("Select the similar item analysis method."))

    def __on_method_changed(self, combo: RAMSTKComboBox) -> None:
        """Wrap the _do_set_sensitive() method when goal combo changes.

        :param combo: the allocation calculation method RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        self._method_id = combo.get_active()
        pub.sendMessage('succeed_change_similar_item_method',
                        method_id=self._method_id)


class SimilarItemPanel(RAMSTKPanel):
    """Panel to display Similar Item analysis worksheet."""

    # Define private dictionary class attributes.
    _dic_quality: Dict[int, str] = {
        0: '',
        1: 'Space',
        2: 'Full Military',
        3: 'Ruggedized',
        4: 'Commercial'
    }
    _dic_environment: Dict[int, str] = {
        0: '',
        1: 'Ground, Benign',
        2: 'Ground,Mobile',
        3: 'Naval, Sheltered',
        4: 'Airborne, Inhabited, Cargo',
        5: 'Airborne, Rotary Wing',
        6: 'Space, Flight'
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Similar Item analysis worksheet."""
        super().__init__()

        # Initialize private dictionary instance attributes.
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'hardware_id': [None, 'edited', 1],
            'quality_from_id': [None, 'edited', 4],
            'quality_to_id': [None, 'edited', 5],
            'environment_from_id': [None, 'edited', 6],
            'environment_to_id': [None, 'edited', 7],
            'temperature_from': [None, 'edited', 8],
            'temperature_to': [None, 'edited', 9],
            'change_description_1': [None, 'edited', 10],
            'change_factor_1': [None, 'edited', 11],
            'change_description_2': [None, 'edited', 12],
            'change_factor_2': [None, 'edited', 13],
            'change_description_3': [None, 'edited', 14],
            'change_factor_3': [None, 'edited', 15],
            'change_description_4': [None, 'edited', 16],
            'change_factor_4': [None, 'edited', 17],
            'change_description_5': [None, 'edited', 18],
            'change_factor_5': [None, 'edited', 19],
            'change_description_6': [None, 'edited', 20],
            'change_factor_6': [None, 'edited', 21],
            'change_description_7': [None, 'edited', 22],
            'change_factor_7': [None, 'edited', 23],
            'change_description_8': [None, 'edited', 24],
            'change_factor_8': [None, 'edited', 25],
            'change_description_9': [None, 'edited', 26],
            'change_factor_9': [None, 'edited', 27],
            'change_description_10': [None, 'edited', 28],
            'change_factor_10': [None, 'edited', 29],
            'function_1': [None, 'edited', 30],
            'function_2': [None, 'edited', 31],
            'function_3': [None, 'edited', 32],
            'function_4': [None, 'edited', 33],
            'function_5': [None, 'edited', 34],
            'user_blob_1': [None, 'edited', 40],
            'user_blob_2': [None, 'edited', 41],
            'user_blob_3': [None, 'edited', 42],
            'user_blob_4': [None, 'edited', 43],
            'user_blob_5': [None, 'edited', 44],
            'user_float_1': [None, 'edited', 45],
            'user_float_2': [None, 'edited', 46],
            'user_float_3': [None, 'edited', 47],
            'user_float_4': [None, 'edited', 48],
            'user_float_5': [None, 'edited', 49],
            'user_int_1': [None, 'edited', 50],
            'user_int_2': [None, 'edited', 51],
            'user_int_3': [None, 'edited', 52],
            'user_int_4': [None, 'edited', 53],
            'user_int_5': [None, 'edited', 54],
        }
        self._dic_hardware_attrs: Dict[str, Any] = {}
        self._dic_row_loader = {
            'similar_item': self.__do_load_similar_item,
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._method_id: int = 0
        self._hardware_tree: treelib.Tree = treelib.Tree()
        self._selected_hardware_id: int = 0
        self._title: str = _("Similar Item Analysis")

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.tree: treelib.Tree = treelib.Tree()

        # Make a fixed type panel.
        super().do_make_panel_treeview()
        self.__do_set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_clear_tree, 'request_clear_workviews')
        pub.subscribe(super().do_load_panel, 'succeed_calculate_similar_item')

        pub.subscribe(self._do_set_tree, 'succeed_retrieve_similar_item')
        pub.subscribe(self._do_set_tree, 'succeed_retrieve_hardware')
        pub.subscribe(self._on_select_hardware, 'selected_hardware')
        pub.subscribe(self._on_method_changed,
                      'succeed_change_similar_item_method')

    def do_load_combobox(self) -> None:
        """Load Similar Item analysis RAMSTKComboBox()s.

        :return: None
        :rtype: None
        """
        # Load the quality from and quality to Gtk.CellRendererCombo().
        for _idx in [4, 5]:
            _model = self.tvwTreeView.get_cell_model(_idx, True)
            for _quality in self._dic_quality.values():
                _model.append([_quality])

        # Load the environment from and environment to Gtk.CellRendererCombo().
        for _idx in [6, 7]:
            _model = self.tvwTreeView.get_cell_model(_idx, True)
            for _environment in self._dic_environment.values():
                _model.append([_environment])

    def do_refresh_functions(self, row: Gtk.TreeIter,
                             function: List[str]) -> None:
        """Refresh the Similar Item functions in the RAMSTKTreeView().

        :param row: the row in the Similar Item RAMSTKTreeView() whose
            functions need to be updated.  This is require to allow a recursive
            calling function to load the same function in all rows.
        :param function: the list of user-defined Similar Item functions.
        :return: None
        """
        _model = self.tvwTreeView.get_model()

        _model.set_value(row, self._lst_col_order[30], function[0])
        _model.set_value(row, self._lst_col_order[31], function[1])
        _model.set_value(row, self._lst_col_order[32], function[2])
        _model.set_value(row, self._lst_col_order[33], function[3])
        _model.set_value(row, self._lst_col_order[34], function[4])

    def do_set_callbacks(self) -> None:
        """Set the callback functions and methods for the Similar Item widgets.

        :return: None
        :rtype: None
        """
        super().do_set_callbacks()
        super().do_set_cell_callbacks('wvw_editing_similar_item',
                                      self._lst_col_order[4:])

    def _do_load_hardware_attrs(self) -> None:
        """Load the hardware data dict.

        :return: None
        :rtype: None
        """
        for _node in self._hardware_tree.all_nodes()[1:]:
            _hardware = _node.data['hardware']
            _reliability = _node.data['reliability']
            self._dic_hardware_attrs[_hardware.hardware_id] = [
                _hardware.name, _reliability.hazard_rate_active, _hardware.part
            ]

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Similar Item Work View page.

        :param attributes: a dict of attributes key:value pairs for the
            displayed Hardware item's Similar Item analysis.
        :return: None
        :rtype: None
        """
        self._method_id = attributes['similar_item_method_id']
        self._record_id = attributes['hardware_id']

        if self._record_id > 0:
            self._do_load_tree()
            self._do_set_columns_editable()

    def _do_load_tree(self) -> None:
        """Load the Similar Item RAMSTKTreeView() with allocation data.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

        self._tree_loaded = False
        for _node in self._similar_item_tree.children(self._record_id):
            _node_id = _node.data['hardware'].get_attributes()['hardware_id']
            pub.sendMessage('request_get_hardware_attributes',
                            node_id=_node_id,
                            table='similar_item')
        self._tree_loaded = True

    def _do_set_columns_editable(self) -> None:
        """Set editable columns based on the Similar Item method selected.

        :return: None
        :rtype: None
        """
        _columns: List[str] = [
            'col0', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7',
            'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14',
            'col15', 'col16', 'col17', 'col18', 'col19', 'col20', 'col21',
            'col22', 'col23', 'col24', 'col25', 'col26', 'col27', 'col28',
            'col29', 'col30', 'col31', 'col32', 'col33', 'col34', 'col35',
            'col36', 'col37', 'col38', 'col39', 'col40', 'col41', 'col42',
            'col43', 'col44', 'col45', 'col46', 'col47', 'col48', 'col49',
            'col50', 'col51', 'col52', 'col53', 'col54', 'col55'
        ]

        if self._method_id == 1:
            _editable = [
                'False', 'False', 'False', 'False', 'True', 'True', 'True',
                'True', 'True', 'True', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False'
            ]
            _visible = [
                'False', 'False', 'True', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'True', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'False', 'False', 'False', 'False'
            ]
        else:
            _editable = [
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'False', 'False', 'False', 'False', 'False', 'False', 'False',
                'False', 'False', 'False', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True'
            ]
            _visible = [
                'False', 'False', 'True', 'True', 'False', 'False', 'False',
                'False', 'False', 'False', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'False', 'False', 'False', 'False', 'False', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'True', 'True', 'True', 'True', 'True', 'True', 'True', 'True',
                'True', 'True', 'True'
            ]

        self.tvwTreeView.editable = dict(zip(_columns, _editable))
        self.tvwTreeView.visible = dict(zip(_columns, _visible))

        self.tvwTreeView.do_set_columns_editable()
        self.tvwTreeView.do_set_visible_columns()

    def _do_set_tree(self, tree: treelib.Tree) -> None:
        """Set the work view tree equal to the datamanger tree.

        :param tree: the Hardware datamanger treelib.Tree() of data.
        :return: None
        :rtype: None
        """
        if tree.get_node(0).tag == 'similar_items':
            self.tree = tree
        elif tree.get_node(0).tag == 'hardwares':
            self._hardware_tree = tree
            self._do_load_hardware_attrs()

    def _on_method_changed(self, method_id: int) -> None:
        """Set method ID attributes when user changes the selection.

        :param method_id: the newly selected similar item method.
        :return: None
        :rtype: None
        """
        self._method_id = method_id
        self._do_set_columns_editable()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Hardware package Module View RAMSTKTreeView().

        This method is called whenever a Hardware Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)
        if _attributes:
            self._record_id = _attributes['hardware_id']

    def _on_select_hardware(self, attributes: Dict[str, Any]) -> None:
        """Load the similar item list for the selected hardware item.

        :param attributes: the attributes dict for the selected hardware item.
        :return: None
        :rtype: None
        """
        self._selected_hardware_id = attributes['hardware_id']
        self._method_id = self.tree.get_node(
            attributes['hardware_id']
        ).data['similar_item'].similar_item_method_id
        super().do_load_panel(self.tree)
        self._do_set_columns_editable()

    def __do_get_environment(self, environment_id: int) -> str:
        """Retrieve the environment name given the ID.

        :param environment_id: the ID number of the environment to return.
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
        """Retrieve the quality name given the ID.

        :param quality_id: the ID number of the quality level to return.
        :return: _quality; the noun name of the quality level.
        :rtype; str
        """
        _quality = ''
        try:
            _quality = self._dic_quality[quality_id]
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

        return _quality

    def __do_load_similar_item(self,
                               node: Any = '',
                               row: Gtk.TreeIter = None) -> Gtk.TreeIter:
        """Load the similar item RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # pylint: disable=unused-variable
        _entity = node.data['similar_item']

        if (not self._dic_hardware_attrs[_entity.hardware_id][2]
                and _entity.parent_id == self._selected_hardware_id):
            _hardware = self._hardware_tree.get_node(_entity.hardware_id).data
            _model = self.tvwTreeView.get_model()

            _name = _hardware['hardware'].name
            _hr_active = _hardware['reliability'].hazard_rate_active

            _attributes = [
                _entity.revision_id, _entity.hardware_id, _name, _hr_active,
                self._dic_quality[_entity.quality_from_id],
                self._dic_quality[_entity.quality_to_id],
                self._dic_environment[_entity.environment_from_id],
                self._dic_environment[_entity.environment_to_id],
                _entity.temperature_from, _entity.temperature_to,
                _entity.change_description_1, _entity.change_factor_1,
                _entity.change_description_2, _entity.change_factor_2,
                _entity.change_description_3, _entity.change_factor_3,
                _entity.change_description_4, _entity.change_factor_4,
                _entity.change_description_5, _entity.change_factor_5,
                _entity.change_description_6, _entity.change_factor_6,
                _entity.change_description_7, _entity.change_factor_7,
                _entity.change_description_8, _entity.change_factor_8,
                _entity.change_description_9, _entity.change_factor_9,
                _entity.change_description_10, _entity.change_factor_10,
                _entity.function_1, _entity.function_2, _entity.function_3,
                _entity.function_4, _entity.function_5, _entity.result_1,
                _entity.result_2, _entity.result_3, _entity.result_4,
                _entity.result_5, _entity.user_blob_1, _entity.user_blob_2,
                _entity.user_blob_3, _entity.user_blob_4, _entity.user_blob_5,
                _entity.user_float_1, _entity.user_float_2,
                _entity.user_float_3, _entity.user_float_4,
                _entity.user_float_5, _entity.user_int_1, _entity.user_int_2,
                _entity.user_int_3, _entity.user_int_4, _entity.user_int_5,
                _entity.parent_id
            ]

            try:
                _new_row = _model.append(row, _attributes)
            except (AttributeError, TypeError, ValueError):
                _new_row = None
                _message = _(
                    "An error occurred when loading similar item record {0} "
                    "into the similar item list.  This might indicate it was "
                    "missing it's data package, some of the data in the "
                    "package was missing, or some of the data was the wrong "
                    "type.  Row data was: {1}").format(str(node.identifier),
                                                       _attributes)
                pub.sendMessage(
                    'do_log_warning_msg',
                    logger_name='WARNING',
                    message=_message,
                )

        return _new_row

    def __do_set_properties(self) -> None:
        """Set the properties of the Similar Item widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the Similar Item Analysis for the currently "
              "selected Hardware item."))


class SimilarItem(RAMSTKWorkView):
    """Display Similar Item attribute data in the Work Book.

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
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'similar_item'
    _tablabel: str = _("Similar Item")
    _tabtooltip: str = _(
        "Displays the Similar Item analysis for the selected hardware item.")

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Hardware Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_edit_function)
        self._lst_callbacks.insert(1, self._do_request_rollup)
        self._lst_callbacks.insert(2, self._do_request_calculate)
        self._lst_icons.insert(0, 'edit')
        self._lst_icons.insert(1, 'rollup')
        self._lst_icons.insert(2, 'calculate')
        self._lst_mnu_labels = [
            _("Edit Function"),
            _("Roll-Up Descriptions"),
            _("Calculate Similar Item"),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Edit the similar item analysis functions."),
            _("Roll up descriptions to next higher level assembly."),
            _("Calculate the similar item analysis."),
            _("Save changes to the selected similar item analysis line item."),
            _("Save changes to all similar item analysis line items."),
        ]

        # Initialize private scalar attributes.
        self._pnlMethod: RAMSTKPanel = MethodPanel()
        self._pnlPanel: RAMSTKPanel = SimilarItemPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_set_cursor_active,
            'succeed_roll_up_change_descriptions',
        )

        pub.subscribe(
            self._do_set_record_id,
            'selected_hardware',
        )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the allocation's record ID.

        :param attributes: the attributes dict for the selected allocation
            record.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._parent_id = attributes['parent_id']

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to iteratively calculate the Similar Item metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model = self._pnlPanel.tvwTreeView.get_model()
        _row = _model.get_iter_first()

        # Iterate through the assemblies and calculate the Similar Item hazard
        # intensities.
        super().do_set_cursor_busy()
        _node_ids = []
        while _row is not None:
            _node_ids.append(_model.get_value(_row, 1))
            _row = _model.iter_next(_row)

        for _node_id in _node_ids:
            pub.sendMessage('request_calculate_similar_item', node_id=_node_id)

    def _do_request_edit_function(self, __button: Gtk.ToolButton) -> None:
        """Request to edit the Similar Item analysis user-defined functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        (_model, _row
         ) = self._pnlPanel.tvwTreeView.get_selection().get_selected()  # noqa

        _dialog = EditFunction(
            self._pnlPanel.tvwTreeView,
            dlgparent=self.get_parent().get_parent().get_parent().get_parent())

        if _dialog.do_run() == Gtk.ResponseType.OK:
            _functions = _dialog.do_set_functions(self._pnlPanel.tvwTreeView)
            if _dialog.chkApplyAll.get_active():
                _row = _model.get_iter_first()
                while _row is not None:
                    self._pnlPanel.do_refresh_functions(_row, _functions)
                    _row = _model.iter_next(_row)
            else:
                self._pnlPanel.do_refresh_functions(_row, _functions)

        _dialog.do_destroy()

    def _do_request_rollup(self, __button: Gtk.ToolButton) -> None:
        """Request to roll-up the Similar Item change descriptions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_roll_up_change_descriptions',
                        node=self._pnlPanel.tree.get_node(self._record_id))

    def __make_ui(self) -> None:
        """Build the user interface for the Similar Item tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        super().do_embed_treeview_panel()
        self._pnlPanel.do_load_combobox()
        self._pnlPanel.do_set_callbacks()

        self.remove(self.get_children()[-1])
        _hpaned.pack1(self._pnlMethod, True, True)
        _hpaned.pack2(self._pnlPanel, True, True)

        self.show_all()
