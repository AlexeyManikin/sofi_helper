__author__ = 'Alexey Y Manikin'

import re

date_format = r'([0-9]{2}.[0-9]{2}.[0-9]{4}.\s[0-9]{2}:[0-9]{2}:[0-9]{2})'
date_format2 = r'(?:[0-9]{2}.[0-9]{2}.[0-9]{4}.\s[0-9]{2}:[0-9]{2}:[0-9]{2})'
text_string = r'(?:[\sa-zA-Z0-9]*):\s*[^\n]*\s*\n'
first_block = r'(Receipt serial number:\s(?:[0-9]+)\s*\nReceipt number:\n(?:[^\n]*)\nTime:\s%s\n(?:%s)*)' % (
    date_format2, text_string)

item_rate_price = r'[-]+\nItem \(Rate\) Price\n--[-]+\n((?:[^-]|[-])*?)\n--'
receipt_price = r'(?:[-]+\nReceipt Price\n[-]+\n(?:[^-]*)?-)?'
tipical_block = r'[-]+\n(?:(?:[^-]|[-])*?)\n--'
total_discount = r'[-]+\nTotal:\s*([^\n]*)\nDiscount:\s*([^\n]*)\n-'
check_format = r'Time:\s*%s\s*\nReceipt:\s*([0-9]{1,})\s*\n[=]*\s*\n(?:[^\n]*\n){6}[=]*\s*\n%s%s%s%s%s%s' % (
    date_format, first_block, item_rate_price, receipt_price, tipical_block, tipical_block, total_discount)
re_check_format = re.compile(check_format)

dish_price_format = r'([-]?\d+) x ([-]?\d+\.\d+) ([-]?\d+\.\d+)'
re_dish_price_format = re.compile(dish_price_format)
dish_format = r'([^\n]*)\n%s[\n]?' % dish_price_format
re_dish_format = re.compile(dish_format)

receipt_serial_number = re.compile(r'Receipt number:\n*\s([^\n]+)\s*\n')
operator_name = re.compile(r'Operator:\s([0-9a-zA-Z\s]+)\s*\n')
operator_code = re.compile(r'Operator code:\s([0-9a-zA-Z\s]+)\s*\n')
paid_by = re.compile(r'Paid by:\s([0-9a-zA-Z\s]+)\s*\n')
table_number = re.compile(r'Table:\s([0-9a-zA-Z\s]+)\s*\n')

date_format2 = '%d.%m.%Y. %H:%M:%S'
