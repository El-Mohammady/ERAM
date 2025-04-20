from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    reason_id = fields.Many2one(
        comodel_name='ticket.reason.type',
        string='Reason',
        required=False)
    attachment = fields.Binary(string="Attachment", )
