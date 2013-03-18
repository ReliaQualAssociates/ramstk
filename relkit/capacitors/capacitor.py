#!/usr/bin/env python
""" Capacitor is the meta class for all capacitor types. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       capacitor.py is part of The RelKit Project
#
# All rights reserved.

import pango

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext

try:
    import reliafree.configuration as _conf
    import reliafree.widgets as _widg
except:
    import configuration as _conf
    import widgets as _widg


class Capacitor:

    """ Capacitor meta class.

        Hazard Rate Models:
            1. MIL-HDBK-217F, section 10.
    """

    def __init__(self):

        """ Initializes the Capacitor Component Class. """

        self._ready = False

        self._in_labels = []
        self._out_labels = []

        self.category = 4                       # Category in reliafreecom database.

        # Label text for input data.
        self._in_labels.append(_("Quality:"))
        self._in_labels.append(u"\u03C0<sub>Q</sub> Override:")
        self._in_labels.append(_("Specification:"))
        self._in_labels.append(_("Spec Sheet:"))
        self._in_labels.append(_("Rated Voltage:"))
        self._in_labels.append(_("Applied DC Voltage:"))
        self._in_labels.append(_("Applied AC Voltage:"))
        self._in_labels.append(_("Capacitance (F):"))

        # Label text for output data.
        self._out_labels.append(_(u"Temp Rise (\u2070C):"))
        self._out_labels.append(_(u"Junction Temp (\u2070C):"))
        self._out_labels.append("")
        self._out_labels.append(u"\u03BB<sub>b</sub>:")
        self._out_labels.append(u"\u03C0<sub>Q</sub>:")
        self._out_labels.append(u"\u03C0<sub>E</sub>:")
        self._out_labels.append(u"\u03C0<sub>CV</sub>:")

    def assessment_inputs_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation input tab with the
            widgets needed to select inputs for Capacitor Component Class
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

        # Create and populate the quality combobox.
        part.cmbQuality = _widg.make_combo(simple=True)
        for i in range(len(self._quality)):
            part.cmbQuality.insert_text(i, self._quality[i])
        part.cmbQuality.connect('changed',
                                self._callback_combo,
                                part, 85)
        layout.put(part.cmbQuality, x_pos, y_pos)
        y_pos += 30

        # Create the commercial PiQ entry.
        part.txtCommercialPiQ = _widg.make_entry()
        part.txtCommercialPiQ.connect('focus-out-event',
                                      self._callback_entry,
                                      part, 'float', 79)
        layout.put(part.txtCommercialPiQ, x_pos, y_pos)
        y_pos += 30

        # Create and populate the specification combobox.
        part.cmbSpecification = _widg.make_combo(simple=True)
        for i in range(len(self._specification)):
            part.cmbSpecification.insert_text(i, self._specification[i])
        part.cmbSpecification.connect('changed',
                                      self._callback_combo,
                                      part, 101)
        layout.put(part.cmbSpecification, x_pos, y_pos)
        y_pos += 30

        # Create the specification slash sheetcombobox.
        part.cmbSpecSheet = _widg.make_combo(simple=True)
        part.cmbSpecSheet.connect('changed',
                                  self._callback_combo,
                                  part, 102)
        layout.put(part.cmbSpecSheet, x_pos, y_pos)
        y_pos += 30

        # Create the rated voltage entry.
        part.txtVoltRated = _widg.make_entry()
        part.txtVoltRated.connect('focus-out-event',
                                  self._callback_entry,
                                  part, 'float', 94)
        layout.put(part.txtVoltRated, x_pos, y_pos)
        y_pos += 30

        # Create the applied DC voltage entry.
        part.txtVoltApplied = _widg.make_entry()
        part.txtVoltApplied.connect('focus-out-event',
                                    self._callback_entry,
                                    part, 'float', 66)
        layout.put(part.txtVoltApplied, x_pos, y_pos)
        y_pos += 30

        # Create the applied voltage entry.  We store this in the
        # Operating power field in the program database.
        part.txtACVoltApplied = _widg.make_entry()
        part.txtACVoltApplied.connect('focus-out-event',
                                      self._callback_entry,
                                      part, 'float', 64)
        layout.put(part.txtACVoltApplied, x_pos, y_pos)
        y_pos += 30

        # Create the capacitance entry.
        part.txtCapacitance = _widg.make_entry()
        part.txtCapacitance.connect('focus-out-event',
                                    self._callback_entry,
                                    part, 'float', 15)
        layout.put(part.txtCapacitance, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        return(y_pos)

    def assessment_inputs_load(self, part):

        """ Loads the RelKit Workbook calculation input widgets with
            calculation input information.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        part.cmbQuality.set_active(int(part.model.get_value(part.selected_row, 85)))
        part.cmbSpecification.set_active(int(part.model.get_value(part.selected_row, 101)))
        part.cmbSpecSheet.set_active(int(part.model.get_value(part.selected_row, 102)))
        part.txtVoltRated.set_text(str(fmt.format(part.model.get_value(part.selected_row, 94))))
        part.txtVoltApplied.set_text(str(fmt.format(part.model.get_value(part.selected_row, 66))))
        part.txtACVoltApplied.set_text(str(fmt.format(part.model.get_value(part.selected_row, 64))))
        part.txtCapacitance.set_text(str(fmt.format(part.model.get_value(part.selected_row, 15))))

        if (int(part.model.get_value(part.selected_row, 85)) <= 0):
            part.txtCommercialPiQ.set_text(str(fmt.format(part.model.get_value(part.selected_row, 79))))
        else:
            part.txtCommercialPiQ.set_text("0.0")

        return False

    def assessment_results_create(self, part, layout, x_pos, y_pos):

        """ Populates the RelKit Workbook calculation results tab with the
            widgets to display Capacitor Component Class calculation results.

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
                lbllayout = label.get_layout()
                lbllayout.set_alignment(pango.ALIGN_CENTER)
                label.show_all()
            else:
                label = _widg.make_label(self._out_labels[i])
            layout.put(label, 5, (i * 30 + y_pos))

        part.txtTRise = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtTRise, x_pos, y_pos)
        y_pos += 30

        part.txtTJunc = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtTJunc, x_pos, y_pos)
        y_pos += 60                         # Increment by 60 to make room to
                                            # display reliability formula.

        part.txtLambdaB = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtLambdaB, x_pos, y_pos)
        y_pos += 30

        part.txtPiQ = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiQ, x_pos, y_pos)
        y_pos += 30

        part.txtPiE = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiE, x_pos, y_pos)
        y_pos += 30

        # Create the Pi CV results entry.  We store the Pi CV value in the
        # pi_cf field in the program database.
        part.txtPiCV = _widg.make_entry(editable=False, bold=True)
        layout.put(part.txtPiCV, x_pos, y_pos)
        y_pos += 30

        layout.show_all()

        self._ready = True

        return(y_pos)

    def assessment_results_load(self, part):

        """ Loads the RelKit Workbook calculation results widgets with
            calculation results.

            Keyword Arguments:
            part -- the RelKit COMPONENT object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        part.txtTRise.set_text(str(fmt.format(part.model.get_value(part.selected_row, 107))))
        part.txtTJunc.set_text(str(fmt.format(part.model.get_value(part.selected_row, 39))))
        part.txtLambdaB.set_text(str(fmt.format(part.model.get_value(part.selected_row, 46))))
        part.txtPiQ.set_text(str('{0:0.2g}'.format(part.model.get_value(part.selected_row, 79))))
        part.txtPiE.set_text(str('{0:0.2g}'.format(part.model.get_value(part.selected_row, 72))))
        part.txtPiCV.set_text(str(fmt.format(part.model.get_value(part.selected_row, 70))))

        return False

    def _callback_combo(self, combo, part, _index_):

        """ Callback function for handling Capacitor Class ComboBox changes.

            Keyword Arguments:
              combo -- the combobox widget calling this function.
               part -- the RelKit COMPONENT object.
            _index_ -- the user-definded index for the calling combobx.

        """

        #try:
        model = part._app.winParts.full_model
        row = part._app.winParts.model.convert_iter_to_child_iter(part._app.winParts.selected_row)
        #except:
        #    return True

        idx = combo.get_active()

        # Update the Component object property and the Parts List treeview.
        model.set_value(row, _index_, int(idx))

        if(_index_ == 85):                      # Quality
            if(part.txtCommercialPiQ.get_text() == ""):
                CpiQ = 0.0
            else:
                CpiQ = float(part.txtCommercialPiQ.get_text())

            # Use this value for piQ if not being over-ridden.
            if(CpiQ <= 0.0):
                model.set_value(row, 79, self._piQ[idx - 1])

        elif(_index_ == 101):                   # Specification
            part.cmbSpecSheet.get_model().clear()
            for i in range(len(self._specsheet[idx - 1])):
                part.cmbSpecSheet.insert_text(i, self._specsheet[idx - 1][i])

        return False

    def _callback_entry(self, entry, event, part, convert, _index_):

        """ Callback function for handling Capacitor Class Entry changes.

            Keyword Arguments:
              entry -- the entry widget calling this function.
              event -- the event that triggered calling this function.
               part -- the RelKit COMPONENT object.
            convert -- the data type to convert the entry contents to.
            _index_ -- the position in the Component property array
                       associated with the data from the entry that called
                       this function.

        """

        try:
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
