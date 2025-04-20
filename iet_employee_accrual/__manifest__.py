# -*- coding: utf-8 -*-
{
    'name': "IET Employee Accrual Leave",
    'summary': ' Edit Total Days in accrual Leave ',
    'description': ' Edit Total Days in accrual Leave ',
    'author': "Noura",
    'website': "https://www.intelligent-experts.com",
    'category': 'Uncategorized',
    'sequence': '200',
    'depends': ['base', 'hr_payroll_customs','l10n_sa_hr_payroll'],
    'data': [
        'views/hr_contracr_inherit_form_view.xml',
        # 'wizard/journal_item_wizard.xml',
        # 'report/report_action.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
