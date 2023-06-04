# -*- coding: utf-8 -*-
# Â© 20118 Eficent Business and IT Consulting Services S.L. (www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models
from datetime import datetime, timedelta
from odoo.osv import expression

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def get_move_lines_for_reconciliation(
            self, excluded_ids=None, str=False, offset=0, limit=None,
            additional_domain=None, overlook_partner=False):
        
        
        
        # Blue lines = payment on bank account not assigned to a statement yet
        reconciliation_aml_accounts = [self.journal_id.default_credit_account_id.id, self.journal_id.default_debit_account_id.id]
      
        domain_reconciliation = ['&',('statement_id', '=', False), ('account_id', 'in', reconciliation_aml_accounts)]
        # Black lines = unreconciled & (not linked to a payment or open balance created by statement
        domain_matching = [('reconciled', '=', False)]
        if self.partner_id.id or overlook_partner:
            domain_matching = expression.AND([domain_matching, [('account_id.internal_type', 'in', ['payable', 'receivable'])]])
        else:
            # TODO : find out what use case this permits (match a check payment, registered on a journal whose account type is other instead of liquidity)
            domain_matching = expression.AND([domain_matching, [('account_id.reconcile', '=', True)]])

        # Let's add what applies to both
        domain = expression.OR([domain_reconciliation, domain_matching])
        if self.partner_id.id and not overlook_partner:
            domain = expression.AND([domain, [('partner_id', '=', self.partner_id.id)]])

        # Domain factorized for all reconciliation use cases
        ctx = dict(self._context or {})
        ctx['bank_statement_line'] = self
        generic_domain = self.env['account.move.line'].with_context(ctx).domain_move_lines_for_reconciliation(excluded_ids=excluded_ids, str=str)
        domain = expression.AND([domain, generic_domain])

        # Domain from caller
        if additional_domain is None:
            additional_domain = []
        else:
            additional_domain = expression.normalize_domain(additional_domain)
        domain = expression.AND([domain, additional_domain])

        return self.env['account.move.line'].search(domain, offset=offset, limit=limit, order="date_maturity desc, id desc")
        
    
    
    
    
    
    
    
    
    
    
    
