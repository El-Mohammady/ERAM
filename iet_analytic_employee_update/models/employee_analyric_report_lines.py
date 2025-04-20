from odoo import models,api,fields



class employeeAnalyticReportLine(models.Model):
    _name = 'employee.analytic.report.line'
    _description = "Employee Analytic Report Line"

    employee_id = fields.Many2one('hr.employee',related='employee_analytic_id.employee_id', string="Employee",store=True)
    employee_custom_analytic_id = fields.Many2one('account.account',string="Employee Analytic")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id", string="Currency", readonly=True)
    debit = fields.Monetary( string='Debit')
    credit = fields.Monetary(string='Credit')
    balance = fields.Monetary(string='Balance')
    employee_analytic_id = fields.Many2one('employee.analytic.report', string="Employee Analytic")
