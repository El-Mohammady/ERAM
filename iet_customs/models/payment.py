# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('technical_review', 'Technical Review'),
            ('revision', 'Revision'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )

    def action_revision(self):
      for rec in self:
        rec.state = 'revision'

    def action_technical_review(self):
      for rec in self:
        rec.state = 'technical_review'

    def action_post(self):
        result = super(AccountPayment, self).action_post()
        self.state = 'posted'
        return result

    def action_draft(self):
        result = super(AccountPayment, self).action_draft()
        self.state = 'draft'
        return result

    # hide create and edit from tree & form & kanban for specific group
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('tree', 'form', 'kanban'):
            nodes = arch.xpath("//tree")
            nodes_form = arch.xpath("//form")
            nodes_kanban = arch.xpath("//kanban")
            for node in nodes:
                if self.env.user.has_group('iet_customs.prevent_create_payment'):
                    node.set('create', '0')
                    node.set('edit', '0')
                    # node.set('import', '0')
            for n in nodes_form:
                if self.env.user.has_group('iet_customs.prevent_create_payment'):
                    n.set('create', '0')
                    n.set('edit', '0')
                    # n.set('import', '0')
            for k in nodes_kanban:
                if self.env.user.has_group('iet_customs.prevent_create_payment'):
                    k.set('create', '0')
                    k.set('edit', '0')
                    # k.set('import', '0')
        return arch, view
