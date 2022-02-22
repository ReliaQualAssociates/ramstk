# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.reliability.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Reliability Panels."""

# Standard Library Imports
import locale
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class ReliabilityInputPanel(RAMSTKFixedPanel):
    """Panel to display hazard rate inputs about the selected Hardware item.

    The widgets of a Reliability input panel are:

    :ivar cmbFailureDist: the RAMSTKComboBox() used to select and display the failure
        distribution for the selected hardware item.
    :ivar cmbHRMethod: the RAMSTKComboBox() used to select and display the method
        used to calculate the hazard rate for the selected hardware item.
    :ivar cmbHRType: the RAMSTKComboBox() used to select and display the
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

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "hazard_rate_type_id": [
                17,
                self.cmbHRType,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The type of reliability assessment for the selected hardware "
                        "item."
                    ),
                    "width": 200,
                },
                _("Assessment Type:"),
                "gint",
            ],
            "hazard_rate_method_id": [
                11,
                self.cmbHRMethod,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The assessment method to use for the selected hardware item."
                    ),
                    "width": 200,
                },
                _("Assessment Method:"),
                "gint",
            ],
            "hazard_rate_specified": [
                16,
                self.txtSpecifiedHt,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The stated hazard rate."),
                    "width": 125,
                },
                _("Stated Hazard Rate [h(t)]:"),
                "gfloat",
            ],
            "hr_specified_variance": [
                22,
                self.txtSpecifiedHtVar,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The variance of the stated hazard rate."),
                    "width": 125,
                },
                _("Stated h(t) Variance:"),
                "gfloat",
            ],
            "mtbf_specified": [
                26,
                self.txtSpecifiedMTBF,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The stated mean time between failure (MTBF)."),
                    "width": 125,
                },
                _("Stated MTBF:"),
                "gfloat",
            ],
            "mtbf_specified_variance": [
                30,
                self.txtSpecifiedMTBFVar,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The variance of the stated mean time between failure (MTBF)."
                    ),
                    "width": 125,
                },
                _("Stated MTBF Variance:"),
                "gfloat",
            ],
            "failure_distribution_id": [
                7,
                self.cmbFailureDist,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The statistical failure distribution of the selected hardware "
                        "item."
                    ),
                    "width": 200,
                },
                _("Failure Distribution:"),
                "gint",
            ],
            "scale_parameter": [
                39,
                self.txtFailScale,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The scale parameter of the statistical failure distribution."
                    ),
                    "width": 125,
                },
                _("Scale Parameter:"),
                "gfloat",
            ],
            "shape_parameter": [
                40,
                self.txtFailShape,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The shape parameter of the statistical failure distribution."
                    ),
                    "width": 125,
                },
                _("Shape Parameter:"),
                "gfloat",
            ],
            "location_parameter": [
                24,
                self.txtFailLocation,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The location parameter of the statistical failure "
                        "distribution."
                    ),
                    "width": 125,
                },
                _("Location Parameter:"),
                "gfloat",
            ],
            "add_adj_factor": [
                2,
                self.txtAddAdjFactor,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "An adjustment factor to add to the assessed hazard rate."
                    ),
                    "width": 125,
                },
                _("Additive Adjustment Factor:"),
                "gfloat",
            ],
            "mult_adj_factor": [
                31,
                self.txtMultAdjFactor,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                1.0,
                {
                    "tooltip": _(
                        "An adjustment factor to multiply the assessed hazard rate."
                    ),
                    "width": 125,
                },
                _("Multiplicative Adjustment Factor:"),
                "gfloat",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.

    def do_load_hr_distributions(self, distributions: List[str]) -> None:
        """Load the hazard rate distribution RAMSTKComboBox().

        :param distributions: the list of s-distribution names RAMSTK currently
            supports.
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


class ReliabilityResultsPanel(RAMSTKFixedPanel):
    """Panel to display reliability results for the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_reliability_attributes"
    _tag: str = "reliability"
    _title: str = _("Reliability Assessment Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Reliability Results panel."""
        super().__init__()

        # Initialize widgets.
        self.txtActiveHt: RAMSTKEntry = RAMSTKEntry()
        self.txtActiveHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHt: RAMSTKEntry = RAMSTKEntry()
        self.txtDormantHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionHtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBF: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionMTBFVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionRtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtPercentHt: RAMSTKEntry = RAMSTKEntry()
        self.txtSoftwareHt: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "hazard_rate_active": [
                8,
                self.txtActiveHt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the active failure intensity for the selected "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Active Failure Intensity [\u03BB(t)]:"),
                "gfloat",
            ],
            "hr_active_variance": [
                18,
                self.txtActiveHtVar,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "Displays the variance on the active failure intensity "
                        "for the selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "hazard_rate_dormant": [
                9,
                self.txtDormantHt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the dormant failure intensity for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                _("Dormant \u03BB(t):"),
                "gfloat",
            ],
            "hr_dormant_variance": [
                19,
                self.txtDormantHtVar,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "Displays the variance on the dormant failure intensity "
                        "for the selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "hazard_rate_software": [
                15,
                self.txtSoftwareHt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the software failure intensity for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                _("Software \u03BB(t):"),
                "gfloat",
            ],
            "hazard_rate_logistics": [
                10,
                self.txtLogisticsHt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the logistics failure intensity for the "
                        "selected hardware item.  This is the sum of the "
                        "active, dormant, and software hazard rates."
                    ),
                    "width": 125,
                },
                _("Logistics \u03BB(t):"),
                "gfloat",
            ],
            "hr_logistics_variance": [
                20,
                self.txtLogisticsHtVar,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "Displays the variance on the logistics failure "
                        "intensity for the selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "hazard_rate_mission": [
                12,
                self.txtMissionHt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the mission failure intensity for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                _("Mission \u03BB(t):"),
                "gfloat",
            ],
            "hr_mission_variance": [
                21,
                self.txtMissionHtVar,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the variance on the mission failure "
                        "intensity for the selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "hazard_rate_percent": [
                14,
                self.txtPercentHt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the percentage of the system failure "
                        "intensity the selected hardware item represents."
                    ),
                    "width": 125,
                },
                _("Percent \u03BB(t):"),
                "gfloat",
            ],
            "mtbf_logistics": [
                25,
                self.txtLogisticsMTBF,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the logistics mean time between failure "
                        "(MTBF) for the selected hardware item."
                    ),
                    "width": 125,
                },
                _("Logistics MTBF:"),
                "gfloat",
            ],
            "mtbf_logistics_variance": [
                28,
                self.txtLogisticsMTBFVar,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the variance on the logistics MTBF for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "mtbf_mission": [
                26,
                self.txtMissionMTBF,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the mission mean time between failure (MTBF) "
                        "for the selected hardware item."
                    ),
                    "width": 125,
                },
                _("Mission MTBF:"),
                "gfloat",
            ],
            "mtbf_mission_variance": [
                29,
                self.txtMissionMTBFVar,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the variance on the mission MTBF for the selected "
                        "hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "reliability_logistics": [
                35,
                self.txtLogisticsRt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the logistics reliability for the selected "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Logistics Reliability [R(t)]:"),
                "gfloat",
            ],
            "reliability_log_variance": [
                37,
                self.txtLogisticsRtVar,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the variance on the logistics reliability "
                        "for the selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "reliability_mission": [
                36,
                self.txtMissionRt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the mission reliability for the selected "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Mission R(t):"),
                "gfloat",
            ],
            "reliability_miss_variance": [
                38,
                self.txtMissionRtVar,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the variance on the mission reliability for "
                        "the selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        self.__do_nudge_widgets()

        # Subscribe to PyPubSub messages.

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the RAMSTKEntry() widgets.

        This method ensures results RAMSTKEntry() widgets are set insensitive and
        loads the contents.  The PyPubSub subscriber is in the metaclass.

        :return: None
        :rtype: None
        """
        self._do_load_entries_hazard_rate(attributes)
        self._do_load_entries_mtbf(attributes)
        self._do_load_entries_reliability(attributes)

    def _do_load_entries_hazard_rate(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the hazard rate RAMSTKEntry().

        :return: None
        :rtype: None
        """
        self.txtActiveHt.do_update(
            str(self.fmt.format(attributes["hazard_rate_active"] or 0.0)),
            signal="changed",
        )
        self.txtActiveHtVar.do_update(
            str(self.fmt.format(attributes["hr_active_variance"] or 0.0)),
            signal="changed",
        )
        self.txtDormantHt.do_update(
            str(self.fmt.format(attributes["hazard_rate_dormant"] or 0.0)),
            signal="changed",
        )
        self.txtDormantHtVar.do_update(
            str(self.fmt.format(attributes["hr_dormant_variance"] or 0.0)),
            signal="changed",
        )
        self.txtSoftwareHt.do_update(
            str(self.fmt.format(attributes["hazard_rate_software"] or 0.0)),
            signal="changed",
        )
        self.txtLogisticsHt.do_update(
            str(self.fmt.format(attributes["hazard_rate_logistics"] or 0.0)),
            signal="changed",
        )
        self.txtLogisticsHtVar.do_update(
            str(self.fmt.format(attributes["hr_logistics_variance"] or 0.0)),
            signal="changed",
        )
        self.txtMissionHt.do_update(
            str(self.fmt.format(attributes["hazard_rate_mission"] or 0.0)),
            signal="changed",
        )
        self.txtMissionHtVar.do_update(
            str(self.fmt.format(attributes["hr_mission_variance"] or 0.0)),
            signal="changed",
        )
        self.txtPercentHt.do_update(
            str(self.fmt.format(attributes["hazard_rate_percent"] or 0.0)),
            signal="changed",
        )

    def _do_load_entries_mtbf(self, attributes: Dict[str, Any]) -> None:
        """Load contents of MTBF RAMSTKEntry().

        :return: None
        :rtype: None
        """
        self.txtLogisticsMTBF.do_update(
            str(self.fmt.format(attributes["mtbf_logistics"] or 0.0)),
            signal="changed",
        )
        self.txtLogisticsMTBFVar.do_update(
            str(self.fmt.format(attributes["mtbf_logistics_variance"] or 0.0)),
            signal="changed",
        )
        self.txtMissionMTBF.do_update(
            str(self.fmt.format(attributes["mtbf_mission"] or 0.0)),
            signal="changed",
        )
        self.txtMissionMTBFVar.do_update(
            str(self.fmt.format(attributes["mtbf_mission_variance"] or 0.0)),
            signal="changed",
        )

    def _do_load_entries_reliability(self, attributes: Dict[str, Any]) -> None:
        """Load contents of reliability RAMSTKEntry().

        :return: None
        :rtype: None
        """
        self.txtLogisticsRt.do_update(
            str(self.fmt.format(attributes["reliability_logistics"] or 1.0)),
            signal="changed",
        )
        self.txtLogisticsRtVar.do_update(
            str(self.fmt.format(attributes["reliability_log_variance"] or 0.0)),
            signal="changed",
        )
        self.txtMissionRt.do_update(
            str(self.fmt.format(attributes["reliability_mission"] or 1.0)),
            signal="changed",
        )
        self.txtMissionRtVar.do_update(
            str(self.fmt.format(attributes["reliability_miss_variance"] or 0.0)),
            signal="changed",
        )

    def __do_nudge_widgets(self) -> None:
        """Adjust widgets from their default positions.

        :return: None
        :rtype: None
        """
        _lst_labels: List[object] = []
        _x_pos: List[int] = [
            0,
            self.txtActiveHt.get_preferred_size()[0].width + 5,
        ]
        _y_pos: List[int] = []
        _n_rows: int = 0

        _fixed = self.get_children()[0].get_children()[0].get_children()[0]
        _widgets = (
            self.get_children()[0].get_children()[0].get_children()[0].get_children()
        )

        for _widget in _widgets[::2]:
            _y_pos.append(_fixed.child_get_property(_widget, "y"))
            if _widget.get_text() != "":
                _lst_labels.append(_widget)
                _x_pos[0] = max(_x_pos[0], _widget.get_preferred_size()[0].width)
                _n_rows += 1

        _x_pos[0] += 10
        _x_pos[1] = _x_pos[0] + _x_pos[1] + 5
        for _idx, _pos in enumerate(_y_pos[:_n_rows]):
            _fixed.move(_lst_labels[_idx], 5, _pos)

        _fixed.move(self.txtActiveHtVar, _x_pos[1], _y_pos[0])
        _fixed.move(self.txtDormantHt, _x_pos[0], _y_pos[1])
        _fixed.move(self.txtDormantHtVar, _x_pos[1], _y_pos[1])
        _fixed.move(self.txtSoftwareHt, _x_pos[0], _y_pos[2])
        _fixed.move(self.txtLogisticsHt, _x_pos[0], _y_pos[3])
        _fixed.move(self.txtLogisticsHtVar, _x_pos[1], _y_pos[3])
        _fixed.move(self.txtMissionHt, _x_pos[0], _y_pos[4])
        _fixed.move(self.txtMissionHtVar, _x_pos[1], _y_pos[4])
        _fixed.move(self.txtPercentHt, _x_pos[0], _y_pos[5])
        _fixed.move(self.txtLogisticsMTBF, _x_pos[0], _y_pos[6])
        _fixed.move(self.txtLogisticsMTBFVar, _x_pos[1], _y_pos[6])
        _fixed.move(self.txtMissionMTBF, _x_pos[0], _y_pos[7])
        _fixed.move(self.txtMissionMTBFVar, _x_pos[1], _y_pos[7])
        _fixed.move(self.txtLogisticsRt, _x_pos[0], _y_pos[8])
        _fixed.move(self.txtLogisticsRtVar, _x_pos[1], _y_pos[8])
        _fixed.move(self.txtMissionRt, _x_pos[0], _y_pos[9])
        _fixed.move(self.txtMissionRtVar, _x_pos[1], _y_pos[9])


class AvailabilityResultsPanel(RAMSTKFixedPanel):
    """Panel to display availability results for the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_reliability_attributes"
    _tag: str = "reliability"
    _title: str = _("Availability Assessment Results")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Availability Results panel."""
        super().__init__()

        # Initialize widgets.
        self.txtCostFailure: RAMSTKEntry = RAMSTKEntry()
        self.txtCostHour: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAt: RAMSTKEntry = RAMSTKEntry()
        self.txtLogisticsAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAt: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionAtVar: RAMSTKEntry = RAMSTKEntry()
        self.txtPartCount: RAMSTKEntry = RAMSTKEntry()
        self.txtTotalCost: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "availability_logistics": [
                3,
                self.txtLogisticsAt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the logistics availability for the selected "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Logistics Availability [A(t)]:"),
                "gfloat",
            ],
            "avail_log_variance": [
                5,
                self.txtLogisticsAtVar,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "Displays the variance on the logistics availability for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "availability_mission": [
                4,
                self.txtMissionAt,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the mission availability for the selected "
                        "hardware item."
                    ),
                    "width": 125,
                },
                _("Mission A(t):"),
                "gfloat",
            ],
            "avail_mis_variance": [
                6,
                self.txtMissionAtVar,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "Displays the variance on the mission availability for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                "",
                "gfloat",
            ],
            "total_cost": [
                31,
                self.txtTotalCost,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the total cost of the selected hardware item."
                    ),
                    "width": 125,
                },
                _("Total Cost:"),
                "gfloat",
            ],
            "cost_failure": [
                8,
                self.txtCostFailure,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the cost per failure of the selected hardware item."
                    ),
                    "width": 125,
                },
                _("Cost/Failure:"),
                "gfloat",
            ],
            "cost_hour": [
                9,
                self.txtCostHour,
                "",
                None,
                "",
                1.0,
                {
                    "tooltip": _(
                        "Displays the failure cost per life time hour for the "
                        "selected hardware item."
                    ),
                    "width": 125,
                },
                _("Cost/Hour:"),
                "gfloat",
            ],
            "total_part_count": [
                32,
                self.txtPartCount,
                "",
                None,
                "",
                0.0,
                {
                    "tooltip": _(
                        "Displays the total part count for the selected hardware item."
                    ),
                    "width": 125,
                },
                _("Total # of Parts:"),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        self.__do_nudge_widgets()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_load_entries_hardware,
            "succeed_get_hardware_attributes",
        )

    def _do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the RAMSTKEntry() widgets.

        This method ensures results RAMSTKEntry() widgets are set insensitive and
        loads the contents.  The PyPubSub subscriber is in the metaclass.

        :return: None
        :rtype: None
        """
        self.txtLogisticsAt.do_update(
            str(self.fmt.format(attributes["availability_logistics"] or 1.0)),
            signal="changed",
        )
        self.txtLogisticsAtVar.do_update(
            str(self.fmt.format(attributes["avail_log_variance"] or 0.0)),
            signal="changed",
        )
        self.txtMissionAt.do_update(
            str(self.fmt.format(attributes["availability_mission"] or 1.0)),
            signal="changed",
        )
        self.txtMissionAtVar.do_update(
            str(self.fmt.format(attributes["avail_mis_variance"] or 0.0)),
            signal="changed",
        )

    def _do_load_entries_hardware(self, attributes: Dict[str, Any]) -> None:
        """Load contents of the RAMSTKEntry() widgets.

        This method ensures results RAMSTKEntry() widgets are set insensitive and
        loads the contents.  The PyPubSub subscriber is in the metaclass.

        :return: None
        :rtype: None
        """
        self.txtTotalCost.do_update(
            str(locale.currency(attributes["total_cost"])),
            signal="changed",
        )
        self.txtCostFailure.do_update(
            str(locale.currency(attributes["cost_failure"])),
            signal="changed",
        )
        self.txtCostHour.do_update(
            str(locale.currency(attributes["cost_hour"])),
            signal="changed",
        )
        self.txtPartCount.do_update(
            str(f"{attributes['total_part_count']}"),
            signal="changed",
        )

    def __do_nudge_widgets(self) -> None:
        """Adjust widgets from their default positions.

        :return: None
        :rtype: None
        """
        _lst_labels: List[object] = []
        _x_pos: List[int] = [
            0,
            self.txtLogisticsAt.get_preferred_size()[0].width + 5,
        ]
        _y_pos: List[int] = []
        _n_rows: int = 0

        _fixed = self.get_children()[0].get_children()[0].get_children()[0]
        _widgets = (
            self.get_children()[0].get_children()[0].get_children()[0].get_children()
        )

        for _widget in _widgets[::2]:
            _y_pos.append(_fixed.child_get_property(_widget, "y"))
            if _widget.get_text() != "":
                _lst_labels.append(_widget)
                _x_pos[0] = max(_x_pos[0], _widget.get_preferred_size()[0].width)
                _n_rows += 1

        _x_pos[0] += 10
        _x_pos[1] = _x_pos[0] + _x_pos[1] + 5
        for _idx, _pos in enumerate(_y_pos[:_n_rows]):
            _fixed.move(_lst_labels[_idx], 5, _pos)

        _fixed.move(self.txtLogisticsAtVar, _x_pos[1], _y_pos[0])
        _fixed.move(self.txtMissionAt, _x_pos[0], _y_pos[1])
        _fixed.move(self.txtMissionAtVar, _x_pos[1], _y_pos[1])
        _fixed.move(self.txtTotalCost, _x_pos[0], _y_pos[2])
        _fixed.move(self.txtCostFailure, _x_pos[0], _y_pos[3])
        _fixed.move(self.txtCostHour, _x_pos[0], _y_pos[4])
        _fixed.move(self.txtPartCount, _x_pos[0], _y_pos[5])
