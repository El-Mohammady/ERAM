# -*- coding: utf-8 -*-
{
    'name': "IET Employee Analytic Update",
    'summary': ' Edit analytic Employee Form to get debit and credit in each account ',
    'description': ' Edit analytic Employee Form to get debit and credit in each account ',
    'author': "Noura",
    'website': "https://www.intelligent-experts.com",
    'category': 'Uncategorized',
    'sequence': '200',
    'depends': ['base', 'employee_analytic_report','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_analytic_report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
