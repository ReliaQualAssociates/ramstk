# -*- coding: utf-8 -*-
#
#       rtk.modules.RAMSTKDataController.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Datamodels Package RAMSTKDataController."""

from pubsub import pub  # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RAMSTKDataController(object):
    """
    Provide an interface between data models and RAMSTK views.

    This is the meta-class for all RAMSTK data controllers.

    :ivar _configuration: the :class:`rtk.Configuration.Configuration`
                          instance associated with the current RAMSTK instance.
    :ivar _dtm_data_model: the RAMSTKDataModel associated with the
                           RAMSTKDataController.
    :ivar bool _test: indicates whether or not Data Controller is being tested.
                      used to suppress pypubsub sending messages when running
                      tests.
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize a RAMSTKDataController instance.

        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        :keyword model: the RAMSTKDataModel() to associate.
        :rtk_module: the all lowercase name of the RAMSTK Module the Data
                     Controller is for.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._configuration = configuration
        self._dtm_data_model = kwargs['model']
        self._test = kwargs['test']

        self._module = None
        for __, char in enumerate(kwargs['rtk_module']):
            if char.isalpha():
                self._module = kwargs['rtk_module'].capitalize()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_handle_results(self, error_code, error_msg, pub_msg=None):
        """
        Handle the error code and error message from other methods.

        This methods processes the error code and error message from the
        insert, delete, update, and calculate methods.

        :param int error_code: the error code returned by the Data Model when
                               requested to insert.
        :param str error_msg: the error message returned by the Data Model when
                              requested to insert.
        :param str pub_msg: the message to be published by pypubsub.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # If the insert, delete, update, or calculation was successful log the
        # error message to the user log.  Otherwise, log it to the debug log.
        if error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(error_msg)

            if pub_msg is not None and not self._test:
                pub.sendMessage(pub_msg)
        else:
            self._configuration.RAMSTK_DEBUG_LOG.error(error_msg)
            _return = True

        return _return

    def request_do_select(self, node_id, **kwargs):
        """
        Request the RAMSTK Program database record associated with Node ID.

        :param int node_id: the Node ID to retrieve from the Tree.
        :return: the RAMSTK Program database record requested.
        """
        return self._dtm_data_model.do_select(node_id, **kwargs)

    def request_do_select_all(self, **kwargs):
        """
        Retrieve the treelib Tree() from the Data Model.

        :return: tree; the treelib Tree() of RAMSTKRequirement models in the
                 Requirement tree.
        :rtype: dict
        """
        return self._dtm_data_model.do_select_all(**kwargs)

    def request_get_attributes(self, node_id):
        """
        Request the attributes from the record associated with the Node ID.

        :param int node_id: the ID of the record in the RAMSTK Program database
                            whose attributes are being requested.
        :return: _attributes
        :rtype: dict
        """
        _entity = self.request_do_select(node_id)

        return _entity.get_attributes()

    def request_set_attributes(self, node_id, attributes):
        """
        Set the attributes of the record associated with the Node ID.

        :param int node_id: the ID of the record in the RAMSTK Program database
                            table whose attributes are to be set.
        :param dict attributes: the dictionary of attributes and values.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _entity = self.request_do_select(node_id)

        return _entity.set_attributes(attributes)

    def request_last_id(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request the last entity ID used in the RAMSTK Program database.

        :return: the last entity ID used.
        :rtype: int
        """
        return self._dtm_data_model.last_id
