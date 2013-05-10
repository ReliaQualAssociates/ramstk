#!/usr/bin/env python

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       variable.py is part of The RelKit Project
#
# All rights reserved.

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except:
    import calculations as _calc
    import widgets as _widg

from capacitor import Capacitor


class Ceramic(Capacitor):

    """ Variable Ceramic Capacitor Component Class.
        Covers specification MIL-C-81.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.16

    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-81 (CV)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C"]]

    def __init__(self):

        """ Initializes the Variable Ceramic Capacitor Component Class. """

        Capacitor.__init__(self)

        self.subcategory = 55                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0,
                     0.4, 20.0, 52.0, 950.0]
        self._piQ = [4.0, 20.0]
        self._lambdab_count =[0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2, 12.0, 4.1, 0.032, 1.9, 5.9, 85.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.remove(u"\u03C0<sub>CV</sub>:")

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Variable Ceramic Capacitor Component Class
            calculation results.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_results_create(self, part, layout,
                                                    x_pos, y_pos)

        # Remove the capacitance correction factor entry.  It is not
        # needed for this type of capacitor.
        layout.remove(part.txtPiCV)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Variable Ceramic Capacitor Component Class.

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
            the Variable Ceramic Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

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
        if(idx == 1):                           # 85C
            Tref = 358.0
        elif(idx == 2):                         # 125C
            Tref = 398.0
        else:                                   # Default
            Tref = 358.0

        _hrmodel['lambdab'] = 0.00224 * ((S / 0.17)**3 + 1) * exp(1.59 * ((Tamb + 273) / Tref)**10.1)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Piston(Capacitor):

    """ Variable Piston Type Capacitor Component Class.
        Covers specification MIL-C-14409.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.17

    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-14409 (PC)"]
    _specsheet = [["", u"125\u00B0C", u"150\u00B0C"]]

    def __init__(self):

        """ Initializes the Variable Piston Type Capacitor Component Class. """

        Capacitor.__init__(self)

        self.subcategory = 56                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 12.0, 7.0, 18.0, 3.0, 4.0, 20.0, 30.0, 32.0,
                     0.5, 18.0, 46.0, 830.0]
        self._piQ = [3.0, 10.0]
        self._lambdab_count =[0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2, 3.3, 2.2, 0.16, 0.93, 3.2, 37.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.remove(u"\u03C0<sub>CV</sub>:")

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Variable Piston Type Capacitor Component Class
            calculation results.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_results_create(self, part, layout,
                                                    x_pos, y_pos)

        # Remove the capacitance correction factor entry.  It is not
        # needed for this type of capacitor.
        layout.remove(part.txtPiCV)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Variable Piston Type Capacitor Component Class.

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
            the Variable Piston Type Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

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
        if(idx == 1):               # 125C
            Tref = 398.0
        elif(idx == 2):             # 150C
            Tref = 423.0
        else:                       # Default
            Tref = 398.0

        _hrmodel['lambdab'] = 0.00000073 * ((S / 0.33)**3 + 1) * exp(12.1 * (Tamb + 273) / Tref)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class AirTrimmer(Capacitor):

    """ Variable Air Trimmer Capacitor Component Class.
        Covers specification MIL-C-92.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.18

    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-92 (CT)"]
    _specsheet = [["", u"85\u00B0C"]]

    def __init__(self):

        """ Initializes the Variable Air Trimmer Capacitor Component Class. """

        Capacitor.__init__(self)

        self.subcategory = 57                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0,
                     0.5, 20.0, 52.0, 950.0]
        self._piQ = [5.0, 20.0]
        self._lambdab_count = [0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0, 8.1, 0.032, 2.5, 8.9, 100.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.remove(u"\u03C0<sub>CV</sub>:")

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Variable Air Trimmer Capacitor Component Class
            calculation results.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_results_create(self, part, layout,
                                                    x_pos, y_pos)

        # Remove the capacitance correction factor entry.  It is not
        # needed for this type of capacitor.
        layout.remove(part.txtPiCV)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Variable Air Trimmer Capacitor Component Class.

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
            the Variable Air Trimmer Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ * piE"

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
            Tref = 358.0
        else:                       # Default
            Tref = 358.0

        _hrmodel['lambdab'] = 0.00000192 * ((S / 0.33)**3 + 1) * exp(10.8 * (Tamb + 273) / Tref)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Gas(Capacitor):

    """ Variable and Fixed Gas or Vacuum Capacitor Component Class.
        Covers specification MIL-C-23183.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.19

    """

    _construction = ["", "Fixed", "Variable"]
    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-23183 (CT)"]
    _specsheet = [["", u"85\u00B0C", u"100\u00B0C", u"125\u00B0C"]]

    def __init__(self):

        """ Initializes the Variable and Fixed Gas or Vacuum Capacitor
            Component Class.

        """

        Capacitor.__init__(self)

        self.subcategory = 58                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piCF = [0.10, 1.0]
        self._piE = [1.0, 3.0, 14.0, 8.0, 27.0, 10.0, 18.0, 70.0, 108.0, 40.0,
                     0.5, 0.0, 0.0, 0.0]
        self._piQ = [3.0, 20.0]
        self._lambdab_count = [0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0, 23.0, 20.0, 0.0, 0.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"
        self._in_labels.append(u"Configuration:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CF</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels[6] = u"\u03C0<sub>CF</sub>:"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation input tab with the
            widgets needed to select inputs for Variable and Fixed Gas or
            Vacuum Capacitor Component Class prediction calculations.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- teh x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Capacitor.assessment_inputs_create(self, part, layout,
                                                   x_pos, y_pos)

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                     self.combo_callback,
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

        part.cmbConstruction.set_active(int(partmodel.get_value(partrow, 16)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Variable and Fixed Gas or Vacuum Capacitor Component Class.

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
            the Variable and Fixed Gas or Vacuum Capacitor Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp, sqrt

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piCF * piQ * piE"

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
            Tref = 358.0
        elif(idx == 2):             # 100C
            Tref = 373.0
        elif(idx == 3):             # 125C
            Tref =398.0
        else:                       # Default
            Tref = 358.0

        _hrmodel['lambdab'] = 0.0112 * ((S / 0.17)**3 + 1) * exp(1.59 * ((Tamb + 273) / Tref)**10.1)

        # Configuration correction factor.
        idx = partmodel.get_value(partrow, 16)
        _hrmodel['piCF'] = self._piCF[idx - 1]

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 70, _hrmodel['piCF'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
