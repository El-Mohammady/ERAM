# -*- coding: utf-8 -*-
{
    'name': "IET Create Ticket Portal",

    'summary': "Module to Create Tickets From Portal",

    'description': """""",

    'author': "Ezzedin Saleh | IET",
    'website': "https://intelligent-experts.com/",

    'version': '0.1',

    'depends': ['base', 'website_helpdesk', 'helpdesk', 'sale', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'views/ticket_reason_type_views.xml',
        'views/create_ticket_template.xml',
        'views/helpdesk_ticket.xml',
    ],
}
