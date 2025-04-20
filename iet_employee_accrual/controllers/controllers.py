# -*- coding: utf-8 -*-
# from odoo import http


# class IetEmployeeAccrual(http.Controller):
#     @http.route('/iet_employee_accrual/iet_employee_accrual', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_employee_accrual/iet_employee_accrual/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_employee_accrual.listing', {
#             'root': '/iet_employee_accrual/iet_employee_accrual',
#             'objects': http.request.env['iet_employee_accrual.iet_employee_accrual'].search([]),
#         })

#     @http.route('/iet_employee_accrual/iet_employee_accrual/objects/<model("iet_employee_accrual.iet_employee_accrual"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_employee_accrual.object', {
#             'object': obj
#         })
