from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.account.models.account_payment import AccountPayment as AP

class AccountTax(models.Model):
    _inherit = "account.tax"

    is_withholding = fields.Boolean("Is Withholding Tax", default=False)

class AccountPayment(models.Model):
    _inherit = "account.payment"
    amount_to_withhold = fields.Float(string="Amount to Withhold")
    paid_to = fields.Monetary(string='Paid to', store=True, readonly=True, compute='_compute_paid_to_amount')
    tax_code = fields.Many2one('account.tax', string='Tax Code', domain=[('is_withholding', '=', True)])
    tax_account = fields.Many2one('account.account', string='Tax Account', readonly=True)
    tax_perc = fields.Float(string='Tax %', readonly=True)
    tax_amount = fields.Float(string='Tax Amount', readonly=True)
    total_amount = fields.Float(string='Total Amount', readonly=True)

    amount_to_withhold_service = fields.Float(string="Amount to Withhold")
    paid_to_service = fields.Monetary(string='Paid to', store=True, readonly=True, compute='_compute_paid_to_amount')
    tax_code_service = fields.Many2one('account.tax', string='Tax Code', domain=[('is_withholding', '=', True)])
    tax_account_service = fields.Many2one('account.account', string='Tax Account', readonly=True)
    tax_perc_service = fields.Float(string='Tax %', readonly=True)
    tax_amount_service = fields.Float(string='Tax Amount', readonly=True)
    total_amount_service = fields.Float(string='Total Amount', readonly=True)


    @api.onchange('tax_code' , 'tax_code_service')
    def _compute_tax_fields(self):
        for record in self:
            for data in record.tax_code.invoice_repartition_line_ids:
                if self.amount_to_withhold:
                    record.tax_account = data.account_id.id
                    record.tax_perc = 	record.tax_code.amount
                    record.tax_amount = round(record.amount_to_withhold * (record.tax_perc / 100))
                    record.total_amount = round(record.amount_to_withhold - record.tax_amount)

            for dat in record.tax_code_service.invoice_repartition_line_ids:
                if self.amount_to_withhold_service:
                    record.tax_account_service = dat.account_id.id
                    record.tax_perc_service = 	record.tax_code_service.amount
                    record.tax_amount_service = round(record.amount_to_withhold_service * (record.tax_perc_service / 100))
                    record.total_amount_service = round(record.amount_to_withhold_service - record.tax_amount_service)
                # record.paid_to = record.amount + record.tax_amount
                # record.paid_to = record.amount + record.tax_amount
    
    @api.onchange('amount')
    def _onchange_amounts(self):
        for record in self:
            record.tax_code = False
            record.tax_account = False
            record.tax_perc = 	False
            record.tax_amount = False
            record.total_amount = False

            record.tax_code_service = False
            record.tax_account_service = False
            record.tax_perc_service = 	False
            record.tax_amount_service = False
            record.total_amount_service = False
            # record.paid_to = False
    
    @api.depends('amount')
    def _compute_paid_to_amount(self):
        for record in self:
            record.paid_to = record.amount + record.tax_amount + record.tax_amount_service

    
    
    
    #Withholding methods
    # def _seek_for_lines(self):
    #     ''' Helper used to dispatch the journal items between:
    #     - The lines using the temporary liquidity account.
    #     - The lines using the counterpart account.
    #     - The lines being the write-off lines.
    #     :return: (liquidity_lines, counterpart_lines, writeoff_lines)
    #     '''
    #     self.ensure_one()

    #     liquidity_lines = self.env['account.move.line']
    #     counterpart_lines = self.env['account.move.line']
    #     writeoff_lines = self.env['account.move.line']
    #     wth_lines = self.env['account.move.line']

    #     for line in self.move_id.line_ids:
    #         if line.account_id in (
    #                 self.journal_id.default_account_id,
    #                 self.journal_id.payment_debit_account_id,
    #                 self.journal_id.payment_credit_account_id,
    #         ):
    #             liquidity_lines += line
    #         elif line.account_id.internal_type in ('receivable', 'payable') or line.partner_id == line.company_id.partner_id:
    #             counterpart_lines += line
    #         elif line.account_id.id == self.tax_account.id:
    #             wth_lines += line
    #         else:
    #             writeoff_lines += line

    #     return liquidity_lines, counterpart_lines, writeoff_lines, wth_lines

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
        wth_lines = self.env['account.move.line']

        ser_wht_line = self.env['account.move.line']


        for line in self.move_id.line_ids:
            if line.account_id in self._get_valid_liquidity_accounts():
                liquidity_lines += line
            elif line.account_id.internal_type in ('receivable', 'payable') or line.partner_id == line.company_id.partner_id:
                counterpart_lines += line
            elif line.account_id.id == self.tax_account.id:
                wth_lines += line
            elif line.account_id.id == self.tax_account_service.id:
                ser_wht_line += line
            else:
                writeoff_lines += line

        return liquidity_lines, counterpart_lines, writeoff_lines,wth_lines,ser_wht_line



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

        # if not self.journal_id.payment_debit_account_id or not self.journal_id.payment_credit_account_id:
        #     raise UserError(_(
        #         "You can't create a new payment without an outstanding payments/receipts account set on the %s journal.",
        #         self.journal_id.display_name))
        if not self.outstanding_account_id:
            raise UserError(_(
                "You can't create a new payment without an outstanding payments/receipts account set either on the company or the %s payment method in the %s journal.",
                self.payment_method_line_id.name, self.journal_id.display_name))

        # Compute amounts.
        write_off_amount = write_off_line_vals.get('amount', 0.0)

        if self.payment_type == 'inbound':
            # Receive money.
            counterpart_amount = -self.amount
            write_off_amount *= -1
        elif self.payment_type == 'outbound':
            # Send money.
            counterpart_amount = self.amount
        else:
            counterpart_amount = 0.0
            write_off_amount = 0.0

        balance = self.currency_id._convert(counterpart_amount, self.company_id.currency_id, self.company_id, self.date)
        counterpart_amount_currency = counterpart_amount
        write_off_balance = self.currency_id._convert(write_off_amount, self.company_id.currency_id, self.company_id, self.date)
        write_off_amount_currency = write_off_amount
        currency_id = self.currency_id.id

        if self.is_internal_transfer:
            if self.payment_type == 'inbound':
                liquidity_line_name = _('Transfer to %s', self.journal_id.name)
            else: # payment.payment_type == 'outbound':
                liquidity_line_name = _('Transfer from %s', self.journal_id.name)
        else:
            liquidity_line_name = self.payment_reference

        # Compute a default label to set on the journal items.

        payment_display_name = {
            'outbound-customer': _("Customer Reimbursement"),
            'inbound-customer': _("Customer Payment"),
            'outbound-supplier': _("Vendor Payment"),
            'inbound-supplier': _("Vendor Reimbursement"),
        }

        default_line_name = self.env['account.move.line']._get_default_line_name(
            _("Internal Transfer") if self.is_internal_transfer else payment_display_name['%s-%s' % (self.payment_type, self.partner_type)],
            self.amount,
            self.currency_id,
            self.date,
            partner=self.partner_id,
        )
        line_vals_list = []
        if self.partner_type == 'supplier':
            line_vals_list = [
                # Liquidity line.
                {
                    'name': liquidity_line_name or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': -counterpart_amount_currency + (self.tax_amount + self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': balance - (self.tax_amount + self.tax_amount_service) > 0.0 and balance - (self.tax_amount + self.tax_amount_service) or 0.0,
                    'partner_id': self.partner_id.id,
                    # 'account_id': self.journal_id.payment_debit_account_id.id if balance < 0.0 else self.journal_id.payment_credit_account_id.id,
                    'account_id':self.outstanding_account_id.id,
                },
                # Receivable / Payable.
                {
                    'name': self.payment_reference or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': counterpart_amount_currency + write_off_amount_currency if currency_id else 0.0,
                    'currency_id': currency_id,
                    'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                    'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                },
            ]
        elif self.partner_type == 'customer' and self.payment_type == 'outbound':
        # Payment to Customer with WTH Tax.
            line_vals_list = [
                # Liquidity line.
                {
                    'name': liquidity_line_name or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': -counterpart_amount_currency + (self.tax_amount + self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': balance < 0.0 and -balance or 0.0,
                    'credit': balance - (self.tax_amount + self.tax_amount_service) > 0.0 and balance - (self.tax_amount + self.tax_amount_service) or 0.0,
                    'partner_id': self.partner_id.id,
                    # 'account_id': self.journal_id.payment_debit_account_id.id if balance < 0.0 else self.journal_id.payment_credit_account_id.id,
                    'account_id': self.outstanding_account_id.id,
                },
                # Receivable / Payable.
                {
                    'name': self.payment_reference or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': counterpart_amount_currency + write_off_amount_currency if currency_id else 0.0,
                    'currency_id': currency_id,
                    'debit': balance + write_off_balance > 0.0 and balance + write_off_balance or 0.0,
                    'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                },
            ]
        else:
        # Payment from Customer with WTH Tax
            line_vals_list = [
                # Liquidity line.
                {
                    'name': liquidity_line_name or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': -counterpart_amount_currency+(self.tax_amount + self.tax_amount_service),
                    'currency_id': currency_id,
                    'debit': balance+(self.tax_amount + self.tax_amount_service) < 0.0 and -balance-(self.tax_amount + self.tax_amount_service) or 0.0,
                    'credit': balance > 0.0 and balance or 0.0,
                    'partner_id': self.partner_id.id,
                    # 'account_id': self.journal_id.payment_debit_account_id.id if balance < 0.0 else self.journal_id.payment_credit_account_id.id,
                    'account_id': self.outstanding_account_id.id,
                },
                # Receivable / Payable.
                {
                    'name': self.payment_reference or default_line_name,
                    'date_maturity': self.date,
                    'amount_currency': (counterpart_amount_currency + write_off_amount_currency) if currency_id else 0.0,
                    'currency_id': currency_id,
                    'debit': balance + write_off_balance  > 0.0 and balance + write_off_balance or 0.0,
                    'credit': balance + write_off_balance < 0.0 and -balance - write_off_balance or 0.0,
                    'partner_id': self.partner_id.id,
                    'account_id': self.destination_account_id.id,
                },
            ]
        if write_off_balance:
            # Write-off line.
            line_vals_list.append({
                'name': write_off_line_vals.get('name') or default_line_name,
                'amount_currency': -write_off_amount_currency,
                'currency_id': currency_id,
                'debit': write_off_balance < 0.0 and -write_off_balance or 0.0,
                'credit': write_off_balance > 0.0 and write_off_balance or 0.0,
                'partner_id': self.partner_id.id,
                'account_id': write_off_line_vals.get('account_id'),
            })
        if self.tax_amount:
            # Supplier WTH Tax condition
            if self.partner_type == 'supplier':
                balance1 = self.currency_id._convert(self.tax_amount, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': liquidity_line_name,
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
                balance1 = self.currency_id._convert(self.tax_amount, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': liquidity_line_name,
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
                balance1 = self.currency_id._convert(self.tax_amount, self.company_id.currency_id, self.company_id, self.date)
                # Write-off line.
                line_vals_list.append({
                    'name': self.payment_reference or default_line_name,
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
        #raise UserError(str(line_vals_list))
        return line_vals_list

    def _synchronize_to_moves(self, changed_fields):
        ''' Update the account.move regarding the modified account.payment.
        :param changed_fields: A list containing all modified fields on account.payment.
        '''
        #raise UserError(changed_fields)
        if self._context.get('skip_account_move_synchronization'):
            return

        if not any(field_name in changed_fields for field_name in (
            'date', 'amount', 'payment_type', 'partner_type', 'payment_reference', 'is_internal_transfer',
            'currency_id', 'partner_id', 'destination_account_id', 'partner_bank_id','total_amount', 'tax_code',
        )):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):
            liquidity_lines, counterpart_lines, writeoff_lines, wth_lines, ser_wht_line = pay._seek_for_lines()

            # Make sure to preserve the write-off amount.
            # This allows to create a new payment with custom 'line_ids'.

            if writeoff_lines:
                writeoff_amount = sum(writeoff_lines.mapped('amount_currency'))
                counterpart_amount = counterpart_lines['amount_currency']
                if writeoff_amount > 0.0 and counterpart_amount > 0.0:
                    sign = 1
                else:
                    sign = -1

                write_off_line_vals = {
                    'name': writeoff_lines[0].name,
                    'amount': writeoff_amount * sign,
                    'account_id': writeoff_lines[0].account_id.id,
                }
            else:
                write_off_line_vals = {}

            line_vals_list = pay._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
            #raise UserError(str(line_vals_list))
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

            if writeoff_lines:
                line_ids_commands.append((0, 0, line_vals_list[2]))

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
        for pay in self:
            liquidity_lines, counterpart_lines, writeoff_lines, wth_lines, ser_wht_line = pay._seek_for_lines()

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
                liquidity_lines, counterpart_lines, writeoff_lines, wth_lines ,ser_wht_line = pay._seek_for_lines()

                # if len(liquidity_lines) != 1 or len(counterpart_lines) != 1:
                    # raise UserError(_(
                        # "The journal entry %s reached an invalid state relative to its payment.\n"
                        # "To be consistent, the journal entry must always contains:\n"
                        # "- one journal item involving the outstanding payment/receipts account.\n"
                        # "- one journal item involving a receivable/payable account.\n"
                        # "- optional journal items, all sharing the same account.\n\n"
                    # ) % move.display_name)

                if writeoff_lines and len(writeoff_lines.account_id) != 1:
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, all the write-off journal items must share the same account."
                    ) % move.display_name)

                if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal items must share the same currency."
                    ) % move.display_name)

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "The journal entry %s reached an invalid state relative to its payment.\n"
                        "To be consistent, the journal items must share the same partner."
                    ) % move.display_name)

                if counterpart_lines.account_id.user_type_id.type == 'receivable':
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
                    'payment_type': 'inbound' if liquidity_amount > 0.0 else 'outbound',
                    'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })

            move.write(move._cleanup_write_orm_values(move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(pay, payment_vals_to_write))

    @api.depends('move_id.line_ids.amount_residual', 'move_id.line_ids.amount_residual_currency', 'move_id.line_ids.account_id')
    def _compute_reconciliation_status(self):
        ''' Compute the field indicating if the payments are already reconciled with something.
        This field is used for display purpose (e.g. display the 'reconcile' button redirecting to the reconciliation
        widget).
        '''
        for pay in self:
            liquidity_lines, counterpart_lines, writeoff_lines, wth_lines , ser_wht_line= pay._seek_for_lines()

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
    