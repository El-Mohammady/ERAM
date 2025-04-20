# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta, date, datetime

class HRLeaveInheritView(models.Model):
    _inherit = 'hr.leave'

    return_date = fields.Date(string="Return Date")
    date_now = fields.Date(string="Date", default=fields.Date.today())
    amount = fields.Float(string='Amount', )
    last_working_date = fields.Date(string='Last Working Date', )
    return_vacation_ids = fields.Many2many('return.vacation',)
    time_off_types = fields.Selection([
        ('annual_vacation', 'Annual Vacation'),
        ('paid_time_off', 'Paid time off'),
        ('sick_time_off', 'Sick time off'),
        ('compensatory_days', 'Compensatory Days'),
        ('unpaid', 'Unpaid'),
    ], string='Time Off Types',)

    def action_validate(self):
        for rec in self:
            for emp in rec.employee_ids:
                vals = {
                    'employee_id': emp.id,
                    'leave_id': rec.id,
                    'return_date': rec.return_date,
                    'state': 'draft',
                    'time_off_types': rec.time_off_types,
                }
                return_vacation = self.env['return.vacation'].create(vals)
                self.return_vacation_ids = [(4, return_vacation.id)]

        res = super(HRLeaveInheritView, self).action_validate()
        return res

    return_vacation_count = fields.Integer(compute='open_return_vacation_count')

    def open_return_vacation(self):
        return {
            'name': _('Return From Vacation'),
            'domain': [('id', 'in', self.return_vacation_ids.ids)],
            'view_type': 'form',
            'res_model': 'return.vacation',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def open_return_vacation_count(self):
        count = self.env['return.vacation'].search_count([('id', 'in', self.return_vacation_ids.ids)])
        self.return_vacation_count = count

    @api.onchange('request_date_to')
    def _onchange_request_date_to(self):
        print('_onchange_request_date_to')
        for rec in self:
            if rec.request_date_to:
                # print('_onchange_request_date_to', rec.request_date_to)
                end_date = rec.request_date_to + timedelta(days=1)
                # print('end_date', end_date)
                rec.return_date = end_date
            if rec.request_date_from:
                last_date = rec.request_date_from - timedelta(days=1)
                print('last_date', last_date)
                rec.last_working_date = last_date

    number_of_days = fields.Float(
        'Duration (Days)', store=True, readonly=False, compute = '_custom_compute_number_of_days_custom', copy=False, tracking=True,
        help='Number of days of the time off request. Used in the calculation. To manually correct the duration, use this field.')
    # compute = '_compute_number_of_days',

    @api.depends('request_date_from', 'request_date_to')
    def _custom_compute_number_of_days_custom(self):
        for rec in self:
            if rec.request_date_to and rec.request_date_from:
                d1 = datetime.strptime(str(rec.request_date_from), "%Y-%m-%d")
                d2 = datetime.strptime(str(rec.request_date_to), "%Y-%m-%d")
                # print('rec.eeee', abs((d2 - d1).days))
                rec.number_of_days = abs((d2 - d1).days)
            else:
                rec.number_of_days = 0.00


    @api.onchange('number_of_days')
    def _onchange_number_of_days(self):
        for rec in self:
            if rec.number_of_days and rec.request_date_from :
                rec.request_date_to = rec.request_date_from + timedelta(days=rec.number_of_days)
                print('rec.request_date_to', rec.request_date_to)