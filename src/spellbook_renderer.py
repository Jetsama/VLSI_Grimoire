from mistletoe.html_renderer import HtmlRenderer #, escape_url

from mistletoe.span_token import SpanToken
import re

class GithubWiki(SpanToken):
    pattern = re.compile(r"\[\[ *(.+?) *\| *(.+?) *\]\]")
    def __init__(self, match_obj):
        self.target = match_obj.group(2)

class SpellbookRenderer(HtmlRenderer):
    def __init__(self):
        super().__init__(GithubWiki)

    def render_github_wiki(self, token):
        template = '<a href="{target}">{inner}</a>'
        target = HtmlRenderer.escape_url(token.target)
        inner = self.render_inner(token)
        return template.format(target=target, inner=inner)



# small test case!
if __name__ == "__main__":
    from mistletoe import Document

    with open('foo.md', 'r') as fin:
        with SpellbookRenderer() as renderer:
            rendered = renderer.render(Document(fin))
            print(rendered)