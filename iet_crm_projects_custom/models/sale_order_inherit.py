# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        sale = super().action_confirm()
        for rec in self:
            for line in rec.order_line.filtered(lambda l: l.product_template_id.property_number_id):
                property_record = line.product_template_id.property_number_id
                if property_record.product_template_id and property_record.state == "sold":
                    raise ValidationError(_(f"Cannot confirm Sale Order for a Sold property {line.product_template_id.name}."))
                if property_record.reserved_to_id and property_record.reserved_to_id.id != rec.partner_id.id:
                    raise ValidationError(_(f"This property Reserved to another Customer {property_record.reserved_to_id.name}."))
                property_record.write({
                    "product_template_id": line.product_template_id.id,
                    "sale_order_id": rec.id,
                    "sold_to_id": rec.partner_id.id,
                    "state": "sold",
                })
        return sale

    def action_cancel(self):
        sale=super(SaleOrderInherit, self).action_cancel()
        for rec in self:
            for line in rec.order_line.filtered(lambda l: l.product_template_id.property_number_id):
                property_record = line.product_template_id.property_number_id
                if property_record.product_template_id and property_record.state == "sold":
                    property_record.write({
                        "product_template_id": False,
                        "sale_order_id": False,
                        "sold_to_id": False,
                        "state": "ready",
                    })
        return sale

