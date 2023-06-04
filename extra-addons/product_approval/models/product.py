# -*- coding: utf-8 -*-
from odoo import models, fields, api
from lxml import etree
from odoo.osv.orm import setup_modifiers
from odoo.tools.safe_eval import safe_eval

class product_template(models.Model):
    _inherit = 'product.template'

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('refuse', 'Refuse')], string="Status", default='draft', track_visibility='always')
#    approved_by = fields.Many2one('res.users', 'By', track_visibility='always', default=lambda self: self.env.user)
#   if multi company is enabled, the res.user who modified before is not readable for logged in user to log message such as above, moreover its already mentioned who changed state field so track _visibility is indeed not needed.
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        args += [['state', '=', 'confirmed']]
        res = super(product_template, self).name_search(name, args=args, operator=operator, limit=limit)
        return res

    @api.model
    def create(self, vals):
        res = super(product_template, self).create(vals)
        if not self.env.user.has_group('product_approval.group_product_manager'):
            ctx = {}
            domain = []
            if res.company_id:
                domain.append(('company_id', '=', res.company_id.id))
            email_list = [user.email for user in self.env['res.users'].sudo().search(domain) if user.has_group('product_approval.group_product_manager')]
            if email_list:
                ctx['product_manager_email'] = ','.join([email for email in email_list if email])
                ctx['email_from'] = self.env.user.email
                ctx['user_name'] = self.env.user.name
                ctx['product_name'] = res.name

                template = self.env.ref('product_approval.product_approve_mail_template')
                base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                db = self.env.cr.dbname
                ctx['action_url'] = "{}/web?db={}#id={}&view_type=form&model=product.template".format(base_url, db, res.id)
                template.with_context(ctx).sudo().send_mail(self.id, force_send=True, raise_exception=False)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(product_template, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == "form":
            doc = etree.XML(result['arch'])
            for node in doc.iter(tag="field"):
                if 'readonly' in node.attrib.get("modifiers", ''):
                    attrs = node.attrib.get("attrs", '')
                    if 'readonly' in attrs:
                        attrs_dict = safe_eval(node.get('attrs'))
                        readonly_list = attrs_dict.get('readonly',)
                        if type(readonly_list) == list:
                            readonly_list.insert(0, ('state', '=', 'confirmed'))
                            if len(readonly_list) > 1:
                                readonly_list.insert(0, '|')
                        attrs_dict.update({'readonly': readonly_list})
                        node.set('attrs', str(attrs_dict))
                        setup_modifiers(node, result['fields'][node.get("name")])
                        continue
                    else:
                        continue
                node.set('attrs', "{'readonly':[('state','=','confirmed')]}")
                setup_modifiers(node, result['fields'][node.get("name")])
            result['arch'] = etree.tostring(doc)
        return result

    @api.multi
    def product_confirm(self):
        self.state = 'confirmed'
        self.approved_by = self.env.user.id

    @api.multi
    def product_refuse(self):
        self.state = 'refuse'
        self.approved_by = self.env.user.id

    @api.multi
    def reset_to_draft_product(self):
        self.state = 'draft'
        self.approved_by = self.env.user.id


class product_product(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        args += [['state', '=', 'confirmed']]
        res = super(product_product, self).name_search(name, args, operator, limit)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(product_product, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type == "form":
            doc = etree.XML(result['arch'])
            for node in doc.iter(tag="field"):
                if 'readonly' in node.attrib.get("modifiers", ''):
                    attrs = node.attrib.get("attrs", '')
                    if 'readonly' in attrs:
                        attrs_dict = safe_eval(node.get('attrs'))
                        readonly_list = attrs_dict.get('readonly',)
                        if type(readonly_list) == list:
                            readonly_list.insert(0, ('state', '=', 'confirmed'))
                            if len(readonly_list) > 1:
                                readonly_list.insert(0, '|')
                        attrs_dict.update({'readonly': readonly_list})
                        node.set('attrs', str(attrs_dict))
                        setup_modifiers(node, result['fields'][node.get("name")])
                        continue
                    else:
                        continue
                node.set('attrs', "{'readonly':[('state','=','confirmed')]}")
                if node.get("name") in result['fields']:
                    setup_modifiers(node, result['fields'][node.get("name")])
            result['arch'] = etree.tostring(doc)
        return result

    @api.multi
    def product_confirm(self):
        self.state = 'confirmed'
        self.approved_by = self.env.user.id

    @api.multi
    def product_refuse(self):
        self.state = 'refuse'
        self.approved_by = self.env.user.id

    @api.multi
    def reset_to_draft_product(self):
        self.state = 'draft'
        self.approved_by = self.env.user.id
