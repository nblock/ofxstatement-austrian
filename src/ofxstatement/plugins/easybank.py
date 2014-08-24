#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import csv
import re
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import generate_transaction_id
from ofxstatement import statement
from ofxstatement.plugins.utils import clean_multiple_whitespaces, fix_amount_string

class EasybankCsvParser(CsvStatementParser):
    """The csv parser for Easybank (base)."""

    date_format = "%d.%m.%Y"

    def split_records(self):
        """Split records using a custom dialect."""
        return csv.reader(self.fin, delimiter=";")


class EasybankCreditCardCsvParser(EasybankCsvParser):
    """The csv parser for Easybank (credit card)."""

    mappings = {
                "memo": 1,
                "id": 2,
                "date": 3,
                "amount": 5,
                }

    def parse(self):
        """Parse."""
        stmt = super(EasybankCreditCardCsvParser, self).parse()
        statement.recalculate_balance(stmt)
        return stmt

    def parse_record(self, line):
        """Parse a single record."""
        # Split the description into two parts and save it to the line list.
        parts = line[1].split('|')

        # 3 parts: Description, foreign language, transaction id
        # 2 parts: Description, transaction id
        if len(parts) == 3:
            line[1] = "{} ({})".format(parts[0], parts[1])
        else:
            line[1] = parts[0]
        line.insert(2, parts[-1])

        # Account id
        if not self.statement.account_id:
            self.statement.account_id = line[0]

        # Currency
        if not self.statement.currency:
            self.statement.currency = line[6]

        # Cleanup amount
        line[5] = fix_amount_string(line[5])
        line[1] = clean_multiple_whitespaces(line[1])

        # Create statement and fixup missing parts
        stmtline = super(EasybankCreditCardCsvParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'

        return stmtline


class EasybankGiroCsvParser(EasybankCsvParser):
    """The csv parser for Easybank (giro)."""

    mappings = {
                "check_no": 1,
                "memo": 2,
                "payee": 3,
                "date": 4,
                "amount": 6,
                }

    reg_description = re.compile(r'[A-Z]{2}/[0-9]{9}')
    reg_iban = re.compile(r'([A-Z]{6}[A-Z0-9]{2}[^\s]*)?\s?([A-Z]{2}[0-9]{10,34})\s(.*)')
    reg_legacy = re.compile(r'(.*)([0-9]{5,})\s([0-9]{6,})(.*)')

    def extract_check_no(self, description):
        '''Try to extract the statement check_no.'''
        result = ''
        mo = self.reg_description.search(description)
        if mo:
            result = str(int(mo.group(0).split('/')[1]))
        return result

    def extract_description(self, description):
        '''Cleanup description from a giro account.'''
        # extract iban/bic, account number, ...
        parts = [x.strip() for x in self.reg_description.split(description)]

        # parts: memo, transaction
        if not parts[1]:
            return parts[0], parts[0]

        # parts: memo, transaction, banking information
        else:
            # extract iban, bic and text
            iban_bic = self.reg_iban.search(parts[1])
            if iban_bic:
                # iban, bic and text
                if iban_bic.group(1):
                    result = '{0} ({1} {2})'.format(iban_bic.group(3),
                            iban_bic.group(2), iban_bic.group(1))
                # iban only
                else:
                    result = '{0} ({1})'.format(iban_bic.group(3),
                            iban_bic.group(2))

                return parts[0], result

            # extract legacy banking number
            account_number = self.reg_legacy.search(parts[1])
            if account_number:
                if account_number.group(1):
                    text = account_number.group(1).strip()
                else:
                    text = account_number.group(4).strip()

                return parts[0], '{0} ({1} {2})'.format(text,
                            account_number.group(3),
                            account_number.group(2))

            # Could not extract anything useful, return parts as is.
            return parts[0], parts[1]

    def parse(self):
        """Parse."""
        stmt = super(EasybankGiroCsvParser, self).parse()
        statement.recalculate_balance(stmt)
        return stmt

    def parse_record(self, line):
        """Parse a single record."""
        # Extract check_no/id
        description = line[1]
        del line[1]

        # Get check_no from description
        line.insert(1, self.extract_check_no(description))

        # Get memo and payee from description
        tt = self.extract_description(description)
        line.insert(2, tt[0])
        line.insert(3, tt[1])
        # line.insert(2, self.extract_description(description))

        # Account id
        if not self.statement.account_id:
            self.statement.account_id = line[0]

        # Currency
        if not self.statement.currency:
            self.statement.currency = line[7]

        # Cleanup parts
        line[6] = fix_amount_string(line[6])
        line[2] = clean_multiple_whitespaces(line[2])
        line[3] = clean_multiple_whitespaces(line[3])

        # Create statement and fixup missing parts
        stmtline = super(EasybankGiroCsvParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.id = generate_transaction_id(stmtline)

        return stmtline


class EasybankPlugin(Plugin):
    """Easybank (CSV)"""

    def determine_parser(self, fp):
        """Determine the parser to use based on the first booking line."""
        description = fp.readline().split(";")[1]
        fp.seek(0)  # reset pointer
        if '|' in description:
            return EasybankCreditCardCsvParser(fp)
        else:
            return EasybankGiroCsvParser(fp)

    def get_parser(self, filename):
        """Get a parser instance."""
        encoding = self.settings.get('charset', 'cp1252')
        f = open(filename, 'r', encoding=encoding)
        parser = self.determine_parser(f)
        parser.statement.bank_id = self.settings.get('bank', 'Easybank')
        return parser

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
