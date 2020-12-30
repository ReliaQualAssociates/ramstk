# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.moduleview.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Validation GTK3 module view."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog, RAMSTKModuleView, RAMSTKPanel
)

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS


class ValidationPanel(RAMSTKPanel):
    """Panel to display flat list of validation tasks."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Validation panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'validation_id': [None, 'edited', 1],
            'acceptable_maximum': [None, 'edited', 2],
            'acceptable_mean': [None, 'edited', 3],
            'acceptable_minimum': [None, 'edited', 4],
            'acceptable_variance': [None, 'edited', 5],
            'confidence': [None, 'edited', 6],
            'cost_average': [None, 'edited', 7],
            'cost_ll': [None, 'edited', 8],
            'cost_maximum': [None, 'edited', 9],
            'cost_mean': [None, 'edited', 10],
            'cost_minimum': [None, 'edited', 11],
            'cost_ul': [None, 'edited', 12],
            'cost_variance': [None, 'edited', 13],
            'date_end': [None, 'edited', 14],
            'date_start': [None, 'edited', 15],
            'description': [None, 'edited', 16],
            'measurement_unit': [None, 'edited', 17],
            'name': [None, 'edited', 18],
            'status': [None, 'edited', 19],
            'task_specification': [None, 'edited', 20],
            'task_type': [None, 'edited', 21],
            'time_average': [None, 'edited', 22],
            'time_ll': [None, 'edited', 23],
            'time_maximum': [None, 'edited', 24],
            'time_mean': [None, 'edited', 25],
            'time_minimum': [None, 'edited', 26],
            'time_ul': [None, 'edited', 27],
            'time_variance': [None, 'edited', 28],
        }
        self._dic_row_loader = {
            'validation': self.__do_load_verification,
        }

        # Initialize private list class attributes.
        self._lst_measurement_units: List[str] = []
        self._lst_verification_types: List[str] = []

        # Initialize private scalar class attributes.
        self._title = _("Verification Task List")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()
        self.__do_set_properties()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_validations')
        pub.subscribe(super().do_load_panel, 'succeed_insert_validation')
        pub.subscribe(super().do_refresh_tree, 'wvw_editing_validation')
        pub.subscribe(super().on_delete, 'succeed_delete_validation')

        pub.subscribe(self._on_module_switch, 'mvwSwitchedPage')

    def do_load_measurement_units(
            self, measurement_unit: Dict[int, Tuple[str, str]]) -> None:
        """Load the verification task measurement unit list.

        :param measurement_unit: the dict containing the units of measure.
        :return: None
        """
        self._lst_measurement_units = [""]

        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position['col17']).get_cells()[0]
        _cell.set_property('has-entry', False)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for __, _key in enumerate(measurement_unit):
            self._lst_measurement_units.append(measurement_unit[_key][1])
            _cellmodel.append([measurement_unit[_key][1]])

    def do_load_verification_types(
            self, verification_type: Dict[int, Tuple[str, str]]) -> None:
        """Load the verification task type list.

        :param verification_type: the dict containing the verification task
            types.
        :return: None
        """
        self._lst_verification_types = [""]

        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position['col21']).get_cells()[0]
        _cell.set_property('has-entry', False)
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for __, _key in enumerate(verification_type):
            self._lst_verification_types.append(verification_type[_key][1])
            _cellmodel.append([verification_type[_key][1]])

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'validation' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Validation {0}: {1}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Validation Module View RAMSTKTreeView().

        This method is called whenever a Validation Module View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Validation class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['validation_id']

            _title = _("Analyzing Verification Task {0}").format(
                str(_attributes['name']))

            pub.sendMessage(
                'selected_validation',
                attributes=_attributes,
            )
            pub.sendMessage(
                'request_get_validation_attributes',
                node_id=self._record_id,
                table='validation',
            )
            pub.sendMessage(
                'request_set_title',
                title=_title,
            )

    def __do_load_verification(self, node: treelib.Node,
                               row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a verification task into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the requirement
            tree.
        :return: _new_row; the row that was just populated with requirement
            data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _measurement_unit = self._lst_measurement_units[
            _entity.measurement_unit]
        _task_type = self._lst_verification_types[_entity.task_type]

        _attributes = [
            _entity.revision_id,
            _entity.validation_id,
            _entity.acceptable_maximum,
            _entity.acceptable_mean,
            _entity.acceptable_minimum,
            _entity.acceptable_variance,
            _entity.confidence,
            _entity.cost_average,
            _entity.cost_ll,
            _entity.cost_maximum,
            _entity.cost_mean,
            _entity.cost_minimum,
            _entity.cost_ul,
            _entity.cost_variance,
            str(_entity.date_end),
            str(_entity.date_start),
            _entity.description,
            _measurement_unit,
            _entity.name,
            _entity.status,
            _entity.task_specification,
            _task_type,
            _entity.time_average,
            _entity.time_ll,
            _entity.time_maximum,
            _entity.time_mean,
            _entity.time_minimum,
            _entity.time_ul,
            _entity.time_variance,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _error_msg = _(
                "An error occurred when loading verification task {0} in the "
                "verification task list.  This might indicate it was missing "
                "it's data package, some of the data in the package was "
                "missing, or some of the data was the wrong type.  Row data "
                "was: {1}").format(str(node.identifier), _attributes)
            pub.sendMessage(
                'do_log_warning_msg',
                logger_name='WARNING',
                message=_error_msg,
            )

        return _new_row

    def __do_set_properties(self) -> None:
        """Set common properties of the ModuleView and widgets.

        :return: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of validations."))


class ModuleView(RAMSTKModuleView):
    """Display Validation attribute data in the RAMSTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Validation
    Module View are:

    :cvar _module: the name of the module.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'validation'
    _tablabel: str = 'Verification'
    _tabtooltip: str = _("Displays the list of verification tasks for the "
                         "selected Revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Validation Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/validation.png')

        # Initialize private list attributes.
        self._lst_mnu_labels = [
            _("Add Verification Task"),
            _("Delete Selected Task"),
            _("Save Selected Task"),
            _("Save All Tasks"),
        ]
        self._lst_tooltips = [
            _("Add a new verification task."),
            _("Remove the currently selected verification task."),
            _("Save changes to the currently selected verification task."),
            _("Save changes to all verification tasks."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = ValidationPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id,
                      'selected_{0}'.format(self._module))

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _prompt = _("You are about to delete Validation {0:d} and all "
                    "data associated with it.  Is this really what "
                    "you want to do?").format(self._record_id)
        _dialog: RAMSTKMessageDialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type('question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage('request_delete_validation',
                            node_id=self._record_id)

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Verification task's record ID.

        :param attributes: the attributes dict for the selected Verification
            task.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

    def __make_ui(self) -> None:
        """Build the user interface for the requirement module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_load_measurement_units(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS)
        self._pnlPanel.do_load_verification_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE)
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.do_set_cell_callbacks(
            'mvw_editing_validation',
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
