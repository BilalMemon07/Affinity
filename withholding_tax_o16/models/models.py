from odoo import api, fields, models, _,Command
from odoo.exceptions import UserError
from odoo.addons.account.models.account_payment import AccountPayment as AP

class AccountTax(models.Model):
    _inherit = "account.tax"

    is_withholding = fields.Boolean("Is Withholding Tax", default=False)
    is_service_withholding = fields.Boolean("Is Service Withholding Tax", default=False)

class AccountPayment(models.Model):
    _inherit = "account.payment"

    paid_to = fields.Monetary(string='Paid to', store=True, readonly=True, compute='_compute_paid_to_amount')
    tax_code = fields.Many2one('account.tax', string='Tax Code', domain=[('is_withholding', '=', True)])
    tax_account = fields.Many2one('account.account', string='Tax Account', readonly=True)
    tax_perc = fields.Float(string='Tax %', readonly=True)
    tax_amount = fields.Float(string='Tax Amount', readonly=True)
    total_amount = fields.Float(string='Total Amount', readonly=True)
    # service Tax
    amount_to_withhold_service = fields.Float(string="Amount to Withhold")
    paid_to_service = fields.Monetary(string='Paid to', store=True, readonly=True, compute='_compute_paid_to_amount')
    tax_code_service = fields.Many2one('account.tax', string='Tax Code', domain=[('is_service_withholding', '=', True)])
    tax_account_service = fields.Many2one('account.account', string='Tax Account', readonly=True)
    tax_perc_service = fields.Float(string='Tax %', readonly=True)
    tax_amount_service = fields.Float(string='Tax Amount', readonly=True)
    total_amount_service = fields.Float(string='Total Amount', readonly=True)


    @api.onchange('tax_code')
    def _compute_tax_fields(self):
        for record in self:
            for data in record.tax_code.invoice_repartition_line_ids:
                record.tax_account = data.account_id.id
                record.tax_perc = 	record.tax_code.amount
                record.tax_amount = round(record.amount * (record.tax_perc / 100))
                record.total_amount = round(record.amount - record.tax_amount)
                # record.paid_to = record.amount + record.tax_amount

        for dat in record.tax_code_service.invoice_repartition_line_ids:
            if self.amount_to_withhold_service:
                record.tax_account_service = dat.account_id.id
                record.tax_perc_service = 	record.tax_code_service.amount
                record.tax_amount_service = round(record.amount_to_withhold_service * (record.tax_perc_service / 100))
                record.total_amount_service = round(record.amount_to_withhold_service - record.tax_amount_service)

    @api.onchange('amount')
    def _onchange_amounts(self):
        for record in self:
            record.tax_code = False
            record.tax_account = False
            record.tax_perc = 	False
            record.tax_amount = False
            record.total_amount = False
            # record.paid_to = False

            record.tax_code_service = False
            record.tax_account_service = False
            record.tax_perc_service = 	False
            record.tax_amount_service = False
            record.total_amount_service = False
    
    @api.depends('amount')
    def _compute_paid_to_amount(self):
        for record in self:
            record.paid_to = record.amount + record.tax_amount + record.tax_amount_service

    #Withholding methods
    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the temporary liquidity account.
        - The lines using the counterpart account.
        - The lines being the write-off lines.
        :return: (liquidity_lines, counterpart_lines, writeoff_lines)
        '''
        self.ensure_one()

        liquidity_lines = self.env['account.move.line']
        counterpart_lines = self.env['account.move.line']
        writeoff_lines = self.env['account.move.line']
        #withholding
        wth_lines = self.env['account.move.line']
        
        ser_wht_line = self.env['account.move.line']


        for line in self.move_id.line_ids:
            if line.account_id in self._get_valid_liquidity_accounts():
                liquidity_lines += line
            elif line.account_id.account_type in ('asset_receivable', 'liability_payable') or line.partner_id == line.company_id.partner_id:
                counterpart_lines += line
            #withholding
            elif line.account_id.id == self.tax_account.id:
                wth_lines += line
            # service 
            elif line.account_id.id == self.tax_account_service.id:
                ser_wht_line += line
            else:
                writeoff_lines += line

        #withholding
        return liquidity_lines, counterpart_lines, writeoff_lines, wth_lines,ser_wht_line
    
    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        ''' Prepare the dictionary to create the default account.move.lines for the current payment.
        :param write_off_line_vals: Optional dictionary to create a write-off account.move.line easily containing:
            * amount:       The amount to be added to the counterpart amount.
            * name:         The label to set on the line.
            * account_id:   The account on which create the write-off.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        '''
        self.ensure_one()
        write_off_line_vals = write_off_line_vals or {}

        if not self.outstanding_account_id:
            raise UserError(_(
                "You can't create a new payment without an outstanding payments/receipts account set either on the company or the %s payment method in the %s journal.",
                self.payment_method_line_id.name, self.journal_id.display_name))

        # Compute amounts.
        write_off_line_vals_list = write_off_line_vals or []
        write_off_amount_currency = sum(x['amount_currency'] for x in write_off_line_vals_list)
        write_off_balance = sum(x['balance'] for x in write_off_line_vals_list)

        #withholding
        if self.payment_type == 'inbound':
            counterpart_amount = -self.amount
            # Receive money.
            liquidity_amount_currency = self.amount
        elif self.payment_type == 'outbound':
            counterpart_amount = self.amount
            # Send money.
            liquidity_amount_currency = -self.amount
        else:
            liquidity_amount_currency = counterpart_amount = 0.0

        liquidity_balance = self.currency_id._convert(
            liquidity_amount_currency,
            self.company_id.currency_id,
            self.company_id,
            self.date,
        )
        counterpart_amount_currency = -liquidity_amount_currency - write_off_amount_currency
        counterpart_balance = -liquidity_balance - write_off_balance
        currency_id = self.currency_id.id

        # Compute a default label to set on the journal items.
        liquidity_line_name = ''.join(x[1] for x in self._get_liquidity_aml_display_name_list())
        counterpart_line_name = ''.join(x[1] for x in self._get_counterpart_aml_display_name_list())

        balance = self.currency_id._convert(counterpart_amount, self.company_id.currency_id, self.company_id, self.date)

        #Asir withholding
        payment_debit_account_id = 0
        payment_credit_account_id = 0
        for record in self:
            method_line = self.env['account.payment.method.line'].search([('id','=',record.payment_method_line_id.id)])
            payment_method_id = method_line.payment_method_id.id
            for line in record.journal_id.inbound_payment_method_line_ids:
                if line.payment_method_id.id == payment_method_id:
                    payment_debit_account_id = line.payment_account_id.id
                    break
                    
            for line in record.journal_id.outbound_payment_method_line_ids:
                if line.payment_method_id.id == payment_method_id:
                    payment_credit_account_id = line.payment_account_id.id
                    break
        
        #Asir withholding
        line_vals_list = []
        if self.partner_type == 'supplier':
            # raise UserError('1')
        # Payment to Supplier with WTH Tax.
            line_vals_list = [
                # Liquidity line.
                {
                    'name': liquidity_line_name,
                    'date_maturity': self.date,
                    'amount_currency': liquidity_amount_currency + (self.tax_amount + self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                    'credit': -liquidity_balance + (self.tax_amount + self.tax_amount_service) if liquidity_balance < 0.0 else 0.0,
                    # 'debit': balance < 0.0 and -balance or 0.0,
                    # 'credit': balance - (self.tax_amount) > 0.0 and balance - (self.tax_amount) or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.outstanding_account_id.id,
                    # 'account_id': payment_debit_account_id if balance < 0.0 else payment_credit_account_id,
                },
                # Receivable / Payable.
                {
                    'name': counterpart_line_name,
                    'date_maturity': self.date,
                    'amount_currency': counterpart_amount_currency,
                    'currency_id': currency_id,
                    'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
                    'credit': -counterpart_balance if counterpart_balance < 0.0 else 0.0,
                    # 'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                    # 'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                },
            ]

        elif self.partner_type == 'customer' and self.payment_type == 'outbound':
            # raise UserError('2')
        # Payment to Customer with WTH Tax.
            line_vals_list = [
                # Liquidity line.
                {
                    'name': liquidity_line_name,
                    'date_maturity': self.date,
                    'amount_currency': liquidity_amount_currency + (self.tax_amount + self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                    'credit': -liquidity_balance + (self.tax_amount + self.tax_amount_service) if liquidity_balance < 0.0 else 0.0,
                    # 'debit': balance < 0.0 and -balance or 0.0,
                    # 'credit': balance - (self.tax_amount) > 0.0 and balance - (self.tax_amount) or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.outstanding_account_id.id,
                    # 'account_id': payment_debit_account_id if balance < 0.0 else payment_credit_account_id,
                },
                # Receivable / Payable.
                {
                    'name': counterpart_line_name,
                    'date_maturity': self.date,
                    'amount_currency': counterpart_amount_currency,
                    'currency_id': currency_id,
                    'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
                    'credit': -counterpart_balance if counterpart_balance < 0.0 else 0.0,
                    # 'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                    # 'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                },
            ]
        
        else:
            # raise UserError('3')
            # Payment from Customer with WTH Tax
            line_vals_list = [
                # Liquidity line.
                {
                    'name': liquidity_line_name,
                    'date_maturity': self.date,
                    'amount_currency': liquidity_amount_currency-(self.tax_amount + self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                    'credit': -liquidity_balance + (self.tax_amount + self.tax_amount_service) if liquidity_balance < 0.0 else 0.0,
                    # 'debit': balance+(self.tax_amount) < 0.0 and -balance-(self.tax_amount) or 0.0,
                    # 'credit': balance > 0.0 and balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.outstanding_account_id.id,
                    # 'account_id': payment_debit_account_id if balance < 0.0 else payment_credit_account_id,
                },
                # Receivable / Payable.
                {
                    'name': counterpart_line_name,
                    'date_maturity': self.date,
                    'amount_currency': counterpart_amount_currency,
                    'currency_id': currency_id,
                    'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
                    'credit': -counterpart_balance if counterpart_balance < 0.0 else 0.0,
                    # 'debit': balance + write_off_balance  > 0.0 and balance + write_off_balance or 0.0,
                    # 'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                },
            ]
        
        if self.tax_amount:
            # Supplier WTH Tax condition
            if self.partner_type == 'supplier':
                # raise UserError('1')
                balance1 = self.currency_id._convert(self.tax_amount, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': 'Withholding Tax',
                    'amount_currency': -(self.tax_amount),
                    'currency_id': currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': (self.tax_amount),
                    'date_maturity': self.date,
                    'partner_id': self.partner_id.commercial_partner_id.id,
                    'account_id': self.tax_account.id,
                    'payment_id': self.id,
                })
            # Payment to Customer with Tax condition
            elif self.partner_type == 'customer' and self.payment_type == 'outbound':
                # raise UserError('2')
                balance1 = self.currency_id._convert(self.tax_amount, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': 'Withholding Tax',
                    'amount_currency': -(self.tax_amount),
                    'currency_id': currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': (self.tax_amount),
                    'date_maturity': self.date,
                    'partner_id': self.partner_id.commercial_partner_id.id,
                    'account_id': self.tax_account.id,
                    'payment_id': self.id,
                })
            # Payment from Customer with WTH Tax
            else:
                # raise UserError('3')
                balance1 = self.currency_id._convert(self.tax_amount, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': self.payment_reference,
                    'date_maturity': self.date,
                    'amount_currency': (self.tax_amount),
                    'currency_id': currency_id,
                    'debit': (self.tax_amount),
                    'credit': 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.tax_account.id,
                })

        if self.tax_amount_service:
            # Supplier WTH Tax condition
            if self.partner_type == 'supplier':
                balance1 = self.currency_id._convert(self.tax_amount_service, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': liquidity_line_name,
                    'amount_currency': -(self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': (self.tax_amount_service),
                    'date_maturity': self.date,
                    'partner_id': self.partner_id.commercial_partner_id.id,
                    'account_id': self.tax_account_service.id,
                    'payment_id': self.id,
                })
            # Payment to Customer with Tax condition
            elif self.partner_type == 'customer' and self.payment_type == 'outbound':
                balance1 = self.currency_id._convert(self.tax_amount_service, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': liquidity_line_name,
                    'amount_currency': -(self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': (self.tax_amount_service),
                    'date_maturity': self.date,
                    'partner_id': self.partner_id.commercial_partner_id.id,
                    'account_id': self.tax_account_service.id,
                    'payment_id': self.id,
                })
            # Payment from Customer with WTH Tax
            else:
                balance1 = self.currency_id._convert(self.tax_amount_service, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': self.payment_reference or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': (self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': (self.tax_amount_service),
                    'credit': 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.tax_account_service.id,
                })

       
        #default code odoo16
        # line_vals_list = [
        #     # Liquidity line.
        #     {
        #         'name': liquidity_line_name,
        #         'date_maturity': self.date,
        #         'amount_currency': liquidity_amount_currency,
        #         'currency_id': currency_id,
        #         'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
        #         'credit': -liquidity_balance if liquidity_balance < 0.0 else 0.0,
        #         'partner_id': self.partner_id.id,
        #         'account_id': self.outstanding_account_id.id,
        #     },
        #     # Receivable / Payable.
        #     {
        #         'name': counterpart_line_name,
        #         'date_maturity': self.date,
        #         'amount_currency': counterpart_amount_currency,
        #         'currency_id': currency_id,
        #         'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
        #         'credit': -counterpart_balance if counterpart_balance < 0.0 else 0.0,
        #         'partner_id': self.partner_id.id,
        #         'account_id': self.destination_account_id.id,
        #     },
        # ]
        # raise UserError(str(line_vals_list))
        return line_vals_list + write_off_line_vals_list

    def _synchronize_to_moves(self, changed_fields):
        ''' Update the account.move regarding the modified account.payment.
        :param changed_fields: A list containing all modified fields on account.payment.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        #withholding
        if not any(field_name in changed_fields for field_name in (
            'date', 'amount', 'payment_type', 'partner_type', 'payment_reference', 'is_internal_transfer',
            'currency_id', 'partner_id', 'destination_account_id', 'partner_bank_id', 'journal_id', 'tax_code'
        )):
            return
        #defualt code odoo16
        # if not any(field_name in changed_fields for field_name in self._get_trigger_fields_to_synchronize()):
            # return

        for pay in self.with_context(skip_account_move_synchronization=True):
            liquidity_lines, counterpart_lines, writeoff_lines, wth_lines,ser_wht_line = pay._seek_for_lines()

            # Make sure to preserve the write-off amount.
            # This allows to create a new payment with custom 'line_ids'.

            write_off_line_vals = []
            if liquidity_lines and counterpart_lines and writeoff_lines:
                write_off_line_vals.append({
                    'name': writeoff_lines[0].name,
                    'account_id': writeoff_lines[0].account_id.id,
                    'partner_id': writeoff_lines[0].partner_id.id,
                    'currency_id': writeoff_lines[0].currency_id.id,
                    'amount_currency': sum(writeoff_lines.mapped('amount_currency')),
                    'balance': sum(writeoff_lines.mapped('balance')),
                })

            line_vals_list = pay._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)

            #default code odoo 16
            # line_ids_commands = [
            #     Command.update(liquidity_lines.id, line_vals_list[0]) if liquidity_lines else Command.create(line_vals_list[0]),
            #     Command.update(counterpart_lines.id, line_vals_list[1]) if counterpart_lines else Command.create(line_vals_list[1])
            # ]

            #withholding
            if wth_lines:
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                    (1, wth_lines.id, line_vals_list[2]),
                ]
            elif self.tax_account:
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                    (0, wth_lines.id, line_vals_list[2]),
                ]
            else:
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                ]

            if ser_wht_line:
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                    (1, ser_wht_line.id, line_vals_list[2]),
                ]
            elif self.tax_account_service:
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                    (0, ser_wht_line.id, line_vals_list[2]),
                ]
            else:
                line_ids_commands = [
                    (1, liquidity_lines.id, line_vals_list[0]),
                    (1, counterpart_lines.id, line_vals_list[1]),
                ]
            for line in writeoff_lines:
                line_ids_commands.append((2, line.id))

            for extra_line_vals in line_vals_list[2:]:
                line_ids_commands.append((0, 0, extra_line_vals))

            # Update the existing journal items.
            # If dealing with multiple write-off lines, they are dropped and a new one is generated.

            pay.move_id.write({
                'partner_id': pay.partner_id.id,
                'currency_id': pay.currency_id.id,
                'partner_bank_id': pay.partner_bank_id.id,
                'line_ids': line_ids_commands,
            })

    def _compute_reconciliation_status(self):
        ''' Compute the field indicating if the payments are already reconciled with something.
        This field is used for display purpose (e.g. display the 'reconcile' button redirecting to the reconciliation
        widget).
        '''
        #withholding
        for pay in self:
            liquidity_lines, counterpart_lines, writeoff_lines, wth_lines,ser_wht_line = pay._seek_for_lines()

            if not pay.currency_id or not pay.id:
                pay.is_reconciled = False
                pay.is_matched = False
            elif pay.currency_id.is_zero(pay.amount):
                pay.is_reconciled = True
                pay.is_matched = True
            else:
                residual_field = 'amount_residual' if pay.currency_id == pay.company_id.currency_id else 'amount_residual_currency'
                if pay.journal_id.default_account_id and pay.journal_id.default_account_id in liquidity_lines.account_id:
                    # Allow user managing payments without any statement lines by using the bank account directly.
                    # In that case, the user manages transactions only using the register payment wizard.
                    pay.is_matched = True
                else:
                    pay.is_matched = pay.currency_id.is_zero(sum(liquidity_lines.mapped(residual_field)))

                reconcile_lines = (counterpart_lines + writeoff_lines).filtered(lambda line: line.account_id.reconcile)
                pay.is_reconciled = pay.currency_id.is_zero(sum(reconcile_lines.mapped(residual_field)))
    
    def _synchronize_from_moves(self, changed_fields):
        ''' Update the account.payment regarding its related account.move.
        Also, check both models are still consistent.
        :param changed_fields: A set containing all modified fields on account.move.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):

            # After the migration to 14.0, the journal entry could be shared between the account.payment and the
            # account.bank.statement.line. In that case, the synchronization will only be made with the statement line.
            if pay.move_id.statement_line_id:
                continue

            move = pay.move_id
            move_vals_to_write = {}
            payment_vals_to_write = {}

            if 'journal_id' in changed_fields:
                if pay.journal_id.type not in ('bank', 'cash'):
                    raise UserError(_("A payment must always belongs to a bank or cash journal."))

            if 'line_ids' in changed_fields:
                all_lines = move.line_ids
                #withholding
                liquidity_lines, counterpart_lines, writeoff_lines, wth_lines, ser_wht_line = pay._seek_for_lines()

                if len(liquidity_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one outstanding payments/receipts account.",
                        move.display_name,
                    ))

                if len(counterpart_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one receivable/payable account (with an exception of "
                        "internal transfers).",
                        move.display_name,
                    ))

                if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same currency.",
                        move.display_name,
                    ))

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same partner.",
                        move.display_name,
                    ))

                if counterpart_lines.account_id.account_type == 'asset_receivable':
                    partner_type = 'customer'
                else:
                    partner_type = 'supplier'

                liquidity_amount = liquidity_lines.amount_currency

                move_vals_to_write.update({
                    'currency_id': liquidity_lines.currency_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                payment_vals_to_write.update({
                    'amount': abs(liquidity_amount),
                    'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                if liquidity_amount > 0.0:
                    payment_vals_to_write.update({'payment_type': 'inbound'})
                elif liquidity_amount < 0.0:
                    payment_vals_to_write.update({'payment_type': 'outbound'})

            move.write(move._cleanup_write_orm_values(move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(pay, payment_vals_to_write))
    
    
    @api.depends('move_id.line_ids.amount_residual', 'move_id.line_ids.amount_residual_currency', 'move_id.line_ids.account_id')
    def _compute_reconciliation_status(self):
        ''' Compute the field indicating if the payments are already reconciled with something.
        This field is used for display purpose (e.g. display the 'reconcile' button redirecting to the reconciliation
        widget).
        '''
        for pay in self:
            liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

            if not pay.currency_id or not pay.id:
                pay.is_reconciled = False
                pay.is_matched = False
            elif pay.currency_id.is_zero(pay.amount):
                pay.is_reconciled = True
                pay.is_matched = True
            else:
                residual_field = 'amount_residual' if pay.currency_id == pay.company_id.currency_id else 'amount_residual_currency'
                if pay.journal_id.default_account_id and pay.journal_id.default_account_id in liquidity_lines.account_id:
                    # Allow user managing payments without any statement lines by using the bank account directly.
                    # In that case, the user manages transactions only using the register payment wizard.
                    pay.is_matched = True
                else:
                    pay.is_matched = pay.currency_id.is_zero(sum(liquidity_lines.mapped(residual_field)))

                reconcile_lines = (counterpart_lines + writeoff_lines).filtered(lambda line: line.account_id.reconcile)
                pay.is_reconciled = pay.currency_id.is_zero(sum(reconcile_lines.mapped(residual_field)))

    
    #replacing all default methods of account payment with withholding methods
    AP._seek_for_lines = _seek_for_lines
    AP._prepare_move_line_default_vals = _prepare_move_line_default_vals
    AP._synchronize_to_moves = _synchronize_to_moves
    AP._compute_reconciliation_status = _compute_reconciliation_status
    AP._synchronize_from_moves = _synchronize_from_moves
    AP._compute_reconciliation_status = _compute_reconciliation_status
