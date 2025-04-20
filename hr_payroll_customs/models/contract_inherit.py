# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class HRContractInherit(models.Model):
    _inherit = 'hr.contract'

    total_salary = fields.Monetary(string='Total Salary')
    base_currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    country_code = fields.Char(related='company_country_id.code', string='Saudi Company Country Code')
    contract_history_line_ids = fields.One2many('hr.contract.history.line', 'link_id')
    custom_transportation_allowance = fields.Monetary(string='Transportation Allowance')
    food_allowance = fields.Monetary()
    phone_allowance = fields.Monetary()
    month_count = fields.Integer()

    @api.onchange("month_count", "date_start")
    def get_end_date(self):
        for contract in self:
            if contract.date_start:
                contract.date_end = contract.date_start + relativedelta(months=contract.month_count)

    @api.onchange('custom_transportation_allowance', 'l10n_sa_housing_allowance', 'l10n_sa_transportation_allowance',
                  'l10n_sa_other_allowances', 'wage', 'food_allowance', 'phone_allowance')
    def _onchange_salary(self):
        for rec in self:
            rec.total_salary = rec.l10n_sa_housing_allowance + rec.custom_transportation_allowance + \
                               rec.l10n_sa_transportation_allowance + rec.l10n_sa_other_allowances + rec.wage + rec.food_allowance + rec.phone_allowance

    def compute_total_salary(self):
        self._onchange_salary()
        for rec in self:
            line_ids = []
            val = {
                'link_id': rec.id,
                'date': fields.Date.today(),
                'total_salary': rec.total_salary,
            }
            line_ids.append((0, 0, val))
            rec.contract_history_line_ids = line_ids


class HRContractHistoryInherit(models.Model):
    _name = 'hr.contract.history.line'
    _description = "Contract History Line"

    link_id = fields.Many2one('hr.contract')
    date = fields.Date(string='Date')
    total_salary = fields.Float(string='Total Salary')
