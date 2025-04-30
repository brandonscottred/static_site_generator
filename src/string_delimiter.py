from textnode import TextNode, TextType

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
