# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class hr_employee(models.Model):
    _inherit = 'hr.employee'
    
    leave_count = fields.Integer(compute='_leave_count', string="Total leave")    
    hr_employee_holidays_ids = fields.One2many('hr.holidays', 'employee_id', string ='Employee Leave')
    
    
    @api.depends('hr_employee_holidays_ids')
    def _leave_count(self):
        for each_leave in self:
            each_leave.leave_count = len(each_leave.hr_employee_holidays_ids)
            
    @api.multi
    def show_request_leave(self):
        action = self.env.ref('hr_leave_form_button.open_company_allocation_leave_from_button').read()[0]
        leave = self.mapped('hr_employee_holidays_ids')
        if len(leave) > 1:
            action['domain'] = [('id', 'in', leave.ids)]
        elif leave:
            action['views'] = [(self.env.ref('hr_holidays.edit_holiday_new').id, 'form')]
            action['res_id'] = leave.id
        return action


    
