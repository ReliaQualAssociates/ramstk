#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       variable.py is part of the RTK Project
#
# All rights reserved.

from math import exp, sqrt

try:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
from capacitor import Capacitor


class Ceramic(Capacitor):
    """
    Variable Ceramic Capacitor Component Class.

    Covers specification MIL-C-81.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.16
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-81 (CV)"]
    _specsheet = [["", u"85\u00B0C", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Variable Ceramic Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 55               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0,
                     0.4, 20.0, 52.0, 950.0]
        self._piQ = [4.0, 20.0]
        self._lambdab_count = [0.08, 0.27, 1.2, 0.71, 2.3, 0.69, 1.1, 6.2,
                               12.0, 4.1, 0.032, 1.9, 5.9, 85.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.remove(u"\u03C0<sub>CV</sub>:")

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display Variable Ceramic Capacitor Component Class calculation results.

        :param rtk.Component part: the current instance of the rtk.Component()
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = Capacitor.reliability_results_create(self, part, layout,
                                                        x_pos, y_pos)

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        # Remove the capacitance correction factor entry.  It is not
        # needed for this type of capacitor.
        layout.remove(part.txtPiCV)

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
            Variable Ceramic Capacitor Component Class.

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
            the Variable Ceramic Capacitor Component Class.

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
            Reff = partmodel.get_value(partrow, 95)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # 85C
                Tref = 358.0
            elif idx == 2:                  # 125C
                Tref = 398.0
            else:                           # Default
                Tref = 358.0

            _hrmodel['lambdab'] = 0.00224 * ((S / 0.17)**3 + 1) * exp(1.59 * ((Tamb + 273) / Tref)**10.1)

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


class Piston(Capacitor):
    """
    Variable Piston Type Capacitor Component Class.

    Covers specification MIL-C-14409.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.17
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-14409 (PC)"]
    _specsheet = [["", u"125\u00B0C", u"150\u00B0C"]]

    def __init__(self):
        """
        Initializes the Variable Piston Type Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 56               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 12.0, 7.0, 18.0, 3.0, 4.0, 20.0, 30.0, 32.0,
                     0.5, 18.0, 46.0, 830.0]
        self._piQ = [3.0, 10.0]
        self._lambdab_count = [0.033, 0.13, 0.62, 0.31, 0.93, 0.21, 0.28, 2.2,
                               3.3, 2.2, 0.16, 0.93, 3.2, 37.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.remove(u"\u03C0<sub>CV</sub>:")

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display Variable Piston Type Capacitor Component Class calculation
        results.

        :param rtk.Component part: the current instance of the rtk.Component()
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = Capacitor.reliability_results_create(self, part, layout,
                                                        x_pos, y_pos)

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        # Remove the capacitance correction factor entry.  It is not
        # needed for this type of capacitor.
        layout.remove(part.txtPiCV)

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
            Variable Piston Type Capacitor Component Class.

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
            Performs MIL-HDBK-217F part stress hazard rate calculations for the
            Variable Piston Type Capacitor Component Class.

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
            Reff = partmodel.get_value(partrow, 95)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # 125C
                Tref = 398.0
            elif idx == 2:                  # 150C
                Tref = 423.0
            else:                           # Default
                Tref = 398.0

            _hrmodel['lambdab'] = 0.00000073 * ((S / 0.33)**3 + 1) * exp(12.1 * (Tamb + 273) / Tref)

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


class AirTrimmer(Capacitor):
    """
    Variable Air Trimmer Capacitor Component Class.

    Covers specification MIL-C-92.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.18
    """

    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-92 (CT)"]
    _specsheet = [["", u"85\u00B0C"]]

    def __init__(self):
        """
        Initializes the Variable Air Trimmer Capacitor Component Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 57               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 3.0, 13.0, 8.0, 24.0, 6.0, 10.0, 37.0, 70.0, 36.0,
                     0.5, 20.0, 52.0, 950.0]
        self._piQ = [5.0, 20.0]
        self._lambdab_count = [0.80, 0.33, 1.6, 0.87, 3.0, 1.0, 1.7, 9.9, 19.0,
                               8.1, 0.032, 2.5, 8.9, 100.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = _(u"Temperature Rating:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.remove(u"\u03C0<sub>CV</sub>:")

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display Variable Air Trimmer Capacitor Component Class calculation
        results.

        :param rtk.Component part: the current instance of the rtk.Component()
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = Capacitor.reliability_results_create(self, part, layout,
                                                        x_pos, y_pos)

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        # Remove the capacitance correction factor entry.  It is not
        # needed for this type of capacitor.
        layout.remove(part.txtPiCV)

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
            Variable Air Trimmer Capacitor Component Class.

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
            Performs MIL-HDBK-217F part stress hazard rate calculations for the
            Variable Air Trimmer Capacitor Component Class.

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
            Reff = partmodel.get_value(partrow, 95)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # 85C
                Tref = 358.0
            else:                           # Default
                Tref = 358.0

            _hrmodel['lambdab'] = 0.00000192 * ((S / 0.33)**3 + 1) * exp(10.8 * (Tamb + 273) / Tref)

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


class Gas(Capacitor):
    """
    Variable and Fixed Gas or Vacuum Capacitor Component Class.

    Covers specification MIL-C-23183.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 10.19
    """

    _construction = ["", "Fixed", "Variable"]
    _quality = ["", "MIL-SPEC", "Lower"]
    _specification = ["", "MIL-C-23183 (CT)"]
    _specsheet = [["", u"85\u00B0C", u"100\u00B0C", u"125\u00B0C"]]

    def __init__(self):
        """
        Initializes the Variable and Fixed Gas or Vacuum Capacitor Component
        Class.
        """

        Capacitor.__init__(self)

        self.subcategory = 58               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piCF = [0.10, 1.0]
        self._piE = [1.0, 3.0, 14.0, 8.0, 27.0, 10.0, 18.0, 70.0, 108.0, 40.0,
                     0.5, 0.0, 0.0, 0.0]
        self._piQ = [3.0, 20.0]
        self._lambdab_count = [0.4, 1.3, 6.8, 3.6, 13.0, 5.7, 10.0, 58.0, 90.0,
                               23.0, 20.0, 0.0, 0.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = u"Temperature Rating:"
        self._in_labels.append(u"Configuration:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CF</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels[6] = u"\u03C0<sub>CF</sub>:"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the widgets
        needed to select inputs for Variable and Fixed Gas or Vacuum Capacitor
        Component Class prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component()
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = Capacitor.assessment_inputs_create(self, part, layout,
                                                      x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the component specific display widgets.
        part.cmbConstruction = rtk.widgets.make_combo(simple=True)

        # Load all the gtk.ComboBox().
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[2])

        # Connect to callback methods.
        part.cmbConstruction.connect("changed", self.combo_callback, part, 16)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation input
        information.

        :param rtk.Component part: the current instance of the rtk.Component()
                                   class.
        """

        (_model, _row) = Capacitor.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))

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
            Variable and Fixed Gas or Vacuum Capacitor Component Class.

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
            Performs MIL-HDBK-217F part stress hazard rate calculations for the
            Variable and Fixed Gas or Vacuum Capacitor Component Class.

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
            _hrmodel['equation'] = "lambdab * piCF * piQ * piE"

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
            Reff = partmodel.get_value(partrow, 95)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Irated = partmodel.get_value(partrow, 92)

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 102)
            S = (Vapplied + sqrt(2) * VappliedAC) / Vrated
            if idx == 1:                    # 85C
                Tref = 358.0
            elif idx == 2:                  # 100C
                Tref = 373.0
            elif idx == 3:                  # 125C
                Tref = 398.0
            else:                           # Default
                Tref = 358.0

            _hrmodel['lambdab'] = 0.0112 * ((S / 0.17)**3 + 1) * exp(1.59 * ((Tamb + 273) / Tref)**10.1)

            # Configuration correction factor.
            idx = partmodel.get_value(partrow, 16)
            _hrmodel['piCF'] = self._piCF[idx - 1]

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
            partmodel.set_value(partrow, 70, _hrmodel['piCF'])

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
