from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective


class playground(nodes.General, nodes.Element):
    pass


class Playground(SphinxDirective):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
        "title": directives.unchanged,
        "height": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self):
        return [
            playground(
                embed_link=self.arguments[0],
                title=self.options.get("title"),
                height=self.options.get("height"),
                width=self.options.get("width"),
            )
        ]


def embed_playground(self, node):

    title = node["title"]
    height = node["height"] or 500
    width = node["width"] or "100%"
    id = '-'.join(title.split(' ')).lower()

    url = "/".join(
        [
            self.config['playground_options']['url'],
            '?github.com',
            self.config["playground_options"]["github_repo"],
            "blob",
            self.config["playground_options"]["commit_sha"],
            node["embed_link"],
        ]
    )

    embed_code = f"""
<iframe
  src="{url}"
  loading="lazy"
  allow="fullscreen"
  id="p-embed-{id}"
  class="p-embed-iframe"
  name="p-embed-{id}"
  width="{width}"
  height="{height}"
  style="border: 1px solid #ddd;"
  title="{title}"
></iframe>"""

    self.body.append(embed_code)

    raise nodes.SkipNode


def setup(app: Sphinx):
    app.add_node(playground, html=(embed_playground, None))

    if not app.config["playground_options"]["commit_sha"]:
        raise ExtensionError("Commit SHA is needed.")

    app.add_config_value(
        "playground_options", {"commit_sha": None, "github_repo": None, 'url': None}, "html"
    )
    app.add_directive("playground", Playground)

    return {"version": "0.1.0", "parallel_read_safe": True, "parallel_write_safe": True}
