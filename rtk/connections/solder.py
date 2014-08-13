#!/usr/bin/env python
"""
This is the solder connection class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       solder.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

try:
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    import rtk.widgets as _widg
except ImportError:
    import calculations as _calc
    import configuration as _conf
    import widgets as _widg
from connection import Connection

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class PTH(Connection):
    """
    Plated Through Hole Connection Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 16.1.
    """

    _technology = [u"", _(u"Printed Wiring Assembly with PTHs"),
                   _(u"Discrete Wiring with Electroless Deposited PTH")]
    _quality = ["", "MIL-SPEC", _(u"Lower")]

    def __init__(self):
        """
        Initializes the Plated Through Hole Connection Component Class.
        """

        Connection.__init__(self)

        self.subcategory = 75               # Subcategory ID in rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [0.00041, 0.00026]
        self._piE = [1.0, 2.0, 7.0, 5.0, 13.0, 5.0, 8.0, 16.0, 28.0, 19.0,
                     0.5, 10.0, 27.0, 500.0]
        self._piQ = [1.0, 2.0]
        self._lambdab_count = [0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 043, 0.85,
                               1.5, 1.0, 0.027, 0.53, 1.4, 27.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(_(u"Technology:"))
        self._in_labels.append(_(u"# of Circuit Planes:"))
        self._in_labels.append(_(u"# of Wave Soldered PTH:"))
        self._in_labels.append(_(u"# of Hand Soldered PTH:"))

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>[N<sub>1</sub>\u03C0<sub>C</sub> + N<sub>2</sub>(\u03C0<sub>C</sub> + 13)]\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>C</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Plated Through Hole Connection
        Component Class prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Connection.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 35

        # Create the display widgets specific to the PTH.
        part.cmbTechnology = _widg.make_combo(simple=True)
        # Create the Number of Circuit Planes Entry.  We store this value
        # in the number_elements field in the program database.
        part.txtNumberPlanes = _widg.make_entry()
        part.txtNumberWave = _widg.make_entry()
        part.txtNumberHand = _widg.make_entry()

        # Load the gtk.ComboBox().
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.put(part.txtNumberPlanes, _x_pos, _y_pos[3])
        layout.put(part.txtNumberWave, _x_pos, _y_pos[4])
        layout.put(part.txtNumberHand, _x_pos, _y_pos[5])

        # Connect to callback methods.
        part.cmbTechnology.connect('changed', self._callback_combo, part, 104)
        part.txtNumberPlanes.connect('focus-out-event', self._callback_entry,
                                     part, 'float', 58)
        part.txtNumberWave.connect('focus-out-event', self._callback_entry,
                                   part, 'float', 61)
        part.txtNumberHand.connect('focus-out-event', self._callback_entry,
                                   part, 'float', 59)

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

        (_model, _row) = Connection.assessment_inputs_load(self, part)

        part.cmbTechnology.set_active(int(_model.get_value(_row, 104)))
        part.txtNumberPlanes.set_text(str('{0:0.0f}'.format(
            _model.get_value(_row, 58))))
        part.txtNumberHand.set_text(str('{0:0.0f}'.format(
            _model.get_value(_row, 59))))
        part.txtNumberWave.set_text(str('{0:0.0f}'.format(
            _model.get_value(_row, 61))))

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Plated Through Hole Connection Component Class
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Connection.reliability_results_create(self, part, layout,
                                                         x_pos, y_pos)

        # Create the reliability results display widgets.
        part.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)

        # Place the widgets on the gtk.Fixed()
        layout.put(part.txtPiC, _x_pos, _y_pos[3])
        layout.put(part.txtPiQ, _x_pos, _y_pos[4])

        layout.show_all()

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        (_model, _row) = Connection.assessment_results_load(self, part)

        part.txtPiC.set_text(str(fmt.format(_model.get_value(_row, 69))))
        part.txtPiQ.set_text(str('{0:0.2g}'.format(
            _model.get_value(_row, 79))))

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the PCB edge connector class.

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
            Plated Through Hole Connection Component Class.

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
            _hrmodel['equation'] = 'lambdab * piQ'

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Qidx = partmodel.get_value(partrow, 85)         # Quality index
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            #TODO: Lookup base hazard rate for PTH in MIL-HDBK-217.
            _hrmodel['lambdab'] = 1.0

            if Qidx == 1:
                _hrmodel['piQ'] = 1.0
            else:
                _hrmodel['piQ'] = 20.0

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
            the Plated Through Hole Connection Component Class.

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

            from math import exp

            _hrmodel = {}
            _hrmodel['equation'] = 'lambdab * (N1 * piC + N2 * (piC + 13.0)) * piQ * piE'

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
            Eidx = systemmodel.get_value(systemrow, 22)
            P = partmodel.get_value(partrow, 58)
            _hrmodel['N2'] = partmodel.get_value(partrow, 59)
            _hrmodel['N1'] = partmodel.get_value(partrow, 61)
            Qidx = partmodel.get_value(partrow, 85)
            Tidx = partmodel.get_value(partrow, 104)

            # Base hazard rate.
            _hrmodel['lambdab'] = self._lambdab[Tidx - 1]

            # Complexity correction factor.
            if Tidx == 1 and P > 1:
                _hrmodel['piC'] = 0.65 * P**0.63
            else:
                _hrmodel['piC'] = 1.0

            # Quality correction factor.
            _hrmodel['piQ'] = self._piQ[Qidx - 1]

            # Environmental correction factor.
            _hrmodel['piE'] = self._piE[Eidx - 1]

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

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 69, _hrmodel['piC'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 79, _hrmodel['piQ'])

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


class Solder(Connection):
    """
    Non-Plated Through Hole Connection Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 16.1.
    """

    _technology = [u"", _(u"Printed Wiring Assembly with PTHs"),
                   _(u"Discrete Wiring with Electroless Deposited PTH")]
    _quality = ["", _(u"All")]

    def __init__(self, type):
        """
        Initializes the Solder Connection Component Class.
        """

        Connection.__init__(self)

        if type == 1:
            self.subcategory = 76           # Subcategory ID in rtkcom DB.
            self._lambdab = 0.00012
            self._piQ = [1.0]
            self._lambdab_count = [0.00012, 0.00024, 0.00084, 0.00048, 0.0013,
                                   0.00048, 0.00072, 0.00072, 0.00096, 0.0019,
                                   0.00005, 0.0011, 0.0029, 0.050]
        elif type == 2:
            self._quality = ["", _(u"Automated with Daily Pull Test"),
                             _(u"Manual, MIL-SPEC Tools with Two Pull Test"),
                             _(u"Manual, MIL-SPEC Tools with One Pull Test"),
                             _(u"Lower")]
            self.subcategory = 83           # Subcategory ID in rtkcom DB.
            self._lambdab = 0.00026
            self._piQ = [1.0, 1.0, 2.0, 20.0]
            self._lambdab_count = [0.00026, 0.00052, 0.0018, 0.0010, 0.0029,
                                   0.0010, 0.0016, 0.0016, 0.0021, 0.0042,
                                   0.00013, 0.0023, 0.0062, 0.11]
        elif type == 3:
            self.subcategory = 84           # Subcategory ID in rtkcom DB.
            self._lambdab = 0.0026
            self._piQ = [1.0]
            self._lambdab_count = [0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010,
                                   0.016, 0.016, 0.021, 0.042, 0.0013, 0.023,
                                   0.062, 1.1]
        elif type == 8:
            self.subcategory = 85           # Subcategory ID in rtkcom DB.
            self._lambdab = 0.000069
            self._piQ = [1.0]
            self._lambdab_count = [0.000069, 0.000138, 0.000483, 0.000276,
                                   0.000759, 0.000276, 0.000414, 0.000414,
                                   0.000552, 0.001104, 0.000035, 0.000621,
                                   0.001656, 0.02898]
        elif type == 9:
            self.subcategory = 86           # Subcategory ID in rtkcom DB.
            self._lambdab = 0.00005
            self._piQ = [1.0]
            self._lambdab_count = [0.000050, 0.000100, 0.000350, 0.000200,
                                   0.000550, 0.000200, 0.000300, 0.000300,
                                   0.000400, 0.000800, 0.000025, 0.000450,
                                   0.001200, 0.021000]
        elif type == 10:
            self.subcategory = 87           # Subcategory ID in rtkcom DB.
            self._lambdab = 0.00014
            self._piQ = [1.0]
            self._lambdab_count = [0.00014, 0.00028, 0.00096, 0.00056, 0.0015,
                                   0.00056, 0.00084, 0.00084, 0.0011, 0.0022,
                                   0.00007, 0.0013, 0.0034, 0.059]

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 7.0, 4.0, 11.0, 4.0, 6.0, 6.0, 8.0, 16.0, 0.5,
                     9.0, 24.0, 420.0]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Plated Through Hole Connection
        Component Class prediction calculations.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Connection.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)
        _x_pos = max(x_pos, _x_pos) + 25

        # Place all the display widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Non-Plated Through Hole Connection Component
        Class calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = Connection.reliability_results_create(self, part, layout,
                                                         x_pos, y_pos)

        part.txtPiQ = _widg.make_entry(editable=False, bold=True)

        layout.put(part.txtPiQ, _x_pos, _y_pos[3])

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with calculation
        results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if succussful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = Connection.assessment_results_load(self, part)

        part.txtPiQ.set_text(str('{0:0.2g}'.format(
            _model.get_value(_row, 79))))

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the PCB edge connector class.

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
            Non-Plated Through Hole Connection Component Class.

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
            _hrmodel['equation'] = 'lambdab'

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            # TODO: Lookup lammbda_b in MIL-HDBK-217.
            _hrmodel['equation'] = 1.0

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
            the Non-Plated Through Hole Connection Component Class.

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

            from math import exp

            _hrmodel = {}
            _hrmodel['equation'] = 'lambdab * piQ * piE'

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
            Eidx = systemmodel.get_value(systemrow, 22)
            Qidx = partmodel.get_value(partrow, 85)

            # Base hazard rate.
            _hrmodel['lambdab'] = self._lambdab

            # Quality correction factor.
            _hrmodel['piQ'] = self._piQ[Qidx - 1]

            # Environmental correction factor.
            _hrmodel['piE'] = self._piE[Eidx - 1]

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

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 79, _hrmodel['piQ'])

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
