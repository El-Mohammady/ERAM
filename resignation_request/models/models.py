# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date


class DepartureReason(models.Model):
    _inherit = "hr.departure.reason"

    is_departure = fields.Boolean(string="Is Departure", )
    is_termination = fields.Boolean()
    is_resignation = fields.Boolean()


class ResignationRequest(models.Model):
    _name = "resignation.request"
    _description = "Resignation Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def get_hr_departure_id(self):
        return self.env['hr.departure.reason'].sudo().search([('is_departure', '=', True)], limit=1)

    state = fields.Selection([("draft", "Draft"), ("confirmed", "Confirmed")], readonly=True, default="draft",
                             tracking=True)
    name = fields.Text(string="Description", tracking=True)
    date = fields.Date("Date", tracking=True, default=fields.date.today())
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", required=True, tracking=True)
    company_id = fields.Many2one(comodel_name='res.company', string="Company", related='employee_id.company_id')
    department_id = fields.Many2one(comodel_name="hr.department", string="Department",
                                    related='employee_id.department_id')
    job_id = fields.Many2one(comodel_name='hr.job', string='Job Position', related='employee_id.job_id')
    parent_id = fields.Many2one(comodel_name='hr.employee', string='Manager', related='employee_id.parent_id')
    hr_departure_id = fields.Many2one(comodel_name="hr.departure.reason", string="Departure Reason",
                                      default=get_hr_departure_id, required=False, )
    contract_date_end = fields.Date(string="Contract Date End", tracking=True, default=fields.date.today())
    departure_reason = fields.Text(string="Departure Reason", tracking=True)
    # departure_wizard_id = fields.Many2one(comodel_name="hr.departure.wizard", string="Departure Wizard", default=get_hr_departure_id,required=False, )

    identification_id_custom = fields.Char(string='Identification No', related='employee_id.identification_id',
                                           tracking=True, readonly=True)
    custom_pin = fields.Char(string="PIN", readonly=True, related='employee_id.custom_employee_pin_number')

    @api.onchange('employee_id')
    def get_name_employee(self):
        for rec in self:
            rec.name = rec.employee_id.name

    def git_confirmed(self):
        for rec in self:
            print('ddddddddddddddddddddddddddd')
            departure_wizard = self.env['hr.departure.wizard'].sudo().create({
                'departure_reason_id': self.hr_departure_id.id,
                'employee_id': self.employee_id.id,
                'departure_date': self.contract_date_end,
                'departure_description': self.departure_reason,
                'archive_private_address': True,
                'archive_allocation': True,
                'cancel_appraisal': True,
                'cancel_leaves': True,
                'set_date_end': True,
            })
            print('departure_wizard', departure_wizard)
            # self.departure_wizard_id = departure_wizard.id
            # self.env.context.get('toggle_active', False) and
            if self.employee_id.active:
                self.employee_id.with_context(no_wizard=True).toggle_active()
            departure_wizard.action_register_departure()
            print('departure_wizard', departure_wizard)
            self.state = "confirmed"
