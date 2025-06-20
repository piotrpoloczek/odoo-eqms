# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2020 OmniaSolutions (<https://omniasolutions.website>). All Rights Reserved
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
# Matteo Boscolo
# matteo.boscolo@omniasolutions.eu
# 19-03-2022

from odoo import _, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    breakages_count = fields.Integer(
        "# Breakages", compute="_compute_breakages_count", compute_sudo=False
    )

    def open_breakages(self):
        product_id = self.product_id

        return {
            "name": _("Products"),
            "res_model": "plm.breakages",
            "view_type": "form",
            "view_mode": "list,form,pivot",
            "type": "ir.actions.act_window",
            "domain": [("product_id", "=", product_id.id)],
            "context": {"default_parent_id": product_id.id},
        }

    def _compute_breakages_count(self):
        for mrp_bom_line in self:
            product_id = mrp_bom_line.product_id
            mrp_bom_line.breakages_count = self.env["plm.breakages"].search_count(
                [("product_id", "=", product_id.id)]
            )
