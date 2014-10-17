#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       fixed.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

from math import exp, sqrt

try:
    import rtk.configuration as _conf
    import rtk.calculations as _calc
except ImportError:
    import configuration as _conf
    import calculations as _calc
from capacitor import Capacitor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class PaperBypass(Capacitor):
    """
    Fixed Paper Bypass Capacitor Component Class.

    Covers specifications MIL-C-25 and MIL-C-12889.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.1
    """

    _quality = ["", "MIL-SPEC", _(u"Lower")]
    _specification = ["", "MIL-C-25 (CP)", "MIL-C-12889 (CA)"]
    _specsheet = [["", "85\u00B0C", "125\u00B0C"],
                  ["", "85\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Paper Bypass Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 40               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 9.0, 5.0, 15.0, 6.0, 8.0, 17.0, 32.0,
                     22.0, 0.5, 12.0, 32.0, 670.0]
        self._piQ = [3.0, 7.0]
        self._lambdab_count = [[0.0036, 0.0072, 0.330, 0.016, 0.055, 0.023,
                                0.030, 0.07, 0.13, 0.083, 0.0018, 0.044, 0.12,
                                2.1],
                               [0.0039, 0.0087, 0.042, 0.022, 0.070, 0.035,
                                0.047, 0.19, 0.35, 0.130, 0.0020, 0.056, 0.19,
                                2.5]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

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
            Fixed Paper Bypass Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)
            _Sidx = partmodel.get_value(partrow, 102)

            _hrmodel['lambdab'] = self._lambdab_count[_Sidx - 1][_Eidx - 1]

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
            the Fixed Paper Bypass Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 101)
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # MIL-C-25
                if idx2 == 1:               # 85C
                    Tref = 358.0
                elif idx2 == 2:             # 125C
                    Tref = 398.0
                else:
                    Tref = 358.0
            elif idx == 2:                  # MIL-C-12889
                Tref = 358.0
            else:
                Tref = 358.0

            _hrmodel['lambdab'] = 0.00086 * ((S / 0.4)**5.0 + 1.0) * exp(2.5 * ((Tamb + 273.0) / Tref)**18.0)

            # Capacitance correction factor.
            if idx == 1:
                _hrmodel['piCV'] = 1.2 * C**0.095
            else:
                _hrmodel['piCV'] = 1.0

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class PaperFeedthrough(Capacitor):
    """
    Fixed Paper Feedthrough Capacitor Component Class.

    Covers specification MIL-C-11693.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.2
    """

    _quality = ["", "M", "Non-Est. Rel.", "Lower"]
    _specification = ["", "MIL-C-11693 (CZ/CZR)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C", u"150\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Paper Feedthrough Bypass Capacitor class.
        """

        Capacitor.__init__(self)

        self.subcategory = 41               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 9.0, 7.0, 15.0, 6.0, 8.0, 17.0, 28.0, 22.0, 0.5,
                     12.0, 32.0, 570.0]
        self._piQ = [1.0, 3.0, 10.0]
        self._lambdab_count = [0.0047, 0.0096, 0.044, 0.034, 0.073, 0.030,
                               0.040, 0.094, 0.15, 0.11, 0.0024, 0.058, 0.18,
                               2.7]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Paper Feedthrough
        Capacitor class.

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
            Fixed Paper Feedthrough Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Paper Feedthrough Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx2 == 1:                   # 85C
                Tref = 358.0
            elif idx2 == 2:                 # 125C
                Tref = 398.0
            elif idx2 == 3:                 # 150C
                Tref = 423.0
            else:                           # Default
                Tref = 358.0

            _hrmodel['lambdab'] = 0.00115 * ((S / 0.4)**5.0 + 1) * exp(2.5 * ((Tamb + 273) / Tref)**18)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 1.4 * C**0.12

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class PlasticFilm(Capacitor):
    """
    Fixed Paper and Plastic Film Capacitor Component Class.

    Covers specifications MIL-C-14157 and MIL-C-19978.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.3
    """

    _quality = ["", "S", "R", "P", "M", "L",
                "MIL-C-19978, Non-Est. Rel.", "Lower"]
    _specification = ["", "MIL-C-14157 (CPV)", "MIL-C-19978 (CQ/CQR)"]
    _specsheet = [["", u"65\u00B0C", u"85\u00B0C", u"125\u00B0C"],
                  ["", u"65\u00B0C", u"85\u00B0C", u"125\u00B0C",
                   u"170\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Paper and Plastic Film Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 42               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 5.0, 11.0, 20.0,
                     20.0, 0.5, 11.0, 29.0, 530.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
        self._lambdab_count = [0.0021, 0.0042, 0.017, 0.010, 0.030, 0.0068,
                               0.013, 0.026, 0.048, 0.044, 0.0010, 0.023,
                               0.063, 1.1]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Paper and Plastic Film
        Capacitor class.

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
            Fixed Paper and Plastic Film Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _htmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Paper and Plastic Film Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 101)
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # MIL-C-14157
                if idx2 == 1:               # 65C
                    Tref = 338.0
                elif idx2 == 2:             # 85C
                    Tref = 398.0
                elif idx2 == 3:             # 125C
                    Tref = 358.0
                else:                       # Default
                    Tref = 338.0
            elif idx == 2:                  # MIL-C-19978
                if idx2 == 1:               # 65C
                    Tref = 358.0
                elif idx2 == 2:             # 85C
                    Tref = 398.0
                elif idx2 == 3:             # 125C
                    Tref = 338.0
                elif idx2 == 4:             # 170C
                    Tref = 443.0
                else:                       # Default
                    Tref = 338.0
            else:
                Tref = 338.0

            _hrmodel['lambdab'] = 0.0005 * ((S / 0.4)**5.0 + 1) * exp(2.5 * ((Tamb + 273) / Tref)**18)

            # Capacitance correction factor.
            if idx == 1:
                _hrmodel['piCV'] = 1.6 * C**0.13
            else:
                _hrmodel['piCV'] = 1.3 * C**0.077

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class MetallizedPaper(Capacitor):
    """
    Fixed Metallized Paper, Paper-Plastic, and Plastic Capacitor
    Component Class.

    Covers specifications MIL-C-18312 and MIL-C-39022.

    Hazard Rate Models:
        #. MIL-HDBK-217F, section 10.4
    """

    _quality = ["", "S", "R", "P", "M", "L",
                "MIL-C-18312, Non-Est. Rel.", "Lower"]
    _specification = ["", "MIL-C-18312 (CH)", "MIL-C-39022 (CHR)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C"],
                  ["", u"85\u00B0C", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Metallized Paper, Paper-Plastic, and Plastic
        Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 43               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 8.0, 5.0, 14.0, 4.0, 6.0, 11.0, 20.0,
                     20.0, 0.5, 11.0, 29.0, 530.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 7.0, 20.0]
        self._lambdab_count = [0.0029, 0.0058, 0.023, 0.014, 0.041, 0.012,
                               0.018, 0.037, 0.066, 0.060, 0.0014, 0.032,
                               0.088, 1.5]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Metallized Paper,
        Paper-Plastic, and Plastic Capacitor class.

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
            Fixed Metallized Paper, Paper-Plastic, and Plastic Capacitor
            Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Metallized Paper, Paper-Plastic, and Plastic Capacitor
            Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 101)
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # MIL-C-18312
                if idx2 == 1:               # 85C
                    Tref = 358.0
                elif idx2 == 2:             # 125C
                    Tref = 398.0
                else:                       # Default
                    Tref = 358.0
            elif idx == 2:                  # MIL-C-39022
                if idx2 == 1:               # 85C
                    Tref = 358.0
                elif idx2 == 2:             # 125C
                    Tref = 398.0
                else:
                    Tref = 358.0            # Default
            else:
                Tref = 358.0

            _hrmodel['lambdab'] = 0.00069 * ((S / 0.4)**5.0 + 1) * exp(2.5 * ((Tamb + 273) / Tref)**18)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 1.2 * C**0.092

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class Plastic(Capacitor):
    """
    Fixed Plastic and Metallized Plastic Capacitor Component Class.

    Covers specifications MIL-C-55514.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.5
    """

    _quality = ["", "S", "R", "P", "M", "Lower"]
    _specification = ["", "MIL-C-55514 (CFR)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Plastic and Metallized Plastic Capacitor
        Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 44               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 16.0, 6.0, 11.0, 18.0, 30.0,
                     23.0, 0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 10.0]
        self._lambdab_count = [0.0041, 0.0083, 0.042, 0.021, 0.067, 0.026,
                               0.048, 0.086, 0.14, 0.10, 0.0020, 0.054, 0.15,
                               2.5]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Characteristic:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Plastic and Metallized
        Plastic Capacitor class.

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
            Fixed Plastic and Metallized Plastic Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Plastic and Metallized Plastic Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx2 == 1 or idx2 == 2:
                Tref = 358.0
            elif idx2 == 3 or idx2 == 4 or idx2 == 5:
                Tref = 398.0
            else:
                Tref = 358.0

            _hrmodel['lambdab'] = 0.00099 * ((S / 0.4)**5.0 + 1) * exp(2.5 * ((Tamb + 273) / Tref)**18)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 1.1 * C**0.086

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class SuperMetallizedPlastic(Capacitor):
    """
    Fixed Super-Metallized Plastic Capacitor Component Class.

    Covers specifications MIL-C-83421.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.6
    """

    _quality = ["", "S", "R", "P", "M", "Lower"]
    _specification = ["", "MIL-C-83421 (CRH)"]
    _specsheet = [["", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Super-Metallized Plastic Capacitor Component
        Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 45               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 4.0, 8.0, 5.0, 14.0, 4.0, 6.0, 13.0, 20.0,
                     20.0, 0.5, 11.0, 29.0, 530.0]
        self._piQ = [0.02, 0.1, 0.3, 1.0, 10.0]
        self._lambdab_count = [0.0023, 0.0092, 0.019, 0.012, 0.033, 0.0096,
                               0.014, 0.034, 0.053, 0.048, 0.0011, 0.026, 0.07,
                               1.2]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Characteristic:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Super-Metallized
        Plastic Capacitor class.

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
            Fixed Super-Metallized Plastic Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Super-Metallized Plastic Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Base hazard rate.
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx2 == 1:                   # 125C
                Tref = 398
            else:                           # Default
                Tref = 398

            _hrmodel['lambdab'] = 0.00055 * ((S / 0.4)**5.0 + 1) * exp(2.5 * ((Tamb + 273) / Tref)**18)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 1.2 * C**0.092

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class Mica(Capacitor):
    """
    Fixed Mica Capacitor Component Class.

    Covers specifications MIL-C-5 and MIL-C-39001.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.7
    """

    _quality = ["", "T", "S", "R", "P", "M", "L",
                "MIL-C-5, Non-Est. Rel. Dipped",
                "MIL-C-5, Non-Est. Rel. Molded",
                "Lower"]
    _specification = ["", "MIL-C-5 (CM)", "MIL-C-39001 (CMR)"]
    _specsheet = [["", u"70\u00B0C", u"85\u00B0C", u"125\u00B0C",
                   u"150\u00B0C"], ["", u"125\u00B0C", u"150\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Mica Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 46               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0,
                     23.0, 0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 6.0, 15.0]
        self._lambdab_count = [0.0005, 0.0015, 0.0091, 0.0044, 0.014, 0.0068,
                               0.0095, 0.054, 0.069, 0.031, 0.00025, 0.012,
                               0.046, 0.45]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Mica Capacitor class.

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
            Fixed Mica Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Mica Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 101)
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # MIL-C-5
                if idx2 == 1:               # 70C
                    Tref = 343.0
                elif idx2 == 2:             # 85C
                    Tref = 358.0
                elif idx2 == 3:             # 125C
                    Tref = 398.0
                elif idx2 == 4:             # 150C
                    Tref = 423.0
                else:
                    Tref = 343.0            # Default
            elif idx == 2:                  # MIL-C-39001
                if idx2 == 1:               # 125C
                    Tref = 398.0
                elif idx2 == 2:             # 150C
                    Tref = 423.0
                else:                       # Default
                    Tref = 398.0
            else:
                Tref = 343.0

            _hrmodel['lambdab'] = 0.00000000086 * ((S / 0.4)**3.0 + 1.0) * exp(16.0 * (Tamb + 273.0) / Tref)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 0.45 * C**0.14

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class MicaButton(Capacitor):
    """
    Fixed Mica Button Capacitor Component Class.

    Covers specification MIL-C-10950.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.8
    """

    _quality = ["", "MIL-C-10950", "Lower"]
    _specification = ["", "MIL-C-10950 (CB)"]
    _specsheet = [["", u"85\u00B0C", u"150\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Mica Button Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 46               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 16.0, 5.0, 7.0, 22.0, 28.0,
                     23.0, 0.5, 13.0, 34.0, 610.0]
        self._piQ = [5.0, 15.0]
        self._lambdab_count = [0.018, 0.037, 0.19, 0.094, 0.31, 0.10, 0.14,
                               0.47, 0.60, 0.48, 0.0091, 0.25, 0.68, 11.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Mica Button Capacitor
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
            Fixed Mica Button Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Mica Button Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 101)
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # MIL-C-1950
                if idx2 == 1:               # 85C
                    Tref = 358.0
                elif idx2 == 2:             # 150C
                    Tref = 423.0
                else:                       # Default for MIL-C-1950
                    Tref = 358.0
            else:                           # Default
                Tref = 358.0

            _hrmodel['lambdab'] = 0.0053 * ((S / 0.4)**3.0 + 1) * exp(1.2 * ((Tamb + 273) / Tref)**6.3)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 0.31 * C**0.23

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class Glass(Capacitor):
    """
    Fixed Glass Capacitor Component Class.

    Covers specifications MIL-C-11272 and MIL-C-23269.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.9
    """

    _quality = ["", "S", "R", "P", "M", "L", "MIL-C-11272, Non-Est. Rel.",
                "Lower"]
    _specification = ["", "MIL-C-11272 (CY)", "MIL-C-23269 (CYR)"]
    _specsheet = [["", u"125\u00B0C", u"200\u00B0C"], ["", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Glass Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 48               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 6.0, 16.0, 5.0, 7.0, 22.0, 28.0, 23.0, 0.5,
                     13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.10, 0.30, 1.0, 3.0, 3.0, 10.0]
        self._lambdab_count = [0.00032, 0.00096, 0.0059, 0.0029, 0.0094,
                               0.0044, 0.0062, 0.035, 0.045, 0.020, 0.00016,
                               0.0076, 0.030, 0.29]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Glass Capacitor
        Component Class.

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
            Fixed Glass Capacitor Component Class.

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
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Glass Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve junction temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 101)
            idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # MIL-C-11272
                if idx2 == 1:               # 125C
                    Tref = 398.0
                elif idx2 == 2:             # 200C
                    Tref = 473.0
                else:                       # Default
                    Tref = 398.0
            elif idx == 2:                  # MIL-C-23269
                Tref = 473.0
            else:                           # Default
                Tref = 398.0

            _hrmodel['lambdab'] = 0.000000000825 * ((S / 0.5)**4.0 + 1) * exp(16 * ((Tamb + 273) / Tref)**18)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 0.62 * C**0.14

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class CeramicGeneral(Capacitor):
    """
    Fixed General Purpose Ceramic Capacitor Component Class.

    Covers specifications MIL-C-11015 and MIL-C-39014.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.10

    """

    _quality = ["", "S", "R", "P", "M", "L", "MIL-C-11015, Non-Est. Rel.",
                "Lower"]
    _specification = ["", "MIL-C-11015 (CK)", "MIL-C-39014 (CKR)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C", u"150\u00B0C"],
                  ["", u"85\u00B0C", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed General Purpose Ceramic Capacitor Component
        class.
        """

        Capacitor.__init__(self)

        self.subcategory = 39               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----------------------------------------------------------------- #
        self._piE = [1.0, 2.0, 9.0, 5.0, 15.0, 4.0, 4.0, 8.0, 12.0, 20.0, 0.4,
                     13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 3.0, 10.0]
        self._lambdab_count = [0.0036, 0.0074, 0.034, 0.019, 0.056, 0.015,
                               0.015, 0.032, 0.048, 0.077, 0.0014, 0.049,
                               0.13, 2.3]
        # ----------------------------------------------------------------- #

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed General Purpose Ceramic
        Capacitor Component Class.

        :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
        :param gtk.TreeIter partrow: the currently selected gtk.TreeIter() in
                                     the List class gtk.TreeModel().
        :param gtk.TreeModel systemmodel: the RTK Hardware class
                                          gtk.TreeModel().
        :param gtk.TreeIter systemrow: the currently selected gtk.TreeIter() in
                                       the RTK Hardware class gtk.TreeModel().
        """

        def _calculate_mil_217_count(partmodel, partrow,
                                     systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part count hazard rate calculations for the
            Fixed General Purpose Ceramic Capacitor Component Class.

            :param gtk.TreeModel partmodel: the RTK List class gtk.TreeModel().
            :param gtk.TreeIter partrow: the currently selected gtk.TreeIter()
                                         in the List class gtk.TreeModel().
            :param gtk.TreeModel systemmodel: the RTK Hardware class
                                              gtk.TreeModel().
            :param gtk.TreeIter systemrow: the currently selected
                                           gtk.TreeIter() in the RTK Hardware
                                           class gtk.TreeModel().
            """

            _hrmodel = {}
            _hrmodel['equation'] = "lambdab * piQ"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            _Eidx = systemmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed General Purpose Ceramic Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            _idx = partmodel.get_value(partrow, 101)
            _idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if _idx == 1:                       # MIL-C-11015
                if _idx2 == 1:                  # 85C
                    Tref = 358.0
                elif _idx2 == 2:                # 125C
                    Tref = 398.0
                elif _idx2 == 3:                # 150C
                    Tref = 423.0
                else:                           # Default
                    Tref = 358.0
            elif _idx == 2:                     # MIL-C-39014
                if _idx2 == 1:
                    Tref = 358.0
                elif _idx2 == 2:
                    Tref = 398.0
                else:
                    Tref = 358.0
            else:
                Tref = 358.0

            _hrmodel['lambdab'] = 0.0003 * ((S / 0.3)**3 + 1) * exp((Tamb + 273) / Tref)

            # Capacitance correction factor.
            _hrmodel['piCV'] = 0.41 * C**0.11

            # Environmental correction factor.
            _idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[_idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class CeramicChip(Capacitor):
    """
    Fixed Temperature Compensating and Chip Ceramic Capacitor Component
    Class.

    Covers specifications MIL-C-20 and MIL-C-55681.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.11
    """

    _quality = ["", "S", "R", "P", "M", "Non-Est. Rel.", "Lower"]
    _specification = ["", "MIL-C-20 (CC/CCR)", "MIL-C-55681 (CDR)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C"], ["", u"85\u00B0C"]]

    def __init__(self):
        """
        Initializes the Fixed Temperature Compensating and Chip Ceramic
        Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 50               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 10.0, 5.0, 17.0, 4.0, 8.0, 16.0, 35.0, 24.0,
                     0.5, 13.0, 34.0, 610.0]
        self._piQ = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
        self._lambdab_count = [0.00078, 0.0022, 0.013, 0.0056, 0.023, 0.0077,
                               0.015, 0.053, 0.12, 0.048, 0.00039, 0.017,
                               0.065, 0.68]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Fixed Temperature
        Compensating and Chip Ceramic Capacitor Component Class.

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
            Fixed Temperature Compensating and Chip Ceramic Capacitor Component
            Class.

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
            _Eidx = systenmodel.get_value(systemrow, 22)

            _hrmodel['lambdab'] = self._lambdab_count[_Eidx - 1]

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
            the Fixed Temperature Compensating and Chip Ceramic Capacitor
            Component Class.

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
            _hrmodel['equation'] = "lambdab * piCV * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve temperature inputs.
            Tamb = partmodel.get_value(partrow, 37)

            # Retrieve hazard rate inputs.
            C = partmodel.get_value(partrow, 15)
            VappliedAC = partmodel.get_value(partrow, 64)
            Vapplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Vrated = partmodel.get_value(partrow, 94)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            spec_idx = partmodel.get_value(partrow, 101)
            temp_idx2 = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if spec_idx == 1:               # MIL-C-20
                if temp_idx2 == 1:          # 85C
                    Tref = 358.0
                elif temp_idx2 == 2:        # 125C
                    Tref = 398.0
                else:
                    Tref = 398.0
            elif spec_idx == 2:             # MIL-C-55681
                Tref = 398.0
            else:                           # Default
                Tref = 358.0

            _hrmodel['lambdab'] = 0.0000000026 * ((S / 0.3)**3 + 1) * exp(1.4 * ((Tamb + 273) / Tref))

            # Capacitance correction factor.
            _hrmodel['piCV'] = 0.59 * C**0.12

            # Environmental correction factor.
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

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
            _i_ratio = Iapplied / Irated
            _v_ratio = Vapplied / Vrated

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 70, _hrmodel['piCV'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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
