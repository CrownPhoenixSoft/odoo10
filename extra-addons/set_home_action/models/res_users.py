from odoo import fields, models, api, _
from odoo.exceptions import Warning


class ResUsers(models.Model):
	_inherit = "res.users"

	@api.model
	def set_home_action(self, href):
		search_index = str(href).find('action')
		if search_index != -1:
			action = href.split('action=')
			self.env.user.sudo().write({
					'action_id': int(action[1]),
				})
		else:
			raise Warning(_("Menu Action Not found !"))
