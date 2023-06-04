# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api


class EmployeeCaseReportView(models.AbstractModel):
    _name = 'report.employee_case_report.report_employee_case'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        employee_case_report = self.env['employee_case_report.employee_case_report'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'docs': employee_case_report,
        }
        return report_obj.render('employee_case_report.report_employee_case', docargs)
