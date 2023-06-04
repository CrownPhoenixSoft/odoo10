
from odoo import models,api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def name_get(self):
        new_result = []
        if self.env.context.get("so_product_stock_inline"):
            res = super(ProductProduct, self).name_get()
            self = self.with_context(warehouse=self.env.context.get("warehouse"))
            availability = {r.id: [r.reception_count, r.qty_available] for r in self}
            precision = self.env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )
            new_res = []
            for _i in res:
                name = "{} ({:.{}f} )".format(
                    _i[1], availability[_i[0]][1], precision
                )
                new_res.append((_i[0], name))
            return new_res
        else:
            return super(ProductProduct, self).name_get()

