# -*- coding: utf-8 -*-
# from odoo import http


# class IetPayrollRule(http.Controller):
#     @http.route('/iet_payroll_rule/iet_payroll_rule', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_payroll_rule/iet_payroll_rule/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_payroll_rule.listing', {
#             'root': '/iet_payroll_rule/iet_payroll_rule',
#             'objects': http.request.env['iet_payroll_rule.iet_payroll_rule'].search([]),
#         })

#     @http.route('/iet_payroll_rule/iet_payroll_rule/objects/<model("iet_payroll_rule.iet_payroll_rule"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_payroll_rule.object', {
#             'object': obj
#         })
