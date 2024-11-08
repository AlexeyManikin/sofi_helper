# Для считывания PDF
import PyPDF2


class ReadPDF(object):

    def __init__(self, path_to_file: str):
        self.pdf_path = path_to_file

    def parse_pdf(self) -> str:
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = "".join([reader.getPage(i).extractText() for i in range(reader.numPages)])
        return self.format_output(text)

    @staticmethod
    def format_output(income_text: str) -> str:
        text_per_page = income_text.split("\n")
        return_str = ""
        for text in text_per_page:
            if "app.ariapos.me" in text:
                continue
            if " Document" in text:
                continue
            return_str += text + "\n"
        return return_str

    @staticmethod
    def write_in_file(file_name: str, text: str):
        file = open(file_name, "w")
        file.write(text)
        file.close()
