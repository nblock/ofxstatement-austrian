#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import datetime
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.ingdiba import IngDiBaCsvParser

class TestLivebankCsvParser(unittest.TestCase):
    """Unit tests for IngDiBaCsvParser."""

    def setUp(self):
        csvfile = os.path.join(os.path.dirname(__file__), 'samples', 'ing-diba.csv')
        with open(csvfile, 'r', encoding='iso-8859-1') as fin:
            self.statement = IngDiBaCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 6)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, -992.03)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "12345678001")
        self.assertEqual(self.statement.start_date, datetime.datetime(2013, 8, 13, 0, 0))
        self.assertEqual(self.statement.end_date, datetime.datetime(2013, 12, 31, 0, 0))

    def test_line0_interest_earned(self):
        l = self.statement.lines[0]
        self.assertEqual(l.amount, 12.23)
        self.assertEqual(l.memo, "Habenzinsen")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 12, 31, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line1_interest_paid(self):
        l = self.statement.lines[1]
        self.assertEqual(l.amount, -34.56)
        self.assertEqual(l.memo, "Kapitalertragsteuer")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 12, 31, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line2_credit(self):
        l = self.statement.lines[2]
        self.assertEqual(l.amount, 500.00)
        self.assertEqual(l.memo, "Eingang: XXX")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 12, 23, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line3_transfer_credit(self):
        l = self.statement.lines[3]
        self.assertEqual(l.amount, 20.30)
        self.assertEqual(l.memo, "Umbuchung von 003")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 9, 25, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line4_debit(self):
        l = self.statement.lines[4]
        self.assertEqual(l.amount, -1500)
        self.assertEqual(l.memo, "Auszahlung - XXX")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 8, 27, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line5_bonus(self):
        l = self.statement.lines[5]
        self.assertEqual(l.amount, 10.00)
        self.assertEqual(l.memo, "Prämie Foo")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 8, 13, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
