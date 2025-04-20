from odoo import models,api,fields



class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    employee_id = fields.Many2one(related="employee_analytic_id.employee_id", string="Employee",store=True)
    is_compute = fields.Boolean(default=False)


    @api.model
    def create(self, vals):
        move_line = super(AccountMoveLineInherit, self).create(vals)
        if 'employee_analytic_id' in vals:
            report = self.env['employee.analytic.report'].search([('id','=',vals['employee_analytic_id'])])
            report.check_journal = True
        return move_line

