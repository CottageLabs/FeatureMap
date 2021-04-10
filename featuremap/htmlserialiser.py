import os

from featuremap.models import Serialiser

from jinja2 import Environment

class HTMLSerialiser(Serialiser):

    def serialise(self, data):
        container = self.create_my_directory()
        html_template = self.my_config.get("template")

        env = Environment()
        with open(html_template, "r", encoding="utf-8") as f:
            template = env.from_string(f.read())

        page = template.render(data=data)

        outfile = os.path.join(container, "index.html")
        outdir = os.path.dirname(outfile)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(page)