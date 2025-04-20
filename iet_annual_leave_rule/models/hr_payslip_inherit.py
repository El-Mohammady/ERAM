# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hrEmployeeInherit(models.Model):
    _inherit='hr.payslip'

    # annual_days = fields.Float()
    annual_days = fields.Float(compute='_compute_annal_days')
    days_of_month = fields.Float(compute='_compute_annal_days')


    @api.depends('annual_days','date_from','date_to')
    def _compute_annal_days(self):
        for rec in self:
            days_of_month = (rec.date_to - rec.date_from).days
            if days_of_month == 28:
                rec.days_of_month = 28
            else:
                rec.days_of_month = 30
            all_leave = self.env['hr.leave'].search([('employee_id','=',self.employee_id.id),('request_date_from','>=',self.date_from),('request_date_to','<=',self.date_to)])
            if all_leave:
                if all_leave.holiday_status_id.name == 'annual leave':
                    rec.annual_days = all_leave.number_of_days_display
                else:
                    rec.annual_days ==0.00
            else:
                rec.annual_days = 0.00


