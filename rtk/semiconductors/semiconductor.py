#!/usr/bin/env python
""" This is the semiconductor component meta-class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       semiconductor.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import relkit.widgets as _widg
except ImportError:
    import widgets as _widg


class Semiconductor:
    """
    Discrete Semiconductor meta class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, section 6.
    """

    _quality = ["", "JANTXV", "JANTX", "JAN", "Lower", "Plastic"]
    _package = ["", "TO-1", "TO-3", "TO-5", "TO-8", "TO-9", "TO-12",
                "TO-18", "TO-28", "TO-33", "TO-39", "TO-41", "TO-44",
                "TO-46", "TO-52", "TO-53", "TO-57", "TO-59", "TO-60",
                "TO-61", "TO-63", "TO-66", "TO-71", "TO-72", "TO-83",
                "TO-89", "TO-92", "TO-94", "TO-99", "TO-126", "TO-127",
                "TO-204", "TO-204AA", "TO-205AD", "TO-205AF", "TO-220",
                "DO-4", "DO-5", "DO-7", "DO-8", "DO-9", "DO-13", "DO-14",
                "DO-29", "DO-35", "DO-41", "DO-45", "DO-204MB",
                "DO-205AB", "PA-42A", "PA-42B", "PD-36C", "PD-50",
                "PD-77", "PD-180", "PD-319", "PD-262", "PD-975", "PD-280",
                "PD-216", "PT-2G", "PT-6B", "PH-13", "PH-16", "PH-56",
                "PY-58", "PY-373"]

    def __init__(self):
        """ Initializes the Discrete Semiconductor Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 2                   # Category in relkitcom database.

        # MIL-HDK-217F hazard rate calculation variables.
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
        self._Tcase = [35, 45, 50, 45, 50, 60, 60, 75, 75, 60, 35, 50, 60, 45]
        self._thetaJC = [70, 10, 70, 70, 70, 70, 70, 5, 70, 70, 10, 70, 70, 70,
                         5, 5, 5, 5, 5, 5, 10, 70, 70, 5, 22, 70, 5, 70, 5, 5,
                         10, 10, 70, 70, 5, 5, 5, 10, 5, 5, 10, 5, 10, 10, 10,
                         5, 70, 5, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                         70, 70, 70, 70, 70, 70]
        # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

        # Label text for input data.
        self._in_labels.append("Quality:")
        self._in_labels.append("Package:")
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")

        # Label text for output data.
        self._out_labels.append(u"Temp Rise (\u2070C):")
        self._out_labels.append(u"Junction Temp (\u2070C):")
        self._out_labels.append("")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>T</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Discrete Semiconductor
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC,
        # then it needs to be removed before placing new
        # widgets.
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

        part.cmbPackage = _widg.make_combo(simple=True)
        for i in range(len(self._package)):
            part.cmbPackage.insert_text(i, self._package[i])
        part.cmbPackage.connect("changed",
                                self.combo_callback,
                                part, 67)
        layout.put(part.cmbPackage, x_pos, y_pos)
        y_pos += 30

        part.txtCommercialPiQ = _widg.make_entry(width=entry_width)
        part.txtCommercialPiQ.connect("focus-out-event",
                                      self.entry_callback,
                                      part, "float", 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return(y_pos)

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Discrete Semicondutor calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        entry_width = int((int(part.fmt) + 5) * 8)

        # Get the list of widgets already on the layout.
        # Check each child widget's name.  If it is IC,
        # then it needs to be removed before placing new
        # widgets.
        chwidgets = layout.get_children()
        for i in range(len(chwidgets)):
            if(chwidgets[i].get_name() == "TRANSIENT"):
                layout.remove(chwidgets[i])

        # Create and place all the labels.
        numlabels = len(self._out_labels)
        for i in range(numlabels):
            if(i == 2):
                label = _widg.make_label(self._out_labels[i], width=400)
                llayout = label.get_layout()
                llayout.set_alignment(pango.ALIGN_CENTER)
                label.show_all()
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

        part.txtLambdaB = _widg.make_entry(width=entry_width,
                                           editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiT = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiT, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(width=entry_width,
                                       editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        self._ready = True

        return(y_pos)

    def assessment_inputs_load(self, part):
        """
        Loads the RelKit Workbook calculation input widgets with
        calculation input information.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.cmbPackage.set_active(int(part.model.get_value(part.selected_row, 67)))
        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(fmt.format(part.model.get_value(part.selected_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_load(self, part):
        """
        Loads the RelKit Workbook calculation results widgets with
        calculation results.

        Keyword Arguments:
        part -- the RelKit COMPONENT object.
        """

        fmt = "{0:0." + str(part.fmt) + "g}"

        part.txtPiQ.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 79))))
        part.txtPiT.set_text(str(fmt.format(part.model.get_value(part.selected_row, 82))))
        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtTJunc.set_text(str(fmt.format(part.model.get_value(part.selected_row, 39))))
        part.txtTRise.set_text(str(fmt.format(part.model.get_value(part.selected_row, 107))))
        part.txtPiE.set_text(str("{0:0.2g}".format(part.model.get_value(part.selected_row, 72))))

        return False

    def combo_callback(self, combo, part, _index_):
        """
        Callback function for handling Discrete Semicondutor Class
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
        part._calc_data[_index_] = int(idx)
        model.set_value(row, _index_, int(idx))

        if(_index_ == 85):                  # Quality
            if(part.txtCommercialPiQ.get_text() == ""):
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if(CpiQ <= 0.0):
                part._calc_data[79] = self._piQ[idx - 1]
                model.set_value(row, 79, part._calc_data[79])

        return False

    def entry_callback(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Discrete Semiconductor Device
        Class Entry changes.

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
            part._calc_data[_index_] = entry.get_text()
            model.set_value(row, _index_, entry.get_text())

        elif(convert == "int"):
            part._calc_data[_index_] = int(entry.get_text())
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == "float"):
            part._calc_data[_index_] = float(entry.get_text())
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                part._calc_data[79] = CpiQ
                model.set_value(row, 79, CpiQ)

        if(self._ready):
            part.calculate()

        return False
