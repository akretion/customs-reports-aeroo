# -*- encoding: utf-8 -*-
#################################################################################
#
#    report_proforma_invoice module for OpenERP
#    Copyright (C) 2012-2013 Akretion (http://www.akretion.com)
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
#################################################################################


{
    'name': 'Aeroo Report Proforma Invoice',
    'summary': 'Adds a Proforma Invoice for Customs on Delivery Orders',
    'version': '1.0',
    'category': 'Customs',
    'license': 'AGPL-3',
    'description': """Adds a Proforma Invoice report on Delivery orders. This report is designed to be printed and placed on the package ; the Customs administration will use this invoice to compute the import taxes when the package arrives in the destination country.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': [
        'l10n_fr_intrastat_product', # we will need to have a generic module "intrastat_product" one day...
        'sale',  # we display some fields that are declared in "sale"
        'report_aeroo',
        ],
    'data': ['report.xml'],
    'installable': True,
    'active': False,
}

