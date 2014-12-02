# -*- encoding: utf-8 -*-
##############################################################################
#
#    CN23 Aeroo
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'CN23 Aeroo',
    'version': '0.1',
    'category': 'Carrier',
    'license': 'AGPL-3',
    'summary': 'CN23 report in Aeroo format',
    'description': """
This module replaces the CN23 report of the module
*delivery_carrier_label_colissimo* by an Aeroo report with output in ODT
format, so that it can be manually modified by the user before printing.

This module has been developped by Alexis de Lattre
<alexis.delattre@akretion.com>
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'report_aeroo',
        'delivery_carrier_label_colissimo',
        'partner_address_street3',
        ],
    'data': ['report.xml'],
    'installable': True,
}
