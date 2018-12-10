# -*- coding: utf-8 -*-
#
#       ramstk.modules.RAMSTKDataController.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Datamodels Package RAMSTKDataController."""

# Import third party modules.
from pubsub import pub

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


class RAMSTKDataController(object):
    """
    Provide an interface between data models and RAMSTK views.

    This is the meta-class for all RAMSTK data controllers.

    :ivar _configuration: the :class:`ramstk.Configuration.Configuration`
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
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :keyword model: the RAMSTKDataModel() to associate.
        :ramstk_module: the all lowercase name of the RAMSTK Module the Data
                     Controller is for.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._configuration = configuration
        self._dtm_data_model = kwargs['model']
        self._test = kwargs['test']

        self._module = None
        for __, char in enumerate(kwargs['ramstk_module']):
            if char.isalpha():
                self._module = kwargs['ramstk_module'].capitalize()

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

    def request_do_calculate(self, node_id, **kwargs):
        """
        Request to calculate the record.

        :param int node_id: the PyPubSub Tree() ID of the Stakeholder to
                            calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate(node_id, **kwargs)

    def request_do_calculate_all(self, **kwargs):
        """
        Request to calculate all records for the module.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate_all(**kwargs)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTK Program database table record.

        :param int node_id: the PyPubSub Tree() ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return self.do_handle_results(_error_code, _msg, None)

    def request_do_insert(self, **kwargs):
        """
        Request to add an RAMSTK Program database table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(**kwargs)

        return self.do_handle_results(_error_code, _msg, None)

    def request_do_select(self, node_id, **kwargs):
        """
        Request the RAMSTK Program database record associated with Node ID.

        :param int node_id: the Node ID to retrieve from the Tree.
        :return: the RAMSTK Program database record requested.
        """
        return self._dtm_data_model.do_select(node_id, **kwargs)

    def request_do_select_all(self, attributes):
        """
        Retrieve the treelib Tree() from the RAMSTK Data Model.

        The RAMSTK Data Model method sends the 'retrieved_<module>' PyPubSub
        message.

        :return: None
        :rtype: None
        """
        return self._dtm_data_model.do_select_all(
            revision_id=attributes['revision_id'])

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTK Program database table record.

        :param int node_id: the PyPubSub Tree() ID of the Revision to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return self.do_handle_results(_error_code, _msg, None)

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the RAMSTK Program database table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return self.do_handle_results(_error_code, _msg, None)

    def request_get_attributes(self, node_id):
        """
        Request attributes from the record associated with the Node ID.

        :param int node_id: the ID of the record in the RAMSTK Program
                            database whose attributes are being
                            requested.
        :return: _attributes
        :rtype: dict
        """
        _entity = self.request_do_select(node_id)

        return _entity.get_attributes()

    def request_set_attributes(self, module_id, key, value):
        """
        Request to set a RAMSTK record's attribute.

        :param int module_id: the ID of the entity who's attribute is to
                              be set.
        :param str key: the key of the attributes to set.
        :param value: the value to set the attribute identified by the
                      key.
        :return:
        :rtype:
        """
        _entity = self.request_do_select(module_id)
        _attributes = _entity.get_attributes()

        _attributes[key] = value

        return _entity.set_attributes(_attributes)

    def request_last_id(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request the last entity ID used in the RAMSTK Program database.

        :return: the last entity ID used.
        :rtype: int
        """
        return self._dtm_data_model.last_id

    def request_tree(self):
        """
        Request the Treelib tree from the Data Model.

        :return: tree; the Treelib Tree() object containing the module's data.
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.tree
