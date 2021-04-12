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
in documentation, deployment scripts, configuration, etc.

## Getting Started

### Show me it

This repository is fully annotated using FeatureMap, so you can quickly see what the 
annotations and the output of a FeatureMap report look like.

[Look at our core.py source file](https://github.com/CottageLabs/FeatureMap/blob/main/featuremap/core.py)

Throughout that file you will see annotations like

```
~~ParseTree:Core~~
```

later followed by

```
# ~~-> Config:Config~~
```

These are all in python line comments next to the code most relevant to the entity or relationship being
defined.

When FeatureMap is run against the code it will extract those to a report that allows you to explore the
structure of your code:

[See the FeatureMap's FeatureMap!](https://cottagelabs.github.io/FeatureMap/map/html/relationships.html)


### Show me it on my machine

Clone this repo:

```
git clone git@github.com:CottageLabs/FeatureMap.git
```

Install the library into your (virtual environment):

```
pip install -r requirements.txt
```

Go into the `FeatureMap` root directory and run:

```
featuremap -c .featuremap/config.yml
```

That will re-generate the FeatureMap into the `docs/map` directory.

Open one of the report pages in your favourite browser.  You will find, for example, the relationships report here:

```
docs/map/html/relationships.html
```

## Key concepts

1. **Entities**

An entity is any **thing** which you identify in your source file.  By placing a name of an
entity in a source file anywhere at all (or even in multiple plates), FeatureMapw will
regiser that as an entity.  See below for how to identify an entity.


2. **Entity Names**

An entity is named in a well defined way:

```
[name]:[type]
```

Here the `[name]` is absolutely any string you like, provided it does not contain any spaces and
does not contain the character `:`.

The `[type]` is a reference to the type of entity.  You can also make these up yourself as you
like (see next section for details).

Therefore your entity might have a names like:

* Homepage:Page - the homepage of your webapp, which is a kind of `Page`
* Login:Feature - the login capability for your site, which is a kind of `Feature`

3. **Entity Types**

As described above, entities must have a type.  You are free to invent whichever types 
work for your project.  If you wish you can register the types in the `.featuremap/types.csv`
file.  If you do that, and set FeatureMap to validate types, it will check that any
types it finds are registered.  This allows you to enforce a certain vocabulary and
ensures you are aware of any new types that creep into your annotations.

4. **Relationships**

Entities may be related to other entities.  This is done by specifying a relationship.

You can create whatever relationships you like.  FeatureMap also has a default special
relationship which simply means X "is related in a non-specific way to" Y.  This is the
`->` operator.  For example:

* `Homepage:Page -> Page:Page` - the homepage is related to the concept of a generic page
* `Login:Feature -> Logout:Feature` - the login feature is related in some way to the logout feature

If you wish to type these relationships you can do that instead:

* `Homepage:Page isA Page:Page` - the homepage is a kind of page
* `Login:Feature activates Logout:Feature` - the login feature activates the logout feature

Note that if you introduce your own relationship types you need to maintain them.  For many
basic purposes, knowing that a relationship exists is sufficient, and developers can infer
the relationship type from the code and their knowledge of the system.


## How to annotate your source

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

