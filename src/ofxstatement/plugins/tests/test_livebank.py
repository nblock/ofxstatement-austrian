#!/usr/bin/env python3
# This file is part of ofxstatement-austrian.
# See README.rst for more information.

import datetime
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.livebank import LivebankCsvParser


class TestLivebankCsvParser(unittest.TestCase):
    """Unit tests for LivebankCsvParser."""

    def setUp(self):
        csvfile = os.path.join(
            os.path.dirname(__file__), 'samples', 'livebank.csv')
        with open(csvfile, 'r', encoding='iso-8859-1') as fin:
            self.statement = LivebankCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 3)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, 5050)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "12345678")
        self.assertEqual(
            self.statement.start_date, datetime.datetime(2013, 6, 5, 0, 0))
        self.assertEqual(
            self.statement.end_date, datetime.datetime(2013, 7, 3, 0, 0))

    def test_line0_credit(self):
        line = self.statement.lines[0]
        self.assertEqual(line.amount, 150.00)
        self.assertEqual(line.memo, "Datenträger-Umsatz")
        self.assertEqual(
            line.payee, "A name, A text, REF: XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2013, 7, 3, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line1_debit(self):
        line = self.statement.lines[1]
        self.assertEqual(line.amount, -100)
        self.assertEqual(line.memo, "Internetauftrag")
        self.assertEqual(
            line.payee, "A text, A reference, A text")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2013, 6, 10, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line2_credit(self):
        line = self.statement.lines[2]
        self.assertEqual(line.amount, 5000)
        self.assertEqual(line.memo, "Datenträger-Umsatz")
        self.assertEqual(
            line.payee, "A name, A text, REF: XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2013, 6, 5, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
