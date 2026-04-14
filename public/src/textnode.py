from enum import Enum

class TextType(Enum):
    PLAIN = "plain_text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    CODE = "code_text"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = TextType(text_type) 
        self.url = url if url is not None and (TextType.LINK.value == text_type or TextType.Image.value) else None

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
