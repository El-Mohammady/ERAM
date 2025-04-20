from odoo import api, fields, models, _
from datetime import datetime, date, timedelta, time
from odoo.exceptions import ValidationError
import warnings
from odoo.exceptions import ValidationError


class ReturnFromVacation(models.Model):
    _name = 'return.vacation'
    _description = "Return Vacation"
    _rec_name = 'employee_id'

    def action_submit(self):
        for rec in self:
            rec.state = 'submit'

    def action_manager_approve(self):
        for rec in self:
            # for emp in rec.employee_id:
            rec.employee_id.warning_employee = ''
            rec.employee_id.warning_text = ''
            rec.state = 'approved'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    employee_ids = fields.Many2many('hr.employee', string='Employees')
    department_id = fields.Many2one('hr.department', string="Department",)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    leave_id = fields.Many2one('hr.leave', string="Time Off",)
    description = fields.Text(string="Description", )
    return_date = fields.Date(string="Return Date")

    time_off_types = fields.Selection([
        ('annual_vacation', 'Annual Vacation'),
        ('paid_time_off', 'Paid time off'),
        ('sick_time_off', 'Sick time off'),
        ('compensatory_days', 'Compensatory Days'),
        ('unpaid', 'Unpaid'),
    ], string='Time Off Types',)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approved', 'APPROVED'),
        ('cancel', 'Canceled'),
    ], string='Status', readonly=True, default='draft')


    def unlink(self):
        print('unlink')
        for rec in self:
            if rec.state == 'approved':
                # print('unliqqqnk' * 2)
                raise ValidationError(_('You can`t delete this record in this state'))
        return super(ReturnFromVacation, self).unlink()
