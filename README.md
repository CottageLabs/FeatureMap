# FeatureMap

For annotating text files with features and their connections to other features.

## Why

FeatureMap allows you to annotate software, and indeed any text files, and to extract
annotations into views that allow you to quickly see how parts of the software are
related to each other.  This then allows you to have a better understanding of the 
structure of your system, and to make more informed judgments about the impact of 
proposed changes.

FeatureMap differs from simple dependency analysis in that it is not constrained to 
creating a map of how functions within your software call each other.  It can work
across all document types, irrespective of language, and irrespective of whether they
are code files at all.  Provided the file is plain text, and in the case of a code file
has some form of comment syntax, then FeatureMap can be used.  This allows it to 
provide a view across all source files of all different languages, as well as bringing
in documentation, deployment scripts, etc.

## How

FeatureMap allows you to insert 4 different types of annotation into your source files:

1. **Identify an Entity**

Inserting the name of an entity and its type (see below for more details), registers
that the entity exists, and sets the current entity context until the end of the current
file

```
# ~~Homepage:Page~~
```

2. **Assert a relationship from the current entity context to another entity**

Inserting a relationship to another entity when you are in an entity context registers
a relationship from the current entity context to that other entity.  If the other entity
has not already been registered, it will be registered at this point.

```
# First set the entity context
# ~~Homepage:Page~~
#
# Then define a relationship
# ~~-> Login:Feature~~

```

Here we use `->` as the relationship, but you can use any string, which means you can type
the relationships if you wish.

This has now registered that `Homepage:Page` is related to `Login:Feature`

3. **Identify an Entity and assert a relationship at the same time**

As a convenient shorthand, you can combine (1) and (2) above into a single command which
registers the entity, sets the entity context, and registers the relationship.

```
# ~~Homepage:Page->Login:Feature~~
```

4. **Identify an Entity, assert a relationship, but do not switch entity context**

If you wish to assert an arbitrary relationship between two entities at any point (for example, it makes
sense to do so because of a particular code snippet in the file), you can do so without switching
the entity context by prefixing with `!`

```
# Set the current entity context
# ~~Homepage:Page~~
#
# Declare a relationship without switching context
# ~~!Login:Feature->Login:Page~~
```

