# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, time

from odoo import api, fields, models, tools
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.translate import _

class HrLeaveInherit(models.Model):
    _inherit = 'hr.leave'

    net_days = fields.Float(string='Net Days', related='employee_id.net_days')
    identification_id_custom = fields.Char(string='Identification No', tracking=True, readonly=False)
    custom_pin = fields.Char(string="Employee Number", readonly=False)
    custom_to = fields.Char(string="To", readonly=False)
    from_custom = fields.Char(string="From", readonly=False)
    related_leave_id = fields.Many2one(comodel_name="hr.leave", string="Related Leave", required=False, )


    def action_validate(self):
        current_employee = self.env.user.employee_id
        leaves = self._get_leaves_on_public_holiday()
        # if leaves:
        #     raise ValidationError(_('The following employees are not supposed to work during that period:\n %s') % ','.join(leaves.mapped('employee_id.name')))

        if any(holiday.state not in ['confirm', 'validate1'] and holiday.validation_type != 'no_validation' for holiday in self):
            raise UserError(_('Time off request must be confirmed in order to approve it.'))

        self.write({'state': 'validate'})

        leaves_second_approver = self.env['hr.leave']
        leaves_first_approver = self.env['hr.leave']

        for leave in self:
            if leave.validation_type == 'both':
                leaves_second_approver += leave
            else:
                leaves_first_approver += leave

            if leave.holiday_type != 'employee' or\
                (leave.holiday_type == 'employee' and len(leave.employee_ids) > 1):
                if leave.holiday_type == 'employee':
                    employees = leave.employee_ids
                elif leave.holiday_type == 'category':
                    employees = leave.category_id.employee_ids
                elif leave.holiday_type == 'company':
                    employees = self.env['hr.employee'].search([('company_id', '=', leave.mode_company_id.id)])
                else:
                    employees = leave.department_id.member_ids

                conflicting_leaves = self.env['hr.leave'].with_context(
                    tracking_disable=True,
                    mail_activity_automation_skip=True,
                    leave_fast_create=True
                ).search([
                    ('date_from', '<=', leave.date_to),
                    ('date_to', '>', leave.date_from),
                    ('state', 'not in', ['cancel', 'refuse']),
                    ('holiday_type', '=', 'employee'),
                    ('employee_id', 'in', employees.ids)])

                if conflicting_leaves:
                    # YTI: More complex use cases could be managed in master
                    if leave.leave_type_request_unit != 'day' or any(l.leave_type_request_unit == 'hour' for l in conflicting_leaves):
                        raise ValidationError(_('You can not have 2 time off that overlaps on the same day.'))

                    # keep track of conflicting leaves states before refusal
                    target_states = {l.id: l.state for l in conflicting_leaves}
                    conflicting_leaves.action_refuse()
                    split_leaves_vals = []
                    for conflicting_leave in conflicting_leaves:
                        if conflicting_leave.leave_type_request_unit == 'half_day' and conflicting_leave.request_unit_half:
                            continue

                        # Leaves in days
                        if conflicting_leave.date_from < leave.date_from:
                            before_leave_vals = conflicting_leave.copy_data({
                                'date_from': conflicting_leave.date_from.date(),
                                'date_to': leave.date_from.date() + timedelta(days=-1),
                                'state': target_states[conflicting_leave.id],
                            })[0]
                            before_leave = self.env['hr.leave'].new(before_leave_vals)
                            before_leave._compute_date_from_to()

                            # Could happen for part-time contract, that time off is not necessary
                            # anymore.
                            # Imagine you work on monday-wednesday-friday only.
                            # You take a time off on friday.
                            # We create a company time off on friday.
                            # By looking at the last attendance before the company time off
                            # start date to compute the date_to, you would have a date_from > date_to.
                            # Just don't create the leave at that time. That's the reason why we use
                            # new instead of create. As the leave is not actually created yet, the sql
                            # constraint didn't check date_from < date_to yet.
                            if before_leave.date_from < before_leave.date_to:
                                split_leaves_vals.append(before_leave._convert_to_write(before_leave._cache))
                        if conflicting_leave.date_to > leave.date_to:
                            after_leave_vals = conflicting_leave.copy_data({
                                'date_from': leave.date_to.date() + timedelta(days=1),
                                'date_to': conflicting_leave.date_to.date(),
                                'state': target_states[conflicting_leave.id],
                            })[0]
                            after_leave = self.env['hr.leave'].new(after_leave_vals)
                            after_leave._compute_date_from_to()
                            # Could happen for part-time contract, that time off is not necessary
                            # anymore.
                            if after_leave.date_from < after_leave.date_to:
                                split_leaves_vals.append(after_leave._convert_to_write(after_leave._cache))

                    split_leaves = self.env['hr.leave'].with_context(
                        tracking_disable=True,
                        mail_activity_automation_skip=True,
                        leave_fast_create=True,
                        leave_skip_state_check=True
                    ).create(split_leaves_vals)

                    split_leaves.filtered(lambda l: l.state in 'validate')._validate_leave_request()

                values = leave._prepare_employees_holiday_values(employees)
                leaves = self.env['hr.leave'].with_context(
                    tracking_disable=True,
                    mail_activity_automation_skip=True,
                    leave_fast_create=True,
                    no_calendar_sync=True,
                    leave_skip_state_check=True,
                ).create(values)

                leaves._validate_leave_request()

        leaves_second_approver.write({'second_approver_id': current_employee.id})
        leaves_first_approver.write({'first_approver_id': current_employee.id})

        employee_requests = self.filtered(lambda hol: hol.holiday_type == 'employee')
        employee_requests._validate_leave_request()
        if not self.env.context.get('leave_fast_create'):
            employee_requests.filtered(lambda holiday: holiday.validation_type != 'no_validation').activity_update()
        return True


    @api.onchange('identification_id_custom', 'custom_pin')
    def _onchange_identification_id_custom(self):
        for rec in self:
            if rec.identification_id_custom:
                all_emp = self.env['hr.employee'].sudo().search([('identification_id', '=', rec.identification_id_custom)])
                # print('all emp', all_emp)
                # print('all emp=len(rec.employee_ids)=', len(rec.employee_ids))
                if len(rec.employee_ids) == 0:
                    # print('all emp===========', rec.employee_ids)
                    if len(all_emp) == 1:
                        self.write({'employee_ids': [(6, 0, all_emp.ids)]})
                        rec.custom_pin = all_emp.custom_employee_pin_number
            if rec.custom_pin:
                all_emp = self.env['hr.employee'].sudo().search([('pin', '=', rec.custom_pin)])
                if len(rec.employee_ids) == 0:
                    # print('all emp===========', rec.employee_ids)
                    if len(all_emp) == 1:
                        self.write({'employee_ids': [(6, 0, all_emp.ids)]})
                        rec.identification_id_custom = all_emp.identification_id

    @api.onchange('employee_ids')
    def _onchange_employee_ids_id_custom(self):
        for rec in self:
            if rec.employee_ids:
                # print('employee_ids==', rec.employee_ids)
                # print('employee_ids==', rec.employee_ids[0]._origin.id)
                all_emp = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_ids[0]._origin.id)])
                if len(all_emp) == 1:
                    rec.identification_id_custom = all_emp.identification_id
                    # rec.custom_pin = all_emp.pin
                    rec.custom_pin = all_emp.custom_employee_pin_number

    def _get_leaves_on_public_holiday(self):
        print('_get_leaves_on_public_holiday')
        # var = self.filtered(lambda l: l.employee_id and not l.number_of_days)
        # print('_get_leaves_on_public_holiday==', var)
        return self.filtered(lambda l: l.employee_id and not l.number_of_days)

    def action_create_unpaid(self):
        for rec in self:
            if rec.number_of_days > rec.net_days and rec.holiday_status_id.create_unpaid == True:
                new_days = rec.number_of_days - rec.net_days
                # print('new days==', new_days)
                rec.number_of_days = rec.net_days
                unpaid_id = self.env['hr.leave.type'].sudo().search([('name', '=', 'Unpaid')])
                # print('000', unpaid_id)
                # print('000', rec.employee_ids, rec.employee_ids.ids, rec.employee_ids.id)
                if unpaid_id:
                    rfq_obj = self.env['hr.leave'].sudo().create({
                        'employee_id': rec.employee_ids.id,
                        'holiday_status_id': unpaid_id.id,
                        'number_of_days': new_days,
                        'time_off_types': 'unpaid',
                        'return_date': rec.return_date,
                        'last_working_date': rec.last_working_date,
                        'related_leave_id': rec.id,
                        'state': 'draft',
                    })
                    # print('rfq_obj====', rfq_obj)
                    if rfq_obj:
                        rec.related_leave_id = rfq_obj.id
                        rfq_obj.action_confirm()
                        rfq_obj.action_approve()
                        # rfq_obj.write({'employee_ids': [(6, 0, rec.employee_ids.ids)]})
                        # print('rfq_obj==', rfq_obj)
            else:
                print('Done')

    def action_approve(self):
        # if validation_type == 'both': this method is the first approval approval
        # if validation_type != 'both': this method calls action_validate() below
        if any(holiday.state != 'confirm' for holiday in self):
            raise UserError(_('Time off request must be confirmed ("To Approve") in order to approve it.'))

        current_employee = self.env.user.employee_id
        self.filtered(lambda hol: hol.validation_type == 'both').write({'state': 'validate1', 'first_approver_id': current_employee.id})


        # Post a second message, more verbose than the tracking message
        for holiday in self.filtered(lambda holiday: holiday.employee_id.user_id):
            holiday.message_post(
                body=_(
                    'Your %(leave_type)s planned on %(date)s has been accepted',
                    leave_type=holiday.holiday_status_id.display_name,
                    date=holiday.date_from
                ),
                partner_ids=holiday.employee_id.user_id.partner_id.ids)

        self.filtered(lambda hol: not hol.validation_type == 'both').action_validate()
        if not self.env.context.get('leave_fast_create'):
            self.activity_update()

        self.action_create_unpaid()
        print("action_approve")
        print("action_create_unpaid")
        print("action_create_unpaid done")
        for rec in self:
            if rec.holiday_status_id.add_to == True:
                if len(rec.employee_id) == 1:
                    rec.employee_id.in_a_num_to_compute = rec.employee_id.in_a_num_to_compute + rec.number_of_days
                    rec.employee_id.last_time_off_last_days = rec.employee_id.time_off_custom_days
                    rec.employee_id.time_off_custom_days = rec.number_of_days
                    # print('rec.employee_id.in_a_num_to_compute====', rec.employee_id.in_a_num_to_compute)
                # if len(rec.employee_ids) == 1:
                #     rec.employee_ids.in_a_num_to_compute = rec.employee_ids.in_a_num_to_compute + rec.number_of_days
        return True

    @api.constrains('date_from', 'date_to', 'employee_id')
    def _check_date(self):
        if self.env.context.get('leave_skip_date_check', False):
            return
        for holiday in self.filtered('employee_id'):
            if holiday.date_to and holiday.date_from:
                domain = [
                    ('date_from', '<', holiday.date_to),
                    ('date_to', '>', holiday.date_from),
                    ('employee_id', '=', holiday.employee_id.id),
                    ('id', '!=', holiday.id),
                    ('state', 'not in', ['cancel', 'refuse']),
                ]
                nholidays = self.search_count(domain)
                if nholidays:
                    print('hi')
                    # raise ValidationError(
                    #     _('You can not set 2 time off that overlaps on the same day for the same employee.') + '\n- %s' % (holiday.display_name))

class HrLeaveInherit(models.Model):
    _inherit = 'hr.leave.type'

    add_to = fields.Boolean(string="Add To Days Taken")
    create_unpaid = fields.Boolean(string="Create Unpaid")