# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_

class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    client_interests_ids = fields.Many2many(
        comodel_name='client.interests',
        string='Client Interests')
    special_interests_ids = fields.Many2many(
        comodel_name='special.interests',
        string='Special Interests')
    real_state_interests_ids = fields.Many2many(
        comodel_name='real.state.interests',
        string='Real State Interests')
    preferred_means_communication_ids = fields.Many2many(
        comodel_name='preferred.means.communication',
        string='Preferred Means of Communication')
    preferred_times_communication = fields.Char( string='Preferred Times of Communication')
    purpose_purchase_ids = fields.Many2many(
        comodel_name='purpose.purchase',
        string='Purpose Of Purchase')
    property_number_id = fields.Many2one('crm.projects')
    project_id = fields.Many2one("project.name",related="property_number_id.project_id")
    number_of_rooms = fields.Integer(
        string='Number of rooms',
        related="property_number_id.number_of_rooms",
        required=False)
    area = fields.Float(
        string='Built Up Area',
        related="property_number_id.area",
        required=False)
    private_space = fields.Float(string='Private Space',related="property_number_id.private_space",required=False)
    total_area = fields.Float(string='Total Area',related="property_number_id.total_area",required=False)
    bathroom = fields.Float(string='Bathroom',related="property_number_id.bathroom",required=False)
    maid_room = fields.Boolean(string="Nanny's Room",related="property_number_id.maid_room",required=False)
    maid_bathroom = fields.Float(string="Nanny's Bathroom",related="property_number_id.maid_bathroom",required=False)
    driver_room = fields.Boolean(string="Driver's Room",related="property_number_id.driver_room",required=False)
    driver_bathroom = fields.Float(string="Driver's Bathroom",related="property_number_id.driver_bathroom",required=False)
    nanny = fields.Float(string="Nanny",related="property_number_id.nanny",required=False)
    unit_description=fields.Text(related="property_number_id.unit_description",)
    log_file_ids = fields.One2many(
        comodel_name='log.file',
        inverse_name='crm_lead_id',
        string='Log file',
        required=False)
    similar_project_ids = fields.Many2many('crm.projects', 'crm_lead_projects_rel',
                                           'crm_lead_id', 'crm_project_id',related="property_number_id.similar_project_ids")
