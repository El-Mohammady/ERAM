# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import format_date



class CustomHREmployeeInheritCustom(models.Model):
  _inherit = 'hr.employee'

  custom_employee_pin_number = fields.Char(string="Employee Number", readonly=False)


  @api.onchange('pin', 'identification_id', 'custom_employee_pin_number')
  def _onchange_pin_or_identification_id_custom_employee_pin_number(self):
    # print('allonchange_weight')
    if self.pin:
      all_pins = self.env['hr.employee'].search([('pin', '=', self.pin), ('id', '!=', self._origin.id)])
      # print('all_pins', all_pins)
      if all_pins:
        raise ValidationError(_("You can't create this employee ,Please change the pin code"))
    if self.identification_id:
      all_identification = self.env['hr.employee'].search([('identification_id', '=', self.identification_id),
                                                           ('id', '!=', self._origin.id)])
      # print('all_identification', all_identification)
      if all_identification:
        raise ValidationError(_("You can't create this employee ,Please change the identification number"))
    if self.custom_employee_pin_number:
      all_custom_employee_pin_number = self.env['hr.employee'].search([('custom_employee_pin_number', '=', self.custom_employee_pin_number),
                                                 ('id', '!=', self._origin.id)])
      if all_custom_employee_pin_number:
        raise ValidationError(_("You can't create this employee ,Please change the Employee Number"))

  def write(self,vals):
      super(CustomHREmployeeInheritCustom, self).write(vals)
      self._onchange_pin_or_identification_id_custom_employee_pin_number()
      return True
