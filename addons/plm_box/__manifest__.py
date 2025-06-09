# -*- encoding: utf-8 -*-
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
    "name": "Plm Box",
    "version": "18.0.1.0.0",
    "author": "OmniaSolutions",
    "website": "https://odooplm.omniasolutions.website",
    "category": "Productivity/Documents",
    "sequence": 1,
    "summary": "",
    "depends": [
        "base",
        "plm",
        "account",  # to work with plm box entities
        "project",  # to work with plm box entities
        "sale",  # to work with plm box entities
    ],
    "license": "AGPL-3",
    "data": [
        "security/plm_security.xml",
        "data/plm_box_sequence_data.xml",
        "views/non_cad_doc.xml",
        "views/box_object_rel.xml",
        "views/ir_attachment.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
