#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

import datetime
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.easybank import EasybankCreditCardCsvParser, EasybankGiroCsvParser

class TestEasybankCreditCardCsvParser(unittest.TestCase):
    """Unit tests for EasybankCreditCardCsvParser."""

    def setUp(self):
        csvfile = os.path.join(os.path.dirname(__file__), 'samples', 'easybank-creditcard.csv')
        with open(csvfile, 'r', encoding='cp1252') as fin:
            self.statement = EasybankCreditCardCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 3)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, 2.31)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "12345678901")
        self.assertEqual(self.statement.start_date, datetime.datetime(2013, 2, 19, 0, 0))
        self.assertEqual(self.statement.end_date, datetime.datetime(2013, 7, 2, 0, 0))

    def test_line0_debit(self):
        l = self.statement.lines[0]
        self.assertEqual(l.amount, -5.99)
        self.assertEqual(l.memo, "Some vendor/info")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 7, 2, 0, 0))
        self.assertEqual(l.id, "12345678909876543212345")

    def test_line1_credit(self):
        l = self.statement.lines[1]
        self.assertEqual(l.amount, 30.99)
        self.assertEqual(l.memo, "Another vendor")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2013, 6, 21, 0, 0))
        self.assertEqual(l.id, "23456789098765432123456")

    def test_line2_debit_with_foreign_currency(self):
        l = self.statement.lines[2]
        self.assertEqual(l.amount, -22.69)
        self.assertEqual(l.memo, "Someone (GBP 22,89)")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2013, 2, 19, 0, 0))
        self.assertEqual(l.id, "34567890987654321234567")


class TestEasybankGiroCsvParser(unittest.TestCase):
    """Unit tests for EasybankGiroCsvParser."""

    def setUp(self):
        csvfile = os.path.join(os.path.dirname(__file__), 'samples', 'easybank-giro.csv')
        with open(csvfile, 'r', encoding='cp1252') as fin:
            self.statement = EasybankGiroCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 9)
        self.assertEqual(self.statement.start_balance, 0.0)
        self.assertAlmostEqual(self.statement.end_balance, -1572.84)
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "AT123456789012345678")
        self.assertEqual(self.statement.start_date, datetime.datetime(2014, 1, 1, 0, 0))
        self.assertEqual(self.statement.end_date, datetime.datetime(2014, 2, 28, 0, 0))

    def test_line0_interest_paid(self):
        l = self.statement.lines[0]
        self.assertEqual(l.check_no, "1")
        self.assertEqual(l.amount, -0.42)
        self.assertEqual(l.memo, "Einbehaltene KESt")
        self.assertEqual(l.payee, l.memo)
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 1, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line1_interest_earned(self):
        l = self.statement.lines[1]
        self.assertEqual(l.check_no, "2")
        self.assertEqual(l.amount, 1.23)
        self.assertEqual(l.memo, "Zinsen HABEN")
        self.assertEqual(l.payee, l.memo)
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 1, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line2_debit_with_iban_bic(self):
        l = self.statement.lines[2]
        self.assertEqual(l.check_no, "3")
        self.assertEqual(l.amount, -123.45)
        self.assertEqual(l.memo, "Usage, specific reason")
        self.assertEqual(l.payee, "Payment receiver (AT098765432109876543 ABCDEF1G235)")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 4, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line3_debit_legacy_bank_account(self):
        l = self.statement.lines[3]
        self.assertEqual(l.check_no, "4")
        self.assertEqual(l.amount, -32)
        self.assertEqual(l.memo, "Abbuchung Einzugsermächtigung")
        self.assertEqual(l.payee, "Amazon *Mktplce EU-AT (01234567890 01234)")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 8, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line4_debit_iban_only(self):
        l = self.statement.lines[4]
        self.assertEqual(l.check_no, "5")
        self.assertEqual(l.amount, -1001.00)
        self.assertEqual(l.memo, "CustomerNo: XXXXX OrderNr: YYYYYYYY")
        self.assertEqual(l.payee, "Payment receiver (AT098765432109876543)")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 19, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line5_debit_withdraw(self):
        l = self.statement.lines[5]
        self.assertEqual(l.check_no, "6")
        self.assertEqual(l.amount, -400)
        self.assertEqual(l.memo, "Auszahlung Maestro 10.01")
        self.assertEqual(l.payee, "AUTOMAT 01234567 K1 27.07.UM 18.57")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 28, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line6_debit_with_more_text_before_check_no(self):
        l = self.statement.lines[6]
        self.assertEqual(l.check_no, "7")
        self.assertEqual(l.amount, -20.9)
        self.assertEqual(l.memo, "XYZ INVOICE 01/14 123456789012345")
        self.assertEqual(l.payee, "Foobar XZY service AG (AT098765432109876543 ABCDEF1G235)")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 1, 31, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line7_debit_with_more_text_before_check_no_and_without_banking_infos(self):
        l = self.statement.lines[7]
        self.assertEqual(l.check_no, "8")
        self.assertEqual(l.amount, -8.4)
        self.assertEqual(l.memo, "AT 8,40 DEBIT POS 18.0 5.14 10.08K1")
        self.assertEqual(l.payee, "Somebody someony somewhere")
        self.assertEqual(l.trntype, "DEBIT")
        self.assertEqual(l.date, datetime.datetime(2014, 2, 21, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

    def test_line8_credit_iban_bic(self):
        l = self.statement.lines[8]
        self.assertEqual(l.check_no, "9")
        self.assertEqual(l.amount, 12.1)
        self.assertEqual(l.memo, "Gutschrift Überweisung")
        self.assertEqual(l.payee, "Some person (AT098765432109876543 ABCDEF1G235)")
        self.assertEqual(l.trntype, "CREDIT")
        self.assertEqual(l.date, datetime.datetime(2014, 2, 28, 0, 0))
        self.assertEqual(l.id, generate_transaction_id(l))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
