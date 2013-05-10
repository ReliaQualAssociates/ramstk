#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'


# -*- coding: utf-8 -*-
#
#       electrolytic.py is part of The RelKit Project
#
# All rights reserved.

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except:
    import calculations as _calc
    import widgets as _widg

from capacitor import Capacitor


class TantalumSolid(Capacitor):
    """
    Fixed Solid Tantalum Electrolytic Capacitor Component Class.
    Covers specification MIL-C-39003.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 10.12
    """

    _quality = ["", "D", "C", "S", "B", "R", "P", "M", "L", "Lower"]
    _specification = ["", "MIL-C-39003 (CSR)"]
    _specsheet = [["", "All"]]

    def __init__(self):
        """
        Initializes the Fixed Solid Tantalum Electrolytic Capacitor
        Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 51                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0, 12.0, 20.0,
                     24.0, 0.4, 11.0, 29.0, 530.0]
        self._piQ = [0.001, 0.01, 0.03, 0.03, 0.1, 0.3, 1.0, 1.5, 10.0]
        self._lambdab_count = [0.0018, 0.0039, 0.016, 0.0097, 0.028, 0.0091, 0.011, 0.034, 0.057, 0.055, 0.00072, 0.022, 0.066, 1.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Eff. Series Resistance:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>SR</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Fixed Solid Tantalum
        Electrolytic Capacitor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_inputs_create(self, part, layout,
                                                   x_pos, y_pos)

        part.txtEffResistance = _widg.make_entry()
        part.txtEffResistance.connect("focus-out-event",
                                      self._callback_entry,
                                      part, "float", 95)
        layout.put(part.txtEffResistance, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):

        """ Loads the RelKit Workbook calculation input widgets with
            calculation input information.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Capacitor.assessment_inputs_load(self, part)

        part.txtEffResistance.set_text(str(fmt.format(part.model.get_value(part.selected_row, 95))))

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Fixed Solid Tantalum Electrolytic Capacitor
            Component Class calculation results.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_results_create(self, part, layout,
                                                    x_pos, y_pos)

        part.txtPiSR = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiSR, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_load(self, part):

        """ Loads the RelKit Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        Capacitor.assessment_results_load(self, part)

        part.txtPiSR.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 81))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Fixed Solid Tantalum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Fixed Solid Tantalum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piCV * piSR * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        C = partmodel.get_value(partrow, 15)
        VappliedAC = partmodel.get_value(partrow, 64)
        Vapplied = partmodel.get_value(partrow, 66)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Vrated = partmodel.get_value(partrow, 94)
        Reff = partmodel.get_value(partrow, 95)

        # Base hazard rate.
        S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
        _hrmodel['lambdab'] = 0.00375 * exp((S / 0.4)**3 + 1) * exp(2.6 * ((Tamb + 273) / 398)**9.0)

        # Capacitance correction factor.
        _hrmodel['piCV'] = 1.0 * C**0.12

        # Series resistance correction factor.
        CR = Reff / Vapplied
        if(CR > 0.8):
            _hrmodel['piSR'] = 0.066
        elif(CR < 0.8 and CR >= 0.6):
            _hrmodel['piSR'] = 0.10
        elif(CR < 0.6 and CR >= 0.4):
            _hrmodel['piSR'] = 0.13
        elif(CR < 0.4 and CR >= 0.2):
            _hrmodel['piSR'] = 0.20
        elif(CR < 0.2 and CR >= 0.1):
            _hrmodel['piSR'] = 0.27
        elif(CR < 0.1 and CR >= 0.0):
            _hrmodel['piSR'] = 0.33
        else:
            _hrmodel['piSR'] = 0.33

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 70, _hrmodel['piCV'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 81, _hrmodel['piSR'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class TantalumNonSolid(Capacitor):

    """ Fixed Non-Solid Tantalum Electrolytic Capacitor Component Class.
        Covers specifications MIL-C-3965 and MIL-C-39006.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.13

    """

    _construction = ["", "Slug, All Tantalum", "Foil, Hermetic",
                     "Slug, Hermetic", "Foil, Non-Hermetic",
                     "Slug, Non-Hermetic"]
    _quality = ["", "S", "R", "P", "M", "L", "MIL-C-3965, Non-Est. Rel.",
                "Lower"]
    _specification = ["", "MIL-C-3965 (CL)", "MIL-C-39003 (CLR)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C", u"175\u00B0C"],
                  ["", u"125\u00B0C"]]

    def __init__(self):

        """ Initializes the Fixed Non-Solid Tantalum Electrolytic Capacitor
            Component Class.

        """

        Capacitor.__init__(self)

        self.subcategory = 52                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [0.3, 1.0, 2.0, 2.5, 3.0]
        self._piE = [1.0, 2.0, 10.0, 6.0, 16.0, 4.0, 8.0, 14.0, 30.0,
                     23.0, 0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0]
        self._lambdab_count =[0.0061, 0.013, 0.069, 0.039, 0.11, 0.031, 0.061, 0.13, 0.29, 0.18, 0.0030, 0.069, 0.26, 4.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"
        self._in_labels.append(u"Construction:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation input tab with the
            widgets needed to select inputs for Fixed Non-Solid Tantalum
            Electrolytic Capacitor Component Class prediction calculations.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_inputs_create(self, part, layout,
                                                   x_pos, y_pos)

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                     self._callback_combo,
                                     part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):

        """ Loads the RelKit Workbook calculation input widgets with
            calculation input information.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        Capacitor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(part.model.get_value(par.selected_trow, 16)))

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Fixed Non-Solid Tantalum Electrolytic Capacitor
            Component Class calculation results.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_results_create(self, part, layout,
                                                    x_pos, y_pos)

        part.txtPiC = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_load(self, part):

        """ Loads the RelKit Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        Capacitor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 69))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Fixed Non-Solid Tantalum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Fixed Non-Solid Tantalum Electrolytic Capacitor Component
            Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piCV * piC * piQ * piE"

        model = partmodel
        row = partrow

        # Retrieve junction temperature inputs.
        Tamb = model.get_value(row, 37)
        Trise = model.get_value(row, 107)
        thetaJC = model.get_value(row, 109)

        # Retrieve hazard rate inputs.
        C = model.get_value(row, 15)
        VappliedAC = model.get_value(row, 64)
        Vapplied = model.get_value(row, 66)
        _hrmodel['piQ'] = model.get_value(row, 79)
        Vrated = model.get_value(row, 94)
        Reff = model.get_value(row, 95)

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 102)
        S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
        if(idx == 1):
            Tref = 358
        elif(idx == 2):
            Tref = 398
        elif(idx == 3):
            Tref = 448
        else:
            Tref = 358

        _hrmodel['lambdab'] = 0.00375 * exp((S / 0.4)**3 + 1) * exp(2.6 * ((Tamb + 273) / Tref)**9.0)

        # Capacitance correction factor.
        _hrmodel['piCV'] = 0.82 * C**0.066

        # Construction correction factor.
        idx = partmodel.get_value(partrow, 16)
        _hrmodel['piC'] = self._piC[idx - 1]

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        model.set_value(row, 46, _hrmodel['lambdab'])
        model.set_value(row, 69, _hrmodel['piC'])
        model.set_value(row, 70, _hrmodel['piCV'])
        model.set_value(row, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Aluminum(Capacitor):

    """ Fixed Wet Aluminum Electrolytic Capacitor Component Class.
        Covers specification MIL-C-39016.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.14
    """

    _quality = ["", "S", "R", "P", "M", "Non-Est. Rel.", "Lower"]
    _specification = ["", "MIL-C-39016 (CU and CUR)"]
    _specsheet = [["", u"85\u00B0C", u"105\u00B0C", u"125\u00B0C"]]

    def __init__(self):

        """ Initializes the Fixed Wet Aluminum Electrolytic Capacitor
            Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 53                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0, 28.0, 35.0,
                     27.0, 0.5, 14.0, 38.0, 690.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
        self._lambdab_count =[0.024, 0.061, 0.42, 0.18, 0.59, 0.46, 0.55, 2.1, 2.6, 1.2, .012, 0.49, 1.7, 21.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Fixed Wet Aluminum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(hmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Fixed Wet Aluminum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        C = partmodel.get_value(partrow, 15)
        VappliedAC = partmodel.get_value(partrow, 64)
        Vapplied = partmodel.get_value(partrow, 66)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Vrated = partmodel.get_value(partrow, 94)
        Reff = partmodel.get_value(partrow, 95)

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 102)
        S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
        if(idx == 1):               # 85C
            Tref = 358
        elif(idx == 2):             # 105C
            Tref = 378
        elif(idx == 3):             # 125C
            Tref = 398
        else:                       # Default
            Tref = 358

        _hrmodel['lambdab'] = 0.00254 * exp((S / 0.5)**3 + 1) * exp(5.09 * ((Tamb + 273) / Tref)**5.0)

        # Capacitance correction factor.
        _hrmodel['piCV'] = 0.34 * C**0.186

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 70, _hrmodel['piCV'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class AluminumDry(Capacitor):

    """ Fixed Dry Aluminum Electrolytic Capacitor Component Class.
        Covers specification MIL-C-62.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.15
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-62 (CE)"]
    _specsheet = [["", u"85\u00B0C"]]

    def __init__(self):

        """ Initializes the Fixed Dry Aluminum Electrolytic Capacitor
            Component Class.

        """

        Capacitor.__init__(self)

        self.subcategory = 54                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 12.0, 6.0, 17.0, 10.0, 12.0, 28.0, 35.0,
                     27.0, 0.5, 14.0, 38.0, 690.0]
        self._piQ = [3.0, 10.0]
        self._lambdab_count =[0.029, 0.081, 0.58, 0.24, 0.83, 0.73, 0.88, 4.3, 5.4, 2.0, 0.015, 0.68, 2.8, 28.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Fixed Dry Aluminum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Eidx = systemmodel.get_value(systemrow, 22)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Fixed Dry Aluminum Electrolytic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        C = partmodel.get_value(partrow, 15)
        VappliedAC = partmodel.get_value(partrow, 64)
        Vapplied = partmodel.get_value(partrow, 66)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Vrated = partmodel.get_value(partrow, 94)
        Reff = partmodel.get_value(partrow, 95)

        # Base hazard rate.
        idx = partmodel.get_value(partrow, 102)
        S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
        if(idx == 1):               # 85C
            Tref = 358
        else:                       # Default
            Tref = 358

        _hrmodel['lambdab'] = 0.00254 * exp((S / 0.55)**3 + 1) * exp(4.09 * ((Tamb + 273) / Tref)**5.9)

        # Capacitance correction factor.
        _hrmodel['piCV'] = 0.34 * C**0.186

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 70, _hrmodel['piCV'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
