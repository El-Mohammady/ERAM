# -*- coding: utf-8 -*-
# from odoo import http


# class IetHrPayrollRule(http.Controller):
#     @http.route('/iet_hr_payroll_rule/iet_hr_payroll_rule', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_hr_payroll_rule/iet_hr_payroll_rule/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_hr_payroll_rule.listing', {
#             'root': '/iet_hr_payroll_rule/iet_hr_payroll_rule',
#             'objects': http.request.env['iet_hr_payroll_rule.iet_hr_payroll_rule'].search([]),
#         })

#     @http.route('/iet_hr_payroll_rule/iet_hr_payroll_rule/objects/<model("iet_hr_payroll_rule.iet_hr_payroll_rule"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_hr_payroll_rule.object', {
#             'object': obj
#         })
