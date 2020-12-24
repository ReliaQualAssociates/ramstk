# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.failure_definition.listview.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition list view module."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView, RAMSTKPanel


class FailureDefinitionPanel(RAMSTKPanel):
    """Panel to display list of failure definitions."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'failure_definitions'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the failure definition panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attribute_keys = {
            2: ['definition', 'string'],
        }
        self._dic_attribute_updater = {
            'revision_id': [None, 'edited', 0],
            'definition_id': [None, 'edited', 1],
            'definition': [None, 'edited', 2],
        }
        self._dic_row_loader = {
            'definition': self.__do_load_failure_definition,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Failure Definition List")

        # Initialize public dictionary class attributes.

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel,
                      'succeed_retrieve_{0}'.format(self._module))
        pub.subscribe(super().do_load_panel,
                      'succeed_insert_failure_definition')
        pub.subscribe(super().on_delete, 'succeed_delete_failure_definition')

        pub.subscribe(self._on_module_switch, 'lvwSwitchedPage')

    def do_set_callbacks(self) -> None:
        """Set callbacks for the failure definition list view.

        :return: None
        """
        super().do_set_callbacks()
        super().do_set_cell_callbacks('lvw_editing_failure_definition', [2])

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set up the RAMSTKTreeView() for Failure Definitions.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.tvwTreeView.set_tooltip_text(
            _("Displays the list of failure definitions for the selected "
              "revision."))

        _cell = self.tvwTreeView.get_columns()[1].get_cells()[0]
        _cell.set_property('editable', False)

        _cell = self.tvwTreeView.get_columns()[2].get_cells()[0]
        _cell.set_property('editable', True)

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'failure_definition' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[1])
            _title = _("Analyzing Failure Definition {0:s}").format(str(_code))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Read attributes from newly selected RAMSTKTreeView() row.

        This method is called whenever a view's RAMSTKTreeView() row is
        activated/changed.

        :param selection: the Gtk.TreeSelection() for the newly selected row.
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes['definition_id']

            pub.sendMessage('selected_failure_definition',
                            attributes=_attributes)

    def __do_load_failure_definition(self, node: treelib.Node,
                                     row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure definition into the RAMSTKTreeView().

        :param node: the treelib Node() with the definition data to load.
        :param row: the parent row of the definition to load.
        :return: _new_row; the row that was just populated with definition
            data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _attributes = [
            _entity.revision_id, _entity.definition_id, _entity.definition
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure definition {0:s}.  "
                "This might indicate it was missing it's data package, some "
                "of the data in the package was missing, or some of the data "
                "was the wrong type.  Row data was: {1}").format(
                    str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row


class FailureDefinition(RAMSTKListView):
    """Display failure definitions associated with the selected revision.

    The attributes of the failure definition list view are:

    :cvar _module: the name of the module.  Spaces are replaced with single
        underscores if the name is more than one word.
    :cvar _tablabel: the text to display on the view's tab.
    :cvar _tabtooltip: the text to display in the tooltip for the view's tab.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'failure_definitions'
    _tablabel = "<span weight='bold'>" + _("Failure\nDefinitions") + "</span>"
    _tabtooltip = _("Displays failure definitions for the "
                    "selected revision.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the List View for the failure definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, self._do_request_delete)
        self._lst_icons.insert(1, 'remove')
        self._lst_mnu_labels = [
            _("Add Definition"),
            _("Delete Selected Definition"),
            _("Save Selected Definition"),
            _("Save All Definitions"),
        ]
        self._lst_tooltips = [
            _("Add a new failure definition."),
            _("Delete the currently selected failure definition."),
            _("Save changes to the currently selected failure definition"),
            _("Save changes to all failure definitions."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = FailureDefinitionPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_failure_definition')

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Failure Definition record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_("You are about to delete Failure Definition {0:d} and "
                      "all data associated with it.  Is this really what you "
                      "want to do?").format(self._record_id))
        _dialog.do_set_message_type(message_type='question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                'request_delete_failure_definitions',
                node_id=self._record_id,
            )

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the failure definition's record ID.

        :param attributes: the attributes dict for the selected failure
            definition.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['definition_id']

    def __make_ui(self) -> None:
        """Build the user interface for the failure definition list view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
