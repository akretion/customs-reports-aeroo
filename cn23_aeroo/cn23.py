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
            'factored_stock_pack_operations':
            self._get_factored_stock_pack_operations,
            'currency_name': self._get_currency_name,
        })

    def _get_currency_name(self, picking, context=None):
        if picking.sale_id:
            currency_name = picking.sale_id.currency_id.name
        else:
            currency_name = picking.company_id.currency_id.name
        return currency_name

    def _get_factored_stock_pack_operations(self, picking, context=None):
        precision = self.pool['decimal.precision'].precision_get(
            self.cr, self.uid, 'Account')

        currency_name = self._get_currency_name(picking, context=context)

        # First, group by package
        pack_ops_by_package = {}
        # key = pack_obj
        # value = [line_op_obj1, line_op_obj2, ...]
        for line in picking.pack_operation_ids:
            if not line.result_package_id:
                raise orm.except_orm(
                    _('Error:'),
                    _("The pack operation line with product '%s' is not in "
                        "a package.")
                    % line.product_id.name)
            if line.result_package_id in pack_ops_by_package:
                pack_ops_by_package[line.result_package_id].append(line)
            else:
                pack_ops_by_package[line.result_package_id] = [line]

        # Build the factorised list of stock move
        factorized_pack_ops_by_package = {}
        # key = package
        # value = {} with key = special key ; value = {'amount': 6.76,
        # 'qty': 5, 'weight_net': 89.8, 'product': product_obj}
        for pack, lines in pack_ops_by_package.iteritems():
            factorized_pack_ops_by_package[pack] = {}
            for line in lines:
                if (
                        line.linked_move_operation_ids
                        and line.linked_move_operation_ids[0].move_id
                        and line.linked_move_operation_ids[0].move_id
                            .procurement_id
                        and line.linked_move_operation_ids[0].move_id
                            .procurement_id.sale_line_id):
                    sale_line_id = line.linked_move_operation_ids[0].move_id.\
                        procurement_id.sale_line_id
                    discounted_unit_price = round(
                        sale_line_id.price_unit *
                        (1 - (sale_line_id.discount or 0.0) / 100.0),
                        precision)
                    assert currency_name == \
                        sale_line_id.order_id.currency_id.name,\
                        'Wrong currency'
                else:
                    discounted_unit_price = line.product_id.lst_price

                key = (
                    unicode(line.product_id.id) + ";" +
                    unicode(line.product_uom_id.id))

                if key in factorized_pack_ops_by_package[pack]:
                    factorized_pack_ops_by_package[pack][key]['qty']\
                        += line.product_qty
                    factorized_pack_ops_by_package[pack][key]['amount']\
                        += line.product_qty * discounted_unit_price
                    factorized_pack_ops_by_package[pack][key]['weight_net']\
                        += line.product_qty * line.product_id.weight_net
                else:
                    factorized_pack_ops_by_package[pack][key] = {
                        'qty': line.product_qty,
                        'product': line.product_id,
                        'amount': line.product_qty * discounted_unit_price,
                        'weight_net':
                        line.product_qty * line.product_id.weight_net,
                    }

        # Return a dict of factorised stock op
        # key = package_obj
        # value = {'total_amount': 80.88, 'total_weight_net': 7.8,
        # 'lines': [{'product_obj': product, 'qty': 5.0, 'price_unit': ...,
        # 'currency_name': 'EUR', price_subtotal': 205.56}, {second_line}...]}
        result = {}
        for pack, special_dict in factorized_pack_ops_by_package.iteritems():
            result[pack] = {
                'total_amount': 0.0,
                'total_weight_net': 0.0,
                'lines': []}
            for special_key, special_values in special_dict.iteritems():
                result[pack]['total_amount'] += special_values['amount']
                result[pack]['total_weight_net']\
                    += special_values['weight_net']
                result[pack]['lines'].append(special_values)
        return result
