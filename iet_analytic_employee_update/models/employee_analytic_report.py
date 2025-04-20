from odoo import fields,models,api

class EmployeeAnalyticReportInherit(models.Model):
    _inherit = 'employee.analytic.report'

    employee_account = fields.Many2one('account.account', string="Employee Account")
    move_line_ids = fields.One2many('employee.analytic.report.line', 'employee_analytic_id', string="Move Lines" ,readonlt=False)
    check_journal = fields.Boolean(default=False)

    @api.onchange('check_journal')
    def action_compute_totals(self):
        for rec in self:
            # if rec.employee_account:
            print('Computing totals for account:', rec.employee_account)
            print('employee_analytic_id:', rec.id)

            account_totals = {}

            related_requests = self.env['account.move.line'].search([
                ('move_id.state', '=', 'posted'),
                ('employee_analytic_id', '=', rec.id),
            ])
            print('related_requests', related_requests)

            for record in related_requests:
                account_id = record.account_id.id
                print('account_id', account_id)

                account_totals.setdefault(account_id, {'debit': 0.0, 'credit': 0.0})
                account_totals[account_id]['debit'] += record.debit
                account_totals[account_id]['credit'] += record.credit


            move_line_data = []
            for account_id, totals in account_totals.items():
                if totals['debit'] != 0 or totals['credit'] != 0:
                    existing_line = rec.move_line_ids.filtered(
                        lambda line: line.employee_custom_analytic_id.id == account_id)
                    if not existing_line:
                        move_line_data.append((0, 0, {
                            'employee_custom_analytic_id': account_id,
                            'debit': totals['debit'],
                            'credit': totals['credit'],
                            'balance': totals['credit'] - totals['debit'],
                        }))

            rec.move_line_ids = move_line_data





