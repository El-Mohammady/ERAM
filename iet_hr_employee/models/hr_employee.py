# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    national_add = fields.Text(string='National Address')
    zip_id = fields.Integer(string='ZIP')
    national_attach = fields.Image(string='National Attachment')
    bank_ids = fields.One2many(comodel_name='bank.account', inverse_name='bank_id', string='Bank Account')


class BankAccount(models.Model):
    _name = 'bank.account'
    _description = "Bank Account"

    bank_id = fields.Many2one(comodel_name='hr.employee', string='Bank')
    bank = fields.Text(string='Bank')
    account_num = fields.Char(string='Account Number')
    short_code = fields.Text(string='Short Code')
