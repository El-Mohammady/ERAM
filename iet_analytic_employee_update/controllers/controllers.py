# -*- coding: utf-8 -*-
# from odoo import http


# class IetAnalyticEmployeeUpdate(http.Controller):
#     @http.route('/iet_analytic_employee_update/iet_analytic_employee_update', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_analytic_employee_update/iet_analytic_employee_update/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_analytic_employee_update.listing', {
#             'root': '/iet_analytic_employee_update/iet_analytic_employee_update',
#             'objects': http.request.env['iet_analytic_employee_update.iet_analytic_employee_update'].search([]),
#         })

#     @http.route('/iet_analytic_employee_update/iet_analytic_employee_update/objects/<model("iet_analytic_employee_update.iet_analytic_employee_update"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_analytic_employee_update.object', {
#             'object': obj
#         })
