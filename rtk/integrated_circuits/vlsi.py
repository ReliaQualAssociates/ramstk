#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       vlsi.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import pango

from math import exp, log, sqrt

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


class VLSI(IntegratedCircuit):
    """
    VHSIC/VHSIC-like and VLSI CMOS integrated circuit class.

    Hazard Rate Models:
        # MIL-HDBK-217F, section 5.3
    """

    _man = ["", _(u"QML or QPL"), _(u"Non QML or Non QPL")]

    _app = ["", _(u"Logic or Custom"), _(u"Gate Array")]

    _package = ["", _(u"Hermetic DIP"), _(u"Hermetic PGA"),
                _(u"Hermetic Chip Carrier"), _(u"Nonhermetic DIP"),
                _(u"Nonhermetic PGA"), _(u"Nonhermetic Chip Carrier")]

    def __init__(self):
        """ Initializes the VLSI integrated circuit class. """

        IntegratedCircuit.__init__(self)

        self.subcategory = 11               # Subcategory ID in the rtkcom DB.

        self._in_labels[2] = _(u"# of Transistors:")
        self._in_labels.append(_(u"Manufacturing Process:"))
        self._in_labels.append(_(u"Application:"))
        self._in_labels.append(_(u"Feature Size:"))
        self._in_labels.append(_(u"Die Area:"))
        self._in_labels.append(_(u"ESD Susceptibility:"))

        self._out_labels[2] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>BD</sub>\u03C0<sub>T</sub>\u03C0<sub>MFG</sub>\u03C0<sub>CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub>\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span>"
        self._out_labels[3] = u"\u03BB<sub>BD</sub>:"
        self._out_labels[5] = u"\u03C0<sub>MFG</sub>:"
        self._out_labels[8] = u"\u03C0<sub>PT</sub>:"
        self._out_labels.append(u"\u03C0<sub>CD</sub>:")
        self._out_labels.append(u"\u03BB<sub>BP</sub>:")
        self._out_labels.append(u"\u03BB<sub>EOS</sub>:")

        self._Ea = [[0.35], [0.35]]
        self._lambdaBD = [0.16, 0.24]
        self._piMFG = [0.55, 2.0]
        self._piPT = [1.0, 2.2, 4.7, 1.3, 2.9, 6.1]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for VLSI Integrated Circuit
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

        # Create the VLSI specific input display widgets.
        part.cmbManufacturing = _widg.make_combo(simple=True)
        part.cmbApplication = _widg.make_combo(simple=True)
        part.txtArea = _widg.make_entry(width=100)
        part.txtESD = _widg.make_entry(width=100)
        part.txtFeature = _widg.make_entry(width=100)

        # Load and update all the gtk.ComboBox().
        part.cmbElements.append_text("")
        part.cmbElements.append_text("> 60000")

        for i in range(len(self._package)):
            part.cmbPackage.insert_text(i, self._package[i])
        for i in range(len(self._man)):
            part.cmbManufacturing.insert_text(i, self._man[i])
        for i in range(len(self._app)):
            part.cmbApplication.insert_text(i, self._app[i])

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.move(part.cmbQuality, _x_pos, _y_pos[0])
        layout.move(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.move(part.cmbTechnology, _x_pos, _y_pos[2])
        layout.move(part.cmbElements, _x_pos, _y_pos[3])
        layout.move(part.cmbPackage, _x_pos, _y_pos[4])
        layout.move(part.txtNumPins, _x_pos, _y_pos[5])
        layout.move(part.txtYears, _x_pos, _y_pos[6])
        layout.put(part.cmbManufacturing, _x_pos, _y_pos[7])
        layout.put(part.cmbApplication, _x_pos, _y_pos[8])
        layout.put(part.txtArea, _x_pos, _y_pos[9])
        layout.put(part.txtESD, _x_pos, _y_pos[10])
        layout.put(part.txtFeature, _x_pos, _y_pos[11])

        part.cmbManufacturing.connect("changed", self._callback_combo,
                                      part, 54)
        part.cmbApplication.connect("changed", self._callback_combo,
                                    part, 5)
        part.txtArea.connect("focus-out-event", self._callback_entry,
                             part, "float", 21)
        part.txtESD.connect("focus-out-event", self._callback_entry,
                            part, "float", 25)
        part.txtFeature.connect("focus-out-event", self._callback_entry,
                                part, "float", 29)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the widgets to
        display VLSI Integrated Circuit calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_x_pos,
         _y_pos) = IntegratedCircuit.reliability_results_create(self, part,
                                                                layout,
                                                                x_pos, y_pos)

        # Create the VLSI specific reliability result display widgets.
        part.txtPiCD = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiMFG = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiPT = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtLambdaBD = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        part.txtLambdaBP = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        part.txtLambdaEOS = _widg.make_entry(width=100, editable=False,
                                             bold=True)

        # Place the reliability result display widgets.
        layout.remove(part.txtC1)
        layout.put(part.txtLambdaBD, _x_pos, _y_pos[1])
        layout.move(part.txtPiT, _x_pos, _y_pos[2])
        layout.remove(part.txtC2)
        layout.put(part.txtPiMFG, _x_pos, _y_pos[3])
        layout.move(part.txtPiE, _x_pos, _y_pos[4])
        layout.move(part.txtPiQ, _x_pos, _y_pos[5])
        layout.remove(part.txtPiL)
        layout.put(part.txtPiPT, _x_pos, _y_pos[6])
        layout.put(part.txtPiCD, _x_pos, _y_pos[7])
        layout.put(part.txtLambdaBP, _x_pos, _y_pos[8])
        layout.put(part.txtLambdaEOS, _x_pos, _y_pos[9])

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

        fmt = "{0:0." + str(_conf.PLACES) + "g}"

        (_model, _row) = IntegratedCircuit.assessment_inputs_load(self, part)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.txtArea.set_text(str(fmt.format(_model.get_value(_row, 21))))
        part.cmbElements.set_active(int(_model.get_value(_row, 24)))
        part.txtESD.set_text(str(fmt.format(_model.get_value(_row, 25))))
        part.txtFeature.set_text(str(fmt.format(_model.get_value(_row, 29))))
        part.cmbManufacturing.set_active(int(_model.get_value(_row, 54)))

        return False

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the rtk.Component().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = "{0:0." + str(_conf.PLACES) + "g}"

        (_model, _row) = IntegratedCircuit.assessment_results_load(self, part)

        part.txtPiCD.set_text(str(fmt.format(_model.get_value(_row, 70))))
        part.txtPiMFG.set_text(str("{0:0.3g}".format(
            _model.get_value(_row, 77))))
        part.txtPiPT.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 78))))
        part.txtLambdaBD.set_text(str(fmt.format(_model.get_value(_row, 8))))
        part.txtLambdaBP.set_text(str(fmt.format(_model.get_value(_row, 52))))
        part.txtLambdaEOS.set_text(str(fmt.format(_model.get_value(_row, 51))))

        part.fxdReliabilityResults.show_all()

        return False

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Integrated Circuit Class
        ComboBox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() calling this method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param int idx: the user-defined index for the calling combobx.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _index = combo.get_active()

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        if idx == 24 or idx == 104:
            _model.set_value(_row, idx, int(_index))
        else:
            IntegratedCircuit._callback_combo(self, combo, part, idx)

        if idx == 5:                        # Application
            _model.set_value(_row, 50, self._lambdaBD[_index - 1])

        elif idx == 54:                     # Manufacturing process
            _model.set_value(_row, 77, self._piMFG[_index - 1])

        elif idx == 67:                     # Package type
            _model.set_value(_row, 78, self._piPT[_index - 1])

        return False

    def entry_callback(self, entry, event, part, convert, idx):
        """
        Callback function for handling Integrated Circuit Class Entry
        changes.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param str convert: the data type to convert the gtk.Entry() contents.
        :param int idx: the position in the Component property array
                        associated with the data from the gtk.Entry() that
                        called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        IntegratedCircuit.entry_callback(self, entry, event,
                                         part, convert, _index_)

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        if idx == 21:                       # Die area
            _model.set_value(_row, 21, float(entry.get_text()))

        elif idx == 25:                     # ESD susceptibility
            _model.set_value(_row, 25, float(entry.get_text()))

        elif idx == 29:                     # Feature size
            _model.set_value(_row, 29, float(entry.get_text()))

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

            print "MIL-HDBK-217 parts count methodology not yet implemented."
            # TODO: Implement MIL-HDBK-217F parts count methodology for VLSI IC.

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
            _hrmodel['equation'] = "lambdaBD * piMFG * piT * piCD + lambdaBP * piE * piQ *piPT + lambdaEOS"

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
            A = partmodel.get_value(partrow, 21)
            Ea = partmodel.get_value(partrow, 22)
            Vth = partmodel.get_value(partrow, 25)
            Xs = partmodel.get_value(partrow, 29)
            _hrmodel['lambdaBD'] = partmodel.get_value(partrow, 50)
            B = partmodel.get_value(partrow, 58)
            Np = partmodel.get_value(partrow, 60)
            _hrmodel['piMFG'] = partmodel.get_value(partrow, 77)
            _hrmodel['piPT'] = partmodel.get_value(partrow, 78)
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

            # Junction temperature
            Tj = Tcase + thetaJC * P

            # Calculate the temperature factor.  We store this in the pi_u
            # field in the Program Database.
            _hrmodel['piT'] = 0.1 * exp((-1.0 * Ea / 0.00008617) * ((1.0 / (Tj + 273.0)) - (1.0 / 298.0)))

            # Environmental factor
            idx = systemmodel.get_value(systemrow, 22)
            _hrmodel['piE'] = self._piE[idx - 1]

            # Die complexity correction factor.  We store this in the pi_cf
            # field in the Program Database.
            _hrmodel['piCD'] = ((A / 0.21) * ((2.0 / Xs) ** 2.0) * 0.64) + 0.36

            # Package base failure rate.  We store this in the lambda_g
            # field in the program database.
            _hrmodel['lambdaBP'] = 0.0022 + (0.0000172 * Np)

            # Electrical overstress failure rate.
            _hrmodel['lambdaEOS'] = (-1.0 * log(1.0 - 0.00057 * exp(-1.0 * 0.0002 * Vth))) / 0.00876

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

            partmodel.set_value(partrow, 17, _i_ratio)
            partmodel.set_value(partrow, 39, Tj)
            partmodel.set_value(partrow, 50, _hrmodel['lambdaBD'])
            partmodel.set_value(partrow, 51, _hrmodel['lambdaEOS'])
            partmodel.set_value(partrow, 52, _hrmodel['lambdaBP'])
            partmodel.set_value(partrow, 70, _hrmodel['piCD'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
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
