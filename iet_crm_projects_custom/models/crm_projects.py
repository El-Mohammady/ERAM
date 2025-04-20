# -*- coding: utf-8 -*-

from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError


class ProjectName(models.Model):
    _name = 'project.name'
    _description = 'Projects name'
    _inherit = ['mail.thread','mail.activity.mixin',]
    _order = 'id desc'

    name = fields.Char(required=True)
    is_apartment = fields.Boolean("Apartment",default=False)
    is_villa = fields.Boolean("Villa",default=False)

class CrmProjects(models.Model):
    _name = 'crm.projects'
    _description = 'Crm Projects'
    _inherit = ['mail.thread','mail.activity.mixin',]
    _order = 'create_date desc'
    # _rec_name="project_id"

    name = fields.Char(string='Property Number',required=False)
    project_id = fields.Many2one('project.name',string="Project Name",required=True)
    is_apartment = fields.Boolean(related="project_id.is_apartment")
    is_villa = fields.Boolean(related="project_id.is_villa")
    number_of_rooms = fields.Integer(string='Number of rooms',required=False)
    area = fields.Float(string='Built-up Area',required=False)
    private_space = fields.Float(string='Private Space',required=False)
    total_area = fields.Float(string='Total Area')
    built_up_special_area = fields.Float(string='Built-up Area and Private Space',required=False,compute="_compute_total_area")
    bathroom = fields.Float(string='Bathroom',required=False)
    maid_room = fields.Boolean(string="Nanny's room",required=False)
    maid_bathroom = fields.Float(string="Nanny's Bathroom",required=False)
    driver_room = fields.Boolean(string="Driver's Room",required=False)
    driver_bathroom = fields.Float(string="Driver's Bathroom",required=False)
    nanny = fields.Float(string="Nanny",required=False)
    unit_description=fields.Text()
    reserved_to_id = fields.Many2one(comodel_name='res.partner')
    sold_to_id = fields.Many2one(comodel_name='res.partner',readonly=True)
    sale_order_id = fields.Many2one(comodel_name='sale.order',string='Sale Order Number',readonly=True)
    product_template_id = fields.Many2one(comodel_name='product.template',string="Product",readonly=True)
    similar_project_ids = fields.Many2many('crm.projects','crm_projects_a_rel',
                                   'crm_project_a_group_id', 'crm_project_a_id')
    state = fields.Selection(
        string='State',
        selection=[('ready', 'Ready'),
                   ('reserved', 'Reserved'),
                   ('sold', 'Sold'),
                   ('cancel', 'Cancelled'),],store=True, tracking=True,
        default='ready')

    @api.depends("area","private_space")
    def _compute_total_area(self):
        for rec in self :
            rec.built_up_special_area = rec.area + rec.private_space

    def action_reset_to_ready(self):
        for rec in self:
            rec.state='ready'

    def action_reserved(self):
        for rec in self:
            if not rec.reserved_to_id:
                raise ValidationError(_('Please select a customer for reservation.'))
            rec.state='reserved'

    def action_sold(self):
        for rec in self:
            rec.state='sold'

    def action_cancel(self):
        for rec in self:
            rec.state='cancel'
            rec.sold_to_id=False
            rec.sale_order_id=False
            rec.product_template_id=False


