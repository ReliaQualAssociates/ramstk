#!/usr/bin/env python
""" This is the solder connection class. """
__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       solder.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import reliafree.calculations as _calc
    import reliafree.configuration as _conf
    import reliafree.widgets as _widg
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

class PTH(Connection):
    """
    Plated Through Hole Connection Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 16.1.
    """

    _technology = [u"", _("Printed Wiring Assembly with PTHs"),
                   _("Discrete Wiring with Electroless Deposited PTH")]
    _quality = ["", _("MIL-SPEC"), _("Lower")]

    def __init__(self):
        """ Initializes the Plated Through Hole Connection Component Class. """

        Connection.__init__(self)

        self.subcategory = 75               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [0.00041, 0.00026]
        self._piE = [1.0, 2.0, 7.0, 5.0, 13.0, 5.0, 8.0, 16.0, 28.0, 19.0,
                     0.5, 10.0, 27.0, 500.0]
        self._piQ = [1.0, 2.0]
        self._lambdab_count = [0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 043, 0.85,
                               1.5, 1.0, 0.027, 0.53, 1.4, 27.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_("Technology:"))
        self._in_labels.append(_("# of Circuit Planes:"))
        self._in_labels.append(_("# of Wave Soldered PTH:"))
        self._in_labels.append(_("# of Hand Soldered PTH:"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>[N<sub>1</sub>\u03C0<sub>C</sub> + N<sub>2</sub>(\u03C0<sub>C</sub> + 13)]\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation input tab with the
        widgets needed to select inputs for Plated Through Hole Connection
        Component Class prediction calculations.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
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

        part.cmbTechnology = _widg.make_combo(simple=True)
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])
        part.cmbTechnology.connect('changed',
                                   self._callback_combo,
                                   part, 104)
        layout.put(part.cmbTechnology, x_pos, y_pos)
        y_pos += 30

        # Create the Number of Circuit Planes Entry.  We store this value
        # in the number_elements field in the program database.
        part.txtNumberPlanes = _widg.make_entry()
        part.txtNumberPlanes.connect('focus-out-event',
                                     self._callback_entry,
                                     part, 'float', 58)
        layout.put(part.txtNumberPlanes, x_pos, y_pos)
        y_pos += 30

        part.txtNumberWave = _widg.make_entry()
        part.txtNumberWave.connect('focus-out-event',
                                   self._callback_entry,
                                   part, 'float', 61)
        layout.put(part.txtNumberWave, x_pos, y_pos)
        y_pos += 30

        part.txtNumberHand = _widg.make_entry()
        part.txtNumberHand.connect('focus-out-event',
                                   self._callback_entry,
                                   part, 'float', 59)
        layout.put(part.txtNumberHand, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the ReliaFree Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        Connection.assessment_inputs_load(self, part)

        part.cmbTechnology.set_active(int(part.model.get_value(part.selected_row, 104)))
        part.txtNumberPlanes.set_text(str('{0:0.0g}'.format(part.model.get_value(part.selected_row, 58))))
        part.txtNumberWave.set_text(str('{0:0.0g}'.format(part.model.get_value(part.selected_row, 61))))
        part.txtNumberHand.set_text(str('{0:0.0g}'.format(part.model.get_value(part.selected_row, 59))))

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation results tab with the
        widgets to display Plated Through Hole Connection Component Class
        calculation results.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
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

        part.txtPiC = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiC, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_load(self, part):
        """
        Loads the ReliaFree Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        Connection.assessment_results_load(self, part)

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        part.txtPiC.set_text(str(fmt.format(part.model.get_value(part.selected_row, 69))))
        part.txtPiQ.set_text(str('{0:0.2g}'.format(part.model.get_value(part.selected_row, 79))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Plated Through Hole Connection Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        _hrmodel = {}
        _hrmodel['equation'] = 'lambdab * piQ'

        # Retrieve hazard rate inputs.
        Qidx = partmodel.get_value(partrow, 85)         # Quality index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        #TODO: Lookup base hazard rate for PTH in MIL-HDBK-217.
        _hrmodel['lambdab'] = 1.0

        if(Qidx == 1):
            _hrmodel['piQ'] = 1.0
        else:
            _hrmodel['piQ'] = 20.0

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
        the Plated Through Hole Connection Component Class.

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
        _hrmodel['equation'] = 'lambdab * (N1 * piC + N2 * (piC + 13.0)) * piQ * piE'

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)
        P = partmodel.get_value(partrow, 58)
        _hrmodel['N2'] = partmodel.get_value(partrow, 59)
        _hrmodel['N1'] = partmodel.get_value(partrow, 61)
        Qidx = partmodel.get_value(partrow, 85)
        Tidx = partmodel.get_value(partrow, 104)

        # Base hazard rate.
        _hrmodel['lambdab'] = self._lambdab[Tidx - 1]

        # Complexity correction factor.
        if(Tidx == 1 and P > 1):
            _hrmodel['piC'] = 0.65 * P**0.63
        else:
            _hrmodel['piC'] = 1.0

        # Quality correction factor.
        _hrmodel['piQ'] = self._piQ[Qidx - 1]

        # Environmental correction factor.
        _hrmodel['piE'] = self._piE[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 69, _hrmodel['piC'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 79, _hrmodel['piQ'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class Solder(Connection):
    """
    Non-Plated Through Hole Connection Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 16.1.
    """

    _technology = [u"", _("Printed Wiring Assembly with PTHs"),
                   _("Discrete Wiring with Electroless Deposited PTH")]
    _quality = ["", _("All")]

    def __init__(self, type):
        """ Initializes the Solder Connection Component Class. """

        Connection.__init__(self)

        if(type == 1):
            self.subcategory = 76           # Subcategory ID in reliafreecom database.
            self._lambdab = 0.00012
            self._piQ = [1.0]
            self._lambdab_count = [0.00012, 0.00024, 0.00084, 0.00048, 0.0013,
                                   0.00048, 0.00072, 0.00072, 0.00096, 0.0019,
                                   0.00005, 0.0011, 0.0029, 0.050]
        elif(type == 2):
            self._quality = [u"", _("Automated with Daily Pull Test"),
                             _("Manual, MIL-SPEC Tools with Two Pull Test"),
                             _("Manual, MIL-SPEC Tools with One Pull Test"),
                             _("Lower")]
            self.subcategory = 83           # Subcategory ID in reliafreecom database.
            self._lambdab = 0.00026
            self._piQ = [1.0, 1.0, 2.0, 20.0]
            self._lambdab_count = [0.00026, 0.00052, 0.0018, 0.0010, 0.0029,
                                   0.0010, 0.0016, 0.0016, 0.0021, 0.0042,
                                   0.00013, 0.0023, 0.0062, 0.11]
        elif(type == 3):
            self.subcategory = 84           # Subcategory ID in reliafreecom database.
            self._lambdab = 0.0026
            self._piQ = [1.0]
            self._lambdab_count = [0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010,
                                   0.016, 0.016, 0.021, 0.042, 0.0013, 0.023,
                                   0.062, 1.1]
        elif(type == 8):
            self.subcategory = 85           # Subcategory ID in reliafreecom database.
            self._lambdab = 0.000069
            self._piQ = [1.0]
            self._lambdab_count = [0.000069, 0.000138, 0.000483, 0.000276,
                                   0.000759, 0.000276, 0.000414, 0.000414,
                                   0.000552, 0.001104, 0.000035, 0.000621,
                                   0.001656, 0.02898]
        elif(type == 9):
            self.subcategory = 86           # Subcategory ID in reliafreecom database.
            self._lambdab = 0.00005
            self._piQ = [1.0]
            self._lambdab_count = [0.000050, 0.000100, 0.000350, 0.000200,
                                   0.000550, 0.000200, 0.000300, 0.000300,
                                   0.000400, 0.000800, 0.000025, 0.000450,
                                   0.001200, 0.021000]
        elif(type == 10):
            self.subcategory = 87           # Subcategory ID in reliafreecom database.
            self._lambdab = 0.00014
            self._piQ = [1.0]
            self._lambdab_count = [0.00014, 0.00028, 0.00096, 0.00056, 0.0015,
                                   0.00056, 0.00084, 0.00084, 0.0011, 0.0022,
                                   0.00007, 0.0013, 0.0034, 0.059]

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 7.0, 4.0, 11.0, 4.0, 6.0, 6.0, 8.0, 16.0, 0.5,
                     9.0, 24.0, 420.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the ReliaFree Workbook calculation results tab with the
        widgets to display Non-Plated Through Hole Connection Component
        Class calculation results.

        Keyword Arguments:
        part   -- the ReliaFree COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        try:
            treemodel = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        Connection.assessment_results_create(self, part, layout,
                                             x_pos, y_pos)

        part.txtPiQ = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)

        return False

    def assessment_results_load(self, part):
        """
        Loads the ReliaFree Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the ReliaFree COMPONENT object.
        """

        Connection.assessment_results_load(self, part)

        part.txtPiQ.set_text(str('{0:0.2g}'.format(partmodel.get_value(partrow, 79))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Non-Plated Through Hole Connection Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        _hrmodel = {}
        _hrmodel['equation'] = 'lambdab'

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

        #TODO: Lookup lammbda_b in MIL-HDBK-217.
        _hrmodel['equation'] = 1.0

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
        the Non-Plated Through Hole Connection Component Class.

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
        _hrmodel['equation'] = 'lambdab * piQ * piE'

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)
        Qidx = partmodel.get_value(partrow, 85)

        # Base hazard rate.
        _hrmodel['lambdab'] = self._lambdab

        # Quality correction factor.
        _hrmodel['piQ'] = self._piQ[Qidx - 1]

        # Environmental correction factor.
        _hrmodel['piE'] = self._piE[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 79, _hrmodel['piQ'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
