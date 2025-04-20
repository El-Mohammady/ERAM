# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('technical_review', 'Technical Review'),
        ('revision', 'Revision'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    # state = fields.Selection(selection_add=[('technical_review', 'Technical Review'), ('revision', 'Revision'), ])

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'revision']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def action_revision(self):
      for rec in self:
        rec.state = 'revision'

    def action_technical_review(self):
      for rec in self:
        rec.state = 'technical_review'

    # hide create and edit from tree & form & kanban for specific group
    def _get_view(self, view_id=None, view_type='form', **options):
      arch, view = super()._get_view(view_id, view_type, **options)
      if view_type in ('tree', 'form', 'kanban'):
        nodes = arch.xpath("//tree")
        nodes_form = arch.xpath("//form")
        nodes_kanban = arch.xpath("//kanban")
        for node in nodes:
          if self.env.user.has_group('iet_customs.prevent_create_purchase_order'):
            node.set('create', '0')
            node.set('edit', '0')
            # node.set('import', '0')
        for n in nodes_form:
          if self.env.user.has_group('iet_customs.prevent_create_purchase_order'):
            n.set('create', '0')
            n.set('edit', '0')
            # n.set('import', '0')
        for k in nodes_kanban:
          if self.env.user.has_group('iet_customs.prevent_create_purchase_order'):
            k.set('create', '0')
            k.set('edit', '0')
            # k.set('import', '0')
      return arch, view


    # @api.model
    # def create(self, vals):
    #   if self.env.user.has_group('iet_customs.prevent_create_purchase_order'):
    #     raise ValidationError(_('You can`t create This record.'))
    #   return super(PurchaseOrder, self).write(vals)

    # def write(self, vals):
    #   if self.env.user.has_group('iet_customs.prevent_create_purchase_order'):
    #     raise ValidationError(_('You can`t create This.'))
    #   return super(PurchaseOrder, self).write(vals)
