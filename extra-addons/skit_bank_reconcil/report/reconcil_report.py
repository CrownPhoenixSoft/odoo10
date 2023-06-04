# -*- coding: utf-8 -*-
from odoo import api, models, fields

    
class SkitBankReconcilReport(models.AbstractModel):
    _name = "report.skit_bank_reconcil.reconcil_report"
    
    
    
    
    
    

    @api.model
    def render_html(self, docids, data=None):
        
       
        
        report_obj = self.env['report']
        report =  report_obj._get_report_from_name('skit_bank_reconcil.reconcil_report')
         
       
       
        print("hhere --gett")
        data = data if data is not None else {}
        if(data.get('skit_report_type') == 'pdf'):
            journal_id = data.get('journal_id')
            date_from = data.get('date_from')
            date_to = data.get('date_to')
        else:
            journal_id = data['form']['journal_id'][0]
            date_from = data['form']['date_from']
            date_to = data['form']['date_to']
        journal = self.env['account.journal'].search([('id','=', journal_id)])
        last_bank_stmt = self.env['account.bank.statement'].search([('journal_id', '=', journal.id)], order="date desc, id desc", limit=1)
        last_balance = last_bank_stmt and last_bank_stmt[0].balance_end or 0
        
        gl_code = journal.default_debit_account_id.name
        default_debit_acc_id = journal.default_debit_account_id.id
        
        #Virtual GL Balance:
        account_ids = tuple(filter(None, [journal.default_debit_account_id.id, journal.default_credit_account_id.id]))
        amount_field = 'balance' if (not journal.currency_id or journal.currency_id == journal.company_id.currency_id) else 'amount_currency'
        current_balance = 0
        ids =str(account_ids)
        if account_ids:
            query = """SELECT sum("""+amount_field+""") FROM account_move_line WHERE account_id in """+(ids)
            list=[]
            list.append(account_ids)
            if date_from:
                date_frompara = "'"+date_from+"'"
                query = query+(""" AND date >="""+date_frompara)
                list.append(date_from)
            if date_to:
                date_toparam = "'"+date_to+"'"
                query=query+(""" AND date <=""" +date_toparam)
                list.append(date_to)
            self.env.cr.execute(query, [],)
            query_results = self.env.cr.dictfetchall()
            if query_results and query_results[0].get('sum') != None:
                current_balance = query_results[0].get('sum')
        self.env.cr.execute("""SELECT COALESCE(SUM(AMOUNT),0) 
                        FROM account_move am join account_move_line aml on aml.move_id = am.id where aml.statement_id 
                        IN (SELECT line.id 
                            FROM account_bank_statement_line AS line 
                            LEFT JOIN account_bank_statement AS st 
                            ON line.statement_id = st.id 
                            WHERE st.journal_id = %s and st.state = 'open')""", (journal.id,))
        already_reconciled = self.env.cr.fetchone()[0]
        self.env.cr.execute("""SELECT COALESCE(SUM(AMOUNT),0) 
                            FROM account_bank_statement_line AS line 
                            LEFT JOIN account_bank_statement AS st 
                            ON line.statement_id = st.id 
                            WHERE st.journal_id = %s and st.state = 'open'""", (journal.id,))
        all_lines = self.env.cr.fetchone()[0]
        virtual_gl_balance = all_lines - already_reconciled
        
        #Unreconciled Bank Statement Lines
        journal_id = str(journal.id)
        company_id = str(self.env.user.company_id.id)
        sql_query = """SELECT stl.id 
                        FROM account_bank_statement_line stl  \
                        where account_id IS NULL AND journal_id= """+journal_id+""" \
                        AND not exists (select 1 from account_move am join account_move_line aml on aml.move_id = am.id where am.statement_line_id  = stl.id) \
                        AND company_id= """+company_id
                    
        list=[]
        list.append({'journal_id':journal.id,'company_id' :self.env.user.company_id.id,})
        if date_from:
            date_fromparam = "'"+date_from+"'"
            sql_query = sql_query+(""" AND date::date >="""+date_fromparam)
            list.append(date_from)
        if date_to: 
            date_toparam = "'"+date_to+"'"
            sql_query=sql_query+(""" AND date::date <="""+date_toparam)
            list.append(date_to)
        sql_query += """ ORDER BY stl.id"""
        self.env.cr.execute(sql_query, [],)
        
        st_lines_left = self.env['account.bank.statement.line'].browse([line.get('id') for line in self.env.cr.dictfetchall()])
        
        
        #Validated Payments not linked with a Bank Statement Line
        domain_checks_to_print = [
                                  ('account_id', '=', default_debit_acc_id),
                                  ('full_reconcile_id','=', False), 
                                  ('statement_id','=',False),            
            
        ]
        if date_from:
            domain_checks_to_print.append(('date', '>=', date_from),)
        if date_to:
            domain_checks_to_print.append(('date', '<=', date_to),)
        pay_move_line = self.env['account.move.line'].search(domain_checks_to_print)
        
        payment_lines=[]
        for pay in pay_move_line:
                pay_dict = {}
                pay_dict['name']=pay.name
                pay_dict['payment_date']=pay.date
                pay_dict['ref']=pay.move_id.name
                pay_dict['amount']=pay.balance
            
                payment_lines.append(pay_dict)
        
        fleet_args= {
        'ids': [],
        'model': 'account.move.line',
        'docs': pay_move_line,
        'data':data,
        'current_balance':current_balance,
        'default_debit_acc_id':default_debit_acc_id,
        'gl_code':gl_code,
        'last_balance':last_balance,
        'payment_lines':payment_lines,
        'virtual_gl_balance': virtual_gl_balance,
        'st_lines_left':st_lines_left,
        'data': dict(
                data,
                journal= journal,
            ),
        }
       
       
       
       
       
        
         
      
          
        return report_obj.render('skit_bank_reconcil.reconcil_report', fleet_args)
    
      
  
        