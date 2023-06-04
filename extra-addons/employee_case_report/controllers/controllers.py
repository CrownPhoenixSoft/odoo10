# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeCaseReport(http.Controller):
#     @http.route('/employee_case_report/employee_case_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_case_report/employee_case_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_case_report.listing', {
#             'root': '/employee_case_report/employee_case_report',
#             'objects': http.request.env['employee_case_report.employee_case_report'].search([]),
#         })

#     @http.route('/employee_case_report/employee_case_report/objects/<model("employee_case_report.employee_case_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_case_report.object', {
#             'object': obj
#         })
