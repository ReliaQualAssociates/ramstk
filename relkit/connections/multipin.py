#!/usr/bin/env python
""" This is the multipin electrical connection class."""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       multipin.py is part of The RelKit Project
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


class Multipin(Connection):
    """
    Multipin Connection Component Class.
    Covers specifications MIL-C-24308, MIL-C-28748, MIL-C-28804,
    MIL-C-83513, MIL-C-83733, MIL-C-5015, MIL-C-26482, MIL-C-28840,
    MIL-C-38999, MIL-C-81511, MIL-C-83723, MIL-C-3607, MIL-C-3643,
    MIL-C-3650, MIL-C-3655, MIL-C-25516, MIL-C-39012, MIL-C-55235,
    MIL-C-55339, MIL-C-3767, MIL-C-22992, MIL-C-49142.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 15.1
    """

    _configuration = ["", _("Rack and Panel"), _("Circular"), _("Power"),
                      _("Coaxial"), _("Triaxial")]
    _awg = ["", u"22", u"20", u"16", u"12"]
    _insert = ["", _("Vitreous Glass"), _("Alumina Ceramic"), _("Polyimide"),
               _("Diallylphtalate"), _("Melamine"), _("Flourosilicone"),
               _("Silicone Rubber"), _("Polysulfone"), _("Epoxy Resin"),
               _("Teflon"), _("Chlorotrifluorethylene"), _("Polyamide"),
               _("Polychloroprene"), _("Polyethylene")]
    _quality = ["", _("MIL-SPEC"), _("Lower")]

    def __init__(self):
        """ Initializes the Multipin Connection Component Class. """

        Connection.__init__(self)

        self.subcategory = 72               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._gauge = [0.989, 0.640, 0.274, 0.100]
        self._piK = [1.0, 1.5, 2.0, 3.0, 4.0]
        self._piE = [[1.0, 1.0, 8.0, 5.0, 13.0, 3.0, 5.0, 8.0, 12.0, 19.0, 0.5,
                      10.0, 27.0, 490.0],
                     [2.0, 5.0, 21.0, 10.0, 27.0, 12.0, 18.0, 17.0, 25.0, 37.0,
                      0.8, 20.0, 54.0, 970.0]]
        self._lambdab_count = [[0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098,
                                0.23, 0.34, 0.37, 0.0054, 0.16, 0.42, 6.8],
                               [0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098,
                                0.23, 0.34, 0.37, 0.0054, 0.16, 0.42, 6.8],
                               [0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098,
                                0.23, 0.34, 0.37, 0.0054, 0.16, 0.42, 6.8],
                               [0.012, 0.015, 0.13, 0.075, 0.21, 0.050, 0.10,
                                0.22, 0.32, 0.38, 0.0061, 0.16, 0.54, 7.3],
                               [0.012, 0.015, 0.13, 0.075, 0.21, 0.050, 0.10,
                                0.22, 0.32, 0.38, 0.0061, 0.16, 0.54, 7.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_("Configuration:"))
        self._in_labels.append(_("Insert Material:"))
        self._in_labels.append(_("Contact Gauge:"))
        self._in_labels.append(_("Amperes per Contact:"))
        self._in_labels.append(_("Mate/Unmate Cycles (per 1000 hours):"))
        self._in_labels.append(_("# of Active Pins:"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub></span>"
        self._out_labels.append(u"\u03C0<sub>K</sub>:")
        self._out_labels.append(u"\u03C0<sub>P</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Multipin Connection Component
        Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
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

        # Create hte Configuration ComboBox.  We store the index value in the
        # construction_id field in the program database.
        part.cmbConfiguration = _widg.make_combo(simple=True)
        for i in range(len(self._configuration)):
            part.cmbConfiguration.insert_text(i, self._configuration[i])
        part.cmbConfiguration.connect('changed',
                                      self._callback_combo,
                                    part, 16)
        layout.put(part.cmbConfiguration, x_pos, y_pos)
        y_pos += 30

        # Create hte Insert Material ComboBox.  We store the index value in the
        # insulation_id field in the program database.
        part.cmbInsert = _widg.make_combo(simple=True)
        for i in range(len(self._insert)):
            part.cmbInsert.insert_text(i, self._insert[i])
        part.cmbInsert.connect('changed',
                               self._callback_combo,
                               part, 38)
        layout.put(part.cmbInsert, x_pos, y_pos)
        y_pos += 30

        # Create the Contact Gauge Entry.  We store the index value in the
        # cycles_id field in the program database.
        part.cmbContactGauge = _widg.make_combo(simple=True)
        for i in range(len(self._awg)):
            part.cmbContactGauge.insert_text(i, self._awg[i])
        part.cmbContactGauge.connect('changed',
                                     self._callback_combo,
                                     part, 18)
        layout.put(part.cmbContactGauge, x_pos, y_pos)
        y_pos += 30

        # Create the Amperes per Contact Entry.  We store the index value in
        # the s2 field in the program database.
        part.txtAmpsContact = _widg.make_entry()
        part.txtAmpsContact.connect('focus-out-event',
                                    self._callback_entry,
                                    part, 'float', 98)
        layout.put(part.txtAmpsContact, x_pos, y_pos)
        y_pos += 30

        # Create the Mate/Demate Cycles Entry.  We store the index value in the
        # s3 field in the program database.
        part.txtMateCycles = _widg.make_entry()
        part.txtMateCycles.connect('focus-out-event',
                                   self._callback_entry,
                                   part, 'float', 99)
        layout.put(part.txtMateCycles, x_pos, y_pos)
        y_pos += 30

        part.txtActivePins = _widg.make_entry()
        part.txtActivePins.connect('focus-out-event',
                                   self._callback_entry,
                                   part, 'float', 60)
        layout.put(part.txtActivePins, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        Connection.assessment_inputs_load(self, part)

        part.cmbConfiguration.set_active(int(partmodel.get_value(partrow, 16)))
        part.cmbInsert.set_active(int(partmodel.get_value(partrow, 38)))
        part.cmbContactGauge.set_active(int(partmodel.get_value(partrow, 18)))
        part.txtAmpsContact.set_text(str(fmt.format(partmodel.get_value(partrow, 98))))
        part.txtMateCycles.set_text(str(fmt.format(partmodel.get_value(partrow, 99))))
        part.txtActivePins.set_text(str('{0:0.0g}'.format(partmodel.get_value(partrow, 60))))

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Mulitpin Connection Component Class calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
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

        part.txtPiK = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiK, x_pos, y_pos)
        y_pos += 30

        # Create the piP Entry.  We store this value in the piPT field in the
        # program database.
        part.txtPiP = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiP, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        Connection.assessment_results_load(self, part)

        part.txtPiK.set_text(str('{0:0.2g}'.format(partmodel.get_value(partrow, 75))))
        part.txtPiP.set_text(str(fmt.format(partmodel.get_value(partrow, 78))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Mulitpin Connection Component Class.

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
        Cidx = partmodel.get_value(partrow, 16)         # Configuration index
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Qidx = partmodel.get_value(partrow, 85)         # Quality index

        _hrmodel['lambdab'] = self._lambdab_count[Cidx - 1][Eidx - 1]

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
        the Multipin Connection Component Class.

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
        _hrmodel['equation'] = 'lambdab * piK * piP * piE'

        # Retrieve temperature rise inputs.
        Gidx = partmodel.get_value(partrow, 18)         # Contact gauge index
        i = partmodel.get_value(partrow, 98)            # Amps per contact

        # Retrieve hazard rate inputs.
        Cidx = partmodel.get_value(partrow, 16)         # Configuration index
        Iidx = partmodel.get_value(partrow, 38)         # Insert index
        N = partmodel.get_value(partrow, 60)            # Number of active pins
        Qidx = partmodel.get_value(partrow, 85)
        cycles = partmodel.get_value(partrow, 99)       # Mate/Demate cycles

        # Temperature rise.
        K = self._gauge[Gidx - 1]
        To = K * i**1.85

        # Base hazard rate.
        if(Iidx > 1 and Iidx < 4):
            _hrmodel['lambdab'] = 0.020 * exp((-1592.0 / (To + 273.0)) + (((To + 273.0) / 473.0)**5.36))
        elif(Iidx > 3 and Iidx < 10):
            _hrmodel['lambdab'] = 0.431 * exp((-2073.6 / (To + 273.0)) + (((To + 273.0) / 423.0)**4.66))
        elif(Iidx > 9 and Iidx < 13):
            _hrmodel['lambdab'] = 0.190 * exp((-1298.0 / (To + 273.0)) + (((To + 273.0) / 373.0)**4.25))
        elif(Iidx > 12 and Iidx < 16):
            _hrmodel['lambdab'] = 0.770 * exp((-1528.8 / (To + 273.0)) + (((To + 273.0) / 358.0)**4.72))
        else:
            _hrmodel['lambdab'] = 0.0

        # Mate/Unmate correction factor.
        if(cycles <= 0.05):
            _hrmodel['piK'] = 1.0
        elif(cycles > 0.05 and cycles <= 0.5):
            _hrmodel['piK'] = 1.5
        elif(cycles > 0.5 and cycles <= 5):
            _hrmodel['piK'] = 2.0
        elif(cycles > 5 and cycles <= 50):
            _hrmodel['piK'] = 3.0
        else:
            _hrmodel['piK'] = 4.0

        # Active pins correction factor.
        if(N >= 2):
            _hrmodel['piP'] = exp(((N - 1) / 10)**0.51064)
        else:
            _hrmodel['piP'] = 0.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[Qidx - 1][idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 75, _hrmodel['piK'])
        partmodel.set_value(partrow, 78, _hrmodel['piP'])
        partmodel.set_value(partrow, 107, To)

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
