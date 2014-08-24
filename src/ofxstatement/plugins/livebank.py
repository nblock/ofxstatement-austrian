#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import csv
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import generate_transaction_id
from ofxstatement import statement
from ofxstatement.plugins.utils import clean_multiple_whitespaces, fix_amount_string


class LivebankCsvParser(CsvStatementParser):
    """The csv parser for Livebank."""

    date_format = "%Y-%m-%d"

    mappings = {
                "date": 2,
                "amount": 7,
                "memo": 8,
                "payee": 9,
                }

    def parse(self):
        """Parse."""
        stmt = super(LivebankCsvParser, self).parse()
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

        # Skip lines without amount
        if line[7] == "0,00":
            return None

        # Account id
        if not self.statement.account_id:
            self.statement.account_id = line[0]

        # Currency
        if not self.statement.currency:
            self.statement.currency = line[6]

        # Cleanup parts
        line[7] = fix_amount_string(line[7])
        line[9] = clean_multiple_whitespaces(", ".join(line[9:]))

        # Create statement and fixup missing parts
        stmtline = super(LivebankCsvParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.id = generate_transaction_id(stmtline)

        return stmtline


class LivebankPlugin(Plugin):
    """Livebank (CSV)"""

    def get_parser(self, filename):
        """Get a parser instance."""
        encoding = self.settings.get('charset', 'iso-8859-1')
        f = open(filename, 'r', encoding=encoding)
        parser = LivebankCsvParser(f)
        parser.statement.bank_id = self.settings.get('bank', 'Livebank')
        return parser

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
