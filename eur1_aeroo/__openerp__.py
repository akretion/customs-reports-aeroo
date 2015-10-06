# -*- coding: utf-8 -*-
##############################################################################
#
#    report_eur1 module for Odoo
#    Copyright (C) 2012-2015 Akretion (www.akretion.com)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'EUR.1 report',
    'version': '1.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Adds EUR.1 report on stock picking',
    'description': """
This module adds an EUR.1 report on stock picking, that can be directly
printed on the official EUR.1 form.

This module has been written by Alexis de Lattre
from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': [
        'intrastat_product',
        'report_aeroo',
        'sale',  # we display some fields that are declared in "sale"
        ],
    'data': ['report.xml'],
    'installable': True,
}
