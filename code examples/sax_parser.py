import xml.sax
import xml.parsers.expat


class MyHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        print("startElement", name)
        p = xml.parsers.expat.ParserCreate()
        p.ParseFile()

    def endElement(self, name):
        print("endElement", name)

    def characters(self, text):
        print("characters", repr(text)[:40])


if __name__ == '__main__':
    xml.sax.parse("data/bus.xml", MyHandler())
