from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    default_customer_id = fields.Many2one("res.partner", string="Default Customer",
        help="Select Customer to set as default customer in sale order.",
        domain=[('customer','=',True)])
    default_payment_journal_id = fields.Many2one("account.journal", string="Default Payment Journal",
        help="Select payment journal to set as default journal at registering payment.",
        domain=[('at_least_one_inbound', '=', True), ('type', 'in', ('bank', 'cash'))]) # 'at_least_one_inbound' is for customer invoice journal
    
    @api.multi
    def write(self,values):
    	self.SELF_WRITEABLE_FIELDS = ['signature', 'action_id', 'company_id', 'email', 'name', 'image', 'image_medium', 'image_small', 'lang', 'tz','default_payment_journal_id','default_customer_id']
    	res =super(ResUsers,self).write(values)
    	return res
