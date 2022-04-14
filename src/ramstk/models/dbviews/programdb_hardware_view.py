# -*- coding: utf-8 -*-
#
#       ramstk.models.dbviews.programdb_hardware_view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware BoM View Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from pubsub import pub
from sqlalchemy.orm.exc import ObjectDeletedError
from treelib import Tree

# RAMSTK Local Imports
from .baseview import RAMSTKBaseView


class RAMSTKHardwareBoMView(RAMSTKBaseView):
    """Contain the attributes and methods of the Hardware BoM view model.

    This class manages the hardware BoM data from the RAMSTKHardware,
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKMilHdbkF, RAMSTKNSWC, and
    RAMSTKReliability table models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "hardware_bom"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a Hardware BoM view model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_load_functions = {
            "hardware": self._do_load_hardware,
            "design_electric": self._do_load_design_electric,
            "design_mechanic": self._do_load_design_mechanic,
            "milhdbk217f": self._do_load_milhdbk217f,
            "nswc": self._do_load_nswc,
            "reliability": self._do_load_reliability,
        }
        self._dic_stress_limits = kwargs.get(
            "stress_limits",
            dict(
                integrated_circuit={
                    "digital": {
                        "mos": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "fanout": [1.0, 0.9, 0.9],
                                "frequency": [0.9, 0.9, 0.9],
                                "temperature": [125.0, 110.0, 100.0],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "fanout": [1.0, 0.9, 0.0],
                                "frequency": [0.9, 0.8, 0.0],
                                "temperature": [90.0, 85.0, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "fanout": [0.8, 0.0, 0.0],
                                "frequency": [0.8, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                            },
                        },
                        "bipolar": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "fanout": [0.9, 0.85, 0.8],
                                "frequency": [1.0, 0.9, 0.85],
                                "temperature": [125.0, 110.0, 100.0],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "fanout": [0.9, 0.8, 0.0],
                                "frequency": [1.0, 0.9, 0.0],
                                "temperature": [90.0, 85.0, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "fanout": [0.7, 0.0, 0.0],
                                "frequency": [0.75, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                            },
                        },
                    },
                    "linear": {
                        "mos": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "fanout": [1.0, 0.9, 0.9],
                                "frequency": [0.9, 0.9, 0.9],
                                "temperature": [125.0, 110.0, 100.0],
                                "voltage": [0.8, 0.8, 0.7],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "fanout": [1.0, 0.9, 0.0],
                                "frequency": [0.9, 0.8, 0.0],
                                "temperature": [90.0, 85.0, 0.0],
                                "voltage": [0.8, 0.7, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "fanout": [0.8, 0.0, 0.0],
                                "frequency": [0.8, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                                "voltage": [0.6, 0.0, 0.0],
                            },
                        },
                        "bipolar": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "fanout": [0.9, 0.85, 0.8],
                                "frequency": [1.0, 0.9, 0.85],
                                "temperature": [125.0, 110.0, 100.0],
                                "voltage": [0.8, 0.8, 0.7],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "fanout": [0.9, 0.8, 0.0],
                                "frequency": [1.0, 0.9, 0.0],
                                "temperature": [90.0, 85.0, 0.0],
                                "voltage": [0.8, 0.7, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "fanout": [0.7, 0.0, 0.0],
                                "frequency": [0.75, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                                "voltage": [0.6, 0.0, 0.0],
                            },
                        },
                    },
                    "microprocessor": {
                        "mos": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "fanout": [1.0, 0.9, 0.9],
                                "frequency": [0.9, 0.9, 0.9],
                                "temperature": [125.0, 110.0, 100.0],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "fanout": [1.0, 0.85, 0.0],
                                "frequency": [0.9, 0.8, 0.0],
                                "temperature": [85.0, 75.0, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "fanout": [0.8, 0.0, 0.0],
                                "frequency": [0.8, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                            },
                        },
                        "bipolar": {
                            "hermetic": {
                                "current": [0.8, 0.75, 0.7],
                                "fanout": [0.8, 0.75, 0.7],
                                "frequency": [0.9, 0.8, 0.75],
                                "temperature": [125.0, 110.0, 100.0],
                            },
                            "plastic1": {
                                "current": [0.8, 0.75, 0.0],
                                "fanout": [0.8, 0.75, 0.0],
                                "frequency": [0.9, 0.8, 0.0],
                                "temperature": [85.0, 75.0, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "fanout": [0.7, 0.0, 0.0],
                                "frequency": [0.75, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                            },
                        },
                    },
                    "memory": {
                        "mos": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "frequency": [1.0, 0.9, 0.9],
                                "temperature": [125.0, 110.0, 100.0],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "frequency": [1.0, 0.9, 0.0],
                                "temperature": [90.0, 85.0, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "frequency": [0.8, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                            },
                        },
                        "bipolar": {
                            "hermetic": {
                                "current": [0.9, 0.85, 0.8],
                                "frequency": [1.0, 1.0, 0.9],
                                "temperature": [125.0, 110.0, 100.0],
                            },
                            "plastic1": {
                                "current": [0.9, 0.8, 0.0],
                                "frequency": [1.0, 0.95, 0.0],
                                "temperature": [90.0, 85.0, 0.0],
                            },
                            "plastic2": {
                                "current": [0.7, 0.0, 0.0],
                                "frequency": [0.8, 0.0, 0.0],
                                "temperature": [70.0, 0.0, 0.0],
                            },
                        },
                    },
                },
                semiconductor={
                    "diode": {
                        "general_purpose": {
                            "jantx": {
                                "current": [1.0, 1.0, 1.0],
                                "surge_current": [1.0, 0.9, 0.8],
                                "voltage": [0.95, 0.9, 0.85],
                                "temperature": [150.0, 125.0, 125.0],
                            },
                            "military": {
                                "current": [0.9, 0.9, 0.7],
                                "surge_current": [0.8, 0.8, 0.5],
                                "voltage": [0.8, 0.75, 0.5],
                                "temperature": [100.0, 85.0, 70.0],
                            },
                            "commercial": {
                                "current": [0.75, 0.7, 0.0],
                                "surge_current": [0.6, 0.3, 0.0],
                                "voltage": [0.7, 0.6, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                            },
                        },
                        "power_rectifier": {
                            "jantx": {
                                "current": [1.0, 1.0, 1.0],
                                "voltage": [0.95, 0.9, 0.85],
                                "temperature": [150.0, 125.0, 125.0],
                            },
                            "military": {
                                "current": [0.9, 0.85, 0.6],
                                "voltage": [0.8, 0.75, 0.3],
                                "temperature": [100.0, 85.0, 70.0],
                            },
                            "commercial": {
                                "current": [0.6, 0.5, 0.0],
                                "voltage": [0.5, 0.3, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                            },
                        },
                        "schottky": {
                            "jantx": {
                                "power": [1.0, 1.0, 0.9],
                                "voltage": [0.95, 0.9, 0.85],
                                "temperature": [150.0, 125.0, 125.0],
                            },
                            "military": {
                                "power": [0.9, 0.9, 0.5],
                                "voltage": [0.8, 0.8, 0.25],
                                "temperature": [100.0, 85.0, 70.0],
                            },
                            "commercial": {
                                "power": [0.75, 0.75, 0.0],
                                "voltage": [0.5, 0.3, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                            },
                        },
                        "regulator": {
                            "jantx": {
                                "power": [1.0, 1.0, 0.9],
                                "temperature": [150.0, 125.0, 125.0],
                            },
                            "military": {
                                "power": [0.9, 0.8, 0.5],
                                "temperature": [100.0, 85.0, 70.0],
                            },
                            "commercial": {
                                "power": [0.5, 0.5, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                            },
                        },
                        "suppressor": {
                            "jantx": {
                                "current": [1.0, 1.0, 0.9],
                                "power": [1.0, 1.0, 0.9],
                                "temperature": [150.0, 125.0, 125.0],
                            },
                            "military": {
                                "current": [0.8, 0.8, 0.5],
                                "power": [0.8, 0.8, 0.5],
                                "temperature": [100.0, 85.0, 70.0],
                            },
                            "commercial": {
                                "current": [0.75, 0.5, 0.0],
                                "power": [0.75, 0.5, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                            },
                        },
                    },
                    "thyristor": {
                        "jantx": {
                            "current": [1.0, 1.0, 0.9],
                            "temperature": [150.0, 125.0, 125.0],
                            "voltage": [1.0, 1.0, 0.9],
                        },
                        "military": {
                            "current": [0.9, 0.8, 0.5],
                            "temperature": [100.0, 85.0, 70.0],
                            "voltage": [0.9, 0.8, 0.5],
                        },
                        "commercial": {
                            "current": [0.6, 0.5, 0.0],
                            "temperature": [70.0, 35.0, 0.0],
                            "voltage": [0.6, 0.5, 0.0],
                        },
                    },
                    "transistor": {
                        "bjt": {
                            "jantx": {
                                "current": [1.0, 0.9, 0.9],
                                "power": [1.0, 1.0, 0.9],
                                "temperature": [150.0, 125.0, 125.0],
                                "voltage": [1.0, 0.9, 0.8],
                            },
                            "military": {
                                "current": [0.9, 0.8, 0.6],
                                "power": [0.9, 0.8, 0.6],
                                "temperature": [100.0, 85.0, 70.0],
                                "voltage": [0.8, 0.75, 0.3],
                            },
                            "commercial": {
                                "current": [0.5, 0.5, 0.0],
                                "power": [0.5, 0.5, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                                "voltage": [0.25, 0.25, 0.0],
                            },
                        },
                        "fet": {
                            "jantx": {
                                "power": [1.0, 1.0, 0.9],
                                "temperature": [150.0, 125.0, 125.0],
                                "voltage": [1.0, 0.95, 0.9],
                            },
                            "military": {
                                "power": [0.9, 0.8, 0.5],
                                "temperature": [100.0, 85.0, 70.0],
                                "voltage": [0.8, 0.75, 0.5],
                            },
                            "commercial": {
                                "power": [0.5, 0.5, 0.0],
                                "temperature": [70.0, 35.0, 0.0],
                                "voltage": [0.25, 0.25, 0.0],
                            },
                        },
                    },
                },
                resistor={
                    "fixed_chip": {
                        "low_power": {
                            "power": [0.7, 0.7, 0.7],
                            "temperature": [0.7, 0.7, 0.7],
                        },
                        "high_power": {
                            "power": [0.55, 0.55, 0.55],
                            "temperature": [0.55, 0.55, 0.55],
                        },
                    },
                    "fixed_film": {
                        "low_power": {
                            "power": [0.65, 0.65, 0.65],
                            "temperature": [0.65, 0.65, 0.65],
                            "voltage": [0.7, 0.7, 0.7],
                        },
                        "high_power": {
                            "power": [0.55, 0.55, 0.55],
                            "temperature": [0.55, 0.55, 0.55],
                            "voltage": [0.7, 0.7, 0.7],
                        },
                    },
                    "fixed_film_power": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                    },
                    "fixed_film_network": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "fixed_wirewound": {
                        "low_power": {
                            "power": [0.7, 0.7, 0.7],
                            "temperature": [1.0, 1.0, 1.0],
                            "voltage": [0.7, 0.7, 0.7],
                        },
                        "high_power": {
                            "power": [0.5, 0.5, 0.5],
                            "temperature": [1.0, 1.0, 1.0],
                            "voltage": [0.7, 0.7, 0.7],
                        },
                    },
                    "fixed_wirewound_power": {
                        "power": [0.6, 0.6, 0.6],
                        "temperature": [0.6, 0.6, 0.6],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "fixed_wirewound_chassis": {
                        "power": [0.5, 0.5, 0.5],
                        "temperature": [0.5, 0.5, 0.5],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "variable_wirewound": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                    },
                    "variable_wirewound_precision": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                    },
                    "variable_wirewound_power": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [110.0, 110.0, 110.0],
                    },
                    "variable_composition": {
                        "power": [0.5, 0.5, 0.5],
                        "temperature": [0.5, 0.5, 0.5],
                    },
                    "variable_film": {
                        "power": [0.5, 0.5, 0.5],
                        "temperature": [0.5, 0.5, 0.5],
                    },
                    "variable_non_wirewound": {
                        "power": [0.55, 0.55, 0.55],
                        "temperature": [0.55, 0.55, 0.55],
                    },
                },
                capacitor={
                    "paper": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.55, 0.55, 0.55],
                    },
                    "plastic": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.55, 0.55, 0.55],
                    },
                    "metallized": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.55, 0.55, 0.55],
                    },
                    "mica": {
                        "temperature": [25.0, 25.0, 25.0],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "mica_button": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.55, 0.55, 0.55],
                    },
                    "glass": {
                        "temperature": [15.0, 15.0, 15.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "ceramic_fixed": {
                        "temperature": [15.0, 15.0, 15.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "temp_comp_ceramic": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "ceramic_chip": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "tantalum_chip": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "tantalum_solid": {
                        "reverse_voltage": [0.02, 0.02, 0.02],
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "tantalum_wet": {
                        "reverse_voltage": [0.02, 0.02, 0.02],
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "aluminum": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "aluminum_dry": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.7, 0.7, 0.7],
                    },
                    "ceramic_variable": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "piston": {
                        "temperature": [15.0, 15.0, 15.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "trimmer": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                    "vacuum": {
                        "temperature": [10.0, 10.0, 10.0],
                        "voltage": [0.6, 0.6, 0.6],
                    },
                },
                inductor={
                    "low_frequency": {
                        "current": [0.7, 0.7, 0.6],
                        "surge_current": [0.9, 0.9, 0.8],
                        "surge_voltage": [0.9, 0.9, 0.8],
                        "temperature": [30.0, 30.0, 30.0],
                        "voltage": [0.7, 0.7, 0.6],
                    },
                    "high_frequency": {
                        "current": [0.9, 0.9, 0.8],
                        "temperature": [30.0, 30.0, 30.0],
                    },
                },
                relay={
                    "capacitive_load": {
                        "current": [0.7, 0.6, 0.5],
                        "drop_out": [0.9, 0.9, 0.9],
                        "pick_up": [1.1, 1.1, 1.1],
                        "temperature": [10.0, 20.0, 30.0],
                    },
                    "inductive_load": {
                        "current": [0.5, 0.4, 0.3],
                        "drop_out": [0.9, 0.9, 0.9],
                        "pick_up": [1.1, 1.1, 1.1],
                        "temperature": [10.0, 20.0, 30.0],
                    },
                    "resistive_load": {
                        "current": [0.7, 0.6, 0.5],
                        "drop_out": [0.9, 0.9, 0.9],
                        "pick_up": [1.1, 1.1, 1.1],
                        "temperature": [10.0, 20.0, 30.0],
                    },
                },
                switch={
                    "lamp_load": {
                        "current": [0.2, 0.1, 0.1],
                        "power": [0.7, 0.6, 0.5],
                        "surge_current": [0.8, 0.8, 0.8],
                    },
                    "inductive_load": {
                        "current": [0.5, 0.4, 0.3],
                        "power": [0.7, 0.6, 0.5],
                        "surge_current": [0.8, 0.8, 0.8],
                    },
                    "resistive_load": {
                        "current": [0.7, 0.6, 0.5],
                        "power": [0.7, 0.6, 0.5],
                        "surge_current": [0.8, 0.8, 0.8],
                    },
                },
                connection={"current": [1.0, 1.0, 1.0]},
                miscellaneous={"lamp": {"current": [0.2, 0.1, 0.1]}},
            ),
        )
        self._dic_trees = {
            "hardware": Tree(),
            "design_electric": Tree(),
            "design_mechanic": Tree(),
            "milhdbk217f": Tree(),
            "nswc": Tree(),
            "reliability": Tree(),
        }

        # Initialize private list attributes.
        self._lst_modules = [
            "hardware",
            "design_electric",
            "design_mechanic",
            "milhdbk217f",
            "nswc",
            "reliability",
        ]

        # Initialize private scalar attributes.
        self._hr_multiplier: float = kwargs.get("hr_multiplier", 1.0)  # type: ignore

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_tree, "succeed_insert_hardware")
        pub.subscribe(super().do_set_tree, "succeed_insert_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_insert_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_insert_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_insert_nswc")
        pub.subscribe(super().do_set_tree, "succeed_insert_reliability")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_hardware")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_nswc")
        pub.subscribe(super().do_set_tree, "succeed_retrieve_all_reliability")
        pub.subscribe(super().do_set_tree, "succeed_delete_hardware")
        pub.subscribe(super().do_set_tree, "succeed_delete_design_electric")
        pub.subscribe(super().do_set_tree, "succeed_delete_design_mechanic")
        pub.subscribe(super().do_set_tree, "succeed_delete_milhdbk217f")
        pub.subscribe(super().do_set_tree, "succeed_delete_nswc")
        pub.subscribe(super().do_set_tree, "succeed_delete_reliability")
        pub.subscribe(self.do_calculate_hardware, "request_calculate_hardware")
        pub.subscribe(self.do_make_composite_ref_des, "request_make_comp_ref_des")

    def do_calculate_assembly_hazard_rates(self, node_id: int) -> None:
        """Calculate the hazard rates for assemblies.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)

        # There are no children for this node, or it is using one of the specified
        # hazard rate methods.  The specified methods will ignore the hazard rates of
        # any children.
        if _record.is_leaf() or _record.data["reliability"].hazard_rate_type_id != 1:
            _attributes = {
                **_record.data["hardware"].get_attributes(),
                **_record.data["reliability"].get_attributes(),
            }

            _record.data["reliability"].do_calculate_hazard_rate_active(
                self._hr_multiplier,
                _attributes,
                time=_record.data["hardware"].mission_time,
            )
        else:
            _hazard_rate_active: float = 0.0
            _hazard_rate_dormant: float = 0.0

            for _node in self.tree.children(node_id):
                self.do_calculate_hazard_rates(_node.identifier)
                _hazard_rate_active += _node.data["reliability"].hazard_rate_active
                _hazard_rate_dormant += _node.data["reliability"].hazard_rate_dormant

            _hazard_rate_active = (
                (_hazard_rate_active + _record.data["reliability"].add_adj_factor)
                * _record.data["reliability"].mult_adj_factor
                * (_record.data["hardware"].duty_cycle / 100.0)
                * _record.data["hardware"].quantity
            )

            _record.data["reliability"].hazard_rate_active = _hazard_rate_active
            _record.data["reliability"].hazard_rate_dormant = _hazard_rate_dormant

    def do_calculate_cost(self, node_id: int) -> None:
        """Calculate the cost related metrics.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data["hardware"]
        _total_cost: float = 0.0

        if _record.part == 1:
            _record.do_calculate_total_cost()
        else:
            for _node in self.tree.children(node_id):
                self.do_calculate_cost(_node.identifier)
                _total_cost += _node.data["hardware"].total_cost

            _total_cost *= _record.quantity
            _record.set_attributes({"cost": _total_cost})
            _record.set_attributes({"total_cost": _total_cost})

    def do_calculate_hardware(self, node_id: int) -> None:
        """Calculate all metrics for the hardware associated with node ID.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        self.do_calculate_cost(node_id)
        self.do_calculate_part_count(node_id)
        self.do_calculate_power_dissipation(node_id)
        self.do_calculate_hazard_rates(node_id)

        for _table in ["design_electric", "milhdbk217f", "reliability"]:
            pub.sendMessage(
                f"request_get_{_table}_attributes",
                node_id=node_id,
            )

    def do_calculate_hazard_rates(self, node_id: int) -> None:
        """Calculate the hazard rate of a hardware item.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)

        if _record.data["hardware"].part == 1:
            self.do_calculate_part_hazard_rates(node_id)
        else:
            self.do_calculate_assembly_hazard_rates(node_id)

        _record.data["reliability"].do_calculate_hazard_rate_logistics()
        _record.data["reliability"].do_calculate_hazard_rate_mission(
            _record.data["hardware"].duty_cycle
        )
        _record.data["reliability"].do_calculate_mtbf(
            multiplier=self._hr_multiplier,
        )
        _record.data["reliability"].do_calculate_reliability(
            _record.data["hardware"].mission_time,
            multiplier=self._hr_multiplier,
        )

    def do_calculate_part_count(self, node_id: int) -> None:
        """Calculate the total part count of a hardware item.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data["hardware"]
        _total_part_count: int = 0

        if _record.part == 1:
            _record.total_part_count = _record.quantity
        else:
            for _node in self.tree.children(node_id):
                self.do_calculate_part_count(_node.identifier)
                _total_part_count += _node.data["hardware"].total_part_count

            _total_part_count *= _record.quantity
            _record.set_attributes({"total_part_count": _total_part_count})

    def do_calculate_part_hazard_rates(self, node_id: int) -> None:
        """Calculate the hazard rates for parts.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)
        _attributes = {
            **_record.data["hardware"].get_attributes(),
            **_record.data["design_mechanic"].get_attributes(),
            **_record.data["design_electric"].get_attributes(),
            **_record.data["milhdbk217f"].get_attributes(),
            **_record.data["nswc"].get_attributes(),
            **_record.data["reliability"].get_attributes(),
        }

        self.do_calculate_part_stress(node_id)

        _record.data["reliability"].do_calculate_hazard_rate_active(
            self._hr_multiplier,
            _attributes,
            time=_record.data["hardware"].mission_time,
        )

        _record.data["reliability"].do_calculate_hazard_rate_dormant(
            _record.data["hardware"].category_id,
            _record.data["hardware"].subcategory_id,
            _record.data["design_electric"].environment_active_id,
            _record.data["design_electric"].environment_dormant_id,
        )

    def do_calculate_part_stress(self, node_id: int) -> None:
        """Calculate the electrical, mechanical, and thermal stress ratios on a part.

        :param node_id: the record ID to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id)

        if _record.data["hardware"].category_id != 9:
            _record.data["design_electric"].do_stress_analysis(
                _record.data["hardware"].category_id
            )

            _record.data["design_electric"].do_derating_analysis(
                _record.data["hardware"].category_id,
                _record.data["hardware"].subcategory_id,
                _record.data["reliability"].quality_id,
                self._dic_stress_limits,
            )

    def do_calculate_power_dissipation(self, node_id: int) -> float:
        """Calculate the total power dissipation of a hardware item.

        :param node_id: the record ID to calculate.
        :return: _total_power_dissipation; the total power dissipation.
        :rtype: float
        """
        _record = self.tree.get_node(node_id)
        _total_power_dissipation: float = 0.0

        if _record.data["hardware"].part == 1:
            _total_power_dissipation = (
                _record.data["design_electric"].power_operating
                * _record.data["hardware"].quantity
            )
        else:
            for _node_id in _record.successors(self.tree.identifier):
                _total_power_dissipation += self.do_calculate_power_dissipation(
                    _node_id
                )

            _total_power_dissipation *= _record.data["hardware"].quantity

        _record.data["hardware"].set_attributes(
            {"total_power_dissipation": _total_power_dissipation}
        )

        return _total_power_dissipation

    def do_make_composite_ref_des(self, node_id: int = 1) -> None:
        """Make the composite reference designators.

        :param node_id: the record ID to start making the composite reference
            designators.
        :return: None
        :rtype: None
        """
        # Retrieve the parent hardware item's composite reference designator.
        _node = self.tree.get_node(node_id)
        _record = _node.data["hardware"]

        if self.tree.parent(node_id).identifier != 0:
            _p_comp_ref_des = self.tree.parent(node_id).data["hardware"].comp_ref_des
        else:
            _p_comp_ref_des = ""

        if _p_comp_ref_des != "":
            _record.comp_ref_des = f"{_p_comp_ref_des}:{_record.ref_des}"
            _node.tag = f"{_p_comp_ref_des}:{_record.ref_des}"
        else:
            _record.comp_ref_des = _record.ref_des
            _node.tag = _record.ref_des

        # Now make the composite reference designator for all the child nodes.
        for _child_node in self.tree.children(node_id):
            self.do_make_composite_ref_des(node_id=_child_node.identifier)

        _record.set_attributes({"comp_ref_des": _record.comp_ref_des})

        pub.sendMessage(
            "succeed_make_comp_ref_des",
            comp_ref_des=_record.comp_ref_des,
        )

    def _do_load_hardware(self) -> None:
        """Load the hardware data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["hardware"].all_nodes()[1:]:
            _hardware = _node.data["hardware"]

            self.tree.create_node(
                tag="hardware",
                identifier=_hardware.hardware_id,
                parent=_hardware.parent_id,
                data={"hardware": _hardware},
            )

        self._dic_load_functions["design_electric"]()
        self._dic_load_functions["design_mechanic"]()
        self._dic_load_functions["milhdbk217f"]()
        self._dic_load_functions["nswc"]()
        self._dic_load_functions["reliability"]()

    def _do_load_design_electric(self) -> None:
        """Load the design electric data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["design_electric"].all_nodes()[1:]:
            _design_electric = _node.data["design_electric"]

            try:
                _par_node = self.tree.get_node(_design_electric.hardware_id)
                _par_node.data["design_electric"] = _design_electric
            except ObjectDeletedError:
                self._dic_trees["design_electric"].remove_node(_node.identifier)

    def _do_load_design_mechanic(self) -> None:
        """Load the design_mechanic into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["design_mechanic"].all_nodes()[1:]:
            _design_mechanic = _node.data["design_mechanic"]

            try:
                _par_node = self.tree.get_node(_design_mechanic.hardware_id)
                _par_node.data["design_mechanic"] = _design_mechanic
            except ObjectDeletedError:
                self._dic_trees["design_mechanic"].remove_node(_node.identifier)

    def _do_load_milhdbk217f(self) -> None:
        """Load the MIL-HDBK-217F data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["milhdbk217f"].all_nodes()[1:]:
            _milhdbk217f = _node.data["milhdbk217f"]

            try:
                _par_node = self.tree.get_node(_milhdbk217f.hardware_id)
                _par_node.data["milhdbk217f"] = _milhdbk217f
            except ObjectDeletedError:
                self._dic_trees["milhdbk217f"].remove_node(_node.identifier)

    def _do_load_nswc(self) -> None:
        """Load the NSWC data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["nswc"].all_nodes()[1:]:
            _nswc = _node.data["nswc"]

            try:
                _par_node = self.tree.get_node(_nswc.hardware_id)
                _par_node.data["nswc"] = _nswc
            except ObjectDeletedError:
                self._dic_trees["nswc"].remove_node(_node.identifier)

    def _do_load_reliability(self) -> None:
        """Load the reliability data into the tree.

        :return: None
        :rtype: None
        """
        for _node in self._dic_trees["reliability"].all_nodes()[1:]:
            _reliability = _node.data["reliability"]

            try:
                _par_node = self.tree.get_node(_reliability.hardware_id)
                _par_node.data["reliability"] = _reliability
            except ObjectDeletedError:
                self._dic_trees["reliability"].remove_node(_node.identifier)
