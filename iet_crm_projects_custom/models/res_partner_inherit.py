# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_
from odoo.osv import expression

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    similar_project_ids = fields.One2many('crm.projects',"sold_to_id")

    _sql_constraints = [
        ('phone_uniq', 'unique(phone)', 'The phone of Customer must be unique !'),
        ('mobile_uniq', 'unique(mobile)', 'The mobile of Customer must be unique '),
    ]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not name:
            return super().name_search(name, args, operator, limit)


        positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
        is_positive = operator not in expression.NEGATIVE_TERM_OPERATORS
        domain = args or []
        partners = self.browse()

        if operator in positive_operators:
            partners = self.search_fetch(expression.AND([
                domain,
                [('phone', '=', name)]
            ]), ['display_name'], limit=limit) or self.search_fetch(expression.AND([
                domain,
                [('mobile', '=', name)]
            ]), ['display_name'], limit=limit)

        if not partners:
            if is_positive:
                partners = self.search_fetch(expression.AND([
                    domain,
                    [('phone', operator, name)]
                ]), ['display_name'], limit=limit)

                limit_rest = limit - len(partners) if limit else None

                if limit_rest is None or limit_rest > 0:
                    extra_domain = [
                        ('id', 'not in', partners.ids),
                        '|',
                        ('mobile', operator, name),
                        ('name', operator, name),
                    ]
                    partners |= self.search_fetch(expression.AND([
                        domain,
                        extra_domain
                    ]), ['display_name'], limit=limit_rest)
            else:
                domain_neg = [
                    '|',
                    ('name', operator, name),
                    '|',
                    ('phone', operator, name),
                    ('mobile', operator, name)
                ]
                partners = self.search_fetch(expression.AND([
                    domain,
                    domain_neg
                ]), ['display_name'], limit=limit)

        return [(partner.id, partner.display_name) for partner in partners.sudo()]
