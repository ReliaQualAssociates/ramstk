#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       thyristor.py is part of The RTK Project
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
from semiconductor import Semiconductor

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Thyristor(Semiconductor):
    """
    Thyristor Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.10
    """

    def __init__(self):
        """
        Initializes the Thyristor Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 21               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [0.0025, 0.020, 0.034, 0.030, 0.072, 0.064, 0.14,
                               0.14, 0.31, 0.12, 0.0012, 0.053, 0.16, 1.1]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Rated Forward Current (I<sub>F</sub>):"))
        self._in_labels.append(_(u"Applied Voltage (V<sub>Applied</sub>):"))
        self._in_labels.append(_(u"Rated Voltage (V<sub>Rated</sub>):"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>R</sub>:")
        self._out_labels.append(u"\u03C0<sub>S</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Thyristor prediction
        calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 45

        # Create component specific input widgets.
        part.txtFwdCurrent = _widg.make_entry(width=100)
        part.txtVApplied = _widg.make_entry(width=100)
        part.txtVRated = _widg.make_entry(width=100)

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.txtFwdCurrent, _x_pos, _y_pos[3])
        layout.put(part.txtVApplied, _x_pos, _y_pos[4])
        layout.put(part.txtVRated, _x_pos, _y_pos[5])

        # Connect component specific widgets to callback methods.
        part.txtFwdCurrent.connect("focus-out-event", self._callback_entry,
                                   part, "float", 62)
        part.txtVApplied.connect("focus-out-event", self._callback_entry,
                                 part, "float", 66)
        part.txtVRated.connect("focus-out-event", self._callback_entry,
                               part, "float", 94)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Thyristor calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiR = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiS = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specifci reliability result display widgets.
        layout.put(part.txtPiR, _x_pos, _y_pos[5])
        layout.put(part.txtPiS, _x_pos, _y_pos[6])

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

        (_model, _row) = Semiconductor.assessment_inputs_load(self, part)

        part.txtFwdCurrent.set_text(str(fmt.format(
            _model.get_value(_row, 62))))
        part.txtVApplied.set_text(str(fmt.format(_model.get_value(_row, 66))))
        part.txtVRated.set_text(str(fmt.format(_model.get_value(_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Semiconductor.assessment_results_load(self, part)

        part.txtPiR.set_text(str(fmt.format(_model.get_value(_row, 80))))
        part.txtPiS.set_text(str(fmt.format(_model.get_value(_row, 81))))

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
            Thyristor Class.

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
            the Thyristor Class.

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
            _hrmodel['equation'] = "lambdab * piT * piR * piS * piQ * piE"

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
            P = partmodel.get_value(partrow, 64)
            Trise = partmodel.get_value(partrow, 107)
            thetaJC = partmodel.get_value(partrow, 109)

            # Retrieve hazard rate inputs.
            IF = partmodel.get_value(partrow, 62)
            VApplied = partmodel.get_value(partrow, 66)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            VRated = partmodel.get_value(partrow, 94)
            _hrmodel['lambdab'] = 0.0022

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

            # Junction temperature.
            Tj = Tcase + thetaJC * P

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-3082.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Current rating correction factor.
            _hrmodel['piR'] = IF**0.4

            # Voltage stress correction factor.  We store this in the pi_sr
            # field in the Program Database.
            Vs = VApplied / VRated
            if Vs > 0.3:
                _hrmodel['piS'] = Vs**1.9
            else:
                _hrmodel['piS'] = 0.10

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

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 80, _hrmodel['piR'])
            partmodel.set_value(partrow, 81, _hrmodel['piS'])
            partmodel.set_value(partrow, 82, _hrmodel['piT'])

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
