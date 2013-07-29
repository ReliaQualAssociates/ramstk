#!/usr/bin/env python
""" This is the thyristor component class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       thyristor.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from semiconductor import Semiconductor


class Thyristor(Semiconductor):
    """
    Thyristor Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.10
    """

    def __init__(self):
        """ Initializes the Thyristor Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 21               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14,
                               0.14, 0.31, 0.12, 0.0012, 0.053, 0.16, 1.1]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Rated Forward Current (I<sub>F</sub>):")
        self._in_labels.append(u"Applied Voltage (V<sub>Applied</sub>):")
        self._in_labels.append(u"Rated Voltage (V<sub>Rated</sub>):")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>R</sub>:")
        self._out_labels.append(u"\u03C0<sub>S</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Thyristor prediction
        calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the rated forward current entry.
        part.txtFwdCurrent = _widg.make_entry(_width_=entry_width)
        part.txtFwdCurrent.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 62)
        layout.put(part.txtFwdCurrent, x_pos, y_pos)
        y_pos += 30

        # Create the applied voltage entry.
        part.txtVApplied = _widg.make_entry(_width_=entry_width)
        part.txtVApplied.connect("focus-out-event",
                                 self.entry_callback,
                                 part, "float", 66)
        layout.put(part.txtVApplied, x_pos, y_pos)
        y_pos += 30

        # Create the rated voltage entry.
        part.txtVRated = _widg.make_entry(_width_=entry_width)
        part.txtVRated.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 94)
        layout.put(part.txtVRated, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Thyristor calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the current rating correction factor results entry.
        part.txtPiR = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiR, x_pos, y_pos)
        y_pos += 30

        # Create the voltage stress correction factor results entry.
        part.txtPiS = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiS, x_pos, y_pos)

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

        Semiconductor.assessment_inputs_load(self, part)

        part.txtFwdCurrent.set_text(str(fmt.format(part.model.get_value(part.selected_row, 62))))
        part.txtVApplied.set_text(str(fmt.format(part.model.get_value(part.selected_row, 66))))
        part.txtVRated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_results_load(self, part)

        part.txtPiR.set_text(str(fmt.format(part.model.get_value(part.selected_row, 80))))
        part.txtPiS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 81))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Thyristor Class.

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
        the Thyristor Class.

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
        _hrmodel['equation'] = "lambdab * piT * piR * piS * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        IF = partmodel.get_value(partrow, 62)
        VApplied = partmodel.get_value(partrow, 66)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        VRated = partmodel.get_value(partrow, 94)
        _hrmodel['lambdab'] = 0.0022

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

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-3082.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Current rating correction factor.
        _hrmodel['piR'] = IF**0.4

        # Voltage stress correction factor.  We store this in the pi_sr
        # field in the Program Database.
        Vs = VApplied / VRated
        if(Vs > 0.3):
            _hrmodel['piS'] = Vs**1.9
        else:
            _hrmodel['piS'] = 0.10

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 81, _hrmodel['piS'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
