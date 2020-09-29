import subprocess
import xml.sax
import mwparserfromhell
import string
import os

import timeit

from helper import binary_search_recursive

masculine_nouns = []
feminine_nouns = []

noun_file_path = "nouns/nouns.txt"
with open(noun_file_path, 'r') as noun_file:
    for line in noun_file:
        if line.split()[2][2] == 'M':
            masculine_nouns.append(line.split()[0])
        elif line.split()[2][2] == 'F':
            feminine_nouns.append(line.split()[0])


def count_nouns_in_page(page):

    wiki = mwparserfromhell.parse(page[1])
    words = wiki.strip_code(normalize=True).split()

    number_of_masculine_words = 0
    number_of_feminine_words = 0

    for word in words:
        stripped_word = word.lower().translate(str.maketrans('', '', string.punctuation))
        if stripped_word == "":
            continue
        if binary_search_recursive(masculine_nouns, stripped_word, 0, len(masculine_nouns)):
            number_of_masculine_words += 1
        elif binary_search_recursive(feminine_nouns, stripped_word, 0, len(feminine_nouns)):
            number_of_feminine_words += 1

    return [number_of_masculine_words, number_of_feminine_words]


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""

    def __init__(self, _output_file):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self.output_file = _output_file

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            try:
                counts = count_nouns_in_page((self._values['title'], self._values['text']))
                self.output_file.write(f"{counts[0]} {counts[1]} {self._values['title']}\n")
            except mwparserfromhell.parser.ParserError:
                # Unknown error occurs, so ignore pages with this error.
                self.output_file.write(f"- - {self._values['title']}\n")


for data_file_name in os.listdir("downloads/"):

    data_path = "downloads/" + data_file_name
    output_file_path = "counts/" + data_file_name.split(".")[0] + "-" + data_file_name.split(".")[1] + ".txt"

    start_time = timeit.default_timer()

    print(f"Analysing {data_file_name}")

    with open(output_file_path, "w") as output_file:

        # Object for handling xml
        handler = WikiXmlHandler(output_file)

        # Parsing object
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)

        # Iteratively process file
        for line in subprocess.Popen(['bzcat'],
                                     stdin=open(data_path),
                                     stdout=subprocess.PIPE).stdout:
            parser.feed(line)

    print("Successful: ", timeit.default_timer() - start_time, "seconds")