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

from openerp.report import report_sxw
from openerp.osv import orm
from openerp.tools.translate import _


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'currency_name': self._get_currency_name,
            'product_price': self._get_product_price,
            'total_weight': self._get_total_weight,
        })

    def _get_currency_name(self, picking, context=None):
        if picking.sale_id:
            currency_name = picking.sale_id.currency_id.name
        else:
            currency_name = picking.company_id.currency_id.name
        return currency_name

    def _get_product_price(self, move, context=None):
        precision = self.pool['decimal.precision'].precision_get(
            self.cr, self.uid, 'Account')

        currency_name = self._get_currency_name(move.picking_id, context=context)
        if move.sale_line_id:
            sale_line = move.sale_line_id
            discounted_unit_price = round(
                sale_line.price_unit *
                (1 - (sale_line.discount or 0.0) / 100.0),
                precision)
            assert currency_name == \
                sale_line_id.order_id.currency_id.name,\
                'Wrong currency'
        else:
            discounted_unit_price = move.product_id.list_price
        return discounted_unit_price

    def _get_total_weight(self, picking, context=None):
        total_weight = 0.0
        for line in picking.move_lines:
            line_weight = line.product_qty * line.product_id.weight
            total_weight += line_weight
        return total_weight
