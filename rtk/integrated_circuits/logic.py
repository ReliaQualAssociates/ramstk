#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       logic.py is part of The RTK Project
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
except:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
from ic import IntegratedCircuit

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Logic(IntegratedCircuit):
    """
    Logic (digital) integrated circuit class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.1
    """

    # For family combobox item list.
    _family = ["", "TTL", "ASTTL", "CML", "HTTL", "FTTL", "DTL", "ECL",
               "ALSTTL", "FLTTL", "STTL", "BiCMOS", "LSTTL", "III", "IIIL",
               "ISL"]

    def __init__(self):
        """ Initializes the Logic IC Component Class. """

        IntegratedCircuit.__init__(self)

        self.subcategory = 2                # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[0.0025, 0.005, 0.01, 0.02, 0.04, 0.08],
                    [0.01, 0.02, 0.04, 0.08, 0.16, 0.29]]
        self._Ea = [[0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.45, 0.45, 0.5,
                     0.5, 0.6, 0.6, 0.6],
                    [0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35,
                     0.35, 0.35, 0.35, 0.35, 0.35, 0.35]]

        self._lambdab_count = [[[0.0036, 0.012, 0.024, 0.024, 0.035, 0.025,
                                 0.030, 0.032, 0.049, 0.047, 0.0036, 0.030,
                                 0.069, 1.20],
                                [0.0060, 0.020, 0.038, 0.037, 0.055, 0.039,
                                 0.048, 0.051, 0.077, 0.074, 0.0060, 0.046,
                                 0.110, 1.90],
                                [0.0110, 0.035, 0.066, 0.065, 0.097, 0.070,
                                 0.085, 0.091, 0.140, 0.130, 0.0110, 0.082,
                                 0.190, 3.30],
                                [0.0330, 0.120, 0.220, 0.220, 0.330, 0.230,
                                 0.280, 0.300, 0.460, 0.440, 0.0330, 0.280,
                                 0.650, 12.0],
                                [0.0520, 0.170, 0.330, 0.330, 0.480, 0.340,
                                 0.420, 0.450, 0.680, 0.650, 0.0520, 0.410,
                                 0.950, 17.0],
                                [0.0750, 0.230, 0.440, 0.430, 0.630, 0.460,
                                 0.560, 0.610, 0.900, 0.850, 0.0750, 0.530,
                                 1.200, 21.0]],
                               [[0.0057, 0.015, 0.027, 0.027, 0.039, 0.029,
                                 0.035, 0.039, 0.056, 0.052, 0.0057, 0.033,
                                 0.074, 1.20],
                                [0.0100, 0.028, 0.045, 0.043, 0.062, 0.049,
                                 0.057, 0.068, 0.092, 0.083, 0.0100, 0.053,
                                 0.120, 1.90],
                                [0.0190, 0.047, 0.080, 0.077, 0.110, 0.088,
                                 0.100, 0.120, 0.170, 0.150, 0.0190, 0.095,
                                 0.210, 3.30],
                                [0.0490, 0.140, 0.250, 0.240, 0.360, 0.270,
                                 0.320, 0.360, 0.510, 0.480, 0.0490, 0.300,
                                 0.690, 12.0],
                                [0.0840, 0.220, 0.390, 0.370, 0.540, 0.420,
                                 0.490, 0.560, 0.790, 0.720, 0.0840, 0.460,
                                 1.000, 17.0],
                                [0.1300, 0.310, 0.530, 0.510, 0.730, 0.590,
                                 0.690, 0.820, 1.100, 0.980, 0.1300, 0.830,
                                 1.400, 21.0]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[3] = _(u"# of Gates:")
        self._in_labels.append(_(u"Family:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Logic Integrated Circuit
        prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the Logic IC specific input display widgets.
        part.cmbFamily = _widg.make_combo(simple=True)

        # Update or load all the gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text("1 to 100")
        part.cmbElements.append_text("101 to 1000")
        part.cmbElements.append_text("1001 to 3000")
        part.cmbElements.append_text("3001 to 10000")
        part.cmbElements.append_text("10001 to 30000")
        part.cmbElements.append_text("30001 to 60000")

        for i in range(len(self._family)):
            part.cmbFamily.insert_text(i, self._family[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])
        layout.put(part.cmbFamily, _x_pos, _y_pos[7])

        # Connect to callback methods.
        part.cmbFamily.connect("changed", self._callback_combo, part, 28)

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

        (_model, _row) = IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(_model.get_value(_row, 24)))
        part.cmbFamily.set_active(int(_model.get_value(_row, 28)))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Logic IC Class ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        IntegratedCircuit._callback_combo(self, combo, part, idx)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        # The family (Logic IC only) combobox called the function.
        _index = combo.get_active()
        _index2 = part.cmbTechnology.get_active()

        _model.set_value(_row, 22, self._Ea[_index2 - 1][_index - 1])

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
            Linear Integrated Circuit Class.

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
            _hrmodel['equation'] = "lambdab * piQ * piL"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)    # Environment index

            Bidx = partmodel.get_value(partrow, 24)     # No. of elements index
            Tidx = partmodel.get_value(partrow, 104)    # Technology index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity / 1000000.0

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 32, _lambdaa)
            systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

            return False

        def _calculate_mil_217_stress(partmodel, partrow,
                                      systemmodel, systemrow):
            """
            Performs MIL-HDBK-217F part stress hazard rate calculations for
            the Logic Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT + C2 * piE) * piQ * piL"

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
            P = partmodel.get_value(partrow, 64)

            # Retrieve hazard rate inputs.
            _hrmodel['C1'] = partmodel.get_value(partrow, 8)
            Ea = partmodel.get_value(partrow, 22)
            K5 = partmodel.get_value(partrow, 35)
            K6 = partmodel.get_value(partrow, 36)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            # Retrieve stress inputs.
            Iapplied = partmodel.get_value(partrow, 62)
            Vapplied = partmodel.get_value(partrow, 66)
            Irated = partmodel.get_value(partrow, 92)
            Vrated = partmodel.get_value(partrow, 94)

            # Calculate junction temperature.  If ambient temperature and
            # temperature rise are not set (i.e., equal to zero), use the
            # default case temperature values that are based on the active
            # environment.  Otherwise calculate case temperature.
            if Tamb == 0 and Trise == 0:
                idx = int(systemmodel.get_value(systemrow, 22))
                Tcase = self._Tcase[idx - 1]
            else:
                Tcase = Tamb + Trise

            # Determine the junction-case thermal resistance.  If thetaJC is
            # not set (i.e., equal to zero), use the default value which is
            # based on the package type.
            if thetaJC == 0:
                idx = int(partmodel.get_value(partrow, 67))
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * Ea / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))
            _hrmodel['C2'] = K5 * (Np ** K6)

            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piL'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])
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
