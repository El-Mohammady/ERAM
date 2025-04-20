# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Followers(models.Model):
    _name = 'followers'
    _description = 'Followers'

    followers_id = fields.Many2one(comodel_name="hr.employee")
    name = fields.Char(string="Name", required=True)
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'), ], required=True)
    birthday = fields.Date(string="Birthday")
    identification_id = fields.Char(string="Identification No")


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    end_date_identification = fields.Date(string="identification End Date")
    end_date_passport = fields.Date(string="Passport End Date")
    attachment_identification = fields.Binary(string="Identification Attachment", attachment=True)
    attachment_passport = fields.Binary(string="Passport Attachment", attachment=True)
    is_identification = fields.Boolean()
    is_passport = fields.Boolean()
    followers_ids = fields.One2many(comodel_name="followers", inverse_name="followers_id")
    residency_date = fields.Date(string="Residency Date",)
    residency = fields.Char(string="Residency", )
    insurance_num = fields.Char(string="GOSI Number")
    insurance_date = fields.Date(string="GOSI Date")
    border_num = fields.Char(string="Border Number")
    date_of_entry = fields.Date(string="Date of entry")

    # @api.onchange('identification_id', 'passport_id')
    # def onchange_identification_passport(self):
    #     for rec in self:
    #         rec.is_identification = True if rec.identification_id else False
    #         rec.is_passport = True if rec.passport_id else False

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(HrEmployeeInherit, self).create(vals_list)
    #     if res.id > 0:
    #         module_metadata = {
    #             'employee_id': res.id,
    #         }
    #         self.env['employee.analytic.report'].create(module_metadata)
    #     return res
