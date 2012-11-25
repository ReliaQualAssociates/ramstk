#!/usr/bin/env python
""" This is the Coil class."""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       coil.py is part of The RelKit Project
#
# All rights reserved.

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from inductor import Inductor


class Coil(Inductor):
    """
    Coil Component Class.
    Covers specifications MIL-C-15305 and MIL-C-39010.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.2
    """

    _construction = ["", "Fixed", "Variable"]
    _quality = ["", "S", "R", "P", "M", "MIL-C-15305", "Lower"]
    _insulation = ["", "A", "B", "F", "O"]

    def __init__(self):
        """ Initializes the Coil Component Class. """

        Inductor.__init__(self)

        self.subcategory = 63               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [1.0, 2.0]
        self._piE = [1.0, 4.0, 12.0, 5.0, 16.0, 5.0, 7.0, 6.0, 8.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 4.0, 20.0]
        self._lambdab_count = [[0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022, 0.052, 0.00083, 0.25, 0.073, 1.1],
                               [0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044, 0.10, 0.0017, 0.05, 0.15, 2.2]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Construction:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation input tab with the
        widgets needed to select inputs for Coil Component Class
        prediction calculations.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the dfirst widget.
        """

        y_pos = Inductor.assessment_inputs_create(self, part, layout,
                                                  x_pos, y_pos)

        part.cmbConstruction = _widg.make_combo(simple=True)
        part.cmbConstruction.set_name("TRANSIENT")
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the ReliaFree Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        Inductor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(partmodel.get_value(partrow, 16)))

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation results tab with the
        widgets to display Coil Component Class calculation results.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- teh x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Inductor.assessment_results_create(self, part, layout,
                                                   x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiC = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        part.txtPiC.set_name("TRANSIENT")
        layout.put(part.txtPiC, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_load(self, part):
        """
        Loads the ReliaFree Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        Inductor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2g}".format(partmodel.get_value(partrow, 69))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Coil Component Class.

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

        model = partmodel
        row = partrow

        # Retrieve hazard rate inputs.
        Cidx = part._attribute[16]                      # Construction index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Cidx - 1][Eidx - 1]

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
        the Coil Component Class.

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
        _hrmodel['equation'] = "lambdab * piC * piQ * piE"

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
        if(idx == 1):                       # Class A
            Tref = 352.0
            K = 14.0
        elif(idx == 2):                     # Class B
            Tref = 364.0
            K = 8.7
        elif(idx == 3):                     # Class F
            Tref = 409.0
            K = 10.0
        elif(idx == 4):                     # Class O
            Tref = 329.0
            K = 15.6
        else:                               # Default
            Tref = 329.0
            K = 15.6

        _hrmodel['lambdab'] = 0.00375 * exp(((Ths + 273) / Tref)**K)

        # Construction correction factor.
        idx = partmodel.get_value(partrow, 16)
        _hrmodel['piC'] = self._piC[idx - 1]

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Ths)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 69, _hrmodel['piC'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 107, Trise)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
