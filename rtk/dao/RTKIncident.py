#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKIncident.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKIncident Package.
"""

from datetime import date, timedelta

# Import the database models.
from sqlalchemy import BLOB, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKIncident(Base):
    """
    Class to represent the table rtk_validation in the RTK Program datanase.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-One relationship with rtk_incident_detail.
    This table shares a One-to-Many relationship with rtk_incident_action.
    """

    __tablename__ = 'rtk_incident'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    incident_id = Column('fld_incident_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

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
    date_approved = Column('fld_date_approved', Date,
                           default=date.today() + timedelta(days=30))
    date_complete = Column('fld_date_complete', Date,
                           default=date.today() + timedelta(days=30))
    date_requested = Column('fld_date_requested', Date, default=date.today())
    date_reviewed = Column('fld_date_reviewed', Date,
                           default=date.today() + timedelta(days=30))
    description_long = Column('fld_description_long', BLOB, default='')
    description_short = Column('fld_description_short', String(512),
                               default='')
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

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='incident')
    incident_detail = relationship('RTKIncidentDetail',
                                   back_populates='incident')
    incident_action = relationship('RTKIncidentAction',
                                   back_populates='incident')

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

        _attributes = (self.revision_id, self.incident_id, self.accepted,
                       self.approved, self.approved_by, self.analysis,
                       self.category_id, self.chargeable, self.chargeable_1,
                       self.chargeable_2, self.chargeable_3, self.chargeable_4,
                       self.chargeable_5, self.chargeable_6, self.chargeable_7,
                       self.chargeable_8, self.chargeable_9,
                       self.chargeable_10, self.complete, self.complete_by,
                       self.cost, self.criticality_id, self.date_approved,
                       self.date_complete, self.date_requested,
                       self.date_reviewed, self.description_long,
                       self.description_short, self.detection_method_id,
                       self.execution_time, self.hardware_id,
                       self.incident_age, self.life_cycle_id, self.relevant,
                       self.relevant_1, self.relevant_2, self.relevant_3,
                       self.relevant_4, self.relevant_5, self.relevant_6,
                       self.relevant_7, self.relevant_8, self.relevant_9,
                       self.relevant_10, self.relevant_11, self.relevant_12,
                       self.relevant_13, self.relevant_14, self.relevant_15,
                       self.relevant_16, self.relevant_17, self.relevant_18,
                       self.relevant_19, self.relevant_20, self.remarks,
                       self.request_by, self.reviewed, self.reviewed_by,
                       self.software_id, self.status_id, self.test_case,
                       self.test_found, self.type_id, self.unit)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKIncident data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKIncident {0:d} attributes.". \
               format(self.incident_id)

        try:
            self.accepted = int(attributes[0])
            self.approved = int(attributes[1])
            self.approved_by = int(attributes[2])
            self.analysis = str(attributes[3])
            self.category_id = int(attributes[4])
            self.chargeable = int(attributes[5])
            self.chargeable_1 = int(attributes[6])
            self.chargeable_2 = int(attributes[7])
            self.chargeable_3 = int(attributes[8])
            self.chargeable_4 = int(attributes[9])
            self.chargeable_5 = int(attributes[10])
            self.chargeable_6 = int(attributes[11])
            self.chargeable_7 = int(attributes[12])
            self.chargeable_8 = int(attributes[13])
            self.chargeable_9 = int(attributes[14])
            self.chargeable_10 = int(attributes[15])
            self.complete = int(attributes[16])
            self.complete_by = int(attributes[17])
            self.cost = float(attributes[18])
            self.criticality_id = int(attributes[19])
            self.date_approved = attributes[20]
            self.date_complete = attributes[21]
            self.date_requested = attributes[22]
            self.date_reviewed = attributes[23]
            self.description_long = str(attributes[24])
            self.description_short = str(attributes[25])
            self.detection_method_id = int(attributes[26])
            self.execution_time = float(attributes[27])
            self.hardware_id = int(attributes[28])
            self.incident_age = int(attributes[29])
            self.life_cycle_id = int(attributes[30])
            self.relevant = int(attributes[31])
            self.relevant_1 = int(attributes[32])
            self.relevant_2 = int(attributes[33])
            self.relevant_3 = int(attributes[34])
            self.relevant_4 = int(attributes[35])
            self.relevant_5 = int(attributes[36])
            self.relevant_6 = int(attributes[37])
            self.relevant_7 = int(attributes[38])
            self.relevant_8 = int(attributes[39])
            self.relevant_9 = int(attributes[40])
            self.relevant_10 = int(attributes[41])
            self.relevant_11 = int(attributes[42])
            self.relevant_12 = int(attributes[43])
            self.relevant_13 = int(attributes[44])
            self.relevant_14 = int(attributes[45])
            self.relevant_15 = int(attributes[46])
            self.relevant_16 = int(attributes[47])
            self.relevant_17 = int(attributes[48])
            self.relevant_18 = int(attributes[49])
            self.relevant_19 = int(attributes[50])
            self.relevant_20 = int(attributes[51])
            self.remarks = str(attributes[52])
            self.request_by = int(attributes[53])
            self.reviewed = int(attributes[54])
            self.reviewed_by = int(attributes[55])
            self.software_id = int(attributes[56])
            self.status_id = int(attributes[57])
            self.test_case = str(attributes[58])
            self.test_found = str(attributes[59])
            self.type_id = int(attributes[60])
            self.unit = str(attributes[61])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKIncident.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKIncident attributes."

        return _error_code, _msg
