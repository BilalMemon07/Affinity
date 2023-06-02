from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from dateutil.relativedelta import relativedelta


class AccountMove(models.Model):
    _inherit = 'account.move'

    def apply_intrest_calculation(self):
        final_list = []
        
        
        intrest = 0 
        for line in self.invoice_line_ids:
            if line.product_id.id == 4:
                intrest = line.price_unit
        start_date = self.invoice_date
        end_date = self.invoice_date_due


        tenor = end_date - start_date
        final_date = str(tenor).split(" ")[0]
        tenor = float(final_date) + 1
        res  = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month + 1) 

        intrest_per_day = intrest / (tenor - 1)
        print(tenor - 1)
        print(intrest_per_day)

        print(type(start_date.month))
        count = 1
        sum_of_31_days = 0
        sum_of_30_days = 0
        sum_of_28_days = 0
        sum_of_29_days = 0
        total_of_intrest = 0.0

        for x in range(res):
            date_after_month = start_date + relativedelta(months=x)
            
            # print(date_after_month)
            sum_of_30_days_2 = 0
            sum_of_30_days_1 = 0
            sum_of_30_days_3 = 0
            if date_after_month.month in [4,6,9,11]:
                
                if date_after_month.month != end_date.month:

                    if count == 1:
                        print('1')
                        remaining_days = 30 - start_date.day 
                        print("Intrest for month " + str(date_after_month) +" "+ str(remaining_days) +" "+ str(round(remaining_days * intrest_per_day)))
                        final_list.append((0,0,{
                            "intrest_of_month":str(date_after_month.strftime("%B")),
                            "intrest_of_year": str(date_after_month.year),
                            "date": date_after_month,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                        count = 2
                        # sum_of_30_days_1 = sum_of_30_days_1 + remaining_days * intrest_per_day
                        # print("count" + str(count))
                        
                    else:

                        print("else")
                        change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                        remaining_days = 31 - (change_day.day)
                        final_list.append((0,0,{
                            "intrest_of_month":str(change_day.strftime("%B")),
                            "intrest_of_year": str(change_day.year),
                            "date": change_day,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                        print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                        # sum_of_30_days_2 = sum_of_30_days_2 + remaining_days * intrest_per_day
                else:
                    if date_after_month.month != end_date.month:
                        print('2')
                        
                        change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                        remaining_days = 31 - (end_date.day) 
                        print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                        final_list.append((0,0,{
                            "intrest_of_month":str(change_day.strftime("%B")),
                            "intrest_of_year": str(change_day.year),
                            "date": change_day,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                    else:
                        change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                        remaining_days =  (end_date.day) - (date_after_month.day)
                        print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                        final_list.append((0,0,{
                            "intrest_of_month":str(change_day.strftime("%B")),
                            "intrest_of_year": str(change_day.year),
                            "date": change_day,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                        print("start = end")
                    # sum_of_30_days_3 = sum_of_30_days_3 + remaining_days * intrest_per_day
                # sum_of_30_days = sum_of_30_days_1 + sum_of_30_days_2 + sum_of_30_days_3

                # date_after_month = start_date + relativedelta(months=1)
                # print(date_after_month) 
            

            elif date_after_month.month in [2]:
                sum_of_28_days_2 = 0
                sum_of_28_days_1 = 0
                sum_of_28_days_3 = 0
                
                if (date_after_month.year % 4) != 0:
                    if count == 1:
                        remaining_days = 29 - start_date.day 
                        print("Intrest for month " + str(date_after_month) +" "+ str(remaining_days) +" "+ str(round(remaining_days * intrest_per_day)))
                        count = 2
                        # sum_of_28_days_1 = sum_of_28_days_1 + remaining_days * intrest_per_day
                        final_list.append((0,0,{
                            "intrest_of_month":str(date_after_month.strftime("%B")),
                            "intrest_of_year": str(date_after_month.year),
                            "date": date_after_month,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                    else:
                        if date_after_month.month != end_date.month:
                            change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                            remaining_days = 29 - (change_day.day) 
                            final_list.append((0,0,{
                                "intrest_of_month":str(change_day.strftime("%B")),
                                "intrest_of_year": str(change_day.year),
                                "date": change_day,
                                "no_of_days": str(remaining_days),
                                "intrest_of_this_month":round(remaining_days * intrest_per_day)
                            }))
                            print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                            # sum_of_28_days_2 = sum_of_28_days_2 + remaining_days * intrest_per_day
                        else:
                            change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                            remaining_days = 29 - (end_date.day)
                            final_list.append((0,0,{
                                "intrest_of_month":str(change_day.strftime("%B")),
                                "intrest_of_year": str(change_day.year),
                                "date": change_day,
                                "no_of_days": str(remaining_days),
                                "intrest_of_this_month":round(remaining_days * intrest_per_day)
                            }))
                            print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                            # sum_of_28_days_3 = sum_of_28_days_3 + remaining_days * intrest_per_day
                    # sum_of_28_days = sum_of_28_days_1 + sum_of_28_days_2 + sum_of_28_days_3
                else:
                    sum_of_29_days_2 = 0
                    sum_of_29_days_1 = 0
                    sum_of_29_days_3 = 0
                    if count == 1:
                        print("1")
                        remaining_days = 30 - start_date.day
                        final_list.append((0,0,{
                                "intrest_of_month":str(date_after_month.strftime("%B")),
                                "intrest_of_year": str(date_after_month.year),
                                "date": date_after_month,
                                "no_of_days": str(remaining_days),
                                "intrest_of_this_month":round(remaining_days * intrest_per_day)
                            }))
                        print("Intrest for month " + str(date_after_month) +" "+ str(remaining_days) +" "+ str(round(remaining_days * intrest_per_day)))
                        count = 2
                        # sum_of_29_days_1 = sum_of_29_days_1 + remaining_days * intrest_per_day
                        
                    else:
                        if date_after_month.month != end_date.month:
                            print("2")
                            change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                            remaining_days = 30 - (change_day.day)
                            final_list.append((0,0,{
                                "intrest_of_month":str(change_day.strftime("%B")),
                                "intrest_of_year": str(change_day.year),
                                "date": change_day,
                                "no_of_days": str(remaining_days),
                                "intrest_of_this_month":round(remaining_days * intrest_per_day)
                            }))
                            print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                            # sum_of_29_days_2 = sum_of_29_days_2 + remaining_days * intrest_per_day
                        else:
                            print("3")
                            change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                            remaining_days = (end_date.day)
                            final_list.append((0,0,{
                                "intrest_of_month":str(change_day.strftime("%B")),
                                "intrest_of_year": str(change_day.year),
                                "date": change_day,
                                "no_of_days": str(remaining_days),
                                "intrest_of_this_month":round(remaining_days * intrest_per_day)
                            }))
                            print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                            # sum_of_29_days_3 = sum_of_29_days_3 + remaining_days * intrest_per_day
                
                # sum_of_29_days = sum_of_29_days_1 + sum_of_29_days_2 + sum_of_29_days_3

            elif date_after_month.month in [1,3,5,7,8,10,12]:
                
                sum_of_30_days_2 = 0
                sum_of_30_days_1 = 0
                sum_of_30_days_3 = 0

                if count == 1:
                    print("1")
                    remaining_days = 32 - start_date.day 
                    final_list.append((0,0,{
                        "intrest_of_month":str(date_after_month.strftime("%B")),
                        "intrest_of_year": str(date_after_month.year),
                        "date": date_after_month,
                        "no_of_days": str(remaining_days),
                        "intrest_of_this_month":round(remaining_days * intrest_per_day)
                    }))
                    print("Intrest for month " + str(date_after_month) +" "+ str(remaining_days) +" "+ str(round(remaining_days * intrest_per_day)))
                    count = 2
                    # sum_of_30_days_1 = sum_of_30_days_1 + remaining_days * intrest_per_day
                    
                else:
                    print("2")
                    if date_after_month.month != end_date.month:
                        print("3")
                        change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                        remaining_days = 32 - (change_day.day) 
                        final_list.append((0,0,{
                            "intrest_of_month":str(change_day.strftime("%B")),
                            "intrest_of_year": str(change_day.year),
                            "date": change_day,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                        print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day)))
                        # sum_of_30_days_2 = sum_of_30_days_2 + remaining_days * intrest_per_day
                    else:
                        print("4")
                        change_day = date_after_month + relativedelta(days= (date_after_month.day * -1) + 1)
                        remaining_days =  (end_date.day) 
                        final_list.append((0,0,{
                            "intrest_of_month":str(change_day.strftime("%B")),
                            "intrest_of_year": str(change_day.year),
                            "date": change_day,
                            "no_of_days": str(remaining_days),
                            "intrest_of_this_month":round(remaining_days * intrest_per_day)
                        }))
                        print("Intrest for month " + str(change_day) +" "+ str(remaining_days)  +" "+ str(round(remaining_days * intrest_per_day) ))
                        # sum_of_30_days_3 = sum_of_30_days_3 + remaining_days * intrest_per_day
                
                # sum_of_30_days = sum_of_30_days_1 + sum_of_30_days_2 + sum_of_30_days_3
        self.write({
            'intrest_calculator_id':final_list
        })
        # raise UserError(str(final_list))
        # total_of_intrest = sum_of_30_days + sum_of_31_days + sum_of_29_days + 