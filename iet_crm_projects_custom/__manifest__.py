# -*- coding: utf-8 -*-
{
    'name': "IET Crm Custom",

    'summary': "Module to send email to create ticket inside help desk",

    'description': """""",

    'author': "Ali El-Mohammady | IET",
    'website': "https://intelligent-experts.com/",

    'version': '0.1',

    'depends': ['base','crm','mail','sale','product','sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/crm_projects.xml',
        'views/product_template_inherit.xml',
        'views/models.xml',
        'views/crm_lead_inherit.xml',
        'views/res_partner_inherit.xml',
    ],
    # 'assets': {
    #     'survey.survey_assets': [
    #         '/iet_helpdesk_survey_custom/static/src/js/survey_form.js']
    # }
}

