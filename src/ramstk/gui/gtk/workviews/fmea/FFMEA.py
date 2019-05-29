# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.fmea.FFMEA.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK FFMEA Work View."""

# Third Party Imports
from pubsub import pub
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKFrame, RAMSTKLabel
from ramstk.gui.gtk.ramstk.Widget import Gdk, GdkPixbuf, Gtk, _
from ramstk.gui.gtk.workviews.WorkView import RAMSTKWorkView

# RAMSTK Local Imports
from .FMEA import FMEA


class FFMEA(FMEA):
    """
    Display Functional FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Functional Failure Mode
    and Effects Analysis (FFMEA). The attributes of a FFMEA Work View are:

    :ivar int _function_id: the ID of the Function whose FMEA is being
                            displayed.
    :ivar bool _functional: indicates this is a Functional FMEA.

    _lst_handler_id contains the following callback signals:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | tvw_fmea `cursor_changed`                 |
    +----------+-------------------------------------------+
    |      1   | tvw_fmea `button_press_event`             |
    +----------+-------------------------------------------+
    |      2   | tvw_fmea `edited`                         |
    +----------+-------------------------------------------+
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Functional FMEA.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        FMEA.__init__(self, configuration, module="FFMEA", **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None
        self._functional = True

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, "closed_program")
        pub.subscribe(self._do_load_page, "retrieved_ffmea")

    def __load_combobox(self):
        """
        Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        # Load the severity classes into the Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[7])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_SEVERITY:
            _severity = self.RAMSTK_CONFIGURATION.RAMSTK_SEVERITY[_item][1]
            _model.append((_severity, ))

        # Load the users into the Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[8])

        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_USERS:
            _user = (
                self.RAMSTK_CONFIGURATION.RAMSTK_USERS[_item][0] + ", " +
                self.RAMSTK_CONFIGURATION.RAMSTK_USERS[_item][1]
            )
            _model.append((_user, ))

        # Load the status values into the Gtk.CellRendererCombo()
        _model = self._get_cell_model(self._lst_col_order[10])

        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_ACTION_STATUS:
            _status = self.RAMSTK_CONFIGURATION.RAMSTK_ACTION_STATUS[_item][0]
            _model.append((_status, ))

    def __make_ui(self):
        """
        Make the Functional FMEA Work View page.

        :return: None
        :rtype: None
        """
        _buttonbox = FMEA._make_buttonbox(
            self,
            tooltips=[
                _(
                    "Add a new FFMEA entity at the same level as the "
                    "currently selected entity.", ),
                _(
                    "Add a new FFMEA entity one level below the currently "
                    "selected entity.", ),
                _("Remove the selected entity from the FFMEA."),
            ],
            callbacks=[
                self.do_request_insert_sibling,
                self.do_request_insert_child,
                self._do_request_delete,
            ],
            icons=["insert_sibling", "insert_child", "remove"],
        )

        self.pack_start(_buttonbox, False, True, 0)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrollwindow.add(self.treeview)

        _frame = RAMSTKFrame(
            label=_("Functional Failure Mode and Effects Analysis (FFMEA)"), )
        _frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack_end(_frame, True, True, 0)

        _label = RAMSTKLabel(
            _("FFMEA"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays the Functional Failure Mode and Effects "
                "Analysis (FFMEA) for the selected function.", ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback methods and functions for the FFMEA widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.treeview.connect("cursor_changed", self._do_change_row), )
        self._lst_handler_id.append(
            self.treeview.connect(
                "button_press_event",
                self._on_button_press,
            ), )

        for _idx in self._lst_col_order:
            _cell = self.treeview.get_column(
                self._lst_col_order[_idx], ).get_cells()

            if isinstance(_cell[0], Gtk.CellRendererPixbuf):
                pass
            elif isinstance(_cell[0], Gtk.CellRendererToggle):
                _cell[0].connect(
                    "toggled",
                    self._on_cell_edit,
                    None,
                    _idx,
                    self.treeview.get_model(),
                )
            elif isinstance(_cell[0], Gtk.CellRendererCombo):
                _cell[0].connect(
                    "edited",
                    self._on_cell_edit,
                    _idx,
                    self.treeview.get_model(),
                )
            else:
                _cell[0].connect(
                    "edited",
                    self._on_cell_edit,
                    _idx,
                    self.treeview.get_model(),
                )

    def __set_properties(self):
        """
        Set the properties of the Functional FMEA RAMSTK widgets.

        :return: None
        :rtype: None
        """
        self._dic_headings["mode"][0] = _("Mode ID")
        for _index in [1, 2, 3, 4, 5, 6, 7, 16]:
            self._dic_headings["mode"][_index] = self.treeview.headings[
                self._lst_col_order[_index]
            ]

        self._dic_headings["cause"][0] = _("Cause ID")
        self._dic_headings["cause"][1] = _("Failure\nCause")

        self._dic_headings["control"][0] = _("Control ID")
        self._dic_headings["control"][1] = _("Existing\nControl")

        self._dic_headings["action"][0] = _("Action ID")
        self._dic_headings["action"][1] = _("Recommended\nAction")
        for _index in [8, 9, 10, 11, 12, 13, 14, 15]:
            self._dic_headings["action"][_index] = self.treeview.headings[
                self._lst_col_order[_index]
            ]

        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _(
                "Displays the Functional Failure Mode and Effects "
                "Analysis (FFMEA) for the currently selected "
                "Function.", ), )

    def _do_change_row(self, treeview):
        """
        Handle events for the Functional FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param treeview: the Functional FMEA RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 18)
            _headings = self._dic_headings[self._get_level(_node_id)]
        except (KeyError, TypeError):
            _node_id = 0
            _headings = []

        _columns = self.treeview.get_columns()

        i = 0

        for _heading in _headings:
            _label = RAMSTKLabel(
                _heading,
                justify=Gtk.Justification.CENTER,
                wrap=True,
            )
            _label.show_all()
            _columns[i].set_widget(_label)

            if _heading == "":
                _columns[i].set_visible(False)
            else:
                _columns[i].set_visible(True)

            i += 1

        treeview.handler_unblock(self._lst_handler_id[0])

    def _do_load_page(self, attributes):
        """
        Iterate through the tree and load the Functional FMEA RAMSTKTreeView().

        :param dict attributes: a dict of attribute key:value pairs for the
                                selected Functional FMEA.
        :return: None
        :rtype: None
        """
        _row = attributes['row']
        _tree = attributes['tree']

        _data = []
        _model = self.treeview.get_model()

        _node = _tree.nodes[list(SortedDict(_tree.nodes).keys())[0]]
        _entity = _node.data
        try:
            if _entity.is_mode:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["mode"],
                    22,
                    22,
                )
                _data = [
                    _entity.mode_id,
                    _entity.description,
                    _entity.effect_local,
                    _entity.effect_next,
                    _entity.effect_end,
                    _entity.design_provisions,
                    _entity.operator_actions,
                    _entity.severity_class,
                    "",
                    "",
                    "",
                    "",
                    0,
                    "",
                    0,
                    "",
                    _entity.remarks,
                    _icon,
                    _node.identifier,
                ]
                _row = None
            elif _entity.is_cause and _row is not None:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["cause"],
                    22,
                    22,
                )
                _data = [
                    _entity.cause_id,
                    _entity.description,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    0,
                    "",
                    0,
                    "",
                    "",
                    _icon,
                    _node.identifier,
                ]
            elif _entity.is_control and _row is not None:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["control"],
                    22,
                    22,
                )
                _data = [
                    _entity.control_id,
                    _entity.description,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    0,
                    "",
                    0,
                    "",
                    "",
                    _icon,
                    _node.identifier,
                ]
            elif _entity.is_action and _row is not None:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["action"],
                    22,
                    22,
                )
                _data = [
                    _entity.action_id,
                    _entity.action_recommended,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    _entity.action_owner,
                    _entity.action_due_date,
                    _entity.action_status,
                    _entity.action_taken,
                    _entity.action_approved,
                    _entity.action_approve_date,
                    _entity.action_closed,
                    _entity.action_close_date,
                    "",
                    _icon,
                    _node.identifier,
                ]

            try:
                _new_row = _model.append(_row, _data)
            except TypeError:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more Functional FMEA line items had the wrong "
                        "data type in it's data package and is not displayed "
                        "in the FMEA form.", ), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    "RAMSTK ERROR: Data for FMEA ID {0:s} for Function ID "
                    "{1:s} is the wrong type for one or more "
                    "columns.".format(
                        str(_node.identifier),
                        str(self._function_id),
                    ), )
                _new_row = None
            except ValueError:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more Functional FMEA line items was missing "
                        "some of it's data and is not displayed in the FMEA "
                        "form.", ), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    "RAMSTK ERROR: Too few fields for FMEA ID {0:s} for "
                    "Function ID {1:s}.".format(
                        str(_node.identifier),
                        str(self._function_id),
                    ), )
                _new_row = None

        except AttributeError:
            if _node.identifier != 0:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more Functional FMEA line items was missing "
                        "it's data package and is not displayed in the FMEA "
                        "form.", ), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    "RAMSTK ERROR: There is no data package for FMEA ID {0:s} "
                    "for Function ID {1:s}.".format(
                        str(_node.identifier),
                        str(self._function_id),
                    ), )
            _new_row = None

        for _n in _tree.children(_node.identifier):
            _child_tree = _tree.subtree(_n.identifier)
            self._do_load_page(
                attributes={
                    "tree": _child_tree,
                    "row": _new_row,
                }, )

        _row = _model.get_iter_first()
        self.treeview.expand_all()

        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Failure Modes for Function ID {0:d}").format(
                self._function_id, ),
        )

        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the Functional FMEA.

        :return: None
        :rtype: None
        """
        _sibling = kwargs["sibling"]

        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 18)
            _level = self._get_level(_node_id)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = "0"
            _level = "mode"
            _prow = None

        # Dict to hold the set of arguments to use for flow control.
        # Outer key is FMEA level.  Inner key determines whether sibling or
        # child is requested for insert.  Value is the entity ID, parent ID,
        # whether to raise ActionControl dialog, and if an undefined condition
        # exists (no child for control or action).
        _dic_args = {
            "mode": {
                True: [self._function_id, 0, False, False],
                False:
                [_model.get_value(_row, 0), _node_id, "cause", False, False],
            },
            "cause": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 18),
                    False,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, True, False],
            },
            "control": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 18),
                    True,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, False, True],
            },
            "action": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 18),
                    True,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, False, True],
            },
        }

        # The _entity_id is the RAMSTK Program database Function ID, or Mode
        # ID, to add the new entity to.  The _parent_id is the Node ID of the
        # parent node in the treelib Tree().
        (
            _entity_id,
            _parent_id,
            _choose,
            _undefined,
        ) = _dic_args[_sibling][_level]

        if _level == "mode" and not _sibling:
            _level = "cause"

        FMEA._do_request_insert(
            entity_id=_entity_id,
            parent_id=_parent_id,
            level=_level,
            choose=_choose,
            undefined=_undefined,
        )

    @staticmethod
    def _get_level(node_id):
        """
        Return the level in the Functional FMEA based on the Node ID.

        :param str node_id: the Node ID of the selected Node in the Functional
                            FMEA Tree().
        :return: _level
        :rtype: str
        """
        _level = ""

        if node_id.count(".") <= 1:
            _level = "mode"
        elif node_id.count(".") == 2:
            _level = "cause"
        elif node_id.count(".") == 3 and node_id[-1] == "c":
            _level = "control"
        elif node_id.count(".") == 3 and node_id[-1] == "a":
            _level = "action"

        return _level

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Functional FMEA Work View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`.
        :param str path: the path that was edited.
        :param str new_text: the edited text.
        :param int position: the column position in the RAMSTKTreeView() that
                             is being edited.
        :param model: the Gtk.TreeModel() for the Functional FMEA
                      RAMSTKTreeView().
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _dic_keys = {
            1: 'description',
            2: 'effect_local',
            3: 'effect_next',
            4: 'effect_end',
            5: 'design_provisions',
            6: 'operator_actions',
            7: 'severity_class',
            8: 'action_owner',
            9: 'action_due_date',
            10: 'action_status',
            11: 'action_taken',
            12: 'action_approved',
            13: 'action_approve_date',
            14: 'action_closed',
            15: 'action_close_date',
            16: 'remarks',
        }

        _node_id = model.get_value(model.get_iter(path), 0)
        try:
            _key = _dic_keys[position]
        except KeyError:
            _key = ""

        if not self.treeview.do_edit_cell(
                __cell,
                path,
                new_text,
                position,
                model,
        ):

            self.do_set_cursor(Gdk.CursorType.WATCH)
            pub.sendMessage(
                'wvw_editing_fmea',
                module_id=_node_id,
                key=_key,
                value=new_text,
            )
            self.do_set_cursor(Gdk.CursorType.LEFT_PTR)
