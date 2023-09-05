# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    

    @api.onchange("invoice_line_ids")
    def apply_discount(self):
        for rec in self:
            total = 0
            if rec.move_type == "out_refund":
                # rec['x_studio_total_discount'] = rec.x_studio_distributor_discount + rec.x_studio_sole_commission + rec.x_studio_cartage
                for line in rec.invoice_line_ids:
                    total += line.x_studio_total_discount
                rec['x_studio_total_discount'] = total
                
            elif self.move_type == "out_invoice":
                for line in rec.invoice_line_ids:
                    total += line.x_studio_total_discount
                rec['x_studio_total_discount'] = total

    @api.onchange("invoice_line_ids","x_studio_total_discount")
    def conpute_discount_on_journel_items(self):
        if self.move_type == "out_refund":
            list_item = []
            flag = False
            for rec in self:
                all_credit = 0
                for line in rec.line_ids:
                    all_credit += line.debit
                    already_exists = self.line_ids.filtered(lambda line: line.name and line.name.find('ABS Discount') == 0)
                        # raise UserError(str(receivable_account))

                    if already_exists:
                        receivable_account = self.line_ids.filtered(lambda line: line.account_id.user_type_id.name and line.account_id.user_type_id.name.find('Receivable') == 0)
                        if receivable_account:
                            total_amount_currency = sum(receivable_account.mapped('amount_currency'))
                            receivable_account.with_context(check_move_validity=False).update({
                                'amount_currency': total_amount_currency,
                                'credit': all_credit > 0.0 and all_credit or 0.0,
                                'debit': all_credit < 0.0 and -all_credit or 0.0,
                            })
                                
                        if line.account_id.user_type_id.name == "Receivable":
                            all_credit
                            # raise UserError(line.debit)
                        already_exists.with_context(check_move_validity=False).update({
                            'credit': rec.x_studio_total_discount > 0.0 and rec.x_studio_total_discount or 0.0,
                            'debit': rec.x_studio_total_discount < 0.0 and -rec.x_studio_total_discount or 0.0,
                            'amount_currency': rec.x_studio_total_discount > 0.0 and rec.x_studio_total_discount or 0.0,
                        })
                    
                        receivable_account.with_context(check_move_validity=False).update({
                                'credit': receivable_account.credit - already_exists.credit > 0.0 and receivable_account.credit - already_exists.credit or 0.0,
                                'debit': receivable_account.credit < 0.0 and receivable_account.credit or 0.0,
                                'amount_currency': receivable_account.credit - already_exists.credit > 0.0 and receivable_account.credit - already_exists.credit or 0.0,
                            })
                        if line.account_id.user_type_id.name == "Receivable":
                            line.with_context(check_move_validity=False)['credit'] -= already_exists.credit
                            # line.with_context(check_move_validity=False)['amounst_currency'] -= already_exists.debit
                            # raise UserError(line.with_context(check_move_validity=False)['debit'])


                    else:
                        list_item.append((0,0,{
                            'name': "ABS Discount",
                            'credit': rec.x_studio_total_discount,
                            'account_id': 960,
                            'exclude_from_invoice_tab': True,
                            'partner_id': rec.partner_id.id,
                        }))
                        flag = True
                        if line.account_id.user_type_id.name == "Receivable":
                            line.with_context(check_move_validity=False)['credit'] =line.with_context(check_move_validity=False)['credit'] - rec.x_studio_total_discount
                            line.with_context(check_move_validity=False)['amount_currency'] =line.with_context(check_move_validity=False)['amount_currency'] + rec.x_studio_total_discount
                        break
                        # raise UserError(str(aa))
                        
                if flag :
                    rec.with_context(check_move_validity=False).update({
                            'line_ids': list_item
                    })


        elif self.move_type == "out_invoice":
            list_item = []
            flag = False
            for rec in self:
                all_credit = 0
                for line in rec.line_ids:
                    all_credit += line.credit
                    already_exists = self.line_ids.filtered(lambda line: line.name and line.name.find('ABS Discount') == 0)
                        # raise UserError(str(receivable_account))

                    if already_exists:
                        receivable_account = self.line_ids.filtered(lambda line: line.account_id.user_type_id.name and line.account_id.user_type_id.name.find('Receivable') == 0)
                        if receivable_account:
                            total_amount_currency = sum(receivable_account.mapped('amount_currency'))
                            receivable_account.with_context(check_move_validity=False).update({
                                'amount_currency': -total_amount_currency,
                                'debit': all_credit > 0.0 and all_credit or 0.0,
                                'credit': all_credit < 0.0 and -all_credit or 0.0,
                            })
                                
                        if line.account_id.user_type_id.name == "Receivable":
                            all_credit
                            # raise UserError(line.debit)
                        already_exists.with_context(check_move_validity=False).update({
                            'debit': rec.x_studio_total_discount > 0.0 and rec.x_studio_total_discount or 0.0,
                            'credit': rec.x_studio_total_discount < 0.0 and -rec.x_studio_total_discount or 0.0,
                            'amount_currency': rec.x_studio_total_discount > 0.0 and rec.x_studio_total_discount or 0.0,
                        })
                    
                        receivable_account.with_context(check_move_validity=False).update({
                                'debit': receivable_account.debit - already_exists.debit > 0.0 and receivable_account.debit - already_exists.debit or 0.0,
                                'credit': receivable_account.debit < 0.0 and receivable_account.debit or 0.0,
                                'amount_currency': receivable_account.debit - already_exists.debit > 0.0 and receivable_account.debit - already_exists.debit or 0.0,
                            })
                        if line.account_id.user_type_id.name == "Receivable":
                            line.with_context(check_move_validity=False)['debit'] -= already_exists.debit
                            # line.with_context(check_move_validity=False)['amounst_currency'] -= already_exists.debit
                            # raise UserError(line.with_context(check_move_validity=False)['debit'])


                    else:
                        list_item.append((0,0,{
                            'name': "ABS Discount",
                            'debit': rec.x_studio_total_discount,
                            'account_id': 960,
                            'exclude_from_invoice_tab': True,
                            'partner_id': rec.partner_id.id,
                        }))
                        flag = True
                        if line.account_id.user_type_id.name == "Receivable":
                            line.with_context(check_move_validity=False)['debit'] =line.with_context(check_move_validity=False)['debit'] - rec.x_studio_total_discount
                            line.with_context(check_move_validity=False)['amount_currency'] =line.with_context(check_move_validity=False)['amount_currency'] + rec.x_studio_total_discount
                        break
                        # raise UserError(str(aa))
                        
                if flag :
                    rec.with_context(check_move_validity=False).update({
                            'line_ids': list_item
                    })
        

    
    
    def write(self,vals):

        result = super(AccountMove, self.with_context(check_move_validity=False, skip_account_move_synchronization=True, force_delete=True)).write(vals)
        # result = super(AccountMove, self).write(vals)
        for rec in self:
            if self.move_type == "out_refund":    
            # line_number = 1
                if rec.x_studio_custom_new_tax_1 > 0:
                    receivableCompute = False
                    for line in rec.line_ids:
                        # if line.x_studio_check == False:
                        if line.name:
                            # if line.name == 'GST 17 % Incl':
                            if line.name == 'GST 18 % Incl':
                                receivableCompute = True
                                line.with_context(check_move_validity=False)['debit'] = rec.x_studio_custom_new_only_tax
                                line.with_context(check_move_validity=False)['amount_currency'] = (rec.x_studio_custom_new_only_tax)*-1
                                # line['credit'] = rec.x_studio_custom_new_tax_1
                            # elif line.name == 'GST 18 % Incl':
                            #     receivableCompute = True
                            #     line.with_context(check_move_validity=False).credit = rec.x_studio_custom_new_only_tax
                            #     line.with_context(check_move_validity=False).amount_currency = (rec.x_studio_custom_new_only_tax)*-1
                            #     # line['credit'] = rec.x_studio_custom_new_tax_1
                            elif "Further" in line.name:
                                receivableCompute = True
                                # raise UserError("Asir")
                                line.with_context(check_move_validity=False)['debit'] = rec.x_studio_custom_new_further_tax
                                line.with_context(check_move_validity=False)['amount_currency'] = (rec.x_studio_custom_new_further_tax)*-1
                            # Bilal 
                            if receivableCompute:
                                receivable_account = self.line_ids.filtered(lambda line: line.account_id.user_type_id.name and line.account_id.user_type_id.name.find('Receivable') == 0)
                                # tax_17 = self.line_ids.filtered(lambda line: line.name and line.name.find('GST 17 % Incl') == 0)
                                total_tax = (rec.x_studio_total_discount * 0.17)
                                if receivable_account:
                                    receivable_account.with_context(check_move_validity=False)['credit'] = (rec.amount_untaxed - rec.x_studio_total_discount) + rec.x_studio_custom_new_tax_1#rec.x_studio_custom_new_only_tax  #receivable_account.with_context(check_move_validity=False)['debit'] - total_tax 
            elif self.move_type == "out_invoice":    
                if rec.x_studio_custom_new_tax_1 > 0:
                    receivableCompute = False
                    for line in rec.line_ids:
                        # if line.x_studio_check == False:
                        if line.name:
                            # if line.name == 'GST 17 % Incl':
                            if line.name == 'GST 18 % Incl':
                                receivableCompute = True
                                line.with_context(check_move_validity=False)['credit'] = rec.x_studio_custom_new_only_tax
                                line.with_context(check_move_validity=False)['amount_currency'] = (rec.x_studio_custom_new_only_tax)*-1
                                # line['credit'] = rec.x_studio_custom_new_tax_1
                            # elif line.name == 'GST 18 % Incl':
                            #     receivableCompute = True
                            #     line.with_context(check_move_validity=False).credit = rec.x_studio_custom_new_only_tax
                            #     line.with_context(check_move_validity=False).amount_currency = (rec.x_studio_custom_new_only_tax)*-1
                            #     # line['credit'] = rec.x_studio_custom_new_tax_1
                            elif line.name == 'GST 17 % Incl':
                                receivableCompute = True
                                line.with_context(check_move_validity=False)['credit'] = rec.x_studio_custom_new_only_tax
                                line.with_context(check_move_validity=False)['amount_currency'] = (rec.x_studio_custom_new_only_tax)*-1
                                # line['credit'] = rec.x_studio_custom_new_tax_1
                            # elif line.name == 'GST 18 % Incl':
                            #     receivableCompute = True
                            #     line.with_context(check_move_validity=False).credit = rec.x_studio_custom_new_only_tax
                            #     line.with_context(check_move_validity=False).amount_currency = (rec.x_studio_custom_new_only_tax)*-1
                            #     # line['credit'] = rec.x_studio_custom_new_tax_1
                            elif "Further" in line.name:
                                receivableCompute = True
                                # raise UserError("Asir")
                                line.with_context(check_move_validity=False)['credit'] = rec.x_studio_custom_new_further_tax
                                line.with_context(check_move_validity=False)['amount_currency'] = (rec.x_studio_custom_new_further_tax)*-1
                            # Bilal 
                            if receivableCompute:
                                receivable_account = self.line_ids.filtered(lambda line: line.account_id.user_type_id.name and line.account_id.user_type_id.name.find('Receivable') == 0)
                                # tax_17 = self.line_ids.filtered(lambda line: line.name and line.name.find('GST 17 % Incl') == 0)
                                total_tax = (rec.x_studio_total_discount * 0.17)
                                if receivable_account:
                                    receivable_account.with_context(check_move_validity=False)['debit'] = (rec.amount_untaxed - rec.x_studio_total_discount) + rec.x_studio_custom_new_tax_1#rec.x_studio_custom_new_only_tax  #receivable_account.with_context(check_move_validity=False)['debit'] - total_tax 

        return result   




class SaleOrder(models.Model):
    _inherit = 'sale.order'


    
    def update(self, vals):
        result = super(SaleOrder, self).update(vals)
        total_discount = 0
        for rec in self:
            for line in rec.order_line:
                total_discount += line.x_studio_total_discount
            rec['amount_total'] -= total_discount  
   
        return result
    
    @api.onchange("order_line")
    def compute_discount(self):
        total = 0
        for rec in self:
            for line in rec.order_line:
                total += line.x_studio_total_discount
            rec['x_studio_discount'] = total