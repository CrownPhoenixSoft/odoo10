# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api
from odoo import tools


# Extended name search is only used on some operators
ALLOWED_OPS = set(['ilike', 'like', '='])


@tools.ormcache(skiparg=0)
def _get_rec_names(self):
    "List of fields to search into"
    model = self.env['ir.model'].search(
        [('model', '=', str(self._name))])
    rec_name = [self._rec_name] or []
    other_names = model.name_search_ids.mapped('name')
    return rec_name + other_names


def _extend_name_results(self, domain, results, limit):
    result_count = len(results)
    if result_count < limit:
        domain += [('id', 'not in', [x[0] for x in results])]
        recs = self.search(domain, limit=limit - result_count)
        results.extend(recs.name_get())
    return results


class ModelExtended(models.Model):
    _inherit = 'ir.model'

    name_search_ids = fields.Many2many(
        'ir.model.fields', 'model_fields_table_rel', 'f_id', 'm_id',
        string='Name Search Fields')

    def _register_hook(self, ids=None):
        def make_name_search():
            @api.model
            def name_search(self, name='', args=None,
                            operator='ilike', limit=100):
                # Perform standard name search
                self.clear_caches()
                res = name_search.origin(
                    self, name=name, args=args, operator=operator, limit=limit)
                enabled = self.env.context.get('name_search_extended', True)
                # Perform extended name search
                # Note: Empty name causes error on
                #       Customer->More->Portal Access Management
                if name and enabled and operator in ALLOWED_OPS:
                    # Support a list of fields to search on
                    all_names = _get_rec_names(self)
                    base_domain = args or []
                    # Try regular search on each additional search field
                    for rec_name in all_names[1:]:
                        domain = [(rec_name, operator, name)]
                        res = _extend_name_results(
                            self, base_domain + domain, res, limit)
                    # Try ordered word search on each of the search fields
                    for rec_name in all_names:
                        domain = [(rec_name, operator, name.replace(' ', '%'))]
                        res = _extend_name_results(
                            self, base_domain + domain, res, limit)
                    # Try unordered word search on each of the search fields
                    for rec_name in all_names:
                        domain = [(rec_name, operator, x)
                                  for x in name.split() if x]
                        res = _extend_name_results(
                            self, base_domain + domain, res, limit)
                return res
            return name_search

        if ids is None:
            ids = self.search([]).ids
        for model in self.browse(ids):
            model_name = model.model
            Model = self.env[model_name]
            Model._patch_method('name_search', make_name_search())
        return super(ModelExtended, self)._register_hook()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: