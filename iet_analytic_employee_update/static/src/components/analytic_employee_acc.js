/** @odoo-module **/
const {xml, Component} = owl;
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import {registry} from "@web/core/registry";


export class AnalyticEmployee extends Component {
    setup() {
        super.setup();
    }
}

AnalyticEmployee.template = xml`<pre t-esc="props.value" class="bg-primary text-white p-3 rounded"/>`;
AnalyticEmployee.props = standardFieldProps;


registry.category("fields").add("code", CodeField);