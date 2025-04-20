# -*- coding: utf-8 -*-
{
    'name': "hr_payroll_customs",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_contract', 'hr_payroll', 'hr_holidays', 'l10n_sa_hr_payroll',
                "resignation_request",
                ],

    # always loaded
    'data': [
        'data/rule_data.xml',
        'data/cron_for_payroll_information.xml',
        'data/hr_data.xml',
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/contract_inherit.xml',
        'views/leave_inherit.xml',
        'report/payroll_report.xml',
    ],
    "license": "LGPL-3",
}
