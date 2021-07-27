import os
import fnmatch
import re
import csv

from featuremap.exceptions import MapException
from featuremap.models import Analysis
from featuremap.lex import parser
from featuremap import plugin


def parse_tree(config, analysis):
    """
    ~~ParseTree:Core~~
    :param config:
    :param analysis:
    :return:
    """

    # ~~->$ Config:Config~~
    directory = config.get("base_dir")
    exclude_dirs = config.get("exclude_dirs", [])
    exclude = config.get("exclude", [])
    include = config.get("include", [])

    for root, dirs, files in os.walk(directory):
        skip = False
        for ed in exclude_dirs:
            chd = os.path.join(directory, ed)
            if root.startswith(chd):
                skip = True
                break
        if skip:
            continue

        for name in files:
            path = os.path.join(root, name)
            excluded = False

            for exclude_pattern in exclude:
                if fnmatch.fnmatch(path, os.path.join(".", exclude_pattern)):
                    excluded = True
                    break

            included = False
            for incf in include:
                if fnmatch.fnmatch(path, os.path.join(".", incf)):
                    included = True

            if excluded and not included:
                continue

            # ~~->ParseFile:Core ~~
            parse_file(config, path, analysis)


def parse_file(config, file, analysis):
    """
    ~~ParseFile:Core~~
    :param config:
    :param file:
    :param analysis:
    :return:
    """

    # ~~-> Config:Config~~
    valid_types = config.get("valid_types", [])
    type_validation = config.get("type_validation", "none")
    ignore_parse_errors = file in [os.path.join(config.get("base_dir"), x) for x in config.get("ignore_parse_errors", [])]

    delimiter = config.get("delimiter", "~~")
    rx = delimiter + "(.+)" + delimiter

    # ~~->Analysis:Model~~
    analysis.add_file(file)
    with open(file, "r") as f:
        context = False
        last_entity = False
        ln = 0
        try:
            for line in f:
                ln += 1
                if delimiter in line:
                    m = re.findall(rx, line)
                    if not m:
                        continue
                    for annotation in m:
                        analysis.annotation_hit(file)

                        try:
                            # ~~-> ParseReference:Core ~~
                            ref = parse_reference(annotation)
                        except MapException as e:
                            # ~~-> MapException:Exception ~~
                            if ignore_parse_errors:
                                continue
                            e.file = f.name
                            e.line = ln
                            raise

                        new_context, new_last_entity = _apply_operation(ref, valid_types, type_validation, f, ln, analysis, context, last_entity)
                        if new_context is not None:
                            context = new_context
                        if new_last_entity is not None:
                            last_entity = new_last_entity

        except UnicodeDecodeError as e:
            print("UnicodeDecodeError on file {f}".format(f=file))


def _apply_operation(ref, valid_types, type_validation, f, ln, analysis, original_context, original_last_entity):
    new_context = None
    last_entity = None

    if "context" in ref:
        context = ref["context"]

        try:
            # ~~-> ValidateEntity:Core~~
            validate_entity(context, valid_types, type_validation)
        except MapException as e:
            # ~~-> MapException:Exception ~~
            e.file = f.name
            e.line = ln
            raise

        analysis.add_entity_definition(context, f.name, ln)
        last_entity = context

        if ref.get("switch_context", False):
            new_context = context

        if "rel" in ref and "target" in ref:
            try:
                validate_entity(ref["target"], valid_types, type_validation)
            except MapException as e:
                # ~~-> MapException:Exception ~~
                e.file = f.name
                e.line = ln
                raise

            relation = analysis.add_relation(context)
            relation.add_ref(ref["rel"], ref["target"], f.name, ln)

            if ref.get("register_relation_as_entity", False):
                analysis.add_entity_definition(ref["target"], f.name, ln)
                last_entity = ref["target"]

    else:
        try:
            validate_entity(ref["target"], valid_types, type_validation)
        except MapException as e:
            # ~~-> MapException:Exception ~~
            e.file = f.name
            e.line = ln
            raise

        if ref.get("register_on_last_entity", False):
            if not original_last_entity:
                # ~~-> MapException:Exception ~~
                raise MapException("No previously defined entity set when annotation provided", f.name, ln)
            relation = analysis.add_relation(original_last_entity)
        else:
            if not original_context:
                # ~~-> MapException:Exception ~~
                raise MapException("Context not set when annotation provided", f.name, ln)
            relation = analysis.add_relation(original_context)
        relation.add_ref(ref["rel"], ref["target"], f.name, ln)

        if ref.get("register_relation_as_entity", False):
            analysis.add_entity_definition(ref["target"], f.name, ln)
            last_entity = ref["target"]

    return new_context, last_entity


def validate_entity(entity, valid_types, type_validation):
    """
    ~~ValidateEntity:Core~~
    :param entity:
    :param valid_types:
    :param type_validation:
    :return:
    """
    if type_validation == "none":
        return True
    type = entity.split(":")[1]
    if type in valid_types:
        return True
    if type_validation == "error":
        # ~~-> MapException:Exception ~~
        raise MapException("Type '{x}' is not an allowed type".format(x=type))


def parse_reference(text):
    """
    ~~ParseReference:Core~~
    :param text:
    :return:
    """
    try:
        #~~->Parser:Core~~
        tree = parser.parse(text.strip())
    except:
        #~~-> MapException:Exception ~~
        raise MapException("Unable to parse text '{x}'".format(x=text))

    resp = {
        "switch_context" : True,
        "register_on_last_entity": False,
        "register_relation_as_entity" : False
    }
    for child in tree.children:
        field_name = child.data
        field_value = child.children[0].value.strip()

        if field_name == "noswitch":
            resp["switch_context"] = False
        if field_name == "context":
            resp["context"] = field_value
        if field_name == "link":
            resp["rel"] = field_value
        if field_name == "entity":
            resp["target"] = field_value
        if field_name == "pointer":
            resp["register_on_last_entity"] = True
        if field_name == "register":
            resp["register_relation_as_entity"] = True
    return resp


def run(config):
    """
    ~~Runner:Core~~
    :param config:
    :return:
    """

    # ~~->Config:Config~~
    type_source = config.get("types")
    terminals_source = config.get("terminals")

    try:
        # ~~->Types:Config~~
        valid_types = []
        if type_source is not None:
            with open(type_source, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                valid_types = [row[0] for row in reader]
        config["valid_types"] = valid_types

        # ~~->Terminals:Config~~
        terminal_entities = []
        if terminals_source is not None:
            with open(terminals_source, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                terminal_entities = [row[0] for row in reader]

        # ~~->Analysis:Model~~
        data = Analysis()
        data.terminals = terminal_entities

        # ~~->ParseTree:Core~~
        parse_tree(config, data)

        # ~~->Serialiser:Serialiser~~
        serialisers = config.get("serialisers", [])
        for serialiser in serialisers:
            klazz = plugin.load_class(serialiser.get("class"))
            inst = klazz(config, serialiser)
            inst.serialise(data)

    except MapException as e:
        # ~~-> MapException:Exception ~~
        print(str(e))
        exit(1)