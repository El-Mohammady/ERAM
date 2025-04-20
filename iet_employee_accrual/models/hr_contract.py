from odoo import models,fields,api
from dateutil.relativedelta import relativedelta


class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    food_allowance = fields.Monetary()
    phone_allowance = fields.Monetary()
    month_counts = fields.Integer()

    @api.onchange("month_counts", "date_start")
    def get_end_date(self):
        for contract in self:
            if contract.date_start:
                contract.date_end = contract.date_start + relativedelta(months=contract.month_counts)

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
