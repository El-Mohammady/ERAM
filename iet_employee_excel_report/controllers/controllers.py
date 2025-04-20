# -*- coding: utf-8 -*-
# from odoo import http


# class IetEmployeeExcelReport(http.Controller):
#     @http.route('/iet_employee_excel_report/iet_employee_excel_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_employee_excel_report/iet_employee_excel_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_employee_excel_report.listing', {
#             'root': '/iet_employee_excel_report/iet_employee_excel_report',
#             'objects': http.request.env['iet_employee_excel_report.iet_employee_excel_report'].search([]),
#         })

#     @http.route('/iet_employee_excel_report/iet_employee_excel_report/objects/<model("iet_employee_excel_report.iet_employee_excel_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_employee_excel_report.object', {
#             'object': obj
#         })
