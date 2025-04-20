from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = 'account.move'

    journal_id_name = fields.Char(related="journal_id.name", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            journal_id = val.get('journal_id')
            if journal_id:
                miscelleneous_operations = self.env['account.journal'].browse(journal_id).name in ['Miscellaneous Operations']
                if not self.user_has_groups("iet_eram_test.allow_miscelleneous_operations") and miscelleneous_operations:
                    raise UserError(_("You are not allowed to create miscelleneous operations record."))
        
        return super(AccountMove, self).create(vals_list)
    
    def write(self, vals):
        journal_id = vals.get('journal_id')
        if journal_id:
            miscelleneous_operations = self.env['account.journal'].browse(journal_id).name in ['Miscellaneous Operations']
            if not self.user_has_groups("iet_eram_test.allow_miscelleneous_operations") and miscelleneous_operations:
                raise UserError(_("You are not allowed to create miscelleneous operations record."))
            
        return super(AccountMove, self).write(vals)