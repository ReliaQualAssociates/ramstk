#!/usr/bin/env python

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       meter.py is part of The RTK Project
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

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ElapsedTime(object):
    """
    Elapsed Time Meter Component Class.

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 12.3.
    """

    _type = [u"", u"A.C.", _(u"Inverter Driven"), _(u"Cummutator D.C.")]

    def __init__(self):
        """
        Initializes the Elapsed Time Meter Component Class.
        """

        self._ready = False

        self.category = 9                   # Category in the rtkcom database.
        self.subcategory = 77               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._lambdab = [20.0, 30.0, 80.0]
        self._piE = [1.0, 2.0, 12.0, 7.0, 18.0, 5.0, 8.0, 16.0, 25.0, 26.0,
                     0.5, 14.0, 38.0, 0.0]
        self._lambdab_count = [[10.0, 20.0, 120.0, 70.0, 180.0, 50.0, 80.0,
                                160.0, 250.0, 260.0, 5.0, 140.0, 380.0, 0.0],
                               [15.0, 30.0, 180.0, 105.0, 270.0, 75.0, 120.0,
                                240.0, 375.0, 390.0, 7.5, 210.0, 570.0, 0.0],
                               [40.0, 80.0, 480.0, 280.0, 720.0, 200.0, 320.0,
                                640.0, 1000.0, 1040.0, 20.0, 560.0, 1520.0,
                                0.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels = [_(u"Type:"), _(u"Operating Temperature (\u00B0C):"),
                           _(u"Rated Temperature (\u00B0C):")]

        # Label text for output data.
        self._out_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>T</sub>:",
                            u"\u03C0<sub>E</sub>:"]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the widgets
        needed to select inputs for Elapsed Time Meter Component Class
        prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed() except the
        # calculation model gtk.Label() and gtk.ComboBox().
        for _child in layout.get_children()[2:]:
            layout.remove(_child)

        # Create the input widgets.
        # Create the Meter Type ComboBox.  We store the index in the
        # technology_id field in the program database.
        part.cmbType = _widg.make_combo(simple=True)
        part.txtOperatingTemp = _widg.make_entry(width=100)
        part.txtRatedTemp = _widg.make_entry(width=100)

        # Load all the gtk.ComboBox().
        for i in range(len(self._type)):
            part.cmbType.insert_text(i, self._type[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos += 35

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.put(part.cmbType, _x_pos, _y_pos[0])
        layout.put(part.txtOperatingTemp, _x_pos, _y_pos[1])
        layout.put(part.txtRatedTemp, _x_pos, _y_pos[2])

        # Connect to callback methods.
        part.cmbType.connect("changed", self._callback_combo, part, 104)
        part.txtOperatingTemp.connect("focus-out-event", self._callback_entry,
                                      part, "float", 105)
        part.txtRatedTemp.connect("focus-out-event", self._callback_entry,
                                  part, "float", 55)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Elapsed Time Meter Component Class calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[20:]:
            layout.remove(_child)

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        # Create the piT Entry.  We store this value in the pi_sr field in the
        # program database.
        part.txtPiT = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels,
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiT, _x_pos, _y_pos[2])
        layout.put(part.txtPiE, _x_pos, _y_pos[3])

        layout.show_all()

        return _x_pos, _y_pos

    def stress_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook stress calculation results tab with the
        widgets to display Capacitor Component Class stress results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the widgets.
        :param int y_pos: the y position of the first widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[16:]:
            layout.remove(_child)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation input
        information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.txtRatedTemp.set_text(str(fmt.format(_model.get_value(_row, 55))))
        part.cmbType.set_active(int(_model.get_value(_row, 104)))
        part.txtOperatingTemp.set_text(str(fmt.format(
            _model.get_value(_row, 105))))

        return _model, _row

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))
        part.txtPiT.set_text(str(fmt.format(_model.get_value(_row, 81))))

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Elapsed Time Meter Component Class
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

        # Update the Component object property and the Parts List treeview.
        _model.set_value(_row, idx, int(_index))

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Elapsed Time Meter Component Class
        Entry changes.

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

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        # Update the Component object property.
        if convert == "text":
            _model.set_value(_row, idx, entry.get_text())

        elif convert == "int":
            _model.set_value(_row, idx, int(entry.get_text()))

        elif convert == "float":
            _model.set_value(_row, idx, float(entry.get_text()))

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Elapsed Time Meter class.

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
            _hrmodel['equation'] = "lambdab"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Tidx = partmodel.get_value(partrow, 104)        # Type index

            _hrmodel['lambdab'] = self._lambdab_count[Tidx - 1][Eidx - 1]

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
            _hrmodel['equation'] = "lambdab * piT * piE"

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
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index
            Trate = partmodel.get_value(partrow, 55)
            Tidx = partmodel.get_value(partrow, 104)        # Type index
            Toper = partmodel.get_value(partrow, 105)

            # Base hazard rate.
            _hrmodel['lambdab'] = self._lambdab[Tidx - 1]

            # Temperature stress correction factor.
            try:
                S = Toper / Trate
            except:
                S = 1.0

            if S <= 0.5:
                _hrmodel['piT'] = 0.5
            elif S > 0.5 and S <= 0.6:
                _hrmodel['piT'] = 0.6
            elif S > 0.6 and S <= 0.8:
                _hrmodel['piT'] = 0.8
            else:
                _hrmodel['piT'] = 1.0

            # Environmental correction factor.
            _hrmodel['piE'] = self._piE[Eidx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdas

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 81, _hrmodel['piT'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 29, 0.0)
            systemmodel.set_value(systemrow, 32, _lambdap)
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


class Panel(object):
    """
    Panel Meter Component Class.
    Covers specifications MIL-M-10304.

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 18.1.
    """

    _application = [u"", _(u"Direct Current"), _(u"Alternating Current")]
    _quality = [u"", u"MIL-M-10304", _(u"Lower")]
    _type = [u"", _(u"Ammeter"), _(u"Voltmeter"), _(u"Other")]

    def __init__(self):
        """
        Initializes the Panel Meter Component Class.
        """

        self._ready = False
        self.category = 9                   # Category in the rtkcom database.
        self.subcategory = 78               # Subcategory ID in the rtkcom DB.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._piA = [1.0, 1.7]
        self._piE = [1.0, 4.0, 25.0, 12.0, 35.0, 28.0, 42.0, 58.0, 73.0, 60.0,
                     1.1, 60.0, 0.0, 0.0]
        self._piF = [1.0, 1.0, 2.8]
        self._piQ = [1.0, 3.4]
        self._lambdab_count = [[0.09, 0.36, 2.3, 1.1, 3.2, 2.5, 3.8, 5.2, 6.6,
                                5.4, 0.099, 5.4, 0.0, 0.0],
                               [0.15, 0.81, 2.8, 1.8, 5.4, 4.3, 6.4, 8.9, 11.0,
                                9.2, 0.17, 9.2, 0.0, 0.0]]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                           _(u"Application:"), _(u"Function:")]

        # Label text for output data.
        self._out_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>A</sub>:",
                            u"\u03C0<sub>F</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation input tab with the
        widgets needed to select inputs for Panel Meter Component
        Class prediction calculations.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the input widgets.
        :param int x_pos: the x position of the input widgets.
        :param int y_pos: the y position of the first input widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed() except the
        # calculation model gtk.Label() and gtk.ComboBox().
        for _child in layout.get_children()[2:]:
            layout.remove(_child)

        # Create the input widgets.
        part.cmbQuality = _widg.make_combo(simple=True)
        part.txtCommercialPiQ = _widg.make_entry(width=100)
        part.cmbApplication = _widg.make_combo(simple=True)
        # Create the Meter Type ComboBox.  We store the index in the
        # technology_id filed in the program database.
        part.cmbType = _widg.make_combo(simple=True)

        # Load all the gtk.ComboBox().
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        for i in range(len(self._application)):
            part.cmbApplication.insert_text(i, self._application[i])
        for i in range(len(self._type)):
            part.cmbType.insert_text(i, self._type[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._in_labels, layout, 5, y_pos)
        _x_pos = max(_x_pos, x_pos)

        # Place the input widgets.
        layout.move(part.cmbCalcModel, _x_pos, 5)
        layout.put(part.cmbQuality, _x_pos, _y_pos[0])
        layout.put(part.txtCommercialPiQ, _x_pos, _y_pos[1])
        layout.put(part.cmbApplication, _x_pos, _y_pos[2])
        layout.put(part.cmbType, _x_pos, _y_pos[3])

        # Connect to callback methods.
        part.cmbQuality.connect("changed", self._callback_combo, part, 85)
        part.cmbApplication.connect("changed", self._callback_combo, part, 5)
        part.cmbType.connect("changed", self._callback_combo, part, 104)
        part.txtCommercialPiQ.connect("focus-out-event", self._callback_entry,
                                      part, "float", 79)

        layout.show_all()

        return False

    def reliability_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook calculation results tab with the
        widgets to display Panel Meter Component Class calculation
        results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[20:]:
            layout.remove(_child)

        # Create the reliability result display widgets.
        part.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        part.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiF = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        part.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Create and place all the labels.
        (_x_pos, _y_pos) = _widg.make_labels(self._out_labels,
                                             layout, x_pos, y_pos)
        _x_pos += x_pos
        _x_pos -= 30

        # Place the reliability result display widgets.
        layout.put(part.txtLambdaB, _x_pos, _y_pos[1])
        layout.put(part.txtPiA, _x_pos, _y_pos[2])
        layout.put(part.txtPiF, _x_pos, _y_pos[3])
        layout.put(part.txtPiQ, _x_pos, _y_pos[4])
        layout.put(part.txtPiE, _x_pos, _y_pos[5])

        layout.show_all()

        return False

    def stress_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RTK Workbook stress calculation results tab with the
        widgets to display Capacitor Component Class stress results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :param gtk.Fixed layout: the gtk.Fixed() to contain the display
                                 widgets.
        :param int x_pos: the x position of the widgets.
        :param int y_pos: the y position of the first widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
        """

        # Clear all the display widgets from the gtk.Fixed().
        for _child in layout.get_children()[16:]:
            layout.remove(_child)

        return False

    def assessment_inputs_load(self, part):
        """
        Loads the RTK Workbook calculation input widgets with calculation input
        information.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.cmbApplication.set_active(int(_model.get_value(_row, 5)))
        part.cmbQuality.set_active(int(_model.get_value(_row, 85)))
        part.cmbType.set_active(int(_model.get_value(_row, 104)))
        if int(_model.get_value(_row, 85)) <= 0:
            part.txtCommercialPiQ.set_text(str(fmt.format(
                _model.get_value(_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return _model, _row

    def assessment_results_load(self, part):
        """
        Loads the RTK Workbook calculation results widgets with
        calculation results.

        :param rtk.Component part: the current instance of the RTK Component
                                   class.
        :return: (_model, _row); the Parts List gtk.Treemodel and selected
                 gtk.TreeIter()
        :rtype: tuple
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        part.txtLambdaB.set_text(str(fmt.format(_model.get_value(_row, 46))))
        part.txtPiA.set_text(str(fmt.format(_model.get_value(_row, 68))))
        part.txtPiE.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 72))))
        part.txtPiF.set_text(str(fmt.format(_model.get_value(_row, 74))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(
            _model.get_value(_row, 79))))

        return _model, _row

    def _callback_combo(self, combo, part, idx):
        """
        Callback function for handling Panel Meter Component Class ComboBox
        changes.

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

        # Update the Component object property and the Parts List treeview.
        _model.set_value(_row, idx, int(_index))

        return False

    def _callback_entry(self, entry, event, part, convert, idx):
        """
        Callback function for handling Panel Meter Component Class
        Entry changes.

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

        _path = part._app.winParts._treepaths[part.assembly_id]
        _model = part._app.winParts.tvwPartsList.get_model()
        _row = _model.get_iter(_path)

        # Update the Component object property.
        if convert == "text":
            _model.set_value(_row, idx, entry.get_text())
        elif convert == "int":
            _model.set_value(_row, idx, int(entry.get_text()))
        elif convert == "float":
            _model.set_value(_row, idx, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if _index_ == 79:
            CpiQ = float(entry.get_text())

        return False

    def calculate(self, partmodel, partrow, systemmodel, systemrow):
        """
        Performs hazard rate calculations for the Elapsed Time Meter class.

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
            _hrmodel['equation'] = "lambdab * piQ"

            _quantity = systemmodel.get_value(systemrow, 67)

            # Retrieve hazard rate inputs.
            Aidx = partmodel.get_value(partrow, 5)          # Application index
            _hrmodel['piQ'] = partmodel.get_value(partrow, 79)
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            _hrmodel['lambdab'] = self._lambdab_count[Aidx - 1][Eidx - 1]

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
            _hrmodel['equation'] = "lambdab * piA * piF * piQ * piE"

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
            Aidx = partmodel.get_value(partrow, 5)          # Application index
            Qidx = partmodel.get_value(partrow, 85)         # Quality index
            Tidx = partmodel.get_value(partrow, 104)        # Type index
            Eidx = systemmodel.get_value(systemrow, 22)     # Environment index

            # Base hazard rate.
            _hrmodel['lambdab'] = 0.090

            # Application correction factor.
            _hrmodel['piA'] = self._piA[Aidx - 1]

            # Function correction factor.
            _hrmodel['piF'] = self._piF[Tidx - 1]

            # Quality correction factor.
            _hrmodel['piQ'] = self._piQ[Qidx - 1]

            # Environmental correction factor.
            _hrmodel['piE'] = self._piE[Eidx - 1]

            # Calculate component active hazard rate.
            _lambdaa = _calc.calculate_part(_hrmodel)
            _lambdaa = _lambdaa * _quantity

            # Calculate the component predicted hazard rate.
            _lambdap = _lambdaa + _lambdas

            partmodel.set_value(partrow, 46, _hrmodel['lambdab'])
            partmodel.set_value(partrow, 68, _hrmodel['piA'])
            partmodel.set_value(partrow, 72, _hrmodel['piE'])
            partmodel.set_value(partrow, 74, _hrmodel['piF'])
            partmodel.set_value(partrow, 79, _hrmodel['piQ'])

            systemmodel.set_value(systemrow, 28, _lambdaa)
            systemmodel.set_value(systemrow, 29, 0.0)
            systemmodel.set_value(systemrow, 32, _lambdap)
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
