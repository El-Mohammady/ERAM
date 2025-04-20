from odoo import api, fields, models


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Employees')
