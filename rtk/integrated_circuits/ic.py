#!/usr/bin/env python
""" This is the integrated circuit meta-class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       ic.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import relkit.widgets as _widg
except ImportError:
    import widgets as _widg


class IntegratedCircuit:
    """
    Integrated Circuit meta class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 5.
    """

    _quality = ["", "S", "B", "B-1", "Commercial"]
    _technology = ["", "Bipolar", "CMOS"]
    _package = ["", "Hermetic DIP", "Flatpack", "Can", "Non-Hermetic DIP"]

    def __init__(self):
        """ Initializes the Integrated Circuit Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 1                   # Category ID in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self.pi_Q_specified = 0.0
        self._piE = [0.5, 2.0, 4.0, 4.0, 6.0, 4.0, 5.0, 5.0, 8.0, 8.0, 0.5,
                     5.0, 12.0, 220.0]
        self._piQ = [0, 0.25, 1.0, 2.0, 10.0]
        self._Tcase = [35, 45, 50, 45, 50, 60, 60, 75, 75, 60, 35, 50, 60, 45]
        self._thetaJC = [28, 20, 20, 28, 22, 70, 28, 20, 20]
        self._K5 = [0.00028, 0.00009, 0.00003, 0.00003, 0.00036]
        self._K6 = [1.08, 1.51, 1.82, 2.01, 1.08]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels.append("Quality:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append("Technology:")
        self._in_labels.append("# of Elements:")
        self._in_labels.append("Package Type:")
        self._in_labels.append("# of Pins:")
        self._in_labels.append("Years in Production:")

        # Label text for output data.
        self._out_labels.append(u"Temp Rise (\u2070C):")
        self._out_labels.append(u"Junction Temp (\u2070C):")
        self._out_labels.append("")
        self._out_labels.append(u"C<sub>1</sub>:")
        self._out_labels.append(u"\u03C0<sub>T</sub>:")
        self._out_labels.append(u"C<sub>2</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>L</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Integrated Circuit prediction
        calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC
        # or ALL then it needs to be removed before placing
        # new widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels for the inputs.
        numlabels = len(self._in_labels)
        for i in range(numlabels):
            label = _widg.make_label(self._in_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        part.cmbQuality = _widg.make_combo(simple=True)
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.cmbQuality.connect("changed",
                                self.combo_callback,
                                part, 85)
        layout.put(part.cmbQuality, x_pos, y_pos)
        y_pos += 30

        part.txtCommercialPiQ = _widg.make_entry(width=entry_width)
        part.txtCommercialPiQ.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        part.cmbTechnology = _widg.make_combo(simple=True)
        for i in range(len(self._technology)):
            part.cmbTechnology.insert_text(i, self._technology[i])
        part.cmbTechnology.connect("changed",
                                   self.combo_callback,
                                   part, 104)
        layout.put(part.cmbTechnology, x_pos, y_pos)
        y_pos += 30

        part.cmbElements = _widg.make_combo(simple=True)
        part.cmbElements.connect("changed",
                                 self.combo_callback,
                                 part, 24)
        layout.put(part.cmbElements, x_pos, y_pos)
        y_pos += 30

        part.cmbPackage = _widg.make_combo(simple=True)
        for i in range(len(self._package)):
            part.cmbPackage.insert_text(i, self._package[i])
        part.cmbPackage.connect("changed",
                                self.combo_callback,
                                part, 67)
        layout.put(part.cmbPackage, x_pos, y_pos)
        y_pos += 30

        part.txtNumPins = _widg.make_entry(width=entry_width)
        part.txtNumPins.connect("focus-out-event",
                                self.entry_callback,
                                part, "int", 60)
        layout.put(part.txtNumPins, x_pos, y_pos)
        y_pos += 30

        part.txtYears = _widg.make_entry(width=entry_width)
        part.txtYears.connect("focus-out-event",
                              self.entry_callback,
                              part, "int", 112)
        layout.put(part.txtYears, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return(y_pos)

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtNumPins.set_text(str("{0:0.0f}".format(part.model.get_value(part.selected_row, 60))))
        part.cmbPackage.set_active(int(part.model.get_value(part.selected_row, 67)))
        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        part.cmbTechnology.set_active(int(part.model.get_value(part.selected_row, 104)))
        part.txtYears.set_text(str("{0:0.0f}".format(part.model.get_value(part.selected_row, 112))))

        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(fmt.format(part.model.get_value(part.selected_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Integrated Circuit calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC
        # or ALL then it needs to be removed before placing
        # new widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels.
        numlabels = len(self._out_labels)
        for i in range(numlabels):
            if(i == 2):
                label = _widg.make_label(self._out_labels[2], width=400)
            else:
                label = _widg.make_label(self._out_labels[i])

            layout.put(label, 5, (i * 30 + y_pos))

        part.txtTRise = _widg.make_entry(width=entry_width,
                                         editable=False, bold=True)
        layout.put(part.txtTRise, x_pos, y_pos)
        y_pos += 30

        part.txtTJunc = _widg.make_entry(width=entry_width,
                                         editable=False, bold=True)
        layout.put(part.txtTJunc, x_pos, y_pos)
        y_pos += 60                         # Increment by 60 to make room to
                                            # display reliability formula.

        part.txtC1 = _widg.make_entry(width=entry_width,
                                      editable=False, bold=True)
        layout.put(part.txtC1, x_pos, y_pos)
        y_pos += 30

        part.txtPiT = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiT, x_pos, y_pos)
        y_pos += 30

        part.txtC2 = _widg.make_entry(width=entry_width,
                                      editable=False, bold=True)
        layout.put(part.txtC2, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)
        y_pos += 30

        part.txtPiL = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiL, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        self._ready = True

        return(y_pos)

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtC1.set_text(str("{0:0.3g}".format(part.model.get_value(part.selected_row, 8))))
        part.txtC2.set_text(str(fmt.format(part.model.get_value(part.selected_row, 9))))
        part.txtTJunc.set_text(str(fmt.format(part.model.get_value(part.selected_row, 39))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))
        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))
        part.txtPiL.set_text(str(fmt.format(part.model.get_value(part.selected_row, 80))))
        part.txtPiT.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtTRise.set_text(str(fmt.format(part.model.get_value(part.selected_row, 107))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Integrated Circuit Class
        ComboBox changes.

        Keyword Arguments:
        combo   -- the combobox widget calling this function.
        part    -- the RelKit COMPONENT object.
        _index_ -- the user-definded index for the calling combobx.
        """

        try:
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        idx = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        model.set_value(row, _index_, int(idx))

        # The Number of Elements combobox called the function.
        if(_index_ == 24):
            idx2 = part.cmbTechnology.get_active()
            model.set_value(row, 8, self._C1[idx2 - 1][idx - 1])

        # The Package Type combobox called the function.
        elif(_index_ == 67):
            model.set_value(row, 35, self._K5[idx - 1])
            model.set_value(row, 36, self._K6[idx - 1])

        # The Quality combobox called the function.
        elif(_index_ == 85):
            if(part.txtCommercialPiQ.get_text() == ""):
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if(CpiQ <= 0):
                model.set_value(row, 79, self._piQ[idx])

        # The Technology combobox called the function.
        elif(_index_ == 104):
            idx2 = part.cmbElements.get_active()
            model.set_value(row, 8, self._C1[idx - 1][idx2 - 1])

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Integrated Circuit Class Entry
        changes.

        Keyword Arguments:
        entry   -- the entry widget calling this function.
        event   -- the event that triggered calling this function.
        part    -- the RelKit COMPONENT object.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component property array
                   associated with the data from the entry that called
                   this function.
        """

        try:
            # Get the Parts List treeview full model and full model iter.
            model = part._app.winParts.full_model
            row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        except:
            return True

        # Update the Component object property.
        if(convert == "text"):
            model.set_value(row, _index_, entry.get_text())

        elif(convert == "int"):
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == "float"):
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                model.set_value(row, 79, CpiQ)

        return False
