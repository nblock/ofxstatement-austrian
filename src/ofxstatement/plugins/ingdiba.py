#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import csv
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import generate_transaction_id
from ofxstatement import statement
from ofxstatement.plugins.utils import fix_amount_string


class IngDiBaCsvParser(CsvStatementParser):
    """The csv parser for ING-DiBa."""

    date_format = "%d.%m.%Y"

    mappings = {
                "memo": 1,
                "date": 2,
                "amount": 4,
                }

    def parse(self):
        """Parse."""
        stmt = super(IngDiBaCsvParser, self).parse()
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

        # Account id
        if not self.statement.account_id:
            self.statement.account_id = line[0]

        # Currency
        if not self.statement.currency:
            self.statement.currency = line[3]

        # Save credit/debit on line[4]
        if line[4] == "0,00":
            line[4] = fix_amount_string(line[5])
        else:
            line[4] = "-{}".format(fix_amount_string(line[4]))

        # Create statement and fixup missing parts
        stmtline = super(IngDiBaCsvParser, self).parse_record(line)
        stmtline.trntype = 'DEBIT' if stmtline.amount < 0 else 'CREDIT'
        stmtline.id = generate_transaction_id(stmtline)

        return stmtline


class IngDiBaPlugin(Plugin):
    """ING-DiBa (CSV)"""

    def get_parser(self, filename):
        """Get a parser instance."""
        encoding = self.settings.get('charset', 'iso-8859-1')
        f = open(filename, 'r', encoding=encoding)
        parser = IngDiBaCsvParser(f)
        parser.statement.bank_id = self.settings.get('bank', 'ING-DiBa')
        return parser

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
