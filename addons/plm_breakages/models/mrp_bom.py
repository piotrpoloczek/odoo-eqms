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
# Leonardo Cazziolati
# leonardo.cazziolati@omniasolutions.eu
# 23-06-2020

from odoo import _, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    breakages_count = fields.Integer(
        "# Breakages", compute="_compute_breakages_count", compute_sudo=False
    )

    def open_breakages(self):
        product_id = self.product_id
        product_ids = self.get_bom_product_breakeges()
        return {
            "name": _("Products"),
            "res_model": "plm.breakages",
            "view_type": "form",
            "view_mode": "list,form,pivot",
            "type": "ir.actions.act_window",
            "domain": [("product_id", "in", product_ids)],
            "context": {"default_parent_id": product_id.id},
        }

    def get_bom_product_breakeges(self):
        out = []
        for mrp_bom in self:
            product_id = mrp_bom.product_id
            out.append(product_id.id)
            out.extend(mrp_bom.bom_line_ids.mapped("product_id").ids)
        return out

    def _compute_breakages_count(self):
        for mrp_bom in self:
            product_ids = self.get_bom_product_breakeges()
            mrp_bom.breakages_count = self.env["plm.breakages"].search_count(
                [("product_id", "in", product_ids)]
            )
