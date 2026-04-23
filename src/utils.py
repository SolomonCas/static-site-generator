import re
import os

from htmlnode import LeafNode, ParentNode, HTMLNode
from textnode import TextType, TextNode
from blocktype import BlockType


def text_node_to_html_node(text_node):
    if not TextType(text_node.text_type):
        raise Exception("Not a valid TextType")

    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    return LeafNode(None, text_node.text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("Invalid markdown syntax")
            
            for i in range(0, len(split_text)):
                if i % 2 == 1:
                    new_list.append(TextNode(split_text[i], text_type))
                elif split_text[i].strip() != "":
                    new_list.append(TextNode(split_text[i], TextType.TEXT))
        else:
            new_list.append(node)
    return new_list

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_list = []

    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            image_list = extract_markdown_images(node.text)
            if len(image_list) < 1:
                new_list.append(node)
            else:
                split_text = []
                copy_text = node.text
                for key, value in image_list:
                    split_text = copy_text.split(f"![{key}]({value})", 1)
                    copy_text = split_text[1] if len(split_text) == 2 else ""

                    if len(split_text[0].strip()) > 0:
                        new_list.append(TextNode(split_text[0], TextType.TEXT))
                    new_list.append(TextNode(key, TextType.IMAGE, value))

                if len(copy_text.strip()) > 0:
                    new_list.append(TextNode(copy_text, TextType.TEXT))
                    
        else:
            new_list.append(node)
    return new_list

def split_nodes_link(old_nodes):
    new_list = []

    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            link_list = extract_markdown_links(node.text)
            if len(link_list) < 1:
                new_list.append(node)
            else:
                split_text = []
                copy_text = node.text
                for key, value in link_list:
                    split_text = copy_text.split(f"[{key}]({value})", 1)
                    copy_text = split_text[1] if len(split_text) == 2 else ""

                    if len(split_text[0].strip()) > 0:
                        new_list.append(TextNode(split_text[0], TextType.TEXT))
                    new_list.append(TextNode(key, TextType.LINK, value))

                if len(copy_text.strip()) > 0:
                    new_list.append(TextNode(copy_text, TextType.TEXT))
                    
        else:
            new_list.append(node)
    return new_list

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip(), blocks)))
    
def block_to_block_type(block):
    is_quote = True
    is_unordered = True
    is_ordered = True
    split_block = block.split("\n")


    if re.match(r"^(#{1,6})\s+(.*)", block):
        return BlockType.HEADING
    if re.match(r"^```[^\n]*\n[\s\S]*?\n```$", block):
        return BlockType.CODE

    for line in split_block:
        is_quote = re.match(r">", line)
        is_unordered = re.match(r"- ", line)
        is_ordered = re.match(r". ", line)
    
    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED
    if is_ordered:
        return BlockType.ORDERED
    

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text) 
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            match = re.match(r"^(#{1,6})\s+(.*)", block)
            level = len(match.group(1))
            content = match.group(2)
            children = text_to_children(content)
            node = ParentNode(f"h{level}", children=children)

        elif block_type == BlockType.CODE:
            # remove ```
            content = block.strip("```").strip("\n")

            text_node = TextNode(content + "\n", TextType.TEXT)
            code_child = text_node_to_html_node(text_node)

            code_node = ParentNode("code", children=[code_child])
            node = ParentNode("pre", children=[code_node])

        elif block_type == BlockType.QUOTE:
            content = "\n".join([line.lstrip("> ").strip() for line in block.split("\n")])
            children = text_to_children(content)
            node = ParentNode("blockquote", children=children)

        elif block_type == BlockType.UNORDERED:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                content = item.lstrip("- ").strip()
                children = text_to_children(content)
                li_nodes.append(ParentNode("li", children=children))
            node = ParentNode("ul", children=li_nodes)

        elif block_type == BlockType.ORDERED:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                content = re.sub(r"^\d+\.\s*", "", item)
                children = text_to_children(content)
                li_nodes.append(ParentNode("li", children=children))
            node = ParentNode("ol", children=li_nodes)

        else:
            children = text_to_children(block.replace("\n", " "))
            node = ParentNode("p", children=children)


        parent.children.append(node)

    return parent

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    header1 = None

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            match = re.match(r"^(#{1,6})\s+(.*)", block)
            level = len(match.group(1))
            if level == 1:
                header1 = match.group(2)

    if header1 == None:
        raise Exception("No Title found")

    return header1

