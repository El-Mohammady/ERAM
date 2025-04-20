from odoo import api, fields, models


class TicketReasonType(models.Model):
    _name = 'ticket.reason.type'

    name = fields.Char()
