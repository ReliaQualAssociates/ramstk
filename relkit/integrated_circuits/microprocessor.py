#!/usr/bin/env python
""" This is the microprocessor integrated circuit class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       microprocessor.py is part of The RelKit Project
#
# All rights reserved.

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from ic import IntegratedCircuit


class Microprocessor(IntegratedCircuit):
    """
    Microprocessor class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.1
    """

    def __init__(self):
        """
        Initializes the Microprocessor Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 4                # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[0.06, 0.12, 0.24, 0.48], [0.14, 0.28, 0.56, 1.12]]
        self._Ea = [[0.65], [0.65]]

        self._lambdab_count = [[[0.028, 0.061, 0.098, 0.091, 0.13, 0.12, 0.13, 0.17, 0.22, 0.18, 0.028, 0.11, 0.24, 3.30],
                                [0.052, 0.110, 0.180, 0.160, 0.23, 0.21, 0.24, 0.32, 0.39, 0.31, 0.052, 0.20, 0.41, 5.60],
                                [0.110, 0.230, 0.360, 0.330, 0.47, 0.44, 0.49, 0.65, 0.81, 0.65, 0.110, 0.42, 0.86, 12.0]],
                               [[0.048, 0.089, 0.130, 0.120, 0.16, 0.16, 0.17, 0.24, 0.28, 0.22, 0.048, 0.15, 0.28, 3.40],
                                [0.093, 0.170, 0.240, 0.220, 0.29, 0.30, 0.32, 0.45, 0.52, 0.40, 0.093, 0.27, 0.50, 5.60],
                                [0.190, 0.340, 0.490, 0.450, 0.60, 0.61, 0.66, 0.90, 1.10, 0.82, 0.190, 0.54, 1.00, 12.0]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = "# of Bits:"
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation input tab with the
        widgets needed to select inputs for Microprocessor Integrated
        Circuit prediction calculations.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        part.cmbElements.append_text("")
        part.cmbElements.append_text("Up to 8 Bits")
        part.cmbElements.append_text("Up to 16 Bits")
        part.cmbElements.append_text("Up to 32 Bits")
        part.cmbElements.append_text("Up to 64 Bits")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation results tab with the
        widgets to display Microprocessor Integrated Circuit calculation
        results.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the ReliaFree Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Microprocessor Integrated Circuit Class.

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
        _hrmodel['equation'] = "lambdab * piQ * piL"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Bidx = partmodel.get_value(partrow, 24)         # No of elements index
        Tidx = partmodel.get_value(partrow, 104)        # Technology index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Y = partmodel.get_value(partrow, 112)

        _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Bidx - 1][Eidx - 1]

        # Calculate the learning factor.  We store this in the pi_r
        # field in the Program Database.
        _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Microprocessor Integrated Circuit Class.

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
        _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)
        P = partmodel.get_value(partrow, 64)

        # Retrieve hazard rate inputs.
        _hrmodel['C1'] = partmodel.get_value(partrow, 8)
        K1 = partmodel.get_value(partrow, 40)
        K2 = partmodel.get_value(partrow, 41)
        K3 = partmodel.get_value(partrow, 42)
        B = partmodel.get_value(partrow, 58)
        Np = partmodel.get_value(partrow, 60)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Tbase = partmodel.get_value(partrow, 103)
        Y = partmodel.get_value(partrow, 112)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        idx = int(partmodel.get_value(partrow, 67))
        if(thetaJC == 0):
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)
        else:
            thetaJC = partmodel.get_value(partrow, 109)

        Tj = Tcase + thetaJC * P

        # Calculate the temperature factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        K5 = self._K5[idx - 1]
        K6 = self._K6[idx - 1]
        _hrmodel['C2'] = K5 * (Np ** K6)

        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate the learning factor.  We store this in the pi_r
        # field in the Program Database.
        _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 35, K5)
        partmodel.set_value(partrow, 36, K6)
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
