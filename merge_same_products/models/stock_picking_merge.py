from odoo import api, models
from odoo.exceptions import UserError, ValidationError

class StockPickingMerge(models.Model):
    _inherit = "stock.picking"

    
    def merge_picking(self):
        for record in self:
            product_qty_dict = {}
            product_name_dict = {}
            product_location_dict = {}
            product_location_dest_dict = {}
            lines_to_insert = []
            for line in record.move_ids_without_package:
                if product_qty_dict:
                    if line.product_id.id not in product_qty_dict.keys():
                        product_qty_dict[line.product_id.id] = line.product_uom_qty
                        product_name_dict[line.product_id.id] = line.name
                        product_location_dict[line.product_id.id] = line.location_id.id
                        product_location_dest_dict[line.product_id.id] = line.location_dest_id.id
                    else:
                        product_qty =  product_qty_dict[line.product_id.id]
                        product_qty += line.product_uom_qty
                        product_qty_dict[line.product_id.id] = product_qty
                else:
                    product_qty_dict[line.product_id.id] = line.product_uom_qty
                    product_name_dict[line.product_id.id] = line.name
                    product_location_dict[line.product_id.id] = line.location_id.id
                    product_location_dest_dict[line.product_id.id] = line.location_dest_id.id
                line.write({
                    'state':'draft',
                })
                line.unlink()
            for key in product_qty_dict.keys():
                lines_to_insert.append((0,0,{
                    'name': product_name_dict[key],
                    'location_id': product_location_dict[key],
                    'location_dest_id': product_location_dest_dict[key],
                    'product_id': key,
                    'product_uom_qty': product_qty_dict[key],
                    'product_uom': self.env['product.product'].search([('id','=',key)]).uom_id.id,
                    'picking_id': record.id,
                }))
            
            record.write({
                'move_ids_without_package': lines_to_insert
            })

    # def write(self,vals):
    #     product_list_ext = []
    #     product_list_new = []
    #     if "move_ids_without_package" in vals.keys():
    #         new_list = vals['move_ids_without_package']
    #         pro_list = []
    #         for att in new_list:
    #             if att[0] == 4:
    #                 s = self.move_ids_without_package.browse(att[1])
    #                 if s.product_id not in product_list_ext:
    #                     product_list_ext.append(s.product_id.id)
    #             if att[0] == 1:
    #                 s = self.move_ids_without_package.browse(att[1])
    #                 if s.product_id not in product_list_ext:
    #                     product_list_ext.append(s.product_id.id)
    #             if att[0] == 0:
    #                 if att[2]['product_id'] not in product_list_new:
    #                     product_list_new.append(att[2]['product_id'])
    #         raise UserError(product_list_new)
    #         for obj in product_list_new:
    #             pro_qty = 0
    #             if obj in product_list_ext:
    #                 for att in new_list:
    #                     if att[0] == 4:
    #                         o = self.move_ids_without_package.browse(att[1])
    #                         if o.product_id.id == obj:
    #                             pro_qty += o.product_uom_qty
    #                     if att[0] == 1:
    #                         o = self.move_ids_without_package.browse(att[1])
    #                         if o.product_id.id == obj:
    #                             pro_qty += att[2]['product_uom_qty']
    #                     if att[1] == 0:
    #                         if att[2]['product_id'] == obj:
    #                             pro_qty += att[2]['product_uom_qty']

    #                 for att1 in new_list:
    #                     if att1[0] == 4:
    #                         o = self.move_ids_without_package.browse(att1[1])
    #                         if o.product_id.id == obj:
    #                                 o.product_uom_qty = pro_qty
    #                                 o.product_uom_qty = pro_qty
    #                     if att1[0] == 1:
    #                         o = self.move_ids_without_package.browse(att1[1])
    #                         if o.product_id.id == obj:
    #                             att1[2]['product_uom_qty'] = pro_qty
    #                             o.product_uom_qty = pro_qty
    #         for obj1 in product_list_new:
    #             pro_qty = 0
    #             count = 0
    #             if obj1 not in product_list_ext:
    #                 for att1 in new_list:
    #                     if att1[0] == 0:
    #                         if att1[2]['product_id'] == obj1:
    #                             pro_qty += att1[2]['product_uom_qty']
    #                 for att2 in new_list:
    #                     if att2[0] == 0:
    #                         if att2[2]['product_id'] == obj1:
    #                             count += 1
    #                             if count == 1:
    #                                 att2[2]['product_uom_qty'] = pro_qty
    #                                 att2[2]['product_uos_qty'] = pro_qty
    #                                 pro_list.append(att2)

    #         for obj2 in product_list_ext:
    #             if obj2 not in product_list_new:
    #                 for att2 in new_list:
    #                     if att2[0] == 4:
    #                         o = self.move_ids_without_package.browse(att2[1])
    #                         if o.product_id.id == obj2:
    #                             pro_list.append(att2)
    #         for att3 in new_list:
    #             if att3[0] == 2:
    #                 pro_list.append(att3)
    #             if att3[0] == 1:
    #                 o = self.move_ids_without_package.browse(att3[1])
    #                 o.product_uom_qty = att3[2]['product_uom_qty']

    #         vals['move_ids_without_package'] = pro_list
    #     res = super(StockPickingMerge, self).write(vals)
    #     return res