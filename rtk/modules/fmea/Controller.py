# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Controller."""

from pubsub import pub

# Import other RTK modules.
from rtk.Utilities import OutOfRangeError
from rtk.datamodels import RTKDataController
from . import dtmFMEA


class FMEADataController(RTKDataController):
    """
    Provide an interface between the FMEA data model and an RTK view model.

    A single FMEA controller can manage one or more FMEA data models.
    The attributes of a FMEA data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a FMEA data controller instance.

        :param dao: the RTK Program DAO instance to pass to the FMEA Data
                    Model.
        :type dao: :class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmFMEA(dao),
            rtk_module='FMEA',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select_all(self, parent_id, **kwargs):
        """
        Load the entire FMEA for a Function or Hardware item.

        :param int parent_id: the Function ID (functional FMEA) or Hardware ID
                              (hardware FMEA) to retrieve the FMEA and build
                              trees for.
        :return: tree; the FMEA treelib Tree().
        :rtype: :py:class:`treelib.Tree`
        """
        _functional = kwargs['functional']

        return self._dtm_data_model.select_all(
            parent_id, functional=_functional)

    def request_insert(self, entity_id, parent_id, level):
        """
        Request to add a FMEA table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            entity_id=entity_id, parent_id=parent_id, level=level)
        self._dtm_data_model.tree.show()
        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + '  Failed to add a new {0:s} to the RTK ' \
                'Program database.'.format(level)
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, node_id):
        """
        Request entity and it's children be deleted from the FMEA.

        :param str node_id: the Mode, Mechanism, Cause, Controle, or Action ID
                            to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.delete(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_update_all(self):
        """
        Request all (D)FME(C)A entities be saved to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_calculate(self):
        """
        Request the (D)FME(C)A be calculated.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _meg = 'RTK SUCCESS: Calculating (D)FME(C)A.'

        try:
            _error_code, _msg = self._dtm_data_model.calculate_rpn()
        except OutOfRangeError:
            _error_code = 50
            _msg = ("RTK WARNING: OutOfRangeError raised when calculating "
                    "(D)FME(C)A.")

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
