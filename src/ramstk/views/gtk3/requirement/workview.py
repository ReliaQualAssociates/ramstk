# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Requirement Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton, RAMSTKCheckButton, RAMSTKComboBox, RAMSTKDateSelect,
    RAMSTKEntry, RAMSTKPanel, RAMSTKTextView, RAMSTKWorkView
)

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS


class GeneralDataPanel(RAMSTKPanel):
    """Panel to display general data about the selected Requirement."""
    def __init__(self) -> None:
        """Initialize an instance of the Requirement General Data panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Requirement Code:"),
            _("Requirement Description:"),
            _("Requirement Type:"),
            "",
            _("Specification:"),
            _("Page Number:"),
            _("Figure Number:"),
            _("Priority:"),
            _("Owner:"),
            "",
            _("Validated Date:"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("General Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.btnValidateDate: RAMSTKButton = RAMSTKButton()

        self.chkDerived: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirement is derived."))
        self.chkValidated: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirement is validated."))

        self.cmbOwner: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbRequirementType: RAMSTKComboBox = RAMSTKComboBox(index=1,
                                                                 simple=False)
        self.cmbPriority: RAMSTKComboBox = RAMSTKComboBox()

        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtFigNum: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtPageNum: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtValidatedDate: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'derived': [self.chkDerived.do_update, 'toggled', 2],
            'description': [self.txtName.do_update, 'changed', 3],
            'figure_number': [self.txtFigNum.do_update, 'changed', 4],
            'owner': [self.cmbOwner, 'changed', 5],
            'page_number': [self.txtPageNum.do_update, 'changed', 6],
            'priority': [self.cmbPriority, 'changed', 8],
            'specification': [self.txtSpecification.do_update, 'changed', 10],
            'requirement_type': [self.cmbRequirementType, 'changed', 11],
            'validated': [self.chkValidated.do_update, 'toggled', 12],
            'validated_date': [self.txtValidatedDate.do_update, 'changed', 13],
        }
        self._lst_widgets = [
            self.txtCode,
            self.txtName,
            self.cmbRequirementType,
            self.chkDerived,
            self.txtSpecification,
            self.txtPageNum,
            self.txtFigNum,
            self.cmbPriority,
            self.cmbOwner,
            self.chkValidated,
            self.txtValidatedDate,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_requirement')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_code, 'succeed_create_requirement_code')
        pub.subscribe(self._do_load_panel, 'selected_requirement')

    def do_load_priorities(self) -> None:
        """Load the priority RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _priorities: List[List[str]] = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

    def do_load_requirement_types(
            self, requirement_types: Dict[int, Tuple[str]]) -> None:
        """Load the requirement types RAMSTKComboBox().

        :param requirement_types:
        :return: None
        :rtype: None
        """
        _requirement_types: List[Tuple[str]] = []

        # pylint: disable=unused-variable
        for __, _key in enumerate(requirement_types):
            _requirement_types.append(requirement_types[_key])
        self.cmbRequirementType.do_load_combo(entries=_requirement_types,
                                              simple=False)

    def do_load_workgroups(self, workgroups: Dict[int, Tuple[str]]) -> None:
        """Load the workgroups RAMSTKComboBox().

        :param workgroups:
        :return: None
        :rtype: None
        """
        _owners = []

        # pylint: disable=unused-variable
        for __, _key in enumerate(workgroups):
            _owners.append(workgroups[_key])
        self.cmbOwner.do_load_combo(_owners)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', signal='changed')
        self.txtName.do_update('', signal='changed')

        self.cmbRequirementType.do_update(0, signal='changed')

        self.chkDerived.do_update(False, signal='toggled')
        self.txtSpecification.do_update('', signal='changed')
        self.txtPageNum.do_update('', signal='changed')
        self.txtFigNum.do_update('', signal='changed')

        self.cmbPriority.do_update(0, signal='changed')
        self.cmbOwner.do_update(0, signal='changed')

        self.chkValidated.do_update(False, signal='toggled')
        self.txtValidatedDate.do_update('', signal='changed')

    def _do_load_code(self, requirement_code: int) -> None:
        """Load the Requirement code RAMSTKEntry().

        :param requirement_code: the Requirement code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.do_update(str(requirement_code), signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Requirement General Data page widgets.

        :param attributes: the Requirement attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        self.txtCode.do_update(str(attributes['requirement_code']),
                               signal='changed')
        self.txtName.do_update(str(attributes['description']),
                               signal='changed')
        self.chkDerived.do_update(int(attributes['derived']), signal='toggled')
        self.cmbRequirementType.do_update(int(attributes['requirement_type']),
                                          signal='changed')
        self.txtSpecification.do_update(str(attributes['specification']),
                                        signal='changed')
        self.txtPageNum.do_update(str(attributes['page_number']),
                                  signal='changed')
        self.txtFigNum.do_update(str(attributes['figure_number']),
                                 signal='changed')
        self.cmbPriority.do_update(int(attributes['priority']),
                                   signal='changed')
        self.cmbOwner.do_update(int(attributes['owner']), signal='changed')
        self.chkValidated.do_update(int(attributes['validated']),
                                    signal='toggled')
        if attributes['validated']:
            self.txtValidatedDate.do_update(str(attributes['validated_date']),
                                            signal='changed')
        else:
            self.txtValidatedDate.do_update("", signal='changed')

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        """Request to launch a date selection dialog.

        This method is used to select the validation date for the Requirement.

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :param __event: the Gdk.Event() that called this method.
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _parent = entry.get_parent().get_parent().get_parent().get_parent(
        ).get_parent().get_parent().get_parent().get_parent().get_parent()

        _dialog: RAMSTKDateSelect = RAMSTKDateSelect(dlgparent=_parent)

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.do_update(_date)
        super().on_changed_entry(entry, 13, 'wvw_editing_requirement')

        return _date

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        self.btnValidateDate.dic_handler_id[
            'released'] = self.btnValidateDate.connect('button-release-event',
                                                       self._do_select_date,
                                                       self.txtValidatedDate)

        self.chkDerived.dic_handler_id['toggled'] = self.chkDerived.connect(
            'toggled',
            super().on_toggled, 2, 'wvw_editing_requirement')
        self.chkValidated.dic_handler_id[
            'toggled'] = self.chkValidated.connect('toggled',
                                                   super().on_toggled, 12,
                                                   'wvw_editing_requirement')

        self.cmbOwner.dic_handler_id['changed'] = self.cmbOwner.connect(
            'changed',
            super().on_changed_combo, 5, 'wvw_editing_requirement')
        self.cmbPriority.dic_handler_id['changed'] = self.cmbPriority.connect(
            'changed',
            super().on_changed_combo, 8, 'wvw_editing_requirement')
        self.cmbRequirementType.dic_handler_id[
            'changed'] = self.cmbRequirementType.connect(
                'changed',
                super().on_changed_combo, 11, 'wvw_editing_requirement')

        _buffer: Gtk.TextBuffer = self.txtName.do_get_buffer()
        self.txtName.dic_handler_id['changed'] = (_buffer.connect(
            'changed',
            super().on_changed_textview, 3, 'wvw_editing_requirement',
            self.txtName))
        self.txtFigNum.dic_handler_id['changed'] = self.txtFigNum.connect(
            'changed',
            super().on_changed_entry, 4, 'wvw_editing_requirement')
        self.txtPageNum.dic_handler_id['changed'] = self.txtPageNum.connect(
            'changed',
            super().on_changed_entry, 6, 'wvw_editing_requirement')
        self.txtCode.dic_handler_id['changed'] = self.txtCode.connect(
            'changed',
            super().on_changed_entry, 9, 'wvw_editing_requirement')
        self.txtSpecification.dic_handler_id[
            'changed'] = self.txtSpecification.connect(
                'changed',
                super().on_changed_entry, 10, 'wvw_editing_requirement')
        self.txtValidatedDate.dic_handler_id[
            'changed'] = self.txtValidatedDate.connect(
                'changed',
                super().on_changed_entry, 13, 'wvw_editing_requirement')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        # ----- BUTTONS
        self.btnValidateDate.do_set_properties(height=25, width=25)

        self.chkDerived.do_set_properties(tooltip=_(
            "Indicates whether or not the selected requirement is derived."),
                                          width=400)  # noqa
        self.chkValidated.do_set_properties(tooltip=_(
            "Indicates whether or not the selected requirement is validated."),
                                            width=400)  # noqa

        # ----- COMBOBOXES
        self.cmbPriority.do_set_properties(width=50)

        # ----- ENTRIES
        self.txtCode.do_set_properties(
            width=125,
            tooltip=_("A unique code for the selected requirement."))
        self.txtName.do_set_properties(
            height=100,
            width=800,
            tooltip=_("The description of the selected requirement."))
        self.txtValidatedDate.do_set_properties(
            tooltip=_("The date the selected requirement was validated."))


class AnalysisPanel(RAMSTKPanel):
    """Meta-Class for requirement analysis panels."""
    def __init__(self) -> None:
        """Initialize an instance of the Requirement analysis panel."""
        super().__init__()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_edit, 'mvw_editing_requirement')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_requirement')

    def do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        for _index, _checkbutton in enumerate(self._lst_widgets):
            _checkbutton.dic_handler_id['toggled'] = (_checkbutton.connect(
                'toggled',
                super().on_toggled, _index, 'wvw_editing_requirement'))

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        for _checkbutton in self._lst_widgets:
            _checkbutton.do_set_properties(height=30)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        for _checkbutton in self._lst_widgets:
            _checkbutton.do_update(False, signal='toggled')


class ClarityPanel(AnalysisPanel):
    """Panel to display clarity questions about the selected Requirement."""
    def __init__(self) -> None:
        """Initialize an instance of the Requirement clarity panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys = {
            0: ['q_clarity_0', 'integer'],
            1: ['q_clarity_1', 'integer'],
            2: ['q_clarity_2', 'integer'],
            3: ['q_clarity_3', 'integer'],
            4: ['q_clarity_4', 'integer'],
            5: ['q_clarity_5', 'integer'],
            6: ['q_clarity_6', 'integer'],
            7: ['q_clarity_7', 'integer'],
            8: ['q_clarity_8', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels = [
            _("1. The requirement clearly states what is needed or "
              "desired."),
            _("2. The requirement is unambiguous and not open to "
              "interpretation."),
            _("3. All terms that can have more than one meaning are "
              "qualified so that the desired meaning is readily "
              "apparent."),
            _("4. Diagrams, drawings, etc. are used to increase "
              "understanding of the requirement."),
            _("5. The requirement is free from spelling and "
              "grammatical errors."),
            _("6. The requirement is written in non-technical "
              "language using the vocabulary of the stakeholder."),
            _("7. Stakeholders understand the requirement as written."),
            _("8. The requirement is clear enough to be turned over "
              "to an independent group and still be understood."),
            _("9. The requirement avoids stating how the problem is "
              "to be solved or what techniques are to be used."),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Clarity of Requirement")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkClarityQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ8: RAMSTKCheckButton = RAMSTKCheckButton()

        self._dic_attribute_updater = {
            'q_clarity_0': [self.chkClarityQ0, 'toggled', 0],
            'q_clarity_1': [self.chkClarityQ1, 'toggled', 2],
            'q_clarity_2': [self.chkClarityQ2, 'toggled', 3],
            'q_clarity_3': [self.chkClarityQ3, 'toggled', 4],
            'q_clarity_4': [self.chkClarityQ4, 'toggled', 5],
            'q_clarity_5': [self.chkClarityQ5, 'toggled', 6],
            'q_clarity_6': [self.chkClarityQ6, 'toggled', 7],
            'q_clarity_7': [self.chkClarityQ7, 'toggled', 8],
            'q_clarity_8': [self.chkClarityQ8, 'toggled', 9],
        }

        self._lst_widgets = [
            self.chkClarityQ0,
            self.chkClarityQ1,
            self.chkClarityQ2,
            self.chkClarityQ3,
            self.chkClarityQ4,
            self.chkClarityQ5,
            self.chkClarityQ6,
            self.chkClarityQ7,
            self.chkClarityQ8,
        ]

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel_fixed(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Requirements clarity panel.

        :param attributes: the Requirement attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        for _index, _checkbutton in enumerate(self._lst_widgets):
            _checkbutton.do_update(int(
                attributes['q_clarity_{0:d}'.format(_index)]),
                                   signal='toggled')  # noqa


class CompletenessPanel(AnalysisPanel):
    """Panel to display completeness questions about selected Requirement."""
    def __init__(self) -> None:
        """Initialize an instance of the Requirement completeness panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys = {
            0: ['q_complete_0', 'integer'],
            1: ['q_complete_1', 'integer'],
            2: ['q_complete_2', 'integer'],
            3: ['q_complete_3', 'integer'],
            4: ['q_complete_4', 'integer'],
            5: ['q_complete_5', 'integer'],
            6: ['q_complete_6', 'integer'],
            7: ['q_complete_7', 'integer'],
            8: ['q_complete_8', 'integer'],
            9: ['q_complete_9', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels = [
            _("1. Performance objectives are properly documented from the "
              "user's point of view."),
            _("2. No necessary information is missing from the requirement."),
            _("3. The requirement has been assigned a priority."),
            _("4. The requirement is realistic given the technology that will "
              "be used to implement the system."),
            _("5. The requirement is feasible to implement given the defined "
              "project time frame, scope, structure and budget."),
            _("6. If the requirement describes something as a 'standard' the "
              "specific source is cited."),
            _("7. The requirement is relevant to the problem and its "
              "solution."),
            _("8. The requirement contains no implied design details."),
            _("9. The requirement contains no implied implementation "
              "constraints."),
            _("10. The requirement contains no implied project management "
              "constraints."),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Completeness of Requirement")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkCompleteQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ8: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ9: RAMSTKCheckButton = RAMSTKCheckButton()

        self._dic_attribute_updater = {
            'q_complete_0': [self.chkCompleteQ0, 'toggled', 0],
            'q_complete_1': [self.chkCompleteQ1, 'toggled', 1],
            'q_complete_2': [self.chkCompleteQ2, 'toggled', 2],
            'q_complete_3': [self.chkCompleteQ3, 'toggled', 3],
            'q_complete_4': [self.chkCompleteQ4, 'toggled', 4],
            'q_complete_5': [self.chkCompleteQ5, 'toggled', 5],
            'q_complete_6': [self.chkCompleteQ6, 'toggled', 6],
            'q_complete_7': [self.chkCompleteQ7, 'toggled', 7],
            'q_complete_8': [self.chkCompleteQ8, 'toggled', 8],
            'q_complete_9': [self.chkCompleteQ9, 'toggled', 9],
        }

        self._lst_widgets = [
            self.chkCompleteQ0,
            self.chkCompleteQ1,
            self.chkCompleteQ2,
            self.chkCompleteQ3,
            self.chkCompleteQ4,
            self.chkCompleteQ5,
            self.chkCompleteQ6,
            self.chkCompleteQ7,
            self.chkCompleteQ8,
            self.chkCompleteQ9,
        ]

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel_fixed(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Requirements clarity panel.

        :param attributes: the Requirement attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        for _index, _checkbutton in enumerate(self._lst_widgets):
            _checkbutton.do_update(int(
                attributes['q_complete_{0:d}'.format(_index)]),
                                   signal='toggled')  # noqa


class ConsistencyPanel(AnalysisPanel):
    """Panel to display consistency questions about selected Requirement."""
    def __init__(self) -> None:
        """Initialize an instance of the Requirement consistency panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys = {
            0: ['q_consistent_0', 'integer'],
            1: ['q_consistent_1', 'integer'],
            2: ['q_consistent_2', 'integer'],
            3: ['q_consistent_3', 'integer'],
            4: ['q_consistent_4', 'integer'],
            5: ['q_consistent_5', 'integer'],
            6: ['q_consistent_6', 'integer'],
            7: ['q_consistent_7', 'integer'],
            8: ['q_consistent_8', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels = [
            _("1. The requirement describes a single need or want; "
              "it could not be broken into several different "
              "requirements."),
            _("2. The requirement requires non-standard hardware or "
              "must use software to implement."),
            _("3. The requirement can be implemented within known "
              "constraints."),
            _("4. The requirement provides an adequate basis for "
              "design and testing."),
            _("5. The requirement adequately supports the business "
              "goal of the project."),
            _("6. The requirement does not conflict with some "
              "constraint, policy or regulation."),
            _("7. The requirement does not conflict with another "
              "requirement."),
            _("8. The requirement is not a duplicate of another "
              "requirement."),
            _("9. The requirement is in scope for the project."),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Consistency of Requirement")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkConsistentQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ8: RAMSTKCheckButton = RAMSTKCheckButton()

        self._dic_attribute_updater = {
            'q_consistent_0': [self.chkConsistentQ0, 'toggled', 0],
            'q_consistent_1': [self.chkConsistentQ1, 'toggled', 1],
            'q_consistent_2': [self.chkConsistentQ2, 'toggled', 2],
            'q_consistent_3': [self.chkConsistentQ3, 'toggled', 3],
            'q_consistent_4': [self.chkConsistentQ4, 'toggled', 4],
            'q_consistent_5': [self.chkConsistentQ5, 'toggled', 5],
            'q_consistent_6': [self.chkConsistentQ6, 'toggled', 6],
            'q_consistent_7': [self.chkConsistentQ7, 'toggled', 7],
            'q_consistent_8': [self.chkConsistentQ8, 'toggled', 8],
        }

        self._lst_widgets = [
            self.chkConsistentQ0,
            self.chkConsistentQ1,
            self.chkConsistentQ2,
            self.chkConsistentQ3,
            self.chkConsistentQ4,
            self.chkConsistentQ5,
            self.chkConsistentQ6,
            self.chkConsistentQ7,
            self.chkConsistentQ8,
        ]

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel_fixed(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Requirements clarity panel.

        :param attributes: the Requirement attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        for _index, _checkbutton in enumerate(self._lst_widgets):
            _checkbutton.do_update(int(
                attributes['q_consistent_{0:d}'.format(_index)]),
                                   signal='toggled')  # noqa


class VerifiabilityPanel(AnalysisPanel):
    """Panel to display verifiability questions about selected Requirement."""
    def __init__(self) -> None:
        """Initialize an instance of the Requirement verifiability panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys = {
            0: ['q_verifiable_0', 'integer'],
            1: ['q_verifiable_1', 'integer'],
            2: ['q_verifiable_2', 'integer'],
            3: ['q_verifiable_3', 'integer'],
            4: ['q_verifiable_4', 'integer'],
            5: ['q_verifiable_5', 'integer'],
        }

        # Initialize private list instance attributes.
        self._lst_labels = [
            _("1. The requirement is verifiable by testing, demonstration, "
              "review, or analysis."),
            _("2. The requirement lacks 'weasel words' (e.g. various, mostly, "
              "suitable, integrate, maybe, consistent, robust, modular, "
              "user-friendly, superb, good)."),
            _("3. Any performance criteria are quantified such that they are "
              "testable."),
            _("4. Independent testing would be able to determine whether the "
              "requirement has been satisfied."),
            _("5. The task(s) that will validate and verify the final design "
              "satisfies the requirement have been identified."),
            _("6. The identified V&amp;V task(s) have been added to the "
              "validation plan (e.g., DVP)"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Verifiability of Requirement")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkVerifiableQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ5: RAMSTKCheckButton = RAMSTKCheckButton()

        self._dic_attribute_updater = {
            'q_verifiable_0': [self.chkVerifiableQ0, 'toggled', 0],
            'q_verifiable_1': [self.chkVerifiableQ1, 'toggled', 1],
            'q_verifiable_2': [self.chkVerifiableQ2, 'toggled', 2],
            'q_verifiable_3': [self.chkVerifiableQ3, 'toggled', 3],
            'q_verifiable_4': [self.chkVerifiableQ4, 'toggled', 4],
            'q_verifiable_5': [self.chkVerifiableQ5, 'toggled', 5],
        }

        self._lst_widgets = [
            self.chkVerifiableQ0,
            self.chkVerifiableQ1,
            self.chkVerifiableQ2,
            self.chkVerifiableQ3,
            self.chkVerifiableQ4,
            self.chkVerifiableQ5,
        ]

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel_fixed(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Requirements clarity panel.

        :param attributes: the Requirement attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']

        for _index, _checkbutton in enumerate(self._lst_widgets):
            _checkbutton.do_update(int(
                attributes['q_verifiable_{0:d}'.format(_index)]),
                                   signal='toggled')  # noqa


class GeneralData(RAMSTKWorkView):
    """Display general Requirement attribute data in the RAMSTK Work Book.

    The Requirement Work View displays all the general data attributes for the
    selected Requirement.  The attributes of a requirement Work View are:

    :cvar str _module: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """
    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'requirement'
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _(
        "Displays general information for the selected Requirement.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Requirement Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons['create_code'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/create_code.png')

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_create_code)
        self._lst_icons.insert(0, 'create_code')
        self._lst_mnu_labels = [
            _("Create Code"),
            _("Save Selected Requirement"),
            _("Save All Requirements"),
        ]
        self._lst_tooltips = [
            _("Automatically create code for the selected requirement."),
            _("Save changes to the currently selected requirement."),
            _("Save changes to all requirements."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = GeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_cursor_active, 'succeed_create_code')

        pub.subscribe(self._do_set_record_id, 'selected_requirement')

    def _do_request_create_code(self, __button: Gtk.ToolButton) -> None:
        """Request that requirement codes be built.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prefix = self._pnlGeneralData.cmbRequirementType.get_value()

        super().do_set_cursor_busy()
        pub.sendMessage('request_create_requirement_code',
                        node_id=self._record_id,
                        prefix=_prefix)

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record and parent ID.

        :param attributes: the attributes dict for the selected requirement.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Requirement General Data tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        # Add the validation date dialog launcher button to the right of the
        # validated date RAMSTKEntry.
        _fixed: Gtk.Fixed = self._pnlGeneralData.get_children(
        )[0].get_children()[0].get_children()[0]
        _entry: RAMSTKEntry = _fixed.get_children()[-1]
        _x_pos: int = _fixed.child_get_property(_entry, 'x') + 205
        _y_pos: int = _fixed.child_get_property(_entry, 'y')
        _fixed.put(self._pnlGeneralData.btnValidateDate, _x_pos, _y_pos)

        self._pnlGeneralData.do_load_priorities()
        self._pnlGeneralData.do_load_requirement_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE)
        self._pnlGeneralData.do_load_workgroups(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_WORKGROUPS)

        self.pack_end(self._pnlGeneralData, True, True, 0)
        self.show_all()


class RequirementAnalysis(RAMSTKWorkView):
    """Display Requirement attribute data in the RAMSTK Work Book.

    The Requirement Analysis Work View displays all the analysis questions and
    answers for the selected Requirement. The attributes of a Requirement
    Analysis Work View are:

    :cvar str _module: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """
    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'requirement'
    _tablabel: str = "<span weight='bold'>" + _("Analysis") + "</span>"
    _tabtooltip: str = _("Analyzes the selected requirement.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Requirements analysis work view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._pnlClarity: RAMSTKPanel = ClarityPanel()
        self._pnlCompleteness: RAMSTKPanel = CompletenessPanel()
        self._pnlConsistency: RAMSTKPanel = ConsistencyPanel()
        self._pnlVerifiability: RAMSTKPanel = VerifiabilityPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_requirement')

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record and parent ID.

        :param attributes: the attributes dict for the selected requirement.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['requirement_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Requirement Analysis tab.

        :return: None
        :rtype: None
        """
        _vpaned_left, _vpaned_right = super().do_make_layout_llrr()

        _vpaned_left.pack1(self._pnlClarity, False)
        _vpaned_left.pack2(self._pnlCompleteness, False)
        _vpaned_right.pack1(self._pnlConsistency, False)
        _vpaned_right.pack2(self._pnlVerifiability, False)

        self.show_all()
