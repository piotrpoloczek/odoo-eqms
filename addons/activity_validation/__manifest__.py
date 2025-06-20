# -*- encoding: utf-8 -*-
# ##############################################################################
#
#    OmniaSolutions, Open Source Management Solution
#    Copyright (C) 2010-2019 OmniaSolutions (<https://www.omniasolutions.website>).
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
    "name": "Activity Validation",
    "version": "18.0.1.0.4",
    "author": "OmniaSolutions",
    "website": "https://github.com/OmniaGit/odooplm",
    "category": "Custom",
    "sequence": 1,
    "summary": "",
    "depends": [
        "mail",
        "plm",
    ],
    "license": "AGPL-3",
    "data": [
        "security/security.xml",
        "data/mail_activity_data.xml",
        "views/mail_activity_type.xml",
        "views/mail_activity.xml",
        "views/mail_activity_children_rel.xml",
        "report/bom_activity_product_product.xml",
        "report/bom_activity_product_template.xml",
    ],
    "qweb": ["static/src/xml/*.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
