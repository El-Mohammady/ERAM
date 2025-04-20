from odoo import api, fields, models


class PosProductsReportExcel(models.AbstractModel):
    _name = 'report.iet_employee_excel_report.employee_report_excel'
    _description = "Report iet_employee_excel_report"
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        sheet = workbook.add_worksheet('Employee Report Excel')

        # Define formats
        main_title = workbook.add_format({
            'font_size': 16,
            'border': True,
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'bg_color': '#008080',
            'font_color': 'white'
        })
        space_title = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'bg_color': 'white',
            'font_color': 'white'
        })
        header_format = workbook.add_format({
            'font_size': 14,
            'bottom': True,
            'right': True,
            'left': True,
            'valign': 'vcenter',
            'top': True,
            'align': 'center',
            'bg_color': '#008080',
            'font_color': 'white',
            'bold': True
        })
        line_format = workbook.add_format({
            'font_size': 12,
            'bottom': True,
            'right': True,
            'left': True,
            'valign': 'vcenter',
            'top': True,
            'align': 'center',
            'bg_color': 'white',
            'font_color': 'black',
            'bold': True
        })

        # Define merge range parameters
        start_row, end_row, start_col, end_col = 0, 3, 0, 11

        # Merge each row once (avoid overlapping merges)
        for r in range(start_row, end_row + 1):
            sheet.merge_range(r, start_col, r, end_col, "", space_title)

        # Move to next row after merged rows
        row = end_row + 1

        # Set column widths
        for col in range(0, 8):
            if col == 0:
                sheet.set_column(col, col, 10)
            elif col in [1, 2, 3, 7]:
                sheet.set_column(col, col, 30)
            else:
                sheet.set_column(col, col, 20)
        for col in range(8, 11):
            sheet.set_column(col, col, 40)

        # Set row height for main title row and merge cells for the title
        sheet.set_row(row, 25)
        sheet.merge_range(row, 0, row, 10, "Employee Report Excel", main_title)
        row += 1

        # Write header row
        sheet.set_row(row, 50)
        sheet.write(row, 0, "Count", header_format)
        sheet.write(row, 1, "Employee Name", header_format)
        sheet.write(row, 2, "Employee Number", header_format)
        sheet.write(row, 3, "Department", header_format)
        sheet.write(row, 4, "Contract", header_format)
        sheet.write(row, 5, "Contract Start", header_format)
        sheet.write(row, 6, "Contract End", header_format)
        sheet.write(row, 7, "Contract Change Days", header_format)
        sheet.write(row, 8, "Identification Number", header_format)
        sheet.write(row, 9, "Identification End", header_format)
        sheet.write(row, 10, "Identification Change Days", header_format)
        row += 1

        # Define domain for employees (example domain; adjust if needed)
        employee_domain = [('contract_id.state', '=', "open")]
        employee_ids = self.env['hr.employee'].search(employee_domain, order="id asc")
        print("@@@@@@@@@@@@@@@@@@@@", employee_ids)

        counter = 0
        for employee in employee_ids:
            contract = employee.contract_id
            counter += 1
            sheet.write(row, 0, counter, line_format)
            sheet.write(row, 1, employee.name, line_format)
            sheet.write(row, 2, employee.custom_employee_pin_number, line_format)
            sheet.write(row, 3, employee.department_id.name, line_format)
            sheet.write(row, 4, contract.name, line_format)
            sheet.write(row, 5, str(contract.date_start), line_format)
            sheet.write(row, 6, str(contract.date_end), line_format)
            today = fields.Date.today()
            change_days = str((contract.date_end - today).days) if contract.date_end else ""
            sheet.write(row, 7, change_days, line_format)
            sheet.write(row, 8, employee.identification_id, line_format)
            sheet.write(row, 9, str(employee.end_date_identification), line_format)
            identification_days = str(
                (employee.end_date_identification - today).days) if employee.end_date_identification else "0"
            sheet.write(row, 10, identification_days, line_format)
            row += 1
