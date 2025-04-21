class HTMLNode:
    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == {} or self.props is None:
            return ""
        
        def format_prop(item):
            key, value = item
            return f' {key}="{value}"'
        
        formatted_props = map(format_prop, self.props.items())
        
        return "".join(formatted_props)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        if value is None:
            raise ValueError("A LeafNode must have a value")
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value to render")
        if not self.tag:
            return self.value
        props_string = self.props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        concatenate_child_nodes = ""

        for child in self.children:
            child_html = child.to_html()
            concatenate_child_nodes += child_html
        return f"<{self.tag}{self.props_to_html()}>{concatenate_child_nodes}</{self.tag}>" 

        
        
