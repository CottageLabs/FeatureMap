import json
import os

from featuremap.models import Serialiser

class JSONSerialiser(Serialiser):

    def serialise(self, data):
        j = json.dumps(data.as_dict(), indent=2)
        container = self.create_my_directory()
        out = os.path.join(container, "featuremap.json")
        with open(out, "w", encoding="utf-8") as f:
            f.write(j)
