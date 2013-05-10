#!/usr/bin/env python
""" This is the electrical connection meta-class. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       connection.py is part of The RelKit Project
#
# All rights reserved.

import pango

try:
    import relkit.configuration as _conf
    import relkit.widgets as _widg
except ImportError:
    import configuration as _conf
    import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except ImportError:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Connection:
    """
    Connections meta class.

    Hazard Rate Models:
        1. MIL-HDBK-217F, sections 15, 16, and 17.
    """

    def __init__(self):
        """ Initializes the Connections Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 8                   # Category in relkitcom database.

        # Label text for input data.
        self._in_labels.append(_("Quality:"))
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")

        # Label text for output data.
        self._out_labels.append("")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation input tab with the
        widgets needed to select inputs for Connections Component Class
        prediction calculations.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """

        # Create and place all the labels for the inputs.
        numlabels = len(self._in_labels)
        for i in range(numlabels):
            label = _widg.make_label(self._in_labels[i], 200, 25)
            layout.put(label, 5, (i * 30 + y_pos))

        part.cmbQuality = _widg.make_combo(simple=True)
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.cmbQuality.connect('changed',
                                self._callback_combo,
                                part, 85)
        layout.put(part.cmbQuality, x_pos, y_pos)
        y_pos += 30

        part.txtCommercialPiQ = _widg.make_entry()
        part.txtCommercialPiQ.connect('focus-out-event',
                                      self._callback_entry,
                                      part, 'float', 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        quality = part.model.get_value(part.selected_row, 85)
        part.cmbQuality.set_active(int(quality))
        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            commpiq = part.model.get_value(part.selected_row, 79)
            part.txtCommercialPiQ.set_text(str(fmt.format(commpiq)))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):
        """
        Populates the RelKit Workbook calculation results tab with the
        widgets to display Connections Component Class calculation results.

        Keyword Arguments:
        part   -- the RelKit COMPONENT object.
        layout -- the layout widget to contain the display widgets.
        x_pos  -- the x position of the widgets.
        y_pos  -- the y position of the first widget.
        """
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

        y_pos += 30

        part.txtLambdaB = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)
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

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        lambdab = part.model.get_value(part.selected_row, 46)
        pie = part.model.get_value(part.selected_row, 72)
        part.txtLambdaB.set_text(str(fmt.format(lambdab)))
        part.txtPiE.set_text(str('{0:0.2g}'.format(pie)))

        return False

    def _callback_combo(self, combo, part, _index_):
        """
        Callback function for handling Connections Component Class ComboBox
        changes.

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

        # Update the Parts List.
        model.set_value(row, _index_, int(idx))

        return False

    def _callback_entry(self, entry, event, part, convert, _index_):
        """
        Callback function for handling Connections Component Class
        Entry changes.

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
        if(convert == 'text'):
            model.set_value(row, _index_, entry.get_text())

        elif(convert == 'int'):
            model.set_value(row, _index_, int(entry.get_text()))

        elif(convert == 'float'):
            model.set_value(row, _index_, float(entry.get_text()))

        # Commercial PiQ entry called the function.
        if(_index_ == 79):
            CpiQ = float(entry.get_text())

            # Use this value for piQ if it is greater than zero.
            if(CpiQ > 0):
                model.set_value(row, 79, CpiQ)

        return False
