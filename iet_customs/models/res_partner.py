# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    # hide create and edit from tree & form & kanban for specific group
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('tree', 'form', 'kanban'):
            nodes = arch.xpath("//tree")
            nodes_form = arch.xpath("//form")
            nodes_kanban = arch.xpath("//kanban")
            for node in nodes:
                if self.env.user.has_group('iet_customs.prevent_create_partner'):
                    node.set('create', '0')
                    node.set('edit', '0')
                    # node.set('import', '0')
            for n in nodes_form:
                if self.env.user.has_group('iet_customs.prevent_create_partner'):
                    n.set('create', '0')
                    n.set('edit', '0')
                    # n.set('import', '0')
            for k in nodes_kanban:
                if self.env.user.has_group('iet_customs.prevent_create_partner'):
                    k.set('create', '0')
                    k.set('edit', '0')
                    # k.set('import', '0')
        return arch, view
