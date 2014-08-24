#!/usr/bin/env python3
# This file is part of ofxstatement-austrian. See README.rst for more information.

def clean_multiple_whitespaces(uncleaned_string):
    """Clean a string from multiple consecutive white spaces."""
    return ' '.join(uncleaned_string.split())

def fix_amount_string(amount):
    """Replace »,« with ».« to make the amount parseable."""
    return amount.replace('.', '').replace(',', '.')

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent autoindent
