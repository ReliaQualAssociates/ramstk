#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       palpla.py is part of The RTK Project
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


class PALPLA(IntegratedCircuit):
    """
    PAL/PLA device class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.1
    """

    def __init__(self):
        """
        Initializes the PAL/PLA IC Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 3                # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[0.01, 0.021, 0.042], [0.00085, 0.0017, 0.0034, 0.0068]]
        self._Ea = [[0.65], [0.65]]

        self._lambdab_count = [[[0.0061, 0.016, 0.029, 0.027, 0.040, 0.032,
                                 0.037, 0.044, 0.061, 0.054, 0.0061, 0.034,
                                 0.076, 1.2],
                                [0.0110, 0.028, 0.048, 0.046, 0.065, 0.054,
                                 0.063, 0.077, 0.100, 0.089, 0.0110, 0.057,
                                 0.120, 1.9],
                                [0.0220, 0.052, 0.087, 0.082, 0.120, 0.099,
                                 0.110, 0.140, 0.190, 0.160, 0.0220, 0.100,
                                 0.220, 3.3]],
                               [[0.0046, 0.018, 0.035, 0.035, 0.052, 0.035,
                                 0.044, 0.044, 0.070, 0.070, 0.0046, 0.044,
                                 0.100, 1.9],
                                [0.0056, 0.021, 0.042, 0.042, 0.062, 0.042,
                                 0.052, 0.053, 0.084, 0.083, 0.0056, 0.052,
                                 0.120, 2.3],
                                [0.0061, 0.022, 0.043, 0.042, 0.063, 0.043,
                                 0.054, 0.055, 0.086, 0.084, 0.0081, 0.053,
                                 0.130, 2.3],
                                [0.0095, 0.033, 0.064, 0.063, 0.094, 0.065,
                                 0.080, 0.083, 0.130, 0.130, 0.0095, 0.079,
                                 0.190, 3.3]]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels[2] = _(u"# of Gates:")
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for PAL/PLA Integrated Circuit
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

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        # Update the number of elements gtk.ComboBox().
        part.cmbElements.append_text("")
        if _model.get_value(_row, 104) == 1:      # Bipolar
            part.cmbElements.append_text("1 to 200")
            part.cmbElements.append_text("201 to 1000")
            part.cmbElements.append_text("1001 to 5000")
        elif _model.get_value(_row, 104) == 2:    # CMOS
            part.cmbElements.append_text("1 to 500")
            part.cmbElements.append_text("501 to 1000")
            part.cmbElements.append_text("1001 to 5000")
            part.cmbElements.append_text("5001 to 20000")

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Bidx = partmodel.get_value(partrow, 24)         # No of elements index
            Tidx = partmodel.get_value(partrow, 104)        # Technology index
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
            the Linear Integrated Circuit Class.

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
            K1 = partmodel.get_value(partrow, 40)
            K2 = partmodel.get_value(partrow, 41)
            K3 = partmodel.get_value(partrow, 42)
            K5 = partmodel.get_value(partrow, 35)
            K6 = partmodel.get_value(partrow, 36)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Tbase = partmodel.get_value(partrow, 103)
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
            _hrmodel['piT'] = 0.1 * exp((-1.0 * 0.65 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

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
