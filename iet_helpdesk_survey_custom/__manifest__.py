# -*- coding: utf-8 -*-
{
    'name': "IET Helpdesk Survey Custom",

    'summary': "Module to send email to create ticket inside help desk",

    'description': """""",

    'author': "Ali El-Mohammady | IET",
    'website': "https://intelligent-experts.com/",

    'version': '0.1',

    'depends': ['base','survey','helpdesk'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/survey_inherit.xml',
        'views/survey_template_inherit.xml',
    ],
    'assets': {
        'survey.survey_assets': [
            '/iet_helpdesk_survey_custom/static/src/js/survey_form.js']
    }
}

