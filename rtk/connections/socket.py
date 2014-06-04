#!/usr/bin/env python
""" This is the IC Socket connection class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       socket.py is part of The RTK Project
#
# All rights reserved.

import pango

try:
    import relkit.calculations as _calc
    import relkit.configuration as _conf
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext

from connection import Connection


class ICSocket(Connection):
    """
    IC Socket Connection Component Class.
    Covers specifications MIL-S-83734.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 15.3.
    """

    _quality = ["", _("MIL-SPEC"), _("Lower")]

    def __init__(self):
        """ Initializes the IC Socket Connection Component Class. """

        Connection.__init__(self)

        self.subcategory = 74                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 14.0, 6.0, 18.0, 8.0, 12.0, 11.0, 13.0, 25.0,
                     0.5, 14.0, 36.0, 650.0]
        self._lambdab_count = [0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015,
                               0.023, 0.021, 0.025, 0.048, 0.00097, 0.027,
                               0.070, 1.3]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_("# of Active Contacts:"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub>\u03C0<sub>P</sub></span>"
        self._out_labels.append(u"\u03C0<sub>P</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for IC Socket Connection Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the RTK COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        try:
            treemodel = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        y_pos = Connection.assessment_inputs_create(self, part, layout,
                                                    x_pos, y_pos)

        part.txtActiveContacts = _widg.make_entry()
        part.txtActiveContacts.connect('focus-out-event',
                                       self._callback_entry,
                                       part, 'float', 57)
        layout.put(part.txtActiveContacts, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display IC Socket Connection Component Class
        calculation results.

        Keyword Arguments:
        part   -- the RTK COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        try:
            treemodel = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        y_pos = Connection.assessment_results_create(self, part, layout,
                                                     x_pos, y_pos)

        # Create the piP Entry.  We store this value in the piPT field in the
        # program database.
        part.txtPiP = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiP, x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RTK COMPONENT object.
        """

        Connection.assessment_inputs_load(self, part)

        num_contacts = part.model.get_value(part.selected_row, 57)
        part.txtActiveContacts.set_text(str('{0:0.0g}'.format(num_contacts)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RTK COMPONENT object.
        """

        Connection.assessment_results_load(self, part)

        fmt = '{0:0.' + str(part.fmt) + 'g}'

        pip = part.model.get_value(part.selected_row, 78)
        part.txtPiP.set_text(str(fmt.format(pip)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        IC Socket Connection Component Class.

        Keyword Arguments:
        partmodel   -- the RTK winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RTK HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RTK HARWARE
                       object gtk.TreeModel.
        """

        _hrmodel = {}
        _hrmodel['equation'] = 'lambdab * piQ'

        # Retrieve hazard rate inputs.
        Qidx = partmodel.get_value(partrow, 85)         # Quality index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        if(Qidx == 1):
            _hrmodel['piQ'] = 1.0
        else:
            _hrmodel['piQ'] = 2.0

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
        the IC Socket Connection Component Class.

        Keyword Arguments:
        partmodel   -- the RTK winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RTK HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RTK HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = 'lambdab * piP * piE'

        # Retrieve hazard rate inputs.
        N = partmodel.get_value(partrow, 57)                 # Number of active pins
        Qidx = partmodel.get_value(partrow, 85)              # Quality index

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.00042

        # Active pins correction factor.
        if(N - 1 > 0):
            _hrmodel['piP'] = exp(((N - 1) / 10)**0.51064)
        else:
            _hrmodel['piP'] = 0.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 78, _hrmodel['piP'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
