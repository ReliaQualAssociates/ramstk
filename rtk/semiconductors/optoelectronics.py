#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       optoelectronics.py is part of The RTK Project
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


class Detector(Semiconductor):
    """
    Photodetector Component Class.  Includes photodetectors, optoisolators,
    and photoemitters.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.11
    """

    _application = ["", _(u"Photodetector"), _(u"Optoisolator"), _(u"Emitter")]
    _detector = ["", _(u"Phototransistor"), _(u"Photodiode")]
    _isolator = ["", _(u"Photodiode Output, Single Device"),
                 _(u"Phototransistor Output, Single Device"),
                 _(u"Photodarlington Output, Single Device"),
                 _(u"Light Sensitive Resistor, Single Device"),
                 _(u"Photodiode Output, Dual Device"),
                 _(u"Phototransistor Output, Dual Device"),
                 _(u"Photodarlington Output, Dual Device"),
                 _(u"Light Sensitive Resistor, Dual Device")]
    _emitter = ["", _(u"Infrared Light Emitting Diode (IRLED)"),
                _(u"Light Emitting Diode (LED)")]
    _construction = ["", _(u"With Logic Chip"), _(u"Without Logic Chip")]

    def __init__(self):
        """
        Initializes the Photodetector Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 22               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [[0.0055, 0.0040],
                         [0.0025, 0.013, 0.013, 0.0064, 0.0033, 0.017, 0.017,
                          0.0086], [0.0013, 0.00023]]
        self._piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5,
                     9.0, 24.0, 450.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.01100, 0.0290, 0.0830, 0.0590, 0.1800,
                                0.0840, 0.1100, 0.2100, 0.3500, 0.3400,
                                0.00570, 0.1500, 0.510, 3.70],
                               [0.02700, 0.0700, 0.2000, 0.1400, 0.4300,
                                0.2000, 0.2500, 0.4900, 0.8300, 0.8000,
                                0.01300, 0.3500, 1.200, 8.70],
                               [0.00047, 0.0012, 0.0035, 0.0025, 0.0077,
                                0.0035, 0.0044, 0.0086, 0.0150, 0.0140,
                                0.00024, 0.0053, 0.021, 0.15]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Type:"))
        self._in_labels.append(_(u"Construction:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Photodetector Component Class
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
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos)

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.cmbConstruction = _widg.make_combo(simple=True)

        # Load the gtk.ComboBox()
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[4])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)

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

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Photodetector Component Class
        ComboBox changes.

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

        Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Application
            if _index == 1:
                for i in range(len(self._detector)):
                    part.cmbConstruction.insert_text(i, self._detector[i])

            elif _index == 2:
                for i in range(len(self._isolator)):
                    part.cmbConstruction.insert_text(i, self._isolator[i])

            elif _index == 3:
                for i in range(len(self._emitter)):
                    part.cmbConstruction.insert_text(i, self._emitter[i])

            part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))

        elif idx == 16:                     # Construction
            _index2 = _model.get_value(_row, 5)
            _model.set_value(_row, 46, self._lambdab[_index2 - 1][_index - 1])

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
            Photodetector Component Class.

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
            Aidx = partmodel.get_value(partrow, 5)          # Application
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            _hrmodel['lambdab'] = self._lambdab_count[Aidx - 1][Eidx - 1]

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
            the Photodetector Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piQ * piE"

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
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            _hrmodel['piT'] = exp(-2790.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class Display(Semiconductor):
    """
    Alphanumeric Display Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.12
    """

    _application = ["", _(u"Segment"), _(u"Diode Array")]
    _construction = ["", _(u"With Logic Chip"), _(u"Without Logic Chip")]

    def __init__(self):
        """
        Initializes the Alphanumeric Display Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 23               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdaIC = [0.000043, 0.0]
        self._piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5,
                     9.0, 24.0, 450.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.0062, 0.016, 0.045, 0.032, 0.10, 0.046,
                                0.058, 0.11, 0.19, 0.18, 0.0031, 0.082, 0.28,
                                2.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Display Type:"))
        self._in_labels.append(_(u"Construction:"))
        self._in_labels.append(_(u"# of Segments:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Alphanumeric Display Component
        Class prediction calculations.

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
        _x_pos = max(x_pos, _x_pos)

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtNumSegments = _widg.make_entry(width=100)

        # Load the gtk.ComboBox()
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[4])
        layout.put(part.txtNumSegments, _x_pos, _y_pos[5])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtNumSegments.connect("focus-out-event", self._callback_entry,
                                    part, "float", 58)

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

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        part.txtNumSegments.set_text(str("{0:0.0g}".format(
            _model.get_value(_row, 58))))

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
            Alphanumeric Display Component Class.

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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
            the Alphanumeric Display Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piQ * piE"

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
            C = partmodel.get_value(partrow, 58)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

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

            # Base hazard rate.
            idx = partmodel.get_value(partrow, 16)
            lambdaIC = self._lambdaIC[idx - 1]

            idx = partmodel.get_value(partrow, 5)
            if idx == 1:
                _hrmodel['lambdab'] = 0.00043 * float(C) + lambdaIC
            else:
                _hrmodel['lambdab'] = 0.00009 + 0.00017 * float(C) + lambdaIC

            # Temperature correction factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = exp(-2790.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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


class LaserDiode(Semiconductor):
    """
    Laser Diode Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 6.13
    """

    _application = ["", _(u"Continuous"), _(u"Pulsed")]
    _construction = ["", "GaAs/Al GaAs", "In GaAs/In GaAsP"]
    _quality = ["", _(u"Hermetic Packaging"),
                _(u"Nonhermetic with Facet Coating"),
                _(u"Nonhermetic without Facet Coating")]

    def __init__(self):
        """
        Initializes the Laser Diode Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 24               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [3.23, 5.65]
        self._piE = [1.0, 2.0, 8.0, 5.0, 12.0, 4.0, 6.0, 6.0, 8.0, 17.0, 0.5,
                     9.0, 24.0, 450.0]
        self._piQ = [1.0, 1.0, 3.3]
        self._lambdab_count = [[5.1, 16.0, 49.0, 32.0, 110.0, 58.0, 72.0,
                                100.0, 170.0, 230.0, 2.6, 87.0, 350.0, 2000.0],
                               [8.9, 28.0, 85.0, 55.0, 190.0, 100.0, 130.0,
                                180.0, 300.0, 400.0, 4.5, 150.0, 600.0,
                                3500.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Duty Cycle:"))
        self._in_labels.append(_(u"Technology:"))
        self._in_labels.append(_(u"Peak Fwd Current(I<sub>Fpk</sub>):"))
        self._in_labels.append(_(u"Rated Optical Pwr(P<sub>Rated</sub>):"))
        self._in_labels.append(_(u"Required Optical Pwr(P<sub>Rqd</sub>):"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>C</sub>\u03C0<sub>I</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>I</sub>:")
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>P</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Laser Diode Component Class
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
         _y_pos) = Semiconductor.assessment_inputs_create(self, part, layout,
                                                          x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 45

        # Create component specific input widgets.
        part.cmbApplication = _widg.make_combo(simple=True)
        part.txtDutyCycle = _widg.make_entry(width=100)
        part.cmbConstruction = _widg.make_combo(simple=True)
        part.txtFwdCurrent = _widg.make_entry(width=100)
        # Create the rated optical power entry.  We store these results
        # in the operating_freq field in the program database.
        part.txtRatedOptPwr = _widg.make_entry(width=100)
        part.txtRqdOptPwr = _widg.make_entry(width=100)

        # Load the gtk.ComboBox().
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.cmbPackage, _x_pos, _y_pos[1])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[2])
        layout.put(part.cmbApplication, _x_pos, _y_pos[3])
        layout.put(part.txtDutyCycle, _x_pos, _y_pos[4])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[5])
        layout.put(part.txtFwdCurrent, _x_pos, _y_pos[6])
        layout.put(part.txtRatedOptPwr, _x_pos, _y_pos[7])
        layout.put(part.txtRqdOptPwr, _x_pos, _y_pos[8])

        # Connect component specific widgets to callback methods.
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.txtDutyCycle.connect("focus-out-event", self._callback_entry,
                                  part, "float", 19)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.txtFwdCurrent.connect("focus-out-event", self._callback_entry,
                                   part, "float", 62)
        part.txtRatedOptPwr.connect("focus-out-event", self._callback_entry,
                                    part, "float", 63)
        part.txtRqdOptPwr.connect("focus-out-event", self._callback_entry,
                                  part, "float", 93)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Laser Diode Component Class calculation
        results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Semiconductor.reliability_results_create(self, part, layout,
                                                            x_pos, y_pos)

        # Create component specific reliability result display widgets.
        part.txtPiI = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiP = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.put(part.txtPiI, _x_pos, _y_pos[5])
        layout.put(part.txtPiA, _x_pos, _y_pos[6])
        layout.put(part.txtPiP, _x_pos, _y_pos[7])

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

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        part.txtDutyCycle.set_text(str(fmt.format(
            _model.get_value(_row, 19))))
        part.txtFwdCurrent.set_text(str(fmt.format(
            _model.get_value(_row, 62))))
        part.txtRatedOptPwr.set_text(str(fmt.format(
            _model.get_value(_row, 63))))
        part.txtRqdOptPwr.set_text(str(fmt.format(_model.get_value(_row, 93))))

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

        part.txtPiA.set_text(str(fmt.format(_model.get_value(_row, 68))))
        part.txtPiI.set_text(str(fmt.format(_model.get_value(_row, 75))))
        part.txtPiP.set_text(str(fmt.format(_model.get_value(_row, 78))))

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Laser Diode Component Class
        ComboBox changes.

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

        Semiconductor._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Duty cycle
            if _index == 2:
                part.txtDutyCycle.show()
            else:
                part.txtDutyCycle.hide()

        elif idx == 16:                     # Construction
            _model.set_value(_row, 46, self._lambdab[_index - 1])

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
            Laser Diode Component Class.

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
            Cidx = partmodel.get_value(partrow, 16)         # Construction index
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

            _hrmodel['lambdab'] = self._lambdab_count[Cidx - 1][Eidx - 1]

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
            the Laser Diode Component Class.

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
            _hrmodel['equation'] = "lambdab * piT * piI * piA * piP * piQ * piE"

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
            DC = partmodel.get_value(partrow, 19)
            _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
            IF = partmodel.get_value(partrow, 62)
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Prated = partmodel.get_value(partrow, 63)
            Prqd = partmodel.get_value(partrow, 93)

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
            _hrmodel['piT'] = exp(-4635.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Forward current correction factor.
            _hrmodel['piI'] = IF**0.68

            # Application correction factor.
            if partmodel.get_value(partrow, 5) == 1:
                _hrmodel['piA'] = 4.4
            else:
                _hrmodel['piA'] = DC**0.5

            # Power degradation correction factor.
            _hrmodel['piP'] = 1.0 / (2.0 * (1 - (Prqd / Prated)))

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
            _lambdad = _lambdad * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdad + _lambdas

            # Calculate overstresses.
            (_overstress,
             self.reason) = _calc.overstressed(partmodel, partrow,
                                               systemmodel, systemrow)

            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 68, _hrmodel['piA'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 75, _hrmodel['piI'])
            partmodel.set_value(partrow, 78, _hrmodel['piP'])
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
