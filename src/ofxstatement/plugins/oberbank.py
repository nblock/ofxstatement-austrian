#!/usr/bin/env python3
# This file is part of ofxstatement-austrian.
# See README.rst for more information.

import csv
from ofxstatement import statement
from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import generate_transaction_id
from ofxstatement.plugins.utils import \
    clean_multiple_whitespaces, fix_amount_string


class OberbankCsvParser(CsvStatementParser):
    """The csv parser for Oberbank."""

    date_format = "%d.%m.%Y"

    mappings = {
        "date": 0,
        "memo": 10,
        "amount": 2,
        }

    def parse(self):
        """Parse."""
        stmt = super(OberbankCsvParser, self).parse()
        statement.recalculate_balance(stmt)
        return stmt

    def split_records(self):
        """Split records using a custom dialect."""
        return csv.reader(self.fin, delimiter=";")

    def parse_record(self, line):
        """Parse a single record."""
        # Skip header line
        if self.cur_record == 1:
            return None

        # Currency
        if not self.statement.currency:
            self.statement.currency = line[3]

        # Cleanup parts
        line[2] = fix_amount_string(line[2])
        line[10] = clean_multiple_whitespaces(line[10])

        # Create statement and fixup missing parts
        stmtline = super(OberbankCsvParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.id = generate_transaction_id(stmtline)

        return stmtline


class OberbankPlugin(Plugin):
    """Oberbank (CSV)"""

    def get_parser(self, filename):
        """Get a parser instance."""
        encoding = self.settings.get('charset', 'cp1252')
        f = open(filename, 'r', encoding=encoding)
        parser = OberbankCsvParser(f)
        parser.statement.account_id = self.settings.get('account', 'default')
        parser.statement.bank_id = self.settings.get('bank', 'Oberbank')
        return parser

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
