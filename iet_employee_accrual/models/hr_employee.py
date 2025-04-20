from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, time, timedelta


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    @api.depends('total_days_all', 'in_a_num_to_compute', 'time_off_custom_days')
    def _compute_net_days(self):
        for rec in self:
            # total = 0
            # if rec.duration_due > 0:
            #     total = (rec.duration_due * 30) / 365
            # if rec.duration_due_less_than > 0:
            #     total =+ (rec.duration_due_less_than * 21) / 365

            # Edit here
            # rec.net_days = rec.total_days_all - rec.in_a_num_to_compute

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
                total_days = rec.custom_duration0_due_less_than5 + rec.custom_duration0_due0
                if rec.thirty_days:
                    rec.net_days = (total_days * 30) / 360
                else:
                    rec.net_days = (total_days * 21) / 360
                if rec.in_a_num_to_compute and rec.net_days:
                    rec.net_days = rec.net_days - rec.in_a_num_to_compute
                # rec.custom_accrual0_leave0 = rec.net_days * p_day
                rec.custom_accrual0_leave0 = rec.time_off_custom_days * p_day
                rec.amount_of_total_days = rec.total_days_all * p_day
                rec.amount_of_net_days = rec.net_days * p_day
                rec.amount_of_days_taken = rec.in_a_num_to_compute * p_day
            else:
                rec.amount_of_total_days = 0
                rec.amount_of_net_days = 0
                rec.amount_of_days_taken = 0

    def compute_custom_accrual_leave(self):
        print('compute_custom_accrual_leave')
        # hr_contract = self.env['hr.employee'].search(['|', ('active','=',True), ('active','=',False)])
        for rec in self:
            print('compute_custom_accrual_leave==', rec)
            all_return_vacation = self.env['return.vacation'].search([('employee_id', '=', rec.id),
                                                                      ('time_off_types', '=', 'annual_vacation')])
            # ('state', '=', 'approved')
            print('all_return_vacation', all_return_vacation, len(all_return_vacation))
            if all_return_vacation:
                print('if=======')
                if len(all_return_vacation) == 1:
                    print('len 1=====')
                    print('return_vacation.leave_id.last_working_date',
                          all_return_vacation.leave_id.last_working_date)
                    all_return_vacation.leave_id.last_working_date = all_return_vacation.leave_id.request_date_from - timedelta(
                        days=1)
                    if all_return_vacation.leave_id.last_working_date < date.today():
                        # dat1 all_return_vacation.leave_id.last_working_date
                        # all_return_vacation.leave_id.last_working_date = all_return_vacation.leave_id.request_date_from - timedelta(days=1)
                        print('return_vacation.leave_id.last_working_date',
                              all_return_vacation.leave_id.last_working_date)
                        d1 = all_return_vacation.leave_id.last_working_date
                        print('first contract date',rec.first_contract_date)
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
                        rec.custom_total0_year0 = delta.days / 360
                        if rec.custom_total0_year0 < 0:
                            rec.custom_total0_year0 = 0
                        if delta.days >= 1800:
                            rec.custom_duration0_due_less_than5 = 1800
                            if rec.thirty_days == True:
                                true_days_less_than = (1800 * 15) / 360
                            else:
                                true_days_less_than = (1800 * 21) / 360
                            rec.custom_duration0_due0 = delta.days - 1800
                            if rec.custom_duration0_due0 < 0:
                                rec.custom_duration0_due0 = 0
                            true_days = (rec.custom_duration0_due0 * 30) / 360
                            total_days = true_days_less_than + true_days
                            rec.total_days_all = total_days
                            print('rec.total_days_all', rec.total_days_all)
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
                                print('delta.days',delta.days)
                                true_days_less_than = (delta.days * 15) / 360
                            else:
                                true_days_less_than = (delta.days * 21) / 360
                            rec.custom_duration0_due0 = 0
                            # true_days = (rec.custom_duration0_due0 * 30) / 360
                            # total_days = true_days_less_than + true_days
                            rec.total_days_all = true_days_less_than
                            print('rec.total_days_all====>2', rec.total_days_all)
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
                    the_num_of_year = the_num.days / 360
                    # print('the_num_of_year', the_num_of_year)
                    if the_num_of_year <= 5:
                        rec.custom_duration0_due_less_than5 = delta.days
                        if rec.custom_duration0_due_less_than5 < 0:
                            rec.custom_duration0_due_less_than5 = 0
                        if rec.thirty_days == True:
                            true_days_less_than = (delta.days * 30) / 360
                        else:
                            true_days_less_than = (delta.days * 21) / 360
                        rec.custom_duration0_due0 = 0
                        # true_days = (rec.custom_duration0_due0 * 30) / 360
                        # total_days = true_days_less_than + true_days
                        rec.total_days_all = true_days_less_than
                        print('rec.total_days_all====4>', rec.total_days_all)
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
                            true_days_less_than = (1800 * 30) / 360
                        else:
                            true_days_less_than = (1800 * 21) / 360
                        rec.custom_duration0_due0 = delta.days - 1800

                        if rec.custom_duration0_due0 < 0:
                            rec.custom_duration0_due0 = 0

                        true_days = (rec.custom_duration0_due0 * 30) / 360
                        total_days = true_days_less_than + true_days
                        rec.total_days_all = total_days
                        print('rec.total_days_all=======3>', rec.total_days_all)
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
                print('else')
                print('sart date',rec.first_contract_date)
                if rec.first_contract_date:
                    get_date_contract = self.env['hr.contract'].search([('employee_id', '=', rec.id),
                                                                        ('state', 'in', ['close', 'open'])], limit=1)

                    if rec.active == False:
                        if get_date_contract:
                            d1 = get_date_contract[0].date_end
                            # print('d1==', d1, rec, rec.id)
                        else:
                            d1 = date.today()
                    else:
                        d1 = date.today()

                    d2 = rec.first_contract_date
                    print('d2',d2)
                    delta = d1 - d2
                    print('delta', delta)
                    rec.no_vacation11 = d1
                    rec.no_custom_vacation22 = d2
                    # print('delta', delta)
                    rec.custom_total0_year0 = delta.days / 360
                    if rec.custom_total0_year0 < 0:
                        rec.custom_total0_year0 = 0
                    if delta.days >= 1800:
                        rec.custom_duration0_due_less_than5 = 1800
                        if rec.thirty_days == True:
                            true_days_less_than = (1800 * 15) / 360
                        else:
                            true_days_less_than = (1800 * 21) / 360
                        rec.custom_duration0_due0 = delta.days - 1800

                        if rec.custom_duration0_due0 < 0:
                            rec.custom_duration0_due0 = 0

                        true_days = (rec.custom_duration0_due0 * 30) / 360
                        total_days = true_days_less_than + true_days
                        rec.total_days_all = total_days
                        print('rec.total_days_all=====2>', rec.total_days_all)
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
                            print('rec.custom_year',rec.custom_total0_year0)
                            true_days_less_than = (delta.days * 15) / 360
                            print('true_days_less_than11#####', true_days_less_than)
                        else:
                            true_days_less_than = (delta.days * 21) / 360
                            print('true_days_less_than333#####', true_days_less_than)
                        rec.custom_duration0_due0 = 0
                        # true_days = (rec.custom_duration0_due0 * 30) / 360
                        # total_days = true_days_less_than + true_days
                        rec.total_days_all = true_days_less_than
                        print('rec.total_days_all =====111>', rec.total_days_all)
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



