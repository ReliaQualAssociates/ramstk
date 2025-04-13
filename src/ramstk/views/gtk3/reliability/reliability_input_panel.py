# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.reliability.reliability_input_panel.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Reliability Input panel module."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
)


class ReliabilityInputPanel(RAMSTKFixedPanel):
    """Panel to display hazard rate inputs about the selected Hardware item.

    The widgets of a Reliability input panel are:

    :ivar cmbFailureDist: the RAMSTKComboBox() used to select and display the failure
        distribution for the selected hardware item.
    :ivar cmbHRMethod: the RAMSTKComboBox() used to select and display the method
        used to calculate the hazard rate for the selected hardware item.
    :ivar cmbHRType: the RAMSTKComboBox() used to select and display the hazard rate
    type.
    :ivar txtAddAdjFactor: the RAMSTKEntry() used to input and display the
        hazard rate additive adjustment factor for the selected hardware item.
    :ivar txtFailLocation: the RAMSTKEntry() used to input and display the location
        parameter for the selected failure distribution.
    :ivar txtFailScale: the RAMSTKEntry() used to input and display the scale
        parameter for the selected failure distribution.
    :ivar txtFailShape: the RAMSTKEntry() used to input and display the shape
        parameter for the selected failure distribution.
    :ivar txtMultAdjFactor: the RAMSTKEntry() used to input and display the hazard
        rate multiplicative adjustment factor for the selected hardware item.
    :ivar txtSpecifiedHt: the RAMSTKEntry() used to input and display the specified
        hazard rate for the selected hardware item.
    :ivar txtSpecifiedHtVar: the RAMSTKEntry() used to input and display the variance of
        the specified hazard rate for the selected hardware item.
    :ivar txtSpecifiedMTBF: the RAMSTKEntry() used to input and display the specified
        MTBF for the selected hardware item.
    :ivar txtSpecifiedMTBFVar: the RAMSTKEntry() used to input and display the
        variance of the specified MTBF for the selected hardware item.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_reliability_attributes"
    _tag: str = "reliability"
    _title: str = _("Reliability Assessment Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Assessment Input panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbFailureDist: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbHRMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbHRType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtAddAdjFactor: RAMSTKEntry = RAMSTKEntry()
        self.txtFailLocation: RAMSTKEntry = RAMSTKEntry()
        self.txtFailScale: RAMSTKEntry = RAMSTKEntry()
        self.txtFailShape: RAMSTKEntry = RAMSTKEntry()
        self.txtMultAdjFactor: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecifiedMTBFVar: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.cmbHRType,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hazard_rate_type_id",
                    "index": 17,
                    "label_text": _("Assessment Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The type of reliability assessment for the selected hardware "
                        "item."
                    ),
                    "visible": True,
                    "width": 200,
                },
            },
            {
                "widget": self.cmbHRMethod,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hazard_rate_method_id",
                    "index": 11,
                    "label_text": _("Assessment Method:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The assessment method to use for the selected hardware item."
                    ),
                    "visible": True,
                    "width": 200,
                },
            },
            {
                "widget": self.txtSpecifiedHt,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_specified",
                    "index": 16,
                    "label_text": _("Stated Hazard Rate [h(t)]:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The stated hazard rate."),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtSpecifiedHtVar,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hr_specified_variance",
                    "index": 22,
                    "label_text": _("Stated h(t) Variance:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The variance of the stated hazard rate."),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtSpecifiedMTBF,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_specified",
                    "index": 26,
                    "label_text": _("Stated MTBF:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The stated mean time between failure (MTBF)."),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtSpecifiedMTBFVar,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mtbf_specified_variance",
                    "index": 30,
                    "label_text": _("Stated MTBF Variance:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The variance of the stated mean time between failure (MTBF)."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.cmbFailureDist,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "failure_distribution_id",
                    "index": 7,
                    "label_text": _("Failure Distribution:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The statistical failure distribution of the selected "
                        "hardware item."
                    ),
                    "visible": True,
                    "width": 200,
                },
            },
            {
                "widget": self.txtFailScale,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "scale_parameter",
                    "index": 39,
                    "label_text": _("Scale Parameter:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The scale parameter of the statistical failure distribution."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtFailShape,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "shape_parameter",
                    "index": 40,
                    "label_text": _("Shape Parameter:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The shape parameter of the statistical failure distribution."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtFailLocation,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "location_parameter",
                    "index": 24,
                    "label_text": _("Location Parameter:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The location parameter of the statistical failure "
                        "distribution."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtAddAdjFactor,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "add_adj_factor",
                    "index": 2,
                    "label_text": _("Additive Adjustment Factor:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "An adjustment factor to add to the assessed hazard rate."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
            {
                "widget": self.txtMultAdjFactor,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "mult_adj_factor",
                    "index": 31,
                    "label_text": _("Multiplicative Adjustment Factor:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "An adjustment factor to multiply the assessed hazard rate."
                    ),
                    "visible": True,
                    "width": 125,
                },
            },
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

    def do_load_hr_distributions(self, distributions: List[List[str]]) -> None:
        """Load the hazard rate distribution RAMSTKComboBox().

        :param distributions: the list of s-distribution names RAMSTK currently
            supports.
        """
        self.cmbFailureDist.do_load_combo(distributions)

    def do_load_hr_methods(self, methods: List[List[str]]) -> None:
        """Load the hazard rate method RAMSTKComboBox().

        The hazard rate methods are:

            * MIL-HDBK-217F Parts Count
            * MIL-HDBK-217F Parts Stress
            * NSWC-11

        :param methods: the list of methods for assessing the hazard rate.
        """
        self.cmbHRMethod.do_load_combo(methods)

    def do_load_hr_types(self, hr_types: List[List[str]]) -> None:
        """Load the hazard rate type RAMSTKComboBox().

        The hazard rate types are:

            * Assessed
            * Defined, Hazard Rate
            * Defined, MTBF
            * Defined, Distribution

        :param hr_types: the types (or ways) of establishing the hazard rate
            for a hardware item.
        """
        self.cmbHRType.do_load_combo(hr_types)

    def _set_sensitive(self, attributes: Dict[str, Any]) -> None:
        """Set certain widgets sensitive or insensitive.

        This method will set the sensitivity of various widgets depending on the hazard
        rate assessment type selected.
        """
        self._set_sensitive_assessed(attributes["hazard_rate_type_id"])
        self._set_sensitive_specified_ht(attributes["hazard_rate_type_id"])
        self._set_sensitive_specified_mtbf(attributes["hazard_rate_type_id"])
        self._set_sensitive_specified_distribution(attributes["hazard_rate_type_id"])

    def _set_sensitive_assessed(self, type_id: int) -> None:
        """Set the widgets used in handbook assessments sensitive.

        :param type_id: the hazard rate type (source).
        """
        if type_id == 1:  # Assessed hazard rate using handbook models.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(True)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)

    def _set_sensitive_specified_ht(self, type_id: int) -> None:
        """Set the widgets used for specifying a hazard rate sensitive.

        :param type_id: the hazard rate type (source).
        """
        if type_id == 2:  # User specified hazard rate.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(True)
            self.txtSpecifiedHtVar.set_sensitive(True)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)

    def _set_sensitive_specified_mtbf(self, type_id: int) -> None:
        """Set the widgets used for specifying an MTBF sensitive.

        :param type_id: the hazard rate type (source).
        """
        if type_id == 3:  # User specified MTBF.
            self.cmbFailureDist.set_sensitive(False)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(False)
            self.txtFailScale.set_sensitive(False)
            self.txtFailShape.set_sensitive(False)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(True)
            self.txtSpecifiedMTBFVar.set_sensitive(True)

    def _set_sensitive_specified_distribution(self, type_id: int) -> None:
        """Set widgets used for specifying a failure distribution sensitive.

        :param type_id: the hazard rate type (source).
        """
        if type_id == 4:
            self.cmbFailureDist.set_sensitive(True)
            self.cmbHRMethod.set_sensitive(False)
            self.txtFailLocation.set_sensitive(True)
            self.txtFailScale.set_sensitive(True)
            self.txtFailShape.set_sensitive(True)
            self.txtSpecifiedHt.set_sensitive(False)
            self.txtSpecifiedHtVar.set_sensitive(False)
            self.txtSpecifiedMTBF.set_sensitive(False)
            self.txtSpecifiedMTBFVar.set_sensitive(False)
