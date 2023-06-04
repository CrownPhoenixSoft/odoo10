from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def default_get(self, fields):
        res = super(AccountPayment, self).default_get(fields)
        if self.env.user.default_payment_journal_id:
            res.update({
                'journal_id': self.env.user.default_payment_journal_id.id,
                })
        return res
