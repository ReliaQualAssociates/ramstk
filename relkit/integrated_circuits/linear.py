#!/usr/bin/env python
""" This is the linear integrated circuit class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       linear.py is part of The RelKit Project
#
# All rights reserved.

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from ic import IntegratedCircuit


class Linear(IntegratedCircuit):
    """
    Linear integrated circuit class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.1
    """

    def __init__(self):
        """ Initializes the Linear Integrated Circuit Component Class. """

        IntegratedCircuit.__init__(self)

        self.subcategory = 1                # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[0.01, 0.02, 0.04, 0.06], [0.01, 0.02, 0.04, 0.06]]
        self._Ea = [[0.65], [0.65]]

        self._lambdab_count = [[0.0095, 0.024, 0.039, 0.034, 0.049, 0.057,
                                0.062, 0.12, 0.13, 0.076, 0.0095, 0.044, 0.096,
                                1.1],
                               [0.0170, 0.041, 0.065, 0.054, 0.078, 0.100,
                                0.110, 0.22, 0.24, 0.130, 0.0170, 0.072, 0.150,
                                1.4],
                               [0.0330, 0.074, 0.110, 0.092, 0.130, 0.190,
                                0.190, 0.41, 0.44, 0.220, 0.0330, 0.120, 0.260,
                                2.0],
                               [0.0500, 0.120, 0.180, 0.150, 0.210, 0.300,
                                0.300, 0.63, 0.67, 0.350, 0.0500, 0.190, 0.410,
                                3.4]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = "# of Transistors:"
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Linear Integrated Circuit
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        part.cmbElements.append_text("")
        part.cmbElements.append_text("1 to 100")
        part.cmbElements.append_text("101 to 300")
        part.cmbElements.append_text("301 to 1000")
        part.cmbElements.append_text("1001 to 10000")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Linear Integrated Circuit calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Linear Integrated Circuit Class.

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
        Bidx = partmodel.get_value(partrow, 24)     # No of elements index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Y = partmodel.get_value(partrow, 112)
        Eidx = systemmodel.get_value(systemrow, 22)         # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

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
        the Linear Integrated Circuit Class.

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
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['C1'] = partmodel.get_value(partrow, 8)
        K5 = partmodel.get_value(partrow, 35)
        K6 = partmodel.get_value(partrow, 36)
        B = partmodel.get_value(partrow, 58)
        Np = partmodel.get_value(partrow, 60)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
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
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        Tj = Tcase + thetaJC * P

        # Calculate the temperature factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))
        _hrmodel['C2'] = K5 * (Np ** K6)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate the learning factor.  We store this in the pi_r
        # field in the Program Database.
        _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
