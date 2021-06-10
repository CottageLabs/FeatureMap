import os

from featuremap.models import Serialiser

from jinja2 import Environment
from jinja2 import FileSystemLoader


def rel2abs(file, *args):
    file = os.path.realpath(file)
    if os.path.isfile(file):
        file = os.path.dirname(file)
    return os.path.abspath(os.path.join(file, *args))


class HTMLSerialiser(Serialiser):
    """
    ~~HTML:Serialiser->Serialiser:Serialiser~~
    ~~-> Analysis:Model ~~
    ~~-> Jinja2:Tech ~~
    """
    DEFAULT_TEMPLATE_DIR = rel2abs(__file__, "..", "resources", "htmlserialiser", "templates")

    DEFAULT_TEMPLATES = {
        "relationships": "relationships.html",
        "entities": "entities.html",
        "files": "files.html",
        "no-downstream": "no-downstream.html",
        "unexpected-downstream": "unexpected-downstream.html",
        "unseen-terminals": "unseen-terminals.html"
    }

    def serialise(self, data):
        container = self.create_my_directory()

        env = Environment()
        env.loader = FileSystemLoader(self.my_config.get("template_dirs", [self.DEFAULT_TEMPLATE_DIR]))
        env.globals["config"] = self.global_config

        for template_name, path in self.my_config.get("templates", self.DEFAULT_TEMPLATES).items():
            template = env.get_template(path)
            page = template.render(data=data, page=template_name)
            outfile = os.path.join(container, template_name + ".html")
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(page)