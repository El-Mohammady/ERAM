# -*- coding: utf-8 -*-
{
    'name': "IET Payroll Rule",
    'summary': ' Add new rule in payroll for Saudi and other employee  ',
    'description': ' Add new rule in payroll for Saudi and other employee ',
    'author': "Noura",
    'website': "https://www.intelligent-experts.com",
    'category': 'Uncategorized',
    'depends': ['base', 'hr', 'hr_payroll', 'l10n_sa_hr_payroll'],
    'data': [
        'data/data_rule.xml',
        # 'data/payroll_rule.xml',
        # 'data/activity.xml',
    ],
       'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
