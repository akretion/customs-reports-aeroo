# -*- coding: utf-8 -*-
# © 2012-2017 Akretion (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'EUR.1 aeroo report',
    'version': '8.0.1.0.0',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'summary': 'Adds EUR.1 report on pickings',
    'description': """
EUR.1 Aeroo report
==================

This module adds an EUR.1 report (https://en.wikipedia.org/wiki/EUR.1_movement_certificate) in Aeroo format (ODT output) on pickings. This report is designed to be printed directly on the official EUR.1 paper form.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': [
        'product_harmonized_system',
        'intrastat_base',
        'report_aeroo',
        'stock',
        ],
    'data': ['report.xml'],
    'installable': True,
}
