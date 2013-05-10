#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       thumbwheel.py is part of The RelKit Project
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

class Thumbwheel(Switch):
    """
    Thumbwheel Switch Component Class.
    Covers specifications MIL-S-22710.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 14.4
    """

    _application = ["", u"Resistive", u"Inductive", u"Lamp"]
    _quality = ["", u"MIL-SPEC", u"Lower"]

    def __init__(self):
        """
        Initializes the Toggle or Pushbutton Switch Component Class.
        """

        Switch.__init__(self)

        self.subcategory = 70                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0,
                     0.5, 25.0, 67.0, 1200.0]
        self._lambdab_count = [0.56, 1.7, 10.0, 4.5, 16.0, 5.6, 10.0, 7.3,
                               12.0, 26.0, 0.26, 14.0, 38.0, 670.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"# of Active Contacts:")

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> + \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
        self._out_labels[1] = u"\u03BB<sub>b1</sub>:"
        self._out_labels.append(u"\u03C0<sub>N</sub>:")
        self._out_labels.append(u"\u03BB<sub>b2</sub>:")
        self._out_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>L</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the widgets
        needed to select inputs for Toggle or Pushbutton Switch Component Class
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Switch.assessment_inputs_create(self, part, layout,
                                                x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtActiveContacts = _widg.make_entry(_width_=entry_width)
        part.txtActiveContacts.connect("focus-out-event",
                                       self.entry_callback,
                                       part, "int", 57)
        layout.put(part.txtActiveContacts, x_pos, y_pos)

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

        # Create the piN Entry.  This value is stored in the pi_m field in the
        # program database.
        part.txtPiN = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiN, x_pos, y_pos)
        y_pos += 30

        part.txtLambdaB2 = _widg.make_entry(_width_=entry_width,
                                            editable=False, bold=True)
        layout.put(part.txtLambdaB2, x_pos, y_pos)
        y_pos += 30

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

        part.txtActiveContacts.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 57))))

        return False

    def assessment_results_load(self, part):

        """ Loads the RelKit Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Switch.assessment_results_load(self, part)

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 48))))
        part.txtLambdaB2.set_text(str(fmt.format(part.model.get_value(part.selected_row, 49))))
        part.txtPiCYC.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 71))))
        part.txtPiN.set_text(str("{0:0.0g}".format(part.model.get_value(part.selected_row, 76))))
        part.txtPiL.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))

        return False

    def calculate_mil_217_count(self, part):

        """ Performs MIL-HDBK-217F part count hazard rate calculations for the
            Thumbwheel Switch Component Class.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        part._hrmodel = {}
        part._hrmodel['equation'] = "lambdab * piQ"

        model = part.model
        row = part.selected_row

        # Retrieve hazard rate inputs.
        Qidx = model.get_value(row, 85)
        Eidx = part._app.HARDWARE.model.get_value(part._app.HARDWARE.selected_row, 22)

        part._hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        if(Qidx == 1):
            part._hrmodel['piQ'] = 1.0
        else:
            part._hrmodel['piQ'] = 10.0

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
        part._hrmodel['equation'] = "(lambdab1 + piN * lambdab2) * piCYC * piL * piE"

        model = part.model
        row = part.selected_row

        # Retrieve hazard rate inputs.
        Aidx = model.get_value(row, 5)
        Cycles = model.get_value(row, 19)
        part._hrmodel['piN'] = model.get_value(row, 57)
        Ioper = model.get_value(row, 62)
        Qidx = model.get_value(row, 85)
        Irated = model.get_value(row, 92)

        # Base hazard rate.
        if(Qidx == 1):
            part._hrmodel['lambdab1'] = 0.0067
            part._hrmodel['lambdab2'] = 0.062
        else:
            part._hrmodel['lambdab1'] = 0.086
            part._hrmodel['lambdab2'] = 0.089

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

        model.set_value(row, 48, part._hrmodel['lambdab1'])
        model.set_value(row, 49, part._hrmodel['lambdab2'])
        model.set_value(row, 71, part._hrmodel['piCYC'])
        model.set_value(row, 72, part._hrmodel['piE'])
        model.set_value(row, 76, part._hrmodel['piN'])
        model.set_value(row, 82, part._hrmodel['piL'])

        model = part._app.HARDWARE.model
        row = part._app.HARDWARE.selected_row

        model.set_value(row, 28, lambdap)
        model.set_value(row, 88, list(part._hrmodel.items()))

        part._assessment_results_tab_load()

        return False
