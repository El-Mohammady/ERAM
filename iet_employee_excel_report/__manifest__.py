# -*- coding: utf-8 -*-
{
    'name': "Employee Excel Report",
    'summary': """
        Employee Excel Report
                """,
    'description': """
        Employee Excel Report
    """,
    'author': "IET",
    'website': "https://www.yourcompany.com",
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_contract', 'report_xlsx', 'hr_payroll_customs'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/employee_wizard.xml',
        'reports/employee_excel_action.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
