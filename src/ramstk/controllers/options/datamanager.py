# -*- coding: utf-8 -*-
#
#       ramstk.controllers.options.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.commondb import RAMSTKSiteInfo


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Options data manager.

    This class manages the admin-configurable options and data from the
    Site database.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = 'options'
    _root = 0

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._pkey: Dict[str, List[str]] = {
            'siteinfo': ['site_id'],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._site_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_option_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_option_attributes')

        pub.subscribe(self.do_get_tree, 'request_get_options_tree')
        pub.subscribe(self.do_update, 'request_update_option')

    def do_get_tree(self) -> None:
        """Retrieve the Options treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_options_tree', tree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Options data from the RAMSTK Program database.

        :param attributes: the RAMSTK option attributes for the
            selected Site.
        :return: None
        :rtype: None
        """
        self._site_id = attributes['site_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        # noinspection PyUnresolvedReferences
        for _option in self.dao.do_select_all(RAMSTKSiteInfo,
                                              key=['site_id'],
                                              value=[self._site_id],
                                              order=RAMSTKSiteInfo.site_id):

            self.tree.create_node(tag='siteinfo',
                                  identifier=_option.site_id,
                                  parent=self._root,
                                  data={'siteinfo': _option})

        pub.sendMessage(
            'succeed_retrieve_options',
            tree=self.tree,
        )

    def do_update(self, node_id: str) -> None:
        """Update the record associated with node ID in RAMSTK databases.

        :param node_id: the node ID of the Options item to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['siteinfo'])

            pub.sendMessage(
                'succeed_update_options',
                node_id=node_id,
            )
        except AttributeError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = (
                '{1}: Attempted to save non-existent Site ID {0}.').format(
                    str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_options',
                error_message=_error_msg,
            )
        except KeyError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: No data package found for Site {0} '
                          'options.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_options',
                error_message=_error_msg,
            )
        except (TypeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: The value for one or more attributes for '
                          'Site {0} options was the wrong type.').format(
                              str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_options',
                error_message=_error_msg,
            )
