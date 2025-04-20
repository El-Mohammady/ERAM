from odoo import fields, http, _
from odoo.http import request
import webbrowser
import json
from odoo.addons.website.controllers import form


class WebsiteForm(form.WebsiteForm):
    def insert_attachment(self, model, id_record, files):
        super().insert_attachment(model, id_record, files)
        # If the helpdesk ticket form is submit with attachments,
        # Give access token to these attachments and make the message
        # accessible to the portal user
        # (which will be able to view and download its own documents).
        model_name = model.model
        if model_name == "helpdesk.ticket":
            ticket = model.env[model_name].browse(id_record)
            attachments = request.env['ir.attachment'].sudo().search(
                [('res_model', '=', model_name), ('res_id', '=', ticket.id), ('access_token', '=', False)])
            attachments.generate_access_token()
            message = ticket.message_ids.filtered(lambda m: m.attachment_ids == attachments)
            message.is_internal = False
            message.subtype_id = request.env.ref('mail.mt_comment')

    @http.route(["/ticket/new/data/<string:model_name>", "/ticket/new/data"], type='http', auth="public",
                cors='*', website=True, methods=['GET', "POST"])
    def ticket_create_new(self, model_name='', user=None, **kwargs):
        today = fields.Date.today()
        if request.httprequest.method == 'POST':
            data = self.extract_data(request.env.ref('helpdesk.model_helpdesk_ticket'), kwargs)
            # partner_id = int(kwargs.get('partner_id')) if kwargs.get('partner_id') != '' else None
            reason_id = int(kwargs.get('reason_id')) if kwargs.get('reason_id') != '' else None
            phone = kwargs.get('phone')
            name = kwargs.get('name')
            notes = kwargs.get('description')
            team = int(kwargs.get('team_id')) if kwargs.get('team_id') != '' else None
            values = {
                'name': name,
                'partner_id': request.env.user.partner_id.id,
                'reason_id': reason_id,
                'description': notes,
                'team_id': team,
                'partner_phone': phone,
            }
            ticket = request.env['helpdesk.ticket'].sudo().create(values)
            self.insert_attachment(request.env.ref('helpdesk.model_helpdesk_ticket'), ticket.id, data['attachments'])
            request.session['form_builder_model_model'] = request.env.ref('helpdesk.model_helpdesk_ticket').model
            request.session['form_builder_model'] = request.env.ref('helpdesk.model_helpdesk_ticket').name
            request.session['form_builder_id'] = ticket.id

            return json.dumps({'id': ticket.id})
        else:
            return request.render("iet_ticket_portal.ticket_apply",
                                  {'partners': request.env['res.partner'].sudo().search([]),
                                   'reasons': request.env['ticket.reason.type'].sudo().search([]),
                                   'teams': request.env['helpdesk.team'].sudo().search([])})
