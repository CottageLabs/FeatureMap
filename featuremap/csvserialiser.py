import os
import csv

from featuremap.models import Serialiser

class CSVSerialiser(Serialiser):
    """
    ~~CSV:Serialiser~~
    ~~-> Analysis:Model ~~
    """
    def serialise(self, data):

        container = self.create_my_directory()

        relationships = os.path.join(container, "relationships.csv")
        with open(relationships, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for k, relation in data.relations.items():
                for rel, targets in relation.refs.items():
                    for target, occurrences in targets.items():
                        refs = "; ".join([o["file"] + "#L" + str(o["line"]) for o in occurrences])
                        writer.writerow([k, rel, target, refs])

        filelist = os.path.join(container, "files.csv")
        with open(filelist, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            writer.writerow(["File Path", "Annotation Count"])
            for k, v in data.files.items():
                writer.writerow([k, v])

        entities = os.path.join(container, "entities.csv")
        with open(entities, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for k, v in data.entities.items():
                refs = "; ".join([o["file"] + "#L" + str(o["line"]) for o in v])
                writer.writerow([k, refs])

        no_downstream = os.path.join(container, "no-downstream.csv")
        with open(no_downstream, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for target in data.no_downstreams:
                writer.writerow([target])

        unexpected_downstram = os.path.join(container, "unexpected-downstream.csv")
        with open(unexpected_downstram, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for target in data.unexpected_downstreams:
                writer.writerow([target])

        unseen_terminals = os.path.join(container, "unseen-terminals.csv")
        with open(unseen_terminals, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for target in data.unseen_terminals:
                writer.writerow([target])
