__author__ = 'Alexey Y Manikin'

from pprint import pprint
from config.config import *
import config.model
import json
import requests
import MySQLdb
import traceback
from datetime import date
import time


class LLMParser(object):

    def __init__(self):
        self.connection = self.get_mysql_connection()

    def __del__(self):
        self.connection.close()

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

    @staticmethod
    def print_json(data):
        print(json.dumps(data, ensure_ascii=False, indent=2))

    @staticmethod
    def get_list_of_category() -> dict:
        group_category = {"grocery_shopping" : "продукты",
             "grocery_alco" : "алкоголь",
             "fixed_assets": "средства производства и траты на кафе",
             "salary": "выплаты зарплат",
             "add": "заработанные деньги"}
        return group_category

    @staticmethod
    def get_json_request(text: str, today: date) -> dict:
        # Подготовка запроса
        request_data = {
            "messages": [
                {
                    "role": "system",
                    "content": config.model.get_content_for_llm(today)
                 },
                {   "role": "user",
                    "content": text
                }
            ],
            "model": config.model.model_name,
            "max_tokens": 1000,
            "temperature": 0.0,
            "guided_json": json.dumps(config.model.json_schema),
            "guided_decoding_backend": "lm-format-enforcer",
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "top_p": 1,
            "n": 1,
            "stream": False
        }

        return request_data

    def get_llm_answer(self, today: date, text: str) -> dict:
        #today = date.today()
        request_data = self.get_json_request(text, today)
        start_time = time.time()
        response = requests.post(config.model.openai_api_url, json=request_data)
        end_time = time.time()

        try:
            if response.status_code == 200:
                result = response.json()
                content = json.loads(result['choices'][0]['message']['content'])
                content['usage'] = {}
                content['usage']['prompt_tokens'] = result['usage']['prompt_tokens']
                content['usage']['total_tokens'] = result['usage']['total_tokens']
                content['usage']['completion_tokens'] = result['usage']['completion_tokens']
                content['usage']['elapsed_time'] = end_time - start_time

                if content['group'] == 'salary':
                    content['type_s'] = 'del'

                content['request_data'] = {}
                content['request_data']['request_data'] = request_data
                content['request_data']['code'] = response.status_code
                content['request_data']['response'] = result

                return content
            else:
                return {}
        except Exception as e:
            print(response.text)
            print((traceback.format_exc()))
            return {}

    def insert_in_mysql_raw_data(self, text: str, message_date: int, message_sender: str) -> int:
        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            sql = "INSERT INTO raw_data_from_message(date_create, writer, messages, date_int, is_done) VALUE(NOW(), %s, %s, %s, 0) "
            cursor.execute(sql, (message_sender.encode('utf-8'), text.encode('utf-8'), str(message_date)))
            self.connection.commit()

            cursor.execute(
                """SELECT id FROM raw_data_from_message WHERE writer = %s AND messages = %s AND date_int = %s AND is_done = 0""", (
                message_sender, text, message_date))

            data = cursor.fetchone()
            return data['id']

        except Exception as e:
            print((traceback.format_exc()))
            return 0

    def insert_in_mysql_parsed_data(self, llm_data: dict, raw_id: int):
        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            sql =  """INSERT INTO cost_structure(date_create, raw_data_id, group_type, type, summ, date, description, model, promt, prompt_tokens, total_tokens, completion_tokens, elapsed_time, raw_answer, answer_code) VALUE(NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(sql, (raw_id,
                                 llm_data['group'].encode('utf-8'),
                                 llm_data['type_s'].encode('utf-8'),
                                 llm_data['summ'],
                                 llm_data['date'].encode('utf-8'),
                                 llm_data['description'].encode('utf-8'),
                                 config.model.model_name,
                                 json.dumps(llm_data['request_data']['request_data'], ensure_ascii=False, indent=2).encode('utf-8'),
                                 llm_data['usage']['prompt_tokens'],
                                 llm_data['usage']['total_tokens'],
                                 llm_data['usage']['completion_tokens'],
                                 llm_data['usage']['elapsed_time'],
                                 json.dumps(llm_data['request_data']['response'], ensure_ascii=False, indent=2).encode('utf-8'),
                                 llm_data['request_data']['code']
                                 ))
            self.connection.commit()

            cursor.execute("""SELECT id FROM cost_structure WHERE raw_data_id = %s""" % raw_id )
            data = cursor.fetchone()

            if data['id'] > 0:
                cursor.execute("""UPDATE raw_data_from_message SET is_done = 1 WHERE id = %s""" % raw_id)
                self.connection.commit()

            return data['id']
        except Exception as e:
            print((traceback.format_exc()))
            return 0

    def test_insert_in_mysql_parsed_data(self, llm_data: dict, raw_id: int):
        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            sql =  """INSERT INTO cost_structure_test(date_create, raw_data_id, group_type, type, summ, date, description, model, promt, prompt_tokens, total_tokens, completion_tokens, elapsed_time, raw_answer, answer_code) VALUE(NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(sql, (raw_id,
                                 llm_data['group'].encode('utf-8'),
                                 llm_data['type_s'].encode('utf-8'),
                                 llm_data['summ'],
                                 llm_data['date'].encode('utf-8'),
                                 llm_data['description'].encode('utf-8'),
                                 config.model.model_name,
                                 json.dumps(llm_data['request_data']['request_data'], ensure_ascii=False, indent=2).encode('utf-8'),
                                 llm_data['usage']['prompt_tokens'],
                                 llm_data['usage']['total_tokens'],
                                 llm_data['usage']['completion_tokens'],
                                 llm_data['usage']['elapsed_time'],
                                 json.dumps(llm_data['request_data']['response'], ensure_ascii=False, indent=2).encode('utf-8'),
                                 llm_data['request_data']['code']
                                 ))
            self.connection.commit()

            cursor.execute("""SELECT id FROM cost_structure_test WHERE raw_data_id = %s""" % raw_id )
            data = cursor.fetchone()

            if data['id'] > 0:
                self.connection.commit()

            return data['id']
        except Exception as e:
            print((traceback.format_exc()))
            return 0

    def parse_date(self, text: str, message_date: int, message_sender: str) -> dict:
        today = date.today()
        llm_data = self.get_llm_answer(today, text)
        if llm_data == {} or llm_data['summ'] == 0:
            return {}

        id = self.insert_in_mysql_raw_data(text, message_date, message_sender)
        data_id = self.insert_in_mysql_parsed_data(llm_data, id)

        llm_data['raw_id'] = id
        llm_data['data_id'] = data_id
        return llm_data

    def get_summary_row(self, days_count: int) -> int:
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            """SELECT sum(summ) AS summ FROM cost_structure WHERE type = 'del' AND date > DATE_ADD(NOW(), INTERVAL -%i DAY)""" % days_count)
        data = cursor.fetchone()
        return data['summ']

    def get_list_spending(self, days_count: int) -> dict:
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            """SELECT * FROM cost_structure WHERE date > DATE_ADD(NOW(), INTERVAL -%i DAY)""" % days_count)
        data = cursor.fetchall()
        return data

    def test_parse_date(self, today: date, raw_id: int,  text: str) -> dict:
        llm_data = self.get_llm_answer(today, text)
        if llm_data == {} or llm_data['summ'] == 0:
            return {}

        data_id = self.test_insert_in_mysql_parsed_data(llm_data, raw_id)
        llm_data['raw_id'] = raw_id
        llm_data['data_id'] = data_id
        return llm_data

    def test_model(self):
        try:
            cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("DELETE FROM cost_structure_test WHERE 1=1")
            cursor.execute("SELECT id, date_create, writer, messages FROM raw_data_from_message ORDER BY id")
            records = cursor.fetchall()

            for row in records:
                result = self.test_parse_date(row['date_create'], row['id'], row['messages'])
                if result != {}:
                    d = self.get_list_of_category()
                    try:
                        group = d[result['group']]
                    except KeyError:
                        group = result['group']

                    return_text = "Данные добавлены (%s): \n" % row['id'] + \
                                  "  - сумма: %s\n" % result['summ'] + \
                                  "  - группа: %s\n" % group + \
                                  "  - описание: %s\n" % result['description'] + \
                                  "  - дата: %s\n" % result['date'] + \
                                  "  - обоснование: %s\n\n" % result['reasoning']
                    print(return_text)
            return 0

        except Exception as e:
            print((traceback.format_exc()))
            return 0
