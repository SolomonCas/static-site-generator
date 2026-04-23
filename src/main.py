from textnode import TextNode
from file_utils import generate_pages_recursive, copy_static_to_public

def main():
    # node = TextNode("This is some anchor text", "link", "https://www.bot.dev")
    # print(node)
    copy_static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")
#   generate_page("content/index.md", "template.html", "public/index.html")
#   generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
#   generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
#   generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
#   generate_page("content/contact/index.md", "template.html", "public/contact/index.html")


main()
