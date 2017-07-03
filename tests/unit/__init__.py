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
from sqlalchemy.orm import scoped_session, sessionmaker

import Configuration as Configuration
import Utilities as Utilities
from dao.DAO import *

from dao.RTKUser import RTKUser
from dao.RTKGroup import RTKGroup
from dao.RTKEnviron import RTKEnviron
from dao.RTKModel import RTKModel
from dao.RTKType import RTKType
from dao.RTKCategory import RTKCategory
from dao.RTKSubCategory import RTKSubCategory
from dao.RTKPhase import RTKPhase
from dao.RTKDistribution import RTKDistribution
from dao.RTKManufacturer import RTKManufacturer
from dao.RTKUnit import RTKUnit
from dao.RTKMethod import RTKMethod
from dao.RTKCriticality import RTKCriticality
from dao.RTKRPN import RTKRPN
from dao.RTKLevel import RTKLevel
from dao.RTKApplication import RTKApplication
from dao.RTKHazards import RTKHazards
from dao.RTKStakeholders import RTKStakeholders
from dao.RTKStatus import RTKStatus
from dao.RTKCondition import RTKCondition
from dao.RTKFailureMode import RTKFailureMode
from dao.RTKMeasurement import RTKMeasurement
from dao.RTKLoadHistory import RTKLoadHistory

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

    # Create all the tables in the test program database.
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

    engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the test common database.
    RTKUser.__table__.create(bind=engine)
    RTKGroup.__table__.create(bind=engine)
    RTKEnviron.__table__.create(bind=engine)
    RTKModel.__table__.create(bind=engine)
    RTKType.__table__.create(bind=engine)
    RTKCategory.__table__.create(bind=engine)
    RTKSubCategory.__table__.create(bind=engine)
    RTKPhase.__table__.create(bind=engine)
    RTKDistribution.__table__.create(bind=engine)
    RTKManufacturer.__table__.create(bind=engine)
    RTKUnit.__table__.create(bind=engine)
    RTKMethod.__table__.create(bind=engine)
    RTKCriticality.__table__.create(bind=engine)
    RTKRPN.__table__.create(bind=engine)
    RTKLevel.__table__.create(bind=engine)
    RTKApplication.__table__.create(bind=engine)
    RTKHazards.__table__.create(bind=engine)
    RTKStakeholders.__table__.create(bind=engine)
    RTKStatus.__table__.create(bind=engine)
    RTKCondition.__table__.create(bind=engine)
    RTKFailureMode.__table__.create(bind=engine)
    RTKMeasurement.__table__.create(bind=engine)
    RTKLoadHistory.__table__.create(bind=engine)

    # Add an entry to each table.  These are used as the DUT in each test
    # file.
    session.add(RTKUser())
    session.add(RTKGroup())
    session.add(RTKEnviron())
    session.add(RTKModel())
    session.add(RTKType())
    session.add(RTKPhase())
    session.add(RTKDistribution())
    session.add(RTKManufacturer())
    session.add(RTKUnit())
    session.add(RTKMethod())
    session.add(RTKCriticality())
    session.add(RTKRPN())
    session.add(RTKLevel())
    session.add(RTKApplication())
    session.add(RTKHazards())
    session.add(RTKStakeholders())
    session.add(RTKStatus())
    session.add(RTKCondition())
    session.add(RTKMeasurement())
    session.add(RTKLoadHistory())
    session.commit()

    _category = RTKCategory()
    session.add(_category)
    session.commit()
    _subcategory = RTKSubCategory()
    _subcategory.category_id = _category.category_id
    session.add(_subcategory)
    session.commit()
    _failuremode = RTKFailureMode()
    _failuremode.category_id = _category.category_id
    _failuremode.subcategory_id = _subcategory.subcategory_id
    session.add(_failuremode)
    session.commit()

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

    if os.path.isfile('/tmp/TestCommonDB.rtk'):
        os.remove('/tmp/TestCommonDB.rtk')

    #pass
