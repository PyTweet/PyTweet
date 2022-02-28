"""A Custom extension featuring the required authorizations method!"""

from docutils import nodes

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

mapping = {
    "1": "Oauth 1.1: User Context",
    "2": "Oauth 2.0: Bearer Token",
    "3": "Oauth 2.0: Authorization Code with PKCE",
}

# Create the authorize object, inherits nodes.Admonition to look like info or warn directive.
class authorize(nodes.Admonition, nodes.Element):
    pass


def visit_authorize_node(self, node):
    self.visit_admonition(node)


def depart_authorize_node(self, node):
    self.depart_admonition(node)


# Create the directive.
class AuthorizeDirective(SphinxDirective):

    # this enables content in the directive
    has_content = True

    def run(self):
        raw_text = ""
        targetid = f"todo-{self.env.new_serialno('todo')}"
        targetnode = nodes.target("", "", ids=[targetid])

        codes = "\n".join(self.content).replace(",", "").split(" ")
        for code in codes:
            text = mapping.get(code)
            raw_text += f"{text}\n"
        self.arguments[1] = "EEEE"
        authorize_node = authorize("\n".join(self.arguments))
        authorize_node += nodes.title(_("Authorization Required"), _("Authorization Required"))
        self.state.nested_parse(self.content, self.content_offset, authorize_node)

        return [targetnode, authorize_node]


def purge_todos(app, env, docname):
    if not hasattr(env, "todo_all_todos"):
        return

    env.todo_all_todos = [todo for todo in env.todo_all_todos if todo["docname"] != docname]


def merge_todos(app, env, docnames, other):
    if not hasattr(env, "todo_all_todos"):
        env.todo_all_todos = []
    if hasattr(other, "todo_all_todos"):
        env.todo_all_todos.extend(other.todo_all_todos)


def setup(app):
    app.add_config_value("todo_include_todos", True, "html")
    app.add_node(
        authorize,
        html=(visit_authorize_node, depart_authorize_node),
        latex=(visit_authorize_node, depart_authorize_node),
        text=(visit_authorize_node, depart_authorize_node),
    )

    app.add_directive("authorize", AuthorizeDirective)
    app.connect("env-purge-doc", purge_todos)
    app.connect("env-merge-info", merge_todos)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
