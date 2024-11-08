__author__ = 'Alexey Y Manikin'

import traceback
from datetime import datetime

import MySQLdb

from config.config import *
from config.template import *


class BillParser(object):

    def __init__(self):
        self.connection = self.get_mysql_connection()

    def __del__(self):
        self.connection.close()

    @staticmethod
    def load_from_file(filename) -> str:
        with open(filename, 'r') as f:
            s = f.read()
        return s

    @staticmethod
    def parce_dish(text: str) -> list:
        lines = re.split(r"\n", text)
        result_line = ""
        tmp_line = ""
        for line in lines:
            if re.match(re_dish_price_format, line):
                result_line = result_line + tmp_line.replace('\n', '') + '\n' + line
                tmp_line = ""
            else:
                tmp_line = tmp_line + " " + line

        dish_result = re.findall(re_dish_format, result_line)
        dish = []
        for dr in dish_result:
            data_dish = {'name': str(dr[0]).strip(), 'count': int(dr[1]), 'price': float(dr[2]), 'total': float(dr[3])}
            dish.append(data_dish)
        return dish

    def parce_text(self, text: str) -> list:
        result = re.findall(re_check_format, text)
        result_list = []
        for r in result:
            data = {'date': datetime.strptime(r[0], date_format2), 'bills_id': int(r[1])}

            try:
                data['bills_hash'] = re.findall(receipt_serial_number, r[2])[0]
            except:
                data['bills_hash'] = ""

            try:
                data['operator'] = str(re.findall(operator_name, r[2])[0]).strip()
            except:
                data['operator'] = ""

            try:
                data['operator_code'] = str(re.findall(operator_code, r[2])[0]).strip()
            except:
                data['operator_code'] = ""

            try:
                data['paid_by'] = str(re.findall(paid_by, r[2])[0]).strip()
            except:
                data['paid_by'] = ""

            try:
                data['table'] = str(re.findall(table_number, r[2])[0]).strip()
            except:
                data['table'] = ""

            data['dish'] = self.parce_dish(r[3])
            data['total'] = float(r[4].replace(" ", ""))
            data['total_discount'] = float(r[5].replace(" ", ""))
            result_list.append(data)

        return result_list

    @staticmethod
    def get_mysql_connection() -> MySQLdb.connect:
        connection = MySQLdb.connect(host=MYSQL_HOST,
                                     port=MYSQL_PORT,
                                     user=MYSQL_USER,
                                     db=MYSQL_DATABASE,
                                     passwd=MYSQL_PASSWD,
                                     use_unicode=True,
                                     charset="utf8")

        connection.query("SET SESSION wait_timeout = 3600000")
        connection.query("SET @@sql_mode:=TRADITIONAL")
        connection.autocommit(True)

        return connection

    def insert_into_table(self, list_orders: list) -> dict:
        count_bills = 0
        count_dish = 0
        count_bills_already_insert = 0

        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            for r in list_orders:
                cursor.execute("SELECT count(*) as count_in_base FROM bills WHERE bills_id = %s", (int(r['bills_id']),))

                count_in_base = cursor.fetchone()
                if count_in_base['count_in_base'] == 0:
                    sql = """INSERT INTO bills(date_create,bills_id,bills_hash,operator,
                        operator_code,paied_by,table_desc,total,total_discount) 
                        VALUE(STR_TO_DATE('%s', '%%Y-%%m-%%d %%H:%%i:%%s'), %s, %s, %s, %s, %s, %s, %s, %s)"""

                    cursor.execute(sql, ((str(r['date']),
                                          int(r['bills_id']),
                                          str(r['bills_hash']),
                                          str(r['operator']),
                                          str(r['operator_code']),
                                          str(r['paid_by']),
                                          str(r['table']),
                                          float(r['total']),
                                          float(r['total_discount']))))
                    count_bills += 1
                    for dr in r['dish']:
                        sql_dish = """INSERT INTO dishes(bills_id, name, item_count, price) VALUE( %s, %s, %s, %s)"""
                        cursor.execute(sql_dish,
                                       (int(r['bills_id']), str(dr['name']), int(dr['count']), float(dr['price'])))
                        count_dish += 1
                    self.connection.commit()
                else:
                    count_bills_already_insert += 1
        except Exception as e:
            print((traceback.format_exc()))
            print(e)

        return {"count_bills": count_bills, "count_dish": count_dish,
                "count_bills_already_insert": count_bills_already_insert}

    def run(self, file_name: str) -> dict:
        try:
            data = self.load_from_file(file_name)
            list_data = self.parce_text(data)
            return self.insert_into_table(list_data)
        except Exception as e:
            print((traceback.format_exc()))
            return {}
