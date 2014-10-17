#!/usr/bin/env python
"""
This is the multipin electrical connection class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       multipin.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

try:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
from connection import Connection

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Multipin(Connection):
    """
    Multipin Connection Component Class.
    Covers specifications MIL-C-24308, MIL-C-28748, MIL-C-28804,
    MIL-C-83513, MIL-C-83733, MIL-C-5015, MIL-C-26482, MIL-C-28840,
    MIL-C-38999, MIL-C-81511, MIL-C-83723, MIL-C-3607, MIL-C-3643,
    MIL-C-3650, MIL-C-3655, MIL-C-25516, MIL-C-39012, MIL-C-55235,
    MIL-C-55339, MIL-C-3767, MIL-C-22992, MIL-C-49142.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 15.1
    """

    _configuration = ["", _(u"Rack and Panel"), _(u"Circular"), _(u"Power"),
                      _(u"Coaxial"), _(u"Triaxial")]
    _awg = ["", "22", "20", "16", "12"]
    _insert = ["", _(u"Vitreous Glass"), _(u"Alumina Ceramic"), _(u"Polyimide"),
               _(u"Diallylphtalate"), _(u"Melamine"), _(u"Flourosilicone"),
               _(u"Silicone Rubber"), _(u"Polysulfone"), _(u"Epoxy Resin"),
               _(u"Teflon"), _(u"Chlorotrifluorethylene"), _(u"Polyamide"),
               _(u"Polychloroprene"), _(u"Polyethylene")]
    _quality = ["", "MIL-SPEC", _(u"Lower")]

    def __init__(self):
        """
        Initializes the Multipin Connection Component Class.
        """

        Connection.__init__(self)

        self.subcategory = 72               # Subcategory ID in rtkcom DB.

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

        self._in_labels.append(_(u"Configuration:"))
        self._in_labels.append(_(u"Insert Material:"))
        self._in_labels.append(_(u"Contact Gauge:"))
        self._in_labels.append(_(u"Amperes per Contact:"))
        self._in_labels.append(_(u"# of Active Pins:"))
        self._in_labels.append(_(u"Mate/Unmate Cycles\n(per 1000 hours):"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub></span>"
        self._out_labels.append(u"\u03C0<sub>K</sub>:")
        self._out_labels.append(u"\u03C0<sub>P</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Multipin Connection Component
        Class prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Connection.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the Configuration ComboBox.  We store the index value in the
        # construction_id field in the program database.
        part.cmbConfiguration = _widg.make_combo(simple=True)
        # Create hte Insert Material ComboBox.  We store the index value in the
        # insulation_id field in the program database.
        part.cmbInsert = _widg.make_combo(simple=True)
        # Create the Contact Gauge Entry.  We store the index value in the
        # cycles_id field in the program database.
        part.cmbContactGauge = _widg.make_combo(simple=True)
        # Create the Amperes per Contact Entry.  We store the index value in
        # the s2 field in the program database.
        part.txtAmpsContact = _widg.make_entry()
        part.txtActivePins = _widg.make_entry()
        # Create the Mate/Demate Cycles Entry.  We store the index value in the
        # s3 field in the program database.
        part.txtMateCycles = _widg.make_entry()

        # Load all the gtk.ComboBox().
        for i in range(len(self._configuration)):
            part.cmbConfiguration.insert_text(i, self._configuration[i])
        for i in range(len(self._insert)):
            part.cmbInsert.insert_text(i, self._insert[i])
        for i in range(len(self._awg)):
            part.cmbContactGauge.insert_text(i, self._awg[i])

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbConfiguration, _x_pos, _y_pos[2])
        layout.put(part.cmbInsert, _x_pos, _y_pos[3])
        layout.put(part.cmbContactGauge, _x_pos, _y_pos[4])
        layout.put(part.txtAmpsContact, _x_pos, _y_pos[5])
        layout.put(part.txtActivePins, _x_pos, _y_pos[6])
        layout.put(part.txtMateCycles, _x_pos, _y_pos[7])

        # Connect to callback methods.
        part.cmbConfiguration.connect('changed', self._callback_combo,
                                      part, 16)
        part.cmbContactGauge.connect('changed', self._callback_combo, part, 18)
        part.cmbInsert.connect('changed', self._callback_combo, part, 38)
        part.txtAmpsContact.connect('focus-out-event', self._callback_entry,
                                    part, 'float', 98)
        part.txtMateCycles.connect('focus-out-event', self._callback_entry,
                                   part, 'float', 99)
        part.txtActivePins.connect('focus-out-event', self._callback_entry,
                                   part, 'float', 60)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with
        calculation input information.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Connection.assessment_inputs_load(self, part)

        part.cmbConfiguration.set_active(int(_model.get_value(_row, 16)))
        part.cmbInsert.set_active(int(_model.get_value(_row, 38)))
        part.cmbContactGauge.set_active(int(_model.get_value(_row, 18)))
        part.txtAmpsContact.set_text(str(fmt.format(
            _model.get_value(_row, 98))))
        part.txtMateCycles.set_text(str(fmt.format(
            _model.get_value(_row, 99))))
        part.txtActivePins.set_text(str('{0:0.0f}'.format(
            _model.get_value(_row, 60))))

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Mulitpin Connection Component Class calculation
        results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Connection.reliability_results_create(self, part, layout,
                                                         x_pos, y_pos)

        # Create the multipin connector specific display widgets.
        part.txtPiK = _widg.make_entry(width=100, editable=False, bold=True)
        # Create the piP Entry.  We store this value in the piPT field in the
        # program database.
        part.txtPiP = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the display widgets.
        layout.put(part.txtPiK, _x_pos, _y_pos[3])
        layout.put(part.txtPiP, _x_pos, _y_pos[4])

        layout.show_all()

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with calculation
        results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Connection.assessment_results_load(self, part)

        part.txtPiK.set_text(str('{0:0.2g}'.format(
            _model.get_value(_row, 75))))
        part.txtPiP.set_text(str(fmt.format(_model.get_value(_row, 78))))

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Paper Bypass Capacitor
        class.

        :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
        :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                     in List class gtk.TreeModel().
        :param gtk.TreeModel systemmodel: the RTK Hardware class
                                          gtk.TreeModel().
        :param gtk.TreeIter systemrow: the currently selected
                                       gtk.TreeIter() in the RTK Hardware
                                       class gtk.TreeModel().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        def _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part count hazard rate calculations for the
            Multipin Connection Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            _hrmodel = {}
            _hrmodel['equation'] = 'lambdab * piQ'

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Cidx = partmodel.get_value(partrow, 16)      # Configuration index
            Eidx = systemmodel.get_value(systemrow, 22)  # Environment index
            Qidx = partmodel.get_value(partrow, 85)      # Quality index

            _hrmodel['lambdab'] = self._lambdab_count[Cidx - 1][Eidx - 1]

            if Qidx == 1:
                _hrmodel['piQ'] = 1.0
            else:
                _hrmodel['piQ'] = 2.0

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Multipin Connection Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            :return: False if succussful or True if an error is encountered.
            :rtype: boolean
            """

            from math import exp

            _hrmodel = {}
            _hrmodel['equation'] = 'lambdab * piK * piP * piE'

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve temperature rise inputs.
            Gidx = partmodel.get_value(partrow, 18)     # Contact gauge index
            i = partmodel.get_value(partrow, 98)        # Amps per contact

            # Retrieve hazard rate inputs.
            Cidx = partmodel.get_value(partrow, 16)     # Configuration index
            Iidx = partmodel.get_value(partrow, 38)     # Insert index
            N = partmodel.get_value(partrow, 60)        # Number of active pins
            Qidx = partmodel.get_value(partrow, 85)
            cycles = partmodel.get_value(partrow, 99)   # Mate/Demate cycles

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
            Vrated = partmodel.get_value(partrow, 94)

            # Calculate temperature rise.
            K = self._gauge[Gidx - 1]
            To = K * i**1.85

            # Base hazard rate.
            if Iidx > 1 and Iidx < 4:
                _hrmodel['lambdab'] = 0.020 * exp((-1592.0 / (To + 273.0)) + (((To + 273.0) / 473.0)**5.36))
            elif Iidx > 3 and Iidx < 10:
                _hrmodel['lambdab'] = 0.431 * exp((-2073.6 / (To + 273.0)) + (((To + 273.0) / 423.0)**4.66))
            elif Iidx > 9 and Iidx < 13:
                _hrmodel['lambdab'] = 0.190 * exp((-1298.0 / (To + 273.0)) + (((To + 273.0) / 373.0)**4.25))
            elif Iidx > 12 and Iidx < 16:
                _hrmodel['lambdab'] = 0.770 * exp((-1528.8 / (To + 273.0)) + (((To + 273.0) / 358.0)**4.72))
            else:
                _hrmodel['lambdab'] = 0.0

            # Mate/Unmate cycles correction factor.
            if cycles <= 0.05:
                _hrmodel['piK'] = 1.0
            elif cycles > 0.05 and cycles <= 0.5:
                _hrmodel['piK'] = 1.5
            elif cycles > 0.5 and cycles <= 5:
                _hrmodel['piK'] = 2.0
            elif cycles > 5 and cycles <= 50:
                _hrmodel['piK'] = 3.0
            else:
                _hrmodel['piK'] = 4.0

            # Active pins correction factor.
            if N >= 2:
                _hrmodel['piP'] = exp(((N - 1) / 10)**0.51064)
            else:
                _hrmodel['piP'] = 0.0

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[Qidx - 1][idx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            # Calculate the component dormant hazard rate.
            _lambdad = _calc.dormant_hazard_rate(_category_id, _subcategory_id,
                                                 _active_env, _dormant_env,
                                                 _lambdaa)


            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            # Calculate operating point ratios.
            _i_ratio = float(Iapplied) / float(Irated)
            _v_ratio = float(Vapplied) / float(Vrated)

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 75, _hrmodel['piK'])
            partmodel.set_value(partrow, 78, _hrmodel['piP'])
            partmodel.set_value(partrow, 107, To)
            partmodel.set_value(partrow, 111, _v_ratio)

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 29, _lambdad)
            systemmodel.set_value(systemrow, 32, _lambdap)
            systemmodel.set_value(systemrow, 60, _overstress)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        _calc_model = systemmodel.get_value(systemrow, 10)

        if _calc_model == 1:
            _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow)
        elif _calc_model == 2:
            _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow)

        return False
