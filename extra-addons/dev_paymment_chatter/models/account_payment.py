# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://devintellecs.com>).
#
##############################################################################

from odoo import models, fields, api, _
import time
import datetime
from odoo.exceptions import ValidationError

class account_payment(models.Model):   
    
    _name = 'account.payment'
    _inherit = [
        'account.payment',
        'mail.thread'
    ]
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
    
