# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.books.modulebook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Module Book Module."""

# Standard Library Imports
from typing import Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.function import FunctionModuleView
from ramstk.views.gtk3.hardware import HardwareModuleView
from ramstk.views.gtk3.requirement import RequirementModuleView
from ramstk.views.gtk3.revision import RevisionModuleView
from ramstk.views.gtk3.validation import ValidationModuleView
from ramstk.views.gtk3.widgets import RAMSTKBaseBook


class RAMSTKModuleBook(RAMSTKBaseBook):
    """Display Module Views for the RAMSTK modules.

    Attributes of the Module Book are:

    :ivar dict _dic_module_views: dictionary containing the Module View to
        load into the RAMSTK Module Book for each RAMSTK module.  Key is the
        RAMSTK module name; value is the View associated with that RAMSTK
        module.
    """

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize an instance of the Module Book class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        RAMSTKBaseBook.__init__(self, configuration)

        # Initialize private dictionary attributes.
        self._dic_module_views: Dict[str, object] = {
            "revision": RevisionModuleView(configuration, logger),
            "function": FunctionModuleView(configuration, logger),
            "requirement": RequirementModuleView(configuration, logger),
            "hardware": HardwareModuleView(configuration, logger),
            "validation": ValidationModuleView(configuration, logger),
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.icoStatus: Gtk.StatusIcon = Gtk.StatusIcon()

        self._set_properties("modulebook")
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._on_open,
            "succeed_retrieve_all_revision",
        )
        pub.subscribe(
            self._on_close,
            "succeed_closed_program",
        )

    def _on_close(self) -> None:
        """Update the Module View when a RAMSTK Program database is closed.

        :return: None
        :rtype: None
        """
        # Remove all the non-Revision pages.
        _n_pages = self.get_n_pages()
        # pylint: disable=unused-variable
        for __ in range(_n_pages - 1):
            self.remove_page(-1)

        # Clear the Revision page treeview.
        _model = self._dic_module_views["revision"].treeview.get_model()  # type: ignore
        _model.clear()

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_open(self, tree: Tree) -> None:
        """Insert a page in the module book for each active work stream module.

        :param tree: the work stream module's treelib Tree() containing all
            the data for the work stream module.  Unused in this method,
            but is required as an argument since it is the data package for
            the 'succeed_retrieve_all_revision' message.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        for _key in list(self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER)[1:]:
            _mkey = self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER[_key]
            try:
                _module = self._dic_module_views[_mkey]
                self.insert_page(
                    _module,
                    tab_label=_module.hbx_tab_label,  # type: ignore
                    position=_key,
                )
            except KeyError:
                pass

        pub.sendMessage("mvwSwitchedPage", module="revision")

    def _on_switch_page(
        self, __notebook: Gtk.Notebook, __page: Gtk.Widget, page_num: int
    ) -> None:
        """Handle page changes in the Module Book Gtk.Notebook().

        :param __notebook: the Tree Book notebook widget.
        :type __notebook: :class:`Gtk.Notebook`
        :param __page: the newly selected page's child widget.
        :type __page: :class:`Gtk.Widget`
        :param page_num: the newly selected page number.
            0 = Revision Tree
            1 = Function Tree
            2 = Requirements Tree
            3 = Hardware Tree
            4 = Software Tree (future)
            5 = Testing Tree (future)
            6 = Validation Tree
            7 = Incident Tree (future)
            8 = Survival Analyses Tree (future)

        :return: None
        :rtype: None
        """
        try:
            _module = self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER[page_num]
        except KeyError:
            _module = "revision"
            pub.sendMessage(
                "do_log_debug_msg",
                logger_name="DEBUG",
                message=_(
                    f"Page number {page_num} is not active in this Program.  "
                    f"Active page numbers and their associated work flow "
                    f"module are {self.RAMSTK_USER_CONFIGURATION.RAMSTK_PAGE_NUMBER}.  "
                    f"Selecting the Revision work flow module by default."
                ),
            )

        pub.sendMessage("mvwSwitchedPage", module=_module)

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        self.insert_page(
            self._dic_module_views["revision"],
            tab_label=self._dic_module_views["revision"].hbx_tab_label,  # type: ignore
            position=0,
        )

        self.show_all()
        self.set_current_page(0)

    def __set_callbacks(self) -> None:
        """Set callback methods for the RAMSTKModuleBook and widgets.

        :return: None
        :rtype: None
        """
        self.dic_handler_id["select-page"] = self.connect(
            "select-page", self._on_switch_page
        )
        self.dic_handler_id["switch-page"] = self.connect(
            "switch-page", self._on_switch_page
        )
