# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection=[
            ('draft', "Quotation"),
            ('sent', "Quotation Sent"),
            ('technical_review', 'Technical Review'),
            ('revision', 'Revision'),
            ('sale', "Sales Order"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ], string="Status", readonly=True, copy=False, index=True, tracking=3, default='draft')

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
          if self.env.user.has_group('iet_customs.prevent_create_sales_order'):
            node.set('create', '0')
            node.set('edit', '0')
            # node.set('import', '0')
        for n in nodes_form:
          if self.env.user.has_group('iet_customs.prevent_create_sales_order'):
            n.set('create', '0')
            n.set('edit', '0')
            # n.set('import', '0')
        for k in nodes_kanban:
          if self.env.user.has_group('iet_customs.prevent_create_sales_order'):
            k.set('create', '0')
            k.set('edit', '0')
            # k.set('import', '0')
      return arch, view



