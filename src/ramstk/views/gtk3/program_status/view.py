# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.program_status.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Program Status Views."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKFrame, RAMSTKPlot, RAMSTKWorkView

# RAMSTK Local Imports
from . import ProgramStatusPlotPanel

register_matplotlib_converters()


class ProgramStatusWorkView(RAMSTKWorkView):
    """Display Verification task burn down curve in the RAMSTK Work Book.

    The Verification burn down Curve displays the planned burn down curve (
    solid line) for all tasks in the V&V plan as well as the actual progress
    (points).  The attributes of a Verification burn down curve view are:

    :cvar _tag: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "validation"
    _tablabel = (
        "<span weight='bold'>" + _("Program\nVerification\nProgress") + "</span>"
    )
    _tabtooltip = _(
        "Shows a plot of the total expected time to complete all verification "
        "tasks and the current progress on those tasks."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Work View for the Verification package.

        :param configuration: the RAMSTK configuration instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate_all,
        ]
        self._lst_icons = [
            "charts",
        ]
        self._lst_mnu_labels = [_("Plot Verification Effort")]
        self._lst_tooltips = [
            _(
                "Plot the overall Verification program plan (i.e., "
                "all Verification tasks) and current status."
            ),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = ProgramStatusPlotPanel()

        self._title: str = _("Program Verification Effort")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pltPlot: RAMSTKPlot = RAMSTKPlot()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_validation")

        pub.subscribe(self._do_set_cursor_active, "succeed_calculate_verification_plan")

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_plan",
        )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_set_cursor_active(self, attributes: Dict[str, Any]) -> None:
        """Wrap do_set_cursor_active() of the meta-class.

        This method is called whenever the verification plan is calculated
        successfully.  That PyPubSub MDS includes an attributes data package
        (which is a dict containing the data to plot).  This method is
        needed since the meta-class do_set_cursor_active() method is
        expecting a treelib.Tree() in the MDS.

        :param attributes: the attributes dict for the selected Validation
            task.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_active()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Verification task record ID.

        :param attributes: the attributes dict for the selected Validation
            task.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["record_id"] = attributes["validation_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Verification Status tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        _frame: RAMSTKFrame = RAMSTKFrame()
        _frame.do_set_properties(**{"title": _("Program Verification Effort")})
        _frame.add(self._pnlPanel)

        self.pack_end(_frame, True, True, 0)
        self.show_all()
