import os
import csv

from featuremap.models import Serialiser
from featuremap import metrics


class CSVSerialiser(Serialiser):
    """
    ~~CSV:Serialiser->Serialiser:Serialiser~~
    ~~-> Analysis:Model ~~
    ~~-> Config:Config ~~
    """
    def serialise(self, data):

        container = self.create_my_directory()

        relationships = os.path.join(container, "relationships.csv")
        with open(relationships, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for k, relation in data.relations.items():
                for rel, targets in relation.refs.items():
                    for target, occurrences in targets.items():
                        refs, urls = self._file_refs(occurrences)
                        writer.writerow([k, rel, target, "; ".join(refs), "; ".join(urls)])

        filelist = os.path.join(container, "files.csv")
        with open(filelist, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            writer.writerow(["File Path", "Annotation Count", "Line Count", "Completion Metric"])
            for k, v in data.files.items():
                writer.writerow([k, v.get("annotations"), v.get("total_lines"), metrics.completion_metric(v.get("annotations"), v.get("total_lines"))])

        entities = os.path.join(container, "entities.csv")
        with open(entities, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for k, v in data.entities.items():
                refs, urls = self._file_refs(v)
                writer.writerow([k, "; ".join(refs), "; ".join(urls)])

        no_downstream = os.path.join(container, "no-downstream.csv")
        with open(no_downstream, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for target, entity_defs, relation_defs in data.no_downstreams:
                if entity_defs:
                    erefs, eurls = self._file_refs(entity_defs)
                else:
                    erefs, eurls = [], []

                if relation_defs:
                    rrefs, rurls = self._file_refs(relation_defs)
                else:
                    rrefs, rurls = [], []

                writer.writerow([target, "; ".join(erefs), "; ".join(eurls), "; ".join(rrefs), "; ".join(rurls)])

        unexpected_downstram = os.path.join(container, "unexpected-downstream.csv")
        with open(unexpected_downstram, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for target, entity_defs, relation_defs in data.unexpected_downstreams:
                if entity_defs:
                    erefs, eurls = self._file_refs(entity_defs)
                else:
                    erefs, eurls = [], []

                if relation_defs:
                    rrefs, rurls = self._file_refs(relation_defs)
                else:
                    rrefs, rurls = [], []

                writer.writerow([target, "; ".join(erefs), "; ".join(eurls), "; ".join(rrefs), "; ".join(rurls)])

        unseen_terminals = os.path.join(container, "unseen-terminals.csv")
        with open(unseen_terminals, "w", encoding="utf-8") as o:
            writer = csv.writer(o)
            for target in data.unseen_terminals:
                writer.writerow([target])

    def _file_refs(self, source):
        refs = [o["file"] + "#L" + str(o["line"]) for o in source]
        urls = []
        if self.global_config.get("source_url") is not None:
            urls = [self.global_config.get("source_url") + "/" + f for f in refs]
        return refs, urls
