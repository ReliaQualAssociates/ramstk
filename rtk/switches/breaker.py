#!/usr/bin/env python
"""
breaker.py contains the circuit breaker component class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       breaker.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale

from math import exp, sqrt

try:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
from switch import Switch

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Breaker(Switch):
    """
    Circuit Breaker Switch Component Class.
    Covers specifications MIL-C-55629, MIL-C-83383, MIL-C-39019, and W-C-375.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 14.1
    """

    _application = ["", _(u"Not Used as Power On/Off Switch"),
                    _(u"Used as Power On/Off Switch")]
    _construction = ["", _(u"Magnetic"), _(u"Thermal"), _(u"Thermal-Magnetic")]
    _form = ["", u"SPST", u"DPST", u"3PST", u"4PST"]
    _quality = ["", u"MIL-SPEC", _(u"Lower")]

    def __init__(self):
        """
        Initializes the Circuit Breaker Switch Component Class.
        """

        Switch.__init__(self)

        self.subcategory = 71               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piC = [1.0, 2.0, 3.0, 4.0]
        self._piE = [1.0, 2.0, 15.0, 8.0, 27.0, 7.0, 9.0, 11.0, 12.0, 46.0,
                     0.5, 25.0, 67.0, 0.0]
        self._piQ = [1.0, 8.4]
        self._piU = [1.0, 10.0]
        self._lambdab = [0.020, 0.038, 0.038]
        self._lambdab_count = [0.060, 0.12, 0.90, 0.48, 1.6, 0.42, 0.54, 0.66,
                               0.72, 2.8, 0.030, 1.5, 4.0, 0.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Quality:"))
        self._in_labels.append(_(u"\u03C0<sub>Q</sub> Override:"))
        self._in_labels.append(_(u"Construction:"))
        self._in_labels.append(_(u"Contact Form:"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>:")
        self._out_labels.append(u"\u03C0<sub>U</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the widgets
        needed to select inputs for Circuit Breaker Switch Component Class
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
         _y_pos) = Switch.assessment_inputs_create(self, part, layout,
                                                   x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the component specific input widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.cmbConstruction = _widg.make_combo(simple=True)
        # Create the contact form ComboBox.  We store the index value in the
        # func_id field in the program database.
        part.cmbForm = _widg.make_combo(simple=True)

        # Load the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        for i in range(len(self._form)):
            part.cmbForm.insert_text(i, self._form[i])

        # Place the component specific input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbApplication, _x_pos, _y_pos[0])
        layout.move(part.txtCycleRate, _x_pos, _y_pos[1])
        layout.move(part.txtCurrentRated, _x_pos, _y_pos[2])
        layout.move(part.txtCurrentOper, _x_pos, _y_pos[3])
        layout.put(part.cmbQuality, _x_pos, _y_pos[4])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[5])
        layout.put(part.cmbConstruction, _x_pos, _y_pos[6])
        layout.put(part.cmbForm, _x_pos, _y_pos[7])

        # Connect the component specific widgets to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)
        part.cmbConstruction.connect("changed", self._callback_combo, part, 16)
        part.cmbForm.connect("changed", self._callback_combo, part, 30)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display Circuit Breaker Switch Component Class calculation results.

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
         _y_pos) = Switch.reliability_results_create(self, part, layout,
                                                     x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos)

        # Create the component specific reliability result display widgets.
        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiU = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the component specific reliability result display widgets.
        layout.move(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.move(part.txtPiE, _x_pos, _y_pos[2])
        layout.put(part.txtPiC, _x_pos, _y_pos[3])
        layout.put(part.txtPiU, _x_pos, _y_pos[4])
        layout.put(part.txtPiQ, _x_pos, _y_pos[5])

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation input
        information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Switch.assessment_inputs_load(self, part)

        part.cmbConstruction.set_active(int(_model.get_value(_row, 16)))
        part.cmbForm.set_active(int(_model.get_value(_row, 30)))
        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        if int(_model.get_value(_row, 85)) <= 0:
            part.txtCommercialPiQ.set_text(str(fmt.format(
                _model.get_value(_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Switch.assessment_results_load(self, part)

        part.txtPiC.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 69))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))
        part.txtPiU.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 82))))

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
            Circuit Breaker Switch Component Class.

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
            Qidx = partmodel.get_value(partrow, 85)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

            if Qidx == 1:
                _hrmodel['piQ'] = 1.0
            else:
                _hrmodel['piQ'] = 8.4

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
            the Circuit Breaker Switch Component Class.

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
            _hrmodel['equation'] = "lambdab * piC * piU * piQ * piE"

            # Retrieve the part category, subcategory, active environment,
            # dormant environment, software hazard rate, and quantity.
            # TODO: Replace these with instance attributes after splitting out Assembly and Component as sub-classes of Hardware.
            _category_id = systemmodel.get_value(systemrow, 11)
            _subcategory_id = systemmodel.get_value(systemrow, 78)
            _active_env = systemmodel.get_value(systemrow, 22)
            _dormant_env = systemmodel.get_value(systemrow, 23)
            _lambdas = systemmodel.get_value(systemrow, 33)
            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Aidx = partmodel.get_value(partrow, 5)
            Cidx = partmodel.get_value(partrow, 16)
            Fidx = partmodel.get_value(partrow, 30)
            Qidx = partmodel.get_value(partrow, 85)

            # Base hazard rate.
            _hrmodel['lambdab'] = self._lambdab[Cidx - 1]

            # Quality correction factor.
            _hrmodel['piQ'] = self._piQ[Qidx - 1]

            # Contact for correction factor.
            _hrmodel['piC'] = self._piC[Fidx - 1]

            # Usage correction factor.
            _hrmodel['piU'] = self._piU[Aidx - 1]

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

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 69, _hrmodel['piC'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 79, _hrmodel['piQ'])
            partmodel.set_value(partrow, 82, _hrmodel['piU'])

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
