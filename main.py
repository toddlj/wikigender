import subprocess
import xml.sax
import mwparserfromhell
import string


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


data_path = "downloads/enwiki-20200520-pages-articles-multistream1.xml-p1p30303.bz2"

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
    if len(handler._pages) > 2:
        break

# Create the wiki article
wiki = mwparserfromhell.parse(handler._pages[1][1])
words = wiki.strip_code(normalize=True).split()

for word in words:
    stripped_word = word.lower().translate(str.maketrans('', '', string.punctuation))
    if stripped_word == "":
        continue
    print(stripped_word)
