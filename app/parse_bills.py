__author__ = 'Alexey Y Manikin'

import argparse
import traceback

import classes.bill_parser

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Add help")
        parser.add_argument("file_name", help="Name of file")

        args = parser.parse_args()

        parser = classes.bill_parser.BillParser()
        parser.run(args.file_name)
    except Exception as e:
        print((traceback.format_exc()))
