# -*- coding: utf-8 -*-
{
    'name': "hr_leave_customs",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_holidays', 'hr_contract', 'custom_pin_and_iden'],
    'data': [
        'security/ir.model.access.csv',
        'views/return_from_vacation.xml',
        'views/leave_inherit.xml',
        'report/leave_report.xml',

    ],
    "license": "LGPL-3",
}
