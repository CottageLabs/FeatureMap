import os

from featuremap.models import Serialiser

from jinja2 import Environment
from jinja2 import FileSystemLoader


class HTMLSerialiser(Serialiser):
    """
    ~~HTML:Serialiser->Serialiser:Serialiser~~
    ~~-> Analysis:Model ~~
    ~~-> Jinja2:Tech ~~
    """

    def serialise(self, data):
        container = self.create_my_directory()

        env = Environment()
        env.loader = FileSystemLoader(self.my_config.get("template_dirs", []))
        env.globals["config"] = self.global_config

        for template_name, path in self.my_config.get("templates", {}).items():
            template = env.get_template(path)
            # with open(path, "r", encoding="utf-8") as f:
            #     template = env.from_string(f.read())

            page = template.render(data=data, page=template_name)

            outfile = os.path.join(container, template_name + ".html")
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(page)