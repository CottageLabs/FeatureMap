# ~~Parser:Core -> Lark:Tech~~

from lark import Lark

parser = Lark("""
start: noswitch? context (link entity)?
       | pointer? link register? entity

context: ENTITY
link: LINK
entity: ENTITY
noswitch: NOSWITCH
register: REGISTER
pointer: POINTER

%ignore " "
LINK: "->"
    | SYMBOL
ENTITY: SYMBOL ":" SYMBOL
NOSWITCH: "!"
REGISTER: "$"
POINTER: "^"

LOWER: ("a".."z")
UPPER: ("A".."Z")
NUMBER: ("0".."9")
SYMBOL: (LOWER | UPPER | NUMBER)+
""")


"""
Various examples.  Experment with these at https://lark-parser.github.io/lark/ide/app.html

1. Define an entity context: 

Thing:Feature

2. Define a link to another entity

->Thing:Feature
isA Thing:Feature

3. Define a link to another entity, and also register it as an entity

->$ Thing:Feature
isA $Thing:Feature

4. Define an entity context and also link to another entity at the same time

Thing:Feature -> Other:Whatsit
Thing:Feature isA Other:Whatsit

5. Define an entity and a relationship, but don't switch context

!Thing:Feature -> Other:Whatsit
!Thing:Feature isA Other:Whatsit

6. Define a relationship on the last registered entity rather than the current context

^-> Thing:Feature
^isA Thing:Feature
^->$ Thing:Feature

"""