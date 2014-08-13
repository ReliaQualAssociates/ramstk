#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       transformer.py is part of The RTK Project
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


class Audio(Inductor):
    """
    Audio Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the Audio Transformer Component Class. """

        Inductor.__init__(self)

        self.subcategory = 60                   # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073,
                               0.081, 0.10, 0.22, 0.035, 0.11, 0.31, 4.7]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.move(part.txtOperPwr, _x_pos, _y_pos[3])
        layout.move(part.txtInputPwr, _x_pos, _y_pos[4])
        layout.move(part.txtArea, _x_pos, _y_pos[5])
        layout.move(part.txtWeight, _x_pos, _y_pos[6])

        layout.show_all()

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
            Audio Transformer Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)         # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
            the Audio Transformer Component Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piE"

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
            if idx == 1:                    # 85C
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6
            elif idx == 2:                  # 105C
                Tref = 352.0
                K1 = 0.002
                K2 = 14.0
            elif idx == 3:                  # 130C
                Tref = 364.0
                K1 = 0.0018
                K2 = 8.7
            elif idx == 4:                  # 155C
                Tref = 400.0
                K1 = 0.002
                K2 = 10.0
            elif idx == 5:                  # 170C
                Tref = 398.0
                K1 = 0.00125
                K2 = 3.8
            elif idx == 6:                  # >170C
                Tref = 477.0
                K1 = 0.00159
                K2 = 8.4
            else:                           # Default
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6

            _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

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


class Power(Inductor):
    """
    High Power Pulse and Power Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the High Power Pulse and Power Transformer Component
            Class.
        """

        Inductor.__init__(self)

        self.subcategory = 60               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011, 0.37, 1.2, 16.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.move(part.txtOperPwr, _x_pos, _y_pos[3])
        layout.move(part.txtInputPwr, _x_pos, _y_pos[4])
        layout.move(part.txtArea, _x_pos, _y_pos[5])
        layout.move(part.txtWeight, _x_pos, _y_pos[6])

        layout.show_all()

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
            High Power Pulse and Power Transformer Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
            the High Power Pulse and Power Transformer Component Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piE"

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

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve hazard rate inputs.
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            if idx == 1:                    # 85C
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6
            elif idx == 2:                  # 105C
                Tref = 352.0
                K1 = 0.002
                K2 = 14.0
            elif idx == 3:                  # 130C
                Tref = 364.0
                K1 = 0.0018
                K2 = 8.7
            elif idx == 4:                  # 155C
                Tref = 400.0
                K1 = 0.002
                K2 = 10.0
            elif idx == 5:                  # 170C
                Tref = 398.0
                K1 = 0.00125
                K2 = 3.8
            elif idx == 6:                  # >170C
                Tref = 477.0
                K1 = 0.00159
                K2 = 8.4
            else:                           # Default
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6

            _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

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


class LowPowerPulse(Inductor):
    """
    Low Power Pulse Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """
        Initializes the Low Power Pulse Transformer Component Class.
        """

        Inductor.__init__(self)

        self.subcategory = 60               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.0035, 0.023, 0.049, 0.019, 0.065, 0.027,
                               0.037, 0.041, 0.052, 0.11, 0.0018, 0.053, 0.16,
                               2.3]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.move(part.txtOperPwr, _x_pos, _y_pos[3])
        layout.move(part.txtInputPwr, _x_pos, _y_pos[4])
        layout.move(part.txtArea, _x_pos, _y_pos[5])
        layout.move(part.txtWeight, _x_pos, _y_pos[6])

        layout.show_all()

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
            Low Power Pulse Transformer Component Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)         # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
            the Low Power Pulse Transformer Component Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piE"

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
            if idx == 1:                    # 85C
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6
            elif idx == 2:                  # 105C
                Tref = 352.0
                K1 = 0.002
                K2 = 14.0
            elif idx == 3:                  # 130C
                Tref = 364.0
                K1 = 0.0018
                K2 = 8.7
            elif idx == 4:                  # 155C
                Tref = 400.0
                K1 = 0.002
                K2 = 10.0
            elif idx == 5:                  # 170C
                Tref = 398.0
                K1 = 0.00125
                K2 = 3.8
            elif idx == 6:                  # >170C
                Tref = 477.0
                K1 = 0.00159
                K2 = 8.4
            else:                           # Default
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6

            _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

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


class RF(Inductor):
    """
    Radio Frequency Transformer Component Class.
    Covers specifications MIL-T-27, MIL-T-21038, and MIL-T-55631.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 11.1
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _insulation = ["", u"85\u00B0C", u"105\u00B0C", u"130\u00B0C",
                   u"155\u00B0C", u"170\u00B0C", u">170\u00B0C"]

    def __init__(self):
        """ Initializes the Radio Frequency Transformer Component Class. """

        Inductor.__init__(self)

        self.subcategory = 60               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [3.0, 7.5]
        self._lambdab_count = [0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33,
                               0.42, 0.88, 0.015, 0.42, 1.2, 19.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbInsulation, _x_pos, _y_pos[2])
        layout.move(part.txtOperPwr, _x_pos, _y_pos[3])
        layout.move(part.txtInputPwr, _x_pos, _y_pos[4])
        layout.move(part.txtArea, _x_pos, _y_pos[5])
        layout.move(part.txtWeight, _x_pos, _y_pos[6])

        layout.show_all()

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
            Radio Frequency Transformer Component Class.

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
            _hrmodel['piQ'] = part._calc_data[79]
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

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
            the Radio Frequency Transformer Component Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piE"

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

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve hazard rate inputs.
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            if idx == 1:                    # 85C
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6
            elif idx == 2:                  # 105C
                Tref = 352.0
                K1 = 0.002
                K2 = 14.0
            elif idx == 3:                  # 130C
                Tref = 364.0
                K1 = 0.0018
                K2 = 8.7
            elif idx == 4:                  # 155C
                Tref = 400.0
                K1 = 0.002
                K2 = 10.0
            elif idx == 5:                  # 170C
                Tref = 398.0
                K1 = 0.00125
                K2 = 3.8
            elif idx == 6:                  # >170C
                Tref = 477.0
                K1 = 0.00159
                K2 = 8.4
            else:                           # Default
                Tref = 329.0
                K1 = 0.0018
                K2 = 15.6

            _hrmodel['lambdab'] = K1 * exp(((Ths + 273) / Tref)**K2)

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
