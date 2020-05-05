#!/usr/bin/env python3
# This file is part of ofxstatement-austrian.
# See README.rst for more information.

import datetime
from decimal import Decimal
import os
import unittest
from ofxstatement.statement import generate_transaction_id

from ofxstatement.plugins.easybank \
    import EasybankCreditCardCsvParser, EasybankGiroCsvParser


class TestEasybankCreditCardCsvParser(unittest.TestCase):
    """Unit tests for EasybankCreditCardCsvParser."""

    def setUp(self):
        csvfile = os.path.join(
            os.path.dirname(__file__), 'samples', 'easybank-creditcard.csv')
        with open(csvfile, 'r', encoding='cp1252') as fin:
            self.statement = EasybankCreditCardCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 3)
        self.assertEqual(self.statement.start_balance, Decimal('0.0'))
        self.assertEqual(self.statement.end_balance, Decimal('2.31'))
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "12345678901")
        self.assertEqual(
            self.statement.start_date, datetime.datetime(2013, 2, 19, 0, 0))
        self.assertEqual(
            self.statement.end_date, datetime.datetime(2013, 7, 2, 0, 0))

    def test_line0_debit(self):
        line = self.statement.lines[0]
        self.assertEqual(line.amount, Decimal('-5.99'))
        self.assertEqual(line.memo, "Some vendor/info")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2013, 7, 2, 0, 0))
        self.assertEqual(line.id, "12345678909876543212345")

    def test_line1_credit(self):
        line = self.statement.lines[1]
        self.assertEqual(line.amount, Decimal('30.99'))
        self.assertEqual(line.memo, "Another vendor")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2013, 6, 21, 0, 0))
        self.assertEqual(line.id, "23456789098765432123456")

    def test_line2_debit_with_foreign_currency(self):
        line = self.statement.lines[2]
        self.assertEqual(line.amount, Decimal('-22.69'))
        self.assertEqual(line.memo, "Someone (GBP 22,89)")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2013, 2, 19, 0, 0))
        self.assertEqual(line.id, "34567890987654321234567")


class TestEasybankGiroCsvParser(unittest.TestCase):
    """Unit tests for EasybankGiroCsvParser."""

    def setUp(self):
        csvfile = os.path.join(
            os.path.dirname(__file__), 'samples', 'easybank-giro.csv')
        with open(csvfile, 'r', encoding='cp1252') as fin:
            self.statement = EasybankGiroCsvParser(fin).parse()

    def test_statement_properties(self):
        self.assertEqual(len(self.statement.lines), 10)
        self.assertEqual(self.statement.start_balance, Decimal('0.0'))
        self.assertEqual(self.statement.end_balance, Decimal('-1562.86'))
        self.assertEqual(self.statement.currency, "EUR")
        self.assertEqual(self.statement.account_id, "AT123456789012345678")
        self.assertEqual(
            self.statement.start_date, datetime.datetime(2014, 1, 1, 0, 0))
        self.assertEqual(
            self.statement.end_date, datetime.datetime(2015, 10, 7, 0, 0))

    def test_line0_interest_paid(self):
        line = self.statement.lines[0]
        self.assertEqual(line.check_no, "1")
        self.assertEqual(line.amount, Decimal('-0.42'))
        self.assertEqual(line.memo, "Einbehaltene KESt")
        self.assertEqual(line.payee, line.memo)
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 1, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line1_interest_earned(self):
        line = self.statement.lines[1]
        self.assertEqual(line.check_no, "2")
        self.assertEqual(line.amount, Decimal('1.23'))
        self.assertEqual(line.memo, "Zinsen HABEN")
        self.assertEqual(line.payee, line.memo)
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 1, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line2_debit_with_iban_bic(self):
        line = self.statement.lines[2]
        self.assertEqual(line.check_no, "3")
        self.assertEqual(line.amount, Decimal('-123.45'))
        self.assertEqual(line.memo, "Usage, specific reason")
        self.assertEqual(
            line.payee, "Payment receiver (AT098765432109876543 ABCDEF1G235)")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 4, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line3_debit_legacy_bank_account(self):
        line = self.statement.lines[3]
        self.assertEqual(line.check_no, "4")
        self.assertEqual(line.amount, Decimal('-32'))
        self.assertEqual(line.memo, "Abbuchung Einzugsermächtigung")
        self.assertEqual(line.payee, "Amazon *Mktplce EU-AT (01234567890 01234)")  # noqa: E501
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 8, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line4_debit_iban_only(self):
        line = self.statement.lines[4]
        self.assertEqual(line.check_no, "5")
        self.assertEqual(line.amount, Decimal('-1001.00'))
        self.assertEqual(line.memo, "CustomerNo: XXXXX OrderNr: YYYYYYYY")
        self.assertEqual(line.payee, "Payment receiver (AT098765432109876543)")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 19, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line5_debit_withdraw(self):
        line = self.statement.lines[5]
        self.assertEqual(line.check_no, "6")
        self.assertEqual(line.amount, Decimal('-400'))
        self.assertEqual(line.memo, "Auszahlung Maestro 10.01")
        self.assertEqual(line.payee, "AUTOMAT 01234567 K1 27.07.UM 18.57")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 28, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line6_debit_with_more_text_before_check_no(self):
        line = self.statement.lines[6]
        self.assertEqual(line.check_no, "7")
        self.assertEqual(line.amount, Decimal('-20.9'))
        self.assertEqual(line.memo, "XYZ INVOICE 01/14 123456789012345")
        self.assertEqual(
            line.payee,
            "Foobar XZY service AG (AT098765432109876543 ABCDEF1G235)")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 1, 31, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line7_debit_with_more_text_before_check_no_and_without_banking_infos(self):    # NOQA
        line = self.statement.lines[7]
        self.assertEqual(line.check_no, "8")
        self.assertEqual(line.amount, Decimal('-8.4'))
        self.assertEqual(line.memo, "AT 8,40 DEBIT POS 18.0 5.14 10.08K1")
        self.assertEqual(line.payee, "Somebody someony somewhere")
        self.assertEqual(line.trntype, "DEBIT")
        self.assertEqual(line.date, datetime.datetime(2014, 2, 21, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line8_credit_iban_bic(self):
        line = self.statement.lines[8]
        self.assertEqual(line.check_no, "9")
        self.assertEqual(line.amount, Decimal('12.1'))
        self.assertEqual(line.memo, "Gutschrift Überweisung")
        self.assertEqual(
            line.payee, "Some person (AT098765432109876543 ABCDEF1G235)")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2014, 2, 28, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

    def test_line9_memo_starts_with_forward_slash(self):
        line = self.statement.lines[9]
        self.assertEqual(line.check_no, "10")
        self.assertEqual(line.amount, Decimal('9.98'))
        self.assertEqual(line.memo, "/INV/123456790 1.10.2015")
        self.assertEqual(
            line.payee, "Some company (AT098765432109876543 ABCDEF12345)")
        self.assertEqual(line.trntype, "CREDIT")
        self.assertEqual(line.date, datetime.datetime(2015, 10, 7, 0, 0))
        self.assertEqual(line.id, generate_transaction_id(line))

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
