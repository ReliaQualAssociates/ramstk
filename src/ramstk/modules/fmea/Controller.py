# -*- coding: utf-8 -*-
#
#       ramstk.analyses.fmea.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Controller."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController
from ramstk.Utilities import OutOfRangeError

# RAMSTK Local Imports
from . import dtmFMEA


class FMEADataController(RAMSTKDataController):
    """
    Provide an interface between the FMEA data model and an RAMSTK view model.

    A single FMEA controller can manage one or more FMEA data models.
    The attributes of a FMEA data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a FMEA data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the FMEA Data
                    Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmFMEA(dao, **kwargs),
            ramstk_module='FMEA',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._request_do_select_all, 'selected_function')
        pub.subscribe(self._request_do_select_all, 'selected_hardware')
        pub.subscribe(self.request_do_delete, 'request_delete_fmea')
        pub.subscribe(self._request_do_insert, 'request_insert_fmea')
        pub.subscribe(self.request_do_update, 'request_update_fmea')
        pub.subscribe(self.request_set_attributes, 'wvw_editing_fmea')

    def _request_do_select_all(self, attributes):
        """
        Load the entire FMEA for a Function or Hardware item.

        :param dict attributes: the key:value pairs of the FMEA attributes.
        :return: tree; the FMEA treelib Tree().
        :rtype: :class:`treelib.Tree`
        """
        _functional = False
        try:
            _parent_id = attributes['function_id']
            _functional = True
        except KeyError:
            _parent_id = attributes['hardware_id']
        finally:
            _parent_id = None

        return self._dtm_data_model.do_select_all(
            parent_id=_parent_id,
            functional=_functional,
        )

    def _request_do_insert(self, entity_id, parent_id, level, **kwargs):  # pylint: disable=unused-argument
        """
        Request to add a FMEA table record.

        :param int entity_id: the ID of the new element to insert.
        :param int parent_id: the ID of the parent element in the FMEA.
        :param str level: the level in the FMEA the new insert will be.  Levels
                          are mode, mechanism, cause, control, and action.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            entity_id=entity_id,
            parent_id=parent_id,
            level=level,
        )

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + '  Failed to add a new {0:s} to the RAMSTK ' \
                'Program database.'.format(level)
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(
            self,
            _error_code,
            _msg,
            None,
        )

    def request_do_calculate(self, node_id, **kwargs):  # pylint: disable=unused-argument
        """
        Request the (D)FME(C)A be calculated.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Calculating (D)FME(C)A.'

        try:
            _error_code, _msg = self._dtm_data_model.do_calculate(
                node_id,
                **kwargs,
            )
        except OutOfRangeError:
            _error_code = 50
            _msg = (
                "RAMSTK WARNING: OutOfRangeError raised when calculating "
                "(D)FME(C)A."
            )

        return RAMSTKDataController.do_handle_results(
            self,
            _error_code,
            _msg,
            None,
        )

    def request_item_criticality(self):
        """
        Request the item criticality.

        :return: _item_criticality
        :rtype: float
        """
        return self._dtm_data_model.item_criticality
