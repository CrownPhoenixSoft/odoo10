from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        if self.env.user.default_customer_id:
            res.update({
                'partner_id': self.env.user.default_customer_id.id,
                })
        return res