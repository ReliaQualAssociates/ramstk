# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Validation List View Module."""

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView


class ValidationRequirement(RAMSTKListView):
    """
    Display all the Validation-Requirement matrix for the selected Revision.

    The attributes of the Validation-Requirement Matrix View are:
    """
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'vldtn_rqrmnt') -> None:
        """
        Initialize the List View for the Validation package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param module: the name of the module.
        """
        super().__init__(configuration, logger, module)
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        super().make_ui(vtype='matrix')

        self.tab_label.set_markup("<span weight='bold'>"
                                  + _("Validation-Requirement\nMatrix")
                                  + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays the Validation-Requirement matrix for the selected "
              "revision."))

    def __set_properties(self) -> None:
        """
        Set properties of the Validation::Requirement Matrix View and widgets.

        :return: None
        :rtype: None
        """
        self.matrixview.set_tooltip_text(
            _("Displays the Validation-Requirement matrix for the selected "
              "revision."))
