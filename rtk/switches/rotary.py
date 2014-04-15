#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rotary.py is part of The RelKit Project
#
#       Copyright 2007-2013 Andrew "Weibullguy" Rowland <darowland@ieee.org>
#
# All rights reserved.

import pango

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except:
    import calculations as _calc
    import widgets as _widg

from switch import Switch

class Rotary(Switch):

    """ Rotary Switch Component Class.
        Covers specifications MIL-S-3786.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 14.3.

    """

    _application = ["", u"Resistive", u"Inductive", u"Lamp"]
    _construction = ["", u"Ceramic RF Wafers", u"Medium Power Wafers"]
    _quality = ["", u"MIL-SPEC", u"Lower"]

    def __init__(self):

        """ Initializes the Rotary Switch Component Class. """

        Switch.__init__(self)

        self.subcategory = 69                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0,
                     0.5, 25.0, 67.0, 1200.0]
        self._lambdab_count = [0.33, 0.99, 5.9, 2.6, 9.5, 3.3, 5.9, 4.3, 7.2,
                               15.0, 0.16, 8.2, 22.0, 390.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Construction:")

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>L</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation input tab with the
            widgets needed to select inputs for Rotary Switch Component Class
            prediction calculations.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Switch.assessment_inputs_create(self, part, layout,
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

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Toggle and Pushbutton Switch Component Class
            calculation results.

            Keyword Arguments:
            part   -- the RelKit COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Switch.assessment_results_create(self, part, layout,
                                                 x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiCYC = _widg.make_entry(_width_=entry_width,
                                         editable=False, bold=True)
        layout.put(part.txtPiCYC, x_pos, y_pos)
        y_pos += 30

        # Create the piL Entry.  This value is stored in the pi_u field in the
        # program database.
        part.txtPiL = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiL, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):

        """ Loads the RelKit Workbook calculation input widgets with
            calculation input information.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        Switch.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))

        return False

    def assessment_results_load(self, part):

        """ Loads the RelKit Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Switch.assessment_results_load(self, part)

        part.txtPiCYC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 71))))
        part.txtPiL.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))

        return False

    def calculate_mil_217_count(self, part):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Rotary Switch Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        part._hrmodel = {}
        part._hrmodel['equation'] = "lambdab * piQ"

        model = part.model
        row = part.selected_row

        # Retrieve hazard rate inputs.
        Qidx =model.get_value(row, 85)
        Eidx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)              # Environment index

        part._hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        if(Qidx == 1):
            part._hrmodel['piQ'] = 1.0
        else:
            part._hrmodel['piQ'] = 50.0

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(part._hrmodel)

        model.set_value(row, 46, part._hrmodel['lambdab'])

        model = part._app.HARDWARE.model
        row = part._app.HARDWARE.selected_row

        model.set_value(row, 28, lambdap)
        model.set_value(row, 88, list(part._hrmodel.items()))

        part._assessment_results_tab_load()

        return False

    def calculate_mil_217_stress(self, part):

        """ Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Toggle or Pushbutton Switch Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        from math import exp

        part._hrmodel = {}
        part._hrmodel['equation'] = "lambdab * piCYC * piL * piE"

        model = part.model
        row = part.selected_row

        # Retrieve hazard rate inputs.
        Aidx = model.get_value(row, 5)
        Cidx = model.get_value(row, 16)
        Cycles = model.get_value(row, 19)
        n = model.get_value(row, 40)
        Ioper = model.get_value(row, 62)
        Qidx = model.get_value(row, 85)
        Irated = model.get_value(row, 92)

        # Base hazard rate.
        if(Qidx == 1):
            lambda_be = 0.0067
            if(Cidx == 1):
                lambda_b = 0.00003
            else:
                lambda_b = 0.00003
        elif(Qidx == 2):
            lambda_be = 0.10
            if(Cidx == 1):
                lambda_b = 0.02
            else:
                lambda_b = 0.06
        else:
            lambda_be = 0.10
            lambda_b = 0.06

        part._hrmodel['lambdab'] = lambda_be + n * lambda_b

        # Cycling Rate correction factor.
        if(Cycles <= 1.0):
            part._hrmodel['piCYC'] = 1.0
        else:
            part._hrmodel['piCYC'] = Cycles

        # Load Stress correction factor.
        if(Aidx == 1):                          # Resistive
            K = 0.8
        elif(Aidx == 2):                        # Inductive
            K = 0.4
        elif(Aidx == 3):                        # Lamp
            K = 0.2
        else:                                   # Default
            K = 1.0

        S = Ioper / Irated
        part._hrmodel['piL'] = exp((S / K) ** 2)

        # Environmental correction factor.
        idx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)
        part._hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(part._hrmodel)

        model.set_value(row, 46, part._hrmodel['lambdab'])
        model.set_value(row, 71, part._hrmodel['piCYC'])
        model.set_value(row, 72, part._hrmodel['piE'])
        model.set_value(row, 82, part._hrmodel['piL'])

        model = part._app.HARDWARE.model
        row = part._app.HARDWARE.selected_row

        model.set_value(row, 28, lambdap)
        model.set_value(row, 88, list(part._hrmodel.items()))

        part._assessment_results_tab_load()

        return False
