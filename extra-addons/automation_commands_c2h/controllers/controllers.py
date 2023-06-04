# -*- coding: utf-8 -*-
# from odoo import http


# class AutomationCommandsC2h(http.Controller):
#     @http.route('/automation_commands_c2h/automation_commands_c2h/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/automation_commands_c2h/automation_commands_c2h/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('automation_commands_c2h.listing', {
#             'root': '/automation_commands_c2h/automation_commands_c2h',
#             'objects': http.request.env['automation_commands_c2h.automation_commands_c2h'].search([]),
#         })

#     @http.route('/automation_commands_c2h/automation_commands_c2h/objects/<model("automation_commands_c2h.automation_commands_c2h"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('automation_commands_c2h.object', {
#             'object': obj
#         })
