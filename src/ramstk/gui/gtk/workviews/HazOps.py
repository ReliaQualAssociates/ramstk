# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.HazOps.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK HazOps Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.Configuration import RAMSTK_FAILURE_PROBABILITY
from ramstk.gui.gtk.ramstk import RAMSTKFrame, RAMSTKLabel, RAMSTKTreeView
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
from .WorkView import RAMSTKWorkView


class HazOps(RAMSTKWorkView):
    """
    Display HazOps attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (HazOps). The attributes of a HazOps Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each Gtk.Widget() associated with an editable
                           Functional HazOps attribute.

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | tvw_hazops `cursor_changed`               |
    +-------+-------------------------------------------+
    |   1   | tvw_hazops `button_press_event`           |
    +-------+-------------------------------------------+
    |   2   | tvw_hazops `edited`                       |
    +-------+-------------------------------------------+
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the HazOps.

        :param configuration: the instance of the RAMSTK Configuration() class.
        :type controller: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKWorkView.__init__(
            self,
            configuration,
            module='HazOps',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hazard_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        _fmt_file = (
            self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/' +
            self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE['hazops']
        )
        _fmt_path = "/root/tree[@name='HazOps']/column"

        self.treeview = RAMSTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            "#FFFFFF",
            "#000000",
            pixbuf=False,
        )
        self._lst_col_order = self.treeview.order

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_hardware')
        pub.subscribe(self.do_load_tree, 'retrieved_hazops')

    def __load_combobox(self):
        """
        Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        # Load the potential hazards into the Gtk.CellRendererCombo().
        _model = self._get_cell_model(3)
        for _key in self.RAMSTK_CONFIGURATION.RAMSTK_HAZARDS:
            _hazard = '{0:s}, {1:s}'.format(
                self.RAMSTK_CONFIGURATION.RAMSTK_HAZARDS[_key][0],
                self.RAMSTK_CONFIGURATION.RAMSTK_HAZARDS[_key][1],
            )
            _model.append((_hazard, ))

        # Load the severity classes into the Gtk.CellRendererCombo().
        for i in [6, 10, 14, 18]:
            _model = self._get_cell_model(i)
            for _key in self.RAMSTK_CONFIGURATION.RAMSTK_SEVERITY:
                _severity = self.RAMSTK_CONFIGURATION.RAMSTK_SEVERITY[_key][1]
                _model.append((_severity, ))

        # Load the failure probabilities into the Gtk.CellRendererCombo().
        for i in [7, 11, 15, 19]:
            _model = self._get_cell_model(i)
            for _item in RAMSTK_FAILURE_PROBABILITY:
                _model.append((_item[0], ))

    def __make_ui(self):
        """
        Make the HazOps RAMSTKTreeview().

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
                    'calculate',
                    'add',
                    'remove',
                ],
                tooltips=[
                    _("Calculate the HazOps analysis."),
                    _("Add a hazard to the HazOps analysis."),
                    _(
                        "Remove the selected hazard and all associated data "
                        "from the HazOps analysis.", ),
                ],
                callbacks=[
                    self._do_request_calculate,
                    self.do_request_insert_sibling,
                    self._do_request_delete,
                ],
            ), )
        self.pack_start(_scrolledwindow, False, False, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame(label=_("HazOps Analysis"))
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack_end(_frame, True, True, 0)

        _label = RAMSTKLabel(
            _("HazOps"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays the HazOps analysis for the selected "
                "hardware item.", ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback functions and methods for the HazOps widgets.

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

        for i in self._lst_col_order[3:]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i], ).get_cells()
            try:
                _cell[0].connect(
                    'edited',
                    self._on_cell_edit,
                    i,
                    self.treeview.get_model(),
                )
            except TypeError:
                _cell[0].connect(
                    'toggled',
                    self._on_cell_edit,
                    'new text',
                    i,
                    self.treeview.get_model(),
                )

    def __set_properties(self):
        """
        Set the properties of the HazOps widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _(
                "Displays the HazOps Analysis for the currently "
                "selected Hardware item.", ), )

    def _do_change_row(self, treeview):
        """
        Handle events for the HazOps Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param treeview: the HazOps RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            self._hazard_id = _model.get_value(_row, 2)
        except TypeError:
            self._hazard_id = None

        treeview.handler_unblock(self._lst_handler_id[0])

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

    def _do_load_page(self, attributes):
        """
        Load the HazOps RAMSTKTreeView().

        :return: None
        :rtype: None
        """
        # pylint: disable=attribute-defined-outside-init
        self._revision_id = attributes["revision_id"]
        self._parent_id = attributes["hardware_id"]
        self._hazard_id = attributes["hazard_id"]

        RAMSTKWorkView.on_select(
            self,
            title=_("Hazards analysis for Hardware ID {0:d}", ).format(
                self._parent_id, ),
        )

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

    def _do_request_calculate(self, __button):
        """
        Request to calculate the HazOps HRI.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _node_id = '{0:d}.{1:d}'.format(self._hardware_id, self._hazard_id)

        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_calculate_hazop', node_id=_node_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_delete(self, __button):
        """
        Request to delete the selected hazard from the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        _node_id = '{0:d}.{1:d}'.format(self._hardware_id, self._hazard_id)

        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_delete_hazop', node_id=_node_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request to insert a new hazard into the HazOps.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_insert_hazop',
            revision_id=self._revision_id,
            hardware_id=self._hardware_id,
        )
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Request to save the selected Hazard.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _node_id = '{0:d}.{1:d}'.format(self._hardware_id, self._hazard_id)

        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_hazop', node_id=_node_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the HazOps.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_hazops')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the HazOps Work View RAMSTKTreeView().

        :param treeview: the HazOps TreeView RAMSTKTreeView().
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
            _icons = ['add', 'remove', 'calculate', 'save', 'save-all']
            _labels = [
                _("Add Hazard"),
                _("Remove Selected Hazard"),
                _("Calculate HazOp"),
                _("Save Selected Hazard"),
                _("Save All Hazards"),
            ]
            _callbacks = [
                self._do_request_insert_sibling,
                self._do_request_delete,
                self._do_request_calculate,
                self._do_request_update,
                self._do_request_update_all,
            ]
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the HazOps Work View RAMSTKTreeview().

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
            3: 'potential_hazard',
            4: 'potential_cause',
            5: 'assembly_effect',
            6: 'assembly_severity',
            7: 'assembly_probability',
            9: 'assembly_mitigation',
            10: 'assembly_severity_f',
            11: 'assembly_probability_f',
            13: 'system_effect',
            14: 'system_severity',
            15: 'system_probability',
            17: 'system_mitigation',
            18: 'system_severity_f',
            19: 'system_probability_f',
            21: 'remarks',
        }

        if not self.treeview.do_edit_cell(
                __cell,
                path,
                new_text,
                position,
                model,
        ):

            try:
                _key = _dic_keys[self._lst_col_order[position]]
            except KeyError:
                _key = ''

            pub.sendMessage(
                "wvw_editing_hazops",
                module_id=self._hazard_id,
                key=_key,
                value=new_text,
            )
