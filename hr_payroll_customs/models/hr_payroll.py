from odoo import api, fields, models


class HRPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    # accrual_leave = fields.Float(string='Accrual Leave', related='employee_id.accrual_leave')
    accrual_leave = fields.Float(string='Accrual Leave', related='employee_id.custom_accrual0_leave0')
    show_last_payslip = fields.Boolean(string="Show Basic In Annual")

    def action_print_payslip(self):
        return self.env.ref('hr_payroll_customs.payroll_report_action').report_action(self)

    number_of_absences_days = fields.Float()
    amount_of_absences = fields.Float(compute='_compute_amounts_days', )
    number_of_penalties_days = fields.Float()
    amount_of_penalties = fields.Float(compute='_compute_amounts_days', )
    overtime = fields.Float()
    termination_amount = fields.Float()

    customs_attendances = fields.Float(string="Last day of the Month", compute='_compute_custom_attendance')
    amount_of_attendances = fields.Float(string="Amount of Attendances", compute='_compute_amount_of_attendances')

    def compute_sheet(self):
        for slip in self:
            employee = slip.employee_id
            years_count = employee.custom_total0_year0
            total_salary = employee.contract_id.total_salary
            termination_amount = total_salary * years_count * 0.5 if 1 <= years_count <= 5 else total_salary * years_count if years_count > 5 else 0
            resignation_request = self.env['resignation.request'].search(
                [('employee_id', '=', employee.id), ('state', '=', 'confirmed'), ('date', '>=', slip.date_from),
                 ('date', '<=', slip.date_to)], limit=1)
            if resignation_request and resignation_request.hr_departure_id.is_termination:
                resignation_amount = (termination_amount / 3) if 1 <= years_count <= 5 else (
                        2 * termination_amount / 3) if 5 < years_count <= 10 else termination_amount if years_count > 10 else 0

                actual_termination = termination_amount if not resignation_request.hr_departure_id.is_resignation else resignation_amount
                slip.termination_amount = actual_termination
            print("total_salary", total_salary, "termination_amount", termination_amount)
        return super().compute_sheet()

    @api.depends('date_from', 'date_to')
    def _compute_custom_attendance(self):
        for rec in self:
            if rec.date_from and rec.date_to:
                days_total = rec.date_to - rec.date_from
                # print('days_total', days_total.days)
                rec.customs_attendances = 30
            else:
                rec.customs_attendances = 0

    @api.depends('customs_attendances', 'contract_id')
    def _compute_amount_of_attendances(self):
        for rec in self:
            rec.amount_of_attendances = 0
            if rec.customs_attendances and rec.contract_id:
                rec.amount_of_attendances = (rec.contract_id.total_salary / 30) * rec.customs_attendances

    @api.depends('number_of_absences_days', 'number_of_penalties_days', 'date_to', 'date_from')
    def _compute_amounts_days(self):
        for rec in self:
            rec.amount_of_absences = 0
            rec.amount_of_penalties = 0
            month_days = (rec.date_to - rec.date_from).days + 1
            if rec.contract_id:
                rec.amount_of_absences = (
                                                 rec.contract_id.total_salary / month_days) * rec.number_of_absences_days
                rec.amount_of_penalties = ((
                                                   rec.contract_id.wage + rec.contract_id.l10n_sa_housing_allowance + rec.contract_id.l10n_sa_transportation_allowance) / 30) * rec.number_of_penalties_days
            else:
                rec.amount_of_absences = 0
                rec.amount_of_penalties = 0
