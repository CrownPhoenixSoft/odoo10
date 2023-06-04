# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd. (<http://devintellecs.com>).
#
##############################################################################
from datetime import datetime
from openerp.osv import fields, osv
from openerp.report import report_sxw


class dev_emp_profile_report(report_sxw.rml_parse): 
    def __init__(self, cr, uid, name, context):
        super(dev_emp_profile_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({

         
        })
          
    
class dev_emp_profile_report_print(osv.AbstractModel):
    _name = 'report.dev_employee_profile.dev_emp_profile_report_template' 
    _inherit = 'report.abstract_report'
    _template = 'dev_employee_profile.dev_emp_profile_report_template'
    _wrapped_report_class = dev_emp_profile_report 

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


