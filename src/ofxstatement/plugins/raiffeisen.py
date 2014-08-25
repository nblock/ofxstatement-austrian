#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import csv
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import generate_transaction_id
from ofxstatement import statement
from ofxstatement.plugins.utils import clean_multiple_whitespaces, fix_amount_string


class RaiffeisenCsvParser(CsvStatementParser):
    """The csv parser for Raiffeisen."""

    date_format = "%d.%m.%Y"

    mappings = {
                "date": 0,
                "memo": 1,
                "amount": 3,
                }

    def parse(self):
        """Parse."""
        stmt = super(RaiffeisenCsvParser, self).parse()
        statement.recalculate_balance(stmt)
        return stmt

    def split_records(self):
        """Split records using a custom dialect."""
        return csv.reader(self.fin, delimiter=";")

    def parse_record(self, line):
        """Parse a single record."""
        # Currency
        if not self.statement.currency:
            self.statement.currency = line[4]

        # Cleanup parts
        line[3] = fix_amount_string(line[3])
        line[1] = clean_multiple_whitespaces(line[1])

        # Create statement and fixup missing parts
        stmtline = super(RaiffeisenCsvParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.id = generate_transaction_id(stmtline)

        return stmtline


class RaiffeisenPlugin(Plugin):
    """Raiffeisenbank (CSV)"""

    def get_parser(self, filename):
        """Get a parser instance."""
        encoding = self.settings.get('charset', 'cp1252')
        f = open(filename, 'r', encoding=encoding)
        parser = RaiffeisenCsvParser(f)
        parser.statement.account_id = self.settings['account']
        parser.statement.bank_id = self.settings.get('bank', 'Raiffeisen')
        return parser

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
