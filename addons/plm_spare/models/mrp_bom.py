# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2010-2021 OmniaSolutions (<https://www.omniasolutions.website>). All Rights Reserved
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

"""
Created on 30 Aug 2016

@author: Daniel Smerghetto
"""
from odoo import fields, models


class MrpBomExtension(models.Model):
    _inherit = "mrp.bom"

    type = fields.Selection(
        selection_add=[("spbom", "Spare BoM")], ondelete={"spbom": "cascade"}
    )


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    is_spare_part = fields.Boolean(related="product_id.is_spare_part")

    def action_mrp_product_spare(self):
        pass
