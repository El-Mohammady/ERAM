# -*- coding: utf-8 -*-
# from odoo import http


# class IetAnnualLeaveRule(http.Controller):
#     @http.route('/iet_annual_leave_rule/iet_annual_leave_rule', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iet_annual_leave_rule/iet_annual_leave_rule/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iet_annual_leave_rule.listing', {
#             'root': '/iet_annual_leave_rule/iet_annual_leave_rule',
#             'objects': http.request.env['iet_annual_leave_rule.iet_annual_leave_rule'].search([]),
#         })

#     @http.route('/iet_annual_leave_rule/iet_annual_leave_rule/objects/<model("iet_annual_leave_rule.iet_annual_leave_rule"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iet_annual_leave_rule.object', {
#             'object': obj
#         })
