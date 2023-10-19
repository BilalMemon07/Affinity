from odoo import models, fields, api,Command
from odoo.exceptions import UserError
from odoo.tools import config, human_size, ImageProcess, str2bool, consteq
import base64
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime


class MRP_Production(models.Model):
    _inherit = 'mrp.production'
    
    def send_for_plm(self):
        for rec in self:
            obj = {
                "name": str(rec.name) + ' - ' + str(rec.pj_number.name),
                "product_tmpl_id": rec.product_id.product_tmpl_id.id,
                "bom_id":rec.bom_id.id,
                "type_id" :1,
                "type":'bom',
                "effectivity":'asap',
                "stage_id":1
            }
            self.env['mrp.eco'].create(obj)





    def set_child_mo_to_draft(self, parent_mo):
        child_mos = self.env['mrp.production'].search([('origin','=',parent_mo)])
        if child_mos:
            for child_mo in child_mos:
                # child_mo['state'] = 'draft'
                # self.set_child_mo_to_draft(child_mo.name)
                for line in child_mo.move_raw_ids:
                    # if line.state == 'waiting':
                    line['state'] = 'draft'
                for line2 in child_mo.move_finished_ids:
                    # if line2.state == 'waiting':
                    line2['state'] = 'draft'
                for line3 in child_mo.move_byproduct_ids:
                    # if line3.state == 'waiting':
                    line3['state'] = 'draft'
                for line4 in child_mo.move_dest_ids:
                    # if line4.state == 'waiting':
                    line4['state'] = 'draft'
                for line5 in child_mo.finished_move_line_ids:
                    # if line5.state == 'waiting':
                    line5['state'] = 'draft'
                transfer = self.env['stock.picking'].search([('origin','=',child_mo.name)])
                for tran in transfer:
                    if tran.state not in ('cancel','done'):
                        tran['state'] = 'draft'
                        for line1 in tran.move_ids_without_package:
                            line1['state'] = 'draft'
                        for line2 in tran.move_line_ids_without_package:
                            line2['state'] = 'draft'
                        tran['state'] = 'cancel'
                        tran.unlink()
            
        

        for rec in self:
            if rec.origin:
                sale_order = self.env['sale.order'].search([('name','=',rec.origin)])
                if sale_order:
                    if rec:
                    #   rec['state'] = 'draft'
                        # self.set_child_mo_to_draft(rec.name)
                        for line in rec.move_raw_ids:
                        # if line.state == 'waiting':
                            line['state'] = 'draft'
                        for line2 in rec.move_finished_ids:
                        # if line2.state == 'waiting':
                            line2['state'] = 'draft'
                        for line3 in rec.move_byproduct_ids:
                        # if line3.state == 'waiting':
                            line3['state'] = 'draft'
                        for line4 in rec.move_dest_ids:
                        # if line4.state == 'waiting':
                            line4['state'] = 'draft'
                        for line5 in rec.finished_move_line_ids:
                        # if line5.state == 'waiting':
                            line5['state'] = 'draft'
                        transfer = self.env['stock.picking'].search([('origin','=',rec.name)])
                        for tran in transfer:
                            if tran.state not in ('cancel','done'):
                                tran['state'] = 'draft'
                                for line1 in tran.move_ids_without_package:
                                    line1['state'] = 'draft'
                                for line2 in tran.move_line_ids_without_package:
                                    line2['state'] = 'draft'
                                    tran['state'] = 'cancel'
                                    tran.unlink()
        
    
class MRP_ECO(models.Model):
    _inherit = 'mrp.eco'
    
    def action_apply(self):
        res = super(MRP_ECO, self).action_apply()
        if self.new_bom_id:
            self.new_bom_id['code'] = str(self.name).split(': ')[1]
            name = str(self.name).split(': ')[1].split(' -')[0]
            # raise UserError(name)
            mo_search = self.env['mrp.production'].search([("bom_id", '=', self.bom_id.id),('name' ,'=', name)])            
            mo_search.set_child_mo_to_draft(mo_search.name)
            mo_search['state'] = 'draft'
            mo_search['bom_id'] = False
            if not  mo_search.bom_id:
                mo_search['bom_id'] = self.new_bom_id.id
           
        return res
           

