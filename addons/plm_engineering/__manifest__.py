# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Open Source Management Solution
#    Copyright (C) 2010-2021 OmniaSolutions (<https://www.omniasolutions.website>).
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
{
    "name": "PLM Engineering",
    "version": "18.0.1.0.0",
    "author": "OmniaSolutions",
    "website": "https://odooplm.omniasolutions.website",
    "category": "Manufacturing/Product Lifecycle Management (PLM)",
    "sequence": 15,
    "summary": "Allow to use engineering boms",
    "license": "AGPL-3",
    "depends": ["plm"],
    "data": [
        "views/mrp_bom.xml",
        # 'views/product_product_kanban.xml',
        "views/menu.xml",
        "views/product_product.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
