# -*- encoding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Open Source Management Solution
#    Copyright (C) 2010-2011 OmniaSolutions (<http://www.omniasolutions.eu>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import _, fields, models


class stock_config_settings(models.TransientModel):
    _inherit = "res.config.settings"

    module_stock_plm_box = fields.Boolean(
        _("Allow plm_box relation"), help=_("Adds plm_box relation to Warehouse.")
    )
    module_plm_box_widget = fields.Boolean(
        _("Plm Widget"), help=_("Adds plm_box relation to Warehouse.")
    )
