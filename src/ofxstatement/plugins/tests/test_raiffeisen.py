#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import datetime
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.raiffeisen import RaiffeisenCsvParser

class TestRaiffeisenCsvParser(unittest.TestCase):
    """Unit tests for RaiffeisenCsvParser."""

    def setUp(self):
        csvfile = os.path.join(os.path.dirname(__file__), 'samples', 'raiffeisen.csv')
        with open(csvfile, 'r', encoding='cp1252') as fin:
            self.statement = RaiffeisenCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 7)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, -157.89)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.start_date, datetime.datetime(2013, 6, 28, 0, 0))
        self.assertEqual(self.statement.end_date, datetime.datetime(2013, 7, 4, 0, 0))

    def test_line0_interest_earned(self):
        l = self.statement.lines[0]
        self.assertEqual(l.amount, 0.58)
        self.assertEqual(l.memo, "0,125 % p.a. Habenzinsen ab 01.04.13")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 28, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line1_interest_paid(self):
        l = self.statement.lines[1]
        self.assertEqual(l.amount, -0.15)
        self.assertEqual(l.memo, "Kapitalertragsteuer")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 28, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line2_service_fee_print_statement(self):
        l = self.statement.lines[2]
        self.assertEqual(l.amount, -0.11)
        self.assertEqual(l.memo, "Entgelt Kontoauszug")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 28, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line3_service_fee(self):
        l = self.statement.lines[3]
        self.assertEqual(l.amount, -6.65)
        self.assertEqual(l.memo, "Entgelt Kontoführung")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 28, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line4_elba_payment(self):
        l = self.statement.lines[4]
        self.assertEqual(l.amount, -175.16)
        self.assertEqual(l.memo, "ELBA-INTERNET VOM 29.06 UM 09:16 Empfänger: A person Verwendungszweck: Invoice number 10")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 7, 1, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line5_debit(self):
        l = self.statement.lines[5]
        self.assertEqual(l.amount, -100)
        self.assertEqual(l.memo, "Lastschrift Auftraggeber: A company Kundendaten: 000000000000 111111111111 Verwendungszweck: reason")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 7, 1, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line6_credit(self):
        l = self.statement.lines[6]
        self.assertEqual(l.amount, 123.60)
        self.assertEqual(l.memo, "Gutschrift Auftraggeber: A person Kundendaten: reason")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 7, 4, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
