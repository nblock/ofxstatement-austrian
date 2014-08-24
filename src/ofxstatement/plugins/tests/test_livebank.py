#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import datetime
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.livebank import LivebankCsvParser

class TestLivebankCsvParser(unittest.TestCase):
    """Unit tests for LivebankCsvParser."""

    def setUp(self):
        csvfile = os.path.join(os.path.dirname(__file__), 'samples', 'livebank.csv')
        with open(csvfile, 'r', encoding='iso-8859-1') as fin:
            self.statement = LivebankCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 3)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, 5050)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "12345678")
        self.assertEqual(self.statement.start_date, datetime.datetime(2013, 6, 5, 0, 0))
        self.assertEqual(self.statement.end_date, datetime.datetime(2013, 7, 3, 0, 0))

    def test_line0_credit(self):
        l = self.statement.lines[0]
        self.assertEqual(l.amount, 150.00)
        self.assertEqual(l.memo, "Datenträger-Umsatz")
        self.assertEqual(l.payee,
                "A name, A text, REF: XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 7, 3, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line1_debit(self):
        l = self.statement.lines[1]
        self.assertEqual(l.amount, -100)
        self.assertEqual(l.memo, "Internetauftrag")
        self.assertEqual(l.payee,
                "A text, A reference, A text")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 10, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line2_credit(self):
        l = self.statement.lines[2]
        self.assertEqual(l.amount, 5000)
        self.assertEqual(l.memo, "Datenträger-Umsatz")
        self.assertEqual(l.payee,
                "A name, A text, REF: XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 5, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
