__author__ = 'Alexey Y Manikin'

__author__ = 'Alexey Y Manikin'

import traceback

import classes.llm_parser

if __name__ == '__main__':
    try:
        # llm_parser = LLMParser()
        # llm_parser.get_json_by_text("Хлеб - 9.80")
        # llm_parser.get_json_by_text("Алкоголь -403.16")
        # llm_parser.get_json_by_text("Продукты- 254.43")
        # llm_parser.get_json_by_text("Пылесос - 133")
        # llm_parser.get_json_by_text("Зарплата 210")
        # llm_parser.get_json_by_text("Расходные материалы - 41")
        # llm_parser.get_json_by_text("Расходные материалы - 21")
        # llm_parser.get_json_by_text("Зарплата - 600")
        # llm_parser.get_json_by_text("Хлеб - 9.8")
        # llm_parser.get_json_by_text("Продукты - 402")
        # llm_parser.get_json_by_text("Продукты - 125")
        # llm_parser.get_json_by_text("Продукты - 42")
        # llm_parser.get_json_by_text("Мороженое - 617")
        # llm_parser.get_json_by_text("Зарплата - 335")
        # llm_parser.get_json_by_text("Хлеб - 5.50")
        # llm_parser.get_json_by_text("Посуда - 99.45")
        # llm_parser.get_json_by_text("Продукты - 96.37")
        # llm_parser.get_json_by_text("Продукты 153.85")
        # llm_parser.get_json_by_text("Зарплата - 216")

        # pdf = classes.read_pdf.ReadPDF('/home/sofi/pdf_data/10_01_2024.pdf')
        # pdf.parse_text2()
        #
        # pdf.write_in_file('/home/sofi/pdf_data/10_01_2024.pdf.txt', pdf.format_output(pdf.parse_pdf()))
        # pdf.__del__()

        model = classes.llm_parser.LLMParser()
        result = model.test_model()
        pass

    except Exception as e:
        print((traceback.format_exc()))
