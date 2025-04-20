# -*- coding: utf-8 -*-
{
    'name': "IET CRM API",

    'summary': "End Point to create CRM Lead",

    'description': """
    End Point to create CRM Lead
        """,

    'author': "IET - Mohammed Abd Elkhalek",
    'website': "https://www.intelligent-experts.com",

    'category': 'Sales/CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
