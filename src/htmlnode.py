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
