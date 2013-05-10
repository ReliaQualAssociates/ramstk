#!/usr/bin/env python
""" These are the transistor component classes. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       transistor.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import relkit.calculations as _calc
    import relkit.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from semiconductor import Semiconductor


class LFBipolar(Semiconductor):
    """
    Low Frequency Bipolar Transistor Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.3
    """

    _application = ["", "Linear Amplification", "Switching"]

    def __init__(self):
        """
        Initializes the Low Frequency Bipolar Transistor Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 14               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piA = [1.5, 0.7]
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0,
                     0.5, 14.0, 32.0, 320.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0, 8.0]
        self._lambdab_count = [[0.00015, 0.0011, 0.0017, 0.0017, 0.0037, 0.0030, 0.0067, 0.0060, 0.013, 0.0056, 0.000073, 0.0027, 0.0074, 0.056],
                              [0.0057, 0.042, 0.069, 0.063, 0.15, 0.12, 0.26, 0.23, 0.50, 0.22, 0.0029, 0.11, 0.29, 1.1]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Application:")
        self._in_labels.append(u"Rated Power:")
        self._in_labels.append(u"Applied CE Voltage:")
        self._in_labels.append(u"Rated CE Voltage:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>R</sub>:")
        self._out_labels.append(u"\u03C0<sub>S</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Low Frequency Bipolar
        Transistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.txtPrated = _widg.make_entry(_width_=entry_width)
        part.txtPrated.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 93)
        layout.put(part.txtPrated, x_pos, y_pos)
        y_pos += 30

        # Create the applied CE voltage entry.
        part.txtOpVolts = _widg.make_entry(_width_=entry_width)
        part.txtOpVolts.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 66)
        layout.put(part.txtOpVolts, x_pos, y_pos)
        y_pos += 30

        # Create the rated CE voltage entry.
        part.txtRatedVolts = _widg.make_entry(_width_=entry_width)
        part.txtRatedVolts.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 94)
        layout.put(part.txtRatedVolts, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Low Frequency Bipolar Transistor Component
        Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiA = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
        y_pos += 30

        part.txtPiR = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiR, x_pos, y_pos)
        y_pos += 30

        part.txtPiS = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiS, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.txtOpVolts.set_text(str(fmt.format(part.model.get_value(part.selected_row, 66))))
        part.txtPrated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 93))))
        part.txtRatedVolts.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 68))))
        part.txtPiR.set_text(str(fmt.format(part.model.get_value(part.selected_row, 80))))
        part.txtPiS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 81))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Low Frequency Bipolar Transistor
        Component Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 5):                       # Application
            part._calc_data[68] = self._piA[idx - 1]
            model.set_value(row, 68, part._calc_data[68])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Low Frequency Bipolar Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # TODO: Validate index 64 is operating power.
        if(partmodel.get_value(partrow, 64) <= 0.1):
            Pidx = 0
        else:
            Pidx = 1

        _hrmodel['lambdab'] = self._lambdab_count[Pidx][Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Low Frequency Bipolar Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piR * piS * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        Vapplied = partmodel.get_value(partrow, 66)
        _hrmodel['piA'] = partmodel.get_value(partrow, 68)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)
        Vrated = partmodel.get_value(partrow, 94)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.00074

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-2114.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Power rating correction factor.
        if(Prated <= 0.1):
            _hrmodel['piR'] = 0.43
        else:
            _hrmodel['piR'] = Prated**0.37

        # Voltage stress correction factor.
        try:
            Vs = Vapplied / Vrated
        except:
            Vs = 1

        _hrmodel['piS'] = 0.045 * exp(3.1 * Vs)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 80, _hrmodel['piE'])
        partmodel.set_value(partrow, 81, _hrmodel['piS'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class LFSiFET(Semiconductor):
    """
    Low Frequency Silicon Field Effect Transistor (FET) Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.4
    """

    _application = ["", "Linear Amplification", "Small-Signal Switching",
                    "Power"]
    _technology = ["", "MOSFET", "JFET"]

    def __init__(self):
        """
        Initializes the Low Frequency Silicon FET Transistor Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 15               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [0.012, 0.0045]
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                     14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.014, 0.099, 0.16, 0.15, 0.34, 0.28, 0.62, 0.53, 1.1, 0.51, 0.0069, 0.25, 0.68, 5.3]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append("Application:")
        self._in_labels.append("Transistor Type:")
        self._in_labels.append("Rated Power:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Low Frequency Silicon FET
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.cmbTechnology = _widg.make_combo(simple=True)
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])
        part.cmbTechnology.connect("changed",
                                   self.combo_callback,
                                   part, 104)
        layout.put(part.cmbTechnology, x_pos, y_pos)
        y_pos += 30

        part.txtPrated = _widg.make_entry(_width_=entry_width)
        part.txtPrated.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 93)
        layout.put(part.txtPrated, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Low Frequency Silicon FET calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the current rating correction factor results entry.
        part.txtPiA = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.txtPrated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 93))))
        part.cmbTechnology.set_active(int(part.model.get_value(part.selected_row, 104)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 68))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Low Frequency Silicon FET Component
        Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 104):             # Technology
            part._calc_data[46] = self._lambdab[idx - 1]
            model.set_value(row, 46, part._calc_data[46])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Low Frequency Silicon FET Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Low Frequency Silicon FET Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piA * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-1925.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Application correction factor.
        idx = partmodel.get_value(partrow, 5)
        if(idx == 2):
            _hrmodel['piA'] = 0.7
        elif(Prated < 2.0):
            _hrmodel['piA'] = 1.5
        elif(Prated >= 2.0 and Prated < 5.0):
            _hrmodel['piA'] = 2.0
        elif(Prated >= 5.0 and Prated < 50.0):
            _hrmodel['piA'] = 4.0
        elif(Prated >= 50.0 and Prated < 250.0):
            _hrmodel['piA'] = 8.0
        elif(Prated >= 250.0):
            _hrmodel['piA'] = 10.0
        else:
            _hrmodel['piA'] = 1.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class Unijunction(Semiconductor):
    """
    Unijunction Transistor Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.5
    """

    def __init__(self):
        """ Initializes the Unijunction Transistor Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 16               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 6.0, 9.0, 9.0, 19.0, 13.0, 29.0, 20.0, 43.0, 24.0, 0.5,
                     14.0, 32.0, 320.0]
        self._piQ = [0.7, 1.0, 2.4, 5.5, 8.0]
        self._lambdab_count = [[0.016, 0.12, 0.20, 0.18, 0.42, 0.35, 0.80, 0.74, 1.6, 0.66, 0.0079, 0.31, 0.88, 6.4]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Unijunction Transistor
        Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Unijunction Transistor Component Class
        calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Unijunction Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Unijunction Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        _hrmodel['lambdab'] = partmodel.get_value(partrow, 46)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-2483.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class HFLNBipolar(Semiconductor):
    """
    High Frequency, Low Noise Bipolar Transistor Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.6
    """

    _quality = ["", "JANTXV", "JANTX", "JAN", "Lower"]

    def __init__(self):
        """
        Initializes the High Frequency, Low Noise Bipolar Transistor
        Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 17               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.094, 0.23, 0.63, 0.46, 1.4, 0.60, 0.75, 1.3, 2.3, 2.4, 0.047, 1.1, 3.6, 28.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append("Rated Power:")
        self._in_labels.append("Applied CE Voltage:")
        self._in_labels.append("Rated CE Voltage:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>R</sub>:")
        self._out_labels.append(u"\u03C0<sub>S</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency, Low Noise
        Bipolar Transistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        # Create the rated power entry.
        part.txtPrated = _widg.make_entry(_width_=entry_width)
        part.txtPrated.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 93)
        layout.put(part.txtPrated, x_pos, y_pos)
        y_pos += 30

        # Create the applied CE voltage entry.
        part.txtOpVolts = _widg.make_entry(_width_=entry_width)
        part.txtOpVolts.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 66)
        layout.put(part.txtOpVolts, x_pos, y_pos)
        y_pos += 30

        # Create the rated CE voltage entry.
        part.txtRatedVolts = _widg.make_entry(_width_=entry_width)
        part.txtRatedVolts.connect("focus-out-event",
                                   self.entry_callback,
                                   part, "float", 94)
        layout.put(part.txtRatedVolts, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display High Frequency, Low Noise Bipolar Transistor
        Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiR = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiR, x_pos, y_pos)
        y_pos += 30

        part.txtPiS = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiS, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.txtOpVolts.set_text(str(fmt.format(part.model.get_value(part.selected_row, 66))))
        part.txtPrated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 93))))
        part.txtRatedVolts.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_results_load(self, part)

        part.txtPiR.set_text(str(fmt.format(part.model.get_value(part.selected_row, 80))))
        part.txtPiS.set_text(str(fmt.format(part.model.get_value(part.selected_row, 81))))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        High Frequency, Low Noise Bipolar Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = lambdab * piQ

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the High Frequency, Low Noise Bipolar Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piR * piS * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        Vapplied = partmodel.get_value(partrow, 66)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Prated = partmodel.get_value(partrow, 93)
        Vrated = partmodel.get_value(partrow, 94)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.18

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-2114.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Power rating correction factor.
        if(Prated <= 0.1):
            _hrmodel['piR'] = 0.43
        else:
            _hrmodel['piR'] = Prated**0.37

        # Voltage stress correction factor.
        try:
            Vs = Vapplied / Vrated
        except:
            Vs = 1

        _hrmodel['piS'] = 0.45 * exp(3.1 * Vs)

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piR'])
        partmodel.set_value(partrow, 81, _hrmodel['piS'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class HFHPBipolar(Semiconductor):
    """
    High Frequency, High Power Bipolar Transistor Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.7
    """

    _application = ["", "Pulsed", "CW"]
    _construction = ["", "Gold Metallization", "Aluminum Metallization"]
    _matching = ["", "Input and Output", "Input Only", "None"]
    _quality = ["", "JANTXV", "JANTX", "JAN", "Lower"]

    def __init__(self):
        """
        Initializes the High Frequency, High Power Bipolar Transistor
        Component Class.
        """

        Semiconductor.__init__(self)

        self.subcategory = 18               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piM = [1.0, 2.0, 4.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.074, 0.15, 0.37, 0.29, 0.81, 0.29, 0.37, 0.52, 0.88, 0.037, 0.33, 0.66, 1.8, 18.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append("Application:")
        self._in_labels.append("Duty Cycle:")
        self._in_labels.append("Construction:")
        self._in_labels.append("CE Operating Voltage:")
        self._in_labels.append("CE Breakdown Voltage:")
        self._in_labels.append("Operating Frequency:")
        self._in_labels.append("Network Matching:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>M</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency, High Power
        Bipolar Transistor Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.txtDutyCycle = _widg.make_entry(_width_=entry_width)
        part.txtDutyCycle.connect("focus-out-event",
                                  self.entry_callback,
                                  part, "float", 19)
        layout.put(part.txtDutyCycle, x_pos, y_pos)
        y_pos += 30

        part.cmbConstruction = _widg.make_combo(simple=True)
        for i in range(len(self._construction)):
            part.cmbConstruction.insert_text(i, self._construction[i])
        part.cmbConstruction.connect("changed",
                                    self.combo_callback,
                                    part, 16)
        layout.put(part.cmbConstruction, x_pos, y_pos)
        y_pos += 30

        part.txtOpVolts = _widg.make_entry(_width_=entry_width)
        part.txtOpVolts.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 66)
        layout.put(part.txtOpVolts, x_pos, y_pos)
        y_pos += 30

        # Create the breakdown voltage entry.
        part.txtBDVolts = _widg.make_entry(_width_=entry_width)
        part.txtBDVolts.connect("focus-out-event",
                                self.entry_callback,
                                part, "float", 94)
        layout.put(part.txtBDVolts, x_pos, y_pos)
        y_pos += 30

        part.txtOpFreq = _widg.make_entry(_width_=entry_width)
        part.txtOpFreq.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 63)
        layout.put(part.txtOpFreq, x_pos, y_pos)
        y_pos += 30

        # Create the network matching combo.  We store this in the
        # technology_id field in the Program Database.
        part.cmbMatching = _widg.make_combo(simple=True)
        for i in range(len(self._matching)):
            part.cmbMatching.insert_text(i, self._matching[i])
        part.cmbMatching.connect("changed",
                                 self.combo_callback,
                                 part, 104)
        layout.put(part.cmbMatching, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display High Frequency, High Power Bipolar Transistor
        Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiA = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
        y_pos += 30

        part.txtPiM = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiM, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbConstruction.set_active(int(part.model.get_value(part.selected_row, 16)))
        part.txtDutyCycle.set_text(str(fmt.format(part.model.get_value(part.selected_row, 19))))
        part.txtOpFreq.set_text(str(fmt.format(part.model.get_value(part.selected_row, 63))))
        part.txtOpVolts.set_text(str(fmt.format(part.model.get_value(part.selected_row, 66))))
        part.txtBDVolts.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))
        part.cmbMatching.set_active(int(part.model.get_value(part.selected_row, 104)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 68))))
        part.txtPiM.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 76))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling High Frequency, High Power Bipolar
        Transistor Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 5):                       # Application
            if(idx == 1):
                part.txtDutyCycle.show()
            else:
                part.txtDutyCycle.hide()

        elif(_index_ == 104):                   # Network matching
            part._calc_data[76] = self._piM[idx - 1]
            model.set_value(row, 76, part._calc_data[76])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        High Frequency, High Power Bipolar Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the High Frequency, High Power Bipolar Transistor Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piA * piM * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        DC = partmodel.get_value(partrow, 19)
        Fop = partmodel.get_value(partrow, 63)
        Vop = partmodel.get_value(partrow, 66)
        _hrmodel['piM'] = partmodel.get_value(partrow, 76)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        VBD = partmodel.get_value(partrow, 94)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Base hazard rate.
        _hrmodel['lambdab'] = 0.032 * exp(0.354 * Fop + 0.00558 * P)

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        try:
            Vs = Vop / VBD
        except:
            Vs = 0.0

        if(Vs <= 0.4 and partmodel.get_value(partrow, 16) == 1):
            _hrmodel['piT'] = 0.1 * exp(-2903.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
        elif(Vs > 0.4 and partmodel.get_value(partrow, 16) == 1):
            _hrmodel['piT'] = 2 * (0.35 * Vs) * exp(-2903.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
        elif(Vs <= 0.4 and partmodel.get_value(partrow, 16) == 2):
            _hrmodel['piT'] = 0.38 * exp(-5794.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
        elif(Vs > 0.4 and partmodel.get_value(partrow, 16) == 2):
            _hrmodel['piT'] = 7.55 * (0.35 * Vs) * exp(-5794.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 373.0)))
        else:
            _hrmodel['piT'] = 0.0

        # Application correction factor.
        if(partmodel.get_value(partrow, 5) == 1):
            _hrmodel['piA'] = 0.06 * DC + 0.4
        elif(partmodel.get_value(partrow, 5) == 2):
            _hrmodel['piA'] = 7.6
        else:
            _hrmodel['piA'] = 0.0

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class HFGaAsFET(Semiconductor):
    """
    High Frequency Gallium Arsenide (GaAs) Field Effect Transistor (FET)
    Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.8
    """

    _application = ["", "Low Power and Pulsed", "CW"]
    _matching = ["", "Input and Output", "Input Only", "None"]
    _quality = ["", "JANTXV", "JANTX", "JAN", "Lower"]

    def __init__(self):
        """ Initializes the High Frequency GaAs FET Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 19               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piA = [1.0, 4.0]
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     7.5, 24.0, 250.0]
        self._piM = [1.0, 2.0, 4.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.17, 0.51, 1.5, 1.0, 3.4, 1.8, 2.3, 5.4, 9.2, 7.2, 0.083, 2.8, 11.0, 63.0],
                              [0.42, 1.3, 3.8, 2.5, 8.5, 4.5, 5.6, 13.0, 23.0, 18.0, 0.21, 6.9, 27.0, 160.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append("Application:")
        self._in_labels.append("Operating Frequency:")
        self._in_labels.append("Network Matching:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")
        self._out_labels.append(u"\u03C0<sub>M</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency GaAs FET
        Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)
        y_pos += 30

        part.txtOpFreq = _widg.make_entry(_width_=entry_width)
        part.txtOpFreq.connect("focus-out-event",
                               self.entry_callback,
                               part, "float", 63)
        layout.put(part.txtOpFreq, x_pos, y_pos)
        y_pos += 30

        # Create the network matching combo.  We store this in the
        # technology_id field in the Program Database.
        part.cmbMatching = _widg.make_combo(simple=True)
        for i in range(len(self._matching)):
            part.cmbMatching.insert_text(i, self._matching[i])
        part.cmbMatching.connect("changed",
                                 self.combo_callback,
                                 part, 104)
        layout.put(part.cmbMatching, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display High Frequency GaAs FET Component Class
        calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

        part.txtPiA = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiA, x_pos, y_pos)
        y_pos += 30

        part.txtPiM = _widg.make_entry(_width_=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiM, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.txtOpFreq.set_text(str(fmt.format(part.model.get_value(part.selected_row, 63))))
        part.cmbMatching.set_active(int(part.model.get_value(part.selected_row, 104)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        Semiconductor.assessment_results_load(self, part)

        part.txtPiA.set_text(str(fmt.format(part.model.get_value(part.selected_row, 68))))
        part.txtPiM.set_text(str(fmt.format(part.model.get_value(part.selected_row, 76))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling High Frequency GaAs FET Component
        Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 5):                       # Application
            part._calc_data[68] = self._piA[idx - 1]
            model.set_value(row, 68, part._calc_data[68])

        elif(_index_ == 104):                   # Network matching
            part._calc_data[76] = self._piM[idx - 1]
            model.set_value(row, 76, part._calc_data[76])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        High Frequency GaAs FET Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # TODO: Validate index 64 is operating power.
        if(partmodel.get_value(partrow, 64) <= 0.1):
            Pidx = 0
        else:
            Pidx = 1

        _hrmodel['lambdab'] = self._lambdab_count[Pidx][Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the High Frequency GaAs FET Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piA * piM * piQ * piE"

        # Retrieve junction temperature inputs.
        Tamb = partmodel.get_value(partrow, 37)
        P = partmodel.get_value(partrow, 64)
        Trise = partmodel.get_value(partrow, 107)
        thetaJC = partmodel.get_value(partrow, 109)

        # Retrieve hazard rate inputs.
        Fop = partmodel.get_value(partrow, 63)
        _hrmodel['piA'] = partmodel.get_value(partrow, 68)
        _hrmodel['piM'] = partmodel.get_value(partrow, 76)
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        # Calculate junction temperature.  If ambient temperature and
        # temperature rise are not set (i.e., equal to zero), use the
        # default case temperature values that are based on the active
        # environment.  Otherwise calculate case temperature.
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Base hazard rate.
        if(Fop >= 1.0 and Fop <= 10.0 and P < 0.1):
            _hrmodel['lambdab'] = 0.052
        elif(Fop >= 4.0 and Fop <= 10.0 and P >= 0.1 and P <= 6):
            _hrmodel['lambdab'] = 0.0093 * exp(0.429 * Fop + 0.486 * P)
        else:
            _hrmodel['lambdab'] = 0.0

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-4485.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False


class HFSiFET(Semiconductor):
    """
    High Frequency Silicon Field Effect Transistor (FET) Component Class.

    Hazard Rate Models:
    1. MIL-HDBK-217F, section 6.9
    """

    _quality = ["", "JANTXV", "JANTX", "JAN", "Lower"]
    _technology = ["", "MOSFET", "JFET"]

    def __init__(self):
        """ Initializes the High Frequency Silicon FET Component Class. """

        Semiconductor.__init__(self)

        self.subcategory = 20               # Subcategory ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [0.06, 0.023]
        self._piE = [1.0, 2.0, 5.0, 4.0, 11.0, 4.0, 5.0, 7.0, 12.0, 16.0, 0.5,
                     9.0, 24.0, 250.0]
        self._piQ = [0.5, 1.0, 2.0, 5.0]
        self._lambdab_count = [[0.099, 0.24, 0.64, 0.47, 1.4, 0.61, 0.76, 1.3, 2.3, 2.4, 0.049, 1.2, 3.6, 30.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append(u"Transistor Type:")

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for High Frequency Silicon FET
        Component Class prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_inputs_create(self, part, layout,
                                                       x_pos, y_pos)

        # Create and populate the technology combobox.  We store this
        # in the application_id field in the program database.
        part.cmbTechnology = _widg.make_combo(simple=True)
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])
        part.cmbTechnology.connect("changed",
                                   self.combo_callback,
                                   part, 104)
        layout.put(part.cmbTechnology, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display High Frequency Silicon FET Component Class
        calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = Semiconductor.assessment_results_create(self, part, layout,
                                                        x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        Semiconductor.assessment_inputs_load(self, part)

        part.cmbTechnology.set_active(int(part.model.get_value(part.selected_row, 104)))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling High Frequency Silicon FET Component
        Class ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        Semiconductor.combo_callback(self, combo, part, _index_)

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        if(_index_ == 104):                     # Technology
            part._calc_data[46] = self._lambdab[idx - 1]
            model.set_value(row, 46, part._calc_data[46])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        High Frequency Silicon FET Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piQ"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)

        _hrmodel['lambdab'] = self._lambdab_count[Eidx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the High Frequency Silicon FET Component Class.

        Keyword Arguments:
        partmodel   -- the RelKit winParts full gtk.TreeModel.
        partrow     -- the currently selected row in the winParts full
                       gtk.TreeModel.
        systemmodel -- the RelKit HARDWARE object gtk.TreeModel.
        systemrow   -- the currently selected row in the RelKit HARWARE
                       object gtk.TreeModel.
        """

        from math import exp

        _hrmodel = {}
        _hrmodel['equation'] = "lambdab * piT * piQ * piE"

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
        if(Tamb == 0 and Trise == 0):
            idx = int(systemmodel.get_value(systemrow, 22))
            Tcase = self._Tcase[idx - 1]
        else:
            Tcase = Tamb + Trise

        # Determine the junction-case thermal resistance.  If thetaJC is
        # not set (i.e., equal to zero), use the default value which is
        # based on the package type.
        if(thetaJC == 0):
            idx = int(partmodel.get_value(partrow, 67))
            thetaJC = self._thetaJC[idx - 1]
            partmodel.set_value(partrow, 109, thetaJC)

        # Junction temperature.
        Tj = Tcase + thetaJC * P

        # Temperature correction factor.  We store this in the pi_u
        # field in the Program Database.
        _hrmodel['piT'] = exp(-1925.0 * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

        # Environmental correction factor.
        idx = systemmodel.get_value(systemrow, 22)
        _hrmodel['piE'] = self._piE[idx - 1]

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
