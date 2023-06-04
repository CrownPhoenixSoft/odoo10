from odoo import fields, models, api, _
from odoo.exceptions import Warning


class account_register_payments(models.TransientModel):
    _inherit = "account.register.payments"

    @api.multi
    def validate_and_print(self):
        payment = self.env['account.payment'].create(self.get_payment_vals())
        payment.post()
        return self.env['report'].get_action(self._get_invoices(), 'professional_templates.report_invoice')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def pay_and_print(self):
        journal_id = self.env.user.default_payment_journal_id
        if journal_id:
            payment_values = self.env['account.register.payments'].with_context(active_ids=self.ids,active_model='account.invoice').default_get([])
            payment_method = payment_values.get('payment_type') == 'inbound' and journal_id.inbound_payment_method_ids.ids or journal_id.outbound_payment_method_ids.ids
            payment_values.update({
                'journal_id': journal_id.id,
                'payment_method_id': payment_method[0],
                })
            payment_id = self.env['account.register.payments'].with_context(active_ids=self.ids,active_model='account.invoice').create(payment_values)
            payment_id.create_payment()
            return self.env['report'].get_action(self.id, 'professional_templates.report_invoice')
        else:
            raise Warning(_("Default Journal is not set in user's preferences."))
