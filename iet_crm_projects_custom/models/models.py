# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_


class ClientInterests(models.Model):
    _name = 'client.interests'
    _description = 'Client Interests'
    _inherit = ['mail.thread','mail.activity.mixin',]

    name = fields.Text(
        string='Client Interests',
        tracking=True,
        required=True)



class SpecialInterests(models.Model):
    _name = 'special.interests'
    _description = 'Special Interests'
    _inherit = ['mail.thread','mail.activity.mixin',]

    name = fields.Text(
        string='Special Interests',
        tracking=True,
        required=True)


class RealStateInterests(models.Model):
    _name = 'real.state.interests'
    _description = 'Real State Interests'
    _inherit = ['mail.thread','mail.activity.mixin',]

    name = fields.Text(
        string='Real State Interests',
        tracking=True,
        required=True)



class PreferredMeansOfCommunication(models.Model):
    _name = 'preferred.means.communication'
    _description = 'Preferred Means of Communication'
    _inherit = ['mail.thread','mail.activity.mixin',]

    name = fields.Text(
        string='Preferred Means of Communication',
        tracking=True,
        required=True)

class PurposeOfPurchase(models.Model):
    _name = 'purpose.purchase'
    _description = 'Purpose Of Purchase'
    _inherit = ['mail.thread','mail.activity.mixin',]

    name = fields.Text(
        string='Purpose Of Purchase',
        tracking=True,
        required=True)

class LogFile(models.Model):
    _name = 'log.file'
    _description = 'Log File'

    name = fields.Text(
        string='Description',
        tracking=True,
        required=True)
    date = fields.Datetime(
        string='Date',
        required=True)
    crm_lead_id=fields.Many2one('crm.lead')


