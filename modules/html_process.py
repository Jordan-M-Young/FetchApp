from bs4 import BeautifulSoup


class HtmlHandler():

    def __init__(self, filepath: str="",raw_html: str=""):
        """Initialize html handler, which handles parsing the incoming
        html file into text.
        """

        if filepath:
            self.filepath = filepath
            self.raw_html =  self.load_html()

        if raw_html:
            self.raw_html = raw_html


        if self.raw_html:
            self.parsed_html = self.parse_html()
            self.html_text = self.get_html_text()
            self.text_lines = self.html_text.split("\n")
            self.text_lines = remove_null_elements(self.text_lines)
        

    def load_html(self) -> str:
        #loads email html file to string

        with open(self.filepath, 'r') as html_file:
            return html_file.read()
        
    def parse_html(self) -> BeautifulSoup:
        # parses html string 

        return BeautifulSoup(self.raw_html, 'html.parser')

    def get_html_text(self) -> str:
        # returns text elements of parsed html object

        return self.parsed_html.get_text()


def remove_null_elements(input_list: list) -> list:
    # removes all null strings: '' from a list

    return [element for element in input_list if element != '']



