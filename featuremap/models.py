import os

class Analysis(object):
    """
    ~~Analysis:Model~~
    """
    def __init__(self):
        self._relations = {}
        self._files = {}
        self._entities = {}
        self._targets = set()
        self._terminals = []

    @property
    def relations(self):
        return self._relations

    @property
    def files(self):
        return self._files

    @property
    def entities(self):
        return self._entities

    @property
    def targets(self):
        return self._targets

    @property
    def no_downstreams(self):
        nods = []
        for t in self._targets:
            if t not in self._relations and t not in self._terminals:
                ed = self.entity_definitions(t)
                rd = self.inverse_relation_definitions(t)
                nods.append((t, ed, rd))
        return nods

    @property
    def unexpected_downstreams(self):
        return [
            (
                t,
                self.entity_definitions(t),
                [
                    item for sublist in
                    [ot[3] for ot in self.relations.get(t).ordered_triples]
                    for item in sublist
                ] if self.relations.get(t) is not None else []
            )
            for t in self._terminals if t in self._relations
        ]

    @property
    def unseen_terminals(self):
        return [t for t in self._terminals if t not in self._targets]

    @property
    def terminals(self):
        return self._terminals

    @terminals.setter
    def terminals(self, val):
        self._terminals = val

    @property
    def ordered_triples(self):
        subjects = list(self._targets)
        subjects.sort()

        triples = []
        for s in subjects:
            relations = self._relations.get(s)
            if relations:
                relation_triples = relations.ordered_triples
                triples += relation_triples

            for _, r in self._relations.items():
                if s in r.targets:
                    triples += r.triples_for(s)

        return triples

    def inverse_relation_definitions(self, entity_name):
        irds = []
        for entity, definition in self.relations.items():
            if entity_name in definition.targets:
                for ref, entries in definition.refs.items():
                    if entity_name in entries:
                        irds += entries.get(entity_name)
        return irds

    def entity_definitions(self, entity_name):
        return self._entities.get(entity_name, [])

    def add_known_target(self, target):
        self._targets.add(target)

    def add_entity_definition(self, name, file, line):
        if name not in self._entities:
            self._entities[name] = []
        self._entities[name].append({
            "file" : file,
            "line" : line
        })
        self.add_known_target(name)

    def add_relation(self, name):
        #~~-> Relation:Model ~~
        if name not in self._relations:
            self._relations[name] = Relation(self, name)
        self.add_known_target(name)
        return self._relations[name]

    def add_file(self, filename, total_lines=0):
        if filename not in self._files:
            self._files[filename] = {"annotations" : 0, "total_lines" : total_lines}

    def annotation_hit(self, filename):
        self.add_file(filename)
        self._files[filename]["annotations"] += 1

    def set_total_lines(self, filename, total_lines):
        self.add_file(filename)
        self._files[filename]["total_lines"] = total_lines

    def as_dict(self):
        return {
            "relations": {k : v.as_dict() for (k, v) in self.relations.items()},
            "files": self.files,
            "entities": self.entities,
            "targets": list(self.targets),
            "terminals": self.terminals
        }


class Relation(object):
    """
    ~~Relation:Model~~
    """
    def __init__(self, analysis, name=None):
        # ~~-> Analysis:Model ~~
        self.analysis = analysis
        self.name = name
        self.refs = {}
        self.targets = []

    def add_ref(self, rel, target, file, line):
        if rel not in self.refs:
            self.refs[rel] = {}
        if target not in self.refs[rel]:
            self.refs[rel][target] = []
        self.refs[rel][target].append({
            "file": file,
            "line": line
        })
        self.targets.append(target)
        self.analysis.add_known_target(target)

    @property
    def ordered_triples(self):
        refs = list(self.refs.keys())
        refs.sort()

        triples = []
        for r in refs:
            objects = list(self.refs[r].keys())
            objects.sort()
            for o in objects:
                triples.append((self.name, r, o, self.refs[r][o]))

        return triples

    def triples_for(self, o):
        refs = list(self.refs.keys())
        refs.sort()

        triples = []
        for r in refs:
            if o not in self.refs[r]:
                continue
            triples.append((o, self._reverse(r), self.name, self.refs[r][o]))

        return triples

    def _reverse(self, rel):
        if rel == "->":
            return "<-"
        return "<- " + rel

    def as_dict(self):
        return {
            "name" : self.name,
            "refs" : self.refs,
            "targets" : self.targets
        }


class Serialiser(object):
    """
    ~~Serialiser:Serialiser~~
    """
    def __init__(self, global_config, serialiser_config):
        self.global_config = global_config
        self.my_config = serialiser_config

    def create_my_directory(self):
        od = self.global_config.get("out_dir")
        md = self.my_config.get("dir")
        container = os.path.join(od, md)
        if not os.path.exists(container):
            os.makedirs(container)
        return container

    def serialise(self, data):
        raise NotImplemented()