#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       coil.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

from math import exp, sqrt

try:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
from inductor import Inductor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Coil(Inductor):
    """
    Coil Component Class.
    Covers specifications MIL-C-15305 and MIL-C-39010.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 11.2
    """

    _construction = ["", _(u"Fixed"), _(u"Variable")]
    _quality = ["", "S", "R", "P", "M", "MIL-C-15305", _(u"Lower")]
    _insulation = ["", "A", "B", "F", "O"]

    def __init__(self):
        """
        Initializes the Coil Component Class.
        """

        Inductor.__init__(self)

        self.subcategory = 63               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [1.0, 2.0]
        self._piE = [1.0, 4.0, 12.0, 5.0, 16.0, 5.0, 7.0, 6.0, 8.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 4.0, 20.0]
        self._lambdab_count = [[0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011,
                                0.015, 0.016, 0.022, 0.052, 0.00083, 0.25,
                                0.073, 1.1],
                               [0.0033, 0.015, 0.046, 0.018, 0.061, 0.022,
                                0.03, 0.033, 0.044, 0.10, 0.0017, 0.05, 0.15,
                                2.2]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Construction:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Coil Component Class
        prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = Inductor.assessment_inputs_create(self, part, layout,
                                                     x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 40

        part.cmbConstruction = _widg.make_combo(simple=True)

        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.move(part.txtOperPwr, _x_pos, _y_pos[3])
        layout.move(part.txtInputPwr, _x_pos, _y_pos[4])
        layout.move(part.txtArea, _x_pos, _y_pos[5])
        layout.move(part.txtWeight, _x_pos, _y_pos[6])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[7])

        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Coil Component Class calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Inductor.reliability_results_create(self, part, layout,
                                                       x_pos, y_pos)

        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)

        layout.put(part.txtPiC, _x_pos, _y_pos[4])

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

        (_model, _row) = Inductor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Inductor.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 69))))

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
            Coil Component Class.

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
            _hrmodel['equation'] = "lambdab * piQ"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            _Cidx = part._attribute[16]                   # Construction index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            _Eidx = systemmodel.get_value(systemrow, 22)  # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[_Cidx - 1][_Eidx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Coil Component Class.

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
            _hrmodel['equation'] = "lambdab * piC * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hot spot temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            A = partmodel.get_value(partrow, 44)
            Wt = partmodel.get_value(partrow, 45)
            P = partmodel.get_value(partrow, 64)
            Pin = partmodel.get_value(partrow, 93)

            # Retrieve hazard rate inputs.
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
            Vrated = partmodel.get_value(partrow, 94)

            # Calculate hot spot temperature.
            if P > 0.0 and A > 0.0:
                Trise = 125 * P / A
            elif P > 0.0 and Wt > 0.0:
                Trise = 11.5 * P / (Wt**0.6766)
            elif Pin > 0.0 and Wt > 0.0:
                Trise = 2.1 * Pin / (Wt**0.6766)
            else:
                Trise = 35.0

            Ths = Tamb + 1.1 * Trise

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 38)
            if idx == 1:                    # Class A
                Tref = 352.0
                K = 14.0
            elif idx == 2:                  # Class B
                Tref = 364.0
                K = 8.7
            elif idx == 3:                  # Class F
                Tref = 409.0
                K = 10.0
            elif idx == 4:                  # Class O
                Tref = 329.0
                K = 15.6
            else:                           # Default
                Tref = 329.0
                K = 15.6

            _hrmodel['lambdab'] = 0.00375 * exp(((Ths + 273) / Tref)**K)

            # Construction correction factor.
            idx = partmodel.get_value(partrow, 16)
            _hrmodel['piC'] = self._piC[idx - 1]

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity

            # Calculate the component dormant hazard rate.
            _lambdad = _calc.dormant_hazard_rate(_category_id, _subcategory_id,
                                                 _active_env, _dormant_env,
                                                 _lambdaa)
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            # Calculate operating point ratios.
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 39, Ths)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 69, _hrmodel['piC'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 107, Trise)
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
