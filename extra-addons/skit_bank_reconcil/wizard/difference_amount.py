# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.tools.misc import formatLang


class account_journal(models.Model):
    _inherit = 'account.journal'
        
    
    @api.multi
    def get_journal_dashboard_datas(self):
        currency = self.currency_id or self.company_id.currency_id
        val = super(account_journal, self).get_journal_dashboard_datas()
        if val['difference'] is False:
            val['difference'] = formatLang(self.env, 0, currency_obj=currency)
        return val
    
        
    @api.multi
    def print_report(self):
        
        return {
            'type': 'ir.actions.act_window',
            'name':'Bank Reconciliation',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bank.reconcil.rep',
            'view_id': self.env.ref('skit_bank_reconcil.view_bank_reconciliation_diff').id,
            'context': {'default_journal_id': self.id,
                        },
            'create': False,
            'target': 'new',
        }
        
         
