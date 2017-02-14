# -*- coding: utf-8 -*-
# © 2012-2017 Akretion (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import models, api, _
from openerp.exceptions import Warning as UserError
import logging
logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def report_eur1_lines(self):
        self.ensure_one()
        if self.picking_type_code != 'outgoing':
            raise UserError(_(
                "Picking %s is not an outgoing picking, so printing an EUR.1 "
                "doesn't make sense.") % self.name)
        if not self.partner_id:
            raise UserError(_(
                "Missing partner on picking %s.") % self.name)
        if not self.partner_id.country_id:
            raise UserError(_(
                "Country is missing on the delivery address of picking %s.")
                % self.name)
        if self.partner_id.country_id.intrastat:
            raise UserError(_(
                "The delivery address of the picking %s is located in %s "
                "which is an EU country, so it doesn't make sense to print "
                "an EUR.1.") % (self.name, self.partner_id.country_id.name))
        if not self.company_id.country_id:
            raise UserError(_(
                'Missing country on company %s') % self.company_id.name)
        if not self.company_id.country_id.intrastat:
            raise UserError(_(
                "The company '%s' is located in %s which is not an "
                "EU country, so it is not possible to generate an EUR.1.")
                % (self.company_id.name, self.company_id.country_id.name))
        res = {}
        # key = (product, lot, order)
        # value: weight
        weight_uom_categ = self.env.ref('product.product_uom_categ_kgm')
        unit_uom_categ = self.env.ref('product.product_uom_categ_unit')
        kg_uom = self.env.ref('product.product_uom_kgm')
        puo = self.env['product.uom']
        if not self.pack_operation_ids:
            raise UserError(_(
                "There are no packing operations on picking %s. They are "
                "generated when the picking is transfered.") % self.name)
        for pack in self.pack_operation_ids:
            product = pack.product_id
            if not product.origin_country_id:
                raise UserError(_(
                    "Missing country of origin on product '%s'")
                    % product.name_get()[0][1])
            if not product.origin_country_id.intrastat:
                logger.info(
                    'Skipping product %s because his country of origin is %s',
                    product.name_get()[0][1],
                    product.origin_country_id.name)
                continue
            if product.uom_id == kg_uom:
                qty = pack.product_qty
                uom = kg_uom
            elif product.uom_id.category_id == weight_uom_categ:
                qty = puo.compute(product.uom_id, pack.product_qty, kg_uom)
                uom = kg_uom
            elif product.uom_id.category_id == unit_uom_categ:
                qty = pack.product_qty * product.weight
                uom = kg_uom
            else:
                qty = pack.product_qty
                uom = product.uom_id
            if (product, pack.lot_id, uom) in res:
                res[(product, pack.lot_id, uom)] += qty
            else:
                res[(product, pack.lot_id, uom)] = qty
        if not res:
            raise UserError(_(
                "On picking %s, the are no products made in EU.") % self.name)
        fres = []
        i = 0
        for (product, lot, uom), qty in res.iteritems():
            i += 1
            fres.append({
                'product': product,
                'lot': lot,
                'uom': uom,
                'qty': qty,
                'seq': i,
                })
        return fres
