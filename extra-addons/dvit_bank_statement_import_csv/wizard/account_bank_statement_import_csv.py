# -*- encoding: utf-8 -*

import logging
import StringIO
import codecs
import hashlib
import dateutil.parser

from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import unicodecsv
except ImportError:
    _logger.debug("unicodecsv not found.")
    unicodecsv = None

try:
    import chardet
except ImportError:
    _logger.debug("chardet not found.")
    chardet = None

class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    @api.model
    def _check_csv(self, data_file):
        if not chardet:
            return False
        if not unicodecsv:
            return False
        try:
            csv = unicodecsv.DictReader(data_file, delimiter=',', quotechar='"',
                                         encoding='utf-8')
        except Exception as e:
            _logger.error(e)
            return False
        return csv

    @api.model
    def _prepare_csv_line(self, line):
        entry_date = dateutil.parser.parse(line['date'],
                                           dayfirst=True,
                                           fuzzy=True).date()
        m = hashlib.sha512()
        m.update(str(line))

        vals = {
            'date': entry_date,
            'name': line['name'],
            'ref': line['ref'],
            'amount': float(line['amount']),
            'unique_import_id': m.hexdigest(),
        }

        return vals

    def _parse_file(self, data_file):
        # decode Charset and remove BOM if needed
        encoding = chardet.detect(data_file)
        data_file.decode(encoding['encoding'])
        if data_file[:3] == codecs.BOM_UTF8:
            data_file = data_file[3:]

        csv = self._check_csv(StringIO.StringIO(data_file))
        if not csv:
            return super(AccountBankStatementImport, self)._parse_file(data_file)

        transactions = []
        total_amt = 0.00
        balance = 0.00
        account_number = None
        currency = None
        totalrows = 0
        try:
            for line in csv:
                vals = self._prepare_csv_line(line)
                if vals:
                    transactions.append(vals)
                    total_amt += vals['amount']
                    totalrows += 1
                if line['balance']:
                    balance = line['balance']
                if not currency and line['currency']:
                    currency = line['currency']
                if currency and currency != line['currency']:
                    raise UserError(_('Bank statement line must same currency.'))
                if not account_number and line['account_number']:
                    account_number = line['account_number']
                if account_number and account_number != line['account_number']:
                    raise UserError(_('Account Number must be same.'))
        except Exception, e:
            raise UserError(_(
                'The following problem occurred during import. The file might '
                'not be valid.\n\n %s' % e.message))

        vals_bank_statement = {
            'name': account_number,
            'transactions': transactions,
            'balance_start': float(balance) - total_amt,
            'balance_end_real': balance,
        }
        return currency, account_number, [vals_bank_statement]
