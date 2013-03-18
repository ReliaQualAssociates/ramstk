#!/usr/bin/env python
""" These are the fixed resistor component classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       fixed.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from resistor import Resistor


class Composition(Resistor):
    """
    Fixed Value Carbon Composition Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.1
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-11", "Lower"]
    _range = ["", "<0.1M", "0.1M to 1.0M", "1.0M to 10.0M", "<10.0M"]

    def __init__(self):
        """
        Initializes the Fixed Value Carbon Composition Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 25               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piR = [1.0, 1.1, 1.6, 2.5]
        self._piE = [1.0, 3.0, 8.0, 5.0, 13.0, 4.0, 5.0, 7.0, 11.0, 19.0, 0.5,
                     11.0, 27.0, 490.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._lambdab_count = [0.0005, 0.0022, 0.0071, 0.0037, 0.012, 0.0052, 0.0065, 0.016, 0.025, 0.025, 0.00025, 0.0098, 0.035, 0.36]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Carbon Composition Resistor Component Class.

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
        the Fixed Value Carbon Composition Resistor Component Class.

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
        _hrmodel['equation'] = "lambdab * piR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piR'] = partmodel.get_value(partrow, 80)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        S = P / Prated
        _hrmodel['lambdab'] = 0.0000000045 * exp(12.0 * ((Tamb + 273.0) / 343.0)) * exp((S / 0.6) * ((Tamb + 273.0) / 273.0))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Film(Resistor):
    """
    Fixed Value Film Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.2
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-10509", "MIL-R-22684", "Lower"]
    _range = ["", "<0.1M", "0.1M to 1.0M", "1.0M to 10.0M", "<10.0M"]
    _spec = ["", "MIL-R-39017 (RLR)", "MIL-R-22684 (RL)",
             "MIL-R-55182 (RNR, RNC, RNN)", "MIL-R-10509 (RN)"]

    def __init__(self):
        """ Initializes the Fixed Value Film Resistor Component Class. """

        Resistor.__init__(self)

        self.subcategory = 26               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 8.0, 4.0, 14.0, 4.0, 8.0, 10.0, 18.0, 19.0, 0.2,
                     10.0, 28.0, 510.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 5.0, 15.0]
        self._piR = [1.0, 1.1, 1.6, 2.5]
        self._lambdab_count = [[0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018, 0.033, 0.030, 0.00025, 0.014, 0.044, 0.69],
                               [0.0012, 0.0027, 0.011, 0.0054, 0.020, 0.0063, 0.013, 0.018, 0.033, 0.030, 0.00025, 0.014, 0.044, 0.69],
                               [0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021, 0.038, 0.034, 0.00028, 0.016, 0.050, 0.78],
                               [0.0014, 0.0031, 0.013, 0.0061, 0.023, 0.0072, 0.014, 0.021, 0.038, 0.034, 0.00028, 0.016, 0.050, 0.78]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Specification/Type:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Film Resistor
        Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        part.cmbSpecification = _widg.make_combo(simple=True)
        for i in range(len(self._spec)):
            part.cmbSpecification.insert_text(i, self._spec[i])
        part.cmbSpecification.connect("changed",
                                      self.combo_callback,
                                      part, 101)
        layout.put(part.cmbSpecification, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_inputs_load(self, part)

        part.cmbSpecification.set_active(int(part.model.get_value(part.selected_row, 101)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Film Resistor Component Class.

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
        Sidx = partmodel.get_value(partrow, 101)        # Specification index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Sidx - 1][Eidx - 1]

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
        the Fixed Value Film Resistor Component Class.

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
        _hrmodel['equation'] = "lambdab * piR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piR'] = partmodel.get_value(partrow, 80)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        S = P / Prated

        idx = partmodel.get_value(partrow, 101)
        if(idx == 1 or idx == 2):
            _hrmodel['lambdab'] = 0.000325 * exp((Tamb + 273) / 343)**3 * exp(S * ((Tamb + 273) / 273))
        elif(idx == 3 or idx ==4):
            _hrmodel['lambdab'] = 0.00005 * exp(3.5 * ((Tamb + 273) / 398)) * exp(S * ((Tamb + 273) / 273))
        else:
            _hrmodel['lambdab'] = 1.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class FilmNetwork(Resistor):
    """
    Fixed Value Film Network Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.4
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "Any"]

    def __init__(self):
        """
        Initializes the Fixed Value Film Network Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 28               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0, 0.5,
                     14.0, 36.0, 660.0]
        self._piQ = [1.0, 3.0]
        self._piR = [1.0]
        self._lambdab_count = [0.0023, 0.0066, 0.031, 0.013, 0.055, 0.022, 0.043, 0.077, 0.15, 0.10, 0.0011, 0.055, 0.15, 1.7]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Number of Elements:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels[4] = u"\u03C0<sub>T</sub>:"
        self._out_labels.append(u"\u03C0<sub>NR</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Film Network
        Resistor prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the number of resistors in the network entry.
        part.txtNumber = _widg.make_entry(_width_=entry_width)
        part.txtNumber.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 58)
        layout.put(part.txtNumber, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Fixed Values Film Network Resistor Component
        Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the pi NR results entry.  This is the same value as the
        # number of elements in the program database.
        part.txtPiNR = _widg.make_entry(_width_=entry_width,
                                        editable=False, bold=True)
        layout.put(part.txtPiNR, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_inputs_load(self, part)

        part.txtNumber.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 58))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Resistor.assessment_results_load(self, part)

        part.txtPiNR.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 58))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Film Network Resistor Component Class.

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
        Eidx = systemmodel.get_value(systemrow, 22)              # Environment index

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
        the Fixed Value Film Network Resistor Component Class.

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
        _hrmodel['equation'] = "lambdab * piT * piNR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Tcase = partmodel.get_value(partrow, 105)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piNR'] = partmodel.get_value(partrow, 58)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        _hrmodel['piR'] = partmodel.get_value(partrow, 80)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.00006

        # Temperature correction factor.  We store this value in the pi_u
        # field in the program database.
        S = P / Prated
        if(Tcase == 0):
            Tcase = Tamb + 55 * S

        _hrmodel['piT'] = exp(-4056 * ((1 / (Tcase + 273)) - (1 / 298)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class FilmPower(Resistor):
    """
    Fixed Value Film Power Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.3
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _range = ["", "10 to 100", ">100 to 100K", ">100K to 1M", ">1M"]

    def __init__(self):
        """
        Initializes the Fixed Value Film Power Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 27               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 17.0, 6.0, 8.0, 14.0, 18.0, 25.0, 0.5,
                     14.0, 36.0, 660.0]
        self._piQ = [1.0, 3.0]
        self._piR = [1.0, 1.2, 1.3, 3.5]
        self._lambdab_count = [0.012, 0.025, 0.13, 0.062, 0.21, 0.078, 0.10, 0.19, 0.24, 0.32, 0.0060, 0.18, 0.47, 8.2]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Film Power Resistor Component Class.

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
        the Fixed Value Film Power Resistor Component Class.

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
        _hrmodel['equation'] = "lambdab * piR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piR'] = partmodel.get_value(partrow, 80)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        S = P / Prated
        _hrmodel['lambdab'] = 0.00733 * exp(0.202 * ((Tamb + 273) / 298))**2.6 * exp((S / 1.45) * ((Tamb + 273) / 273)**0.89)**1.3

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Wirewound(Resistor):
    """
    Fixed Value Wirewound Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.5
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-93", "Lower"]
    _range = ["", "<10K", "10K to 100K", "100K to 1M", ">1M"]

    def __init__(self):
        """
        Initializes the Fixed Value Wirewound Resistor Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 29               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 11.0, 5.0, 18.0, 15.0, 18.0, 28.0, 35.0, 27.0,
                     0.8, 14.0, 38.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._piR = [1.0, 1.7, 3.0, 5.0]
        self._lambdab_count = [0.0085, 0.018, 0.10, 0.045, 0.16, 0.15, 0.17, 0.30, 0.38, 0.26, 0.0068, 0.13, 0.37, 5.4]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Wirewound Resistor Component Class.

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
        the Fixed Value Wirewound Resistor Component Class.

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
        _hrmodel['equation'] = "lambdab * piR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piR'] = partmodel.get_value(partrow, 80)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        S = P / Prated
        _hrmodel['lambdab'] = 0.0031 * exp(((Tamb + 273) / 398)**10) * exp((S * ((Tamb + 273) / 273))**1.5)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class WirewoundPower(Resistor):
    """
    Fixed Value Wirewound Power Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.6
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-26", "Lower"]
    _range = [""]
    _ranges = [["", "<500", "500 to 1K", "1K to 5K", "5K to 7.5K",
                "7.5K to 10K", "10K to 15K", "15K to 20K", ">20K"],
               ["", "<100", "100 to 1K", "1K to 10K", "10K to 100K",
                "100K to 150K", "150K to 200K"]]
    _spec = ["", "MIL-R-39007 (RWR)", "MIL-R-26 (RW)"]
    _specsheet = [["", "RWR 71", "RWR 74", "RWR 78", "RWR 80", "RWR 81",
                   "RWR 82", "RWR 84", "RWR 89"], ["", "RW 10", "RW 11",
                   "RW 12", "RW 13", "RW 14", "RW 15", "RW 16", "RW 20",
                   "RW 21", "RW 22", "RW 23", "RW 24", "RW 29", "RW 30",
                   "RW 31", "RW 32", "RW 33", "RW 34", "RW 35", "RW 36",
                   "RW 37", "RW 38", "RW 39", "RW 47", "RW 55", "RW 56",
                   "RW 67", "RW 68", "RW 69", "RW 70", "RW 74", "RW 78",
                   "RW 79", "RW 80", "RW 81"]]

    def __init__(self):
        """
        Initializes the Fixed Value Wirewound Power Resistor Component
        Class.
        """

        Resistor.__init__(self)

        self.subcategory = 30               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0,
                     0.3, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._piR = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._piR_RWR = [[1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0],
                         [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6],
                         [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0]]
        self._piR_RW = [[1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
                        [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
                        [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.2, 0.0, 0.0],
                        [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.5, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 1.6, 0.0],
                        [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
                        [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
                        [1.0, 1.0, 1.4, 2.4, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 2.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.0, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.5, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 0.0, 0.0, 0.0, 0.0]]
        self._Lambdab_count = [[0.014, 0.031, 0.16, 0.077, 0.26, 0.073, 0.15, 0.19, 0.39, 0.42, 0.0042, 0.21, 0.62, 9.4],
                               [0.013, 0.028, 0.15, 0.070, 0.24, 0.065, 0.13, 0.18, 0.35, 0.38, 0.0038, 0.19, 0.56, 8.6]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Specification:")
        self._in_labels.append(u"Spec Sheet:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Wirewound Power
        Resistor prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout)

        part.cmbSpecification = _widg.make_combo(simple=True)
        for i in range(len(self._spec)):
            part.cmbSpecification.insert_text(i, self._spec[i])
        part.cmbSpecification.connect("changed",
                                      self.combo_callback,
                                      part, 101)
        layout.put(part.cmbSpecification, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_inputs_load(self, part)

        part.cmbSpecification.set_active(int(part.model.get_value(part.selected_row, 101)))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Fixed Value Wirewound Power
        Resistor Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        model = part.model
        row = part.selected_row

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 101):                     # Specification
            m = part.cmbSpecSheet.get_model()
            m.clear()

            if(idx == 1):
                for i in range(len(self._ranges[idx - 1])):
                    part.cmbRRange.insert_text(i, self._ranges[idx - 1][i])
            elif(idx == 2):
                for i in range(len(self._ranges[idx - 1])):
                    part.cmbRRange.insert_text(i, self._ranges[idx - 1][i])

            for i in range(len(self._specsheet[idx - 1])):
                part.cmbSpecSheet.insert_text(i, self._specsheet[idx - 1][i])

        elif(_index_ == 102):                   # Specification sheet
            idx2 = part.cmbRRange.get_active()

            if(idx == 1):
                S = self._piR_RWR[idx - 1][idx2 - 1]
            elif(idx == 2):
                S = self._piR_RW[idx - 1][idx2 - 1]
            else:
                S = 1.0

            model.set_value(row, 80, S)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Wirewound Power Resistor Component Class.

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
        Sidx = partmodel.get_value(partrow, 101)        # Specification

        _hrmodel['lambdab'] = self._lambdab_count[Sidx - 1][Eidx - 1]

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
        the Fixed Value Wirewound Power Resistor Component Class.

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
        _hrmodel['equation'] = "lambdab * piR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        S = P / Prated
        _hrmodel['lambdab'] = 0.00148 * exp(((Tamb + 273) / 298)**2) * exp((S / 0.5) * (Tamb + 273) / 273)

        # Resistance correction factor.
        idx = partmodel.get_value(partrow, 102)
        idx2 = partmodel.get_value(partrow, 95)

        if(idx == 1):
            _hrmodel['piR'] = self._piR_RWR[idx - 1][idx2 - 1]
        elif(idx == 2):
            _hrmodel['piR'] = self._piR_RW[idx - 1][idx2 - 1]
        else:
            _hrmodel['piR'] = 1.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class WirewoundPowerChassis(Resistor):
    """
    Fixed Value Wirewound Chassis-Mounted Power Resistor Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 9.7
    """

    _quality = ["", "S", "R", "P", "M", "MIL-R-18546", "Lower"]
    _range = ["", "<500", "500 to 1K", "1K to 5K", "5K to 10K",
              "10K to 20K", ">20K"]
    _spec = ["", "MIL-R-18546 (RER)", "MIL-R-39009 (RE)"]
    _specsheet = [["", "RER 60", "RER 65", "RER 70", "RER 75"], ["", "RE 60",
                   "RE 65", "RE70", "RE 77", "RE 80"]]
    _type = [["", "Type G (Inductive)", "Type N (Non-Inductive)"], ["", "Inductively Wound",
              "Non-Inductively Wound"]]

    def __init__(self):
        """
        Initializes the Fixed Value Wirewound Chassis-Mounted Power Resistor
        Component Class.
        """

        Resistor.__init__(self)

        self.subcategory = 31               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 16.0, 4.0, 8.0, 9.0, 18.0, 23.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 5.0, 15.0]
        self._piR = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._piR_RER = [[1.0, 1.2, 1.2, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                         [1.0, 1.0, 1.2, 1.2, 1.6, 0.0],
                         [1.0, 1.0, 1.0, 1.1, 1.2, 0.0]]
        self._piR_RE = [[1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
                        [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
                        [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
                        [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
                        [1.0, 1.0, 1.0, 1.1, 1.6, 0.0]]
        self._lambdab_count = [0.008, 0.18, 0.096, 0.045, 0.15, 0.044, 0.088, 0.12, 0.24, 0.25, 0.004, 0.13, 0.37, 5.5]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Specification:")
        self._in_labels.append(u"Spec Sheet:")
        self._in_labels.append(u"Construction:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Value Wirewound Chassis-
        Mounted Power Resistor prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Resistor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        part.cmbSpecification = _widg.make_combo(simple=True)
        for i in range(len(self._spec)):
            part.cmbSpecification.insert_text(i, self._spec[i])
        part.cmbSpecification.connect("changed",
                                      self.combo_callback,
                                      part, 101)
        layout.put(part.cmbSpecification, x_pos, y_pos)
        y_pos += 30

        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbSpecSheet.connect("changed",
                                  self.combo_callback,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        part.cmbConstruction = _widg.make_combo(simple=True)
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Resistor.assessment_inputs_load(self, part)

        part.cmbSpecification.set_active(int(part.model.get_value(part.selected_row, 101)))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Fixed Value Wirewound Chassis-
        Mounted Power Resistor Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        model = part.model
        row = part.selected_row

        Resistor.combo_callback(self, combo, part, _index_)

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 16):                      # Construction
            idx = part.cmbSpecSheet.get_active()
            idx2 = part.cmbRRange.get_active()

            if(idx == 1):                       # Inductive
                C = self._piR_RER[idx - 1][idx2 - 1]
            elif(idx == 2):                     # Non-Inductive
                C = self._piR_RE[idx - 1][idx2 - 1]
            else:
                C = 1.0

            model.set_value(row, 80, C)

        elif(_index_ == 101):                   # Specification
            part.cmbSpecSheet.get_model().clear()

            for i in range(len(self._specsheet[idx - 1])):
                part.cmbSpecSheet.insert_text(i, self._specsheet[idx - 1][i])

            for i in range(len(self._type[idx - 1])):
                part.cmbConstruction.insert_text(i, self._type[idx - 1][i])

            part.cmbConstruction.set_active(int(model.get_value(row, 16)))
            part.cmbSpecSheet.set_active(int(model.get_value(row, 102)))

        elif(_index_ == 102):                   # Specification sheet
            idx2 = part.cmbRRange.get_active()

            if(idx == 1):
                S = self._piR_RWR[idx - 1][idx2 - 1]
            elif(idx == 2):
                S = self._piR_RW[idx - 1][idx2 - 1]
            else:
                S = 1.0

            model.set_value(row, 80, S)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fixed Value Wirewound Chassis-Mounted Power Resistor Component
        Class.

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
        the Fixed Value Wirewound Chassis-Mounted Power Resistor Component
        Class.

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
        _hrmodel['equation'] = "lambdab * piR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Base hazard rate.
        S = P / Prated
        _hrmodel['lambdab'] = 0.00015 * exp(2.64 * ((Tamb + 273) / 298)) * exp((S / 0.466) * (Tamb + 273) / 273)

        # Resistance correction factor.
        idx = partmodel.get_value(partrow, 102)
        idx2 = partmodel.get_value(partrow, 95)

        if(idx == 1):               # Inductive
            _hrmodel['piR'] = self._piR_RER[idx - 1][idx2 - 1]
        elif(idx == 2):             # Non-Inductive
            _hrmodel['piR'] = self._piR_RE[idx - 1][idx2 - 1]
        else:
            _hrmodel['piR'] = 1.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
