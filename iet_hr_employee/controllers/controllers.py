# -*- coding: utf-8 -*-
# from odoo import http


# class IetHrEmployee(http.Controller):
#     @http.route('/iet_hr_employee/iet_hr_employee', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_hr_employee/iet_hr_employee/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_hr_employee.listing', {
#             'root': '/iet_hr_employee/iet_hr_employee',
#             'objects': http.request.env['iet_hr_employee.iet_hr_employee'].search([]),
#         })

#     @http.route('/iet_hr_employee/iet_hr_employee/objects/<model("iet_hr_employee.iet_hr_employee"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_hr_employee.object', {
#             'object': obj
#         })
