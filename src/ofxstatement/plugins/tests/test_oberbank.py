#!/usr/bin/env python3
# This file is part of ofxstatement-austrian.
# See README.rst for more information.

import datetime
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.oberbank import OberbankCsvParser


class TestOberbankCsvParser(unittest.TestCase):
    """Unit tests for OberbankCsvParser."""

    def setUp(self):
        csvfile = os.path.join(
            os.path.dirname(__file__), 'samples', 'oberbank.csv')
        with open(csvfile, 'r', encoding='cp1252') as fin:
            self.statement = OberbankCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 5)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, -9.0)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(
            self.statement.start_date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(
            self.statement.end_date, datetime.datetime(2017, 3, 15, 0, 0))

    def test_line0_payment_description_reference(self):
        l = self.statement.lines[0]
        self.assertEqual(l.amount, -11.0)
        self.assertEqual(
            l.memo,
            "Zahlungsreferenz, Empfängername, Adresszeile1, Adresszeile2")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line1_payment_description_usage(self):
        l = self.statement.lines[1]
        self.assertEqual(l.amount, -10.0)
        self.assertEqual(
            l.memo,
            "Verwendungszweck, Empfängername, Adresszeile1, Adresszeile2, "
            "Verwendungszweck, VerwendungszweckZeile2, "
            "VerwendungszweckZeile3, VerwendungszweckZeile4")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line2_payment_description_end2end(self):
        l = self.statement.lines[2]
        self.assertEqual(l.amount, -9.0)
        self.assertEqual(
            l.memo,
            "End2EndID, Empfängername, Adresszeile1, Adresszeile2")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line3_credeit(self):
        l = self.statement.lines[3]
        self.assertEqual(l.amount, 11.0)
        self.assertEqual(l.memo, "Empfängername, SCOR, Verwendungszweck")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line4_credeit(self):
        l = self.statement.lines[4]
        self.assertEqual(l.amount, 10.0)
        self.assertEqual(l.memo, "Empfängername, SCOR, Verwendungszweck")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
