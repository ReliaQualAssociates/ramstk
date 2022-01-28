# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.program_status.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Program Status Panels."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
import pandas as pd

# noinspection PyPackageValidations,PyPackageRequirements
from matplotlib.patches import Ellipse
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKPlotPanel

register_matplotlib_converters()


class ProgramStatusPlotPanel(RAMSTKPlotPanel):
    """Panel to display the Verification plan efforts."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "status_id"
    _select_msg = "selected_revision"
    _tag = "program_status"
    _title = _("Verification Plan Effort")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Burndown Curve panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.
        self.lst_axis_labels = [_(""), _("Total Time [hours]")]
        self.lst_legend = [
            _("Minimum Expected Time"),
            _("Mean Expected Time"),
            _("Maximum Expected Time"),
            _("Actual Remaining Time"),
        ]

        # Initialize public scalar instance attributes.
        self.plot_title = _("Total Verification Effort")

        super().do_make_panel()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, "succeed_calculate_verification_plan")
        pub.subscribe(self._do_load_actuals, "succeed_get_actual_status")

    def _do_load_panel(self, attributes: Dict[str, pd.DataFrame]) -> None:
        """Load the burndown curve with the planned and actual status.

        :param attributes: a dict containing a pandas DataFrames() for each of
            planned burndown and assessment dates/targets.
        :return: None
        """
        self._do_load_plan(attributes["plan"])
        self._do_load_assessment_milestones(
            attributes["assessed"], attributes["plan"].loc[:, "upper"].max()
        )

        super().do_load_panel()

        pub.sendMessage("request_get_actual_status")

    def _do_load_actuals(self, status: pd.DataFrame) -> None:
        """Load the actual progress status points.

        :param status: a Pandas dataframe containing a pandas DataFrames() for the
            actual progress.
        :return: None
        """
        self.pltPlot.do_add_line(
            x_values=list(status.index),
            y_values=list(status.loc[:, "time"]),
            marker="o",
        )

    def _do_load_assessment_milestones(
        self, assessed: pd.DataFrame, y_max: float
    ) -> None:
        """Add the reliability assessment milestones to the plot.

        This method will add a vertical line at all the dates identified as
        dates when a reliability assessment is due.  Annotated along side
        these markers are the reliability targets (lower, mean, upper) for that
        assessment date.

        :return: None
        :rtype: None
        """
        _y_max = max(1.0, y_max)

        for _date in list(assessed.index):
            self.pltPlot.axis.axvline(
                x=_date,
                ymin=0,
                ymax=1.05 * _y_max,
                color="k",
                linewidth=1.0,
                linestyle="-.",
            )
            self.pltPlot.axis.annotate(
                str(self.fmt.format(assessed.loc[pd.to_datetime(_date), "upper"]))
                + "\n"
                + str(self.fmt.format(assessed.loc[pd.to_datetime(_date), "mean"]))
                + "\n"
                + str(self.fmt.format(assessed.loc[pd.to_datetime(_date), "lower"])),
                xy=(_date, 0.9 * _y_max),
                xycoords="data",
                xytext=(-55, 0),
                textcoords="offset points",
                size=12,
                va="center",
                bbox=dict(boxstyle="round", fc="#E5E5E5", ec="None", alpha=0.5),
                arrowprops=dict(
                    arrowstyle="wedge,tail_width=1.",
                    fc="#E5E5E5",
                    ec="None",
                    alpha=0.5,
                    patchA=None,
                    patchB=Ellipse((2, -1), 0.5, 0.5),
                    relpos=(0.2, 0.5),
                ),
            )

    def _do_load_plan(self, plan: pd.DataFrame) -> None:
        """Load the verification plan burndown curve.

        :param plan: the pandas DataFrame() containing the planned task end
            dates and remaining hours of work (lower, mean, upper).
        :return: None
        :rtype: None
        """
        self.pltPlot.axis.cla()
        self.pltPlot.axis.grid(True, which="both")

        self.pltPlot.do_load_plot(
            **{
                "x_values": list(plan.index),
                "y_values": list(plan.loc[:, "lower"]),
                "plot_type": "date",
                "marker": "g--",
            }
        )
        self.pltPlot.do_load_plot(
            **{
                "x_values": list(plan.index),
                "y_values": list(plan.loc[:, "mean"]),
                "plot_type": "date",
                "marker": "b-",
            }
        )
        self.pltPlot.do_load_plot(
            **{
                "x_values": list(plan.index),
                "y_values": list(plan.loc[:, "upper"]),
                "plot_type": "date",
                "marker": "r--",
            }
        )
