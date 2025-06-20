# -*- coding: utf-8 -*-
##############################################################################
#
#    OmniaSolutions, Open Source Management Solution
#    Copyright (C) 2010-2021 OmniaSolutions (<http://www.omniasolutions.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, Trueeither version 3 of the License, or
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
# Developed: matteo.boscolo@omniasolutions.eu (2017)
##############################################################################
{
    "name": "PLM Project",
    "version": "18.0.1.0.2",
    "author": "OmniaSolutions",
    "website": "https://odooplm.omniasolutions.website",
    "category": "Manufacturing/Product Lifecycle Management (PLM)",
    "license": "AGPL-3",
    "sequence": 15,
    "summary": "Connect odoo project with odooPLM",
    "depends": ["plm", "project"],
    "data": [
        "views/project.xml",
        "views/product.xml",
        "views/project_task.xml",
        "views/mail_activity_type.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
