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
            2: ['method_id', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Select Method"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Similar Item Method")

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbSimilarItemMethod: RAMSTKComboBox = RAMSTKComboBox()

        self._dic_attribute_updater = {
            'method_id': [self.cmbSimilarItemMethod.do_update, 'changed', 0],
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
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self._do_load_panel, 'succeed_calculate_hardware')

    def _do_clear_panel(self) -> None:
        """Clear the widgets on the panel.

        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.do_update(0, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Similar Item Work View page.

        :param dict attributes: a dict of attributes key:value pairs for the
            displayed Hardware item's Similar Item analysis.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

        self.cmbSimilarItemMethod.do_update(
            attributes['similar_item_method_id'], signal='changed')

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
                'changed', self.on_changed_combo, 2, 'wvw_editing_hardware')

    def __do_set_properties(self) -> None:
        """Set the properties of the Similar Item widgets.

        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.do_set_properties(
            tooltip=_("Select the similar item analysis method."))


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

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._method_id: int = 0
        self._similar_item_tree: treelib.Tree = treelib.Tree()
        self._title: str = _("Similar Item Analysis")

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_clear_tree, 'request_clear_workviews')

        pub.subscribe(self._do_load_panel, 'do_load_similar_item')
        pub.subscribe(self._do_load_panel, 'succeed_calculate_hardware')
        pub.subscribe(self._do_load_row, 'succeed_get_similar_item_attributes')
        pub.subscribe(self._do_set_tree, 'succeed_get_hardware_tree')

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
        super().do_set_cell_callbacks('wvw_editing_hardware',
                                      self._lst_col_order[3:])

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

    def _do_load_row(self, attributes: Dict[str, Any]) -> None:
        """Load the Similar Item RAMSTKTreeView() and other widgets.

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
            _node_id).data['reliability'].get_attributes()[
                'hazard_rate_active']  # noqa

        super().do_load_row(attributes)

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
        if self._method_id == 1:
            self.tvwTreeView.editable = {
                'col0': 'False',
                'col1': 'False',
                'col2': 'False',
                'col3': 'False',
                'col4': 'True',
                'col5': 'True',
                'col6': 'True',
                'col7': 'True',
                'col8': 'True',
                'col9': 'True',
                'col10': 'False',
                'col11': 'False',
                'col12': 'False',
                'col13': 'False',
                'col14': 'False',
                'col15': 'False',
                'col16': 'False',
                'col17': 'False',
                'col18': 'False',
                'col19': 'False',
                'col20': 'False',
                'col21': 'False',
                'col22': 'False',
                'col23': 'False',
                'col24': 'False',
                'col25': 'False',
                'col26': 'False',
                'col27': 'False',
                'col28': 'False',
                'col29': 'False',
                'col30': 'False',
                'col31': 'False',
                'col32': 'False',
                'col33': 'False',
                'col34': 'False',
                'col35': 'False',
                'col36': 'False',
                'col37': 'False',
                'col38': 'False',
                'col39': 'False',
                'col40': 'False',
                'col41': 'False',
                'col42': 'False',
                'col43': 'False',
                'col44': 'False',
                'col45': 'False',
                'col46': 'False',
                'col47': 'False',
                'col48': 'False',
                'col49': 'False',
                'col50': 'False',
                'col51': 'False',
                'col52': 'False',
                'col53': 'False',
                'col54': 'False',
                'col55': 'False',
            }

            self.tvwTreeView.visible = {
                'col0': 'False',
                'col1': 'False',
                'col2': 'True',
                'col3': 'True',
                'col4': 'True',
                'col5': 'True',
                'col6': 'True',
                'col7': 'True',
                'col8': 'True',
                'col9': 'True',
                'col10': 'False',
                'col11': 'False',
                'col12': 'False',
                'col13': 'False',
                'col14': 'False',
                'col15': 'False',
                'col16': 'False',
                'col17': 'False',
                'col18': 'False',
                'col19': 'False',
                'col20': 'False',
                'col21': 'False',
                'col22': 'False',
                'col23': 'False',
                'col24': 'False',
                'col25': 'False',
                'col26': 'False',
                'col27': 'False',
                'col28': 'False',
                'col29': 'False',
                'col30': 'False',
                'col31': 'False',
                'col32': 'False',
                'col33': 'False',
                'col34': 'False',
                'col35': 'True',
                'col36': 'False',
                'col37': 'False',
                'col38': 'False',
                'col39': 'False',
                'col40': 'False',
                'col41': 'False',
                'col42': 'False',
                'col43': 'False',
                'col44': 'False',
                'col45': 'False',
                'col46': 'False',
                'col47': 'False',
                'col48': 'False',
                'col49': 'False',
                'col50': 'False',
                'col51': 'False',
                'col52': 'False',
                'col53': 'False',
                'col54': 'False',
                'col55': 'False',
            }

        # TODO: Remove editable argument after all RAMSTKTreeView()'s are
        #  updated.
        self.tvwTreeView.do_set_columns_editable(editable=None)
        self.tvwTreeView.do_set_visible_columns()

    def _do_set_tree(self, dmtree: treelib.Tree) -> None:
        """Set the _similar_item_tree equal to the datamanger Hardware tree.

        :param dmtree: the Hardware datamanger treelib.Tree() of data.
        :return: None
        :rtype: None
        """
        self._similar_item_tree = dmtree

    def __do_get_environment(self, environment_id: int) -> str:
        """Retrieve the environment name given the ID.

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
        """Retrieve the quality name given the ID.

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

    def __do_set_properties(self) -> None:
        """Set the properties of the Similar Item widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
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
    _tablabel: str = _("SimilarItem")
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
        self._lst_callbacks = [
            self._do_request_edit_function,
            self._do_request_rollup,
            self._do_request_calculate,
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons = [
            'edit',
            'rollup',
            'calculate',
            'save',
            'save-all',
        ]
        self._lst_mnu_labels = [
            _("Edit Function"),
            _("Roll-Up Descriptions"),
            _("Calculate Similar Item"),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Edit the Similar Item analysis functions."),
            _("Roll up descriptions to next higher level assembly."),
            _("Calculate the Similar Item analysis."),
            _("Save changes to the selected Similar Item analysis line item."),
            _("Save changes to all Similar Item analysis line items."),
        ]

        # Initialize private scalar attributes.
        self._pnlMethod: RAMSTKPanel = MethodPanel()
        self._pnlSimilarItemAnalysis: RAMSTKPanel = SimilarItemPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_hardware')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_hardware')

        pub.subscribe(self._do_load_page,
                      'succeed_get_all_hardware_attributes')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """Load the Allocation page.

        :param attributes: the attributes dict for the selected Hardware item.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to iteratively calculate the Similar Item metrics.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model = self._pnlSimilarItemAnalysis.tvwTreeView.get_model()
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
        (_model,
         _row) = self._pnlSimilarItemAnalysis.tvwTreeView.get_selection(
         ).get_selected()  # noqa

        _dialog = EditFunction(
            self._pnlSimilarItemAnalysis.tvwTreeView,
            dlgparent=self.get_parent().get_parent().get_parent().get_parent())

        if _dialog.do_run() == Gtk.ResponseType.OK:
            _functions = _dialog.do_set_functions(
                self._pnlSimilarItemAnalysis.tvwTreeView)
            if _dialog.chkApplyAll.get_active():
                _row = _model.get_iter_first()
                while _row is not None:
                    self._pnlSimilarItemAnalysis.do_refresh_functions(
                        _row, _functions)
                    _row = _model.iter_next(_row)
            else:
                self._pnlSimilarItemAnalysis.do_refresh_functions(
                    _row, _functions)

        _dialog.do_destroy()

    def _do_request_rollup(self, __button: Gtk.ToolButton) -> None:
        """Request to roll-up the Similar Item change descriptions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_roll_up_similar_item',
                        node_id=self._parent_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to save the selected Similar Item record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_hardware', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the entities in the Similar Item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_hardware')

    def __make_ui(self) -> None:
        """Build the user interface for the Similar Item tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        _hpaned.pack1(self._pnlMethod, True, True)

        _fmt_file = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
            + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[self._module])

        try:
            _bg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                self._module + 'bg']
            _fg_color = self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[
                self._module + 'fg']
        except KeyError:
            _bg_color = '#FFFFFF'
            _fg_color = '#000000'

        self._pnlSimilarItemAnalysis.do_make_treeview(**{
            'bg_color': _bg_color,
            'fg_color': _fg_color,
            'fmt_file': _fmt_file
        })
        self._pnlSimilarItemAnalysis.do_load_combobox()
        self._pnlSimilarItemAnalysis.do_set_callbacks()

        _hpaned.pack2(self._pnlSimilarItemAnalysis, True, True)

        self.show_all()
