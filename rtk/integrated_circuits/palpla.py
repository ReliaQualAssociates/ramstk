#!/usr/bin/env python
""" This is the PAL/PLA integrated circuit class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       palpla.py is part of The RelKit Project
#
# All rights reserved.

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from ic import IntegratedCircuit


class PALPLA(IntegratedCircuit):
    """
    PAL/PLA device class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.1
    """

    def __init__(self):
        """ Initializes the PAL/PLA IC Component Class. """

        IntegratedCircuit.__init__(self)

        self.subcategory = 3        # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[0.01, 0.021, 0.042], [0.00085, 0.0017, 0.0034, 0.0068]]
        self._Ea = [[0.65], [0.65]]

        self._lambdab_count = [[[0.0061, 0.016, 0.029, 0.027, 0.040, 0.032, 0.037, 0.044, 0.061, 0.054, 0.0061, 0.034, 0.076, 1.2],
                                [0.0110, 0.028, 0.048, 0.046, 0.065, 0.054, 0.063, 0.077, 0.100, 0.089, 0.0110, 0.057, 0.120, 1.9],
                                [0.0220, 0.052, 0.087, 0.082, 0.120, 0.099, 0.110, 0.140, 0.190, 0.160, 0.0220, 0.100, 0.220, 3.3]],
                               [[0.0046, 0.018, 0.035, 0.035, 0.052, 0.035, 0.044, 0.044, 0.070, 0.070, 0.0046, 0.044, 0.100, 1.9],
                                [0.0056, 0.021, 0.042, 0.042, 0.062, 0.042, 0.052, 0.053, 0.084, 0.083, 0.0056, 0.052, 0.120, 2.3],
                                [0.0061, 0.022, 0.043, 0.042, 0.063, 0.043, 0.054, 0.055, 0.086, 0.084, 0.0081, 0.053, 0.130, 2.3],
                                [0.0095, 0.033, 0.064, 0.063, 0.094, 0.065, 0.080, 0.083, 0.130, 0.130, 0.0095, 0.079, 0.190, 3.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = "# of Gates:"
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for PAL/PLA Integrated Circuit
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

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        if(model.get_value(row, 104) == 1):     # Bipolar
            part.cmbElements.append_text("1 to 200")
            part.cmbElements.append_text("201 to 1000")
            part.cmbElements.append_text("1001 to 5000")
        elif(model.get_value(row, 104) == 2):   # CMOS
            part.cmbElements.append_text("1 to 500")
            part.cmbElements.append_text("501 to 1000")
            part.cmbElements.append_text("1001 to 5000")
            part.cmbElements.append_text("5001 to 20000")

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
        PAL/PLA Integrated Circuit Class.

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
        the PAL/PLA Integrated Circuit Class.

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
        K5 = partmodel.get_value(partrow, 35)
        K6 = partmodel.get_value(partrow, 36)
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
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)
        else:
            thetaJC = partmodel.get_value(partrow, 109)

        Tj = Tcase + thetaJC * P

        # Calculate the temperature factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        _hrmodel['C2'] = K5 * (Np ** K6)

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
