# Third Party Imports
import pytest


@pytest.fixture(scope="function")
def test_stress_limits():
    yield {
        "integrated_circuit": {
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
        "semiconductor": {
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
        "resistor": {
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
        "capacitor": {
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
            "mica": {"temperature": [25.0, 25.0, 25.0], "voltage": [0.7, 0.7, 0.7]},
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
        "inductor": {
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
        "relay": {
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
        "switch": {
            "capacitive_load": {
                "current": [0.7, 0.6, 0.5],
                "power": [0.7, 0.6, 0.5],
                "surge_current": [0.8, 0.8, 0.8],
            },
            "inductive_load": {
                "current": [0.5, 0.4, 0.3],
                "power": [0.7, 0.6, 0.5],
                "surge_current": [0.8, 0.8, 0.8],
            },
            "resistitive_load": {
                "current": [0.7, 0.6, 0.5],
                "power": [0.7, 0.6, 0.5],
                "surge_current": [0.8, 0.8, 0.8],
            },
        },
        "connection": {"current": [1.0, 1.0, 1.0]},
        "miscellaneous": {"lamp": {"current": [0.2, 0.1, 0.1]}},
    }
