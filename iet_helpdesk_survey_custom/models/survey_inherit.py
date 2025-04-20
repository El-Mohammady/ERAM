# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SurveyInherit(models.Model):
    _inherit = 'survey.survey'

    helpdesk_team_id = fields.Many2one(comodel_name='helpdesk.team')


class SurveyQuestionInherit(models.Model):
    _inherit = 'survey.question.answer'

    create_ticket = fields.Boolean()


class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    suggested_answer_id= fields.Many2one(comodel_name='survey.question.answer')


