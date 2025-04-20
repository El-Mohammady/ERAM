# -*- coding: utf-8 -*-
{
    'name': "IET Payroll Employee Analytic",
    'summary': ' Add analytic Employee checkbox in rule and if it checked make journal create line for each employee in batch   ',
    'description': ' Add analytic Employee checkbox in rule ',
    'author': "Noura",
    'website': "https://www.intelligent-experts.com",
    'category': 'Uncategorized',
    'sequence': '200',
    'depends': ['base', 'hr_payroll_account','hr','employee_analytic_report'],
    'data': [
        # 'views/hr_payroll_account_inherit.xml',
        # 'views/hr_payslip.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
