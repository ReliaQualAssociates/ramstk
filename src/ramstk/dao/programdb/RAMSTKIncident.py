# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKIncident.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RAMSTKIncident Table
===============================================================================
"""

from datetime import date, timedelta

from sqlalchemy import BLOB, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import error_handler, none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


# pylint: disable=R0902
class RAMSTKIncident(RAMSTK_BASE):
    """
    Class to represent the table ramstk_validation in the RAMSTK Program datanase.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-One relationship with ramstk_incident_detail.
    This table shares a One-to-Many relationship with ramstk_incident_action.
    """

    __tablename__ = 'ramstk_incident'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    incident_id = Column(
        'fld_incident_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    accepted = Column('fld_accepted', Integer, default=0)
    approved = Column('fld_approved', Integer, default=0)
    approved_by = Column('fld_approved_by', Integer, default=0)
    analysis = Column('fld_analysis', BLOB, default='')
    category_id = Column('fld_category_id', Integer, default=0)
    chargeable = Column('fld_chargeable', Integer, default=-1)
    chargeable_1 = Column('fld_chargeable_1', Integer, default=-1)
    chargeable_2 = Column('fld_chargeable_2', Integer, default=-1)
    chargeable_3 = Column('fld_chargeable_3', Integer, default=-1)
    chargeable_4 = Column('fld_chargeable_4', Integer, default=-1)
    chargeable_5 = Column('fld_chargeable_5', Integer, default=-1)
    chargeable_6 = Column('fld_chargeable_6', Integer, default=-1)
    chargeable_7 = Column('fld_chargeable_7', Integer, default=-1)
    chargeable_8 = Column('fld_chargeable_8', Integer, default=-1)
    chargeable_9 = Column('fld_chargeable_9', Integer, default=-1)
    chargeable_10 = Column('fld_chargeable_10', Integer, default=-1)
    complete = Column('fld_complete', Integer, default=0)
    complete_by = Column('fld_complete_by', Integer, default=0)
    cost = Column('fld_cost', Float, default=0.0)
    criticality_id = Column('fld_criticality_id', Integer, default=0)
    date_approved = Column(
        'fld_date_approved', Date, default=date.today() + timedelta(days=30))
    date_complete = Column(
        'fld_date_complete', Date, default=date.today() + timedelta(days=30))
    date_requested = Column('fld_date_requested', Date, default=date.today())
    date_reviewed = Column(
        'fld_date_reviewed', Date, default=date.today() + timedelta(days=30))
    description_long = Column('fld_description_long', BLOB, default='')
    description_short = Column(
        'fld_description_short', String(512), default='')
    detection_method_id = Column('fld_detection_method_id', Integer, default=0)
    execution_time = Column('fld_execution_time', Float, default=0)
    hardware_id = Column('fld_hardware_id', Integer, default=0)
    incident_age = Column('fld_incident_age', Integer, default=0)
    life_cycle_id = Column('fld_life_cycle_id', Integer, default=0)
    relevant = Column('fld_relevant', Integer, default=-1)
    relevant_1 = Column('fld_relevant_1', Integer, default=-1)
    relevant_2 = Column('fld_relevant_2', Integer, default=-1)
    relevant_3 = Column('fld_relevant_3', Integer, default=-1)
    relevant_4 = Column('fld_relevant_4', Integer, default=-1)
    relevant_5 = Column('fld_relevant_5', Integer, default=-1)
    relevant_6 = Column('fld_relevant_6', Integer, default=-1)
    relevant_7 = Column('fld_relevant_7', Integer, default=-1)
    relevant_8 = Column('fld_relevant_8', Integer, default=-1)
    relevant_9 = Column('fld_relevant_9', Integer, default=-1)
    relevant_10 = Column('fld_relevant_10', Integer, default=-1)
    relevant_11 = Column('fld_relevant_11', Integer, default=-1)
    relevant_12 = Column('fld_relevant_12', Integer, default=-1)
    relevant_13 = Column('fld_relevant_13', Integer, default=-1)
    relevant_14 = Column('fld_relevant_14', Integer, default=-1)
    relevant_15 = Column('fld_relevant_15', Integer, default=-1)
    relevant_16 = Column('fld_relevant_16', Integer, default=-1)
    relevant_17 = Column('fld_relevant_17', Integer, default=-1)
    relevant_18 = Column('fld_relevant_18', Integer, default=-1)
    relevant_19 = Column('fld_relevant_19', Integer, default=-1)
    relevant_20 = Column('fld_relevant_20', Integer, default=-1)
    remarks = Column('fld_remarks', BLOB, default='')
    request_by = Column('fld_request_by', Integer, default=0)
    reviewed = Column('fld_reviewed', Integer, default=0)
    reviewed_by = Column('fld_reviewed_by', Integer, default=0)
    software_id = Column('fld_software_id', Integer, default=0)
    status_id = Column('fld_status', Integer, default=0)
    test_case = Column('fld_test_case', String(512), default='')
    test_found = Column('fld_test_found', String(512), default='')
    type_id = Column('fld_type_id', Integer, default=0)
    unit = Column('fld_unit', String(256), default='')

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='incident')
    incident_detail = relationship(
        'RAMSTKIncidentDetail', back_populates='incident')
    incident_action = relationship(
        'RAMSTKIncidentAction', back_populates='incident')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Incident data model
        attributes.

        :return: (revision_id, incident_id, accepted, approved, approved_by,
                  analysis, category_id, chargeable, chargeable_1,
                  chargeable_2, chargeable_3, chargeable_4, chargeable_5,
                  chargeable_6, chargeable_7, chargeable_8, chargeable_9,
                  chargeable_10, complete, complete_by, cost, criticality_id,
                  date_approved, date_complete, date_requested, date_reviewed,
                  description_long, description_short, detection_method_id,
                  execution_time, hardware_id, incident_age, life_cycle_id,
                  relevant, relevant_1, relevant_2, relevant_3, relevant_4,
                  relevant_5, relevant_6, relevant_7, relevant_8, relevant_9,
                  relevant_10, relevant_11, relevant_12, relevant_13,
                  relevant_14, relevant_15, relevant_16, relevant_17,
                  relevant_18, relevant_19, relevant_20, remarks, request_by,
                  reviewed, reviewed_by, software_id, status_id, test_case,
                  test_found, type_id, unit)
        :rtype: tuple
        """

        _attributes = (
            self.revision_id, self.incident_id, self.accepted, self.approved,
            self.approved_by, self.analysis, self.category_id, self.chargeable,
            self.chargeable_1, self.chargeable_2, self.chargeable_3,
            self.chargeable_4, self.chargeable_5, self.chargeable_6,
            self.chargeable_7, self.chargeable_8, self.chargeable_9,
            self.chargeable_10, self.complete, self.complete_by, self.cost,
            self.criticality_id, self.date_approved, self.date_complete,
            self.date_requested, self.date_reviewed, self.description_long,
            self.description_short, self.detection_method_id,
            self.execution_time, self.hardware_id, self.incident_age,
            self.life_cycle_id, self.relevant, self.relevant_1,
            self.relevant_2, self.relevant_3, self.relevant_4, self.relevant_5,
            self.relevant_6, self.relevant_7, self.relevant_8, self.relevant_9,
            self.relevant_10, self.relevant_11, self.relevant_12,
            self.relevant_13, self.relevant_14, self.relevant_15,
            self.relevant_16, self.relevant_17, self.relevant_18,
            self.relevant_19, self.relevant_20, self.remarks, self.request_by,
            self.reviewed, self.reviewed_by, self.software_id, self.status_id,
            self.test_case, self.test_found, self.type_id, self.unit)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RAMSTKIncident data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKIncident {0:d} attributes.". \
               format(self.incident_id)

        try:
            self.accepted = int(none_to_default(attributes[0], 0))
            self.approved = int(none_to_default(attributes[1], 0))
            self.approved_by = int(none_to_default(attributes[2], 0))
            self.analysis = str(none_to_default(attributes[3], ''))
            self.category_id = int(none_to_default(attributes[4], 0))
            self.chargeable = int(none_to_default(attributes[5], -1))
            self.chargeable_1 = int(none_to_default(attributes[6], -1))
            self.chargeable_2 = int(none_to_default(attributes[7], -1))
            self.chargeable_3 = int(none_to_default(attributes[8], -1))
            self.chargeable_4 = int(none_to_default(attributes[9], -1))
            self.chargeable_5 = int(none_to_default(attributes[10], -1))
            self.chargeable_6 = int(none_to_default(attributes[11], -1))
            self.chargeable_7 = int(none_to_default(attributes[12], -1))
            self.chargeable_8 = int(none_to_default(attributes[13], -1))
            self.chargeable_9 = int(none_to_default(attributes[14], -1))
            self.chargeable_10 = int(none_to_default(attributes[15], -1))
            self.complete = int(none_to_default(attributes[16], 0))
            self.complete_by = int(none_to_default(attributes[17], 0))
            self.cost = float(none_to_default(attributes[18], 0.0))
            self.criticality_id = int(none_to_default(attributes[19], 0))
            self.date_approved = none_to_default(
                attributes[20], date.today() + timedelta(days=30))
            self.date_complete = none_to_default(
                attributes[21], date.today() + timedelta(days=30))
            self.date_requested = none_to_default(attributes[22], date.today())
            self.date_reviewed = none_to_default(
                attributes[23], date.today() + timedelta(days=30))
            self.description_long = str(none_to_default(attributes[24], ''))
            self.description_short = str(none_to_default(attributes[25], ''))
            self.detection_method_id = int(none_to_default(attributes[26], 0))
            self.execution_time = float(none_to_default(attributes[27], 0.0))
            self.hardware_id = int(none_to_default(attributes[28], 0))
            self.incident_age = int(none_to_default(attributes[29], 0))
            self.life_cycle_id = int(none_to_default(attributes[30], 0))
            self.relevant = int(none_to_default(attributes[31], -1))
            self.relevant_1 = int(none_to_default(attributes[32], -1))
            self.relevant_2 = int(none_to_default(attributes[33], -1))
            self.relevant_3 = int(none_to_default(attributes[34], -1))
            self.relevant_4 = int(none_to_default(attributes[35], -1))
            self.relevant_5 = int(none_to_default(attributes[36], -1))
            self.relevant_6 = int(none_to_default(attributes[37], -1))
            self.relevant_7 = int(none_to_default(attributes[38], -1))
            self.relevant_8 = int(none_to_default(attributes[39], -1))
            self.relevant_9 = int(none_to_default(attributes[40], -1))
            self.relevant_10 = int(none_to_default(attributes[41], -1))
            self.relevant_11 = int(none_to_default(attributes[42], -1))
            self.relevant_12 = int(none_to_default(attributes[43], -1))
            self.relevant_13 = int(none_to_default(attributes[44], -1))
            self.relevant_14 = int(none_to_default(attributes[45], -1))
            self.relevant_15 = int(none_to_default(attributes[46], -1))
            self.relevant_16 = int(none_to_default(attributes[47], -1))
            self.relevant_17 = int(none_to_default(attributes[48], -1))
            self.relevant_18 = int(none_to_default(attributes[49], -1))
            self.relevant_19 = int(none_to_default(attributes[50], -1))
            self.relevant_20 = int(none_to_default(attributes[51], -1))
            self.remarks = str(none_to_default(attributes[52], ''))
            self.request_by = int(none_to_default(attributes[53], 0))
            self.reviewed = int(none_to_default(attributes[54], 0))
            self.reviewed_by = int(none_to_default(attributes[55], 0))
            self.software_id = int(none_to_default(attributes[56], 0))
            self.status_id = int(none_to_default(attributes[57], 0))
            self.test_case = str(none_to_default(attributes[58], ''))
            self.test_found = str(none_to_default(attributes[59], ''))
            self.type_id = int(none_to_default(attributes[60], 0))
            self.unit = str(none_to_default(attributes[61], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKIncident.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKIncident attributes."

        return _error_code, _msg
