#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
#
# Converts OCBC Bank's savings account CSV output into a proper CSV file for input to personal finance applications.
# 
# This runs on Python 3.9
#
# Copyright (c) 2018–2022, Sasmito Adibowo
# https://indiespark.top
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os.path
import csv
import datetime


OUTPUT_DATE_FORMAT = '%Y-%m-%d'


def reformat_date(date_str):
    day_str = date_str[0:2]
    month_str = date_str[3:5]
    year_str = date_str[6:10]
    date_obj = datetime.datetime(int(year_str), int(month_str), int(day_str))
    return date_obj.strftime(OUTPUT_DATE_FORMAT)


def run_convert(input_file_name, output_file_name):
    with open(input_file_name, 'r') as input_file, open(output_file_name, 'w') as output_file:
        csv_input = csv.reader(input_file)
        csv_output = csv.writer(output_file)

        # Skip until the header row
        for cur_input_row in csv_input:
            if len(cur_input_row) > 0 and cur_input_row[0] == 'Transaction date':
                break

        csv_output.writerow(['Transaction_Date', 'Value_Date', 'Withdrawal', 'Deposit', 'Type', 'Ref1'])

        transaction_ref1_str = None
        transaction_ref2_str = None
        prev_input_row = []

        for cur_input_row in csv_input:            
            do_write_row = False
            if len(prev_input_row) == 5:
                transaction_date_str = prev_input_row[0].strip()
                value_date_str = prev_input_row[0].strip()
                debit_amt_str = prev_input_row[3].strip()
                credit_amt_str = prev_input_row[4].strip()
                transaction_ref1_str = prev_input_row[2].strip()
                if len(cur_input_row) == 3:
                    transaction_ref2_str = cur_input_row[2].strip()
                    do_write_row = True
                elif len(cur_input_row) == 5:
                    transaction_ref2_str = None
                    do_write_row = True
            if do_write_row:
                csv_output.writerow([
                    reformat_date(transaction_date_str),
                    reformat_date(value_date_str),
                    debit_amt_str,
                    credit_amt_str,
                    transaction_ref1_str,
                    transaction_ref2_str                    
                ])
            prev_input_row = cur_input_row


def print_help():
    script_name = os.path.basename(__file__)
    text = ("\nReformat OCBC-360 Savings Account pseudo-CSV export into a proper CSV file.\n"
        "Usage:\n"
        "\t {0} {{input-file}} {{output-file}}\n"
        "Where:\n"
        "{{input-file}}\tThe file obtained from OCBC's `Export to CSV` function (the `download` button on the balance history screen).\n"
        "{{output-file}}\tWhere to write the properly-formatted CSV output file.\n"
    ).format(script_name)
    print(text)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_help()
        exit(2)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.isfile(input_file):
        print(f"Input file does not exists: {input_file}") 
        print_help()
        exit(3)
    if os.path.isfile(output_file):
        print(f"Output file already exists: {output_file}") 
        print_help()
        exit(3)
    run_convert(input_file, output_file)
    exit(0)

