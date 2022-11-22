# FeatureMap

For annotating text-based files with definitions and relationships to allow you to build a map of connections.

## Why

FeatureMap allows you to annotate software, and indeed any text-based files, and to extract
annotations into views that allow you to quickly see how parts of the software are
related to each other.  This then allows you to have a better understanding of the 
structure of your system, and to make more informed judgments about the impact of 
proposed changes.

FeatureMap differs from simple dependency analysis in that it is not constrained to 
creating a map of how functions within your software call each other.  It can work
across all document types, irrespective of language, and irrespective of whether they
are code files at all.  Provided the file is text-based then FeatureMap can be used.  This allows it to
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

Install system dependencies (for `yaml.CLoader`) e.g. for Ubuntu:

```
apt install libyaml-dev
```

Install the library into your (virtual) environment:

```
pip install -e .
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

An entity is any **thing**/**feature**/**behaviour** whatever, that you want to track,
which you identify in your source file via annotation.  By placing a name of an
entity in a source file anywhere at all (or even in multiple places), FeatureMap will
register that as an entity.  See below for how to identify an entity.


2. **Entity Names**

An entity is named in a well defined way:

```
[name]:[type]
```

Here the `[name]` is absolutely any alphanumeric string you like.

The `[type]` is a reference to the type of entity (also an alphanumeric string).  You can also make these up yourself as you
like (see next section for details).

Therefore your entity might have a names like:

* `Homepage:Page` - the homepage of your webapp, which is a kind of `Page`; you might put that in an HTML page or a page template
* `Login:Feature` - the login capability for your site, which is a kind of `Feature`; you might put that in the HTML page and/or in the handler for logins

2.1 **Entity Types**

As described above, entities must have a type.  You are free to invent whichever types 
work for your project.  If you wish you can register the types in the `types.csv`
file.  If you do that, and set FeatureMap to validate types (in `config.yml`), it will check that any
types it finds are registered.  This allows you to enforce a certain vocabulary and
ensures you are aware of any new types that creep into your annotations.

3 **Relationships**

Entities may be related to other entities.  This is done by specifying a relationship.

You can create whatever relationships you like.  FeatureMap also has a default special
relationship which simply means X "is related in a non-specific way to" Y.  This is the
`->` operator.  For example:

* `Homepage:Page -> Page:Page` - the homepage is related to the concept of a generic page
* `Login:Feature -> Logout:Feature` - the login feature is related in some way to the logout feature

If you wish to type these relationships you can do that instead:

* `Homepage:Page isA Page:Page` - the homepage is a kind of page
* `Login:Feature activates Logout:Feature` - the login feature activates the logout feature

For many basic purposes, knowing that a relationship exists is sufficient, and developers can infer
the relationship type from the code and their knowledge of the system.


## How to annotate your source

FeatureMap allows you to insert 4 different types of annotation into your source files:

1. **Identify an Entity**

Inserting the name of an entity and its type registers
that the entity exists, and sets the current **entity context** until the end of the current
file, or until a new entity context is defined.

```
# ~~Homepage:Page~~
```

This registers the `Homepage:Page` entity, and sets that as our context. Any context-free relationships declared
beneath this line will be attached to this entity.

2. **Assert a relationship from the current entity context to another entity**

Inserting a relationship to another entity when have an active entity context registers
a relationship on the entity context to the other entity.

```
# First set the entity context
# ~~Homepage:Page~~
#
# Then define a relationship
# ~~-> Login:Feature~~
```

This has now registered that `Homepage:Page` is related to `Login:Feature`

3. **Assert a relationship from the current entity context AND also assert that the related entity should be registered**

By default entities defined as the target of a relationship are not defined as entities *at that point*.  That is,
if you assert:

```
# ~~Homepage:Page~~
# ~~-> Login:Feature~~
```

This will register:

* `Homepage:Page` is an entity
* `Homepage:Page` is related to `Login:Feature`

It is up to you to define the entity `Login:Feature` elsewhere, e.g. in the handler that carries out your user
authentication.

If the `Login:Feature` is not defined meaningfully elsewhere, you may wish to say that at the point you
define the relationship, you also define the place at which the feature is defined.  In this case you can
use the `$` modifier to instruct FeatureMap to record the entity at this point:

```
# ~~Homepage:Page~~
# ~~->$ Login:Feature~~
```

This will register:

* `Homepage:Page` is an entity
* `Homepage:Page` is related to `Login:Feature`
* `Login:feature` is an entity defined at the same line as the relationship

4. **Identify an Entity and assert a relationship at the same time**

As a convenient shorthand, you can combine (1) and (2) above into a single command which
registers the entity, sets the entity context, and registers the relationship.

```
# ~~Homepage:Page->Login:Feature~~
```

Note that you *cannot* use the `$` modifier defined in (3) above at this point.

5. **Identify an Entity, assert a relationship, but do not switch entity context**

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

Note that you *cannot* use the `$` modifier defined in (3) above at this point.

6. **Define a relationship on the last registered entity, not the entity context**

If you define an entity in a relationship as per (3) you may also wish to give that entity some downstream
relationships of its own.

This is possible to do explicitly using the `!` operator:

```
# ~~Homepage:Page~~
# ~~->$ Login:Feature~~
# ~~!Login:Feature->Login:Page~~
```

But there is also a convenient short-hand for this using the `^` pointer, which tells FeatureMap
to assign the relationship to the last entity defined, rather than the current entity context.  The
above is equivalent to:

```
# ~~Homepage:Page~~
# ~~->$ Login:Feature~~
# ~~^->Login:Page~~
```

The `^` pointer will refer to the `Login:Feature` entity until the end of the file, or until another entity
is defined in a relationship with the `$` operator.
