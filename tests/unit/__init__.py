#!/usr/bin/env python -O
"""
This is the test package for testing RTK.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.__init__.py is part of The RTK Project
#
# All rights reserved.
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

from sqlalchemy import create_engine

import Configuration as Configuration
import Utilities as Utilities
from dao.DAO import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


def setUp():

    if os.path.isfile('/tmp/rtk_debug.log'):
        os.remove('/tmp/rtk_debug.log')

    if os.path.isfile('/tmp/rtk_user.log'):
        os.remove('/tmp/rtk_user.log')

    engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)

    # Create all the tables in the test database.
    RTKRevision.__table__.create(bind=engine)
    RTKMission.__table__.create(bind=engine)
    RTKMissionPhase.__table__.create(bind=engine)
    RTKEnvironment.__table__.create(bind=engine)
    RTKFailureDefinition.__table__.create(bind=engine)
    RTKFunction.__table__.create(bind=engine)
    RTKRequirement.__table__.create(bind=engine)
    RTKStakeholderInput.__table__.create(bind=engine)
    RTKMatrix.__table__.create(bind=engine)
    RTKHardware.__table__.create(bind=engine)
    RTKAllocation.__table__.create(bind=engine)
    RTKHazard.__table__.create(bind=engine)
    RTKSimilarItem.__table__.create(bind=engine)
    RTKReliability.__table__.create(bind=engine)
    RTKMilHdbkF.__table__.create(bind=engine)
    RTKNSWC.__table__.create(bind=engine)
    RTKDesignElectric.__table__.create(bind=engine)
    RTKDesignMechanic.__table__.create(bind=engine)
    RTKMode.__table__.create(bind=engine)
    RTKMechanism.__table__.create(bind=engine)
    RTKCause.__table__.create(bind=engine)
    RTKControl.__table__.create(bind=engine)
    RTKAction.__table__.create(bind=engine)
    RTKOpLoad.__table__.create(bind=engine)
    RTKOpStress.__table__.create(bind=engine)
    RTKTestMethod.__table__.create(bind=engine)
    RTKSoftware.__table__.create(bind=engine)
    RTKSoftwareDevelopment.__table__.create(bind=engine)
    RTKSRRSSR.__table__.create(bind=engine)
    RTKPDR.__table__.create(bind=engine)
    RTKCDR.__table__.create(bind=engine)
    RTKTRR.__table__.create(bind=engine)
    RTKSoftwareTest.__table__.create(bind=engine)
    RTKValidation.__table__.create(bind=engine)
    RTKIncident.__table__.create(bind=engine)
    RTKIncidentDetail.__table__.create(bind=engine)
    RTKIncidentAction.__table__.create(bind=engine)
    RTKTest.__table__.create(bind=engine)
    RTKGrowthTest.__table__.create(bind=engine)
    RTKSurvival.__table__.create(bind=engine)
    RTKSurvivalData.__table__.create(bind=engine)

    Configuration.RTK_HR_MULTIPLIER = 1.0
    Configuration.RTK_DEBUG_LOG = Utilities.create_logger("RTK.debug",
                                                          'DEBUG',
                                                          '/tmp/rtk_debug.log')
    Configuration.RTK_USER_LOG = Utilities.create_logger("RTK.user",
                                                         'INFO',
                                                         '/tmp/rtk_user.log')

def tearDown():

    if os.path.isfile('/tmp/TestDB.rtk'):
        os.remove('/tmp/TestDB.rtk')

