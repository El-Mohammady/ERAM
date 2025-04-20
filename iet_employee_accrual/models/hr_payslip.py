from odoo import fields,models,api


class HrPayslipInheritt(models.Model):
    _inherit = 'hr.payslip'

    @api.depends('number_of_absences_days', 'number_of_penalties_days', 'date_to', 'date_from')
    def _compute_amounts_days(self):
        for rec in self:
            rec.amount_of_absences = 0
            rec.amount_of_penalties = 0
            month_days = (rec.date_to - rec.date_from).days + 1
            print('month_days',month_days)
            if rec.contract_id:
                rec.amount_of_absences = (
                                                 rec.contract_id.total_salary / rec.customs_attendances) * rec.number_of_absences_days
                rec.amount_of_penalties = ((
                                                   rec.contract_id.wage + rec.contract_id.l10n_sa_housing_allowance + rec.contract_id.l10n_sa_transportation_allowance) / 30) * rec.number_of_penalties_days
            else:
                rec.amount_of_absences = 0
                rec.amount_of_penalties = 0
