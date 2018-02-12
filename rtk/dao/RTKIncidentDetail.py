# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKIncidentDetail.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKIncidentDetail Table
===============================================================================
"""

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKIncidentDetail(RTK_BASE):
    """
    Class to represent the table rtk_incident_detail in the RTK Program
    database.

    This table shares a One-to-One relationship with rtk_incident.
    """

    __tablename__ = 'rtk_incident_detail'
    __table_args__ = {'extend_existing': True}

    incident_id = Column(
        'fld_incident_id',
        Integer,
        ForeignKey('rtk_incident.fld_incident_id'),
        primary_key=True,
        nullable=False)
    hardware_id = Column('fld_hardware_id', Integer, default=0)

    age_at_incident = Column('fld_age_at_incident', Float, default=0.0)
    cnd_nff = Column('fld_cnd_nff', Integer, default=0)
    failure = Column('fld_failure', Integer, default=0)
    initial_installation = Column(
        'fld_initial_installation', Integer, default=0)
    interval_censored = Column('fld_interval_censored', Integer, default=0)
    mode_type_id = Column('fld_mode_type_id', Integer, default=0)
    occ_fault = Column('fld_occ_fault', Integer, default=0)
    suspension = Column('fld_suspension', Integer, default=0)
    ttf = Column('fld_ttf', Float, default=0.0)
    use_cal_time = Column('fld_use_cal_time', Integer, default=0)
    use_op_time = Column('fld_use_op_time', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    incident = relationship('RTKIncident', back_populates='incident_detail')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Incident Component data
        model attributes.

        :return: (incident_id, hardware_id, age_at_incident, cnd_nff, failure,
                  initial_installation, interval_censored, mode_type,
                  occ_fault, suspension, ttf, use_cal_time, use_op_time)
        :rtype: tuple
        """

        _values = (self.incident_id, self.hardware_id, self.age_at_incident,
                   self.cnd_nff, self.failure, self.initial_installation,
                   self.interval_censored, self.mode_type_id, self.occ_fault,
                   self.suspension, self.ttf, self.use_cal_time,
                   self.use_op_time)

        return _values

    def set_attributes(self, values):
        """
        Method to set the Incident Component data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKIncidentDetail {0:d} attributes.". \
               format(self.incident_id)

        try:
            self.age_at_incident = float(none_to_default(values[0], 0.0))
            self.cnd_nff = int(none_to_default(values[1], 0))
            self.failure = int(none_to_default(values[2], 0))
            self.initial_installation = int(none_to_default(values[3], 0))
            self.interval_censored = int(none_to_default(values[4], 0))
            self.mode_type_id = int(none_to_default(values[5], 0))
            self.occ_fault = int(none_to_default(values[6], 0))
            self.suspension = int(none_to_default(values[7], 0))
            self.ttf = float(none_to_default(values[8], 0.0))
            self.use_op_time = int(none_to_default(values[9], 0))
            self.use_cal_time = int(none_to_default(values[10], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKIncidentDetail.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKIncidentDetail attributes."

        return _error_code, _msg
