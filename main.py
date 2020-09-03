import subprocess
import xml.sax
import mwparserfromhell
import string

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


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []

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
            self._pages.append((self._values['title'], self._values['text']))


data_path = "downloads/eswiki-20200901-pages-articles-multistream1.xml-p1p143637.bz2"

# Object for handling xml
handler = WikiXmlHandler()

# Parsing object
parser = xml.sax.make_parser()
parser.setContentHandler(handler)

# Iteratively process file
for line in subprocess.Popen(['bzcat'],
                             stdin=open(data_path),
                             stdout=subprocess.PIPE).stdout:
    parser.feed(line)

    # Stop when 3 articles have been found
    if len(handler._pages) > 1:
        break

for page_index in range(1, 2):
    start_time = timeit.default_timer()

    # Create the wiki article
    wiki = mwparserfromhell.parse(handler._pages[page_index][1])
    print(handler._pages[page_index][0])
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

    print(number_of_masculine_words, "masculine words")
    print(number_of_feminine_words, "feminine words")

    print("time", timeit.default_timer() - start_time, "seconds")
