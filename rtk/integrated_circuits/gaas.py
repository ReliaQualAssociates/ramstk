#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       gaas.py is part of The RTK Project
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


class GaAsDigital(IntegratedCircuit):
    """
    Digital GaAs Integrated Circuit Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.4
    """

    def __init__(self):
        """
        Initializes the Digital GaAs Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 9                # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[25.0, 51.0], [25.0, 51.0]]

        self._lambdab_count = [[0.0085, 0.030, 0.057, 0.057, 0.084, 0.060,
                                0.073, 0.080, 0.12, 0.11, 0.0085, 0.071, 0.17,
                                3.0],
                               [0.0140, 0.053, 0.100, 0.100, 0.150, 0.110,
                                0.130, 0.140, 0.22, 0.21, 0.0140, 0.130, 0.31,
                                5.5]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Digital GaAs Integrated
        Circuit prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Update the number of elements gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text("1 to 1000")
        part.cmbElements.append_text("1001 to 10000")

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with reliability
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
            Digital GaAs Integrated Circuit Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)  # Environment index
            Bidx = partmodel.get_value(partrow, 24)      # No of elements index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity

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
            the Digital GaAs Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT * piA + C2 * piE) * piQ * piL"

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
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)
            _hrmodel['piA'] = 1.0

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
            idx = int(partmodel.get_value(partrow, 67))
            if thetaJC == 0:
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            # Junction temperature
            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * 1.4 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 423.0)))

            K5 = self._K5[idx - 1]
            K6 = self._K6[idx - 1]
            _hrmodel['C2'] = K5 * (Np ** K6)

            # Environment correction factor
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 35, K5)
            partmodel.set_value(partrow, 36, K6)
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


class GaAsMMIC(IntegratedCircuit):
    """
    Microwave Monolithic GaAs Integrated Circuit Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.4
    """

    _application = ["", _(u"Low Noise & Low Power (<100mW)"),
                    _(u"Driver & High Power (>100mW)"), _(u"Unknown")]

    def __init__(self):
        """
        Initializes the Microwave Monolithic GaAs Integrated Circuit Component
        Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 10               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[4.5, 7.2], [4.5, 7.2]]
        self._piA = [1.0, 3.0, 3.0]

        self._lambdab_count = [[0.0085, 0.030, 0.057, 0.057, 0.084, 0.060,
                                0.073, 0.080, 0.12, 0.11, 0.0085, 0.071, 0.17,
                                3.0],
                               [0.0140, 0.053, 0.100, 0.100, 0.150, 0.110,
                                0.130, 0.140, 0.22, 0.21, 0.0140, 0.130, 0.31,
                                5.5]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Microwave Monolithic GaAs
        Integrated Circuit prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.assessment_inputs_create(self, part,
                                                              layout,
                                                              x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the input display widgets specific to this class.
        part.cmbApplication = _widg.make_combo(simple=True)

        # Update and load all the gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text("1 to 100")
        part.cmbElements.append_text("101 to 1000")

        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])
        layout.put(part.cmbApplication, _x_pos, _y_pos[7])

        # Connec to callback methods.
        part.cmbApplication.connect("changed",
                                    self._callback_combo,
                                    part, 5)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Microwave Monolithic GaAs Integrated Circuit
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.reliability_results_create(self, part,
                                                                layout,
                                                                x_pos, y_pos)

        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)

        layout.move(part.txtC1, _x_pos, _y_pos[1])
        layout.move(part.txtPiT, _x_pos, _y_pos[2])
        layout.move(part.txtC2, _x_pos, _y_pos[3])
        layout.move(part.txtPiE, _x_pos, _y_pos[4])
        layout.move(part.txtPiQ, _x_pos, _y_pos[5])
        layout.move(part.txtPiL, _x_pos, _y_pos[6])
        layout.put(part.txtPiA, _x_pos, _y_pos[7])

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

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbElements.set_active(int(_model.get_value(_row, 24)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = IntegratedCircuit.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 68))))

        return False

    def _callback_combo(self, combo, part, _index_):
        """
        Callback function for handling ComboBox changes specific to the
        Microwave Monolithic GaAs Integrated Circuit Component Class.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        _index = combo.get_active()

        IntegratedCircuit.combo_callback(self, combo, part, _index_)

        if idx == 5:
            _model.set_value(_row, 68, self._piA[_index - 1])

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
            Microwave Monolithic GaAs Integrated Circuit Class.

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
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Y = partmodel.get_value(partrow, 112)

            _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity

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
            the Microwave Monolithic GaAs Integrated Circuit Class.

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
            _hrmodel['equation'] = "(C1 * piT * piA + C2 * piE) * piQ * piL"

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
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piA'] = partmodel.get_value(partrow, 68)
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
            idx = int(partmodel.get_value(partrow, 67))
            if thetaJC == 0:
                thetaJC = self._thetaJC[idx - 1]
                partmodel.set_value(partrow, 109, thetaJC)
            else:
                thetaJC = partmodel.get_value(partrow, 109)

            # Junction temperature
            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * 1.5 / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 423.0)))

            K5 = self._K5[idx - 1]
            K6 = self._K6[idx - 1]
            _hrmodel['C2'] = K5 * (Np ** K6)

            # Environment correction factor
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Calculate the learning factor.  We store this in the pi_r
            # field in the Program Database.
            _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

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

            partmodel.set_value(partrow, 9, _hrmodel['C2'])
            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 35, K5)
            partmodel.set_value(partrow, 36, K6)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 68, _hrmodel['piA'])
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
