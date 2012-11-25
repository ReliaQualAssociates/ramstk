#!/usr/bin/env python
""" This is the transformer class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       transformer.py is part of The RelKit Project
#
# All rights reserved.

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from inductor import Inductor


class Audio(Inductor):
    """
    Audio Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the Audio Transformer Component Class. """

        Inductor.__init__(self)

        self.subcategory = 60                   # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22, 0.035, 0.11, 0.31, 4.7]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Audio Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)         # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Audio Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

        # Retrieve hot spot temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        A = partmodel.get_value(partrow, 44)
        Wt = partmodel.get_value(partrow, 45)
        P = partmodel.get_value(partrow, 64)
        Pin = partmodel.get_value(partrow, 93)

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # Calculate hot spot temperature.
        if(P > 0.0 and A > 0.0):
            Trise = 125 * P / A
        elif(P > 0.0 and Wt > 0.0):
            Trise = 11.5 * P / (Wt**0.6766)
        elif(Pin > 0.0 and Wt > 0.0):
            Trise = 2.1 * Pin / (Wt**0.6766)
        else:
            Trise = 35.0

        Ths = Tamb + 1.1 * Trise

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 38)
        if(idx == 1):                       # 85C
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6
        elif(idx == 2):                     # 105C
            Tref = 352.0
            K1 = 0.002
            K2 = 14.0
        elif(idx == 3):                     # 130C
            Tref = 364.0
            K1 = 0.0018
            K2 = 8.7
        elif(idx == 4):                     # 155C
            Tref = 400.0
            K1 = 0.002
            K2 = 10.0
        elif(idx == 5):                     # 170C
            Tref = 398.0
            K1 = 0.00125
            K2 = 3.8
        elif(idx == 6):                     # >170C
            Tref = 477.0
            K1 = 0.00159
            K2 = 8.4
        else:                               # Default
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6

        _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Ths)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 107, Trise)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class Power(Inductor):
    """
    High Power Pulse and Power Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the High Power Pulse and Power Transformer Component
            Class.
        """

        Inductor.__init__(self)

        self.subcategory = 60               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011, 0.37, 1.2, 16.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        High Power Pulse and Power Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the High Power Pulse and Power Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

        # Retrieve hot spot temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        A = partmodel.get_value(partrow, 44)
        Wt = partmodel.get_value(partrow, 45)
        P = partmodel.get_value(partrow, 64)
        Pin = partmodel.get_value(partrow, 93)

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # Calculate hot spot temperature.
        if(P > 0.0 and A > 0.0):
            Trise = 125 * P / A
        elif(P > 0.0 and Wt > 0.0):
            Trise = 11.5 * P / (Wt**0.6766)
        elif(Pin > 0.0 and Wt > 0.0):
            Trise = 2.1 * Pin / (Wt**0.6766)
        else:
            Trise = 35.0

        Ths = Tamb + 1.1 * Trise

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 38)
        if(idx == 1):                       # 85C
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6
        elif(idx == 2):                     # 105C
            Tref = 352.0
            K1 = 0.002
            K2 = 14.0
        elif(idx == 3):                     # 130C
            Tref = 364.0
            K1 = 0.0018
            K2 = 8.7
        elif(idx == 4):                     # 155C
            Tref = 400.0
            K1 = 0.002
            K2 = 10.0
        elif(idx == 5):                     # 170C
            Tref = 398.0
            K1 = 0.00125
            K2 = 3.8
        elif(idx == 6):                     # >170C
            Tref = 477.0
            K1 = 0.00159
            K2 = 8.4
        else:                               # Default
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6

        _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Ths)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 107, Trise)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class LowPowerPulse(Inductor):
    """
    Low Power Pulse Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the Low Power Pulse Transformer Component Class. """

        Inductor.__init__(self)

        self.subcategory = 60               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052, 0.11, 0.0018, 0.053, 0.16, 2.3]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Low Power Pulse Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)              # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Low Power Pulse Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

        # Retrieve hot spot temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        A = partmodel.get_value(partrow, 44)
        Wt = partmodel.get_value(partrow, 45)
        P = partmodel.get_value(partrow, 64)
        Pin = partmodel.get_value(partrow, 93)

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # Calculate hot spot temperature.
        if(P > 0.0 and A > 0.0):
            Trise = 125 * P / A
        elif(P > 0.0 and Wt > 0.0):
            Trise = 11.5 * P / (Wt**0.6766)
        elif(Pin > 0.0 and Wt > 0.0):
            Trise = 2.1 * Pin / (Wt**0.6766)
        else:
            Trise = 35.0

        Ths = Tamb + 1.1 * Trise

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 38)
        if(idx == 1):                       # 85C
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6
        elif(idx == 2):                     # 105C
            Tref = 352.0
            K1 = 0.002
            K2 = 14.0
        elif(idx == 3):                     # 130C
            Tref = 364.0
            K1 = 0.0018
            K2 = 8.7
        elif(idx == 4):                     # 155C
            Tref = 400.0
            K1 = 0.002
            K2 = 10.0
        elif(idx == 5):                     # 170C
            Tref = 398.0
            K1 = 0.00125
            K2 = 3.8
        elif(idx == 6):                     # >170C
            Tref = 477.0
            K1 = 0.00159
            K2 = 8.4
        else:                               # Default
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6

        _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Ths)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 107, Trise)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class RF(Inductor):
    """
    Radio Frequency Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the Radio Frequency Transformer Component Class. """

        Inductor.__init__(self)

        self.subcategory = 60               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015, 0.42, 1.2, 19.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Radio Frequency Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = part._calc_data[79]
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Radio Frequency Transformer Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

        # Retrieve hot spot temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        A = partmodel.get_value(partrow, 44)
        Wt = partmodel.get_value(partrow, 45)
        P = partmodel.get_value(partrow, 64)
        Pin = partmodel.get_value(partrow, 93)

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # Calculate hot spot temperature.
        if(P > 0.0 and A > 0.0):
            Trise = 125 * P / A
        elif(P > 0.0 and Wt > 0.0):
            Trise = 11.5 * P / (Wt**0.6766)
        elif(Pin > 0.0 and Wt > 0.0):
            Trise = 2.1 * Pin / (Wt**0.6766)
        else:
            Trise = 35.0

        Ths = Tamb + 1.1 * Trise

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 38)
        if(idx == 1):                       # 85C
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6
        elif(idx == 2):                     # 105C
            Tref = 352.0
            K1 = 0.002
            K2 = 14.0
        elif(idx == 3):                     # 130C
            Tref = 364.0
            K1 = 0.0018
            K2 = 8.7
        elif(idx == 4):                     # 155C
            Tref = 400.0
            K1 = 0.002
            K2 = 10.0
        elif(idx == 5):                     # 170C
            Tref = 398.0
            K1 = 0.00125
            K2 = 3.8
        elif(idx == 6):                     # >170C
            Tref = 477.0
            K1 = 0.00159
            K2 = 8.4
        else:                               # Default
            Tref = 329.0
            K1 = 0.0018
            K2 = 15.6

        _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Ths)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 107, Trise)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
