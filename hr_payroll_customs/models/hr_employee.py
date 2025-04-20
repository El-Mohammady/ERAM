from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, time, timedelta
import calendar


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, values):
        res = super(HREmployee, self).create(values)
        res.custom_employee_pin_number = self.env['ir.sequence'].next_by_code('emp.number.seq')
        return res

    custom_duration0_due0 = fields.Float(string='Duration Due', digits=(12, 3))
    custom_duration0_due_less_than5 = fields.Float(string='Duration Due Less Than 5 Years', digits=(12, 3))
    custom_total0_year0 = fields.Float(string='Total Year', digits=(12, 3))
    custom_accrual0_leave0 = fields.Float(string='Accrual Leave of time off days', digits=(12, 3),
                                          help="Amount Of Time Off Days")
    total_days_all = fields.Float(string='Total Days', digits=(12, 3))
    amount_of_total_days = fields.Float(compute="_compute_net_days", digits=(12, 3), help="Amount Of Total Days")

    thirty_days = fields.Boolean(string="30 Days")
    time_off_custom_days = fields.Float(string='Time Off Days', digits=(12, 3))
    last_time_off_last_days = fields.Float(string='Last Time Off')

    in_a_num_to_compute = fields.Float(string='Days Taken', )
    amount_of_days_taken = fields.Float(compute="_compute_net_days", digits=(12, 3), help="Amount Of Days Taken")

    net_days = fields.Float(string='Net Days', compute="_compute_net_days", digits=(12, 3))
    amount_of_net_days = fields.Float(compute="_compute_net_days", digits=(12, 3), help="Amount Of Net Days")

    date11_return_vacation11 = fields.Date(string="last working date in return vacation", required=False, )
    date22_return_vacation22 = fields.Date(string="today date or first contract date", required=False, )
    more11_than_vacation11 = fields.Date(string="more than vacation today date", required=False,
                                         help="Today Date or False")
    more22_than_vacation22 = fields.Date(string="return_date for more than vacation or today date", required=False, )
    custom_today_date00 = fields.Date(string="Today Date", required=False, )
    custom_first_contract_date00_custom = fields.Date(string="First Contract Date", required=False)
    no_vacation11 = fields.Date(string="contract end date or today date", required=False, )
    no_custom_vacation22 = fields.Date(string="first contract date or False", required=False,
                                       help="first contract date or False")

    def get_exceptional_request_departure_resignation(self, id, date_from, date_to):
        # contract = self.env['hr.contract'].search([('employee_id', '=', id)], limit=1)
        the_employee_id = self.env['hr.employee'].search(
            ['|', ('id', '=', id), ('active', '=', True), ('active', '=', False)])
        # print('id==', id)
        # print('employee_id==', the_employee_id)
        # , ('state', '=', 'open')
        # ('state', 'in', ['close', 'open'])
        result = 0
        if the_employee_id:
            # start_date = contract.first_contract_date
            # end_date = contract.date_end
            # # difference = relativedelta(end_date, start_date)
            # # total_days = difference.years * 365 + difference.months * 30 + difference.days
            # # print('total_days years==', total_days)
            # delta = end_date - start_date
            # print('delta==', delta.days)
            # total_days = delta.days
            # compensation = contract.wage + contract.l10n_sa_housing_allowance + contract.l10n_sa_transportation_allowance + contract.l10n_sa_other_allowances
            total_days = the_employee_id.custom_duration0_due0 + the_employee_id.custom_duration0_due_less_than5
            compensation = the_employee_id.total_salary
            # print('$$$==', total_days, compensation)
            if total_days < 730:
                result = 0
            elif 730 <= total_days <= 1825:
                result = (((compensation / 2) * (total_days / 360))) / 3
            elif 1825 < total_days <= 3600:
                # result = ((compensation / 3) * 5)
                # result += ((compensation * ( 2/3 )) * ((total_days / 365) - 5))
                result = ((compensation * (2 / 3)) * (total_days / 360))
            else:
                result = (compensation * (total_days / 360))
            # result = payslip.dict.company_id.currency_id.round(result)
        result = self.company_id.currency_id.round(result)
        return result

    def get_termination_of_the_contract_by_the_company(self, id, date_from, date_to):
        contract = self.env['hr.contract'].search([('employee_id', '=', id), ('state', '=', 'open')], limit=1)
        # ('state', 'in', ['close', 'open'])
        result = 0
        if contract:
            start_date = contract.first_contract_date
            end_date = contract.date_end
            # print('start_date', start_date, 'end_date', end_date)
            difference = relativedelta(end_date, start_date)
            # print('difference', difference,)
            total_days = difference.years * 365 + difference.months * 30 + difference.days
            # print('total_days', total_days,)
            compensation = contract.wage + contract.l10n_sa_housing_allowance + contract.l10n_sa_transportation_allowance + contract.l10n_sa_other_allowances
            if total_days <= 1825:
                result = (compensation / 2 * total_days / 365)
            # elif 720 <= total_days <= 5 * 720:
            #     result = (compensation / 3 * total_days / 365)
            else:
                # result = ((compensation / 2) * 5)
                # result += (compensation * ((total_days / 365) - 5))
                result = (compensation * (total_days / 365))
        result = self.company_id.currency_id.round(result)
        return result

    @api.depends('total_days_all', 'in_a_num_to_compute', 'time_off_custom_days')
    def _compute_net_days(self):
        for rec in self:
            # total = 0
            # if rec.duration_due > 0:
            #     total = (rec.duration_due * 30) / 365
            # if rec.duration_due_less_than > 0:
            #     total =+ (rec.duration_due_less_than * 21) / 365
            rec.net_days = rec.total_days_all - rec.in_a_num_to_compute
            if rec.net_days > 0:
                rec.net_days = rec.net_days
            else:
                rec.net_days = 0
            # contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),('state', '=', 'open')],
            contract = self.env['hr.contract'].search(
                [('employee_id', '=', rec.id), ('state', 'in', ['close', 'open'])],
                limit=1)
            if contract:
                p_day = 0
                for c in contract:
                    p_day = c.total_salary / 30
                # rec.custom_accrual0_leave0 = rec.net_days * p_day
                rec.custom_accrual0_leave0 = rec.time_off_custom_days * p_day
                rec.amount_of_total_days = rec.total_days_all * p_day
                rec.amount_of_net_days = rec.net_days * p_day
                rec.amount_of_days_taken = rec.in_a_num_to_compute * p_day
            else:
                rec.amount_of_total_days = 0
                rec.amount_of_net_days = 0
                rec.amount_of_days_taken = 0

    # @api.depends('first_contract_date')

    # cron to compute some fields in employee screen
    @api.model
    def action_compute_custom_duration0_due0(self):
        print('action_compute_custom_duration0_due0==')
        hr_contract = self.env['hr.employee'].search(['|', ('active', '=', True), ('active', '=', False)])
        # print('hr_contract==', hr_contract)
        for rec in hr_contract:
            # print('rec==', rec)
            # print('first_contract_date', rec.first_contract_date)
            # total_work_days = relativedelta(date.today(), rec.first_contract_date)
            # print('total_work_days', total_work_days)
            # d1 = date.today()
            all_return_vacation = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                                                                      ('time_off_types', '=', 'annual_vacation'),
                                                                      ])
            # ('state', '=', 'approved')
            # print('all_return_vacation', all_return_vacation, len(all_return_vacation))
            if all_return_vacation:
                if len(all_return_vacation) == 1:
                    if all_return_vacation.leave_id.last_working_date:
                        # dat1 all_return_vacation.leave_id.last_working_date
                        print('return_vacation.leave_id.last_working_date',
                              all_return_vacation.leave_id.last_working_date)
                        d1 = all_return_vacation.leave_id.last_working_date
                        if rec.first_contract_date:
                            d2 = rec.first_contract_date
                        else:
                            d2 = date.today()
                        delta = d1 - d2
                        rec.date11_return_vacation11 = d1
                        rec.date22_return_vacation22 = d2
                        # dat2 arec.first_contract_date date.today()
                        # print('delta==', delta)
                        # print('delta==', delta.days)
                        # end_date22 = datetime(all_return_vacation.leave_id.last_working_date.year,
                        #                     all_return_vacation.leave_id.last_working_date.month,
                        #                       calendar.mdays[all_return_vacation.leave_id.last_working_date.month])
                        # print('total_work_days22', end_date22)
                        rec.custom_total0_year0 = delta.days / 365
                        if rec.custom_total0_year0 < 0:
                            rec.custom_total0_year0 = 0
                        if delta.days >= 1800:
                            rec.custom_duration0_due_less_than5 = 1800
                            if rec.thirty_days == True:
                                true_days_less_than = (1800 * 30) / 365
                            else:
                                true_days_less_than = (1800 * 21) / 365
                            rec.custom_duration0_due0 = delta.days - 1800
                            if rec.custom_duration0_due0 < 0:
                                rec.custom_duration0_due0 = 0
                            true_days = (rec.custom_duration0_due0 * 30) / 365
                            total_days = true_days_less_than + true_days
                            rec.total_days_all = total_days
                            if rec.total_days_all < 0:
                                rec.total_days_all = 0
                            hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                          ('state', '=', 'open')],
                                                                         limit=1)
                            # print('hr_contract', hr_contract)
                            if hr_contract:
                                p_day = 0
                                for c in hr_contract:
                                    # print('cc', c.total_salary)
                                    p_day = c.total_salary / 30
                                # print('custom_accrual0_leave0==0=', p_day , rec.total_days_all)
                                rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                                if rec.custom_accrual0_leave0 < 0:
                                    rec.custom_accrual0_leave0 = 0
                            else:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_duration0_due_less_than5 = delta.days

                            if rec.custom_duration0_due_less_than5 < 0:
                                rec.custom_duration0_due_less_than5 = 0
                            if rec.thirty_days == True:
                                true_days_less_than = (delta.days * 30) / 365
                            else:
                                true_days_less_than = (delta.days * 21) / 365
                            rec.custom_duration0_due0 = 0
                            # true_days = (rec.custom_duration0_due0 * 30) / 365
                            # total_days = true_days_less_than + true_days
                            rec.total_days_all = true_days_less_than
                            if rec.total_days_all < 0:
                                rec.total_days_all = 0
                            hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                          ('state', '=', 'open')],
                                                                         limit=1)
                            if hr_contract:
                                p_day = 0
                                for c in hr_contract:
                                    # print('cc', c.total_salary)
                                    p_day = c.total_salary / 30
                                # print('else custom_accrual0_leave0==0=', p_day , rec.total_days_all)
                                rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                                if rec.custom_accrual0_leave0 < 0:
                                    rec.custom_accrual0_leave0 = 0
                                # print('custom_accrual0_leave0=0=', rec.custom_accrual0_leave0)
                            else:
                                rec.custom_accrual0_leave0 = 0
                    # if no last_working_date
                    else:
                        rec.custom_duration0_due0 = 0
                        rec.custom_duration0_due_less_than5 = 0
                        rec.custom_total0_year0 = 0
                        rec.custom_accrual0_leave0 = 0
                        rec.total_days_all = 0
                # if user have more than one return
                else:
                    # first_return_vacation_new = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                    #                                                                 ('time_off_types', '=', 'annual_vacation'),
                    #                                                                 ('state', '=', 'approved')],
                    #                                                                order='return_date DESC', limit=1)
                    # last_return_vacation = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                    #                                                            ('time_off_types', '=', 'annual_vacation'),
                    #                                                            ('state', '=', 'approved')],
                    #                                                           order='return_date asc', limit=1)
                    # the_second_return_vacation = self.env['return.vacation'].search([
                    #     ('id', '!=', all_return_vacation[-1].id),
                    #     ('employee_id', '=', rec.id),
                    #     ('time_off_types', '=', 'annual_vacation'),
                    #     ('state', '=', 'approved')
                    # ])
                    d1 = date.today()
                    if all_return_vacation[-1].return_date:
                        d2 = all_return_vacation[-1].return_date
                    else:
                        d2 = date.today()
                    delta = d1 - d2
                    rec.more11_than_vacation11 = d1
                    rec.more22_than_vacation22 = d2
                    # date
                    # print('delta=return_vacation=', delta)
                    # print('delta=return_vacation=', delta.days)
                    if rec.first_contract_date:
                        d2 = rec.first_contract_date
                    else:
                        d2 = date.today()
                    the_num = d1 - d2
                    rec.custom_today_date00 = d1
                    rec.custom_first_contract_date00_custom = d2
                    # print('the_num_of_year', the_num)
                    the_num_of_year = the_num.days / 365
                    # print('the_num_of_year', the_num_of_year)
                    if the_num_of_year <= 5:
                        rec.custom_duration0_due_less_than5 = delta.days
                        if rec.custom_duration0_due_less_than5 < 0:
                            rec.custom_duration0_due_less_than5 = 0
                        if rec.thirty_days == True:
                            true_days_less_than = (delta.days * 30) / 365
                        else:
                            true_days_less_than = (delta.days * 21) / 365
                        rec.custom_duration0_due0 = 0
                        # true_days = (rec.custom_duration0_due0 * 30) / 365
                        # total_days = true_days_less_than + true_days
                        rec.total_days_all = true_days_less_than
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')], limit=1)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            # print('leave0==0=', p_day , rec.total_days_all)
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                            # print('custom_accrual0_leave0=0=', rec.custom_accrual0_leave0)
                        else:
                            rec.custom_accrual0_leave0 = 0
                    else:
                        rec.custom_duration0_due_less_than5 = 1800
                        if rec.thirty_days == True:
                            true_days_less_than = (1800 * 30) / 365
                        else:
                            true_days_less_than = (1800 * 21) / 365
                        rec.custom_duration0_due0 = delta.days - 1800

                        if rec.custom_duration0_due0 < 0:
                            rec.custom_duration0_due0 = 0

                        true_days = (rec.custom_duration0_due0 * 30) / 365
                        total_days = true_days_less_than + true_days
                        rec.total_days_all = total_days
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')], limit=1)
                        # print('hr_contract', hr_contract)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            # print('custom_accrual0_leave0==0=', p_day , rec.total_days_all)
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_accrual0_leave0 = 0
                    # print('the_num_of_year', the_num_of_year.year)

                    rec.custom_total0_year0 = the_num_of_year
                    if rec.custom_total0_year0 < 0:
                        rec.custom_total0_year0 = 0
                    # print('custom_total0_year0', rec.custom_total0_year0)
            # if no return vaction
            else:
                if rec.first_contract_date:
                    get_date_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                        ('state', 'in', ['close', 'open'])], limit=1)
                    # ('state', 'in', ['close', 'open'])], limit=1)
                    if rec.active == False:
                        if get_date_contract:
                            d1 = get_date_contract[0].date_end
                            # print('d1==', d1, rec, rec.id)
                        else:
                            d1 = date.today()
                    else:
                        d1 = date.today()
                    # print("rec.first_contract_date =", rec.first_contract_date)
                    d2 = rec.first_contract_date
                    delta = d1 - d2
                    rec.no_vacation11 = d1
                    rec.no_custom_vacation22 = d2
                    # print('delta', delta)
                    rec.custom_total0_year0 = delta.days / 365
                    if rec.custom_total0_year0 < 0:
                        rec.custom_total0_year0 = 0
                    if delta.days >= 1800:
                        rec.custom_duration0_due_less_than5 = 1800
                        if rec.thirty_days == True:
                            true_days_less_than = (1800 * 30) / 365
                        else:
                            true_days_less_than = (1800 * 21) / 365
                        rec.custom_duration0_due0 = delta.days - 1800

                        if rec.custom_duration0_due0 < 0:
                            rec.custom_duration0_due0 = 0

                        true_days = (rec.custom_duration0_due0 * 30) / 365
                        total_days = true_days_less_than + true_days
                        rec.total_days_all = total_days
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')],
                                                                     limit=1)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_accrual0_leave0 = 0
                    else:
                        rec.custom_duration0_due_less_than5 = delta.days
                        if rec.custom_duration0_due_less_than5 < 0:
                            rec.custom_duration0_due_less_than5 = 0
                        if rec.thirty_days == True:
                            true_days_less_than = (delta.days * 30) / 365
                        else:
                            true_days_less_than = (delta.days * 21) / 365
                        rec.custom_duration0_due0 = 0
                        # true_days = (rec.custom_duration0_due0 * 30) / 365
                        # total_days = true_days_less_than + true_days
                        rec.total_days_all = true_days_less_than
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')],
                                                                     limit=1)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_accrual0_leave0 = 0
                    # end_date = datetime(date.today().year, date.today().month, calendar.mdays[date.today().month])
                    # print('total_work_days', end_date)
                # if no there is contract
                else:
                    rec.custom_duration0_due0 = 0
                    rec.custom_duration0_due_less_than5 = 0
                    rec.custom_total0_year0 = 0
                    rec.custom_accrual0_leave0 = 0
                    rec.total_days_all = 0

                    # dates
                    rec.date11_return_vacation11 = False
                    rec.date22_return_vacation22 = False
                    rec.more11_than_vacation11 = False
                    rec.more22_than_vacation22 = False
                    rec.custom_today_date00 = False
                    rec.custom_first_contract_date00_custom = False
                    rec.no_vacation11 = False
                    rec.no_custom_vacation22 = False
                    # continue
            rec._compute_net_days()
            the_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id), ('state', '=', 'open')],
                                                          limit=1)
            the_contract.compute_total_salary()
            all_valid_time_off = self.env['hr.leave'].search([('employee_id', '=', rec.id),
                                                              ('state', '=', 'validate')])
            # print('all_valid_time_off', all_valid_time_off)
            new_num = 0
            if all_valid_time_off:
                for t in all_valid_time_off:
                    new_num += t.number_of_days
                rec.in_a_num_to_compute = new_num
                # print('new_num', new_num)

    # button for one employee
    def compute_custom_accrual_leave(self):
        print('compute_custom_accrual_leave')
        # hr_contract = self.env['hr.employee'].search(['|', ('active','=',True), ('active','=',False)])
        for rec in self:
            print('compute_custom_accrual_leave==', rec)
            all_return_vacation = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                                                                      ('time_off_types', '=', 'annual_vacation')])
            # ('state', '=', 'approved')
            # print('all_return_vacation', all_return_vacation, len(all_return_vacation))
            if all_return_vacation:
                if len(all_return_vacation) == 1:
                    if all_return_vacation.leave_id.last_working_date:
                        # dat1 all_return_vacation.leave_id.last_working_date
                        print('return_vacation.leave_id.last_working_date',
                              all_return_vacation.leave_id.last_working_date)
                        d1 = all_return_vacation.leave_id.last_working_date
                        if rec.first_contract_date:
                            d2 = rec.first_contract_date
                        else:
                            d2 = date.today()
                        delta = d1 - d2
                        rec.date11_return_vacation11 = d1
                        rec.date22_return_vacation22 = d2
                        # dat2 arec.first_contract_date date.today()
                        # print('delta==', delta)
                        # print('delta==', delta.days)
                        # end_date22 = datetime(all_return_vacation.leave_id.last_working_date.year,
                        #                     all_return_vacation.leave_id.last_working_date.month,
                        #                       calendar.mdays[all_return_vacation.leave_id.last_working_date.month])
                        # print('total_work_days22', end_date22)
                        rec.custom_total0_year0 = delta.days / 365
                        if rec.custom_total0_year0 < 0:
                            rec.custom_total0_year0 = 0
                        if delta.days >= 1800:
                            rec.custom_duration0_due_less_than5 = 1800
                            if rec.thirty_days == True:
                                true_days_less_than = (1800 * 30) / 365
                            else:
                                true_days_less_than = (1800 * 21) / 365
                            rec.custom_duration0_due0 = delta.days - 1800
                            if rec.custom_duration0_due0 < 0:
                                rec.custom_duration0_due0 = 0
                            true_days = (rec.custom_duration0_due0 * 30) / 365
                            total_days = true_days_less_than + true_days
                            rec.total_days_all = total_days
                            if rec.total_days_all < 0:
                                rec.total_days_all = 0
                            hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                          ('state', '=', 'open')],
                                                                         limit=1)
                            # print('hr_contract', hr_contract)
                            if hr_contract:
                                p_day = 0
                                for c in hr_contract:
                                    # print('cc', c.total_salary)
                                    p_day = c.total_salary / 30
                                # print('custom_accrual0_leave0==0=', p_day , rec.total_days_all)
                                rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                                if rec.custom_accrual0_leave0 < 0:
                                    rec.custom_accrual0_leave0 = 0
                            else:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_duration0_due_less_than5 = delta.days

                            if rec.custom_duration0_due_less_than5 < 0:
                                rec.custom_duration0_due_less_than5 = 0
                            if rec.thirty_days == True:
                                true_days_less_than = (delta.days * 30) / 365
                            else:
                                true_days_less_than = (delta.days * 21) / 365
                            rec.custom_duration0_due0 = 0
                            # true_days = (rec.custom_duration0_due0 * 30) / 365
                            # total_days = true_days_less_than + true_days
                            rec.total_days_all = true_days_less_than
                            if rec.total_days_all < 0:
                                rec.total_days_all = 0
                            hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                          ('state', '=', 'open')],
                                                                         limit=1)
                            if hr_contract:
                                p_day = 0
                                for c in hr_contract:
                                    # print('cc', c.total_salary)
                                    p_day = c.total_salary / 30
                                # print('else custom_accrual0_leave0==0=', p_day , rec.total_days_all)
                                rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                                if rec.custom_accrual0_leave0 < 0:
                                    rec.custom_accrual0_leave0 = 0
                                # print('custom_accrual0_leave0=0=', rec.custom_accrual0_leave0)
                            else:
                                rec.custom_accrual0_leave0 = 0
                    # if no last_working_date
                    else:
                        rec.custom_duration0_due0 = 0
                        rec.custom_duration0_due_less_than5 = 0
                        rec.custom_total0_year0 = 0
                        rec.custom_accrual0_leave0 = 0
                        rec.total_days_all = 0
                # if user have more than one return
                else:
                    # first_return_vacation_new = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                    #                                                                 ('time_off_types', '=', 'annual_vacation'),
                    #                                                                 ('state', '=', 'approved')],
                    #                                                                order='return_date DESC', limit=1)
                    # last_return_vacation = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                    #                                                            ('time_off_types', '=', 'annual_vacation'),
                    #                                                            ('state', '=', 'approved')],
                    #                                                           order='return_date asc', limit=1)
                    # the_second_return_vacation = self.env['return.vacation'].search([
                    #     ('id', '!=', all_return_vacation[-1].id),
                    #     ('employee_id', '=', rec.id),
                    #     ('time_off_types', '=', 'annual_vacation'),
                    #     ('state', '=', 'approved')
                    # ])
                    d1 = date.today()
                    if all_return_vacation[-1].return_date:
                        d2 = all_return_vacation[-1].return_date
                    else:
                        d2 = date.today()
                    delta = d1 - d2
                    rec.more11_than_vacation11 = d1
                    rec.more22_than_vacation22 = d2
                    # date
                    # print('delta=return_vacation=', delta)
                    # print('delta=return_vacation=', delta.days)
                    if rec.first_contract_date:
                        d2 = rec.first_contract_date
                    else:
                        d2 = date.today()
                    the_num = d1 - d2
                    rec.custom_today_date00 = d1
                    rec.custom_first_contract_date00_custom = d2
                    # print('the_num_of_year', the_num)
                    the_num_of_year = the_num.days / 365
                    # print('the_num_of_year', the_num_of_year)
                    if the_num_of_year <= 5:
                        rec.custom_duration0_due_less_than5 = delta.days
                        if rec.custom_duration0_due_less_than5 < 0:
                            rec.custom_duration0_due_less_than5 = 0
                        if rec.thirty_days == True:
                            true_days_less_than = (delta.days * 30) / 365
                        else:
                            true_days_less_than = (delta.days * 21) / 365
                        rec.custom_duration0_due0 = 0
                        # true_days = (rec.custom_duration0_due0 * 30) / 365
                        # total_days = true_days_less_than + true_days
                        rec.total_days_all = true_days_less_than
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')], limit=1)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            # print('leave0==0=', p_day , rec.total_days_all)
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                            # print('custom_accrual0_leave0=0=', rec.custom_accrual0_leave0)
                        else:
                            rec.custom_accrual0_leave0 = 0
                    else:
                        rec.custom_duration0_due_less_than5 = 1800
                        if rec.thirty_days == True:
                            true_days_less_than = (1800 * 30) / 365
                        else:
                            true_days_less_than = (1800 * 21) / 365
                        rec.custom_duration0_due0 = delta.days - 1800

                        if rec.custom_duration0_due0 < 0:
                            rec.custom_duration0_due0 = 0

                        true_days = (rec.custom_duration0_due0 * 30) / 365
                        total_days = true_days_less_than + true_days
                        rec.total_days_all = total_days
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')], limit=1)
                        # print('hr_contract', hr_contract)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            # print('custom_accrual0_leave0==0=', p_day , rec.total_days_all)
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_accrual0_leave0 = 0
                    # print('the_num_of_year', the_num_of_year.year)

                    rec.custom_total0_year0 = the_num_of_year
                    if rec.custom_total0_year0 < 0:
                        rec.custom_total0_year0 = 0
                    # print('custom_total0_year0', rec.custom_total0_year0)
            # if no return vaction
            else:
                if rec.first_contract_date:
                    get_date_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                        ('state', 'in', ['close', 'open'])], limit=1)
                    # ('state', 'in', ['close', 'open'])], limit=1)
                    if rec.active == False:
                        if get_date_contract:
                            d1 = get_date_contract[0].date_end
                            # print('d1==', d1, rec, rec.id)
                        else:
                            d1 = date.today()
                    else:
                        d1 = date.today()
                    # print("rec.first_contract_date =", rec.first_contract_date)
                    d2 = rec.first_contract_date
                    delta = d1 - d2
                    rec.no_vacation11 = d1
                    rec.no_custom_vacation22 = d2
                    # print('delta', delta)
                    rec.custom_total0_year0 = delta.days / 365
                    if rec.custom_total0_year0 < 0:
                        rec.custom_total0_year0 = 0
                    if delta.days >= 1800:
                        rec.custom_duration0_due_less_than5 = 1800
                        if rec.thirty_days == True:
                            true_days_less_than = (1800 * 30) / 365
                        else:
                            true_days_less_than = (1800 * 21) / 365
                        rec.custom_duration0_due0 = delta.days - 1800

                        if rec.custom_duration0_due0 < 0:
                            rec.custom_duration0_due0 = 0

                        true_days = (rec.custom_duration0_due0 * 30) / 365
                        total_days = true_days_less_than + true_days
                        rec.total_days_all = total_days
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')],
                                                                     limit=1)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_accrual0_leave0 = 0
                    else:
                        rec.custom_duration0_due_less_than5 = delta.days
                        if rec.custom_duration0_due_less_than5 < 0:
                            rec.custom_duration0_due_less_than5 = 0
                        if rec.thirty_days == True:
                            true_days_less_than = (delta.days * 30) / 365
                        else:
                            true_days_less_than = (delta.days * 21) / 365
                        rec.custom_duration0_due0 = 0
                        # true_days = (rec.custom_duration0_due0 * 30) / 365
                        # total_days = true_days_less_than + true_days
                        rec.total_days_all = true_days_less_than
                        if rec.total_days_all < 0:
                            rec.total_days_all = 0
                        hr_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                      ('state', '=', 'open')],
                                                                     limit=1)
                        if hr_contract:
                            p_day = 0
                            for c in hr_contract:
                                # print('cc', c.total_salary)
                                p_day = c.total_salary / 30
                            rec.custom_accrual0_leave0 = p_day * rec.total_days_all
                            if rec.custom_accrual0_leave0 < 0:
                                rec.custom_accrual0_leave0 = 0
                        else:
                            rec.custom_accrual0_leave0 = 0
                    # end_date = datetime(date.today().year, date.today().month, calendar.mdays[date.today().month])
                    # print('total_work_days', end_date)
                # if no there is contract
                else:
                    rec.custom_duration0_due0 = 0
                    rec.custom_duration0_due_less_than5 = 0
                    rec.custom_total0_year0 = 0
                    rec.custom_accrual0_leave0 = 0
                    rec.total_days_all = 0

                    # dates
                    rec.date11_return_vacation11 = False
                    rec.date22_return_vacation22 = False
                    rec.more11_than_vacation11 = False
                    rec.more22_than_vacation22 = False
                    rec.custom_today_date00 = False
                    rec.custom_first_contract_date00_custom = False
                    rec.no_vacation11 = False
                    rec.no_custom_vacation22 = False
                    # continue
            rec._compute_net_days()
            the_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id), ('state', '=', 'open')],
                                                          limit=1)
            the_contract.compute_total_salary()
            all_valid_time_off = self.env['hr.leave'].search([('employee_id', '=', rec.id),
                                                              ('state', '=', 'validate')])
            # print('all_valid_time_off', all_valid_time_off)
            new_num = 0
            if all_valid_time_off:
                for t in all_valid_time_off:
                    new_num += t.number_of_days
                rec.in_a_num_to_compute = new_num
                # print('new_num', new_num)
