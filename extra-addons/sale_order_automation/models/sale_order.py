from odoo import api, fields, models,exceptions
class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        imediate_obj=self.env['stock.immediate.transfer']
        res=super(SaleOrder,self).action_confirm()
        
        if self.state in ["sale","done"]:
            
            for order in self:
    
                warehouse=order.warehouse_id
#                 if warehouse.is_delivery_set_to_done and order.picking_ids: 
#                     for picking in self.picking_ids:
#                         picking.action_confirm()
#                         picking.action_assign()
#                         picking.force_assign()
#                         imediate_rec=imediate_obj.create({'pick_id':picking.id})
#                         imediate_rec.process()
    
#                 self._cr.commit()
    
                if warehouse.create_invoice and not order.invoice_ids:
                    order.action_invoice_create()  
    
                if  warehouse.validate_invoice and order.invoice_ids:
                    for invoice in order.invoice_ids:
                        invoice.action_invoice_open()
                
        return res  


     
     
    @api.multi
    def action_approve(self):
        
        imediate_obj=self.env['stock.immediate.transfer']
        res=super(SaleOrder,self).action_approve()
        
        for order in self:
    
                warehouse=order.warehouse_id
#                 if warehouse.is_delivery_set_to_done and order.picking_ids: 
#                     for picking in self.picking_ids:
#                         picking.action_confirm()
#                         picking.action_assign()
#                         picking.force_assign()
#                         imediate_rec=imediate_obj.create({'pick_id':picking.id})
#                         imediate_rec.process()
#     
#                 self._cr.commit()
    
                if warehouse.create_invoice and not order.invoice_ids:
                    order.action_invoice_create()  
    
                if  warehouse.validate_invoice and order.invoice_ids:
                    for invoice in order.invoice_ids:
                        invoice.action_invoice_open()
                        
                        
        
        
        return res
        
        
    
    
    