#!/usr/bin/env python
""" This is the Gallium-Arsenide integrated circuit class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       gaas.py is part of The RelKit Project
#
# All rights reserved.

try:
    import reliafree.calculations as _calc
    import reliafree.widgets as _widg
except ImportError:
    import calculations as _calc
    import widgets as _widg

from ic import IntegratedCircuit


class GaAsDigital(IntegratedCircuit):
    """
    Digital GaAs Integrated Circuit Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.4
    """

    def __init__(self):
        """
        Initializes the Digital GaAs Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 9                    # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[25.0, 51.0],[25.0, 51.0]]

        self._lambdab_count = [[0.0085, 0.030, 0.057, 0.057, 0.084, 0.060, 0.073, 0.080, 0.12, 0.11, 0.0085, 0.071, 0.17, 3.0],
                               [0.0140, 0.053, 0.100, 0.100, 0.150, 0.110, 0.130, 0.140, 0.22, 0.21, 0.0140, 0.130, 0.31, 5.5]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Digital GaAs Integrated
        Circuit prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        part.cmbElements.append_text("")
        part.cmbElements.append_text("1 to 1000")
        part.cmbElements.append_text("1001 to 10000")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Digital GaAs Integrated Circuit calculation
        results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Digital GaAs Integrated Circuit Class.

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
        _hrmodel['equation'] = "lambdab * piQ * piL"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Bidx = partmodel.get_value(partrow, 24)         # No of elements index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Y = partmodel.get_value(partrow, 112)

        _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

        # Calculate the learning factor.  We store this in the pi_r
        # field in the Program Database.
        _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Digital GaAs Integrated Circuit Class.

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
        _hrmodel['equation'] = "(C1 * piT * piA + C2 * piE) * piQ * piL"

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
        idx = int(partmodel.get_value(partrow, 67))
        if(thetaJC == 0):
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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 35, K5)
        partmodel.set_value(partrow, 36, K6)
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

class GaAsMMIC(IntegratedCircuit):
    """
    Microwave Monolithic GaAs Integrated Circuit Component Class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.4
    """

    _application = ["", "Low Noise & Low Power (<100mW)",
                    "Driver & High Power (>100mW)", "Unknown"]

    def __init__(self):
        """
        Initializes the Microwave Monolithic GaAs Integrated Circuit Component Class.
        """

        IntegratedCircuit.__init__(self)

        self.subcategory = 10               # Subcategory ID in reliafreecom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._C1 = [[4.5, 7.2], [4.5, 7.2]]
        self._piA = [1.0, 3.0, 3.0]

        self._lambdab_count = [[0.0085, 0.030, 0.057, 0.057, 0.084, 0.060, 0.073, 0.080, 0.12, 0.11, 0.0085, 0.071, 0.17, 3.0],
                               [0.0140, 0.053, 0.100, 0.100, 0.150, 0.110, 0.130, 0.140, 0.22, 0.21, 0.0140, 0.130, 0.31, 5.5]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        self._in_labels.append("Application:")
        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
        self._out_labels.append(u"\u03C0<sub>A</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Microwave Monolithic GaAs
        Integrated Circuit prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_inputs_create(self, part, layout,
                                                           x_pos, y_pos)

        part.cmbElements.append_text("")
        part.cmbElements.append_text("1 to 100")
        part.cmbElements.append_text("101 to 1000")

        part.cmbApplication = _widg.make_combo(simple=True)
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        part.cmbApplication.connect("changed",
                                    self.combo_callback,
                                    part, 5)
        layout.put(part.cmbApplication, x_pos, y_pos)

        layout.show_all()

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Microwave Monolithic GaAs Integrated Circuit
        calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        y_pos = IntegratedCircuit.assessment_results_create(self, part, layout,
                                                            x_pos, y_pos)

        entry_width = int((int(part.fmt) + 5) * 8)

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

        IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(part.model.get_value(part.selected_row, 5)))
        part.cmbElements.set_active(int(part.model.get_value(part.selected_row, 24)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        IntegratedCircuit.assessment_results_load(self, part)

        part.txtPiA.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 68))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling ComboBox changes specific to the
        Microwave Monolithic GaAs Integrated Circuit Component Class.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        try:
            # Get the Parts List treeview full model and full model iter.
            treemodel = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        IntegratedCircuit.combo_callback(self, combo, part, _index_)

        idx = combo.get_active()

        if(_index_ == 5):
            treemodel.set_value(row, 68, self._piA[idx - 1])

        return False

    def calculate_mil_217_count(self, partmodel, partrow,
                                systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part count hazard rate calculations for the
        Microwave Monolithic GaAs Integrated Circuit Class.

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
        _hrmodel['equation'] = "lambdab * piQ * piL"

        # Retrieve hazard rate inputs.
        Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
        Bidx = partmodel.get_value(partrow, 24)         # No of elements index
        _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
        Y = partmodel.get_value(partrow, 112)

        _hrmodel['lambdab'] = self._lambdab_count[Bidx - 1][Eidx - 1]

        # Calculate the learning factor.  We store this in the pi_r
        # field in the Program Database.
        _hrmodel['piL'] = 0.01 * exp(5.35 - 0.35 * Y)

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False

    def calculate_mil_217_stress(self, partmodel, partrow,
                                 systemmodel, systemrow):
        """
        Performs MIL-HDBK-217F part stress hazard rate calculations for
        the Microwave Monolithic GaAs Integrated Circuit Class.

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
        _hrmodel['equation'] = "(C1 * piT * piA + C2 * piE) * piQ * piL"

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
        idx = int(partmodel.get_value(partrow, 67))
        if(thetaJC == 0):
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

        # Calculate component hazard rate.
        lambdap = _calc.calculate_part(_hrmodel)

        partmodel.set_value(partrow, 9, _hrmodel['C2'])
        partmodel.set_value(partrow, 35, K5)
        partmodel.set_value(partrow, 36, K6)
        partmodel.set_value(partrow, 39, Tj)
        partmodel.set_value(partrow, 68, _hrmodel['piA'])
        partmodel.set_value(partrow, 72, _hrmodel['piE'])
        partmodel.set_value(partrow, 80, _hrmodel['piL'])
        partmodel.set_value(partrow, 82, _hrmodel['piT'])

        systemmodel.set_value(systemrow, 28, lambdap)
        systemmodel.set_value(systemrow, 88, list(_hrmodel.items()))

        return False
