# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.fmea.FFMEA.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK FFMEA Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKFrame, RAMSTKLabel
from ramstk.gui.gtk.ramstk.Widget import Gtk, _

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

    # Define private dict attributes.
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

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_page, "retrieved_ffmea")

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

    def __set_properties(self):
        """
        Set the properties of the Functional FMEA RAMSTK widgets.

        :return: None
        :rtype: None
        """
        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _(
                "Displays the Functional Failure Mode and Effects "
                "Analysis (FFMEA) for the currently selected "
                "Function.", ), )

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
