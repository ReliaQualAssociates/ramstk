#!/usr/bin/env python
""" This is the electric fuse class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       fuse.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg


class Fuse:
    """
    Fuse Component Class.
    Covers specifications MIL-F-5372, MIL-F-23419, MIL-F-15160, W-F-1726,
    and W-F-1814.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 22.1
    """

    def __init__(self):
        """ Initializes the Fuse Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 10                      # Category in reliafreecom database.
        self.subcategory = 82                   # Subcategory in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 8.0, 5.0, 11.0, 9.0, 12.0, 15.0, 18.0, 16.0,
                     0.9, 10.0, 21.0, 230.0]
        self._lambdab_count = [0.01, 0.02, 0.06, 0.05, 0.11, 0.09, 0.12, 0.15,
                               0.18, 0.16, 0.009, 0.1, .021, 2.3]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels.append(u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Fuse Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Fuse Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is LAMP,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels.
        y_pos = 305
        numlabels = len(self._out_labels)
        for i in range(numlabels):
            if(i == 2):
                label = _widg.make_label(self._out_labels[i], width=400)
                llayout = label.get_layout()
                llayout.set_alignment(pango.ALIGN_CENTER)
                label.show_all()
            else:
                label = _widg.make_label(self._out_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        y_pos += 30
        part.txtLambdaB = _widg.make_entry(_width_=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)

        layout.show_all()

        self._ready = True

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Fuse Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab"

        # Retrieve hazard rate inputs.
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
        the Fuse Component Class.

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
        _hrmodel['equation'] = "lambdab * piE"

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.01

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
