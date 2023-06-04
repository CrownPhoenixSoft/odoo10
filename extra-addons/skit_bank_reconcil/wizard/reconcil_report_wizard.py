# -*- coding: utf-8 -*-
from odoo import api, models, fields

    
class skit_reconcil_report(models.TransientModel):
    _name = "bank.reconcil.rep"
    
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    journal_id = fields.Many2one('account.journal',
                                    domain=[('type', '=', 'bank')],
                                    string='Journal',
                                    help="The accounting journal corresponding to this bank account.")
    @api.multi
    def print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        journal_id = self.journal_id.id
        date_from =self.date_from
        date_to =self.date_to
        datas = {
        'ids': active_ids,
        'model': 'account.payment',
        'form': self.read(),
        'journal_id':journal_id,
        'date_from':date_from,
        'date_to':date_to,
        'skit_report_type': 'pdf'
        }
        
        
        
        return self.env['report'].get_action(self, 'skit_bank_reconcil.reconcil_report',data=datas)
      
    
    
    
        

    def _build_contexts(self, data):
        result = {}
        result['date_from'] = 'date_from' in data['form'] and data['form']['date_from'] or False
        result['date_to'] = 'date_to' in data['form'] and data['form']['date_to'] or False
        result['journal_id'] = 'journal_id' in data['form'] and data['form']['journal_id'] or False
        return result
     
    



