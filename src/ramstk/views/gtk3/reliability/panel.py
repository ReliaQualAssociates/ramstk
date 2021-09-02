# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.reliability.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Reliability Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class ReliabilityInputPanel(RAMSTKFixedPanel):
    """Panel to display hazard rate inputs about the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "reliability"
    _title = _("Reliability Assessment Inputs")

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

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_index_map = {
            2: ["add_adj_factor", "float"],
            7: ["failure_distribution_id", "integer"],
            11: ["hazard_rate_method_id", "integer"],
            17: ["hazard_rate_type_id", "integer"],
            16: ["hazard_rate_specified", "float"],
            22: ["hr_specified_variance", "float"],
            24: ["location_parameter", "float"],
            27: ["mtbf_specified", "float"],
            30: ["mtbf_specified_variance", "float"],
            31: ["mult_adj_factor", "float"],
            39: ["scale_parameter", "float"],
            40: ["shape_parameter", "float"],
        }
        self.dic_attribute_widget_map = {
            "hazard_rate_type_id": [
                17,
                self.cmbHRType,
                "changed",
                super().on_changed_combo,
                "wvw_editing_hardware",
                0.0,
                {
                    "tooltip": _(
                        "The type of reliability assessment for the selected hardware "
                        "item."
                    ),
                    "width": 200,
                },
                _("Assessment Type:"),
            ],
            "hazard_rate_method_id": [
                11,
                self.cmbHRMethod,
                "changed",
                super().on_changed_combo,
                "wvw_editing_reliability",
                0.0,
                {
                    "tooltip": _(
                        "The assessment method to use for the selected hardware item."
                    ),
                    "width": 200,
                },
                _("Assessment Method:"),
            ],
            "hazard_rate_specified": [
                16,
                self.txtSpecifiedHt,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                1.0,
                {
                    "tooltip": _("The stated hazard rate."),
                    "width": 125,
                },
                _("Stated Hazard Rate [h(t)]:"),
            ],
            "hr_specified_variance": [
                22,
                self.txtSpecifiedHtVar,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _("The variance of the stated hazard rate."),
                    "width": 125,
                },
                _("Stated h(t) Variance:"),
            ],
            "mtbf_specified": [
                26,
                self.txtSpecifiedMTBF,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _("The stated mean time between failure (MTBF)."),
                    "width": 125,
                },
                _("Stated MTBF:"),
            ],
            "mtbf_specified_variance": [
                30,
                self.txtSpecifiedMTBFVar,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _(
                        "The variance of the stated mean time between failure (MTBF)."
                    ),
                    "width": 125,
                },
                _("Stated MTBF Variance:"),
            ],
            "failure_distribution_id": [
                7,
                self.cmbFailureDist,
                "changed",
                super().on_changed_combo,
                "wvw_editing_reliability",
                0.0,
                {
                    "tooltip": _(
                        "The statistical failure distribution of the selected hardware "
                        "item."
                    ),
                    "width": 200,
                },
                _("Failure Distribution:"),
            ],
            "scale_parameter": [
                39,
                self.txtFailScale,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _(
                        "The scale parameter of the statistical failure distribution."
                    ),
                    "width": 125,
                },
                _("Scale Parameter:"),
            ],
            "shape_parameter": [
                40,
                self.txtFailShape,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _(
                        "The shape parameter of the statistical failure distribution."
                    ),
                    "width": 125,
                },
                _("Shape Parameter:"),
            ],
            "location_parameter": [
                24,
                self.txtFailLocation,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _(
                        "The location parameter of the statistical failure "
                        "distribution."
                    ),
                    "width": 125,
                },
                _("Location Parameter:"),
            ],
            "add_adj_factor": [
                2,
                self.txtAddAdjFactor,
                "changed",
                super().on_changed_entry,
                "wvw_editing_reliability",
                0.0,
                {
                    "tooltip": _(
                        "An adjustment factor to add to the assessed hazard rate."
                    ),
                    "width": 125,
                },
                _("Additive Adjustment Factor:"),
            ],
            "mult_adj_factor": [
                31,
                self.txtMultAdjFactor,
                "changed",
                super().on_changed_entry,
                "mvw_editing_reliability",
                100.0,
                {
                    "tooltip": _(
                        "An adjustment factor to multiply the assessed hazard rate."
                    ),
                    "width": 125,
                },
                _("Multiplicative Adjustment Factor:"),
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.

    def do_load_hr_distributions(self, distributions: List[str]) -> None:
        """Load the hazard rate distribution RAMSTKComboBox().

        :param distributions: the list of s-distribution names RAMSTK
            currently supports.
        :return: None
        """
        self.cmbFailureDist.do_load_combo(entries=distributions)

    def do_load_hr_methods(self, methods: List[str]) -> None:
        """Load the hazard rate method RAMSTKComboBox().

        The hazard rate methods are:

            * MIL-HDBK-217F Parts Count
            * MIL-HDBK-217F Parts Stress
            * NSWC-11

        :param methods: the list of methods for assessing the hazard rate.
        :return: None
        """
        self.cmbHRMethod.do_load_combo(entries=methods)

    def do_load_hr_types(self, hr_types: List[str]) -> None:
        """Load the hazard rate type RAMSTKComboBox().

        The hazard rate types are:

            * Assessed
            * Defined, Hazard Rate
            * Defined, MTBF
            * Defined, Distribution

        :param hr_types: the types (or ways) of establishing the hazard rate
            for a hardware item.
        :return: None
        """
        self.cmbHRType.do_load_combo(entries=hr_types)

    def _do_set_sensitive_assessed(self, type_id: int) -> None:
        """Set the widgets used in handbook assessments sensitive.

        :param type_id: the hazard rate type (source).
        :return: None
        :rtype: None
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

    def _do_set_sensitive_specified_ht(self, type_id: int) -> None:
        """Set the widgets used for specifying a hazard rate sensitive.

        :param type_id: the hazard rate type (source).
        :return: None
        :rtype: None
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

    def _do_set_sensitive_specified_mtbf(self, type_id: int) -> None:
        """Set the widgets used for specifying an MTBF sensitive.

        :param type_id: the hazard rate type (source).
        :return: None
        :rtype: None
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

    def _do_set_sensitive_specified_distribution(self, type_id: int) -> None:
        """Set widgets used for specifying a failure distribution sensitive.

        :param type_id: the hazard rate type (source).
        :return: None
        :rtype: None
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

    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None:
        """Set certain widgets sensitive or insensitive.

        This method will set the sensitivity of various widgets depending on
        the hazard rate assessment type selected.

        :return: None
        :rtype: None
        """
        self._do_set_sensitive_assessed(attributes["hazard_rate_type_id"])
        self._do_set_sensitive_specified_ht(attributes["hazard_rate_type_id"])
        self._do_set_sensitive_specified_mtbf(attributes["hazard_rate_type_id"])
        self._do_set_sensitive_specified_distribution(attributes["hazard_rate_type_id"])
