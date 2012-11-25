#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       breaker.py is part of The ReliaFree Project
#
#       Copyright 2007-2012 Andrew "Weibullguy" Rowland <darowland@ieee.org>
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except:
    import calculations as _calc
    import widgets as _widg

from switch import Switch

class Breaker(Switch):

    """ Circuit Breaker Switch Component Class.
        Covers specifications MIL-C-55629, MIL-C-83383, MIL-C-39019, and
        W-C-375.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 14.1

    """

    _application = ["", u"Not Used as Power On/Off Switch",
                    u"Used as Power On/Off Switch"]
    _construction = ["", u"Magnetic", u"Thermal", u"Thermal-Magnetic"]
    _form = ["", u"SPST", u"DPST", u"3PST", u"4PST"]
    _quality = ["", u"MIL-SPEC", u"Lower"]

    def __init__(self):

        """ Initializes the Circuit Breaker Switch Component Class. """

        Switch.__init__(self)

        self.subcategory = 71                   # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [1.0, 2.0, 3.0, 4.0]
        self._piE = [1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0,
                     0.5, 25.0, 67.0, 0.0]
        self._piQ = [1.0, 8.4]
        self._piU = [1.0, 10.0]
        self._lambdab = [0.020, 0.038, 0.038]
        self._lambdab_count = [0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66,
                               0.72, 2.8, 0.030, 1.5, 4.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Construction:")
        self._in_labels.append(u"Contact Form:")

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>:")
        self._out_labels.append(u"\u03C0<sub>U</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the ReliaFree Workbook calculation input tab with the
            widgets needed to select inputs for Circuit Breaker Switch
            Component Class prediction calculations.

            Keyword Arguments:
            part   -- the ReliaFree COMPONENT object.
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
        y_pos == 30

        # Create the contact form ComboBox.  We store the index value in the
        # func_id field in the program database.
        part.cmbForm = _widg.make_combo(simple=True)
        for i in range(len(self._form)):
            part.cmbForm.insert_text(i, self._form[i])
        part.cmbForm.connect("changed",
                             self.combo_callback,
                             part, 30)
        layout.put(part.cmbForm, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the ReliaFree Workbook calculation results tab with the
            widgets to display Circuit Breaker Switch Component Class
            calculation results.

            Keyword Arguments:
            part   -- the ReliaFree COMPONENT object.
            layout -- the layout widget to contain the display widgets.
            x_pos  -- the x position of the widgets.
            y_pos  -- the y position of the first widget.
        """

        y_pos = Switch.assessment_results_create(self, part, layout,
                                                 x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiC = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)
        y_pos += 30

        part.txtPiU = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiU, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):

        """ Loads the ReliaFree Workbook calculation input widgets with
            calculation input information.

            Keyword Arguments:
            part -- the ReliaFree COMPONENT object.
        """

        Switch.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.cmbForm.set_active(int(part.model.get_value(part.selected_row, 30)))

        return False

    def assessment_results_load(self, part):

        """ Loads the ReliaFree Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the ReliaFree COMPONENT object.
        """

        Switch.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 69))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))
        part.txtPiU.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 82))))

        return False

    def calculate_mil_217_count(self, part):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Circuit Breaker Switch Component Class.

            Keyword Arguments:
            part -- the ReliaFree COMPONENT object.
        """

        part._hrmodel = {}
        part._hrmodel['equation'] = "lambdab * piQ"

        model = part.model
        row = part.selected_row

        # Retrieve hazard rate inputs.
        Qidx = model.get_value(row, 85)
        Eidx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)              # Environment index

        part._hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        if(Qidx == 1):
            part._hrmodel['piQ'] = 1.0
        else:
            part._hrmodel['piQ'] = 8.4

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
            the Circuit Breaker Switch Component Class.

            Keyword Arguments:
            part -- the ReliaFree COMPONENT object.
        """

        from math import exp

        part._hrmodel = {}
        part._hrmodel['equation'] = "lambdab * piC * piU * piQ * piE"

        model = part.model
        row = part.selected_row

        # Retrieve hazard rate inputs.
        Aidx = model.get_value(row, 5)
        Cidx = model.get_value(row, 16)
        Fidx = model.get_value(row, 30)
        Qidx = model.get_value(row, 85)

        # Base hazard rate.
        part._hrmodel['lambdab'] = self._lambdab[Cidx - 1]

        # Quality correction factor.
        part._hrmodel['piQ'] = self._piQ[Qidx - 1]

        # Contact for correction factor.
        part._hrmodel['piC'] = self._piC[Fidx - 1]

        # Usage correction factor.
        part._hrmodel['piU'] = self._piU[Aidx - 1]

        # Environmental correction factor.
        idx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)
        part._hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(part._hrmodel)

        model.set_value(row, 46, part._hrmodel['lambdab'])
        model.set_value(row, 69, part._hrmodel['piC'])
        model.set_value(row, 72, part._hrmodel['piE'])
        model.set_value(row, 79, part._hrmodel['piQ'])
        model.set_value(row, 82, part._hrmodel['piU'])

        model = part._app.HARDWARE.model
        row = part._app.HARDWARE.selected_row

        model.set_value(row, 28, lambdap)
        model.set_value(row, 88, list(part._hrmodel.items()))

        part._assessment_results_tab_load()

        return False
