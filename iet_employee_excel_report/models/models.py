# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class iet_employee_excel_report(models.Model):
#     _name = 'iet_employee_excel_report.iet_employee_excel_report'
#     _description = 'iet_employee_excel_report.iet_employee_excel_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
