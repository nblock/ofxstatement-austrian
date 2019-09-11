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
        line = self.statement.lines[0]
        self.assertEqual(line.amount, -11.0)
        self.assertEqual(
            line.memo,
            "Zahlungsreferenz, Empfängername, Adresszeile1, Adresszeile2")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line1_payment_description_usage(self):
        line = self.statement.lines[1]
        self.assertEqual(line.amount, -10.0)
        self.assertEqual(
            line.memo,
            "Verwendungszweck, Empfängername, Adresszeile1, Adresszeile2, "
            "Verwendungszweck, VerwendungszweckZeile2, "
            "VerwendungszweckZeile3, VerwendungszweckZeile4")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line2_payment_description_end2end(self):
        line = self.statement.lines[2]
        self.assertEqual(line.amount, -9.0)
        self.assertEqual(
            line.memo,
            "End2EndID, Empfängername, Adresszeile1, Adresszeile2")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line3_credeit(self):
        line = self.statement.lines[3]
        self.assertEqual(line.amount, 11.0)
        self.assertEqual(line.memo, "Empfängername, SCOR, Verwendungszweck")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line4_credeit(self):
        line = self.statement.lines[4]
        self.assertEqual(line.amount, 10.0)
        self.assertEqual(line.memo, "Empfängername, SCOR, Verwendungszweck")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2017, 3, 15, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
