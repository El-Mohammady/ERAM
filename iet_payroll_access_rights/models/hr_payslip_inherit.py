from odoo import models, fields, api

class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    can_confirmed = fields.Boolean(compute="_compute_can_confirmed")
    can_approved = fields.Boolean(compute="_compute_can_approved")
    can_paid = fields.Boolean(compute="_compute_can_paid")

    def _compute_can_confirmed(self):
        for record in self:
            record.can_confirmed = self.env.user.has_group('iet_payroll_access_rights.confirm_payslip_group')

    def _compute_can_approved(self):
        for record in self:
            record.can_approved = self.env.user.has_group('iet_payroll_access_rights.approve_payslip_group')

    def _compute_can_paid(self):
        for record in self:
            record.can_paid = self.env.user.has_group('iet_payroll_access_rights.paid_payslip_group')

