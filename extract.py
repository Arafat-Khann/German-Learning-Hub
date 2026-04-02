from html.parser import HTMLParser
import os
import json

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = set()
        self.current_tag = None
        self.skip_tags = {'script', 'style', 'code', 'svg', 'path'}

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text and len(text) > 1 and not text.isdigit():
                self.texts.add(text)

all_texts = set()
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            parser = TextExtractor()
            parser.feed(content)
            all_texts.update(parser.texts)

print(json.dumps(list(all_texts), indent=2))
