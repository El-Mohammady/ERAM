# -*- coding: utf-8 -*-
{
    'name': "iet_payroll_access_rights",

    'summary': """
       Groups of Eram, and Access Levels
       """,

    'description': """
        'Payslip Confirmed' group: payslip state from Draft to Waiting.  
        'Payslip Approved' group: payslip state from Waiting to Done.  
        'Payslip Confirmed' group: payslip state from Done to Paid.  
    """,

    'author': "Mohammed Abd Elkhalek",
    'website': "https://www.intelligent-experts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payroll',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_payroll', 'hr_payroll_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        # 'views/views.xml',
        # 'views/payslip_inherit_view.xml',
    ],
    "license": "LGPL-3",
}
