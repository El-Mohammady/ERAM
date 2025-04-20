# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_number_id = fields.Many2one('crm.projects')
    project_name_id = fields.Many2one("project.name",related="property_number_id.project_id")
    number_of_rooms = fields.Integer(
        string='Number of rooms',
        related="property_number_id.number_of_rooms",
        required=False)
    area = fields.Float(
        string='Built Up Area',
        related="property_number_id.area",
        required=False)
    private_space = fields.Float(string='Private Space',related="property_number_id.private_space",required=False)
    total_area = fields.Float(string='Total Area',related="property_number_id.total_area")
    bathroom = fields.Float(string='Bathroom',related="property_number_id.bathroom",required=False)
    maid_room = fields.Boolean(string="Nanny's Room",related="property_number_id.maid_room",required=False)
    maid_bathroom = fields.Float(string="Nanny's Bathroom",related="property_number_id.maid_bathroom",required=False)
    driver_room = fields.Boolean(string="Driver's Room",related="property_number_id.driver_room",required=False)
    driver_bathroom = fields.Float(string="Driver's Bathroom",related="property_number_id.driver_bathroom",required=False)
    nanny = fields.Float(string="Nanny",related="property_number_id.nanny",required=False)
    unit_description=fields.Text(related="property_number_id.unit_description",)