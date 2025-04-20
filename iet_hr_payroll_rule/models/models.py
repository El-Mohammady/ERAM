# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class iet_hr_payroll_rule(models.Model):
#     _name = 'iet_hr_payroll_rule.iet_hr_payroll_rule'
#     _description = 'iet_hr_payroll_rule.iet_hr_payroll_rule'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
