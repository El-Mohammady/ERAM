# -*- coding: utf-8 -*-
{
    'name': "IET HR Employee",
    'summary': """
        Add fields to Hr model """,
    'description': """
         Add fields to Hr model 
    """,
    'author': "IET, Alshimaa",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/bank_account.xml',
        'views/hr_employee.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
