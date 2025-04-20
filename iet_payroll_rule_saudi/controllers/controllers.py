# -*- coding: utf-8 -*-
# from odoo import http


# class IetPayrollRuleSaudi(http.Controller):
#     @http.route('/iet_payroll_rule_saudi/iet_payroll_rule_saudi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_payroll_rule_saudi/iet_payroll_rule_saudi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_payroll_rule_saudi.listing', {
#             'root': '/iet_payroll_rule_saudi/iet_payroll_rule_saudi',
#             'objects': http.request.env['iet_payroll_rule_saudi.iet_payroll_rule_saudi'].search([]),
#         })

#     @http.route('/iet_payroll_rule_saudi/iet_payroll_rule_saudi/objects/<model("iet_payroll_rule_saudi.iet_payroll_rule_saudi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_payroll_rule_saudi.object', {
#             'object': obj
#         })
