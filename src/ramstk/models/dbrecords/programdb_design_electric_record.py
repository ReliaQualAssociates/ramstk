# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_design_electric_record.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKDesignElectric Record Model."""

# Standard Library Imports
from typing import Dict, List, Tuple, Union

# Third Party Imports
from pubsub import pub
from sqlalchemy import Column, Float, ForeignKey, Integer, String

# RAMSTK Package Imports
from ramstk.analyses import derating, stress
from ramstk.views.gtk3 import _

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


def do_check_overstress(
    overstress: Dict[str, List[float]], stress_type: str, limits: Dict[str, List[float]]
) -> Tuple[int, str]:
    """Check the over stress condition and build a reason message.

    :param overstress: the dict containing the results of the
        over stress analysis.
    :param stress_type: the over stress type being checked.
    :return: (_overstress, _reason); whether a component is overstressed and the reason.
    :rtype: tuple
    """
    _overstress = 0
    _reason = ""

    if overstress["harsh"][0]:
        _overstress = 1
        _reason = _reason + (
            f"Operating {stress_type} ratio is less than the harsh environment limit "
            f"of {limits['harsh'][0]}.\n"
        )
    if overstress["harsh"][1]:
        _overstress = 1
        _reason = _reason + (
            f"Operating {stress_type} ratio is greater than the harsh environment "
            f"limit of {limits['harsh'][1]}.\n"
        )
    if overstress["mild"][0]:
        _overstress = 1
        _reason = _reason + (
            f"Operating {stress_type} ratio is less than the mild environment limit of "
            f"{limits['mild'][0]}.\n"
        )
    if overstress["mild"][1]:
        _overstress = 1
        _reason = _reason + (
            f"Operating {stress_type} ratio is greater than the mild environment limit "
            f"of {limits['mild'][1]}.\n"
        )

    return _overstress, _reason


# pylint: disable=R0902
class RAMSTKDesignElectricRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Represent ramstk_design_electric table in the RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        "application_id": 0,
        "area": 0.0,
        "capacitance": 0.0,
        "configuration_id": 0,
        "construction_id": 0,
        "contact_form_id": 0,
        "contact_gauge": 0,
        "contact_rating_id": 0,
        "current_operating": 0.0,
        "current_rated": 0.0,
        "current_ratio": 0.0,
        "environment_active_id": 0,
        "environment_dormant_id": 0,
        "family_id": 0,
        "feature_size": 0.0,
        "frequency_operating": 0.0,
        "insert_id": 0,
        "insulation_id": 0,
        "manufacturing_id": 0,
        "matching_id": 0,
        "n_active_pins": 0,
        "n_circuit_planes": 1,
        "n_cycles": 0,
        "n_elements": 0,
        "n_hand_soldered": 0,
        "n_wave_soldered": 0,
        "operating_life": 0.0,
        "overstress": 0,
        "package_id": 0,
        "power_operating": 0.0,
        "power_rated": 0.0,
        "power_ratio": 0.0,
        "reason": "",
        "resistance": 0.0,
        "specification_id": 0,
        "technology_id": 0,
        "temperature_active": 35.0,
        "temperature_case": 0.0,
        "temperature_dormant": 25.0,
        "temperature_hot_spot": 0.0,
        "temperature_junction": 0.0,
        "temperature_knee": 25.0,
        "temperature_rated_max": 0.0,
        "temperature_rated_min": 0.0,
        "temperature_rise": 0.0,
        "theta_jc": 0.0,
        "type_id": 0,
        "voltage_ac_operating": 0.0,
        "voltage_dc_operating": 0.0,
        "voltage_esd": 0.0,
        "voltage_rated": 0.0,
        "voltage_ratio": 0.0,
        "weight": 0.0,
        "years_in_production": 1,
    }
    __tablename__ = "ramstk_design_electric"
    __table_args__ = {"extend_existing": True}

    revision_id = Column(
        "fld_revision_id",
        Integer,
        ForeignKey("ramstk_revision.fld_revision_id", ondelete="CASCADE"),
        nullable=False,
    )
    hardware_id = Column(
        "fld_hardware_id",
        Integer,
        ForeignKey("ramstk_hardware.fld_hardware_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    application_id = Column(
        "fld_application_id", Integer, default=__defaults__["application_id"]
    )
    area = Column("fld_area", Float, default=__defaults__["area"])
    capacitance = Column("fld_capacitance", Float, default=__defaults__["capacitance"])
    configuration_id = Column(
        "fld_configuration_id",
        Integer,
        default=__defaults__["configuration_id"],
    )
    construction_id = Column(
        "fld_construction_id", Integer, default=__defaults__["construction_id"]
    )
    contact_form_id = Column(
        "fld_contact_form_id", Integer, default=__defaults__["contact_form_id"]
    )
    contact_gauge = Column(
        "fld_contact_gauge", Integer, default=__defaults__["contact_gauge"]
    )
    contact_rating_id = Column(
        "fld_contact_rating_id",
        Integer,
        default=__defaults__["contact_rating_id"],
    )
    current_operating = Column(
        "fld_current_operating",
        Float,
        default=__defaults__["current_operating"],
    )
    current_rated = Column(
        "fld_current_rated", Float, default=__defaults__["current_rated"]
    )
    current_ratio = Column(
        "fld_current_ratio", Float, default=__defaults__["current_ratio"]
    )
    environment_active_id = Column(
        "fld_environment_active_id",
        Integer,
        default=__defaults__["environment_active_id"],
    )
    environment_dormant_id = Column(
        "fld_environment_dormant_id",
        Integer,
        default=__defaults__["environment_dormant_id"],
    )
    family_id = Column("fld_family_id", Integer, default=__defaults__["family_id"])
    feature_size = Column(
        "fld_feature_size", Float, default=__defaults__["feature_size"]
    )
    frequency_operating = Column(
        "fld_frequency_operating",
        Float,
        default=__defaults__["frequency_operating"],
    )
    insert_id = Column("fld_insert_id", Integer, default=__defaults__["insert_id"])
    insulation_id = Column(
        "fld_insulation_id", Integer, default=__defaults__["insulation_id"]
    )
    manufacturing_id = Column(
        "fld_manufacturing_id",
        Integer,
        default=__defaults__["manufacturing_id"],
    )
    matching_id = Column(
        "fld_matching_id", Integer, default=__defaults__["matching_id"]
    )
    n_active_pins = Column(
        "fld_n_active_pins", Integer, default=__defaults__["n_active_pins"]
    )
    n_circuit_planes = Column(
        "fld_n_circuit_planes",
        Integer,
        default=__defaults__["n_circuit_planes"],
    )
    n_cycles = Column("fld_n_cycles", Integer, default=__defaults__["n_cycles"])
    n_elements = Column("fld_n_elements", Integer, default=__defaults__["n_elements"])
    n_hand_soldered = Column(
        "fld_n_hand_soldered", Integer, default=__defaults__["n_hand_soldered"]
    )
    n_wave_soldered = Column(
        "fld_n_wave_soldered", Integer, default=__defaults__["n_wave_soldered"]
    )
    operating_life = Column(
        "fld_operating_life", Float, default=__defaults__["operating_life"]
    )
    overstress = Column("fld_overstress", Integer, default=__defaults__["overstress"])
    package_id = Column("fld_package_id", Integer, default=__defaults__["package_id"])
    power_operating = Column(
        "fld_power_operating", Float, default=__defaults__["power_operating"]
    )
    power_rated = Column("fld_power_rated", Float, default=__defaults__["power_rated"])
    power_ratio = Column("fld_power_ratio", Float, default=__defaults__["power_ratio"])
    reason = Column("fld_reason", String, default=__defaults__["reason"])
    resistance = Column("fld_resistance", Float, default=__defaults__["resistance"])
    specification_id = Column(
        "fld_specification_id",
        Integer,
        default=__defaults__["specification_id"],
    )
    technology_id = Column(
        "fld_technology_id", Integer, default=__defaults__["technology_id"]
    )
    temperature_active = Column(
        "fld_temperature_active",
        Float,
        default=__defaults__["temperature_active"],
    )
    temperature_case = Column(
        "fld_temperature_case", Float, default=__defaults__["temperature_case"]
    )
    temperature_dormant = Column(
        "fld_temperature_dormant",
        Float,
        default=__defaults__["temperature_dormant"],
    )
    temperature_hot_spot = Column(
        "fld_temperature_hot_spot",
        Float,
        default=__defaults__["temperature_hot_spot"],
    )
    temperature_junction = Column(
        "fld_temperature_junction",
        Float,
        default=__defaults__["temperature_junction"],
    )
    temperature_knee = Column(
        "fld_temperature_knee", Float, default=__defaults__["temperature_knee"]
    )
    temperature_rated_max = Column(
        "fld_temperature_rated_max",
        Float,
        default=__defaults__["temperature_rated_max"],
    )
    temperature_rated_min = Column(
        "fld_temperature_rated_min",
        Float,
        default=__defaults__["temperature_rated_min"],
    )
    temperature_rise = Column(
        "fld_temperature_rise", Float, default=__defaults__["temperature_rise"]
    )
    theta_jc = Column("fld_theta_jc", Float, default=__defaults__["theta_jc"])
    type_id = Column("fld_type_id", Integer, default=__defaults__["type_id"])
    voltage_ac_operating = Column(
        "fld_voltage_ac_operating",
        Float,
        default=__defaults__["voltage_ac_operating"],
    )
    voltage_dc_operating = Column(
        "fld_voltage_dc_operating",
        Float,
        default=__defaults__["voltage_dc_operating"],
    )
    voltage_esd = Column("fld_voltage_esd", Float, default=__defaults__["voltage_esd"])
    voltage_rated = Column(
        "fld_voltage_rated", Float, default=__defaults__["voltage_rated"]
    )
    voltage_ratio = Column(
        "fld_voltage_ratio", Float, default=__defaults__["voltage_ratio"]
    )
    weight = Column("fld_weight", Float, default=__defaults__["weight"])
    years_in_production = Column(
        "fld_years_in_production",
        Integer,
        default=__defaults__["years_in_production"],
    )

    # Define the relationships to other tables in the RAMSTK Program database.

    def get_attributes(self) -> Dict[str, Union[float, int, str]]:
        """Retrieve current values of RAMSTKDesignElectric model attributes.

        :return: {hardware_id, application_id, area, capacitance,
                  configuration_id, construction_id, contact_form_id,
                  contact_gauge, contact_rating_id, current_operating,
                  current_rated, current_ratio, environment_active_id,
                  environment_dormant_id, family_id, feature_size,
                  frequency_operating, insert_id, insulation_id,
                  manufacturing_id, matching_id, n_active_pins,
                  n_circuit_planes, n_cycles, n_elements, n_hand_soldered,
                  n_wave_soldered, operating_life, overstress, package_id,
                  power_operating, power_rated, power_ratio, reason,
                  resistance, specification_id, technology_id,
                  temperature_active, temperature_case, temperature_dormant,
                  temperature_hot_spot, temperature_junction, temperature_knee,
                  temperature_rated_max, temperature_rated_min,
                  temperature_rise, theta_jc, type_id, voltage_ac_operating,
                  voltage_dc_operating, voltage_esd, voltage_rated,
                  voltage_ratio, weight, years_in_production} pairs.
        :rtype: dict
        """
        return {
            "hardware_id": self.hardware_id,
            "application_id": self.application_id,
            "area": self.area,
            "capacitance": self.capacitance,
            "configuration_id": self.configuration_id,
            "construction_id": self.construction_id,
            "contact_form_id": self.contact_form_id,
            "contact_gauge": self.contact_gauge,
            "contact_rating_id": self.contact_rating_id,
            "current_operating": self.current_operating,
            "current_rated": self.current_rated,
            "current_ratio": self.current_ratio,
            "environment_active_id": self.environment_active_id,
            "environment_dormant_id": self.environment_dormant_id,
            "family_id": self.family_id,
            "feature_size": self.feature_size,
            "frequency_operating": self.frequency_operating,
            "insert_id": self.insert_id,
            "insulation_id": self.insulation_id,
            "manufacturing_id": self.manufacturing_id,
            "matching_id": self.matching_id,
            "n_active_pins": self.n_active_pins,
            "n_circuit_planes": self.n_circuit_planes,
            "n_cycles": self.n_cycles,
            "n_elements": self.n_elements,
            "n_hand_soldered": self.n_hand_soldered,
            "n_wave_soldered": self.n_wave_soldered,
            "operating_life": self.operating_life,
            "overstress": self.overstress,
            "package_id": self.package_id,
            "power_operating": self.power_operating,
            "power_rated": self.power_rated,
            "power_ratio": self.power_ratio,
            "reason": self.reason,
            "resistance": self.resistance,
            "specification_id": self.specification_id,
            "technology_id": self.technology_id,
            "temperature_active": self.temperature_active,
            "temperature_case": self.temperature_case,
            "temperature_dormant": self.temperature_dormant,
            "temperature_hot_spot": self.temperature_hot_spot,
            "temperature_junction": self.temperature_junction,
            "temperature_knee": self.temperature_knee,
            "temperature_rated_max": self.temperature_rated_max,
            "temperature_rated_min": self.temperature_rated_min,
            "temperature_rise": self.temperature_rise,
            "theta_jc": self.theta_jc,
            "type_id": self.type_id,
            "voltage_ac_operating": self.voltage_ac_operating,
            "voltage_dc_operating": self.voltage_dc_operating,
            "voltage_esd": self.voltage_esd,
            "voltage_rated": self.voltage_rated,
            "voltage_ratio": self.voltage_ratio,
            "weight": self.weight,
            "years_in_production": self.years_in_production,
        }

    def do_calculate_current_ratio(self) -> None:
        """Calculate the current ratio.

        :return: None
        :rtype: None
        """
        try:
            self.current_ratio = stress.calculate_stress_ratio(
                self.current_operating,
                self.current_rated,
            )
        except ZeroDivisionError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"Failed to calculate current ratio for hardware ID "
                    f"{self.hardware_id}.  Rated current={self.current_rated}, "
                    f"operating current={self.current_operating}."
                ),
            )

    def do_calculate_power_ratio(self) -> None:
        """Calculate the power ratio.

        :return: None
        :rtype: None
        """
        try:
            self.power_ratio = stress.calculate_stress_ratio(
                self.power_operating,
                self.power_rated,
            )
        except ZeroDivisionError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"Failed to calculate power ratio for hardware ID "
                    f"{self.hardware_id}.  Rated power={self.power_rated}, operating "
                    f"power={self.power_operating}."
                ),
            )

    def do_calculate_voltage_ratio(self) -> None:
        """Calculate the voltage ratio.

        :return: None
        :rtype: None
        """
        _voltage_operating = self.voltage_ac_operating + self.voltage_dc_operating

        try:
            self.voltage_ratio = stress.calculate_stress_ratio(
                _voltage_operating, self.voltage_rated
            )
        except ZeroDivisionError:
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"Failed to calculate voltage ratio for hardware ID "
                    f"{self.hardware_id}.  Rated voltage={self.voltage_rated}, "
                    f"operating ac voltage={self.voltage_ac_operating}, operating DC "
                    f"voltage={self.voltage_dc_operating}."
                ),
            )

    def do_derating_analysis(self, stress_limits: List[float]) -> None:
        """Perform a derating analysis.

        :param stress_limits: the list of stress limits for the selected record.
        :return: None
        :rtype: None
        """
        _overstress = 0
        _reason = ""

        _current_limits = {
            "harsh": [0.0, stress_limits[0]],
            "mild": [0.0, stress_limits[1]],
        }
        _power_limits = {
            "harsh": [0.0, stress_limits[2]],
            "mild": [0.0, stress_limits[3]],
        }
        _voltage_limits = {
            "harsh": [0.0, stress_limits[4]],
            "mild": [0.0, stress_limits[5]],
        }

        _ostress, _rsn = do_check_overstress(
            derating.check_overstress(self.current_ratio, _current_limits),
            "current",
            _current_limits,
        )
        _overstress = _overstress or _ostress
        _reason += _rsn

        _ostress, _rsn = do_check_overstress(
            derating.check_overstress(self.power_ratio, _power_limits),
            "power",
            _power_limits,
        )
        _overstress = _overstress or _ostress
        _reason += _rsn

        _ostress, _rsn = do_check_overstress(
            derating.check_overstress(self.voltage_ratio, _voltage_limits),
            "voltage",
            _voltage_limits,
        )
        self.overstress = _overstress or _ostress
        self.reason = _reason + _rsn

    def do_stress_analysis(self, category_id: int) -> None:
        """Perform a stress analysis.

        :param category_id: the component category ID of the record to calculate.
        :return: None
        :rtype: None
        """
        if category_id in {1, 2, 5, 6, 7, 8}:
            self.do_calculate_current_ratio()

        if category_id == 3:
            self.do_calculate_power_ratio()

        if category_id in {4, 5, 8}:
            self.do_calculate_voltage_ratio()
