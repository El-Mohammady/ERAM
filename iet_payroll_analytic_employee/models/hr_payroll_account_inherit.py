from odoo import fields,models



class HrSalaryRuleInherit(models.Model):
    _inherit = 'hr.salary.rule'


    employee_analytic = fields.Boolean(string='Employee Analytic')