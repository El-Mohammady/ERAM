# -*- coding: utf-8 -*-
# from odoo import http


# class IetPayrollAnalyticEmployee(http.Controller):
#     @http.route('/iet_payroll_analytic_employee/iet_payroll_analytic_employee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_payroll_analytic_employee/iet_payroll_analytic_employee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_payroll_analytic_employee.listing', {
#             'root': '/iet_payroll_analytic_employee/iet_payroll_analytic_employee',
#             'objects': http.request.env['iet_payroll_analytic_employee.iet_payroll_analytic_employee'].search([]),
#         })

#     @http.route('/iet_payroll_analytic_employee/iet_payroll_analytic_employee/objects/<model("iet_payroll_analytic_employee.iet_payroll_analytic_employee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_payroll_analytic_employee.object', {
#             'object': obj
#         })
