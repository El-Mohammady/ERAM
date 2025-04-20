from odoo import http
from odoo.http import request
import json
from .responses import valid_response, invalid_response


class CrmLeadApi(http.Controller):
    # CREATE End Point Using http type
    @http.route('/crm/lead/post', type='http', methods=['POST'], auth='public', csrf=False)
    def post_crm_lead(self):
        try:
            # JSON Form
            args = request.httprequest.data.decode()
            # Dictionary Form
            vals = json.loads(args)
            vals_list = {}
            # Handling Expected Issues
            if not vals.get('name'):
                return invalid_response(error='The name not be entered.', status=400)

            vals_list['partner_name'] = vals.get('name') #company name

            if not vals.get('property_number'):
                return invalid_response(error='The property number not be entered.', status=400)
            property_number_id = request.env['crm.projects'].sudo().search([
                ('name', '=', vals.get('property_number'))
            ], limit=1)
            if not property_number_id:
                return invalid_response(error='The property number entered does not exist.', status=404)

            vals_list['property_number_id'] = property_number_id.id #property number
            vals_list['name'] = str(vals.get('name')) + " - " + str(property_number_id.name) #name

            if vals.get('email'):
                vals_list['email_from'] = vals.get('email') #Email

            vals_list['type'] = 'lead'  # user
            vals_list['user_id'] = 11  # user
            vals_list['company_id'] = 2  # company

            lead = request.env['crm.lead'].sudo().create(vals_list)
            return valid_response(
                message="Created Successfully.",
                data={
                'ID': lead.id,
                'Name': lead.name,
                'Property Number': lead.property_number_id.name,
                'Company Name': lead.partner_name,
                'Email': lead.email_from,
            })
        # Handling General Issues
        except Exception as error:
            return invalid_response(error = error, status=400)
