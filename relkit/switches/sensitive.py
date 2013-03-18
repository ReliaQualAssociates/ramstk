#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sensitive.py is part of The RelKit Project
#
#       Copyright 2007-2013 Andrew "Weibullguy" Rowland <darowland@ieee.org>
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

class Sensitive(Switch):

    """ Basic Sensitive Switch Component Class.
        Covers specifications MIL-S-8805

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 14.2.

    """

    _application = ["", u"Resistive", u"Inductive", u"Lamp"]
    _quality = ["", u"MIL-SPEC", u"Lower"]

    def __init__(self):

        """ Initializes the Basic Sensitive Switch Component Class. """

        Switch.__init__(self)

        self.subcategory = 68                   # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 18.0, 8.0, 29.0, 10.0, 18.0, 13.0, 22.0, 46.0,
                     0.5, 25.0, 67.0, 1200.0]
        self._lambdab_count = [0.15, 0.44, 2.7, 1.2, 4.3, 1.5, 2.7, 1.9, 3.3,
                               6.8, 0.74, 3.7, 9.9, 180.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"# of Active Contacts:")
        self._in_labels.append(u"Actuation Differential (in):")

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._out_labels.append(u"\u03C0<sub>L</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation input tab with the
            widgets needed to select inputs for Basic Sensitive Switch
            Component Class prediction calculations.

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
        y_pos += 30

        # Create the Actuation Differential Entry.  This is stored in the
        # K1 field in the program database.
        part.txtActuationDiff = _widg.make_entry(_width_=entry_width)
        part.txtActuationDiff.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 40)
        layout.put(part.txtActuationDiff, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Basic Sensitive Switch Component Class
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

        fmt = "{0:0.}" + str(part.fmt) + "g}"

        Switch.assessment_inputs_load(self, part)

        part.txtActuationDiff.set_text(str(fmt.format(treemodel.get_value(row, 40))))
        part.txtActiveContacts.set_text(str("{0:0.0g}".format(treemodel.get_value(row, 57))))

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
            Basic Sensitive Switch Component Class.

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
            part._hrmodel['piQ'] = 20.0

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
            the Basic Sensitive Switch Component Class.

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
        AD = model.get_value(row, 40)
        n = model.get_value(row, 57)
        Ioper = model.get_value(row, 62)
        Qidx = model.get_value(row, 85)
        Irated = model.get_value(row, 92)

        if(AD > 0.002 and Qidx == 1):
            lambda_b = 0.00045
        elif(AD > 0.002 and Qidx == 2):
            lambda_b = 0.23
        elif(AD <= 0.002 and Qidx == 1):
            lambda_b = 0.0009
        elif(AD <= 0.002 and Qidx == 2):
            lambda_b = 0.63
        else:
            lambda_b = 0.23

        # Base hazard rate.
        part._hrmodel['lambdab'] = 0.10 + n * lambda_b

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
