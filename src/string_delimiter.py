from textnode import TextNode, TextType
from extract_markdown_images_links import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            chunks = node.text.split(delimiter)
            if len(chunks) % 2 == 0:
                raise Exception("missing delimiter- invalid Markdown syntax")
            for i, chunk in enumerate(chunks):
                if i % 2 == 0:
                    new_nodes.append(TextNode(chunk, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(chunk, text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)

            if len(images) == 0:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for image_alt, image_url in images:
                    image_markdown = f"![{image_alt}]({image_url})"
                    parts = remaining_text.split(image_markdown, 1)

                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))

                    new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

                    if len(parts) > 1:
                        remaining_text = parts[1]
                    else:
                        remaining_text = ""

                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)

            if len(links) == 0:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for link_text, link_url in links:
                    link_markdown = f"[{link_text}]({link_url})"
                    parts = remaining_text.split(link_markdown, 1)

                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))

                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

                    if len(parts) > 1:
                        remaining_text = parts[1]
                    else:
                        remaining_text = ""

                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))

        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes