# -*- encoding: utf-8 -*-
##############################################################################
#
#    Report Proforma Invoice module for OpenERP
#    Copyright (C) 2012-2013 Akretion (http://www.akretion.com)
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

from openerp.osv import orm
from openerp.tools.translate import _
from openerp.report import report_sxw
from hashlib import md5

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'factored_stock_moves': self._get_factored_stock_moves,
            'total': self._get_total,
        })


    def _get_factored_stock_moves(self, picking, context=None):
        '''Compute the qty and amount of a move line in order to display it
        on the factorised lines of the proforma invoice'''
        result = []
        stock_moves = []
        precision = self.pool['decimal.precision'].precision_get(self.cr, self.uid, 'Account')

        if picking.sale_id:
            customs_price_from_product = False
        else:
            customs_price_from_product = True

        # Build the factorised list of stock move
        found_product_refs = {}
        for line in picking.move_lines:
            if not customs_price_from_product:
                currency_name = line.sale_line_id.order_id.pricelist_id.currency_id.name
                discounted_unit_price = round(line.sale_line_id.price_unit * (1 - (line.sale_line_id.discount or 0.0) / 100.0), precision)
                currency_name = line.sale_line_id.order_id.pricelist_id.currency_id.name
            else:
                # in this case, we use the pricelist of the customer
                pricelist = picking.partner_id.property_product_pricelist
                if not pricelist:
                    raise orm.except_orm(_('Error :'), _("Missing Sale Pricelist for Partner '%s'.") %(picking.partner_id.name))
                discounted_unit_price = self.pool['product.pricelist'].price_get(
                    self.cr, self.uid, [pricelist.id], line.product_id.id,
                    line.product_qty or 1.0, picking.partner_id.id,
                    {'uom': line.product_uom.id})[pricelist.id]
                if discounted_unit_price is False:
                    raise orm.except_orm(_('Error :'), _("Cannot find a line in the pricelist '%s' matching the product '%s' and its quantity.") %(pricelist.name, line.product_id.name))
                currency_name = pricelist.currency_id.name

            key = unicode(line.product_id.id) + ";" \
                + unicode(line.product_uom.id) + ";" \
                + unicode(discounted_unit_price) + ";" \
                + unicode(currency_name) + ";" \
                + unicode(line.sale_line_id.name)

            key = md5(key.encode('utf8')).hexdigest()


            if not found_product_refs.has_key(key):
                found_product_refs[key] = {}
                found_product_refs[key]["obj"] = line
                found_product_refs[key]["qty"] = line.product_qty
                found_product_refs[key]["price_unit"] = discounted_unit_price
                found_product_refs[key]["price_subtotal"] = found_product_refs[key]["price_unit"] * found_product_refs[key]["qty"]
                found_product_refs[key]["currency_name"] = currency_name
            else:
                found_product_refs[key]["qty"] += line.product_qty
                found_product_refs[key]["price_subtotal"] += line.product_qty * discounted_unit_price

        # Return a dict of factorised moves
        result = []
        for key in found_product_refs.keys():
            res = {}
            res["obj"] = found_product_refs[key]["obj"]
            if found_product_refs[key]["qty"] == int(found_product_refs[key]["qty"]):
                res["product_qty"] = int(found_product_refs[key]["qty"])
            else:
                res["product_qty"] = found_product_refs[key]["qty"]
            res["price_unit"] = found_product_refs[key]["price_unit"]
            res["price_subtotal"] = found_product_refs[key]["price_subtotal"]
            res["currency_name"] = found_product_refs[key]["currency_name"]
            result.append(res)
        return result

    def _get_total(self, picking, context=None):
        res = {}
        total = 0.0
        currency_name = False
        for line in self._get_factored_stock_moves(picking, context=context):
            if not currency_name:
                currency_name = line["currency_name"]
            elif currency_name != line["currency_name"]:
                raise # This should never happen
            total += line["price_subtotal"]
        res['total'] = total
        res['currency_name'] = currency_name
        return res


