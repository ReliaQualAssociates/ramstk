# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Miscellaneous.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Miscellaneous Parts Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


class MiscAssessmentInputs(AssessmentInputs):
    """
    Display Miscellaneous assessment input attribute data in the RAMSTK Work Book.

    The Miscellaneous hardware assessment input view displays all the
    assessment inputs for the selected miscellaneous hardware item.  This
    includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    Miscellaneous hardware assessment input view are:

    :ivar cmbApplication: select and display the application of the
                          miscellaneous item (lamps only).
    :ivar cmbType: the type of miscellaneous item (filters only).
    :ivar txtFrequency: enter and display the operating frequency of the
                        miscellaneous item (crystals only).
    :ivar txtUtilization: enter and display the utilization factor of the
                          miscellaneous item (lamps only).

    Callbacks signals in _lst_handler_id:

    +-------+----------------------------+
    | Index | Widget - Signal            |
    +=======+============================+
    |   0   | cmbQuality - `changed`     |
    +-------+----------------------------+
    |   1   | cmbApplication - `changed` |
    +-------+----------------------------+
    |   2   | cmbType - `changed`        |
    +-------+----------------------------+
    |   3   | txtFrequency - `changed`   |
    +-------+----------------------------+
    |   4   | txtUtilization - `changed` |
    +-------+----------------------------+
    """

    # Define private dictionary attributes.
    _dic_keys = {0: 'quality_id', 1: 'application_id', 2: 'type_id', 3: 'frequency_operating', 4: 'duty_cycle'}

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Application:"),
        _("Type:"),
        _("Operating Frequency:"),
        _("Utilization:"),
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Miscellaneous assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentInputs.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = RAMSTKComboBox(
            index=0, simple=True,
        )
        self.cmbType = RAMSTKComboBox(
            index=0, simple=True,
        )

        self.txtFrequency = RAMSTKEntry()
        self.txtUtilization = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the Misc hardware class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

        self.put(self.cmbApplication, _x_pos, _y_pos[1])
        self.put(self.cmbType, _x_pos, _y_pos[2])
        self.put(self.txtFrequency, _x_pos, _y_pos[3])
        self.put(self.txtUtilization, _x_pos, _y_pos[4])

        self.show_all()

    def __set_callbacks(self):
        """
        Set callback methods for Misc hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self.on_combo_changed, 0),
        )
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self.on_combo_changed, 1),
        )
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self.on_combo_changed, 2),
        )
        self._lst_handler_id.append(
            self.txtFrequency.connect('changed', self.on_focus_out, 3),
        )
        self._lst_handler_id.append(
            self.txtUtilization.connect('changed', self.on_focus_out, 4),
        )

    def __set_properties(self):
        """
        Set properties for Misc hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the lamp."),
        )
        self.cmbType.do_set_properties(
            tooltip=_("The type of electronic filter."),
        )

        self.txtFrequency.do_set_properties(
            width=125, tooltip=_("The operating frequency of the crystal."),
        )
        self.txtUtilization.do_set_properties(
            width=125,
            tooltip=_(
                "The utilization factor (illuminate hours / equipment "
                "operate hours) of the lamp.",
            ),
        )

    def _do_load_comboboxes(self, subcategory_id):  # pylint: disable=unused-argument
        """
        Load the miscellaneous RKTComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the miscellaneous subcategory is changed.

        :param int subcategory_id: the newly selected miscellaneous hardware
                                   item subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_("Lower")]])

        # Load the application RAMSTKComboBox().
        self.cmbApplication.do_load_combo([
            [_("Incandescent, AC")],
            [_("Incandescent, DC")],
        ])

        # Load the type RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            self.cmbType.do_load_combo(
                [
                    [_("Ceramic-Ferrite")], [_("Discrete LC Components")],
                    [_("Discrete LC and Crystal Components")],
                ],
            )
        elif self._hazard_rate_method_id == 2:
            self.cmbType.do_load_combo(
                [
                    [_("MIL-F-15733 Ceramic-Ferrite")],
                    [_("MIL-F-15733 Discrete LC Components")],
                    [_("MIL-F-18327 Discrete LC Components")],
                    [_("MIL-F-18327 Discrete LC and Crystal Components")],
                ],
            )

    def _do_load_page(self, attributes):
        """
        Load the Miscellaneous assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Miscellaneous item.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

        if self._subcategory_id == 4:  # Lamp
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])
        elif self._subcategory_id == 2:  # Filter
            self.cmbType.handler_block(self._lst_handler_id[2])
            self.cmbType.set_active(attributes['type_id'])
            self.cmbType.handler_unblock(self._lst_handler_id[2])

        if self._hazard_rate_method_id == 2:
            if self._subcategory_id == 1:  # Crystal
                self.txtFrequency.handler_block(self._lst_handler_id[3])
                self.txtFrequency.set_text(
                    str(self.fmt.format(attributes['frequency_operating'])),
                )
                self.txtFrequency.handler_unblock(self._lst_handler_id[3])
            elif self._subcategory_id == 4:  # Lamp
                self.txtUtilization.handler_block(self._lst_handler_id[4])
                self.txtUtilization.set_text(
                    str(self.fmt.format(attributes['duty_cycle'])),
                )
                self.txtUtilization.handler_unblock(self._lst_handler_id[4])

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected miscellaneous.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequency.set_sensitive(False)
        self.txtUtilization.set_sensitive(False)

        if self._subcategory_id == 4:  # Lamp
            self.cmbApplication.set_sensitive(True)
        elif self._subcategory_id == 2:  # Filter
            self.cmbType.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id in [1, 2]:  # Crystal or filter
                self.cmbQuality.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            if self._subcategory_id == 1:  # Crystal
                self.cmbQuality.set_sensitive(True)
                self.txtFrequency.set_sensitive(True)
            elif self._subcategory_id == 4:  # Lamp
                self.txtUtilization.set_sensitive(True)
            elif self._subcategory_id == 2:  # Filter
                self.cmbQuality.set_sensitive(True)


class MiscAssessmentResults(AssessmentResults):
    """
    Display Misc assessment results attribute data in the RAMSTK Work Book.

    The Miscellaneous hardware item assessment result view displays all the
    assessment results for the selected miscellaneous hardware item.  This
    includes, currently, results for MIL-HDBK-217FN2 parts count and
    MIL-HDBK-217FN2 part stress methods.  The attributes of a miscellaneous
    hardware item assessment result view are:

    :ivar txtPiA: displays the application factor for the miscellaneous
                  hardware item.
    :ivar txtPiU: displays the utilization factor for the miscellaneous
                  hardware item.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E</sub></span>",
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Miscellaneous assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>U</sub>:")
        self._lst_labels.append("\u03C0<sub>A</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiU = RAMSTKEntry()
        self.txtPiA = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the Misc hardware item Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

        self.put(self.txtPiU, _x_pos, _y_pos[3])
        self.put(self.txtPiA, _x_pos, _y_pos[4])

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Misc hardware assessment result widgets.

        :return: None
        :rtype: None
        """
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the hardware item "
                "failure rate.",
            ),
        )

        self.txtPiU.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The utilization factor for the lamp."),
        )
        self.txtPiA.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The application factor for the lamp."),
        )

    def _do_load_page(self, attributes):
        """
        Load the miscellaneous devices assessment results page.

        :param dict attributes: the attributes dictionary for the selected
                                Miscellaneous item.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiU.set_text(str(self.fmt.format(attributes['piU'])))
        self.txtPiA.set_text(str(self.fmt.format(attributes['piA'])))

        if (
                self._hazard_rate_method_id == 1
                and self._subcategory_id in [3, 4]
        ):
            self._lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                "\u03BB<sub>g</sub></span>",
            )

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected Misc hardware.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiU.set_sensitive(False)
        self.txtPiA.set_sensitive(False)
        self.txtPiQ.set_sensitive(False)
        self.txtPiE.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id in [1, 2]:
                self.txtPiQ.set_sensitive(True)
            self.txtPiE.set_sensitive(False)
        elif self._hazard_rate_method_id == 2:
            if self._subcategory_id in [1, 2]:
                self.txtPiQ.set_sensitive(True)
            elif self._subcategory_id == 4:
                self.txtPiU.set_sensitive(True)
                self.txtPiA.set_sensitive(True)
